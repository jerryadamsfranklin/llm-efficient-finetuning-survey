#!/usr/bin/env python3
"""IEEE Xplore Metadata API search (Protocol v1.2).

Enforces the 50-record relevance cap at request time (max_records=50).
Requires IEEE_API_KEY (local.env or environment). Never commits the key.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import (  # noqa: E402
    append_search_log,
    iter_queries,
    load_local_env,
    load_queries,
    raw_path,
    save_json,
    utc_now_iso,
)

IEEE_API = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
CAP = 50
INTER_REQUEST_SEC = 1.0


def _redact(text: str, api_key: str) -> str:
    out = text
    if api_key:
        out = out.replace(api_key, "REDACTED")
    return out


def _safe_exc(exc: BaseException, api_key: str) -> str:
    return _redact(str(exc), api_key)


class IeeeAuthError(RuntimeError):
    """API key present but developer account / product not activated."""


def fetch_ieee(
    query: str,
    *,
    api_key: str,
    start_year: int,
    end_year: int,
    session: requests.Session,
) -> dict[str, Any]:
    """Request at most CAP records. Prefer sort_field=relevance per v1.2; fall back if rejected."""
    base_params = {
        "apikey": api_key,
        "querytext": query,
        "start_year": start_year,
        "end_year": end_year,
        "max_records": CAP,
        "start_record": 1,
        "format": "json",
    }
    sort_notes: list[str] = []
    data: dict[str, Any] | None = None
    used_params = dict(base_params)

    for sort_attempt in ("relevance", None):
        params = dict(base_params)
        if sort_attempt:
            params["sort_field"] = sort_attempt
        used_params = params
        for attempt in range(5):
            try:
                resp = session.get(IEEE_API, params=params, timeout=60)
            except requests.RequestException as exc:
                wait = min(30, 3 * (attempt + 1))
                print(f"  network error ({_safe_exc(exc, api_key)}); sleep {wait}s", flush=True)
                time.sleep(wait)
                continue
            if resp.status_code == 429:
                wait = min(60, 5 * (2 ** attempt))
                print(f"  429 rate limit; sleep {wait}s", flush=True)
                time.sleep(wait)
                continue
            if resp.status_code >= 500:
                wait = min(30, 5 * (attempt + 1))
                print(f"  HTTP {resp.status_code}; sleep {wait}s", flush=True)
                time.sleep(wait)
                continue
            if resp.status_code >= 400:
                body = _redact((resp.text or "")[:300], api_key)
                if "Developer Inactive" in body or resp.status_code == 403:
                    raise IeeeAuthError(
                        "IEEE API returned 403 Developer Inactive. On developer.ieee.org: "
                        "confirm your account is active, subscribe/approve the Metadata API "
                        "product for this key, then re-run. If activation is denied, fall back "
                        "to manual IEEE search per protocol v1.2."
                    )
                if sort_attempt == "relevance":
                    sort_notes.append(
                        "sort_field=relevance rejected by API; retrying without sort_field "
                        f"(HTTP {resp.status_code})"
                    )
                    print(f"  {sort_notes[-1]}: {body}", flush=True)
                    break
                raise RuntimeError(f"IEEE HTTP {resp.status_code}: {body}")
            data = resp.json()
            if sort_attempt:
                sort_notes.append("sort_field=relevance requested")
            else:
                sort_notes.append(
                    "default API ranking (no sort_field); docs list title/number sorts only"
                )
            break
        if data is not None:
            break

    if data is None:
        raise RuntimeError("IEEE API request failed after retries")

    articles = data.get("articles") or []
    total = data.get("total_records")
    if total is None:
        total = data.get("totalfound")
    returned = len(articles[:CAP])
    return {
        "source": "ieee",
        "api": IEEE_API,
        "protocol_version": "1.2",
        "query": query,
        "query_form": "boolean",
        "start_year": start_year,
        "end_year": end_year,
        "max_records_requested": CAP,
        "cap_enforced_at_request": True,
        "sort_notes": sort_notes,
        "request_params_sans_key": {
            k: v for k, v in used_params.items() if k != "apikey"
        },
        "fetched_at": utc_now_iso(),
        "total_results_reported": total,
        "returned": returned,
        "hit_result_cap": returned >= CAP,
        "articles": articles[:CAP],
        "raw_meta": {
            k: data.get(k)
            for k in (
                "total_records",
                "totalfound",
                "total_searched",
                "start_record",
                "end_record",
            )
            if k in data
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run IEEE Xplore metadata searches (v1.2).")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--block", help="Only run this block id.")
    args = parser.parse_args()

    load_local_env()
    api_key = (os.environ.get("IEEE_API_KEY") or "").strip()
    if not api_key:
        msg = (
            "ERROR: IEEE_API_KEY not set. Register at https://developer.ieee.org, "
            "add the key to local.env as IEEE_API_KEY=..., then re-run. "
            "Per protocol v1.2 do not silently skip IEEE — fall back to manual if key denied."
        )
        print(msg, file=sys.stderr)
        return 2

    data = load_queries()
    meta = data["meta"]
    start_year = int(meta["date_start"][:4])
    end_year = int(meta["date_end"][:4])
    cap = int(meta.get("substituted_source_cap") or meta.get("manual_relevance_cap") or CAP)
    if cap != CAP:
        print(f"WARNING: using meta cap={cap} (expected {CAP})", flush=True)

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "llm-efficient-finetuning-survey/0.2 (research; protocol v1.2)"}
    )

    for block_id, _name, q_idx, query in iter_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path("ieee", block_id, q_idx)
        if out.exists() and not args.force:
            try:
                existing = json.loads(out.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                existing = {}
            if existing.get("protocol_version") == "1.2" and existing.get("returned", 0) >= 0:
                if existing.get("articles") is not None:
                    print(f"skip existing {out.name}")
                    continue

        print(f"ieee {block_id} q{q_idx}: {query}", flush=True)
        try:
            payload = fetch_ieee(
                query,
                api_key=api_key,
                start_year=start_year,
                end_year=end_year,
                session=session,
            )
            # honor configured cap if meta differs
            payload["max_records_requested"] = cap
            payload["articles"] = (payload.get("articles") or [])[:cap]
            payload["returned"] = len(payload["articles"])
            payload["hit_result_cap"] = payload["returned"] >= cap
        except IeeeAuthError as exc:
            print(f"  AUTH ERROR: {exc}", flush=True)
            append_search_log(
                source="ieee",
                block_id="AUTH",
                query_index=0,
                query="(blocked)",
                n_results=0,
                notes=str(exc),
            )
            return 3
        except (requests.RequestException, RuntimeError, ValueError) as exc:
            print(f"  ERROR: {_safe_exc(exc, api_key)}", flush=True)
            append_search_log(
                source="ieee",
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=0,
                notes=f"Request failed: {_safe_exc(exc, api_key)}",
            )
            time.sleep(INTER_REQUEST_SEC)
            continue

        notes = (
            f"protocol=1.2; boolean query; max_records={cap} requested (cap at request time); "
            f"API totalReported={payload['total_results_reported']}; "
            + "; ".join(payload.get("sort_notes") or [])
        )
        if payload.get("hit_result_cap"):
            notes += f"; HIT_CAP={cap}"
        save_json(out, payload)
        append_search_log(
            source="ieee",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=payload["returned"],
            notes=notes,
        )
        print(f"  saved {out.name}: {payload['returned']} articles", flush=True)
        time.sleep(INTER_REQUEST_SEC)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
