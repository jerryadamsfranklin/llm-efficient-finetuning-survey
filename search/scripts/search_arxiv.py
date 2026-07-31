#!/usr/bin/env python3
"""Search arXiv API for protocol queries (Phase 2 / Protocol v1.1).

Supports:
  - Full-window search (legacy)
  - --slice-by-year: date-slice capped queries; recursively split H1/H2 then quarters
  - --v11-rerun: re-run only v1.0 HIT_CAP queries + corrected B3_memory_3

Output: search/raw/arxiv/<block>_<n>.json or <block>_<n>__<slice>.json
"""

from __future__ import annotations

import argparse
import json
import shutil
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
    RAW_V10_ROOT,
    append_search_log,
    iter_queries,
    load_queries,
    raw_path,
    save_json,
    utc_now_iso,
)

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_API = "http://export.arxiv.org/api/query"
MIN_INTERVAL_SEC = 3.0

# From v1.0 execution (commit d7313cd) — queries that hit the 200-cap
V10_HIT_CAP = {
    ("B1_peft", 1),
    ("B1_peft", 2),
    ("B1_peft", 3),
    ("B1_peft", 4),
    ("B2_quantization", 1),
    ("B2_quantization", 3),
    ("B3_memory", 3),  # also corrected string in v1.1
    ("B4_federated", 1),
    ("B4_federated", 2),
}

# Under-cap in v1.0 — keep as valid; copy into search/raw for convenience
V10_VALID = {
    ("B1_peft", 5),
    ("B2_quantization", 2),
    ("B2_quantization", 4),
    ("B2_quantization", 5),
    ("B3_memory", 1),
    ("B3_memory", 2),
    ("B3_memory", 4),
    ("B4_federated", 3),
    ("B4_federated", 4),
}


def build_arxiv_search_query(
    user_query: str,
    categories: list[str],
    date_start: str,
    date_end: str,
) -> str:
    q = user_query.strip()
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
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
    cats = [c.attrib.get("term", "") for c in entry.findall("atom:category", ATOM_NS)]
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


def fetch_arxiv(
    search_query: str,
    *,
    max_results: int,
    session: requests.Session,
    last_request: list[float],
) -> dict[str, Any]:
    page_size = min(100, max_results)
    all_entries: list[dict[str, Any]] = []
    total = 0
    start = 0
    request_urls: list[str] = []

    while start < max_results:
        elapsed = time.time() - last_request[0]
        if last_request[0] and elapsed < MIN_INTERVAL_SEC:
            time.sleep(MIN_INTERVAL_SEC - elapsed)

        params = {
            "search_query": search_query,
            "start": start,
            "max_results": min(page_size, max_results - start),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
        resp = None
        for attempt in range(8):
            resp = session.get(url, timeout=60)
            last_request[0] = time.time()
            if resp.status_code == 429:
                wait = min(120, 5 * (2 ** attempt))
                print(f"  arXiv 429; sleeping {wait}s", flush=True)
                time.sleep(wait)
                continue
            if resp.status_code >= 500:
                time.sleep(min(60, 5 * (attempt + 1)))
                continue
            break
        if resp is None or resp.status_code >= 400:
            if resp is not None:
                resp.raise_for_status()
            raise RuntimeError("arXiv request failed")
        request_urls.append(url)
        page_total, entries = parse_atom(resp.text)
        total = page_total
        all_entries.extend(entries)
        if not entries or len(all_entries) >= max_results or start + len(entries) >= total:
            break
        start += len(entries)

    return {
        "source": "arxiv",
        "protocol_version": "1.1",
        "api": ARXIV_API,
        "search_query": search_query,
        "request_urls": request_urls,
        "fetched_at": utc_now_iso(),
        "total_results_reported": total,
        "returned": len(all_entries[:max_results]),
        "entries": all_entries[:max_results],
        "hit_result_cap": len(all_entries) >= max_results,
    }


def initial_slices(meta: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Return [(slice_id, start_iso, end_iso), ...] from meta.date_slices or default."""
    raw = meta.get("date_slices") or [
        "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026-H1"
    ]
    out = []
    for s in raw:
        if s.endswith("-H1"):
            y = int(s[:4])
            out.append((s, f"{y}-01-01", f"{y}-06-30"))
        elif s.endswith("-H2"):
            y = int(s[:4])
            out.append((s, f"{y}-07-01", f"{y}-12-31"))
        else:
            y = int(s)
            # 2026 full year not in protocol; only H1 for coverage end
            end = f"{y}-06-30" if y == 2026 else f"{y}-12-31"
            sid = "2026-H1" if y == 2026 else s
            out.append((sid, f"{y}-01-01", end))
    # dedupe by slice_id
    seen = set()
    uniq = []
    for item in out:
        if item[0] in seen:
            continue
        seen.add(item[0])
        uniq.append(item)
    return uniq


def split_slice(slice_id: str, start: str, end: str) -> list[tuple[str, str, str]]:
    """Split a capped slice into finer granularity (H1/H2 or quarters)."""
    y = int(start[:4])
    if slice_id.isdigit() or (len(slice_id) == 4 and slice_id.isdigit()):
        return [
            (f"{y}-H1", f"{y}-01-01", f"{y}-06-30"),
            (f"{y}-H2", f"{y}-07-01", f"{y}-12-31"),
        ]
    if slice_id.endswith("-H1"):
        return [
            (f"{y}-Q1", f"{y}-01-01", f"{y}-03-31"),
            (f"{y}-Q2", f"{y}-04-01", f"{y}-06-30"),
        ]
    if slice_id.endswith("-H2"):
        return [
            (f"{y}-Q3", f"{y}-07-01", f"{y}-09-30"),
            (f"{y}-Q4", f"{y}-10-01", f"{y}-12-31"),
        ]
    # Already quarterly — cannot split further
    return []


def is_quarter(slice_id: str) -> bool:
    return "-Q" in slice_id


def copy_v10_valid() -> None:
    """Copy under-cap v1.0 arXiv files into search/raw and log as v1.0-valid."""
    for block_id, q_idx in sorted(V10_VALID):
        src = RAW_V10_ROOT / "arxiv" / f"{block_id}_{q_idx}.json"
        dst = raw_path("arxiv", block_id, q_idx)
        if not src.exists():
            print(f"  WARN missing v1.0 file {src.name}")
            continue
        if not dst.exists():
            shutil.copy2(src, dst)
        data = json.loads(src.read_text(encoding="utf-8"))
        n = len(data.get("entries_in_date_window") or data.get("entries") or [])
        query = data.get("protocol_query") or ""
        append_search_log(
            source="arxiv",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=n,
            notes="v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.",
        )
        print(f"  keep v1.0-valid {block_id}_{q_idx} ({n})")


def run_sliced_query(
    *,
    block_id: str,
    q_idx: int,
    query: str,
    categories: list[str],
    max_results: int,
    session: requests.Session,
    last_request: list[float],
    force: bool,
    slices: list[tuple[str, str, str]],
) -> None:
    queue = list(slices)
    while queue:
        slice_id, d_start, d_end = queue.pop(0)
        out = raw_path("arxiv", block_id, q_idx, slice_id=slice_id)
        if out.exists() and not force:
            print(f"  skip existing {out.name}")
            # If existing hit cap at non-quarter, still need children — inspect
            existing = json.loads(out.read_text(encoding="utf-8"))
            if existing.get("hit_result_cap") and not is_quarter(slice_id):
                children = split_slice(slice_id, d_start, d_end)
                for child in children:
                    child_path = raw_path("arxiv", block_id, q_idx, slice_id=child[0])
                    if not child_path.exists() or force:
                        queue.append(child)
            continue

        arxiv_q = build_arxiv_search_query(query, categories, d_start, d_end)
        print(f"arxiv {block_id} q{q_idx} slice {slice_id}: {query[:70]}...", flush=True)
        try:
            payload = fetch_arxiv(
                arxiv_q, max_results=max_results, session=session, last_request=last_request
            )
        except requests.RequestException as exc:
            print(f"  ERROR: {exc}", flush=True)
            append_search_log(
                source="arxiv",
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=0,
                slice_id=slice_id,
                notes=f"Request failed: {exc}",
            )
            continue

        payload["protocol_query"] = query
        payload["slice_id"] = slice_id
        payload["date_window"] = {"start": d_start, "end": d_end}
        payload["entries_in_date_window"] = payload["entries"]  # filtered server-side
        save_json(out, payload)

        notes = (
            f"protocol=1.1; slice={slice_id}; "
            f"API totalReported={payload['total_results_reported']}"
        )
        if payload["hit_result_cap"]:
            notes += f"; HIT_CAP={max_results}"
            children = split_slice(slice_id, d_start, d_end)
            if children:
                notes += f"; splitting into {[c[0] for c in children]}"
                queue.extend(children)
            elif is_quarter(slice_id):
                notes += (
                    "; RESIDUAL_GAP — quarterly slice still at cap; "
                    "coverage incomplete for this slice (stated stopping rule)"
                )
        append_search_log(
            source="arxiv",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=payload["returned"],
            slice_id=slice_id,
            notes=notes,
        )
        print(
            f"  saved {out.name}: {payload['returned']} "
            f"(totalReported={payload['total_results_reported']}"
            f"{'; HIT_CAP' if payload['hit_result_cap'] else ''})",
            flush=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run arXiv searches (protocol v1.1).")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--block", help="Only this block id.")
    parser.add_argument(
        "--slice-by-year",
        action="store_true",
        help="Date-slice queries (year / H1-H2 / quarters on cap).",
    )
    parser.add_argument(
        "--v11-rerun",
        action="store_true",
        help="Keep v1.0-valid under-cap queries; date-slice only v1.0 HIT_CAP + B3_memory_3.",
    )
    args = parser.parse_args()

    data = load_queries()
    meta = data["meta"]
    categories = meta["arxiv_categories"]
    max_results = int(meta["max_results_per_query"])

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "llm-efficient-finetuning-survey/1.1 (research; mailto:local)"}
    )
    last_request = [0.0]

    if args.v11_rerun:
        print("=== Copying v1.0-valid (under-cap) arXiv results ===", flush=True)
        copy_v10_valid()
        print("=== Date-slicing v1.0 HIT_CAP queries (+ corrected B3_memory_3) ===", flush=True)
        slices = initial_slices(meta)
        for block_id, _name, q_idx, query in iter_queries(data):
            if args.block and block_id != args.block:
                continue
            if (block_id, q_idx) not in V10_HIT_CAP:
                continue
            run_sliced_query(
                block_id=block_id,
                q_idx=q_idx,
                query=query,
                categories=categories,
                max_results=max_results,
                session=session,
                last_request=last_request,
                force=args.force,
                slices=slices,
            )
        return 0

    if args.slice_by_year:
        slices = initial_slices(meta)
        for block_id, _name, q_idx, query in iter_queries(data):
            if args.block and block_id != args.block:
                continue
            run_sliced_query(
                block_id=block_id,
                q_idx=q_idx,
                query=query,
                categories=categories,
                max_results=max_results,
                session=session,
                last_request=last_request,
                force=args.force,
                slices=slices,
            )
        return 0

    # Legacy full-window mode
    for block_id, _name, q_idx, query in iter_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path("arxiv", block_id, q_idx)
        if out.exists() and not args.force:
            print(f"skip existing {out.name}")
            continue
        arxiv_q = build_arxiv_search_query(
            query, categories, meta["date_start"], meta["date_end"]
        )
        print(f"arxiv {block_id} q{q_idx}: {query}", flush=True)
        try:
            payload = fetch_arxiv(
                arxiv_q, max_results=max_results, session=session, last_request=last_request
            )
        except requests.RequestException as exc:
            print(f"  ERROR: {exc}")
            continue
        payload["protocol_query"] = query
        payload["date_window"] = {"start": meta["date_start"], "end": meta["date_end"]}
        payload["entries_in_date_window"] = payload["entries"]
        save_json(out, payload)
        append_search_log(
            source="arxiv",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=payload["returned"],
            notes=f"totalReported={payload['total_results_reported']}",
        )
        print(f"  saved {out.name}: {payload['returned']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
