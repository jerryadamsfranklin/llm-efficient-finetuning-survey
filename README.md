# Fine-Tuning Large Language Models in Resource-Constrained Environments

Companion repository for the survey "Fine-Tuning Large Language Models in
Resource-Constrained Environments: Methods and Trade-offs" (under review,
PeerJ Computer Science).

## Contents

- `protocol/` — search protocol, inclusion criteria, extraction schema (written before searching)
- `search/` — query definitions, search log, raw API responses, search scripts
- `screening/` — screening decisions for every candidate, PRISMA-style counts
- `data/` — final corpus, table data as CSV, BibTeX references
- `figures/` — figure generation scripts and outputs
- `docs/` — Table 4 per-column sourcing and provenance

## Status

| Phase | Status |
|---|---|
| **1 — Protocol design** | Complete. Protocol v1.0 locked in `protocol/` and `search/queries.yaml` (committed before any search). |
| **2 — Execute searches** | Automated discovery complete on branch `phase-2-search`. Manual sources and existing-corpus venue check still open. |
| **3+** | Not started. |

### Phase 2 checklist

- [x] arXiv automated search — 18/18 queries → `search/raw/arxiv/`
- [x] Semantic Scholar automated search — 18/18 queries → `search/raw/semanticscholar/`
- [x] OpenReview automated search — 18/18 queries → `search/raw/openreview/`
- [ ] Manual Google Scholar / IEEE Xplore / ACM DL logging (owner; no scraping)
- [ ] Fill `search/existing-references.yaml` (~42 manuscript refs) and run OpenReview venue check

Search dates and per-query counts are recorded in `search/search-log.md`. Several queries hit the protocol 200-result cap (noted in the log).

## Reproducing the search

```bash
pip install -r search/scripts/requirements.txt

# Automated discovery (re-runnable; skips existing raw files unless --force)
python search/scripts/search_arxiv.py
python search/scripts/search_semanticscholar.py
python search/scripts/search_openreview.py

# Optional: venue-upgrade check for the existing ~42 manuscript references
# (fill search/existing-references.yaml first)
python search/scripts/search_openreview.py --check-existing
```

Optional: set `SEMANTIC_SCHOLAR_API_KEY` to raise Semantic Scholar rate limits.

Each run updates `search/search-log.md` and writes `search/raw/<source>/<block>_<n>.json`.

## Data provenance

Table 4 combines values from primary sources with author estimates. See
`docs/table4-sourcing.md` for per-column provenance.

## Citation

See `CITATION.cff`.

## License

[CC-BY-4.0](LICENSE)
