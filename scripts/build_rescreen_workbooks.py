#!/usr/bin/env python3
"""Build the adjudication and re-screen workbooks per docs/rescreen-plan.md.

Run from the repo root after validation/part1_key.csv and part2_key.csv are committed.
Reads (read-only): validation/part{1,2}_blind.csv, validation/part{1,2}_key.csv,
screening/screening-log.csv, search/candidate-pool.csv.
Writes: validation/rescreen_workbook.xlsx (gitignored).
Deterministic: no randomness; rows ordered by sample_id (adjudication) and record_id (re-screen).
"""
import csv, sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

csv.field_size_limit(sys.maxsize)
REPO = Path(__file__).resolve().parents[1]
V = REPO / "validation"
OUT = V / "rescreen_workbook.xlsx"
F = Font(name="Arial", size=10); FB = Font(name="Arial", size=10, bold=True)
FH = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HDR = PatternFill("solid", fgColor="2E3440"); YEL = PatternFill("solid", fgColor="FFF59D")
GRY = PatternFill("solid", fgColor="ECEFF4")
WRAP = Alignment(wrap_text=True, vertical="top"); TOP = Alignment(vertical="top")
CODES = '"I1,I2,I4,I5,E1,E2,E3,E6"'


def clean(s):
    return ILLEGAL_CHARACTERS_RE.sub("", s or "")


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    log = {r["id"]: r for r in read(REPO / "screening" / "screening-log.csv")}
    pool = {r["candidate_id"]: r for r in read(REPO / "search" / "candidate-pool.csv")}
    adj, reviewed = [], set()
    for part in ("1", "2"):
        blind = {r["sample_id"]: r for r in read(V / f"part{part}_blind.csv")}
        for k in read(V / f"part{part}_key.csv"):
            reviewed.add(k["record_id"])
            b = blind[k["sample_id"]]
            if k["population"] in {"A", "B", "D2"} and k["classifier_decision"] == "exclude" and b["decision"] == "INCLUDE":
                adj.append((k, b))
    adj.sort(key=lambda kb: kb[0]["sample_id"])
    B = [r for r in log.values()
         if r["screener"] in {"automated", "llm_assisted"} and r["decision"] == "exclude" and r["confidence"] == "high"]
    rescreen = sorted((r for r in B if r["id"] not in reviewed), key=lambda r: r["id"])

    wb = Workbook()
    h = wb.active; h.title = "How to use"
    lines = [
        ("Adjudication and re-screen, revision 3 (CS-2026:01:132040). Procedure: docs/rescreen-plan.md", FB),
        ("", F),
        ("Edit only the yellow columns. Do not sort, delete, or edit any other cell. No AI tool for any decision.", F),
        ("Use the Stage 1 criteria on the 'Criteria' tab (same as validation/criteria-sheet.md).", F),
        ("", F),
        ("STEP 1, 'Adjudicate' tab (do this first): each row is a record the classifier excluded and you included.", FB),
        ("  You now see both calls. Decide the final verdict on the written criteria, not on either earlier call.", F),
        ("  final_decision: INCLUDE or EXCLUDE. final_reason_code: required for EXCLUDE, blank for INCLUDE.", F),
        ("  rationale: required on every row, one short phrase (e.g. 'new LoRA variant on LLaMA', 'domain app, LoRA is a tool').", F),
        ("", F),
        ("STEP 2, 'Re-screen' tab: records the classifier excluded with high confidence that no human has reviewed.", FB),
        ("  decision: INCLUDE or EXCLUDE. reason_code: required for EXCLUDE. note: optional.", F),
        ("  INCLUDE only if the research question is a fine-tuning-efficiency method itself, on an LLM.", F),
        ("  Mentioning an LLM, LoRA, or fine-tuning is not enough. If genuinely ambiguous on the criteria, INCLUDE.", F),
        ("", F),
        ("Save after each sitting and run the apply-and-commit block from the chat.", F),
        ("", F),
        ("Example rows (format only, not real records):", FB),
    ]
    for i, (t, f) in enumerate(lines, 1):
        h.cell(row=i, column=1, value=t).font = f
    r = len(lines) + 1
    ex = [["Adjudicate", "final_decision", "final_reason_code", "rationale"],
          ["", "EXCLUDE", "I1", "domain app; LoRA only a tool"],
          ["Re-screen", "decision", "reason_code", "note"],
          ["", "INCLUDE", "", ""]]
    for i, row in enumerate(ex):
        for j, v in enumerate(row, 1):
            c = h.cell(row=r + i, column=j, value=v); c.font = FH if i in (0, 2) else F
            if i in (0, 2): c.fill = HDR
    r += 6
    h.cell(row=r, column=1, value="Progress").font = FB
    h.cell(row=r + 1, column=1, value="Adjudicate rows decided").font = F
    h.cell(row=r + 1, column=2, value=f"=COUNTA(Adjudicate!J2:J{len(adj) + 1})").font = F
    h.cell(row=r + 1, column=3, value=f"of {len(adj)}").font = F
    h.cell(row=r + 2, column=1, value="Re-screen rows decided").font = F
    h.cell(row=r + 2, column=2, value=f"='Re-screen'!H{len(rescreen) + 3}").font = F
    h.cell(row=r + 2, column=3, value=f"of {len(rescreen)}").font = F
    h.column_dimensions["A"].width = 110
    for col in "BCD": h.column_dimensions[col].width = 22

    c = wb.create_sheet("Criteria")
    crit = [("Code", "Fails when (Stage 1 scope)"),
            ("I1", "The contribution is not the fine-tuning-efficiency method itself: a domain task or system that only uses LoRA, QLoRA, adapters, prompt tuning, or quantization as a tool."),
            ("I2", "The model is not a large language model and the non-language domain is clear (vision, speech, audio, graph, multimodal, diffusion), unless the method is general and demonstrated on an LLM. Language-model efficiency surveys stay in."),
            ("I4", "Not written in English."),
            ("I5", "Outside 2019-01-01 to 2026-06-30 (published works dated by publication date)."),
            ("E1", "Exclusively pre-training efficiency, no fine-tuning or adaptation component."),
            ("E2", "Exclusively inference-time optimization, no training or fine-tuning component."),
            ("E3", "Non-transformer architectures only."),
            ("E6", "Blog post, vendor documentation, non-archival white paper, or textbook/tutorial book chapter."),
            ("", ""),
            ("Not applied at Stage 1", "I2 scale (1B parameters), I3 (venue or citations), E4 (duplicates), E5 (qualitative only)."),
            ("Source", "validation/criteria-sheet.md; protocol/inclusion-exclusion.md at commit 839f425.")]
    for i, (a, b) in enumerate(crit, 1):
        x = c.cell(row=i, column=1, value=a); y = c.cell(row=i, column=2, value=b)
        x.font = FH if i == 1 else FB; y.font = FH if i == 1 else F; y.alignment = WRAP
        if i == 1: x.fill = HDR; y.fill = HDR
    c.column_dimensions["A"].width = 24; c.column_dimensions["B"].width = 110

    def sheet(name, cols, widths, rows, n_input, dv_cols):
        s = wb.create_sheet(name)
        for j, v in enumerate(cols, 1):
            x = s.cell(row=1, column=j, value=v); x.font = FH; x.fill = HDR
            s.column_dimensions[chr(64 + j)].width = widths[j - 1]
        first_input = len(cols) - n_input + 1
        for i, vals in enumerate(rows, 2):
            for j, v in enumerate(vals, 1):
                x = s.cell(row=i, column=j, value=clean(v) if v else None); x.font = F
                x.alignment = WRAP if cols[j - 1] in ("title", "abstract", "venue", "rationale", "note") else TOP
                if j >= first_input: x.fill = YEL
                elif cols[j - 1].startswith(("classifier", "your_")): x.fill = GRY
        n = len(rows) + 1
        d1 = DataValidation(type="list", formula1='"INCLUDE,EXCLUDE"', allow_blank=True)
        d1.add(f"{dv_cols[0]}2:{dv_cols[0]}{n}")
        d2 = DataValidation(type="list", formula1=CODES, allow_blank=True)
        d2.add(f"{dv_cols[1]}2:{dv_cols[1]}{n}")
        s.add_data_validation(d1); s.add_data_validation(d2)
        s.freeze_panes = "C2"
        return s

    adj_rows = []
    for k, b in adj:
        lr = log[k["record_id"]]
        adj_rows.append([k["sample_id"], k["record_id"], b["title"], b["abstract"], b["year"], b["venue"],
                         lr.get("exclusion_reason", ""), "INCLUDE", b.get("reason_code", ""), None, None, None])
    sheet("Adjudicate",
          ["sample_id", "record_id", "title", "abstract", "year", "venue", "classifier_exclusion_reason",
           "your_original_decision", "your_original_code", "final_decision", "final_reason_code", "rationale"],
          [9, 13, 40, 70, 6, 20, 16, 12, 10, 12, 12, 35], adj_rows, 3, ("J", "K"))

    rs_rows = []
    for i, r in enumerate(rescreen, 1):
        p = pool.get(r["id"], {})
        rs_rows.append([f"R-{i:04d}", r["id"], p.get("title") or r["title"], p.get("abstract", ""),
                        p.get("year") or r["year"], p.get("venue") or r["venue"], None, None, None])
    s = sheet("Re-screen", ["rescreen_id", "record_id", "title", "abstract", "year", "venue", "decision", "reason_code", "note"],
              [9, 13, 45, 90, 6, 25, 12, 12, 30], rs_rows, 3, ("G", "H"))
    s.cell(row=len(rs_rows) + 3, column=7, value="decided").font = FB
    s.cell(row=len(rs_rows) + 3, column=8, value=f"=COUNTA(G2:G{len(rs_rows) + 1})").font = FB
    wb.save(OUT)
    print(f"Adjudicate rows: {len(adj_rows)}")
    print(f"Re-screen rows: {len(rs_rows)} (population B {len(B)} minus {len(B) - len(rs_rows)} already reviewed)")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
