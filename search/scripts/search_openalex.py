#!/usr/bin/env python3
"""OpenAlex works search (Protocol v1.2).

General index and optional ACM publisher-filtered run. Cap: per_page=50,
sort=relevance_score:desc. Uses s2_queries keyword variants.
"""

from __future__ import annotations

import argparse
import json
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
    iter_s2_queries,
    load_queries,
    raw_path,
    save_json,
    utc_now_iso,
)

OPENALEX_API = "https://api.openalex.org/works"
CAP = 50
INTER_REQUEST_SEC = 0.2  # polite pool with mailto
DEFAULT_MAILTO = "jerry.adamsf@gmail.com"
# Documented in amendment; verified at run time via /publishers
DEFAULT_ACM_PUBLISHER = "P4310319798"


def verify_acm_publisher(session: requests.Session, publisher_id: str, mailto: str) -> dict[str, Any]:
    url = f"https://api.openalex.org/publishers/{publisher_id}"
    resp = session.get(url, params={"mailto": mailto}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    display = data.get("display_name") or ""
    return {
        "id": publisher_id,
        "display_name": display,
        "ids": data.get("ids"),
        "works_count": data.get("works_count"),
        "verified_ok": "association for computing machinery" in display.lower()
        or display.upper() == "ACM"
        or "acm" in display.lower(),
    }


def fetch_openalex(
    query: str,
    *,
    date_start: str,
    date_end: str,
    mailto: str,
    session: requests.Session,
    publisher_lineage: str | None = None,
) -> dict[str, Any]:
    filters = [
        f"from_publication_date:{date_start}",
        f"to_publication_date:{date_end}",
    ]
    if publisher_lineage:
        filters.append(f"primary_location.source.publisher_lineage:{publisher_lineage}")
    params = {
        "search": query,
        "filter": ",".join(filters),
        "per_page": CAP,
        "sort": "relevance_score:desc",
        "mailto": mailto,
    }
    data = None
    for attempt in range(5):
        try:
            resp = session.get(OPENALEX_API, params=params, timeout=60)
        except requests.RequestException as exc:
            wait = min(30, 3 * (attempt + 1))
            print(f"  network error ({exc}); sleep {wait}s", flush=True)
            time.sleep(wait)
            continue
        if resp.status_code == 429:
            wait = min(60, 5 * (2 ** attempt))
            print(f"  429; sleep {wait}s", flush=True)
            time.sleep(wait)
            continue
        if resp.status_code >= 500:
            wait = min(30, 5 * (attempt + 1))
            print(f"  HTTP {resp.status_code}; sleep {wait}s", flush=True)
            time.sleep(wait)
            continue
        resp.raise_for_status()
        data = resp.json()
        break
    if data is None:
        raise RuntimeError("OpenAlex request failed after retries")

    results = data.get("results") or []
    meta = data.get("meta") or {}
    total = meta.get("count")
    returned = len(results[:CAP])
    source_name = "openalex_acm" if publisher_lineage else "openalex"
    return {
        "source": source_name,
        "api": OPENALEX_API,
        "protocol_version": "1.2",
        "query": query,
        "query_form": "s2_keyword_variant",
        "filter": params["filter"],
        "per_page_requested": CAP,
        "cap_enforced_at_request": True,
        "sort": "relevance_score:desc",
        "mailto": mailto,
        "publisher_lineage": publisher_lineage,
        "fetched_at": utc_now_iso(),
        "total_results_reported": total,
        "returned": returned,
        "hit_result_cap": returned >= CAP,
        "results": results[:CAP],
        "meta": meta,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run OpenAlex searches (v1.2).")
    parser.add_argument(
        "--acm",
        action="store_true",
        help="Filter to ACM publisher lineage (openalex_acm output dir).",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--block", help="Only run this block id.")
    args = parser.parse_args()

    data = load_queries()
    meta = data["meta"]
    date_start = meta["date_start"]
    date_end = meta["date_end"]
    mailto = meta.get("openalex_mailto") or DEFAULT_MAILTO
    acm_id = meta.get("openalex_acm_publisher_id") or DEFAULT_ACM_PUBLISHER
    cap = int(meta.get("substituted_source_cap") or meta.get("manual_relevance_cap") or CAP)

    session = requests.Session()
    session.headers.update(
        {"User-Agent": f"llm-efficient-finetuning-survey/0.2 (mailto:{mailto})"}
    )

    publisher = None
    source_dir = "openalex"
    log_source = "openalex"
    if args.acm:
        print(f"Verifying ACM publisher id {acm_id}…", flush=True)
        verified = verify_acm_publisher(session, acm_id, mailto)
        print(f"  OpenAlex publisher: {verified}", flush=True)
        if not verified.get("verified_ok"):
            print(
                "ERROR: publisher id does not look like ACM; aborting ACM run. "
                "Update openalex_acm_publisher_id in queries.yaml after checking OpenAlex.",
                file=sys.stderr,
            )
            return 2
        publisher = acm_id
        source_dir = "openalex_acm"
        log_source = "openalex_acm"

    for block_id, _name, q_idx, query in iter_s2_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path(source_dir, block_id, q_idx)
        if out.exists() and not args.force:
            try:
                existing = json.loads(out.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                existing = {}
            if existing.get("protocol_version") == "1.2" and existing.get("results") is not None:
                print(f"skip existing {out.name}")
                continue

        print(f"{log_source} {block_id} q{q_idx}: {query}", flush=True)
        try:
            payload = fetch_openalex(
                query,
                date_start=date_start,
                date_end=date_end,
                mailto=mailto,
                session=session,
                publisher_lineage=publisher,
            )
            payload["results"] = (payload.get("results") or [])[:cap]
            payload["returned"] = len(payload["results"])
            payload["per_page_requested"] = cap
            payload["hit_result_cap"] = payload["returned"] >= cap
            if args.acm:
                payload["acm_publisher_verified"] = True
                payload["acm_publisher_id"] = acm_id
        except (requests.RequestException, RuntimeError) as exc:
            print(f"  ERROR: {exc}", flush=True)
            append_search_log(
                source=log_source,
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=0,
                notes=f"Request failed: {exc}",
            )
            time.sleep(INTER_REQUEST_SEC)
            continue

        notes = (
            f"protocol=1.2; s2_keyword_variant (not boolean); "
            f"per_page={cap} requested (cap at request time); "
            f"sort=relevance_score:desc; "
            f"API totalReported={payload['total_results_reported']}"
        )
        if args.acm:
            notes += f"; ACM publisher_lineage={acm_id}"
        if payload.get("hit_result_cap"):
            notes += f"; HIT_CAP={cap}"
        save_json(out, payload)
        append_search_log(
            source=log_source,
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=payload["returned"],
            notes=notes,
        )
        print(f"  saved {out.name}: {payload['returned']} works", flush=True)
        time.sleep(INTER_REQUEST_SEC)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
