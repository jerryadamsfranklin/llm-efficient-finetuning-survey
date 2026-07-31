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
    RAW_ROOT,
    append_search_log,
    iter_s2_queries,
    load_local_env,
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


def run_backfill(
    data: dict[str, Any],
    session: requests.Session,
    *,
    force: bool,
    only_block: str | None = None,
    only_slice: str | None = None,
) -> int:
    """Protocol v1.3: date-sliced re-run of every s2_query for the confirmation band.

    v1.2 queried Semantic Scholar once per query with a 200-record cap and no slicing;
    17 of 18 queries saturated that cap and returned only 3.5% pre-2022 records. Slicing
    by year gives each year its own cap, which is the rule v1.1 already applied to arXiv.
    """
    meta = data["meta"]
    slices = [str(s) for s in meta.get("s2_backfill_slices") or []]
    if not slices:
        print("no s2_backfill_slices in queries.yaml (expected under protocol v1.3)", file=sys.stderr)
        return 1
    max_results = int(meta["max_results_per_query"])
    out_root = RAW_ROOT / "semanticscholar_backfill"
    print(f"v1.3 backfill: slices={slices}, cap={max_results}/query/slice -> {out_root}\n", flush=True)

    for block_id, _name, q_idx, query in iter_s2_queries(data):
        if only_block and block_id != only_block:
            continue
        for year in slices:
            if only_slice and year != only_slice:
                continue
            out = raw_path("semanticscholar_backfill", block_id, q_idx, slice_id=year, root=RAW_ROOT)
            if out.exists() and not force:
                print(f"skip existing {out.name}")
                continue
            print(f"backfill {block_id} q{q_idx} {year}: {query}", flush=True)
            try:
                payload = fetch_s2(
                    query,
                    year_start=int(year),
                    year_end=int(year),
                    max_results=max_results,
                    session=session,
                )
            except (requests.RequestException, RuntimeError) as exc:
                print(f"  ERROR: {exc}", flush=True)
                time.sleep(INTER_REQUEST_SEC)
                continue
            payload["protocol_version"] = "1.3"
            payload["protocol_query"] = query
            payload["query_form"] = "s2_keyword_variant"
            payload["run_type"] = "confirmation_band_backfill"
            payload["slice"] = year

            notes = (
                "protocol=1.3 confirmation-band backfill; s2_keyword_variant; "
                f"year slice {year}; API totalReported={payload['total_results_reported']}"
            )
            if payload.get("hit_result_cap"):
                notes += f"; HIT_CAP={max_results}"
            if payload.get("warnings"):
                notes += "; " + "; ".join(payload["warnings"])
            if payload["returned"] == 0 and payload.get("warnings"):
                print(f"  no usable results ({notes}); will retry later", flush=True)
                time.sleep(120)
                continue
            save_json(out, payload)
            append_search_log(
                source="semanticscholar_backfill",
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=payload["returned"],
                notes=notes,
                slice_id=year,
            )
            print(f"  saved {out.name}: {payload['returned']} papers", flush=True)
            time.sleep(INTER_REQUEST_SEC)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Semantic Scholar searches.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--block", help="Only run this block id.")
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Protocol v1.3: date-sliced re-run for the 2019-2021 confirmation band.",
    )
    parser.add_argument("--slice", help="With --backfill: only this year slice.")
    args = parser.parse_args()

    data = load_queries()
    meta = data["meta"]
    year_start = int(meta["date_start"][:4])
    year_end = int(meta["date_end"][:4])
    max_results = int(meta["max_results_per_query"])

    load_local_env()
    session = requests.Session()
    headers = {"User-Agent": "llm-efficient-finetuning-survey/0.1 (research)"}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
        print("using SEMANTIC_SCHOLAR_API_KEY from environment", flush=True)
    else:
        print("WARNING: no SEMANTIC_SCHOLAR_API_KEY; expect heavy 429 throttling", flush=True)
    session.headers.update(headers)

    if args.backfill:
        return run_backfill(
            data, session, force=args.force, only_block=args.block, only_slice=args.slice
        )

    for block_id, _name, q_idx, query in iter_s2_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path("semanticscholar", block_id, q_idx)
        if out.exists() and not args.force:
            try:
                existing = json.loads(out.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                existing = {}
            if existing.get("returned", 0) > 0 and existing.get("protocol_version") == "1.1":
                print(f"skip existing {out.name}")
                continue
            print(f"re-run (v1.1 s2_queries) {out.name}", flush=True)

        print(f"semanticscholar {block_id} q{q_idx}: {query}", flush=True)
        try:
            payload = fetch_s2(
                query,
                year_start=year_start,
                year_end=year_end,
                max_results=max_results,
                session=session,
            )
            payload["protocol_version"] = "1.1"
            payload["protocol_query"] = query
            payload["query_form"] = "s2_keyword_variant"
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

        notes = (
            "protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, "
            "not identical string); "
            f"API totalReported={payload['total_results_reported']}"
        )
        if payload.get("hit_result_cap"):
            notes += f"; HIT_CAP={max_results}"
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
