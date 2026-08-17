# Screening Procedure

**Protocol version:** 1.3  
**Status:** Locked — committed before Stage 1 screening begins  
**Related:** [`inclusion-exclusion.md`](inclusion-exclusion.md), [`search-protocol.md`](search-protocol.md), [`CHANGELOG.md`](CHANGELOG.md)

This document specifies **how** the criteria in `inclusion-exclusion.md` are applied to the
candidate pool, who applies them, and what is verified by the author. It exists because the
procedure involves large language model assistance, and that must be stated plainly rather than
left implicit.

**Counts below reflect the post-v1.3 pool of 15,518 unique candidates**, after the confirmation-band
Semantic Scholar backfill added 5,185 previously unretrieved 2019–2021 records. The rules in this
document were committed before that retrieval ran and are unchanged by it; only the counts moved.

---

## 1. Why this procedure

Stage 1 requires a title/abstract judgement on 15,495 candidates (23 were excluded on metadata
alone; see §5). Three approaches were considered and two were rejected on evidence:

- **Keyword pre-filtering was tested and rejected.** A filter built from the protocol's own query
  vocabulary removed only 37% of the pool while dropping four references the manuscript already
  cites (LoRA+, VeRA, ZeRO-Offload, FlashAttention-2) — 86% recall against known-relevant work.
  Excluding papers the survey itself cites is not defensible, so no keyword filter is used to
  exclude any record.
- **Exhaustive manual screening of all 15,495** by a single author inside the revision window is
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
| **New-work band** | 2024-01-01 – 2026-06-30 | 7,778 | **Full Stage 1 screen** of every record |
| **Confirmation band** | 2019-01-01 – 2023-12-31 | 7,699 | **Targeted confirmation pass** (§4), not a full screen |
| Year missing | — | 18 | Full screen; date verified individually against criterion 5 |

Applying the §4 triggers selects **3,142** of the 7,699 confirmation-band records for screening and
records the remaining **4,557** as `stage_1_not_screened`. Total records receiving a Stage 1
judgement: **10,938**.

Both bands can yield inclusions. The band determines review *depth*, not eligibility: nothing is
excluded for being in the confirmation band, and any confirmation-band record that surfaces as
relevant is screened on the same criteria as the new-work band.

This bound is a stated limitation, reported in `screening/prisma-counts.md` and disclosed in the
manuscript. It is **not** described as exhaustive coverage of 2019–2023.

### 2.1 Scope clarifications (v1.3 — clarification, not change)

Two-part scope plus book-chapter form were written into `inclusion-exclusion.md` during author
calibration of batch 001. The criteria text is unchanged; the readings are now explicit. **Both
apply from new-work batch 002 onward** (and to all subsequent confirmation-band screening). Batch
001 log rows were rewritten after author confirmation of
`screening/reviews/new-work-batch-001-reconciliation.md` (20 author excludes).

| Clarification | Criterion | Rule |
|---|---|---|
| **Method, not application** | 1 | Research-question test: in scope if the question is about the fine-tuning-efficiency method (performance, applicability, improvement), including comparative evaluations of the method on a task used as a testbed. Out of scope if the question is about a task or system and the method is only the tool used to build it. |
| **LLM-only boundary** | 2 | Include only if the model is an LLM, or the paper is a survey of efficiency methods for language models (including SLM efficiency surveys). Vision, speech, graph, audio, multimodal, and general-ML papers fail unless the method is general **and demonstrated on an LLM**. |
| **Book chapters** | 6 | Textbook, tutorial, and pedagogical book chapters are non-archival secondary material. Peer-reviewed conference/journal papers and papers in edited scholarly proceedings remain eligible. |

**Immediate log updates from these rules (author-directed):**

- Held record `C-34a4a73f19` (Large Language Models (LLMs): Quantization) → **exclude** under
  exclusion 6 (De Gruyter book-chapter neighbours).
- Held record `C-3187c706f6` (AttentionletIs All You Need!) → **remains held** (unidentifiable).

Batch 001 record `C-352115b844` (Springer PEFT textbook chapter) is an exclusion 6 case under the
book-chapter rule; the author verifies the batch-001 packet against that reading.

---

## 3. Stage 1 — new-work band (full screen)

Applied to all 7,778 records from 2024-01-01 onward.

**Criteria applied:** inclusion 1, 4, 5; exclusions 1–3 and 6 where obvious from title/abstract;
criterion 2 LLM boundary when the non-language domain is clear (§2.1); book-chapter form under
exclusion 6 when obvious (§2.1).

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

Applied to the 7,699 records from 2019–2023. This band is not fully screened. Records enter review
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

### 6.1 Verification cadence

Verification runs **per block of 375 records** in the new-work band (~2.5 batches at size 150),
roughly **29 rounds** for the full new-work band. Block size was reduced from 750 after batch 001
calibration produced a 35% low-confidence rate; at that rate a 750-record block would generate
~260 review items and is not reviewable within the project window.

Each block emits a packet to `screening/reviews/` containing every include, every low-confidence
decision, and a sample of confident excludes; screening of the next block does not begin until the
packet returns. Blocks are deliberately sized by record count rather than by include volume, because
the errors under audit are false excludes as much as false includes and an include-triggered packet
would surface only the latter. Block size may be widened once the disagreement rate is demonstrably
low, and is tightened if it is not.

**Planning note:** with ~10,770 records remaining at Stage 1 entry, the realistic submission target
for this revision is **2026-08-20**, not 2026-08-01–05.

### 6.2 What `confidence` means

Confidence reports **certainty in the screening decision**, not the strength of the record or
enthusiasm for it. The two move independently: a record can be advanced under bias-to-inclusion
while the screener remains unsure it belongs. A bare title with no abstract rarely supports high
confidence. Records whose title cannot distinguish training-time from inference-time methods are
low confidence even when advanced.

Under the strict LLM-only boundary (§2.1), vision, speech, and multimodal domain papers where
PEFT or quantization is applied as task machinery — not as a generalizable LLM efficiency method —
are **excluded under criterion 2 at Stage 1** when the domain is clear, not advanced at low
confidence. This matters because confidence drives audit intensity: high-confidence rows are
sampled less. **Bias the decision toward inclusion only where the domain boundary is genuinely
unclear; keep confidence honest about how little the metadata supports the call.**

### 6.3 Records that cannot be identified

A record whose identity cannot be established — garbled title, no authors, venue, year, or
citation data, and no match in Semantic Scholar, Crossref, or OpenAlex — is **not** advanced as an
include. Advancing an unidentifiable record is deferring an unmade decision, not making one.
Metadata recovery is attempted first against those three indexes; if it fails, the record is
recorded `decision: hold`, `stage_reached: stage_1_held`, with a note stating what was attempted.
Held records are neither included nor excluded and **must be resolved before the PRISMA counts are
final**.

### 6.4 Automated pass of the new-work band (2026-08-17)

The remaining 7,628 new-work records were screened in a **single automated pass**
(`screener: automated`) rather than in 375-record human-verified blocks. The encoded v1.3
rule was applied by `screening/scripts/auto_stage1.py`. Author verification for this pass is
the ranked shortlist of 30 includes in `screening/reviews/reference-shortlist.md`, not
100% of includes in the band. Author review of that shortlist (2026-08-17): 4 already-cited
duplicates dropped from the insertion set only; 6 domain/inference includes overturned to
exclude; 20 remain in-scope; 13 selected for primary-source verification
(`screening/reviews/shortlist-13-verification.md`). This is a stated departure from the
§6 table's "every include" requirement for this band, recorded here and in `CHANGELOG.md`.
The confirmation band is unchanged.

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
