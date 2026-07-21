#!/usr/bin/env python3
"""Search Semantic Scholar Graph API for protocol queries (Phase 2).

Saves raw JSON under search/raw/semanticscholar/ and appends search/search-log.md.
Uses citationCount for later community-adoption screening.
Backoff on HTTP 429. Optional SEMANTIC_SCHOLAR_API_KEY env var raises limits.
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
    load_queries,
    raw_path,
    save_json,
    utc_now_iso,
)

S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "title,authors,year,venue,citationCount,externalIds,abstract,openAccessPdf"
# Unauthenticated soft limit is roughly 100 req / 5 min; pace accordingly.
INTER_REQUEST_SEC = 3.5


def fetch_s2(
    query: str,
    *,
    year_start: int,
    year_end: int,
    max_results: int,
    session: requests.Session,
) -> dict[str, Any]:
    papers: list[dict[str, Any]] = []
    offset = 0
    limit = min(100, max_results)
    total = None
    warnings: list[str] = []

    while len(papers) < max_results:
        params = {
            "query": query,
            "year": f"{year_start}-{year_end}",
            "fields": FIELDS,
            "limit": min(limit, max_results - len(papers)),
            "offset": offset,
        }
        data = None
        for attempt in range(6):
            try:
                resp = session.get(S2_API, params=params, timeout=45)
            except requests.RequestException as exc:
                wait = min(45, 3 * (attempt + 1))
                print(f"  network error ({exc}); sleep {wait}s", flush=True)
                time.sleep(wait)
                continue
            if resp.status_code == 429:
                wait = min(90, 5 * (2 ** attempt))
                print(f"  429 rate limit; sleeping {wait}s", flush=True)
                time.sleep(wait)
                continue
            if resp.status_code >= 500:
                wait = min(45, 5 * (attempt + 1))
                print(f"  HTTP {resp.status_code}; sleep {wait}s", flush=True)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            break
        if data is None:
            warnings.append("stopped early after repeated rate limits / errors")
            break

        total = data.get("total", total)
        batch = data.get("data") or []
        papers.extend(batch)
        print(f"  got {len(batch)} (cum {len(papers)}; totalReported={total})", flush=True)
        if not batch:
            break
        offset += len(batch)
        if offset >= (total or 0):
            break
        time.sleep(INTER_REQUEST_SEC)

    return {
        "source": "semanticscholar",
        "api": S2_API,
        "query": query,
        "year": f"{year_start}-{year_end}",
        "fields": FIELDS,
        "fetched_at": utc_now_iso(),
        "total_results_reported": total,
        "returned": len(papers[:max_results]),
        "hit_result_cap": len(papers) >= max_results,
        "warnings": warnings,
        "papers": papers[:max_results],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Semantic Scholar searches.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--block", help="Only run this block id.")
    args = parser.parse_args()

    data = load_queries()
    meta = data["meta"]
    year_start = int(meta["date_start"][:4])
    year_end = int(meta["date_end"][:4])
    max_results = int(meta["max_results_per_query"])

    session = requests.Session()
    headers = {"User-Agent": "llm-efficient-finetuning-survey/0.1 (research)"}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
    session.headers.update(headers)

    for block_id, _name, q_idx, query in iter_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path("semanticscholar", block_id, q_idx)
        if out.exists() and not args.force:
            try:
                existing = json.loads(out.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                existing = {}
            if existing.get("returned", 0) > 0:
                print(f"skip existing {out.name}")
                continue
            print(f"retry empty {out.name}", flush=True)

        print(f"semanticscholar {block_id} q{q_idx}: {query}", flush=True)
        try:
            payload = fetch_s2(
                query,
                year_start=year_start,
                year_end=year_end,
                max_results=max_results,
                session=session,
            )
            payload["protocol_query"] = query
        except (requests.RequestException, RuntimeError) as exc:
            print(f"  ERROR: {exc}", flush=True)
            append_search_log(
                source="semanticscholar",
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=0,
                notes=f"Request failed: {exc}",
            )
            time.sleep(INTER_REQUEST_SEC)
            continue

        notes = f"API totalReported={payload['total_results_reported']}"
        if payload.get("hit_result_cap"):
            notes += f"; HIT_CAP={max_results} — consider narrowing this query"
        if payload.get("warnings"):
            notes += "; " + "; ".join(payload["warnings"])
        # Do not persist empty rate-limited failures — allows clean resume.
        if payload["returned"] == 0 and payload.get("warnings"):
            print(f"  no usable results ({notes}); will retry later", flush=True)
            time.sleep(120)
            continue
        save_json(out, payload)
        append_search_log(
            source="semanticscholar",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=payload["returned"],
            notes=notes,
        )
        print(f"  saved {out.name}: {payload['returned']} papers", flush=True)
        time.sleep(INTER_REQUEST_SEC)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
