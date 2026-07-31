#!/usr/bin/env python3
"""Validate and record Stage 1 decisions into screening/screening-log.csv.

Decisions arrive as JSON files in `screening/decisions/` shaped as:

    {"batch": 1, "band": "new_work", "screener": "llm_assisted",
     "decisions": [{"id": "C-ab12cd34ef", "decision": "exclude",
                    "exclusion_reason": "Inclusion 1", "confidence": "high",
                    "notes": "inference-time only"}]}

Every row is validated before anything is written: unknown ids, unknown criterion codes,
exclusions without a criterion, and decisions on already-decided rows are all rejected.
A file with any invalid row is refused in full, so a malformed batch cannot half-apply.

Author decisions (`--screener author`) may overwrite an existing llm_assisted decision;
the machine decision is preserved in `screener_original`. This is how §6 verification and
audit overturns are recorded.

Usage:
  python3 screening/scripts/apply_decisions.py --dry-run
  python3 screening/scripts/apply_decisions.py
  python3 screening/scripts/apply_decisions.py --file screening/decisions/audit_round1.json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = REPO_ROOT / "screening" / "screening-log.csv"
DECISION_DIR = REPO_ROOT / "screening" / "decisions"

csv.field_size_limit(10**9)

VALID_DECISIONS = {"include", "exclude"}
VALID_CONFIDENCE = {"high", "low"}
VALID_SCREENERS = {"llm_assisted", "author"}
# Stage 1 applies inclusion 1, 4, 5 and exclusions 1-3, 6 (inclusion-exclusion.md §mapping).
VALID_CRITERIA = {
    "Inclusion 1", "Inclusion 2", "Inclusion 3", "Inclusion 4", "Inclusion 5",
    "Exclusion 1", "Exclusion 2", "Exclusion 3", "Exclusion 4", "Exclusion 5", "Exclusion 6",
}


def validate(payload: dict[str, Any], log: dict[str, dict[str, str]], screener: str,
             source: str) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    rows = payload.get("decisions")
    if not isinstance(rows, list) or not rows:
        return [], [f"{source}: no 'decisions' list"]
    seen: set[str] = set()
    ok: list[dict[str, Any]] = []
    for i, d in enumerate(rows):
        where = f"{source}[{i}]"
        cid = str(d.get("id") or "").strip()
        decision = str(d.get("decision") or "").strip().lower()
        reason = str(d.get("exclusion_reason") or "").strip()
        confidence = str(d.get("confidence") or "").strip().lower()

        if cid not in log:
            errors.append(f"{where}: unknown candidate id {cid!r}")
            continue
        if cid in seen:
            errors.append(f"{where}: duplicate id {cid!r} within file")
            continue
        seen.add(cid)
        if decision not in VALID_DECISIONS:
            errors.append(f"{where}: decision must be include/exclude, got {decision!r}")
            continue
        if confidence and confidence not in VALID_CONFIDENCE:
            errors.append(f"{where}: confidence must be high/low, got {confidence!r}")
            continue
        if decision == "exclude":
            if not reason:
                errors.append(f"{where}: exclusion requires a numbered criterion")
                continue
            if reason not in VALID_CRITERIA:
                errors.append(f"{where}: unknown criterion {reason!r}")
                continue
        elif reason:
            errors.append(f"{where}: inclusion must not carry an exclusion_reason")
            continue

        existing = (log[cid].get("decision") or "").strip()
        prior_screener = (log[cid].get("screener") or "").strip()
        if existing and screener != "author":
            errors.append(
                f"{where}: {cid} already decided by {prior_screener or 'unknown'}; "
                "only --screener author may overwrite"
            )
            continue
        ok.append({
            "id": cid,
            "decision": decision,
            "exclusion_reason": reason,
            "confidence": confidence or "high",
            "notes": str(d.get("notes") or "").strip(),
        })
    return ok, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", action="append", help="Specific decision file(s); default: all in screening/decisions/")
    parser.add_argument("--screener", default="llm_assisted", choices=sorted(VALID_SCREENERS))
    parser.add_argument("--dry-run", action="store_true", help="Validate only; write nothing.")
    args = parser.parse_args()

    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        log = {r["id"]: r for r in reader}

    files = [Path(p) for p in args.file] if args.file else sorted(DECISION_DIR.glob("*.json"))
    if not files:
        print(f"no decision files found in {DECISION_DIR}", file=sys.stderr)
        return 1

    applied: list[dict[str, Any]] = []
    all_errors: list[str] = []
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            all_errors.append(f"{path.name}: unreadable ({exc})")
            continue
        screener = str(payload.get("screener") or args.screener)
        if screener not in VALID_SCREENERS:
            all_errors.append(f"{path.name}: invalid screener {screener!r}")
            continue
        rows, errors = validate(payload, log, screener, path.name)
        if errors:
            all_errors.extend(errors)
            print(f"{path.name}: REFUSED ({len(errors)} invalid row(s)); no rows applied from this file")
            continue
        for r in rows:
            r["_screener"] = screener
        applied.extend(rows)
        print(f"{path.name}: {len(rows)} valid decision(s) [screener={screener}]")

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s):", file=sys.stderr)
        for e in all_errors[:40]:
            print(f"  {e}", file=sys.stderr)
        if len(all_errors) > 40:
            print(f"  ... and {len(all_errors) - 40} more", file=sys.stderr)

    if not applied:
        print("\nnothing to apply")
        return 1 if all_errors else 0

    overturns = 0
    for r in applied:
        row = log[r["id"]]
        prior_decision = (row.get("decision") or "").strip()
        prior_screener = (row.get("screener") or "").strip()
        if prior_decision and r["_screener"] == "author":
            if not (row.get("screener_original") or "").strip():
                row["screener_original"] = f"{prior_screener}:{prior_decision}"
            if prior_decision != r["decision"]:
                overturns += 1
        row["decision"] = r["decision"]
        row["exclusion_reason"] = r["exclusion_reason"]
        row["confidence"] = r["confidence"]
        row["screener"] = r["_screener"]
        row["stage_reached"] = "stage_2_pending" if r["decision"] == "include" else "stage_1"
        if r["notes"]:
            row["notes"] = r["notes"]

    counts = Counter(r["decision"] for r in applied)
    print(f"\napplying {len(applied)}: include={counts['include']} exclude={counts['exclude']}")
    if overturns:
        print(f"author overturned {overturns} prior machine decision(s)")
    low = sum(1 for r in applied if r["confidence"] == "low")
    print(f"low-confidence (require author review): {low}")

    if args.dry_run:
        print("dry run — screening-log.csv unchanged")
        return 0

    with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in log.values():
            w.writerow({k: row.get(k, "") for k in fields})
    print(f"wrote {LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
