#!/usr/bin/env python3
"""Figure 2: modeled peak training memory by component, LLaMA-2-7B, batch 4, sequence 2048.

Every value is read from analysis/memory_results.csv (produced by analysis/memory_model.py).
No value is typed into this script. Configurations are selected by their attributes.
Output: figures/output/fig2_memory_breakdown.png and .pdf
"""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "figures" / "output"
rows = list(csv.DictReader(open(REPO / "analysis" / "memory_results.csv", encoding="utf-8")))


def pick(method, rank, targets, dq, flash, ckpt):
    for r in rows:
        if (r["workload"] == "W1" and r["method"] == method and r["rank"] == rank and r["targets"] == targets
                and r["double_quant"] == dq and r["flash_attention"] == flash and r["checkpointing"] == ckpt):
            return r
    raise LookupError((method, rank, targets, dq, flash, ckpt))


SELECT = [  # (label, selector), drawn top to bottom
    ("Full fine-tuning", ("full_ft", "", "all (full)", "", "no", "no")),
    ("Full fine-tuning + Flash + ckpt", ("full_ft", "", "all (full)", "", "yes", "yes")),
    ("LoRA r=32 (Q,V)", ("lora", "32", "qv", "", "no", "no")),
    ("LoRA r=32 (Q,V) + Flash", ("lora", "32", "qv", "", "yes", "no")),
    ("LoRA r=32 (Q,V) + Flash + ckpt", ("lora", "32", "qv", "", "yes", "yes")),
    ("QLoRA r=32 (Q,V)", ("qlora", "32", "qv", "yes", "no", "no")),
    ("QLoRA r=32 (Q,V) + Flash", ("qlora", "32", "qv", "yes", "yes", "no")),
    ("QLoRA r=32 (Q,V) + Flash + ckpt", ("qlora", "32", "qv", "yes", "yes", "yes")),
]
COMPONENTS = [("weights_gb", "Weights", "#2a78d6"), ("grads_gb", "Gradients", "#eb6834"),
              ("optimizer_gb", "Optimizer states", "#1baf7a"), ("activations_gb", "Activations", "#eda100"),
              ("logits_gb", "Output logits", "#e87ba4")]
INK, MUTED, SURFACE = "#0b0b0b", "#52514e", "#ffffff"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)
fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
data = [(lab, pick(*sel)) for lab, sel in SELECT]
ys = list(range(len(data)))[::-1]
for y, (lab, r) in zip(ys, data):
    left = 0.0
    for key, _, color in COMPONENTS:
        v = float(r[key])
        if v > 0:
            ax.barh(y, v, left=left, height=0.62, color=color, edgecolor=SURFACE, linewidth=1.0)
        left += v
    ax.text(left + 2, y, f"{float(r['total_gb']):.1f} GB", va="center", ha="left", color=INK, fontsize=8.5)
ax.set_yticks(ys); ax.set_yticklabels([d[0] for d in data], color=INK)
ax.set_xlabel("Modeled peak training memory (GB)", color=INK)
ax.set_xlim(0, max(float(r["total_gb"]) for _, r in data) * 1.15)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(MUTED); ax.tick_params(axis="x", colors=MUTED); ax.tick_params(axis="y", length=0)
ax.xaxis.grid(True, color="#e6e5e1", linewidth=0.6); ax.set_axisbelow(True)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in COMPONENTS]
ax.legend(handles, [n for _, n, _ in COMPONENTS], loc="lower left", bbox_to_anchor=(-0.02, 1.0), ncol=5,
          frameon=False, fontsize=8, handlelength=1.2, columnspacing=1.0)
fig.tight_layout()
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "fig2_memory_breakdown.png", dpi=300, facecolor=SURFACE)
fig.savefig(OUT / "fig2_memory_breakdown.pdf", facecolor=SURFACE)
print("wrote", OUT / "fig2_memory_breakdown.png")
