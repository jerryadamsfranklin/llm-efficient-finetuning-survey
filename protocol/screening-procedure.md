# Screening Procedure

**Protocol version:** 1.3  
**Status:** Locked — committed before Stage 1 screening begins  
**Related:** [`inclusion-exclusion.md`](inclusion-exclusion.md), [`search-protocol.md`](search-protocol.md), [`CHANGELOG.md`](CHANGELOG.md)

This document specifies **how** the criteria in `inclusion-exclusion.md` are applied to the 10,333
unique candidates, who applies them, and what is verified by the author. It exists because the
procedure involves large language model assistance, and that must be stated plainly rather than
left implicit.

---

## 1. Why this procedure

Stage 1 requires a title/abstract judgement on 10,310 candidates (23 were excluded on metadata
alone; see §5). Three approaches were considered and two were rejected on evidence:

- **Keyword pre-filtering was tested and rejected.** A filter built from the protocol's own query
  vocabulary removed only 37% of the pool while dropping four references the manuscript already
  cites (LoRA+, VeRA, ZeRO-Offload, FlashAttention-2) — 86% recall against known-relevant work.
  Excluding papers the survey itself cites is not defensible, so no keyword filter is used to
  exclude any record.
- **Exhaustive manual screening of all 10,310** by a single author inside the revision window is
  not achievable without compromising either the deadline or the rigour of the judgements.
- **Adopted:** LLM-assisted screening under author supervision, bounded in scope, with mandatory
  author verification of every inclusion.

---

## 2. Scope bound

The scope-control clause in `inclusion-exclusion.md` §"Scope control" states that the goal is not an
exhaustive re-screen of 2019–2023 literature: the existing corpus is the foundation, and the new
search confirms that coverage while adding new work weighted to January 2024 – June 2026.
Screening effort is allocated accordingly.

| Band | Date range | Candidates | Treatment |
|---|---|---|---|
| **New-work band** | 2024-01-01 – 2026-06-30 | 7,779 | **Full Stage 1 screen** of every record |
| **Confirmation band** | 2019-01-01 – 2023-12-31 | 2,513 | **Targeted confirmation pass** (§4), not a full screen |
| Year missing | — | 18 | Full screen; date verified individually against criterion 5 |

Both bands can yield inclusions. The band determines review *depth*, not eligibility: nothing is
excluded for being in the confirmation band, and any confirmation-band record that surfaces as
relevant is screened on the same criteria as the new-work band.

This bound is a stated limitation, reported in `screening/prisma-counts.md` and disclosed in the
manuscript. It is **not** described as exhaustive coverage of 2019–2023.

---

## 3. Stage 1 — new-work band (full screen)

Applied to all 7,779 records from 2024-01-01 onward.

**Criteria applied:** inclusion 1, 4, 5; exclusions 1–3 and 6 where obvious from title/abstract
(per the stage mapping in `inclusion-exclusion.md`).

**Procedure.** Records are presented to the LLM screener in batches with title, abstract, year,
venue, and citation count. For each record the screener records:

| Field | Meaning |
|---|---|
| `decision` | `include` (advance to Stage 2) or `exclude` |
| `exclusion_reason` | The numbered criterion that triggered exclusion — required for every exclusion |
| `screener` | `llm_assisted`, `author`, or `metadata` — provenance of the decision |
| `confidence` | `high` or `low` — the screener's own certainty |
| `notes` | Basis for the judgement where not self-evident from the title |

**Bias toward inclusion at Stage 1.** Where relevance is uncertain from the title and abstract, the
record is marked `include` with `confidence: low` and resolved at Stage 2 on full text. Stage 1 is a
coarse filter; the cost of wrongly advancing a record is one full-text read, whereas the cost of
wrongly excluding one is a missing reference that a reviewer may notice.

---

## 4. Stage 1 — confirmation band (targeted pass)

Applied to the 2,513 records from 2019–2023. This band is not fully screened. Records enter review
if **any** of the following holds:

1. The record matches a reference already cited in the manuscript
   (`search/existing-references.yaml`) — the confirmation function proper.
2. The record carries **≥ 50 citations**, i.e. it already meets the community-adoption bar of
   inclusion criterion 3 and cannot be dismissed as low-impact.
3. The record names a core method of the survey taxonomy in its title (adapter, LoRA and named
   variants, prefix/prompt tuning, BitFit, quantization methods, ZeRO/offloading, federated
   fine-tuning), i.e. it is on-topic on its face.
4. The record is a survey or review of the field.

Records not meeting any of these are recorded as `not_screened_confirmation_band` with
`stage_reached: stage_1_not_screened`, **not** as exclusions. They are neither included nor
excluded, and they are reported as a distinct PRISMA-style line. Recording them as exclusions would
misrepresent an unexamined record as a judged one.

Rationale for the ≥ 50 citation trigger: a 2019–2023 paper relevant enough to belong in this survey
has had three to seven years to accumulate citations, so the adoption bar is a reasonable proxy for
"would have mattered." The trigger is stated so it can be checked, and it is applied uniformly.

---

## 5. Metadata-only decisions

23 records were excluded before any title/abstract judgement, each citing its numbered criterion:
21 Google Scholar hits flagged out-of-protocol at deduplication and 2 records whose type is
non-archival course material (exclusion criterion 6). These carry `screener: metadata`. No record
is excluded on year, because every retrieved record falls inside the coverage window.

---

## 6. Author verification (mandatory)

LLM-assisted decisions are **provisional** until verified as follows.

| Requirement | Scope |
|---|---|
| **Every `include`** is author-verified before the record advances to Stage 2 | 100% |
| **Every `confidence: low` decision** is author-reviewed | 100% |
| **Random audit of confident exclusions** — stratified by year band, source, and query block | ≥ 250 records |
| **Every record entering the final corpus** is author-verified on full text | 100% |

The audit sample is drawn with a recorded random seed so it is reproducible. The
**disagreement rate** (author overturns screener) is computed and reported in
`screening/prisma-counts.md`. If the audit disagreement rate on exclusions exceeds **5%**, the
LLM-assisted exclusions are not trusted: the affected stratum is re-screened rather than patched.
That threshold is set in advance, before the audit is run, so it cannot be adjusted to fit the
result.

Author verification is recorded per row: `screener` changes to `author` and `notes` records the
overturn where the author disagrees. The original machine decision is preserved in
`screener_original` so the audit trail survives.

---

## 7. Stage 2 and Stage 3

**Stage 2 — full text.** Inclusion criteria 2 (scale/role) and 3 (publication/adoption bar);
exclusions 4 and 5. Author-conducted on full text; not delegated. Where criterion 3 is the deciding
factor, the citation count is confirmed against a second source and both the figure and its source
are recorded (`citations`, `citations_source`). OpenAlex `cited_by_count` is not treated as
self-validating — see `screening/metadata-anomalies.md`.

**Stage 3 — synthesis.** Category and subcategory assignment per `extraction-schema.md`;
identification of records superseded or duplicated in coverage.

---

## 8. Disclosure

The following is the required disclosure, to appear in the manuscript methodology and in
Section 10.4 (limitations). It must not be softened or omitted.

> Title and abstract screening was conducted with large language model assistance under author
> supervision. Every record advanced to full-text assessment was verified by the author, and a
> stratified random sample of at least 250 exclusions was audited, with the disagreement rate
> reported in the companion repository. Full-text assessment, inclusion decisions, and data
> extraction were performed by the author. Screening effort was concentrated on records published
> from January 2024 onward; earlier records were subject to a targeted confirmation pass against
> the existing reference corpus, high-citation work, and core-method terms rather than an
> exhaustive screen. Records not examined under that bound are reported as a separate count and are
> not represented as screened.

### Not claimed

- Not a registered systematic review; not PROSPERO-registered.
- Not dual independent screening. LLM assistance is **not** a second independent screener, and no
  inter-rater reliability statistic is reported for it. The audit disagreement rate is a quality
  control measure on a single-author process, and is described as such.
- Not exhaustive coverage of 2019–2023.
