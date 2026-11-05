#!/usr/bin/env python3
"""Table 4a (modeled memory) from analysis/memory_results.csv. No value typed by hand.

Writes tables/table4a_memory.csv. Totals for workload W1 (batch 4, sequence 2048) and W2 (batch 1, sequence 512).
"""
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(REPO / "analysis" / "memory_results.csv", encoding="utf-8")))


def pick(w, method, rank, targets, dq, flash, ckpt):
    for r in rows:
        if (r["workload"], r["method"], r["rank"], r["targets"], r["double_quant"], r["flash_attention"], r["checkpointing"]) == \
                (w, method, rank, targets, dq, flash, ckpt):
            return r
    raise LookupError((w, method, rank, targets, dq, flash, ckpt))


SPEC = [
    ("Full fine-tuning", "-", "all", "", "no", "no"),
    ("Full fine-tuning", "-", "all", "", "yes", "yes"),
    ("LoRA", "8", "qv", "", "yes", "yes"),
    ("LoRA", "32", "qv", "", "yes", "no"),
    ("LoRA", "32", "qv", "", "yes", "yes"),
    ("LoRA", "64", "qv", "", "yes", "yes"),
    ("LoRA", "128", "qv", "", "yes", "yes"),
    ("LoRA", "32", "all", "", "yes", "yes"),
    ("QLoRA (NF4, DQ)", "16", "qv", "yes", "yes", "yes"),
    ("QLoRA (NF4, DQ)", "32", "qv", "yes", "yes", "yes"),
    ("QLoRA (NF4, DQ)", "64", "all", "yes", "yes", "yes"),
]
METHOD = {"Full fine-tuning": "full_ft", "LoRA": "lora", "QLoRA (NF4, DQ)": "qlora"}
TARGET = {"qv": "Q, V", "all": "All linear"}
out = []
for name, rank, tgt, dq, flash, ckpt in SPEC:
    m = METHOD[name]; rk = "" if rank == "-" else rank; t = "all (full)" if m == "full_ft" else tgt
    w1 = pick("W1", m, rk, t, dq, flash, ckpt); w2 = pick("W2", m, rk, t, dq, flash, ckpt)
    out.append({
        "Method": name, "Rank": rank, "Targets": "All parameters" if m == "full_ft" else TARGET[tgt],
        "FlashAttention": flash, "Gradient checkpointing": ckpt,
        "Trainable params (%)": f"{float(w1['trainable_pct']):.2f}" if m != "full_ft" else "100",
        "Model states (GB)": w1["model_states_gb"], "Activations, W1 (GB)": w1["activations_gb"],
        "Total, W1 batch 4 seq 2048 (GB)": w1["total_gb"], "Total, W2 batch 1 seq 512 (GB)": w2["total_gb"],
        "config_ids": f"{w1['config_id']}; {w2['config_id']}",
    })
(REPO / "tables").mkdir(exist_ok=True)
with open(REPO / "tables" / "table4a_memory.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for r in out:
    print(" | ".join(str(v) for v in r.values()))
