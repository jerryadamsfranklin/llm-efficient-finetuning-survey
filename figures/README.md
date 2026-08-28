# Figures

Publication figures for the PeerJ CS survey. Each script is self-contained.

```bash
pip install -r figures/requirements.txt
python figures/fig1_taxonomy.py
python figures/fig2_pareto.py
python figures/fig3_decision_tree.py
```

Outputs (PNG at 300 DPI + PDF) land in `figures/output/`.

| Script | Output | Notes |
|---|---|---|
| `fig1_taxonomy.py` | Four-column method taxonomy | Colorblind-safe Okabe–Ito palette |
| `fig2_pareto.py` | Memory–accuracy Pareto frontier | Exact Table 4 midpoints; manual label offsets + leader lines |
| `fig3_decision_tree.py` | Method-selection decision tree | Boxes sized from text metrics + padding |
