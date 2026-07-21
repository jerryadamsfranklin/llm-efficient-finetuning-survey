# Search Protocol

**Protocol version:** 1.1  
**Status:** Locked amendment after v1.0 execution — commit before any v1.1 re-runs  
**Supersedes:** v1.0 query definitions only (see `protocol/CHANGELOG.md`)  
**Companion paper:** Fine-Tuning Large Language Models in Resource-Constrained Environments: Methods and Trade-offs (PeerJ Computer Science, under revision)  
**Repository:** `llm-efficient-finetuning-survey`

v1.0 raw results are preserved under `search/raw_v1.0/`. Do not delete them.

---

## 1. Purpose and framing

This protocol defines a **structured, reproducible, protocol-driven literature search** for the companion survey repository. Search strings, databases, dates, and screening decisions are recorded here and in linked artifacts so the manuscript methodology section is verifiable.

### What this is

- A structured search with pre-specified queries, inclusion/exclusion criteria, and extraction fields
- PRISMA-**informed** reporting of flow counts (for transparency)

### What this is not

- A formal PRISMA systematic review
- A PROSPERO-registered review
- A dual-independent-screener process (single author)

Manuscript wording must use “structured search,” “protocol-driven search,” or “PRISMA-informed counts” — never “registered systematic review” or claims of dual screening.

---

## 2. Pre-search decisions (locked)

| Decision | Choice |
|---|---|
| Coverage window | **2019-01-01 through 2026-06-30** |
| Search execution window | Actual calendar dates in **July 2026** (recorded in `search/search-log.md`; not backdated) |
| Scope of new screening effort | (1) Confirmation pass over the existing ~42-reference corpus; (2) discovery weighted to **January 2024 – June 2026**, especially reviewer-named gaps |
| Formal SR / PROSPERO | **No** |
| Google Scholar automation | **Forbidden** (manual logging only; no scraping) |

Rationale for the June 2026 cutoff: revision is occurring in July 2026; extending past December 2025 demonstrates currency without requiring an exhaustive re-screen of 2019–2023 foundational literature already represented in the existing corpus.

---

## 3. Information sources

### 3.1 Automated (API / script)

| Source | Role | API / endpoint |
|---|---|---|
| arXiv | Primary discovery | `http://export.arxiv.org/api/query` |
| Semantic Scholar | Discovery + citation counts (community-adoption criterion) | `https://api.semanticscholar.org/graph/v1/paper/search` |
| OpenReview | Acceptance / venue status for preprints | `https://api2.openreview.net/notes` |
| Papers With Code | Implementation availability (not primary discovery) | `https://paperswithcode.com/api/v1/` |
| Crossref | DOI resolution and published-venue verification | `https://api.crossref.org/works` |

### 3.2 Manual (browser; log by hand)

| Source | Why manual | Logging requirement |
|---|---|---|
| Google Scholar | No official API; scraping violates ToS | Query, date, filters, result count, first-50 screen, candidates carried forward |
| IEEE Xplore | Institutional API key may be unavailable | Same fields as Scholar |
| ACM Digital Library | Subscription / access constraints | Same fields as Scholar |
| Hugging Face documentation | Reference source, not a discovery index | Pages consulted and date |

---

## 4. Query design

Queries are organized into four blocks aligned with the survey taxonomy. Machine-readable definitions live in [`search/queries.yaml`](../search/queries.yaml) (**protocol v1.1**).

| Block ID | Name |
|---|---|
| `B1_peft` | Parameter-Efficient Fine-Tuning |
| `B2_quantization` | Quantization |
| `B3_memory` | Memory Optimization |
| `B4_federated` | Distributed and Federated |

Date filter applied at search time: **2019-01-01 to 2026-06-30**.

### Source-specific query forms (v1.1)

- **Boolean `queries`:** arXiv and manual sources (Google Scholar, IEEE Xplore, ACM DL).
- **Keyword `s2_queries`:** Semantic Scholar only — semantically equivalent phrases, not identical boolean strings. Record this distinction in the search log and manuscript methodology.
- **OpenReview:** v1.1 does not re-run discovery queries (v1.0 results retained as evidence of saturation). Use OpenReview for venue/acceptance checks of the existing corpus.

### arXiv category restriction

When querying arXiv, restrict to `cs.LG`, `cs.CL`, `cs.AI`, and `cs.DC` where the API supports category filtering, to reduce off-topic noise.

### Result caps and date-slicing (v1.1)

Cap automated retrieval at **200 results per query per time slice**. If a query hits the cap, **date-slice** by year (and recursively by half-year / quarter if needed) rather than silently truncating. See `protocol/CHANGELOG.md` and amendment sections 4–5.

---

## 5. Stopping rules

### Automated sources (adopted verbatim in v1.1)

> For automated sources, up to 200 records were retrieved per query per time slice, sorted by submission date, with queries date-sliced by year and further subdivided where a slice reached the retrieval cap. For manual sources, the first 50 records by the interface's relevance ranking were screened per query. Where a query reached the retrieval cap at the finest granularity applied, this is recorded in the search log.

### Manual sources

For Google Scholar, IEEE Xplore, and ACM Digital Library: screen the **first 50 results by relevance** per query (or fewer if the interface returns fewer). Record the actual number.

Do **not** claim exhaustive or complete coverage of the field.

---

## 6. Screening overview

Full criteria: [`inclusion-exclusion.md`](inclusion-exclusion.md).  
Extraction fields: [`extraction-schema.md`](extraction-schema.md).

Three stages (detailed in Phase 3):

1. **Title/abstract** — criteria 1, 4, 5  
2. **Full text** — criteria 2, 3  
3. **Synthesis/grouping** — category, subcategory, supersession / duplicate coverage  

Every candidate is logged in `screening/screening-log.csv` with decision and numbered exclusion reason when excluded.

---

## 7. Deduplication rules (preview)

Match priority: **DOI → arXiv ID → normalized title** (lowercase; strip punctuation/whitespace; fuzzy ratio ≥ 0.95).  
When both preprint and published versions appear, keep the published version and record the arXiv ID as superseded.

---

## 8. Artifacts produced by this protocol

| Artifact | Path |
|---|---|
| Query definitions | `search/queries.yaml` |
| Protocol changelog | `protocol/CHANGELOG.md` |
| Per-run log | `search/search-log.md` |
| Raw API responses (current) | `search/raw/<source>/` |
| Raw API responses (v1.0 preserved) | `search/raw_v1.0/<source>/` |
| Existing corpus for venue check | `search/existing-references.yaml` |
| Reference corrections | `docs/reference-corrections.md` |
| Screening decisions | `screening/screening-log.csv` |
| PRISMA-style counts | `screening/prisma-counts.md` |
| Final corpus | `data/included-papers.csv` |
| Bibliography | `data/references.bib` |

---

## 9. Sequencing constraint

**Protocol versions must be committed before the searches that use them are run.**  
v1.0 was committed before initial discovery. v1.1 corrects query defects found in that execution and must be committed before any date-sliced / S2-keyword re-runs.

After this v1.1 amendment commit: **stop and confirm with the repository owner before re-running searches.**
