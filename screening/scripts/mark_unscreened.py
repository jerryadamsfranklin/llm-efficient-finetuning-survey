#!/usr/bin/env python3
"""Mark confirmation-band records that fall outside the screening scope bound.

Per `protocol/screening-procedure.md` §4, 2019-2023 records that meet none of the four
triggers are **not screened**. They are recorded as `stage_1_not_screened` with an empty
`decision`, because calling an unexamined record "excluded" would misrepresent it as judged.
They are reported as their own PRISMA-style line.

This is deliberately reversible: `--unmark` clears the state so the band can be screened in
full later without ambiguity about what was examined.

Usage:
  python3 screening/scripts/mark_unscreened.py --dry-run
  python3 screening/scripts/mark_unscreened.py
  python3 screening/scripts/mark_unscreened.py --unmark
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from make_batches import confirmation_triggers, load_existing_reference_titles  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parents[1]
LOG_PATH = REPO_ROOT / "screening" / "screening-log.csv"
NOT_SCREENED = "stage_1_not_screened"
NOTE = (
    "Not screened: 2019-2023 confirmation band, meets no trigger in "
    "protocol/screening-procedure.md §4 (existing corpus, >=50 citations, core-method term, survey). "
    "Neither included nor excluded."
)

csv.field_size_limit(10**9)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Report only; write nothing.")
    parser.add_argument("--unmark", action="store_true", help="Clear the not-screened state.")
    args = parser.parse_args()

    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    if args.unmark:
        n = 0
        for r in rows:
            if (r.get("stage_reached") or "") == NOT_SCREENED:
                r["stage_reached"] = "stage_1_pending"
                if (r.get("notes") or "").startswith("Not screened:"):
                    r["notes"] = ""
                n += 1
        print(f"cleared not-screened state on {n} row(s)")
    else:
        ref_titles = load_existing_reference_titles()
        n = 0
        kept = 0
        for r in rows:
            if r.get("priority_band") != "confirmation":
                continue
            if (r.get("decision") or "").strip():
                continue
            if (r.get("stage_reached") or "") == NOT_SCREENED:
                continue
            if confirmation_triggers(r, ref_titles):
                kept += 1
                continue
            r["stage_reached"] = NOT_SCREENED
            r["notes"] = NOTE
            n += 1
        print(f"confirmation band: {kept} to screen (trigger met), {n} marked not screened")
        if not ref_titles:
            print("WARNING: existing-references.yaml unreadable; corpus trigger not applied")

    if args.dry_run:
        print("dry run — screening-log.csv unchanged")
        return 0

    with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"wrote {LOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
