# PRISMA-Style Counts

**Status:** Identification / deduplication complete (Phase 2). Screening counts TBD in Phase 3.

Identification window: protocol coverage **2019-01-01 to 2026-06-30**.  
Dedup run: see `search/dedupe-summary.json` and `search/search-log.md` (`### dedupe`).

| Stage | Count |
|---|---|
| Records retrieved (all sources, pre-dedup) | 18,343 |
| Unique candidates after deduplication | 10,334 |
| Unique candidates for Stage 1 screening (excl. Scholar out-of-protocol) | 10,313 |
| Multi-source merges | 1,538 |
| With DOI / with arXiv ID | 3,995 / 7,782 |
| Title/abstract screened (Stage 1) | TBD |
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
