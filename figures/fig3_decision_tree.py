#!/usr/bin/env python3
"""Figure 3: Method-selection decision framework.

Top-down flowchart. Every box is sized from its rendered text metrics plus padding
so labels never overflow. Saves PNG (300 DPI) and PDF to figures/output/.

Usage:
    python figures/fig3_decision_tree.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT_DIR = Path(__file__).resolve().parent / "output"
DPI = 300

NAVY = "#2D3446"
RED = "#D55E00"
BLUE = "#0072B2"
GREEN = "#009E73"
PURPLE = "#7B5EA7"
GRAY = "#6B7280"
LIGHT_GRAY = "#F3F4F6"
EDGE_GRAY = "#4B5563"


def measure_text(fig, text: str, fontsize: float, weight: str = "normal",
                 family: str = "sans-serif") -> tuple[float, float]:
    """Return (width, height) in inches for multi-line text."""
    tmp = fig.text(0, 0, text, fontsize=fontsize, fontweight=weight,
                   fontfamily=family, linespacing=1.25)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbox = tmp.get_window_extent(renderer=renderer)
    tmp.remove()
    # Convert pixels → inches
    w_in = bbox.width / fig.dpi
    h_in = bbox.height / fig.dpi
    return w_in, h_in


def draw_box(ax, cx, cy, w, h, facecolor, edgecolor, lw=1.6, radius=0.08):
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        zorder=3,
    )
    ax.add_patch(patch)
    return patch


def text_block(ax, cx, cy, text, fontsize, color, weight="normal"):
    ax.text(
        cx, cy, text,
        ha="center", va="center",
        fontsize=fontsize, color=color, fontweight=weight,
        fontfamily="sans-serif", linespacing=1.25, zorder=4,
    )


def sized_box(fig, ax, cx, cy, title, body_lines, edgecolor, title_color,
              title_size=10, body_size=8.2, pad_x=0.28, pad_y=0.18,
              face="white", title_weight="bold"):
    """Draw a box sized to fit title + body with padding. Returns (w, h)."""
    title_w, title_h = measure_text(fig, title, title_size, weight=title_weight)
    if body_lines:
        body = "\n".join(body_lines)
        body_w, body_h = measure_text(fig, body, body_size)
        gap = 0.06
    else:
        body_w = body_h = 0.0
        gap = 0.0

    w = max(title_w, body_w) + 2 * pad_x
    h = title_h + body_h + gap + 2 * pad_y
    draw_box(ax, cx, cy, w, h, face, edgecolor, lw=1.8)

    if body_lines:
        # Title above vertical center, body below
        total_content = title_h + gap + body_h
        top = cy + total_content / 2
        title_cy = top - title_h / 2
        body_cy = top - title_h - gap - body_h / 2
        text_block(ax, cx, title_cy, title, title_size, title_color, weight=title_weight)
        text_block(ax, cx, body_cy, "\n".join(body_lines), body_size, "#1F2937")
    else:
        text_block(ax, cx, cy, title, title_size, title_color, weight=title_weight)
    return w, h


def elbow(ax, x0, y0, x1, y1):
    """Orthogonal connector: vertical then horizontal then vertical."""
    mid_y = (y0 + y1) / 2
    ax.plot([x0, x0, x1, x1], [y0, mid_y, mid_y, y1], color=GRAY, lw=1.3, zorder=1)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11.0, 9.2))
    # Use inch-like coordinates matching figsize for predictable sizing
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9.2)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Force a draw so text metrics work
    fig.canvas.draw()

    # --- Level 1: GPU memory question ---
    l1_x, l1_y = 5.5, 8.55
    w1, h1 = sized_box(
        fig, ax, l1_x, l1_y,
        "Available GPU memory?", [],
        NAVY, "white", title_size=12, pad_x=0.35, pad_y=0.22, face=NAVY,
    )

    # Branch labels + method boxes
    branches = [
        {
            "x": 2.0,
            "label": "< 10 GB",
            "label_color": RED,
            "title": "QLoRA",
            "title_color": RED,
            "edge": RED,
            "body": [
                "rank 16–32, NF4",
                "+ double quantization",
                "+ gradient checkpointing",
                "+ FlashAttention",
            ],
        },
        {
            "x": 5.5,
            "label": "10–24 GB",
            "label_color": BLUE,
            "title": "LoRA",
            "title_color": BLUE,
            "edge": BLUE,
            "body": [
                "rank 32–64, Q,V projections",
                "+ FlashAttention",
                "(general-purpose default)",
            ],
        },
        {
            "x": 9.0,
            "label": "> 24 GB",
            "label_color": GREEN,
            "title": "LoRA (high rank)",
            "title_color": GREEN,
            "edge": GREEN,
            "body": [
                "rank 64–128",
                "or larger batch size",
                "compare vs full FT",
            ],
        },
    ]

    method_y = 6.55
    method_boxes = []
    for b in branches:
        w, h = sized_box(
            fig, ax, b["x"], method_y,
            b["title"], b["body"],
            b["edge"], b["title_color"],
            title_size=11, body_size=8.0, pad_x=0.30, pad_y=0.20,
        )
        method_boxes.append((b["x"], method_y, w, h, b))
        # Connector from L1
        top = method_y + h / 2
        elbow(ax, l1_x, l1_y - h1 / 2, b["x"], top)
        # Branch label beside the drop
        label_y = (l1_y - h1 / 2 + top) / 2 + 0.15
        ax.text(
            b["x"], label_y, b["label"],
            ha="center", va="bottom", fontsize=9, fontweight="bold",
            color=b["label_color"], fontfamily="sans-serif", zorder=5,
            bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.92),
        )

    # --- Level 2: Task characteristics ---
    l2_x, l2_y = 5.5, 4.55
    w2, h2 = sized_box(
        fig, ax, l2_x, l2_y,
        "Task characteristics?", [],
        NAVY, "white", title_size=12, pad_x=0.35, pad_y=0.22, face=NAVY,
    )

    # Converge from method boxes to L2
    for x, y, w, h, _b in method_boxes:
        elbow(ax, x, y - h / 2, l2_x, l2_y + h2 / 2)

    tasks = [
        {
            "x": 2.0,
            "title": "Large domain shift",
            "body": [
                "increase rank to 64–128",
                "target all modules",
                "higher warmup (10%)",
            ],
        },
        {
            "x": 5.5,
            "title": "Small dataset (<10k)",
            "body": [
                "reduce rank to 16",
                "dropout 0.1",
                "early stopping",
            ],
        },
        {
            "x": 9.0,
            "title": "Long-form generation",
            "body": [
                "expect wider gap to",
                "full fine-tuning; verify",
                "against FT baseline",
            ],
        },
    ]

    task_y = 2.85
    task_boxes = []
    for t in tasks:
        w, h = sized_box(
            fig, ax, t["x"], task_y,
            t["title"], t["body"],
            PURPLE, PURPLE,
            title_size=10, body_size=8.0, pad_x=0.28, pad_y=0.18,
        )
        task_boxes.append((t["x"], task_y, w, h))
        elbow(ax, l2_x, l2_y - h2 / 2, t["x"], task_y + h / 2)

    # --- Bottom panel: common defaults ---
    defaults_title = "Common defaults across all branches"
    # Wrap body into two lines for fit
    defaults_lines = [
        "alpha = 2 × rank  |  learning rate 1e-4 to 5e-4 (start 2e-4)  |  AdamW, weight decay 0.01–0.1",
        "gradient clipping 1.0  |  FlashAttention enabled where supported",
    ]
    def_y = 1.15
    tw, th = measure_text(fig, defaults_title, 10, weight="bold")
    bw, bh = measure_text(fig, "\n".join(defaults_lines), 7.8)
    def_w = max(tw, bw) + 0.55
    def_h = th + bh + 0.14 + 0.36
    # Cap width to axes
    def_w = min(def_w, 10.2)
    draw_box(ax, 5.5, def_y, def_w, def_h, LIGHT_GRAY, EDGE_GRAY, lw=1.5, radius=0.06)
    total = th + 0.08 + bh
    top = def_y + total / 2
    text_block(ax, 5.5, top - th / 2, defaults_title, 10, EDGE_GRAY, weight="bold")
    text_block(ax, 5.5, top - th - 0.08 - bh / 2, "\n".join(defaults_lines), 7.8, "#1F2937")

    # Lines from task boxes into defaults panel
    for x, y, w, h in task_boxes:
        ax.plot([x, x, 5.5], [y - h / 2, def_y + def_h / 2 + 0.15, def_y + def_h / 2],
                color=GRAY, lw=1.1, zorder=1)

    # Caption
    ax.text(
        5.5, 0.28,
        "Memory thresholds assume a 7B-parameter model under supervised fine-tuning. "
        "Values follow the configurations in Table 5.",
        ha="center", va="center", fontsize=8, fontstyle="italic",
        color="#4B5563", fontfamily="sans-serif",
    )

    fig.tight_layout(pad=0.3)
    png_path = OUT_DIR / "fig3_decision_tree.png"
    pdf_path = OUT_DIR / "fig3_decision_tree.pdf"
    fig.savefig(png_path, dpi=DPI, bbox_inches="tight", facecolor="white")
    fig.savefig(pdf_path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {png_path}")
    print(f"wrote {pdf_path}")


if __name__ == "__main__":
    main()
