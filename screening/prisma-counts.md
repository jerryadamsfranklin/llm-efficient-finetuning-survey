# PRISMA-Style Counts

**Status:** Identification and deduplication complete. Stage 1 screening in progress (Phase 3).

Identification window: protocol coverage **2019-01-01 to 2026-06-30**.  
Dedup run: see `search/dedupe-summary.json` and `search/search-log.md` (`### dedupe`).

This is a **structured, protocol-driven search** reported with PRISMA-style counts for
transparency. It is not a registered systematic review and does not use dual independent
screening — see `protocol/search-protocol.md`.

| Stage | Count |
|---|---|
| Records retrieved (all sources, pre-dedup) | 18,343 |
| Unique candidates after deduplication | 10,333 |
| Unique candidates for Stage 1 screening (excl. Scholar out-of-protocol) | 10,312 |
| Multi-source merges | 1,537 |
| With DOI / with arXiv ID | 3,995 / 7,974 |
| Excluded before title/abstract review (metadata-decidable) | 23 |
| Title/abstract screened (Stage 1) | in progress |
| Full text assessed (Stage 2) | TBD |
| Included in synthesis | TBD |

### Raw records by source (pre-dedup)

| Source | Records loaded |
|---|---|
| arXiv | 11,841 |
| Semantic Scholar | 3,500 |
| OpenAlex (general) | 900 |
| OpenAlex (ACM-filtered) | 636 |
| IEEE Xplore metadata API | 705 |
| Google Scholar (excl. NOISE_UI/DUPLICATE) | 597 |
| DBLP | 164 |

Dedup rule: DOI → arXiv ID → normalized title (exact, then fuzzy ≥ 0.95). Published/DOI preferred over arXiv-only when merged.

---

## Stage 1 entry state

`screening/screening-log.csv` holds one row per unique candidate (10,333 rows).

| Bucket | Count |
|---|---|
| Excluded on metadata alone (criterion recorded per row) | 23 |
| Awaiting title/abstract judgement | 10,310 |
| — of which 2024-01 onward (new-work band) | 7,779 |
| — of which 2019–2023 (confirmation band) | 2,513 |
| — of which year missing (date to verify) | 18 |
| Awaiting rows with no abstract in pool (title-only screen) | 413 |

The 23 metadata-decidable exclusions are 21 Google Scholar hits flagged out-of-protocol
at dedup and 2 records whose type is non-archival course material, all under exclusion
criterion 6. No candidate was excluded on year, because every retrieved record already
falls inside the 2019–2026 window — an expected consequence of date-sliced querying.

**Band definitions** follow the scope control in `protocol/inclusion-exclusion.md`: the
2019–2023 *confirmation* band verifies coverage of the existing corpus, while the
2024-01 to 2026-06 *new-work* band is where genuinely new inclusions are expected.
Both bands are screened; the bands set review order and depth, not eligibility.

### Screening-support fields

`screening-log.csv` extends the documented column set with fields needed to apply the
criteria without re-querying: `citations` and `citations_source` (inclusion criterion 3),
`is_published`, `doi`, `arxiv_id`, `n_sources`, `all_sources`, `priority_band`, and
`has_abstract`. The first eleven columns remain exactly as specified in the build plan.

Citation coverage in the pool: 3,586 candidates carry a citation count, of which 849
awaiting Stage 1 are at or above the 50-citation adoption bar. Records with no citation
figure are not thereby excluded — criterion 3 is also satisfied by an official library
implementation or a recorded OpenReview acceptance, both checked at Stage 2.

Known metadata defects are recorded in `screening/metadata-anomalies.md`.
