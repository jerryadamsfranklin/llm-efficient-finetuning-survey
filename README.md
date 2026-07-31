# Fine-Tuning Large Language Models in Resource-Constrained Environments

Companion repository for the survey "Fine-Tuning Large Language Models in
Resource-Constrained Environments: Methods and Trade-offs" (under review,
PeerJ Computer Science).

## Contents

- `protocol/` — search protocol, inclusion criteria, extraction schema, changelog
- `search/` — query definitions, search log, raw API responses, search scripts
- `screening/` — screening decisions for every candidate, PRISMA-style counts
- `data/` — final corpus, table data as CSV, BibTeX references
- `figures/` — figure generation scripts and outputs
- `docs/` — Table 4 provenance and reference-correction notes

## Status

| Phase | Status |
|---|---|
| **1 — Protocol design** | Complete. Protocol v1.0 locked and committed before any search. |
| **2 — Execute searches** | **Complete on `phase-2-search`.** Protocol v1.2 sources run; candidate pool deduplicated. |
| **3+** | Not started (Stage 1 screening). |

### Protocol versions

- **v1.0** — initial queries; raw results preserved in `search/raw_v1.0/`
- **v1.1** — corrections after v1.0 execution evidence (`protocol/CHANGELOG.md`): fixed `B3_memory_3` parentheses, added Semantic Scholar `s2_queries`, date-slicing / stopping-rule text
- **v1.2** — source substitution: IEEE metadata API + OpenAlex (ACM coverage); 50-cap per query; Google Scholar remains manual

### Phase 2 checklist

- [x] v1.0 arXiv / Semantic Scholar / OpenReview discovery runs (evidence under `search/raw_v1.0/`)
- [x] Protocol v1.1 amendment written and committed (before any v1.1 re-run)
- [x] `search/existing-references.yaml` populated (42 manuscript references; 12 `priority: HIGH`)
- [x] arXiv: re-run capped queries with date-slicing; re-run corrected `B3_memory_3` (residual quarterly gaps recorded for B3_memory_3)
- [x] Semantic Scholar: re-run all blocks with `s2_queries` (18/18)
- [x] OpenReview: venue check only (no discovery re-run) → `docs/reference-corrections.md`
- [x] Phase 2 closure corrections (reference-corrections review; B3_memory_3 residual-gap note; `protocol_version` field)
- [x] Protocol v1.2 amendment written and committed (before IEEE / OpenAlex / DBLP runs)
- [x] IEEE metadata API: 18 queries, 50-cap (`search/raw/ieee/`)
- [x] OpenAlex general + ACM-filtered: 18 queries each, 50-cap (`P4310319798`)
- [x] DBLP completeness run adopted (18/18; several keyword queries return 0 on DBLP)
- [x] Manual Google Scholar: 18 protocol queries as 34 runs; candidates in `search/raw/google_scholar/`
- [x] Deduplicated candidate pool counted (`search/candidate-pool.csv`: **10,334** unique; **10,313** for screening)

## Reproducing the search

```bash
pip install -r search/scripts/requirements.txt

# v1.1 sources (already executed on this branch)
python search/scripts/search_arxiv.py --v11-rerun
python search/scripts/search_semanticscholar.py

# v1.2 substituted sources (after v1.2 commit; 50-cap enforced in scripts)
python search/scripts/search_ieee.py          # requires IEEE_API_KEY
python search/scripts/search_openalex.py      # general index
python search/scripts/search_openalex.py --acm
python search/scripts/search_dblp.py

# Deduplicate all sources → search/candidate-pool.csv
python search/scripts/dedupe.py

# Venue-upgrade check for the existing ~42 manuscript references
python search/scripts/search_openreview.py --check-existing
```

Optional env vars (via `local.env`, never commit): `SEMANTIC_SCHOLAR_API_KEY`, `IEEE_API_KEY`.

Each run updates `search/search-log.md` and writes `search/raw/<source>/...`.

## Data provenance

Table 4 combines values from primary sources with author estimates. See
`docs/table4-sourcing.md` for per-column provenance.

## Citation

See `CITATION.cff`.

## License

[CC-BY-4.0](LICENSE)
