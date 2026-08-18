# Table 4 — Per-Column Sourcing and Provenance

**Status:** Phase 5 placeholder — per-column attribution not yet ported. Disclosure
language below matches the manuscript Table 4 footnote.

Table 4 combines values from primary sources with author estimates. Relative
speed multipliers, cost figures, and combined-configuration memory values are
author estimates, not measurements from a single controlled experiment.

| Column | Source type | Notes |
|---|---|---|
| TBD | primary / estimate | Per-column analysis to be added in Phase 5 |

## Values fixed when this file is populated (Phase 5)

When the per-column table is completed, these manuscript values must be preserved:

- **Full fine-tuning memory:** **112 GB** for a ~7B LLaMA-family model under mixed-precision
  AdamW (Rajbhandari et al., 2020). Do **not** use 132 GB — that figure was corrected in the
  manuscript abstract and Table 4.
- **Accuracy retention:** task-dependent bands, not a single controlled evaluation across rows.

## Forward notes (Phase 4 CSV population)

When `data/table4_master_comparison.csv` is populated, use the 112 GB full-fine-tuning
baseline and task-dependent accuracy bands consistent with the corrected manuscript Table 4.

When `data/table2_lora_variants.csv` is populated, include verified rows for **PiSSA**
(Meng, Wang, & Zhang, 2024), **LoRA-GA** (Wang, Yu, & Li, 2024), and **HydraLoRA**
(Tian et al., 2024), matching the manuscript Table 2 insertions.
