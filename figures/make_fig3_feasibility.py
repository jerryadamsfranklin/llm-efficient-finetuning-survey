#!/usr/bin/env python3
"""Which configurations fit in which GPU memory budget (modeled), for Figure 3.

Reads analysis/memory_results.csv. A configuration "fits" when its modeled total is at or below the budget;
framework overhead is not modeled (see analysis/memory_assumptions.json, not_modeled).
Writes tables/fig3_feasibility.csv.
"""
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(REPO / "analysis" / "memory_results.csv", encoding="utf-8")))
BUDGETS = [8, 12, 16, 24, 40, 48, 80]


def label(r):
    m = {"full_ft": "Full FT", "lora": "LoRA", "qlora": "QLoRA"}[r["method"]]
    rk = f" r={r['rank']}" if r["rank"] else ""
    t = {"qv": " Q,V", "all": " all-linear", "all (full)": ""}[r["targets"]]
    opts = [o for o, k in (("DQ", "double_quant"), ("Flash", "flash_attention"), ("ckpt", "checkpointing")) if r[k] == "yes"]
    return f"{m}{rk}{t}" + (f" + {' + '.join(opts)}" if opts else "")


out = []
for w in ("W1", "W2"):
    for b in BUDGETS:
        fits = sorted((r for r in rows if r["workload"] == w and float(r["total_gb"]) <= b), key=lambda r: float(r["total_gb"]))
        by_method = {}
        for r in fits:
            by_method.setdefault(r["method"], r)
        out.append({"workload": w, "budget_gb": b, "n_configs_fit": len(fits),
                    "smallest_full_ft": f"{label(by_method['full_ft'])} ({by_method['full_ft']['total_gb']} GB)" if "full_ft" in by_method else "none",
                    "smallest_lora": f"{label(by_method['lora'])} ({by_method['lora']['total_gb']} GB)" if "lora" in by_method else "none",
                    "smallest_qlora": f"{label(by_method['qlora'])} ({by_method['qlora']['total_gb']} GB)" if "qlora" in by_method else "none",
                    "lora_without_ckpt_fits": "yes" if any(r["method"] == "lora" and r["checkpointing"] == "no" for r in fits) else "no",
                    "qlora_without_ckpt_fits": "yes" if any(r["method"] == "qlora" and r["checkpointing"] == "no" for r in fits) else "no"})
(REPO / "tables").mkdir(exist_ok=True)
with open(REPO / "tables" / "fig3_feasibility.csv", "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=list(out[0])); wr.writeheader(); wr.writerows(out)
for o in out:
    print(o["workload"], o["budget_gb"], o["n_configs_fit"], "|", o["smallest_qlora"], "|", o["smallest_lora"], "|", o["smallest_full_ft"], "| LoRA no-ckpt:", o["lora_without_ckpt_fits"], "QLoRA no-ckpt:", o["qlora_without_ckpt_fits"])
