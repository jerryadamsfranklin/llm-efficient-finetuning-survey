#!/usr/bin/env python3
"""Initialise screening/screening-log.csv from the Phase 2 candidate pool.

Every candidate in `search/candidate-pool.csv` gets exactly one row. Decisions
are left empty for a human screener except where a criterion can be applied
mechanically from recorded metadata (see APPLY_MECHANICAL below); those rows
carry the numbered criterion that triggered them, per `protocol/inclusion-exclusion.md`.

Existing decisions are preserved: re-running never overwrites a row that already
has a decision, so this is safe to run again after the pool is regenerated.

Usage:
  python3 screening/scripts/init_screening_log.py            # create / refresh
  python3 screening/scripts/init_screening_log.py --dry-run   # report only
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
POOL_PATH = REPO_ROOT / "search" / "candidate-pool.csv"
LOG_PATH = REPO_ROOT / "screening" / "screening-log.csv"

csv.field_size_limit(10**9)

# Canonical column order from the build plan, then screening-support columns.
CANONICAL_FIELDS = [
    "id",
    "source",
    "title",
    "authors",
    "year",
    "venue",
    "stage_reached",
    "decision",
    "exclusion_reason",
    "category",
    "notes",
]
SUPPORT_FIELDS = [
    "subcategory",
    # Decision provenance, required by protocol/screening-procedure.md §3 and §6.
    "screener",  # metadata | llm_assisted | author
    "screener_original",  # preserves the machine decision when the author overturns it
    "confidence",  # high | low  (low => mandatory author review)
    "doi",
    "arxiv_id",
    "citations",
    "citations_source",
    "is_published",
    "n_sources",
    "all_sources",
    "priority_band",
    "has_abstract",
]
FIELDS = CANONICAL_FIELDS + SUPPORT_FIELDS

# Coverage window is 2019-01-01 .. 2026-06-30 (inclusion criterion 5). The pool
# stores year only, so 2026 rows cannot be confirmed against the June cutoff here.
WINDOW_START = 2019
WINDOW_END = 2026

# Work types that are not archival research output (exclusion criterion 6).
NON_ARCHIVAL_TYPES = {"paratext", "erratum", "editorial", "retraction", "courses", "libguides"}


def band(year: str) -> str:
    """Scope-control band from inclusion-exclusion.md: new work vs confirmation pass."""
    y = (year or "").strip()[:4]
    if not y.isdigit():
        return "unknown_year"
    return "new_work" if int(y) >= 2024 else "confirmation"


def mechanical_decision(row: dict[str, str]) -> tuple[str, str, str]:
    """Return (decision, exclusion_reason, notes) decidable from metadata alone.

    Only unambiguous cases are decided here. Anything needing a judgement about
    topic, scale, or contribution is left for the human title/abstract pass.
    """
    year_raw = (row.get("year") or "").strip()[:4]
    work_type = (row.get("work_type") or "").strip().lower()
    language = (row.get("language") or "").strip().lower()

    if (row.get("out_of_protocol") or "").strip() == "yes":
        return (
            "exclude",
            "Exclusion 6",
            "Scholar hit outside protocol scope (vendor doc / non-archival); flagged at dedup.",
        )

    if year_raw.isdigit() and not (WINDOW_START <= int(year_raw) <= WINDOW_END):
        return "exclude", "Inclusion 5", f"Publication year {year_raw} outside 2019-2026 window."

    if work_type in NON_ARCHIVAL_TYPES:
        return "exclude", "Exclusion 6", f"Record type '{row.get('work_type')}' is not archival output."

    if language and language != "en":
        return "exclude", "Inclusion 4", f"Recorded language '{language}' is not English."

    # Not decidable mechanically — leave for the human pass, but surface caveats.
    notes = []
    if not year_raw.isdigit():
        notes.append("Year missing; verify against criterion 5 before including.")
    elif int(year_raw) == WINDOW_END:
        notes.append("2026 record: confirm date is on/before 2026-06-30 (criterion 5).")
    if not (row.get("abstract") or "").strip():
        notes.append("No abstract in pool; title-only screen or fetch abstract.")
    return "", "", " ".join(notes)


def build_row(cand: dict[str, str]) -> dict[str, str]:
    decision, reason, notes = mechanical_decision(cand)
    return {
        "id": cand.get("candidate_id", ""),
        "source": cand.get("canonical_source", ""),
        "title": cand.get("title", ""),
        "authors": cand.get("authors", ""),
        "year": cand.get("year", ""),
        "venue": cand.get("venue", ""),
        "stage_reached": "stage_1" if decision else "stage_1_pending",
        "decision": decision,
        "exclusion_reason": reason,
        "category": "",
        "notes": notes,
        "subcategory": "",
        "screener": "metadata" if decision else "",
        "screener_original": "",
        "confidence": "high" if decision else "",
        "doi": cand.get("doi", ""),
        "arxiv_id": cand.get("arxiv_id", ""),
        "citations": cand.get("citations", ""),
        "citations_source": cand.get("citations_source", ""),
        "is_published": cand.get("is_published", ""),
        "n_sources": cand.get("n_sources", ""),
        "all_sources": cand.get("sources", ""),
        "priority_band": band(cand.get("year", "")),
        "has_abstract": "yes" if (cand.get("abstract") or "").strip() else "no",
    }


def load_existing() -> dict[str, dict[str, str]]:
    if not LOG_PATH.exists():
        return {}
    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if r.get("id")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report counts without writing.")
    args = parser.parse_args()

    if not POOL_PATH.exists():
        print(f"missing {POOL_PATH}; run search/scripts/dedupe.py first", file=sys.stderr)
        return 1

    with POOL_PATH.open(newline="", encoding="utf-8") as f:
        pool = list(csv.DictReader(f))

    existing = load_existing()
    rows: list[dict[str, str]] = []
    preserved = 0
    for cand in pool:
        row = build_row(cand)
        prior = existing.get(row["id"])
        # A human (or later stage) decision always wins over the mechanical default.
        if prior and (prior.get("decision") or "").strip():
            for key in ("stage_reached", "decision", "exclusion_reason", "category", "subcategory",
                        "notes", "screener", "screener_original", "confidence"):
                if (prior.get(key) or "").strip():
                    row[key] = prior[key]
            preserved += 1
        rows.append(row)

    decided = [r for r in rows if r["decision"]]
    pending = [r for r in rows if not r["decision"]]
    print(f"pool candidates:        {len(pool)}")
    print(f"pre-existing decisions: {preserved}")
    print(f"mechanically decided:   {len(decided)} {dict(Counter(r['exclusion_reason'] for r in decided))}")
    print(f"awaiting Stage 1:       {len(pending)}")
    print(f"  by band:              {dict(Counter(r['priority_band'] for r in pending))}")
    print(f"  without abstract:     {sum(1 for r in pending if r['has_abstract'] == 'no')}")

    if args.dry_run:
        print("dry run — nothing written")
        return 0

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in FIELDS})
    print(f"wrote {LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
