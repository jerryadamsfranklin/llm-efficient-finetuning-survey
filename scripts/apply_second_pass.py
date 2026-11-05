#!/usr/bin/env python3
"""Copy second-pass answers from validation/second_pass_workbook.xlsx to
validation/second_pass_decisions.csv.

Recomputes decision and reason code from Q1-Q3 in Python (does not trust cached
formula values). Rows not yet answered are written with status NOT_REVIEWED.
Warns when an identical rationale is reused on more than 5 rows.
"""
import csv, sys
from collections import Counter
from pathlib import Path
from openpyxl import load_workbook

REPO = Path(__file__).resolve().parents[1]
V = REPO / "validation"


def decide(q1, q2, q3):
    if q1 == "N":
        return "EXCLUDE", "I2"
    if q2 == "N":
        return "EXCLUDE", "I1"
    if q3 == "Inference only":
        return "EXCLUDE", "E2"
    if q3 == "Pre-training only":
        return "EXCLUDE", "E1"
    return "INCLUDE", ""


def main():
    ws = load_workbook(V / "second_pass_workbook.xlsx", read_only=True, data_only=True)["Review"]
    out, errs = [], []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0] or not str(r[0]).startswith("S-"):
            continue
        pid, src, rid = r[0], r[1], r[2]
        q1, q2, q3, rat = [("" if v is None else str(v).strip()) for v in (r[7], r[8], r[9], r[12])]
        answered = [q1, q2, q3]
        if not any(answered) and not rat:
            out.append([pid, src, rid, "", "", "", "", "", "NOT_REVIEWED"]); continue
        if not all(answered) or not rat:
            errs.append(f"{pid}: partially answered (Q1={q1!r} Q2={q2!r} Q3={q3!r} rationale={'yes' if rat else 'no'})"); continue
        if q1 not in {"Y", "N"} or q2 not in {"Y", "N"} or q3 not in {"No", "Inference only", "Pre-training only"}:
            errs.append(f"{pid}: invalid answer"); continue
        d, c = decide(q1, q2, q3)
        out.append([pid, src, rid, q1, q2, q3, d, c, "REVIEWED", rat])
    if errs:
        print("\n".join(errs[:30]), file=sys.stderr); sys.exit(1)
    with open(V / "second_pass_decisions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pass_id", "from", "record_id", "q1_language_model", "q2_efficient_ft_method", "q3_scope",
                    "decision", "reason_code", "status", "rationale"])
        for row in out:
            w.writerow(row + [""] * (10 - len(row)))
    rev = [r for r in out if r[8] == "REVIEWED"]
    print(f"rows: {len(out)}  reviewed: {len(rev)}  not reviewed: {len(out) - len(rev)}")
    print("decisions:", dict(Counter((r[6], r[7]) for r in rev)))
    reused = [(t, n) for t, n in Counter(r[9] for r in rev).items() if n > 5]
    for t, n in reused:
        print(f"WARNING: rationale used on {n} rows: {t!r}")


if __name__ == "__main__":
    main()
