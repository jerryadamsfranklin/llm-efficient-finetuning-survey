#!/usr/bin/env python3
"""Emit Stage 1 screening batches from the pending rows of screening-log.csv.

Implements the band treatment in `protocol/screening-procedure.md`:

  --band new_work      full screen of every pending 2024-01-01 onward record (§3)
  --band confirmation  only records meeting a §4 trigger; the rest are marked
                       not_screened_confirmation_band by mark_unscreened.py
  --band unknown_year  the handful with no year, screened individually

Batches are JSON so decisions can be returned in a validated, machine-checkable form.
Nothing here records a decision; that is `apply_decisions.py`.

Usage:
  python3 screening/scripts/make_batches.py --band new_work --size 150
  python3 screening/scripts/make_batches.py --band confirmation --stats-only
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = REPO_ROOT / "screening" / "screening-log.csv"
POOL_PATH = REPO_ROOT / "search" / "candidate-pool.csv"
REFS_PATH = REPO_ROOT / "search" / "existing-references.yaml"
BATCH_DIR = REPO_ROOT / "screening" / "batches"

ABSTRACT_CHARS = 900
CITATION_TRIGGER = 50

csv.field_size_limit(10**9)

# Core taxonomy terms for the confirmation-band trigger (procedure §4 item 3).
CORE_METHOD_RE = re.compile(
    r"\b(adapter|adapters|lora|adalora|dora|vera|qlora|lokr|loha|"
    r"low[- ]rank adaptation|parameter[- ]efficient|peft|"
    r"prefix[- ]tuning|prompt[- ]tuning|p[- ]tuning|bitfit|soft prompt|"
    r"quantiz\w*|gptq|awq|smoothquant|low[- ]bit|int8|int4|"
    r"zero[- ]?offload|deepspeed|gradient checkpoint\w*|flashattention|"
    r"federated fine[- ]tun\w*|federated lora|fine[- ]tun\w*)\b",
    re.I,
)
SURVEY_RE = re.compile(r"\b(survey|review|systematic review|overview|taxonomy)\b", re.I)


def norm_title(value: Any) -> str:
    s = re.sub(r"[^a-z0-9\s]", " ", str(value or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def load_existing_reference_titles() -> set[str]:
    try:
        import yaml
    except ImportError:
        return set()
    if not REFS_PATH.exists():
        return set()
    refs = yaml.safe_load(REFS_PATH.read_text(encoding="utf-8"))["references"]
    return {norm_title(r["title"]) for r in refs}


def confirmation_triggers(row: dict[str, str], ref_titles: set[str]) -> list[str]:
    """Which §4 triggers this confirmation-band record meets (empty => not screened)."""
    hits: list[str] = []
    if norm_title(row.get("title")) in ref_titles:
        hits.append("existing_corpus")
    try:
        if int(row.get("citations") or 0) >= CITATION_TRIGGER:
            hits.append(f"citations>={CITATION_TRIGGER}")
    except ValueError:
        pass
    title = row.get("title") or ""
    if CORE_METHOD_RE.search(title):
        hits.append("core_method_term")
    if SURVEY_RE.search(title):
        hits.append("survey")
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--band", default="new_work",
                        choices=["new_work", "confirmation", "unknown_year"])
    parser.add_argument("--size", type=int, default=150, help="Records per batch.")
    parser.add_argument("--limit", type=int, help="Only emit this many batches.")
    parser.add_argument("--stats-only", action="store_true", help="Report counts, write nothing.")
    parser.add_argument("--clean", action="store_true", help="Remove existing batches for this band first.")
    args = parser.parse_args()

    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        log = list(csv.DictReader(f))
    with POOL_PATH.open(newline="", encoding="utf-8") as f:
        pool = {r["candidate_id"]: r for r in csv.DictReader(f)}

    pending = [r for r in log if not (r.get("decision") or "").strip()
               and not (r.get("stage_reached") or "").endswith("not_screened")
               and r.get("priority_band") == args.band]

    ref_titles = load_existing_reference_titles()
    if args.band == "confirmation":
        annotated = []
        for r in pending:
            hits = confirmation_triggers(r, ref_titles)
            if hits:
                r = dict(r)
                r["_triggers"] = ",".join(hits)
                annotated.append(r)
        print(f"confirmation band pending: {len(pending)}")
        print(f"  meeting a §4 trigger (to screen):     {len(annotated)}")
        print(f"  no trigger (mark not_screened):       {len(pending) - len(annotated)}")
        pending = annotated
    else:
        print(f"{args.band} band pending: {len(pending)}")

    if not pending:
        print("nothing to batch")
        return 0

    n_batches = (len(pending) + args.size - 1) // args.size
    print(f"batches at size {args.size}: {n_batches}"
          + (f" (emitting {min(args.limit, n_batches)})" if args.limit else ""))
    if args.stats_only:
        return 0

    if args.clean and BATCH_DIR.exists():
        for old in BATCH_DIR.glob(f"stage1_{args.band}_*.json"):
            old.unlink()
    BATCH_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    for bi in range(n_batches):
        if args.limit and bi >= args.limit:
            break
        chunk = pending[bi * args.size:(bi + 1) * args.size]
        records = []
        for r in chunk:
            cand = pool.get(r["id"], {})
            abstract = (cand.get("abstract") or "").strip()
            rec = {
                "id": r["id"],
                "title": r.get("title", ""),
                "year": r.get("year", ""),
                "venue": r.get("venue", ""),
                "citations": r.get("citations", ""),
                # Only ~11% of the pool carries a record type; venue and the arXiv
                # flag carry the archival signal for exclusion 6 when it is absent.
                "record_type": (cand.get("work_type") or "").strip(),
                "arxiv_only": bool((cand.get("arxiv_id") or "").strip())
                and not (cand.get("doi") or "").strip(),
                "abstract": abstract[:ABSTRACT_CHARS] if abstract else "",
                "has_abstract": bool(abstract),
            }
            if r.get("_triggers"):
                rec["confirmation_triggers"] = r["_triggers"]
            records.append(rec)
        out = BATCH_DIR / f"stage1_{args.band}_{bi + 1:03d}.json"
        payload = {
            "batch": bi + 1,
            "band": args.band,
            "n_records": len(records),
            "stage": "stage_1",
            "criteria_reference": "protocol/inclusion-exclusion.md",
            "procedure_reference": "protocol/screening-procedure.md",
            "records": records,
        }
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written += 1
    print(f"wrote {written} batch file(s) to {BATCH_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
