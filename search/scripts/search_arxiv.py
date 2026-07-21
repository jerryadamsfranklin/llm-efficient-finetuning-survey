#!/usr/bin/env python3
"""Search arXiv API for protocol queries (Phase 2).

Reads search/queries.yaml, applies the coverage window and cs category filter,
saves raw JSON under search/raw/arxiv/, and appends search/search-log.md.

Rate limit: >= 3 seconds between requests.
Re-runnable: skips queries whose deterministic raw file already exists
(unless --force).
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
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

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_NS = {"arxiv": "http://arxiv.org/schemas/atom"}
ARXIV_API = "http://export.arxiv.org/api/query"
MIN_INTERVAL_SEC = 3.0


def _parse_date(d: str) -> datetime:
    return datetime.strptime(d, "%Y-%m-%d")


def build_arxiv_search_query(
    user_query: str,
    categories: list[str],
    date_start: str,
    date_end: str,
) -> str:
    """Translate a protocol query into an arXiv search with cats + submittedDate window."""
    q = user_query.strip()
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    # arXiv submittedDate compact form: YYYYMMDDHHMM
    start = date_start.replace("-", "") + "0000"
    end = date_end.replace("-", "") + "2359"
    date_clause = f"submittedDate:[{start} TO {end}]"
    return f"({q}) AND ({cat_clause}) AND {date_clause}"


def entry_to_dict(entry: ET.Element) -> dict[str, Any]:
    def text(tag: str) -> str:
        el = entry.find(f"atom:{tag}", ATOM_NS)
        return (el.text or "").strip() if el is not None else ""

    authors = [
        (a.find("atom:name", ATOM_NS).text or "").strip()
        for a in entry.findall("atom:author", ATOM_NS)
        if a.find("atom:name", ATOM_NS) is not None
    ]
    cats = [
        c.attrib.get("term", "")
        for c in entry.findall("atom:category", ATOM_NS)
    ]
    arxiv_id = text("id").rsplit("/", 1)[-1]
    return {
        "id": text("id"),
        "arxiv_id": arxiv_id,
        "title": " ".join(text("title").split()),
        "summary": " ".join(text("summary").split()),
        "published": text("published"),
        "updated": text("updated"),
        "authors": authors,
        "categories": cats,
    }


def parse_atom(xml_text: str) -> tuple[int, list[dict[str, Any]]]:
    root = ET.fromstring(xml_text)
    total_el = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    total = int(total_el.text) if total_el is not None and total_el.text else 0
    entries = [entry_to_dict(e) for e in root.findall("atom:entry", ATOM_NS)]
    return total, entries


def in_date_window(published: str, start: datetime, end: datetime) -> bool:
    if not published:
        return False
    # published like 2024-03-15T00:00:00Z
    try:
        dt = datetime.fromisoformat(published.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return False
    return start <= dt <= end.replace(hour=23, minute=59, second=59)


def fetch_arxiv(
    search_query: str,
    *,
    max_results: int,
    session: requests.Session,
) -> tuple[str, dict[str, Any]]:
    """Fetch up to max_results, paging in chunks of 100."""
    page_size = min(100, max_results)
    all_entries: list[dict[str, Any]] = []
    total = 0
    start = 0
    request_urls: list[str] = []

    while start < max_results:
        params = {
            "search_query": search_query,
            "start": start,
            "max_results": min(page_size, max_results - start),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
        resp = session.get(url, timeout=60)
        resp.raise_for_status()
        request_urls.append(url)
        page_total, entries = parse_atom(resp.text)
        total = page_total
        all_entries.extend(entries)
        if not entries or len(all_entries) >= max_results or start + len(entries) >= total:
            break
        start += len(entries)
        time.sleep(MIN_INTERVAL_SEC)

    # Store parsed Atom entries as JSON (reproducible via request_urls).
    # Full Atom XML is omitted to keep raw artifacts reviewable in git.
    payload = {
        "source": "arxiv",
        "api": ARXIV_API,
        "search_query": search_query,
        "request_urls": request_urls,
        "fetched_at": utc_now_iso(),
        "total_results_reported": total,
        "returned": len(all_entries),
        "entries": all_entries[:max_results],
    }
    return search_query, payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Run arXiv searches for protocol queries.")
    parser.add_argument("--force", action="store_true", help="Re-fetch even if raw file exists.")
    parser.add_argument("--block", help="Only run this block id (e.g. B1_peft).")
    args = parser.parse_args()

    data = load_queries()
    meta = data["meta"]
    date_start = _parse_date(meta["date_start"])
    date_end = _parse_date(meta["date_end"])
    # Inclusive end-of-day handled in filter
    categories = meta["arxiv_categories"]
    max_results = int(meta["max_results_per_query"])

    session = requests.Session()
    session.headers.update({"User-Agent": "llm-efficient-finetuning-survey/0.1 (research; mailto:local)"})

    last_request = 0.0
    for block_id, _name, q_idx, query in iter_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path("arxiv", block_id, q_idx)
        if out.exists() and not args.force:
            print(f"skip existing {out.relative_to(out.parents[3])}")
            continue

        elapsed = time.time() - last_request
        if last_request and elapsed < MIN_INTERVAL_SEC:
            time.sleep(MIN_INTERVAL_SEC - elapsed)

        arxiv_q = build_arxiv_search_query(
            query,
            categories,
            meta["date_start"],
            meta["date_end"],
        )
        print(f"arxiv {block_id} q{q_idx}: {query}")
        try:
            _, payload = fetch_arxiv(arxiv_q, max_results=max_results, session=session)
            last_request = time.time()
        except requests.RequestException as exc:
            print(f"  ERROR: {exc}")
            append_search_log(
                source="arxiv",
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=0,
                notes=f"Request failed: {exc}",
            )
            continue

        # Client-side date filter (arXiv submittedDate range syntax is brittle across forms)
        filtered = [
            e for e in payload["entries"]
            if in_date_window(e.get("published", ""), date_start, date_end)
        ]
        hit_cap = len(payload["entries"]) >= max_results
        payload["entries_in_date_window"] = filtered
        payload["protocol_query"] = query
        payload["date_window"] = {"start": meta["date_start"], "end": meta["date_end"]}
        payload["hit_result_cap"] = hit_cap

        save_json(out, payload)
        notes = f"API totalReported={payload['total_results_reported']}; in_window={len(filtered)}"
        if hit_cap:
            notes += f"; HIT_CAP={max_results} — consider narrowing this query"
        append_search_log(
            source="arxiv",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=len(filtered),
            notes=notes,
        )
        print(f"  saved {out.name}: {len(filtered)} in window (fetched {payload['returned']})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
