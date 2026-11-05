#!/usr/bin/env python3
"""Copy first-pass adjudication and re-screen decisions from the workbook to CSV.

Reads validation/rescreen_workbook.xlsx (sheets 'Adjudicate', 'Re-screen').
Writes validation/adjudication_first_pass.csv and validation/rescreen_first_pass.csv.
Validates completeness and codes; changes nothing else.
"""
import csv, sys
from pathlib import Path
from openpyxl import load_workbook

REPO = Path(__file__).resolve().parents[1]
V = REPO / "validation"
CODES = {"I1", "I2", "I4", "I5", "E1", "E2", "E3", "E6"}


def rows(ws, ncols):
    out = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0] or not str(r[0]).startswith(("P1-", "P2-", "R-")):
            continue
        out.append([("" if v is None else str(v).strip()) for v in r[:ncols]])
    return out


def check(label, data, di, ci, expected, need_rationale=None):
    errs = []
    if len(data) != expected:
        errs.append(f"{label}: {len(data)} rows, expected {expected}")
    ids = [r[1] for r in data]
    if len(set(ids)) != len(ids):
        errs.append(f"{label}: duplicate record_id")
    for r in data:
        d, c = r[di].upper(), r[ci].upper()
        if d not in {"INCLUDE", "EXCLUDE"}:
            errs.append(f"{label} {r[0]}: decision {r[di]!r}")
        elif d == "EXCLUDE" and c not in CODES:
            errs.append(f"{label} {r[0]}: EXCLUDE needs a code")
        elif d == "INCLUDE" and c:
            errs.append(f"{label} {r[0]}: INCLUDE has code {c}")
        if need_rationale is not None and not r[need_rationale]:
            errs.append(f"{label} {r[0]}: rationale missing")
    return errs


def main():
    wb = load_workbook(V / "rescreen_workbook.xlsx", read_only=True, data_only=True)
    adj = rows(wb["Adjudicate"], 12)
    rs = rows(wb["Re-screen"], 9)
    errs = check("Adjudicate", adj, 9, 10, 286, 11) + check("Re-screen", rs, 6, 7, 3596)
    if errs:
        print("\n".join(errs[:30]), file=sys.stderr)
        sys.exit(1)
    with open(V / "adjudication_first_pass.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "record_id", "final_decision", "final_reason_code", "rationale"])
        for r in adj:
            w.writerow([r[0], r[1], r[9].upper(), r[10].upper(), r[11]])
    with open(V / "rescreen_first_pass.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rescreen_id", "record_id", "decision", "reason_code", "note"])
        for r in rs:
            w.writerow([r[0], r[1], r[6].upper(), r[7].upper(), r[8]])
    for name, data, di in (("Adjudicate", adj, 9), ("Re-screen", rs, 6)):
        inc = sum(1 for r in data if r[di].upper() == "INCLUDE")
        print(f"{name}: {len(data)} rows, INCLUDE {inc}, EXCLUDE {len(data) - inc}")


if __name__ == "__main__":
    main()
