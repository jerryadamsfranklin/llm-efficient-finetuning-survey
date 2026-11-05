#!/usr/bin/env python3
"""Build the second-pass workbook per docs/second-pass-plan.md.

Rows: every first-pass INCLUDE in validation/adjudication_first_pass.csv and
validation/rescreen_first_pass.csv, ordered by record_id. Deterministic.
Writes validation/second_pass_workbook.xlsx (gitignored).
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
F = Font(name="Arial", size=10); FB = Font(name="Arial", size=10, bold=True)
FH = Font(name="Arial", size=10, bold=True, color="FFFFFF")
HDR = PatternFill("solid", fgColor="2E3440"); YEL = PatternFill("solid", fgColor="FFF59D")
GRY = PatternFill("solid", fgColor="ECEFF4")
WRAP = Alignment(wrap_text=True, vertical="top"); TOP = Alignment(vertical="top")


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    pool = {r["candidate_id"]: r for r in read(REPO / "search" / "candidate-pool.csv")}
    items = [("adjudicate", r["sample_id"], r["record_id"]) for r in read(V / "adjudication_first_pass.csv")
             if r["final_decision"] == "INCLUDE"]
    items += [("rescreen", r["rescreen_id"], r["record_id"]) for r in read(V / "rescreen_first_pass.csv")
              if r["decision"] == "INCLUDE"]
    items.sort(key=lambda t: t[2])

    wb = Workbook()
    h = wb.active; h.title = "How to use"
    lines = [
        ("Second pass on first-pass INCLUDE decisions, revision 3. Procedure: docs/second-pass-plan.md", FB),
        ("", F),
        ("Every row is a record you marked INCLUDE in the first pass. Answer the three questions in the yellow columns.", F),
        ("The decision and reason code columns fill in automatically from your answers. Then write a rationale.", F),
        ("", F),
        ("Q1  Is the model studied a language model (or is this a survey of LM efficiency methods)?", FB),
        ("      N if the model is clearly vision, speech, audio, EEG, point cloud, graph, signal, FPGA, or diffusion.", F),
        ("Q2  Does the paper propose, compare, or survey a way to cut compute, memory, or trainable parameters", FB),
        ("      when fine-tuning or adapting that model?  N for tasks, applications, systems, agents, prompting,", F),
        ("      retrieval, evaluation, or benchmarks that do not contribute an efficient fine-tuning method.", F),
        ("Q3  Is it only about inference or only about pre-training?", FB),
        ("      'Inference only' = post-training quantization with no fine-tuning, KV cache, decoding, serving.", F),
        ("      'Pre-training only' = training from scratch with no fine-tuning component.  Otherwise 'No'.", F),
        ("", F),
        ("Result: INCLUDE only if Q1 = Y, Q2 = Y, Q3 = No. Otherwise the first failing code (I2, I1, E2, E1).", F),
        ("Rationale: required. Name the method and the model, e.g. 'new LoRA variant, LLaMA-2'. Generic phrases are not acceptable.", FB),
        ("If the title and abstract genuinely do not let you answer, answer Y/Y/No and write 'ambiguous: <why>'.", F),
        ("", F),
        ("Sittings of about an hour. Save in Excel and run the commit block from the chat after each sitting.", F),
        ("Do not use any AI tool for any answer.", F),
    ]
    for i, (t, f) in enumerate(lines, 1):
        h.cell(row=i, column=1, value=t).font = f
    n = len(items)
    r0 = len(lines) + 2
    h.cell(row=r0, column=1, value="Progress").font = FB
    h.cell(row=r0 + 1, column=1, value="Rows with all three answers and a rationale").font = F
    h.cell(row=r0 + 1, column=2, value=f"=SUMPRODUCT((Review!H2:H{n+1}<>\"\")*(Review!I2:I{n+1}<>\"\")*(Review!J2:J{n+1}<>\"\")*(Review!M2:M{n+1}<>\"\"))").font = F
    h.cell(row=r0 + 1, column=3, value=f"of {n}").font = F
    h.column_dimensions["A"].width = 115; h.column_dimensions["B"].width = 12; h.column_dimensions["C"].width = 10

    s = wb.create_sheet("Review")
    cols = ["pass_id", "from", "record_id", "title", "abstract", "year", "venue",
            "Q1_language_model", "Q2_efficient_ft_method", "Q3_scope", "decision", "reason_code", "rationale"]
    widths = [9, 11, 13, 42, 80, 6, 18, 11, 11, 15, 11, 9, 34]
    for j, v in enumerate(cols, 1):
        x = s.cell(row=1, column=j, value=v); x.font = FH; x.fill = HDR
        s.column_dimensions[chr(64 + j)].width = widths[j - 1]
    for i, (src, sid, rid) in enumerate(items, 2):
        p = pool.get(rid, {})
        vals = [f"S-{i-1:04d}", f"{src}:{sid}", rid, p.get("title", ""), p.get("abstract", ""), p.get("year", ""), p.get("venue", "")]
        for j, v in enumerate(vals, 1):
            x = s.cell(row=i, column=j, value=ILLEGAL_CHARACTERS_RE.sub("", v) if v else None); x.font = F
            x.alignment = WRAP if j in (4, 5, 7) else TOP
        for j in (8, 9, 10, 13):
            x = s.cell(row=i, column=j); x.fill = YEL; x.font = F; x.alignment = WRAP if j == 13 else TOP
        k = s.cell(row=i, column=11, value=(
            f'=IF(OR(H{i}="",I{i}="",J{i}=""),"",IF(H{i}="N","EXCLUDE",IF(I{i}="N","EXCLUDE",'
            f'IF(J{i}="No","INCLUDE","EXCLUDE"))))'))
        c = s.cell(row=i, column=12, value=(
            f'=IF(OR(H{i}="",I{i}="",J{i}=""),"",IF(H{i}="N","I2",IF(I{i}="N","I1",'
            f'IF(J{i}="Inference only","E2",IF(J{i}="Pre-training only","E1","")))))'))
        for x in (k, c):
            x.font = F; x.fill = GRY; x.alignment = TOP
    yn = DataValidation(type="list", formula1='"Y,N"', allow_blank=True)
    yn.add(f"H2:I{n+1}")
    sc = DataValidation(type="list", formula1='"No,Inference only,Pre-training only"', allow_blank=True)
    sc.add(f"J2:J{n+1}")
    s.add_data_validation(yn); s.add_data_validation(sc)
    s.freeze_panes = "D2"
    wb.save(V / "second_pass_workbook.xlsx")
    print(f"Second-pass rows: {n} (adjudicate {sum(1 for t in items if t[0]=='adjudicate')}, "
          f"rescreen {sum(1 for t in items if t[0]=='rescreen')})")


if __name__ == "__main__":
    main()
