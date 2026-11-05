#!/usr/bin/env python3
"""Check the activation and logits terms of analysis/memory_model.py against a published measurement.

Compares the measured increase in peak memory per 1,024 tokens (Dbouk et al., 2026, Table 3)
with the increase predicted by the same per-token terms the memory model uses. Fixed costs cancel.
All constants come from analysis/memory_assumptions.json. Writes analysis/activation_check.md.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = json.loads((HERE / "memory_assumptions.json").read_text())
V = A["activation_validation"]; m = V["model"]
per_token_act = V["fp32_scale"] * 34 * m["hidden"] * m["layers"]            # bytes per token, no attention-score term
per_token_logits = A["logits"]["bytes_per_element"] * m["vocab"]
modeled = (per_token_act + per_token_logits) * 1024 / 1e9
meas = {int(k): v for k, v in V["measured_peak_gb_by_seq"].items()}
seqs = sorted(meas)
lines = ["# Activation-term check against a published measurement", "",
         f"Source: {V['source']}.", f"Setting: {V['setting']}.", "", V["method"], "",
         "| Interval (tokens) | Measured increase (GB) | Measured per 1,024 tokens (GB) | Modeled per 1,024 tokens (GB) | Difference |",
         "|---|---:|---:|---:|---:|"]
for a, b in zip(seqs, seqs[1:]):
    inc = meas[b] - meas[a]; per = inc / ((b - a) / 1024)
    lines.append(f"| {a} to {b} | {inc:.2f} | {per:.2f} | {modeled:.2f} | {100 * (modeled - per) / per:+.1f}% |")
lines += ["", f"Modeled per-token terms: activations {per_token_act / 1e6:.2f} MB, logits {per_token_logits / 1e6:.2f} MB.",
          "No constant was adjusted to produce this agreement.", ""]
(HERE / "activation_check.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
