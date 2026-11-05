#!/usr/bin/env python3
"""Final Stage 1 status of every record after the revision-3 validation, adjudication, re-screen, and second pass.

Precedence (later overrides earlier): screening-log decision; validation decisions (Parts 1 and 2);
adjudication first pass; re-screen first pass; second pass. Reads committed files only.
Writes screening/final-stage1-status.csv and prints the counts reported in the manuscript.
"""
import csv, sys
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)
R = Path(__file__).resolve().parents[1]
V = R / "validation"


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


log = {r["id"]: r for r in read(R / "screening" / "screening-log.csv")}
status = {i: {"decision": r["decision"].upper(), "by": r["screener"] or "none", "stage": r["stage_reached"]} for i, r in log.items()}
sid2rid = {}
for part in ("1", "2"):
    blind = {r["sample_id"]: r for r in read(V / f"part{part}_blind.csv")}
    for k in read(V / f"part{part}_key.csv"):
        sid2rid[k["sample_id"]] = k["record_id"]
        status[k["record_id"]].update(decision=blind[k["sample_id"]]["decision"], by="author_validation")
for r in read(V / "adjudication_first_pass.csv"):
    status[r["record_id"]].update(decision=r["final_decision"], by="author_adjudication")
for r in read(V / "rescreen_first_pass.csv"):
    status[r["record_id"]].update(decision=r["decision"], by="author_rescreen")
for r in read(V / "second_pass_decisions.csv"):
    if r["status"] == "REVIEWED":
        status[r["record_id"]].update(decision=r["decision"], by="author_second_pass")

machine_excl_reversed = sum(1 for i, s in status.items()
                            if log[i]["screener"] in ("automated", "llm_assisted") and log[i]["decision"] == "exclude"
                            and s["decision"] == "INCLUDE")
machine_incl_reversed = sum(1 for i, s in status.items()
                            if log[i]["screener"] in ("automated", "llm_assisted") and log[i]["decision"] == "include"
                            and s["decision"] == "EXCLUDE")
with open(R / "screening" / "final-stage1-status.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "priority_band", "original_decision", "original_screener", "final_decision", "final_decided_by"])
    for i in sorted(status):
        w.writerow([i, log[i]["priority_band"], log[i]["decision"], log[i]["screener"], status[i]["decision"], status[i]["by"]])

for band in ("new_work", "unknown_year", "confirmation"):
    ids = [i for i in status if log[i]["priority_band"] == band]
    print(band, len(ids), dict(Counter(status[i]["decision"] or "NONE" for i in ids)))
nw = [i for i in status if log[i]["priority_band"] == "new_work"]
print("new_work final decided_by:", dict(Counter(status[i]["by"] for i in nw)))
nw_excl = [i for i in nw if status[i]["decision"] == "EXCLUDE"]
print("new_work exclusions:", len(nw_excl), "by:", dict(Counter(status[i]["by"] for i in nw_excl)))
print("machine exclusions reversed to INCLUDE:", machine_excl_reversed)
print("machine inclusions reversed to EXCLUDE:", machine_incl_reversed)
