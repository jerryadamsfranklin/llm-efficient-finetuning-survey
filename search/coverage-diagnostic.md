# Confirmation-Pass Coverage Diagnostic

**Run:** 2026-07-31, at Phase 3 entry, against `search/candidate-pool.csv` (10,333 unique candidates).
**Purpose:** test whether the Phase 2 search retrieved the 42 references already cited in the
manuscript. Per `docs`-level plan, the confirmation pass has to *verify and document* coverage of
the existing corpus; that claim cannot be made without checking it.

**Method:** each of the 42 references in `search/existing-references.yaml` was matched against the
pool by DOI, then arXiv ID, then normalized title. References with no pool match were then searched
for by keyword across all 210 raw response files to distinguish "not retrieved" from
"retrieved but lost during deduplication".

---

## Result

| Outcome | Count |
|---|---|
| Present in the deduplicated pool | 29 |
| Absent — publication date precedes the coverage window | 7 |
| Absent — reference previously rejected at venue check | 1 |
| **Absent — in-window and genuinely not retrieved** | **5** |

None of the five absent in-window references appear in *any* discovery response. They appear only
in `search/raw/openreview/existing_references_venue_check.json`, which is a targeted lookup of the
existing reference list, not a discovery run. So these are true retrieval misses, not dedup losses.

### Correctly absent (7) — outside the 2019-01-01 window

`vaswani2017`, `abadi2016`, `chen2016`, `jacob2018`, `kirkpatrick2017`, `mcmahan2017`,
`micikevicius2018`. These fail inclusion criterion 5 and are cited as foundational background.
Their absence from the pool is the protocol working as specified, not a gap.

### Previously rejected (1)

`bayati2023` ("FlexLoRA"). Rejected during the Phase 2 venue check; see
`docs/reference-corrections.md`. The pool does contain a *different*, real paper with a
near-identical title ("Flexora: Flexible Low Rank Adaptation for Large Language Models"), which is
why a naive title match appears to succeed at ratio 0.99. They are not the same work.

---

## The five in-window misses, attributed

| Key | Reference | Attribution |
|---|---|---|
| `pfeiffer2020` | AdapterFusion: Non-Destructive Task Composition for Transfer Learning (EACL 2021) | **Genuine defect.** On-topic for block B1. See below. |
| `shoeybi2019` | Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism | No protocol query targets tensor/model parallelism; subject is pre-training throughput, which engages exclusion criterion 1. |
| `huang2019` | GPipe: Efficient Training of Giant Neural Networks Using Pipeline Parallelism | No protocol query targets pipeline parallelism; arXiv preprint (1811.06965) predates the window. |
| `loshchilov2019` | Decoupled Weight Decay Regularization (AdamW) | No protocol query targets optimizers; arXiv preprint (1711.05101) predates the window. |
| `rolnick2019` | Experience Replay for Continual Learning | No protocol query targets continual-learning replay; arXiv preprint (1811.11682) predates the window. |

Four of the five are cited in the manuscript as **foundational background** for systems and
optimization context, not as efficient fine-tuning methods. The protocol's query blocks (PEFT,
quantization, memory optimization, distributed/federated) deliberately do not cover optimizers,
pipeline parallelism, or continual-learning replay. Their non-retrieval is explainable and
consistent with the stated scope; it is a boundary condition of the query design, not a failure of
execution.

`pfeiffer2020` is different, and is a real recall defect: adapters are the core subject of block B1.

---

## Why AdapterFusion was missed

Two independent causes, both structural rather than accidental.

### 1. The B1 adapter query is a four-term conjunction

`B1_peft_3` (boolean form, used for arXiv and IEEE) is:

```text
"adapter" AND "transformer" AND "fine-tuning" AND efficient
```

Every term must be present. The arXiv **2020 slice for this query returned 8 records in total**,
and the slice did not reach the 200 result cap — so truncation is ruled out. The conjunction itself
excluded AdapterFusion, whose abstract does not carry all four required terms.

For scale, this query returned 2 records for 2019 and 10 for 2021, against 123 for 2024.

### 2. Semantic Scholar was capped and never date-sliced

Semantic Scholar was run once per query with a 200-record relevance cap and no date slicing.
**17 of 18 queries hit that cap.** Because ranking is by relevance and the recent literature is far
larger, the returned set is overwhelmingly recent:

| Query | Pre-2022 records returned |
|---|---|
| `B1_peft_1` (parameter-efficient fine-tuning large language models) | 0 of 200 |
| `B1_peft_3` (adapter modules transformer parameter efficient) | 2 of 200 |
| All 18 queries combined | 121 of 3,500 (3.5%) |

Semantic Scholar is the source whose relevance ranking would be expected to surface a seminal,
highly cited adapter paper. Under a 200-record cap with no date slicing, it never reached back far
enough to do so.

### Combined consequence

Coverage of 2019–2021 rests almost entirely on arXiv's restrictive boolean conjunctions, because
the relevance-ranked sources were saturated by recent work.

| Retrieval year | arXiv records (all queries) | Pool candidates |
|---|---|---|
| 2019 | 15 | 82 |
| 2020 | 34 | 136 |
| 2021 | 105 | 230 |
| 2024 | 2,972 | 2,602 |

Pre-2022 candidates are **448 of 10,333 (4.3%)** of the pool. The field did grow sharply after 2022,
so some skew is genuine and expected. But 15 arXiv records for all of 2019 across 18 date-sliced
queries is too thin to be explained by growth alone. The queries require vocabulary that
stabilised later — "large language model", "LLM", "PEFT" — whereas 2019–2021 work says
"pre-trained language model", "BERT", or names a specific model.

---

## Supplementary retrieval outcome (protocol v1.3)

Run 2026-07-31 via `search/scripts/search_supplementary.py`; raw output in
`search/raw/supplementary/known_corpus_misses.json`. All six in-window references with no
pool match were looked up by title. **All six resolved.**

| Key | Matched title | Year (source) | Citations | Identifier |
|---|---|---|---|---|
| `pfeiffer2020` | AdapterFusion: Non-Destructive Task Composition for Transfer Learning | 2020 | 1,217 | `10.18653/v1/2021.eacl-main.39`, arXiv 2005.00247 |
| `shoeybi2019` | Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism | 2019 | 3,010 | arXiv 1909.08053 |
| `huang2019` | GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism | 2018 | 2,208 | NeurIPS |
| `rolnick2019` | Experience Replay for Continual Learning | 2018 | 1,742 | arXiv 1811.11682 |
| `loshchilov2019` | Decoupled Weight Decay Regularization | 2017 | 36,964 | ICLR |
| `bayati2023` | **Flexora**: Flexible Low Rank Adaptation for Large Language Models | 2024 | 16 | arXiv 2408.10774 |

AdapterFusion carries **1,217 citations** — far above the 50-citation adoption bar of
inclusion criterion 3. Its omission was therefore a recall failure on a paper that plainly
met the community-adoption threshold, which is the strongest form the defect could take.

### `bayati2023` is a different work, and is not treated as recovered

The lookup for `bayati2023` ("FlexLoRA", cited as 2023) matched **Flexora** (2024,
arXiv 2408.10774) at title ratio 0.992 — a near-identical string for a different paper by
different authors. This independently corroborates the Phase 2 venue-check decision to
reject `bayati2023`: the work does not exist as cited.

`dedupe.py` refuses to load any supplementary lookup whose matched title is not *identical*
to the cited title, precisely so a near-miss cannot silently substitute one paper for
another. `bayati2023` is therefore **not** counted as recovered. Flexora itself was already
retrieved by the Phase 2 queries and remains in the pool on its own merits.

### An additional mechanism: arXiv retrieval keys on submission date

Three of the five — GPipe, experience replay, and AdamW — are in-window by *publication*
date (NeurIPS 2019, NeurIPS 2019, ICLR 2019) but were first posted to arXiv in 2018, 2018,
and 2017 respectively. The arXiv API filters on `submittedDate`, so a date-sliced arXiv
search bounded at 2019-01-01 **cannot** return them regardless of query terms.

This is a general boundary effect at the start of the coverage window, not specific to
these three: any paper published in 2019 after a 2018 preprint is invisible to the
date-sliced arXiv search while still satisfying inclusion criterion 5, which reads
"published (**or** first posted, for preprints)". The v1.3 Semantic Scholar backfill
mitigates this because Semantic Scholar's `year` filter keys on publication year rather
than preprint submission date.

---

## Consequences for the protocol

1. The confirmation pass verifies **24 of 29** in-window manuscript references, not all of them.
   This is stated as such in `screening/prisma-counts.md`; it is not rounded up.
2. The 2019–2021 band is under-retrieved for reasons now understood and documented. Protocol v1.3
   adds a date-sliced Semantic Scholar backfill for 2019–2021 and a targeted supplementary
   retrieval for the known-corpus misses. See `protocol/CHANGELOG.md`.
3. Claims about the *recent* literature (2022 onward) are unaffected. The under-retrieval is
   confined to the confirmation band, which exists to verify already-cited foundational work rather
   than to discover new work.

---

## Backfill outcome (protocol v1.3)

Run 2026-07-31. All 18 `s2_queries` re-run for each of 2019, 2020, 2021 — 54 slices, 200-record
cap per slice. Raw output in `search/raw/semanticscholar_backfill/`.

| Measure | Result |
|---|---|
| Slices run | 54 of 54 |
| Records retrieved | 6,775 |
| Slices reaching the 200 cap | 26 |
| New unique candidates added | 5,185 (all 2019–2021) |
| Pre-2022 share of the pool | 4.3% → **36.4%** |
| Pool size | 10,333 → **15,518** |

Per-year retrieval moved from 82 / 136 / 230 candidates (2019 / 2020 / 2021) to
1,731 / 1,867 / 2,049. The single-query comparison is the clearest evidence that the cause was
cap saturation rather than absence of literature: `B1_peft_1` returned **0** pre-2022 records
unsliced, and **200 of 722 available** for 2019 alone once sliced.

### Residual limit

26 of 54 slices still reached the cap, so the confirmation band is improved but **not
exhaustive**. Recursive sub-slicing (half-year / quarter) was not performed for this band: its
purpose is to verify already-cited work and surface high-adoption papers, not to enumerate the
period. Combined with the arXiv submission-date boundary effect above, no claim of complete
2019–2021 coverage is made.

