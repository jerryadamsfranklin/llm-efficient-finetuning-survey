#!/usr/bin/env python3
"""Figure 1: Taxonomy of resource-efficient LLM fine-tuning methods.

Four-column horizontal taxonomy tree. Saves PNG (300 DPI) and PDF to figures/output/.

Usage:
    python figures/fig1_taxonomy.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT_DIR = Path(__file__).resolve().parent / "output"
DPI = 300

# Colorblind-safe categorical palette (Okabe–Ito inspired)
COLORS = {
    "root": "#2D3446",
    "peft": "#0072B2",
    "quant": "#D55E00",
    "memory": "#009E73",
    "federated": "#CC79A7",
    "line": "#6B7280",
    "caption": "#4B5563",
    "box_fill": "#FFFFFF",
}


def rounded_box(ax, x, y, w, h, facecolor, edgecolor, linewidth=1.5, radius=0.02):
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        mutation_aspect=1.0,
        zorder=3,
    )
    ax.add_patch(patch)
    return patch


def text_in_box(ax, x, y, text, fontsize, color, weight="normal", linespacing=1.25):
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        fontweight=weight,
        fontfamily="sans-serif",
        linespacing=linespacing,
        zorder=4,
        wrap=False,
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12.0, 7.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.2)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # --- Root ---
    root_x, root_y = 6.0, 6.55
    root_w, root_h = 5.2, 0.55
    rounded_box(ax, root_x, root_y, root_w, root_h, COLORS["root"], COLORS["root"], radius=0.04)
    text_in_box(ax, root_x, root_y, "Resource-Efficient LLM Fine-Tuning", 13, "white", weight="bold")

    columns = [
        {
            "x": 1.55,
            "color": COLORS["peft"],
            "header": "Parameter-Efficient\nFine-Tuning",
            "items": [
                "Additive\n(Adapters, Prompt/Prefix)",
                "Reparameterized\n(LoRA, AdaLoRA, DoRA,\nVeRA, LoRA+)",
                "Selective\n(BitFit, IA³)",
            ],
        },
        {
            "x": 4.5,
            "color": COLORS["quant"],
            "header": "Quantization",
            "items": [
                "Post-Training (PTQ)\n(GPTQ, AWQ,\nSmoothQuant)",
                "Quantization-Aware\nTraining (QAT)",
                "Hybrid\n(QLoRA, NF4)",
            ],
        },
        {
            "x": 7.5,
            "color": COLORS["memory"],
            "header": "Memory\nOptimization",
            "items": [
                "Gradient\nCheckpointing",
                "FlashAttention\n1 / 2",
                "Offloading\n(ZeRO, DeepSpeed)",
            ],
        },
        {
            "x": 10.45,
            "color": COLORS["federated"],
            "header": "Distributed &\nFederated",
            "items": [
                "Parallelism\n(Data, Pipeline, Tensor)",
                "Federated Learning\n(FedAvg)",
                "Federated PEFT\n(FlexLoRA, FLoRA)",
            ],
        },
    ]

    header_y = 5.35
    header_w, header_h = 2.55, 0.85
    item_w = 2.55
    # Item heights sized for content (middle PEFT/PTQ need more lines)
    item_heights = [0.85, 1.05, 0.75]
    item_gap = 0.18
    first_item_top = header_y - header_h / 2 - 0.35

    # Trunk from root to horizontal bar
    bar_y = header_y + header_h / 2 + 0.28
    ax.plot([root_x, root_x], [root_y - root_h / 2, bar_y], color=COLORS["line"], lw=1.4, zorder=1)
    xs = [c["x"] for c in columns]
    ax.plot([xs[0], xs[-1]], [bar_y, bar_y], color=COLORS["line"], lw=1.4, zorder=1)

    for col in columns:
        x = col["x"]
        color = col["color"]

        # Drop to header
        ax.plot([x, x], [bar_y, header_y + header_h / 2], color=COLORS["line"], lw=1.4, zorder=1)

        rounded_box(ax, x, header_y, header_w, header_h, color, color, radius=0.04)
        text_in_box(ax, x, header_y, col["header"], 10, "white", weight="bold", linespacing=1.15)

        y = first_item_top
        for item, h in zip(col["items"], item_heights):
            cy = y - h / 2
            # Connector from header / previous
            ax.plot([x, x], [y + 0.02, cy + h / 2], color=COLORS["line"], lw=1.1, zorder=1)
            rounded_box(ax, x, cy, item_w, h, COLORS["box_fill"], color, linewidth=1.6, radius=0.03)
            text_in_box(ax, x, cy, item, 8.5, "#1F2937", linespacing=1.2)
            y = cy - h / 2 - item_gap

    # Caption
    ax.text(
        6.0,
        0.35,
        "Categories address different resource bottlenecks and are largely complementary; "
        "production configurations combine methods across columns.",
        ha="center",
        va="center",
        fontsize=8.5,
        color=COLORS["caption"],
        fontstyle="italic",
        fontfamily="sans-serif",
        wrap=True,
    )

    fig.tight_layout(pad=0.4)
    png_path = OUT_DIR / "fig1_taxonomy.png"
    pdf_path = OUT_DIR / "fig1_taxonomy.pdf"
    fig.savefig(png_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {png_path}")
    print(f"wrote {pdf_path}")


if __name__ == "__main__":
    main()
