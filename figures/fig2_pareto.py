#!/usr/bin/env python3
"""Figure 2: Memory–accuracy Pareto frontier for 7B fine-tuning configurations.

Data match the corrected manuscript Table 4 (Full FT memory = 112 GB).
Label placement uses manual per-point offsets with leader lines so the dense
12–22 GB / ~98% cluster does not overlap.

Usage:
    python figures/fig2_pareto.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

OUT_DIR = Path(__file__).resolve().parent / "output"
DPI = 300

# Exact Table 4 midpoints — do not alter
POINTS = [
    # label, memory_gb, accuracy_pct, family
    ("Full FT", 112, 100.0, "full"),
    ("LoRA r=8", 18, 96.5, "lora"),
    ("LoRA r=32", 22, 98.5, "lora"),
    ("LoRA r=64", 28, 99.2, "lora"),
    ("LoRA r=128", 35, 99.8, "lora"),
    ("QLoRA r=16", 6, 96.0, "qlora"),
    ("QLoRA r=32", 8, 97.0, "qlora"),
    ("QLoRA r=32 +FlashAttn", 12, 98.0, "qlora"),
    ("QLoRA+Ckpt+Flash", 5, 97.0, "qlora"),
    ("Adapters (b=64)", 20, 97.5, "adapter"),
    ("Prefix Tuning", 16, 93.5, "prefix"),
]

# Non-dominated path as specified (labels match POINTS; FlashAttn point is QLoRA)
PARETO_ORDER = [
    "QLoRA+Ckpt+Flash",
    "QLoRA r=32",
    "QLoRA r=32 +FlashAttn",
    "LoRA r=64",
    "LoRA r=128",
    "Full FT",
]

# Manual annotation offsets in axis-fraction of the data range (log-x, linear-y).
# Tuned for the dense 12–22 GB / 97–99% cluster; leader lines drawn when offset is large.
# Values are (dx_in_log10_space_fraction_of_span, dy_percentage_points)
# (dx as fraction of log10 x-span, dy in percentage points)
# Dense cluster (12–22 GB / ~97–99%): FlashAttn up-left, LoRA r=32 up-right,
# Adapters down-right, LoRA r=8 down-left — keeps leader lines from crossing.
LABEL_OFFSETS = {
    "Full FT": (-0.06, -1.55),
    "LoRA r=8": (-0.12, -1.55),
    "LoRA r=32": (0.12, 1.35),
    "LoRA r=64": (0.0, 1.15),
    "LoRA r=128": (0.12, -1.35),
    "QLoRA r=16": (0.08, -1.50),
    "QLoRA r=32": (0.14, 1.15),
    "QLoRA r=32 +FlashAttn": (0.10, 1.70),   # above-right; avoid left clip
    "QLoRA+Ckpt+Flash": (0.14, 1.35),
    "Adapters (b=64)": (0.16, -1.50),
    "Prefix Tuning": (0.08, -1.10),          # keep above y=92
}

FAMILY_STYLE = {
    "full": dict(marker="*", color="#000000", s=220, zorder=6),
    "lora": dict(marker="o", color="#0072B2", s=70, zorder=5),
    "qlora": dict(marker="s", color="#D55E00", s=70, zorder=5),
    "adapter": dict(marker="^", color="#009E73", s=90, zorder=5),
    "prefix": dict(marker="D", color="#CC79A7", s=70, zorder=5),
}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_label = {p[0]: p for p in POINTS}

    fig, ax = plt.subplots(figsize=(9.2, 6.2))

    # Memory bands (log-x)
    ax.axvspan(4.5, 10, color="#FCE8E6", alpha=0.85, zorder=0)
    ax.axvspan(10, 24, color="#E8F1FB", alpha=0.85, zorder=0)
    ax.axvspan(24, 130, color="#E6F5EF", alpha=0.85, zorder=0)

    # Band labels sit high but clear of point annotations
    ax.text(7.0, 100.35, "Extreme (<10 GB)", ha="center", va="top", fontsize=8,
            color="#9B3A2F", fontfamily="sans-serif")
    ax.text(15.5, 100.35, "Moderate (10–24 GB)", ha="center", va="top", fontsize=8,
            color="#2F5F8F", fontfamily="sans-serif")
    ax.text(55, 100.35, "Abundant (>24 GB)", ha="center", va="top", fontsize=8,
            color="#1F6B4A", fontfamily="sans-serif")

    # Pareto frontier
    px = [by_label[n][1] for n in PARETO_ORDER]
    py = [by_label[n][2] for n in PARETO_ORDER]
    ax.plot(px, py, linestyle="--", color="#4B5563", linewidth=1.4, zorder=2, label="_nolegend_")

    # Scatter by family
    for label, mem, acc, family in POINTS:
        style = FAMILY_STYLE[family]
        ax.scatter([mem], [acc], **style, edgecolors="white", linewidths=0.6)

    # Labels with leader lines
    x_lo, x_hi = np.log10(5), np.log10(120)
    for label, mem, acc, _family in POINTS:
        dx_frac, dy = LABEL_OFFSETS[label]
        # Convert fractional log-span offset to a multiplicative x shift
        log_x = np.log10(mem)
        log_target = log_x + dx_frac * (x_hi - x_lo)
        x_text = 10 ** log_target
        y_text = acc + dy

        # Leader line when offset is material
        if abs(dx_frac) > 0.02 or abs(dy) > 0.4:
            ax.annotate(
                "",
                xy=(mem, acc),
                xytext=(x_text, y_text),
                arrowprops=dict(
                    arrowstyle="-",
                    color="#6B7280",
                    lw=0.7,
                    shrinkA=0,
                    shrinkB=4,
                ),
                zorder=3,
            )

        ax.text(
            x_text,
            y_text,
            label,
            ha="center",
            va="center",
            fontsize=7.5,
            fontfamily="sans-serif",
            color="#1F2937",
            zorder=7,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
        )

    ax.set_xscale("log")
    ax.set_xlim(5, 120)
    ax.set_ylim(92.2, 100.7)
    ax.set_xticks([5, 10, 20, 40, 80, 120])
    ax.set_xticklabels(["5", "10", "20", "40", "80", "120"])
    ax.set_xlabel("Peak training memory for a 7B model (GB, log scale)", fontsize=11, fontfamily="sans-serif")
    ax.set_ylabel("Accuracy retention relative to full fine-tuning (%)", fontsize=11, fontfamily="sans-serif")
    ax.grid(True, which="both", linestyle=":", linewidth=0.6, color="#9CA3AF", alpha=0.7, zorder=1)
    ax.tick_params(labelsize=9)

    legend_elements = [
        Line2D([0], [0], marker="*", color="w", markerfacecolor="black", markersize=14, label="Full fine-tuning"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#0072B2", markersize=9, label="LoRA family"),
        Line2D([0], [0], marker="^", color="w", markerfacecolor="#009E73", markersize=10, label="Adapter-based"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor="#CC79A7", markersize=8, label="Prompt/prefix tuning"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#D55E00", markersize=9, label="QLoRA family"),
        Line2D([0], [0], linestyle="--", color="#4B5563", linewidth=1.4, label="Pareto frontier"),
    ]
    ax.legend(
        handles=legend_elements,
        loc="lower right",
        fontsize=8.5,
        framealpha=0.95,
        fancybox=True,
        edgecolor="#D1D5DB",
    )

    fig.tight_layout()
    png_path = OUT_DIR / "fig2_pareto.png"
    pdf_path = OUT_DIR / "fig2_pareto.pdf"
    fig.savefig(png_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {png_path}")
    print(f"wrote {pdf_path}")


if __name__ == "__main__":
    main()
