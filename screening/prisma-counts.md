# PRISMA-Style Counts

**Status:** Identification and deduplication complete (protocol v1.3). Stage 1 screening in progress.

Identification window: protocol coverage **2019-01-01 to 2026-06-30**.  
Dedup run: see `search/dedupe-summary.json` and `search/search-log.md` (`### dedupe`).

This is a **structured, protocol-driven search** reported with PRISMA-style counts for
transparency. It is not a registered systematic review and does not use dual independent
screening. Stage 1 is LLM-assisted under author supervision — see
`protocol/screening-procedure.md`.

## Identification

| Stage | Count |
|---|---|
| Records retrieved, protocol v1.2 (seven sources) | 18,343 |
| Records retrieved, protocol v1.3 confirmation-band backfill | 6,775 |
| Records retrieved, protocol v1.3 known-corpus verification | 5 |
| **Total records retrieved** | **25,123** |
| Unique candidates after deduplication | 15,518 |
| Unique candidates for screening (excl. Scholar out-of-protocol) | 15,497 |
| Multi-source merges | 1,701 |
| With DOI / with arXiv ID | 7,930 / 9,992 |

### Records by source (pre-dedup)

| Source | Records | Protocol |
|---|---|---|
| arXiv | 11,841 | v1.1 |
| Semantic Scholar (unsliced) | 3,500 | v1.2 |
| Semantic Scholar (2019–2021 date-sliced backfill) | 6,775 | **v1.3** |
| OpenAlex (general) | 900 | v1.2 |
| IEEE Xplore metadata API | 705 | v1.2 |
| OpenAlex (ACM-filtered) | 636 | v1.2 |
| Google Scholar (excl. NOISE_UI/DUPLICATE) | 597 | v1.2 |
| DBLP | 164 | v1.2 |
| Supplementary known-corpus lookups | 5 | **v1.3** |

Dedup rule: DOI → arXiv ID → normalized title (exact, then fuzzy ≥ 0.95). Published/DOI
preferred over arXiv-only when merged.

### Effect of the v1.3 backfill

The backfill added **5,185 previously unretrieved unique candidates**, all in 2019–2021.

| | Before v1.3 | After v1.3 |
|---|---|---|
| Pre-2022 candidates | 448 (4.3% of pool) | 5,650 (36.4% of pool) |
| 2019 / 2020 / 2021 | 82 / 136 / 230 | 1,731 / 1,867 / 2,049 |
| 2024-onward candidates | 7,779 | 7,798 |

The 2024-onward figure is materially unchanged, as expected: the backfill targeted only
2019–2021. See `search/coverage-diagnostic.md` for why the original runs under-retrieved
that period.

---

## Screening

`screening/screening-log.csv` holds one row per unique candidate (**15,518** data rows).

### CSV row count vs. physical line count

Do not use `wc -l` on these files. Both pool and screening CSVs contain quoted fields with
embedded newlines (abstracts, notes), so physical line counts exceed logical row counts:

| File | Logical data rows | Physical lines (Aug 2026) | Rows with embedded newlines |
|---|---|---|---|
| `search/candidate-pool.csv` | **15,518** | 17,094 | 203 |
| `screening/screening-log.csv` | **15,518** | 15,532 | 3 |

Count rows with a CSV parser (`csv.DictReader`) or trust `search/dedupe-summary.json`
(`unique_candidates`: 15,518). The canonical post-dedup total is **15,518** unique
candidates; **15,497** are in-protocol for screening (`unique_for_screening` in
`dedupe-summary.json`, excluding 21 out-of-protocol Google Scholar captures).

| Bucket | Count |
|---|---|
| Excluded on metadata alone (criterion recorded per row) | 23 |
| **Receiving a Stage 1 title/abstract judgement** | **10,938** |
| — new-work band, 2024-01 onward (full screen) | 7,778 |
| — confirmation band, 2019–2023, meeting a §4 trigger | 3,142 |
| — year missing (date verified individually) | 18 |
| **Within Stage 1 scope in total** (10,938 + 23) | **10,961** |
| Not screened — confirmation band, no §4 trigger met | 4,557 |
| Title/abstract screened (Stage 1) | new-work band complete (automated pass); confirmation band pending |
| — new-work includes (Stage 2 pending) | 3,011 |
| — new-work excludes | 4,787 |
| Full text assessed (Stage 2) | TBD |
| Included in synthesis | TBD |

### The 4,557 not-screened records are not exclusions

They are 2019–2023 records that meet none of the four triggers in
`protocol/screening-procedure.md` §4 (match to the existing reference corpus, ≥ 50 citations,
a core-method term in the title, or survey status). They carry `stage_reached:
stage_1_not_screened` with an **empty decision**: they were neither included nor excluded,
because describing an unexamined record as excluded would misrepresent it as judged. This is
reported as its own line and disclosed in the manuscript as a bounded-scope limitation.

Of the 10,938 records receiving a judgement, 2,442 already carry ≥ 50 citations.

### Confirmation pass against the existing corpus

| Outcome | Count |
|---|---|
| Manuscript references (total) | 42 |
| Present in the pool after Phase 2 | 29 of 42 |
| Absent — publication date precedes the window | 7 |
| Absent — reference rejected at venue check (`bayati2023`) | 1 |
| Absent — in-window, recovered by v1.3 supplementary lookup | 5 |
| **In-window references now represented** | **34 of 34** |

The five recovered are AdapterFusion, Megatron-LM, GPipe, AdamW, and experience replay. Four
were missed because no query block targets their subject (optimizers, pipeline and tensor
parallelism, continual-learning replay); AdapterFusion was a genuine recall defect on a paper
with 1,217 citations. Full attribution in `search/coverage-diagnostic.md`.

`bayati2023` is **not** counted as recovered: its lookup matched *Flexora* (2024), a different
paper, which corroborates the Phase 2 decision to reject it as not existing as cited.

### Screening-support fields

`screening-log.csv` extends the documented column set with fields needed to apply the criteria
without re-querying: `citations` and `citations_source` (inclusion criterion 3), `screener`,
`screener_original` and `confidence` (decision provenance and audit trail), plus
`is_published`, `doi`, `arxiv_id`, `n_sources`, `all_sources`, `priority_band`, and
`has_abstract`. The first eleven columns remain exactly as specified in the build plan.

`candidate_id` is derived from DOI, arXiv ID, or normalized title rather than row position, so
regenerating the pool cannot reassign decisions recorded against an id.

Known metadata defects are recorded in `screening/metadata-anomalies.md`.

### Residual retrieval limits

26 of the 54 backfill slices reached the 200-record cap, so 2019–2021 retrieval is improved but
still not exhaustive. Combined with the boundary effect that arXiv filters on submission date
(a 2019 publication first posted in 2018 is unreachable by a date-sliced arXiv query), coverage
of the confirmation band is explicitly **not** claimed to be complete.
