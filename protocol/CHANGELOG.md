# Protocol Changelog

## v1.3 — 2026-07-31

Triggered by a confirmation-pass diagnostic run at Phase 3 entry, which tested whether
the Phase 2 search actually retrieved the 42 references the manuscript already cites.
Full evidence: `search/coverage-diagnostic.md`.

### Finding: the confirmation pass verified 24 of 29 in-window references, not all

Of 42 manuscript references, 29 are in the deduplicated pool. Seven of the 13 absent
predate the coverage window (correctly excluded by criterion 5) and one (`bayati2023`)
was already rejected at venue check. Five are in-window and were retrieved by no query
on any of the seven sources.

Four of the five — GPipe, Megatron-LM, AdamW, experience replay — are cited as
foundational systems/optimization background on topics no query block covers (pipeline
parallelism, tensor parallelism, optimizers, continual-learning replay). Their absence
is a documented boundary condition of the query design, not an execution failure.

**AdapterFusion (`pfeiffer2020`) is a genuine recall defect**: adapters are the core
subject of block B1. Two structural causes were identified.

### Defect 1: relevance-ranked retrieval saturated on recent work

v1.2 capped Semantic Scholar at 200 records **per query with no date slicing**, while
v1.1 already required date-slicing for arXiv. **17 of 18 Semantic Scholar queries hit
the cap**, and only 121 of 3,500 returned records (3.5%) predate 2022. `B1_peft_1`
returned zero pre-2022 records. The source whose relevance ranking would have surfaced a
seminal adapter paper never reached back far enough to do so.

Fix: **date-sliced Semantic Scholar backfill for 2019, 2020, 2021** — all 18 `s2_queries`
re-run per year slice at the 200-record cap, into `search/raw/semanticscholar_backfill/`.
This applies the v1.1 arXiv rule to Semantic Scholar; no query string changes.

### Defect 2: over-restrictive conjunction in B1_peft_3

The boolean form `"adapter" AND "transformer" AND "fine-tuning" AND efficient` requires
all four terms. The arXiv 2020 slice for this query returned **8 records and did not
reach the cap**, so truncation is excluded as an explanation — the conjunction itself is
the cause.

**Not fixed by rewriting the query.** Altering query strings after seeing results would
make the search unreproducible against its own log. The limitation is documented and
reported instead, and the affected band is remediated by retrieval (defect 1) rather than
by redefining the query.

### Change: targeted supplementary retrieval of known-corpus misses

In-window references from `search/existing-references.yaml` absent from the pool are
retrieved directly by title/DOI into `search/raw/supplementary/`. This is verification of
an already-cited corpus, **not discovery**, is logged separately as such, and must not be
described as extending the search's reach. Recovered records are screened against the
same criteria as any other candidate.

### Change: screening procedure specified and disclosed

New document: `protocol/screening-procedure.md`.

- Stage 1 is **LLM-assisted under author supervision**. Every inclusion is
  author-verified; every low-confidence decision is author-reviewed; a stratified random
  sample of **≥ 250 exclusions** is audited with a recorded seed, and the disagreement
  rate is reported. A disagreement rate above **5%** requires re-screening the affected
  stratum rather than patching it. Threshold fixed in advance.
- **Scope bound:** full Stage 1 screen of the 7,779 records from 2024-01-01 onward;
  the 2,513 records from 2019–2023 receive a targeted confirmation pass keyed to the
  existing corpus, ≥ 50 citations, core-method terms, or survey status. Records not
  examined under the bound are reported as `not_screened_confirmation_band`, a distinct
  PRISMA line — **not** as exclusions.
- **A keyword pre-filter was tested and rejected.** Built from the protocol's own
  vocabulary, it removed only 37% of the pool while dropping LoRA+, VeRA, ZeRO-Offload,
  and FlashAttention-2 — four references the manuscript cites. 86% recall against
  known-relevant work is not an acceptable basis for exclusion. No keyword filter
  excludes any record.
- Required disclosure wording for the methodology and Section 10.4 is fixed verbatim in
  `screening-procedure.md` §8.

### Unchanged from v1.2

Coverage window, all 18 query strings, inclusion/exclusion criteria, extraction schema,
retrieval caps for arXiv / IEEE / OpenAlex / DBLP, the prohibition on scraping Google
Scholar, and the single-author non-PRISMA framing. v1.3 retrieval is strictly additive:
no v1.2 result is removed or altered.

### Sequencing

v1.3 must be committed **before** the backfill, the supplementary retrieval, and the
first recorded Stage 1 decision.

### Execution outcome (2026-07-31, after this amendment was committed)

**Backfill:** 54 of 54 slices run; 6,775 records retrieved; 5,185 new unique candidates,
all 2019–2021. Pre-2022 share of the pool moved from 4.3% to **36.4%**; pool size
10,333 → **15,518**. The decisive single-query comparison: `B1_peft_1` returned 0
pre-2022 records unsliced and 200 of 722 available for 2019 alone once sliced, confirming
cap saturation rather than absent literature. 26 slices still reached the cap, so the band
is improved but not exhaustive, and is not claimed to be.

**Supplementary retrieval:** all 6 lookups resolved. Five are counted as recovered
(AdapterFusion, Megatron-LM, GPipe, AdamW, experience replay); in-window references now
represented is **34 of 34**. `bayati2023` matched *Flexora* (2024, arXiv 2408.10774), a
different paper, and is **not** counted as recovered — this corroborates the Phase 2 venue
check that rejected it. `dedupe.py` refuses any supplementary match whose title is not
identical to the cited title.

**Two defects found and fixed during execution, both affecting data integrity:**

1. Neither `search_semanticscholar.py` nor `search_supplementary.py` loaded `local.env`, so
   both ran unauthenticated and were heavily throttled. The first supplementary run recorded
   GPipe as "NOT FOUND" purely from rate limiting; it matches at title ratio 1.0 once
   authenticated. Lookups now distinguish `no_match` from `unresolved` so throttling can
   never be recorded as evidence of absence.
2. `candidate_id` was positional (`C00001` by sort order), so regenerating the pool
   renumbered every record and would have silently reassigned screening decisions. Ids are
   now derived from DOI, arXiv ID, or normalized title.

**One metadata correction:** Semantic Scholar reports preprint posting years, which dated
GPipe to 2018, experience replay to 2018, and AdamW to 2017 — outside the coverage window —
even though all three were published in 2019 (NeurIPS, NeurIPS, ICLR). Criterion 5 reads
"published (**or** first posted, for preprints)", so the verified publication year governs
for these records. Without the fix, the mechanical date rule would have excluded the very
references the supplementary retrieval was run to recover.

**Scope bound applied:** of 7,699 confirmation-band records, 3,142 meet a §4 trigger and are
screened; 4,557 are recorded `stage_1_not_screened` with empty decisions. Total receiving a
Stage 1 judgement: **10,961** (10,938 pending plus 23 already excluded mechanically under
exclusion 6).

### Criterion 5 clarified, not changed

The preprint-year correction above rested on an unstated reading of criterion 5, so the
reading is now written into `inclusion-exclusion.md`: **peer-reviewed works are dated by
publication date; "first posted" governs unpublished items only.** The criterion's text and
window are untouched and no decision changes — this records an interpretation that was
already being applied, rather than rewriting criteria after screening began. It affects
three boundary records, BERT among them.

### Batch payload and screening calibration

Batch files gained `record_type` and `arxiv_only` after an author spot-check found record
type absent from the payload. Record type is present for only 1,671 of 15,518 pool records
(11%), so venue and the arXiv-only flag carry exclusion 6 where it is missing.

Author review of the pilot block set a confidence rule now recorded in
`screening-procedure.md`: confidence reports certainty in the decision, not enthusiasm for
the record, and a bare title with no abstract rarely supports high confidence. Bias the
decision toward inclusion; keep the confidence honest. Records that cannot be identified at
all are held for metadata recovery rather than advanced.

### Criteria 1, 2 and 6 clarified, not changed (author calibration, batch 001)

Two scope boundaries were written out during author review of the batch-001 calibration
packet. Criteria text unchanged; readings now explicit in `inclusion-exclusion.md` and
`screening-procedure.md` §2.1. **Applied from new-work batch 002 onward**; batch 001 stands
as screened and is verified by the author against these rules.

**Criterion 2 clarified, not changed — two-part LLM-only rule plus research-question test:**
a paper is in scope only if **(a) the model is an LLM** (or it is a survey of efficiency methods
for language models) and **(b) the research question is about the fine-tuning-efficiency method
itself** (performance, applicability, or improvement), including comparative evaluations of the
method. It is out of scope if the research question is about a task or system and the efficiency
method is only the tool used to build it. Vision, speech, graph, audio, multimodal, and
general-ML papers fail criterion 2 unless the method is general and demonstrated on an LLM.
Domain applications on LLMs fail **inclusion criterion 1**. Author calibration of batch 001
applied this test; see `screening/reviews/new-work-batch-001-reconciliation.md`.

**Criterion 6 — book chapters:** textbook, tutorial, and pedagogical book chapters are excluded
as non-archival secondary material. Peer-reviewed conference/journal papers and papers in
edited scholarly proceedings remain eligible.

**Log updates:** held record `C-34a4a73f19` reclassified to exclude (exclusion 6); held record
`C-3187c706f6` remains held.

**Verification block size** reduced from 750 to **375 records** after batch 001 showed a 35%
low-confidence rate (~260 review items per 750-record block). Realistic submission target noted
as **2026-08-20**.

### New-work band screened in a single automated pass (2026-08-17)

The remaining **7,628** new-work records were screened in one automated Stage 1 pass
(`screener: automated`, `screening/scripts/auto_stage1.py`) under the encoded v1.3 rule.
This is **not** per-block human verification. The classifier was calibrated to 150/150
agreement against author-resolved batch 001, then applied uniformly. Human verification
is applied to the ranked shortlist (`screening/reviews/reference-shortlist.md`), not the
full pool. Confirmation-band records were not part of this pass.

Outcome: **2,982 include / 4,646 exclude** on the 7,628. Combined with batch 001, the
new-work band is **3,016 include / 4,782 exclude**. Ranking used all 3,016 includes.

---

## Phase 3 entry — 2026-07-31 (artifact regeneration, no protocol change)

The search protocol, queries, coverage window, and inclusion/exclusion criteria are
unchanged. Recorded here because published Phase 2 counts moved slightly.

### Candidate pool regenerated to carry screening metadata

`search/scripts/dedupe.py` discarded three fields the screening criteria depend on.
It now carries them from the raw responses already on disk; **no source was re-queried**
and `search/raw/` is byte-identical to the Phase 2 state.

- **Citation counts** (`citations`, `citations_source`) from Semantic Scholar
  `citationCount`, OpenAlex `cited_by_count`, IEEE `citing_paper_count`, and the
  Scholar `cited_by` column. Inclusion criterion 3 cannot be applied without these.
- **Language** (OpenAlex `language`) for criterion 4, and **record type** for
  exclusion criterion 6.
- **Abstracts** reconstructed from OpenAlex `abstract_inverted_index`, which was
  previously dropped. Abstract coverage rose from 9,000 to 9,899 of the pool, which
  matters because Stage 1 is a title/abstract screen.

Two merge refinements, both narrowing rather than widening the pool:

- arXiv IDs are now also read from OpenAlex alternate `locations`, not `ids` alone.
  This merged one additional preprint/published pair: **unique candidates 10,334 →
  10,333**, arXiv-ID coverage 7,782 → 7,974, multi-source merges 1,538 → 1,537.
- Merged clusters now take the longest abstract and the highest citation count from
  any record in the cluster, rather than only the canonical record's. The canonical
  (published) record frequently carried no abstract while its merged preprint did.

Pre-dedup record count is unchanged at **18,343**, confirming the regeneration did not
alter retrieval. Counts in `screening/prisma-counts.md` are updated accordingly.

### Stray duplicate files removed from the working tree

124 byte-identical `"<name> 2.json"` / `"<name> 2.py"` copies (file-manager artifacts,
never tracked by git) were present under `search/raw/` and `search/scripts/`. They
inflated a dedup run to 28,646 raw records before removal. All were verified identical
to their tracked originals by checksum and moved out of the repository. Tracked files
were untouched.

---

## v1.2 — 2026-07-22

Phase 2b source-substitution amendment. Triggered because v1.0/v1.1 classified
IEEE Xplore and ACM Digital Library as manual-only, which was partly incorrect.

### Change: programmatic retrieval for IEEE and ACM coverage

- **IEEE Xplore:** official Metadata Search API (`ieeexploreapi.ieee.org`) with
  free key registration. Boolean queries, year filter, abstracts. Cap:
  **top 50 by relevance per query** (equivalent to the manual stopping rule).
- **ACM Digital Library:** no public search API. ACM-published works retrieved
  via **OpenAlex** (and Crossref for DOI/venue verification), including an
  ACM publisher-filtered OpenAlex run. Keyword `s2_queries` variants; cap 50.
- **OpenAlex (general index):** same keyword queries and 50-cap, for broader
  coverage beyond ACM.
- **ACM publisher ID:** amendment draft cited `P4310320503`; OpenAlex lookup
  confirmed **Association for Computing Machinery** as `P4310319798` (recorded
  in `search/queries.yaml`). Scripts verify the publisher display name before
  the ACM-filtered run.
- **DBLP (optional):** CS-venue completeness check; same 50-cap. Adopted for
  venue-string quality without expanding screening burden beyond the cap.
- **Google Scholar:** unchanged — still manual; no scraping.

### Unchanged from v1.1 / v1.0

Coverage window, inclusion/exclusion, extraction schema, arXiv/S2/OpenReview
decisions, 200-cap date-slicing for arXiv, prohibition on Scholar scraping,
single-author non-PRISMA framing. This is a **retrieval-mechanism** change,
not a scope change.

### Execution outcome (recorded at Phase 2 close, 2026-07-31)

All v1.2 sources ran to completion: IEEE 18/18 (705 records), OpenAlex general
18/18 (900), OpenAlex ACM-filtered 18/18 (636), DBLP 18/18 (164), Google Scholar
18 protocol queries as 34 manual runs (597 records after removing interface
artifacts and one duplicate).

Deduplication across all seven sources reduced **18,343** retrieved records to
**10,334** unique candidates (**10,313** excluding Scholar out-of-protocol rows).
This exceeds the 6,000–7,000 figure the amendment used when arguing for the
50-record cap. The discrepancy comes from arXiv date-slicing under v1.1 (11,841
records across 119 sliced query files), not from the v1.2 substituted sources,
which contributed 2,405 capped records in total. The cap did what it was intended
to do; the pre-existing arXiv volume was simply larger than the amendment
assumed. Stage 1 screening should be planned against 10,313, not 7,000.

### Sequencing

v1.2 protocol text must be committed **before** IEEE / OpenAlex / DBLP runs.

---

## v1.1 — 2026-07-21

Triggered by execution of v1.0 (commit d7313cd). Three defects identified.

### Defect 1: Operator precedence error in B3_memory_3

v1.0 string: `"ZeRO" OR "DeepSpeed" OR "offloading" AND "model training"`  
Boolean precedence binds AND tighter than OR, parsing this as
`ZeRO OR DeepSpeed OR (offloading AND "model training")`. Unbounded on the
first two terms. Evidence: arXiv totalReported approximately 17,852.  
Fix: explicit parentheses. See `docs/PROTOCOL_V1.1_AMENDMENT.md` section 3.1
(local amendment guide) / corrected string in `search/queries.yaml`.

### Defect 2: Query syntax incompatible with Semantic Scholar API

v1.0 specified one boolean syntax for all sources. The Semantic Scholar
`query=` parameter performs relevance keyword matching, not boolean
evaluation. Evidence: B2_quantization_2 returned 0 results,
B3_memory_2 returned 0, B1_peft_2 returned 1.  
Fix: source-specific `s2_queries` keyword variants in `search/queries.yaml`.

### Defect 3: Retrieval cap reached without coverage strategy

9 of 18 arXiv queries reached the 200-result cap with larger totals
reported. v1.0 stated "narrow the query and record the change" but did
not specify a method preserving search intent.  
Fix: date-slicing plus explicit stopping rule (amendment sections 4–5).
Implementation of `--slice-by-year` follows after this amendment is committed
and confirmed.

### Unchanged from v1.0

Coverage window, inclusion/exclusion criteria, extraction schema,
manual stopping rule (first 50 by relevance), prohibition on scraping
Google Scholar, single-author non-PRISMA framing.

### Artifact handling

- v1.0 raw API responses preserved under `search/raw_v1.0/` (not deleted).
- Fresh v1.1 runs will write to `search/raw/` after owner confirmation.
