# Search Protocol

**Protocol version:** 1.0  
**Status:** Locked for Phase 1 — must be committed before any search execution  
**Companion paper:** Fine-Tuning Large Language Models in Resource-Constrained Environments: Methods and Trade-offs (PeerJ Computer Science, under revision)  
**Repository:** `llm-efficient-finetuning-survey`

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

Queries are organized into four blocks aligned with the survey taxonomy. Machine-readable definitions live in [`search/queries.yaml`](../search/queries.yaml).

| Block ID | Name |
|---|---|
| `B1_peft` | Parameter-Efficient Fine-Tuning |
| `B2_quantization` | Quantization |
| `B3_memory` | Memory Optimization |
| `B4_federated` | Distributed and Federated |

Date filter applied at search time: **2019-01-01 to 2026-06-30**.

### arXiv category restriction

When querying arXiv, restrict to `cs.LG`, `cs.CL`, `cs.AI`, and `cs.DC` where the API supports category filtering, to reduce off-topic noise.

### Result caps

Cap automated retrieval at **200 results per query**. If a query hits the cap, narrow the query and record the change in `search/search-log.md`.

---

## 5. Manual stopping rule

For Google Scholar, IEEE Xplore, and ACM Digital Library: screen the **first 50 results by relevance** per query. This is a stated, defensible stopping rule for a curated survey and will be reported in the manuscript methodology.

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
| Per-run log | `search/search-log.md` |
| Raw API responses | `search/raw/<source>/` |
| Screening decisions | `screening/screening-log.csv` |
| PRISMA-style counts | `screening/prisma-counts.md` |
| Final corpus | `data/included-papers.csv` |
| Bibliography | `data/references.bib` |

---

## 9. Sequencing constraint

**Phase 1 (this protocol) must be committed to git before Phase 2 search scripts are written or run.** The commit history is evidence that the protocol preceded results.

After this commit: **stop and confirm with the repository owner before implementing or executing search scripts.**
