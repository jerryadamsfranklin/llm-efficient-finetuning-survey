#!/usr/bin/env python3
"""Figure 3: modeled method feasibility by GPU memory, and sourced starting hyperparameters.

Branch contents are read from tables/fig3_feasibility.csv (produced by figures/make_fig3_feasibility.py from
analysis/memory_results.csv); the lower panel is read from analysis/hyperparameter_sources.json.
Output: figures/output/fig3_decision_tree.png and .pdf
"""
import csv, json, textwrap
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO = Path(__file__).resolve().parents[1]
feas = {(r["workload"], int(r["budget_gb"])): r for r in csv.DictReader(open(REPO / "tables" / "fig3_feasibility.csv", encoding="utf-8"))}
res = list(csv.DictReader(open(REPO / "analysis" / "memory_results.csv", encoding="utf-8")))
hp = json.loads((REPO / "analysis" / "hyperparameter_sources.json").read_text())["entries"]
ft = next(r for r in res if r["workload"] == "W1" and r["method"] == "full_ft" and r["flash_attention"] == "yes" and r["checkpointing"] == "yes")
INK, MUTED, LINE, DARK = "#0b0b0b", "#52514e", "#8a8984", "#2e3440"
COL = {"none": "#e34948", "qlora": "#eb6834", "lora": "#2a78d6", "big": "#1baf7a", "ft": "#6250d6"}


def min_total(**kw):
    c = [float(r["total_gb"]) for r in res if r["workload"] == "W1" and all(r[k] == v for k, v in kw.items())]
    return min(c)


q = min_total(method="qlora"); l = min_total(method="lora")
l_nock = min_total(method="lora", checkpointing="no"); f = float(ft["total_gb"])
q_w2 = min(float(r["total_gb"]) for r in res if r["workload"] == "W2" and r["method"] == "qlora")
branches = [
    (f"Under {q:.1f} GB", COL["none"], "Nothing fits", f"Reduce batch or\nsequence length\n(batch 1, seq 512:\nQLoRA from {q_w2:.1f} GB)"),
    (f"{q:.1f} to {l:.1f} GB", COL["qlora"], "QLoRA", f"NF4, double quant.,\nFlashAttention,\ncheckpointing\n(from {q:.1f} GB)"),
    (f"{l:.1f} to {l_nock:.1f} GB", COL["lora"], "LoRA, 16-bit base", f"FlashAttention,\ncheckpointing\n(from {l:.1f} GB;\nrank 8 to 128 adds\nunder 1.5 GB)"),
    (f"{l_nock:.1f} to {f:.1f} GB", COL["big"], "LoRA without\ncheckpointing", f"FlashAttention only\n(from {l_nock:.1f} GB)"),
    (f"{f:.1f} GB and above", COL["ft"], "Full fine-tuning", f"FlashAttention,\ncheckpointing\n({f:.1f} GB): exceeds\none 80 GB GPU;\nshard with ZeRO"),
]
plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(11, 8.2), dpi=300)
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")


def box(x, y, w, h, edge, fill="#ffffff", lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fill, ec=edge, lw=lw))


box(25, 90, 50, 7, DARK, DARK)
ax.text(50, 94.6, "Available GPU memory", ha="center", va="center", color="white", fontsize=13, weight="bold")
ax.text(50, 91.7, "LLaMA-2-7B, batch 4, sequence 2048, bf16 (modeled)", ha="center", va="center", color="white", fontsize=8.5)
ax.plot([50, 50], [89.6, 87], color=LINE, lw=1.2)
xs = [1.5 + i * 19.7 for i in range(5)]; w = 17.4
ax.plot([xs[0] + w / 2, xs[-1] + w / 2], [87, 87], color=LINE, lw=1.2)
for x, (budget, col, title, body) in zip(xs, branches):
    cx = x + w / 2
    ax.plot([cx, cx], [87, 84.6], color=LINE, lw=1.2)
    box(x, 57, w, 27, col)
    ax.text(cx, 81.6, budget, ha="center", va="center", fontsize=9, weight="bold", color=col)
    ax.text(cx, 77.2, title, ha="center", va="center", fontsize=9.5, weight="bold", color=INK, linespacing=1.2)
    ax.text(cx, 65.8, body, ha="center", va="center", fontsize=8, color=INK, linespacing=1.35)
box(2, 3, 96, 46, DARK, "#f3f3f1")
ax.text(50, 45.2, "Starting hyperparameters reported in primary sources (not tuned recommendations)",
        ha="center", va="center", fontsize=10.5, weight="bold", color=DARK)
y = 40.5
for e in hp:
    lines = textwrap.wrap(e["text"], 125)
    for i, ln in enumerate(lines):
        ax.text(4.5, y, ("• " if i == 0 else "   ") + ln, ha="left", va="center", fontsize=8, color=INK)
        y -= 2.6
    ax.text(6.0, y, f"{e['source']}; {e['setting']}", ha="left", va="center", fontsize=7, color=MUTED, style="italic")
    y -= 4.0
fig.tight_layout()
out = REPO / "figures" / "output"; out.mkdir(parents=True, exist_ok=True)
fig.savefig(out / "fig3_decision_tree.png", dpi=300, facecolor="white")
fig.savefig(out / "fig3_decision_tree.pdf", facecolor="white")
print("wrote", out / "fig3_decision_tree.png")
