# Fine-Tuning Large Language Models in Resource-Constrained Environments

Companion repository for the survey "Fine-Tuning Large Language Models in
Resource-Constrained Environments: Methods and Trade-offs" (under review,
PeerJ Computer Science).

## Contents

- `protocol/` — search protocol, inclusion criteria, extraction schema, changelog
- `search/` — query definitions, search log, raw API responses, search scripts
- `screening/` — screening decisions for every candidate, PRISMA-style counts
- `data/` — extraction schema targets: table templates, corpus CSV, and BibTeX stub (Phase 4 placeholders; extraction not started)
- `figures/` — figure generation scripts and outputs
- `docs/` — Table 4 provenance template (Phase 5) and reference-correction notes

## Status

| Phase | Status |
|---|---|
| **1 — Protocol design** | Complete. Protocol v1.0 locked and committed before any search. |
| **2 — Execute searches** | **Closed 2026-07-31**, merged to `main`. All seven sources run under protocol v1.2; candidate pool deduplicated and counted. |
| **3 — Screening** | **In progress** on `phase-3-screening`. Protocol v1.3 backfill grew the pool to 15,518 unique candidates; 10,938 receive a Stage 1 judgement, 4,557 are out of the stated scope bound, 23 excluded on metadata alone. **Submission target: 2026-08-20.** |
| **4 — Extraction** | Not started. `data/included-papers.csv`, `data/table*.csv`, and `data/references.bib` are header-only Phase 4 templates. |
| **5 — Table provenance** | Not started. `docs/table4-sourcing.md` is a Phase 5 template with disclosure language only. |

### Protocol versions

- **v1.0** — initial queries; raw results preserved in `search/raw_v1.0/`
- **v1.1** — corrections after v1.0 execution evidence (`protocol/CHANGELOG.md`): fixed `B3_memory_3` parentheses, added Semantic Scholar `s2_queries`, date-slicing / stopping-rule text
- **v1.2** — source substitution: IEEE metadata API + OpenAlex (ACM coverage); 50-cap per query; Google Scholar remains manual
- **v1.3** — confirmation-band amendment after a coverage diagnostic (`search/coverage-diagnostic.md`): date-sliced Semantic Scholar backfill for 2019–2021, targeted supplementary retrieval of known-corpus misses, and the screening procedure with its LLM-assistance disclosure (`protocol/screening-procedure.md`). Query strings unchanged.

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
- [x] Deduplicated candidate pool counted at Phase 2 close: **10,333** unique (**10,312** for screening after excluding 21 out-of-protocol Scholar captures). Protocol v1.3 confirmation-band backfill (Phase 3) grew the pool to **15,518** unique — see `screening/prisma-counts.md` § "Effect of the v1.3 backfill" and `search/dedupe-summary.json`.
- [x] Hugging Face documentation entry resolved (reference source; not consulted in Phase 2, zero records)
- [x] No `TBD` placeholders remaining in `search/search-log.md`

Phase 2 is closed. Candidate volume came in above the v1.2 amendment's 6,000–7,000
planning estimate; see `protocol/CHANGELOG.md` ("Execution outcome") for why.

### Phase 3 checklist

- [x] Candidate pool regenerated to carry citation counts, language, record type, and OpenAlex abstracts (no source re-queried)
- [x] `screening/screening-log.csv` initialised — one row per unique candidate (**15,518** after v1.3 pool regeneration; was 10,333 at first init)
- [x] Metadata-decidable exclusions applied with the numbered criterion recorded (23 rows)
- [x] Known metadata defects documented (`screening/metadata-anomalies.md`)
- [x] Confirmation-pass diagnostic: 24 of 29 in-window manuscript references verified in the pool (`search/coverage-diagnostic.md`)
- [x] Protocol v1.3 committed before the runs and screening decisions it authorises
- [x] Semantic Scholar 2019–2021 date-sliced backfill (54/54 slices; +5,185 unique candidates; pre-2022 share 4.3% → 36.4%)
- [x] Targeted supplementary retrieval — all five known-corpus misses recovered; `bayati2023` confirmed a different work
- [x] Scope bound applied: 4,557 confirmation-band records recorded as not screened, with empty decisions rather than exclusions
- [ ] Stage 1 title/abstract screen (10,938 to judge; criteria 1, 4, 5; exclusions 1–3, 6; criterion 2 LLM boundary and book-chapter rule from batch 002 — see `screening-procedure.md` §2.1)
- [ ] Stage 2 full-text screen (criteria 2, 3; adoption bar verified against a second source)
- [ ] Stage 3 synthesis — category / subcategory assignment
- [ ] `screening/prisma-counts.md` completed with final stage counts

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

# Initialise / refresh the screening log (never overwrites recorded decisions)
python screening/scripts/init_screening_log.py

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
