#!/usr/bin/env python3
"""DBLP publication search (Protocol v1.2, optional completeness).

Adopted for CS venue-string quality. Cap: h=50. Uses s2_queries keywords.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import (  # noqa: E402
    append_search_log,
    iter_s2_queries,
    load_queries,
    raw_path,
    save_json,
    utc_now_iso,
)

DBLP_API = "https://dblp.org/search/publ/api"
CAP = 50
INTER_REQUEST_SEC = 3.0
REQUEST_TIMEOUT = 90


def _year_in_window(year: Any, start: int, end: int) -> bool:
    try:
        y = int(str(year)[:4])
    except (TypeError, ValueError):
        return True  # keep if unknown; screening will decide
    return start <= y <= end


def fetch_dblp(
    query: str,
    *,
    year_start: int,
    year_end: int,
    session: requests.Session,
) -> dict[str, Any]:
    params = {
        "q": query,
        "h": CAP,
        "format": "json",
    }
    data = None
    for attempt in range(5):
        try:
            resp = session.get(DBLP_API, params=params, timeout=REQUEST_TIMEOUT)
        except requests.RequestException as exc:
            wait = min(90, 10 * (attempt + 1))
            print(f"  network error ({exc}); sleep {wait}s", flush=True)
            time.sleep(wait)
            continue
        if resp.status_code == 429:
            wait = min(180, 20 * (2 ** attempt))
            print(f"  429; sleep {wait}s", flush=True)
            time.sleep(wait)
            continue
        if resp.status_code == 503:
            wait = min(180, 30 * (attempt + 1))
            print(f"  503; sleep {wait}s", flush=True)
            time.sleep(wait)
            continue
        if resp.status_code >= 500:
            wait = min(90, 10 * (attempt + 1))
            print(f"  HTTP {resp.status_code}; sleep {wait}s", flush=True)
            time.sleep(wait)
            continue
        resp.raise_for_status()
        data = resp.json()
        break
    if data is None:
        raise RuntimeError("DBLP request failed after retries")

    hit = (data.get("result") or {}).get("hits") or {}
    total = hit.get("@total")
    hits = hit.get("hit") or []
    if isinstance(hits, dict):
        hits = [hits]
    # DBLP has no year filter param; post-filter for logging transparency but
    # keep request cap at 50 (do not request more than CAP).
    in_window = []
    for h in hits[:CAP]:
        info = h.get("info") or {}
        if _year_in_window(info.get("year"), year_start, year_end):
            in_window.append(h)
    returned = len(hits[:CAP])
    return {
        "source": "dblp",
        "api": DBLP_API,
        "protocol_version": "1.2",
        "query": query,
        "query_form": "s2_keyword_variant",
        "h_requested": CAP,
        "cap_enforced_at_request": True,
        "year_window": f"{year_start}-{year_end}",
        "fetched_at": utc_now_iso(),
        "total_results_reported": int(total) if total is not None else None,
        "returned": returned,
        "returned_in_coverage_window": len(in_window),
        "hit_result_cap": returned >= CAP,
        "hits": hits[:CAP],
        "hits_in_coverage_window": in_window,
        "request_url_example": f"{DBLP_API}?q={quote(query)}&h={CAP}&format=json",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run DBLP searches (v1.2, adopted).")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--block", help="Only run this block id.")
    args = parser.parse_args()

    data = load_queries()
    meta = data["meta"]
    year_start = int(meta["date_start"][:4])
    year_end = int(meta["date_end"][:4])
    cap = int(meta.get("substituted_source_cap") or meta.get("manual_relevance_cap") or CAP)

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "llm-efficient-finetuning-survey/0.2 (research; protocol v1.2)"}
    )

    # Adoption note once per run
    append_search_log(
        source="dblp",
        block_id="ADOPTION",
        query_index=0,
        query="(meta)",
        n_results=0,
        notes=(
            "protocol=1.2; DBLP ADOPTED as optional CS-venue completeness check; "
            f"h={cap} cap at request time; uses s2_queries keyword variants"
        ),
    )

    for block_id, _name, q_idx, query in iter_s2_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path("dblp", block_id, q_idx)
        if out.exists() and not args.force:
            try:
                existing = json.loads(out.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                existing = {}
            # Re-try zero-result files: DBLP often returns empty payloads under rate pressure.
            if (
                existing.get("protocol_version") == "1.2"
                and existing.get("hits") is not None
                and int(existing.get("returned") or 0) > 0
            ):
                print(f"skip existing {out.name}")
                continue
            if int(existing.get("returned") or 0) == 0:
                print(f"re-try empty {out.name}", flush=True)

        print(f"dblp {block_id} q{q_idx}: {query}", flush=True)
        try:
            payload = fetch_dblp(
                query,
                year_start=year_start,
                year_end=year_end,
                session=session,
            )
            payload["hits"] = (payload.get("hits") or [])[:cap]
            payload["returned"] = len(payload["hits"])
            payload["h_requested"] = cap
            payload["hit_result_cap"] = payload["returned"] >= cap
        except (requests.RequestException, RuntimeError) as exc:
            print(f"  ERROR: {exc}", flush=True)
            append_search_log(
                source="dblp",
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=0,
                notes=f"Request failed: {exc}",
            )
            time.sleep(INTER_REQUEST_SEC)
            continue

        notes = (
            f"protocol=1.2; s2_keyword_variant; h={cap} requested (cap at request time); "
            f"API totalReported={payload['total_results_reported']}; "
            f"in_coverage_window={payload['returned_in_coverage_window']} "
            f"(DBLP has no server-side year filter; window applied post-hoc for notes only)"
        )
        if payload.get("hit_result_cap"):
            notes += f"; HIT_CAP={cap}"
        save_json(out, payload)
        append_search_log(
            source="dblp",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=payload["returned"],
            notes=notes,
        )
        print(
            f"  saved {out.name}: {payload['returned']} hits "
            f"({payload['returned_in_coverage_window']} in window)",
            flush=True,
        )
        time.sleep(INTER_REQUEST_SEC)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
