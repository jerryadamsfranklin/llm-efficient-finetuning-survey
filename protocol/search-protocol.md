# Search Protocol

**Protocol version:** 1.3  
**Status:** Locked v1.3 amendment — commit before the confirmation-band backfill and supplementary retrieval  
**Supersedes:** v1.2 for confirmation-band retrieval and screening procedure only (see `protocol/CHANGELOG.md`)  
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
| IEEE Xplore metadata API | Publisher coverage (boolean queries; abstracts) | `https://ieeexploreapi.ieee.org/api/v1/search/articles` |
| OpenAlex | General index + ACM-published works (publisher filter) | `https://api.openalex.org/works` |
| DBLP (optional completeness) | CS venue strings | `https://dblp.org/search/publ/api` |
| Papers With Code | Implementation availability (not primary discovery) | `https://paperswithcode.com/api/v1/` |
| Crossref | DOI resolution and published-venue verification | `https://api.crossref.org/works` |

**v1.2 retrieval caps:** IEEE, OpenAlex (general and ACM-filtered), and DBLP request at most **50** records per query by native relevance ranking — equivalent to the manual first-50 stopping rule. Do not fetch more and truncate afterward.

**ACM note:** There is no public ACM DL search API. ACM content is retrieved via OpenAlex (and Crossref for verification), not the ACM Digital Library interface. Do not describe the search as “we searched ACM DL” without that qualification.

### 3.2 Manual (browser; log by hand)

| Source | Why manual | Logging requirement |
|---|---|---|
| Google Scholar | No official API; scraping violates ToS | Query, date, filters, result count, first-50 screen, candidates carried forward |
| Hugging Face documentation | Reference source, not a discovery index | Pages consulted and date |
| IEEE Xplore (fallback only) | If API key registration is denied or delayed | Same fields as Scholar; record fallback in search log |

### 3.3 Manuscript methodology language (accuracy)

Draft for the manuscript (do not claim direct ACM DL or unqualified IEEE “website” search):

> Searches were conducted across arXiv, Semantic Scholar, OpenReview, OpenAlex, Crossref, and the IEEE Xplore metadata API, supplemented by manual searching of Google Scholar. Content published by the ACM was retrieved through OpenAlex and Crossref rather than through the ACM Digital Library interface directly. Boolean query strings were used where the source supports Boolean evaluation (arXiv, IEEE Xplore, Google Scholar); semantically equivalent keyword formulations were used for sources performing relevance matching (Semantic Scholar, OpenAlex, DBLP). Both formulations are recorded in the companion repository.

Additional v1.3 sentences on retrieval limits and the confirmation pass:

> Because relevance-ranked sources saturate their retrieval caps on the recent literature, Semantic Scholar queries were additionally date-sliced by year for 2019–2021. Retrieval of the 2019–2021 period remains less complete than for 2022 onward, and this is reported rather than claimed to be exhaustive. A confirmation pass against the existing reference corpus verified 24 of the 29 in-window references already cited; the remainder were recovered by targeted supplementary lookup and are identified as such in the companion repository.

Screening disclosure (LLM assistance, scope bound) is specified verbatim in [`screening-procedure.md`](screening-procedure.md) §8 and must be reproduced in the methodology and in Section 10.4.

---

## 4. Query design

Queries are organized into four blocks aligned with the survey taxonomy. Machine-readable definitions live in [`search/queries.yaml`](../search/queries.yaml) (**protocol v1.2**).

| Block ID | Name |
|---|---|
| `B1_peft` | Parameter-Efficient Fine-Tuning |
| `B2_quantization` | Quantization |
| `B3_memory` | Memory Optimization |
| `B4_federated` | Distributed and Federated |

Date filter applied at search time: **2019-01-01 to 2026-06-30**.

### Source-specific query forms (v1.1 / v1.2)

- **Boolean `queries`:** arXiv, IEEE Xplore metadata API, and Google Scholar.
- **Keyword `s2_queries`:** Semantic Scholar, OpenAlex, and DBLP — semantically equivalent phrases, not identical boolean strings. Record this distinction in the search log and manuscript methodology.
- **OpenReview:** v1.1 does not re-run discovery queries (v1.0 results retained as evidence of saturation). Use OpenReview for venue/acceptance checks of the existing corpus.

### arXiv category restriction

When querying arXiv, restrict to `cs.LG`, `cs.CL`, `cs.AI`, and `cs.DC` where the API supports category filtering, to reduce off-topic noise.

### Result caps and date-slicing (v1.1 / v1.2)

- **arXiv / Semantic Scholar:** Cap automated retrieval at **200 results per query per time slice**. If an arXiv query hits the cap, **date-slice** by year (and recursively by half-year / quarter if needed). See `protocol/CHANGELOG.md` (v1.1).
- **IEEE / OpenAlex / DBLP (v1.2):** Cap at **50 results per query** by native relevance ranking (same volume as the manual stopping rule).

### Confirmation-band retrieval (v1.3)

v1.2 applied the 200-record Semantic Scholar cap **per query, without date slicing**. Because Semantic Scholar ranks by relevance and the recent literature is far larger, 17 of 18 queries saturated the cap and returned only 3.5% pre-2022 records. Coverage of 2019–2021 therefore rested almost entirely on arXiv's boolean conjunctions, and the confirmation pass missed an on-topic reference the manuscript cites (AdapterFusion). Evidence: [`search/coverage-diagnostic.md`](../search/coverage-diagnostic.md).

v1.3 adds two strictly additive retrieval actions. Neither removes or alters any v1.2 result.

1. **Date-sliced Semantic Scholar backfill for 2019, 2020, 2021.** All 18 `s2_queries` re-run once per year slice, 200-record cap per query per slice — the same rule v1.1 already specified for arXiv, now applied to Semantic Scholar. Written to `search/raw/semanticscholar_backfill/`.
2. **Targeted supplementary retrieval of known-corpus misses.** Direct lookup by title/DOI of in-window references from `search/existing-references.yaml` absent from the pool. This is verification of an already-cited corpus, not discovery, and is logged separately as such. Written to `search/raw/supplementary/`.

Supplementary retrieval is **not** a keyword search for new material and must not be described as extending the search's discovery reach. Records it recovers are screened against the same criteria as every other candidate.

**Query strings are unchanged in v1.3.** The `B1_peft_3` four-term conjunction is documented as a recall limitation rather than rewritten, because altering query strings after seeing results would make the search unreproducible against its own log. The limitation is reported instead.

---

## 5. Stopping rules

### Automated sources

> For arXiv, up to 200 records were retrieved per query per time slice, with date-slicing where a slice reached the retrieval cap. For Semantic Scholar, up to 200 records per query. For the IEEE Xplore metadata API, OpenAlex (including ACM-filtered runs), and DBLP, up to 50 records per query by relevance ranking. For Google Scholar (manual), the first 50 records by the interface's relevance ranking were screened per query. Caps and residual gaps are recorded in the search log.

### Manual sources

For Google Scholar (and IEEE only if API fallback is required): screen the **first 50 results by relevance** per query (or fewer if the interface returns fewer). Record the actual number.

Do **not** claim exhaustive or complete coverage of the field.

---

## 6. Screening overview

Full criteria: [`inclusion-exclusion.md`](inclusion-exclusion.md).  
Procedure, scope bound, and disclosure: [`screening-procedure.md`](screening-procedure.md) (**v1.3**).  
Extraction fields: [`extraction-schema.md`](extraction-schema.md).

Three stages (detailed in Phase 3):

1. **Title/abstract** — criteria 1, 4, 5  
2. **Full text** — criteria 2, 3  
3. **Synthesis/grouping** — category, subcategory, supersession / duplicate coverage  

Every candidate is logged in `screening/screening-log.csv` with decision and numbered exclusion reason when excluded.

**v1.3 procedure summary.** Stage 1 is conducted with LLM assistance under author supervision; every inclusion is author-verified and a stratified random sample of at least 250 exclusions is audited, with the disagreement rate reported. Screening is fully applied to records from 2024-01-01 onward; 2019–2023 records receive a targeted confirmation pass, and records not examined under that bound are reported as a separate count rather than as exclusions. A keyword pre-filter was tested and **rejected** — it dropped four references the manuscript itself cites. See `screening-procedure.md` for the full specification and the required disclosure wording.

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
| Screening procedure and disclosure | `protocol/screening-procedure.md` |
| Per-run log | `search/search-log.md` |
| Confirmation-pass coverage diagnostic | `search/coverage-diagnostic.md` |
| Known metadata defects | `screening/metadata-anomalies.md` |
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
v1.0 was committed before initial discovery. v1.1 corrects query defects and was committed before date-sliced / S2-keyword re-runs. v1.2 substitutes IEEE/ACM retrieval mechanisms and was committed before IEEE / OpenAlex / DBLP runs. v1.3 adds the confirmation-band Semantic Scholar backfill, the targeted supplementary retrieval, and the screening procedure, and must be committed before any of the three is executed.

The same constraint applies to screening: `screening-procedure.md`, including the scope bound and the 5% audit-disagreement threshold, is committed **before** Stage 1 decisions are recorded, so neither the bound nor the threshold can be adjusted to fit an outcome.
