#!/usr/bin/env python3
"""Search OpenReview API for protocol queries (Phase 2).

Discovery mode: run each protocol query against notes/search.
Venue-check mode: --check-existing reads search/existing-references.yaml and
looks up each title / arXiv ID for acceptance records (preprint upgrades).

Saves under search/raw/openreview/ and appends search/search-log.md.
"""

from __future__ import annotations

import argparse
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
    REPO_ROOT,
    append_search_log,
    iter_queries,
    load_queries,
    raw_path,
    save_json,
    utc_now_iso,
)

OPENREVIEW_SEARCH = "https://api2.openreview.net/notes/search"
OPENREVIEW_NOTES = "https://api2.openreview.net/notes"
EXISTING_REFS = REPO_ROOT / "search" / "existing-references.yaml"


def _get_with_backoff(session: requests.Session, url: str, params: dict[str, Any]) -> dict[str, Any]:
    for attempt in range(8):
        resp = session.get(url, params=params, timeout=60)
        if resp.status_code == 429:
            wait = min(60, 2 ** attempt)
            print(f"  429; sleeping {wait}s")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Rate limit persisted for {url}")


def search_openreview(
    term: str,
    *,
    max_results: int,
    session: requests.Session,
) -> dict[str, Any]:
    notes: list[dict[str, Any]] = []
    limit = min(50, max_results)
    offset = 0

    while len(notes) < max_results:
        params = {
            "term": term,
            "limit": min(limit, max_results - len(notes)),
            "offset": offset,
        }
        data = _get_with_backoff(session, OPENREVIEW_SEARCH, params)
        batch = data.get("notes") or []
        notes.extend(batch)
        if not batch:
            break
        offset += len(batch)
        time.sleep(0.5)

    return {
        "source": "openreview",
        "api": OPENREVIEW_SEARCH,
        "term": term,
        "fetched_at": utc_now_iso(),
        "returned": len(notes[:max_results]),
        "hit_result_cap": len(notes) >= max_results,
        "notes": notes[:max_results],
    }


def lookup_reference(ref: dict[str, Any], session: requests.Session) -> dict[str, Any]:
    """Best-effort venue/acceptance lookup for one existing corpus reference."""
    title = (ref.get("title") or "").strip()
    arxiv_id = (ref.get("arxiv_id") or "").strip()
    result: dict[str, Any] = {
        "input": ref,
        "searches": [],
        "candidate_notes": [],
    }

    terms = []
    if title:
        terms.append(title)
    if arxiv_id:
        terms.append(arxiv_id)

    for term in terms:
        try:
            data = _get_with_backoff(
                session,
                OPENREVIEW_SEARCH,
                {"term": term, "limit": 10, "offset": 0},
            )
            notes = data.get("notes") or []
            result["searches"].append({"term": term, "n": len(notes)})
            result["candidate_notes"].extend(notes)
        except (requests.RequestException, RuntimeError) as exc:
            result["searches"].append({"term": term, "error": str(exc)})
        time.sleep(0.5)

    # Deduplicate notes by id
    seen = set()
    unique = []
    for n in result["candidate_notes"]:
        nid = n.get("id")
        if nid in seen:
            continue
        seen.add(nid)
        unique.append(
            {
                "id": nid,
                "forum": n.get("forum"),
                "invitation": n.get("invitation"),
                "content_title": (n.get("content") or {}).get("title"),
                "content_venue": (n.get("content") or {}).get("venue"),
                "content_venueid": (n.get("content") or {}).get("venueid"),
            }
        )
    result["candidate_notes"] = unique
    return result


def run_discovery(args: argparse.Namespace, session: requests.Session) -> int:
    data = load_queries()
    max_results = int(data["meta"]["max_results_per_query"])

    for block_id, _name, q_idx, query in iter_queries(data):
        if args.block and block_id != args.block:
            continue
        out = raw_path("openreview", block_id, q_idx)
        if out.exists() and not args.force:
            print(f"skip existing {out.name}")
            continue

        # OpenReview term search works better with a simplified string
        term = (
            query.replace('"', " ")
            .replace(" AND ", " ")
            .replace(" OR ", " ")
            .replace("(", " ")
            .replace(")", " ")
        )
        term = " ".join(term.split())
        print(f"openreview {block_id} q{q_idx}: {term}")
        try:
            payload = search_openreview(term, max_results=max_results, session=session)
            payload["protocol_query"] = query
        except (requests.RequestException, RuntimeError) as exc:
            print(f"  ERROR: {exc}")
            append_search_log(
                source="openreview",
                block_id=block_id,
                query_index=q_idx,
                query=query,
                n_results=0,
                notes=f"Request failed: {exc}",
            )
            continue

        save_json(out, payload)
        notes = ""
        if payload.get("hit_result_cap"):
            notes = f"HIT_CAP={max_results} — consider narrowing this query"
        append_search_log(
            source="openreview",
            block_id=block_id,
            query_index=q_idx,
            query=query,
            n_results=payload["returned"],
            notes=notes,
        )
        print(f"  saved {out.name}: {payload['returned']} notes")
    return 0


def run_existing_check(session: requests.Session) -> int:
    if not EXISTING_REFS.exists():
        print(
            f"Missing {EXISTING_REFS.relative_to(REPO_ROOT)}. "
            "Add titles/arxiv_ids for the existing ~42 references, then re-run "
            "with --check-existing."
        )
        return 1

    refs = yaml.safe_load(EXISTING_REFS.read_text(encoding="utf-8")) or []
    if isinstance(refs, dict):
        refs = refs.get("references") or []
    if not refs:
        print(f"{EXISTING_REFS.name} has no references yet — fill it before venue checks.")
        return 1

    out = REPO_ROOT / "search" / "raw" / "openreview" / "existing_references_venue_check.json"
    results = []
    for i, ref in enumerate(refs, start=1):
        title = (ref.get("title") or ref.get("key") or f"ref_{i}")
        print(f"venue-check {i}/{len(refs)}: {title[:80]}")
        results.append(lookup_reference(ref, session))

    payload = {
        "source": "openreview",
        "mode": "existing_references_venue_check",
        "fetched_at": utc_now_iso(),
        "n_references": len(refs),
        "results": results,
    }
    save_json(out, payload)
    append_search_log(
        source="openreview",
        block_id="existing_refs",
        query_index=1,
        query="venue check for existing manuscript references",
        n_results=len(refs),
        notes=f"Wrote {out.relative_to(REPO_ROOT)}",
    )
    print(f"saved {out.relative_to(REPO_ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run OpenReview searches / venue checks.")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--block", help="Only run this block id (discovery mode).")
    parser.add_argument(
        "--check-existing",
        action="store_true",
        help="Look up acceptance status for search/existing-references.yaml",
    )
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update({"User-Agent": "llm-efficient-finetuning-survey/0.1 (research)"})

    if args.check_existing:
        return run_existing_check(session)
    return run_discovery(args, session)


if __name__ == "__main__":
    raise SystemExit(main())
