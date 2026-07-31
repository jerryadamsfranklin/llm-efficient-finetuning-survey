#!/usr/bin/env python3
"""Protocol v1.3: targeted supplementary retrieval of known-corpus misses.

This is **verification of an already-cited corpus, not discovery.** It looks up
references that the manuscript already cites and that the Phase 2 queries did not
retrieve, so their metadata exists in machine-readable form and they can be screened
against the same criteria as every other candidate.

It must not be described as extending the reach of the search. No keyword search for new
material is performed: every lookup is keyed to a specific known reference.

The missing set is computed, not hardcoded: any in-window reference in
`search/existing-references.yaml` with no match in `search/candidate-pool.csv` is looked up.

Outputs:
  search/raw/supplementary/known_corpus_misses.json
  appends per-reference entries to search/search-log.md

Usage:
  python3 search/scripts/search_supplementary.py --dry-run   # list the missing set only
  python3 search/scripts/search_supplementary.py
"""

from __future__ import annotations

import argparse
import csv
import difflib
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import (  # noqa: E402
    RAW_ROOT,
    REPO_ROOT,
    append_search_log,
    load_local_env,
    save_json,
    utc_now_iso,
)

S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "title,authors,year,venue,citationCount,externalIds,abstract,openAccessPdf,publicationTypes"
CROSSREF = "https://api.crossref.org/works"
POOL_PATH = REPO_ROOT / "search" / "candidate-pool.csv"
REFS_PATH = REPO_ROOT / "search" / "existing-references.yaml"
OUT_PATH = RAW_ROOT / "supplementary" / "known_corpus_misses.json"

WINDOW_START, WINDOW_END = 2019, 2026
TITLE_MATCH_MIN = 0.90
INTER_REQUEST_SEC = 3.5

csv.field_size_limit(10**9)


def norm_title(value: Any) -> str:
    s = re.sub(r"[^a-z0-9\s]", " ", str(value or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def norm_doi(value: Any) -> str:
    return str(value or "").strip().lower().replace("https://doi.org/", "")


def find_missing() -> tuple[list[dict[str, Any]], dict[str, int]]:
    """In-window references from the manuscript corpus with no candidate-pool match."""
    with POOL_PATH.open(newline="", encoding="utf-8") as f:
        pool = list(csv.DictReader(f))
    refs = yaml.safe_load(REFS_PATH.read_text(encoding="utf-8"))["references"]

    pool_titles = {norm_title(r["title"]) for r in pool}
    pool_dois = {norm_doi(r["doi"]) for r in pool if r["doi"]}
    pool_arxiv = {str(r["arxiv_id"]).strip() for r in pool if r["arxiv_id"]}

    missing: list[dict[str, Any]] = []
    stats = {"total": len(refs), "in_pool": 0, "out_of_window": 0, "missing": 0}
    for ref in refs:
        year = ref.get("year")
        if not (isinstance(year, int) and WINDOW_START <= year <= WINDOW_END):
            stats["out_of_window"] += 1
            continue
        doi = norm_doi(ref.get("doi") or ref.get("verified_doi"))
        arx = str(ref.get("arxiv_id") or "").strip()
        if (doi and doi in pool_dois) or (arx and arx in pool_arxiv) or norm_title(ref["title"]) in pool_titles:
            stats["in_pool"] += 1
            continue
        stats["missing"] += 1
        missing.append(ref)
    return missing, stats


def s2_lookup(title: str, session: requests.Session) -> tuple[dict[str, Any] | None, str]:
    """Return (record, status) where status is matched | no_match | unresolved.

    'unresolved' means the API never answered (rate limits / errors). It must never be
    recorded as evidence that the paper is absent — that distinction is the difference
    between a finding and an artifact of throttling.
    """
    params = {"query": title, "fields": S2_FIELDS, "limit": 10}
    for attempt in range(8):
        try:
            resp = session.get(S2_SEARCH, params=params, timeout=45)
        except requests.RequestException as exc:
            print(f"    network error ({exc}); retrying", flush=True)
            time.sleep(min(60, 3 * (attempt + 1)))
            continue
        if resp.status_code == 429:
            wait = min(120, 5 * (2 ** attempt))
            print(f"    429 rate limit; sleeping {wait}s", flush=True)
            time.sleep(wait)
            continue
        if resp.status_code >= 500:
            time.sleep(min(60, 5 * (attempt + 1)))
            continue
        resp.raise_for_status()
        want = norm_title(title)
        best, best_score = None, 0.0
        for cand in resp.json().get("data") or []:
            score = difflib.SequenceMatcher(None, want, norm_title(cand.get("title"))).ratio()
            if score > best_score:
                best, best_score = cand, score
        if best and best_score >= TITLE_MATCH_MIN:
            best["_title_match_ratio"] = round(best_score, 4)
            return best, "matched"
        return None, "no_match"
    return None, "unresolved"


def crossref_lookup(title: str, session: requests.Session) -> dict[str, Any] | None:
    params = {"query.bibliographic": title, "rows": 5}
    try:
        resp = session.get(CROSSREF, params=params, timeout=45)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"    crossref error ({exc})", flush=True)
        return None
    want = norm_title(title)
    best, best_score = None, 0.0
    for item in (resp.json().get("message") or {}).get("items") or []:
        cand_title = (item.get("title") or [""])[0]
        score = difflib.SequenceMatcher(None, want, norm_title(cand_title)).ratio()
        if score > best_score:
            best, best_score = item, score
    if best and best_score >= TITLE_MATCH_MIN:
        return {
            "title": (best.get("title") or [""])[0],
            "doi": best.get("DOI"),
            "year": ((best.get("issued") or {}).get("date-parts") or [[None]])[0][0],
            "venue": (best.get("container-title") or [""])[0],
            "type": best.get("type"),
            "authors": [
                f"{a.get('given','')} {a.get('family','')}".strip()
                for a in best.get("author") or []
            ],
            "citationCount": best.get("is-referenced-by-count"),
            "_title_match_ratio": round(best_score, 4),
        }
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="List the missing set; fetch nothing.")
    args = parser.parse_args()

    missing, stats = find_missing()
    print(
        f"existing references: {stats['total']} | in pool: {stats['in_pool']} | "
        f"outside window: {stats['out_of_window']} | in-window and missing: {stats['missing']}\n"
    )
    for ref in missing:
        print(f"  {ref['key']:16} ({ref.get('year')})  {ref['title'][:66]}")
    if args.dry_run:
        print("\ndry run — nothing fetched")
        return 0
    if not missing:
        print("nothing to retrieve")
        return 0

    load_local_env()
    session = requests.Session()
    headers = {"User-Agent": "llm-efficient-finetuning-survey/0.1 (research; supplementary verification)"}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key
        print("using SEMANTIC_SCHOLAR_API_KEY from environment")
    else:
        print("WARNING: no SEMANTIC_SCHOLAR_API_KEY; expect heavy 429 throttling")
    session.headers.update(headers)

    records: list[dict[str, Any]] = []
    for ref in missing:
        key, title = ref["key"], ref["title"]
        print(f"\nlookup {key}: {title[:70]}", flush=True)
        found, status = s2_lookup(title, session)
        origin = "semanticscholar"
        if not found:
            reason = "no match" if status == "no_match" else "API unresolved"
            print(f"    Semantic Scholar: {reason}; trying Crossref", flush=True)
            found = crossref_lookup(title, session)
            if found:
                origin, status = "crossref", "matched"
        rec = {
            "reference_key": key,
            "reference_title": title,
            "reference_year": ref.get("year"),
            "reference_venue": ref.get("verified_venue") or ref.get("venue_current"),
            "lookup_origin": origin if found else None,
            "lookup_status": status,
            "found": bool(found),
            "record": found,
        }
        records.append(rec)
        if found:
            print(f"    matched via {origin} (ratio {found.get('_title_match_ratio')})", flush=True)
        elif status == "unresolved":
            print("    UNRESOLVED — API did not answer; not evidence of absence", flush=True)
        else:
            print("    no match at title ratio >= %.2f" % TITLE_MATCH_MIN, flush=True)
        append_search_log(
            source="supplementary",
            block_id="known_corpus",
            query_index=len(records),
            query=f'title lookup: "{title}"',
            n_results=1 if found else 0,
            notes=(
                "protocol=1.3 targeted supplementary retrieval (verification of an "
                "already-cited reference, NOT discovery); "
                f"reference_key={key}; status={status}"
                + (f"; matched via {origin}" if found else "")
            ),
        )
        time.sleep(INTER_REQUEST_SEC)

    payload = {
        "source": "supplementary",
        "run_type": "known_corpus_verification",
        "protocol_version": "1.3",
        "purpose": (
            "Retrieve in-window references already cited in the manuscript that the Phase 2 "
            "queries did not return. Verification of a known corpus, not discovery. "
            "See search/coverage-diagnostic.md."
        ),
        "fetched_at": utc_now_iso(),
        "selection_rule": (
            "In-window (2019-2026) reference in search/existing-references.yaml with no "
            "DOI / arXiv ID / normalized-title match in search/candidate-pool.csv."
        ),
        "title_match_min_ratio": TITLE_MATCH_MIN,
        "reference_stats": stats,
        "n_requested": len(missing),
        "n_found": sum(1 for r in records if r["found"]),
        "n_no_match": sum(1 for r in records if r["lookup_status"] == "no_match"),
        "n_unresolved": sum(1 for r in records if r["lookup_status"] == "unresolved"),
        "results": records,
    }
    save_json(OUT_PATH, payload)
    print(f"\nwrote {OUT_PATH}")
    print(
        f"found {payload['n_found']} of {payload['n_requested']}; "
        f"no_match={payload['n_no_match']}; unresolved={payload['n_unresolved']}"
    )
    if payload["n_unresolved"]:
        print("re-run to resolve throttled lookups before drawing conclusions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
