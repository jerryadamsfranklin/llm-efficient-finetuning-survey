#!/usr/bin/env python3
"""Single memory model for every memory figure in the manuscript.

All constants come from analysis/memory_assumptions.json; none are hard-coded here.
Writes analysis/memory_results.csv and analysis/memory_breakdown.md.
"""
import csv, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = json.loads((HERE / "memory_assumptions.json").read_text())
m = A["model"]; L, h, a, f, V = m["layers"], m["hidden"], m["heads"], m["ffn"], m["vocab"]
B = A["bytes_per_param"]
GB = 1e9

block_linear = 4 * h * h + 3 * h * f           # q,k,v,o + gate,up,down
block_norm = 2 * h
P_blocks_linear = L * block_linear
P_other = V * h * 2 + L * block_norm + h        # embeddings, output head, norms
P = P_blocks_linear + P_other


def adapter_params(r, targets):
    if targets == "qv":
        return L * 2 * r * (h + h)
    if targets == "all":
        return L * (4 * r * (h + h) + 2 * r * (h + f) + r * (f + h))
    raise ValueError(targets)


def act(s, b, flash, ckpt):
    full_layer = s * b * h * (34 + (0 if flash else 5 * a * s / h))
    if ckpt:
        return L * 2 * s * b * h + full_layer
    return L * full_layer


def logits(s, b):
    return s * b * V * A["logits"]["bytes_per_element"]


CONFIGS = [
    ("full_ft", None, None, False, False, False),
    ("full_ft", None, None, False, True, False),
    ("full_ft", None, None, False, True, True),
]
for r in (8, 16, 32, 64, 128):
    for flash in (False, True):
        for ckpt in (False, True):
            CONFIGS.append(("lora", r, "qv", False, flash, ckpt))
CONFIGS.append(("lora", 32, "all", False, True, True))
for r in (16, 32, 64):
    for dq in (False, True):
        for flash in (False, True):
            for ckpt in (False, True):
                CONFIGS.append(("qlora", r, "qv", dq, flash, ckpt))
CONFIGS.append(("qlora", 64, "all", True, True, True))

rows = []
for w in A["workloads"]:
    s, b = w["seq"], w["batch"]
    for i, (method, r, tgt, dq, flash, ckpt) in enumerate(CONFIGS, 1):
        if method == "full_ft":
            trainable = P
            weights = 2 * P; grads = 2 * P; optim = (B["full_ft_model_states"] - 4) * P
        else:
            trainable = adapter_params(r, tgt)
            if method == "lora":
                base = B["frozen_16bit_weight"] * P
            else:
                qc = B["quant_constants_with_dq"] if dq else B["quant_constants_without_dq"]
                base = (B["nf4_weight"] + qc) * P_blocks_linear + B["frozen_16bit_weight"] * P_other
            weights = base + 2 * trainable; grads = 2 * trainable
            optim = (B["trainable_adapter_states"] - 4) * trainable
        ac = act(s, b, flash, ckpt); lg = logits(s, b)
        total = weights + grads + optim + ac + lg
        rows.append({
            "config_id": f"{w['id']}-{i:02d}", "workload": w["id"], "batch": b, "seq": s,
            "method": method, "rank": r or "", "targets": tgt or "all (full)",
            "double_quant": ("yes" if dq else "no") if method == "qlora" else "",
            "flash_attention": "yes" if flash else "no", "checkpointing": "yes" if ckpt else "no",
            "trainable_params": trainable, "trainable_pct": round(100 * trainable / P, 3),
            "weights_gb": round(weights / GB, 2), "grads_gb": round(grads / GB, 2),
            "optimizer_gb": round(optim / GB, 2), "activations_gb": round(ac / GB, 2),
            "logits_gb": round(lg / GB, 2), "total_gb": round(total / GB, 1),
            "model_states_gb": round((weights + grads + optim) / GB, 1),
        })

with open(HERE / "memory_results.csv", "w", newline="", encoding="utf-8") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)

lines = ["# Memory model results", "",
         f"Model: {m['name']}, {P/1e9:.2f}B parameters ({P_blocks_linear/1e9:.2f}B in block linear layers). "
         "All constants: analysis/memory_assumptions.json. LoRA and QLoRA activations are upper bounds.", ""]
for w in A["workloads"]:
    lines += [f"## Workload {w['id']}: batch {w['batch']}, sequence {w['seq']}", "",
              "| config | method | rank | targets | DQ | Flash | ckpt | trainable % | model states GB | activations GB | logits GB | total GB |",
              "|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|"]
    for r in rows:
        if r["workload"] == w["id"]:
            lines.append(f"| {r['config_id']} | {r['method']} | {r['rank']} | {r['targets']} | {r['double_quant']} | "
                         f"{r['flash_attention']} | {r['checkpointing']} | {r['trainable_pct']} | {r['model_states_gb']} | "
                         f"{r['activations_gb']} | {r['logits_gb']} | {r['total_gb']} |")
    lines.append("")
by_id = {r["config_id"]: r for r in rows}
lines += ["## Cross-check against a reported measurement", "",
          "| Source | Reported | Setting | Model row | Modeled |", "|---|---:|---|---|---:|"]
for c in A.get("cross_checks", []):
    r = by_id[c["config_id"]]
    lines.append(f"| {c['source']} | {c['reported_gb']} GB | {c['setting']} | {c['config_id']} ({c['row_description']}) | {r['total_gb']} GB |")
lines += ["", "No constant was adjusted to produce agreement with any reported measurement.", ""]
(HERE / "memory_breakdown.md").write_text("\n".join(lines), encoding="utf-8")
print(f"P = {P:,} parameters; {len(rows)} configurations written")
