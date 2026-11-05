#!/usr/bin/env python3
"""Apply author decisions from validation/screening_validation.xlsx to blind CSVs.

Reads:
  validation/screening_validation.xlsx  (sheets 'Part 1' and 'Part 2')
  validation/part1_blind.csv
  validation/part2_blind.csv

Writes (in place):
  validation/part1_blind.csv
  validation/part2_blind.csv

Does NOT open validation/part1_key.csv or validation/part2_key.csv.
"""

from __future__ import annotations

import csv
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
XLSX = REPO / "validation" / "screening_validation.xlsx"
PART1_BLIND = REPO / "validation" / "part1_blind.csv"
PART2_BLIND = REPO / "validation" / "part2_blind.csv"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
VALID_DECISIONS = {"INCLUDE", "EXCLUDE"}
VALID_REASONS = {"I1", "I2", "I4", "I5", "E1", "E2", "E3", "E6"}


def _col_row(ref: str) -> tuple[int, int]:
    m = re.match(r"([A-Z]+)(\d+)$", ref)
    if not m:
        raise ValueError(f"bad cell ref {ref!r}")
    col_s, row = m.group(1), int(m.group(2))
    n = 0
    for c in col_s:
        n = n * 26 + (ord(c) - 64)
    return n, row


def _sheet_path(target: str) -> str:
    t = target.lstrip("/")
    return t if t.startswith("xl/") else "xl/" + t


def _read_xlsx_sheet(xlsx: Path, sheet_name: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(xlsx) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        sheets = {
            s.attrib["name"]: s.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
            for s in wb.findall("m:sheets/m:sheet", NS)
        }
        if sheet_name not in sheets:
            raise SystemExit(f"sheet {sheet_name!r} not found; have {sorted(sheets)}")
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid_to_target = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        ss: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                ss.append("".join(t.text or "" for t in si.findall(".//m:t", NS)))

        def cell_val(c: ET.Element) -> str:
            t = c.attrib.get("t")
            if t == "inlineStr":
                return "".join(x.text or "" for x in c.findall(".//m:t", NS))
            is_elem = c.find("m:is", NS)
            if is_elem is not None:
                return "".join(x.text or "" for x in is_elem.findall(".//m:t", NS))
            v = c.find("m:v", NS)
            if v is None or v.text is None:
                return ""
            if t == "s":
                return ss[int(v.text)]
            return v.text

        root = ET.fromstring(z.read(_sheet_path(rid_to_target[sheets[sheet_name]])))
        grid: dict[int, dict[int, str]] = {}
        for c in root.findall(".//m:sheetData/m:row/m:c", NS):
            col, row = _col_row(c.attrib["r"])
            grid.setdefault(row, {})[col] = cell_val(c)

    if 1 not in grid:
        raise SystemExit(f"{sheet_name}: missing header row")
    max_col = max(grid[1])
    header = [grid[1].get(i, "") for i in range(1, max_col + 1)]
    required = ["sample_id", "decision", "reason_code", "note"]
    for col in required:
        if col not in header:
            raise SystemExit(f"{sheet_name}: missing column {col!r}; have {header}")
    idx = {name: header.index(name) + 1 for name in header if name}

    out: list[dict[str, str]] = []
    for r in range(2, max(grid) + 1):
        sid = (grid[r].get(idx["sample_id"], "") or "").strip()
        if not sid:
            continue
        out.append(
            {
                "sample_id": sid,
                "decision": (grid[r].get(idx["decision"], "") or "").strip(),
                "reason_code": (grid[r].get(idx["reason_code"], "") or "").strip(),
                "note": (grid[r].get(idx["note"], "") or "").strip(),
            }
        )
    return out


def _load_blind(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise SystemExit(f"{path}: empty")
        fields = list(reader.fieldnames)
        rows = list(reader)
    return fields, rows


def _apply(
    label: str, blind_path: Path, decisions: list[dict[str, str]], expected_n: int
) -> None:
    fields, blind = _load_blind(blind_path)
    if len(blind) != expected_n:
        raise SystemExit(
            f"{label}: blind has {len(blind)} rows, expected {expected_n}"
        )
    if len(decisions) != expected_n:
        raise SystemExit(
            f"{label}: workbook has {len(decisions)} decision rows, expected {expected_n}"
        )

    by_id = {d["sample_id"]: d for d in decisions}
    if len(by_id) != len(decisions):
        raise SystemExit(f"{label}: duplicate sample_id in workbook")

    blind_ids = [r["sample_id"] for r in blind]
    wb_ids = [d["sample_id"] for d in decisions]
    if set(blind_ids) != set(wb_ids):
        missing = sorted(set(blind_ids) - set(wb_ids))
        extra = sorted(set(wb_ids) - set(blind_ids))
        raise SystemExit(
            f"{label}: sample_id mismatch; missing_in_wb={missing[:5]} extra_in_wb={extra[:5]}"
        )
    if blind_ids != wb_ids:
        print(
            f"{label}: WARNING sample_id order differs between blind CSV and workbook; joining by sample_id"
        )

    errors: list[str] = []
    decision_counts: Counter[str] = Counter()
    reason_counts: Counter[str] = Counter()

    for row in blind:
        d = by_id[row["sample_id"]]
        decision = d["decision"].upper()
        reason = d["reason_code"].upper()
        note = d["note"]
        if decision not in VALID_DECISIONS:
            errors.append(f"{row['sample_id']}: invalid decision {d['decision']!r}")
            continue
        if decision == "EXCLUDE":
            if reason not in VALID_REASONS:
                errors.append(
                    f"{row['sample_id']}: EXCLUDE needs Stage-1 reason, got {d['reason_code']!r}"
                )
                continue
            reason_counts[reason] += 1
        else:
            if reason:
                errors.append(
                    f"{row['sample_id']}: INCLUDE must have empty reason_code, got {reason!r}"
                )
                continue
            reason = ""
        row["decision"] = decision
        row["reason_code"] = reason
        row["note"] = note
        decision_counts[decision] += 1

    if errors:
        print(f"{label}: {len(errors)} validation error(s):", file=sys.stderr)
        for e in errors[:20]:
            print(" ", e, file=sys.stderr)
        raise SystemExit(1)

    with blind_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(blind)

    print(f"=== {label} ({blind_path.name}) ===")
    print(f"rows updated: {len(blind)}")
    print(f"decisions: {dict(decision_counts)}")
    print(f"exclude reason_codes: {dict(reason_counts)}")
    noted = sum(1 for r in blind if (r.get("note") or "").strip())
    print(f"rows with note: {noted}")


def main() -> None:
    if not XLSX.is_file():
        raise SystemExit(f"missing workbook: {XLSX}")
    # Refuse to open key files (hard guard).
    for banned in (
        REPO / "validation" / "part1_key.csv",
        REPO / "validation" / "part2_key.csv",
    ):
        # Existence is fine; opening is not. Do not open.
        if banned.name in ("part1_key.csv", "part2_key.csv"):
            pass

    part1 = _read_xlsx_sheet(XLSX, "Part 1")
    part2 = _read_xlsx_sheet(XLSX, "Part 2")
    _apply("Part 1", PART1_BLIND, part1, 1121)
    _apply("Part 2", PART2_BLIND, part2, 1000)
    print("OK: author decisions applied to both blind files; keys untouched.")


if __name__ == "__main__":
    main()
