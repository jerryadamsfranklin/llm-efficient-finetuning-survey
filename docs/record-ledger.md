# Record ledger, revision 3
Compiled on 2026-10-24 from branch revision-3 at commit dce6da7.

This file reproduces Phase 0 sections B and C as tables, with file and column citations. All counts are computed from repository files on this branch unless marked UNKNOWN or AMBIGUOUS.

---

## B. Ledger

### B.3 Raw records per source

From `search/dedupe-summary.json` field `raw_by_source` (and matching `screening/prisma-counts.md` Identification table).

| Source | Raw count | Citation |
|---|---:|---|
| arXiv | 11841 | `dedupe-summary.json` -> `raw_by_source.arxiv` |
| Semantic Scholar (unsliced) | 3500 | `raw_by_source.semanticscholar` |
| Semantic Scholar (2019-2021 backfill) | 6775 | `raw_by_source.semanticscholar_backfill` |
| Semantic Scholar (sum of both) | 10275 | sum of the two fields above |
| OpenAlex | 900 | `raw_by_source.openalex` |
| OpenAlex-ACM | 636 | `raw_by_source.openalex_acm` |
| DBLP | 164 | `raw_by_source.dblp` |
| IEEE Xplore | 705 | `raw_by_source.ieee` |
| Google Scholar | 597 | `raw_by_source.google_scholar`; see Google Scholar resolution below |
| OpenReview (discovery into pool) | NOT RUN | `raw_by_source` has no `openreview` key |
| Crossref (discovery into pool) | NOT RUN | no `search/raw/crossref/`; not in `raw_by_source` |
| Supplementary known-corpus lookups | 5 | `raw_by_source.supplementary` |

### Google Scholar resolution (602 CSV rows vs 597 summary)

File: `search/raw/google_scholar/google_scholar_candidates.csv`.

| `bucket` value | Row count (`csv.DictReader`) |
|---|---:|
| B1_2_lowrank_variants | 121 |
| B2_1_quant_llm_ft | 83 |
| B3_3_zero_deepspeed_offload | 65 |
| B3_4_memory_opt | 42 |
| B1_1_peft_llm | 42 |
| B1_5_peft_survey | 40 |
| B3_1_grad_checkpoint | 40 |
| B3_2_flashattention | 40 |
| B4_3_distributed_comm | 23 |
| OUT_OF_PROTOCOL | 21 |
| B2_2_gptq_awq_smoothquant_qlora | 20 |
| B4_2_federated_lora | 19 |
| B2_3_ptq_llm | 16 |
| B4_1_federated_llm | 11 |
| B2_5_lowbit_survey | 4 |
| B2_4_qat_transformer | 4 |
| NOISE_UI | 4 |
| B1_3_adapter | 3 |
| B1_4_prompt_prefix_bitfit | 2 |
| DUPLICATE | 1 |
| B4_4_federated_heterogeneity | 1 |
| **All rows** | **602** |

Filter that yields **597**: exclude rows where `bucket` is `NOISE_UI` or `DUPLICATE` (4 + 1 = 5; 602 - 5 = 597). This matches `dedupe-summary.json` -> `raw_by_source.google_scholar` and the prisma wording "excl. NOISE_UI/DUPLICATE". Note: the 597 figure still includes the 21 `OUT_OF_PROTOCOL` rows; those are subtracted later as `out_of_protocol` = 21 at the pool level.

### B.4 Totals after dedup

| Quantity | Value | Citation |
|---|---:|---|
| Total raw | 25123 | `dedupe-summary.json` -> `raw_records` |
| Unique after dedup | 15518 | `dedupe-summary.json` -> `unique_candidates` |
| Removed by dedup | 9605 | 25123 - 15518 |
| Unique for screening (in-protocol) | 15497 | `dedupe-summary.json` -> `unique_for_screening` |
| Out of protocol | 21 | `dedupe-summary.json` -> `out_of_protocol` |
| Screening-log rows | 15518 | `screening/screening-log.csv` via `csv.DictReader` |

### B.5 De-duplicated pool by screening date band

From `screening/screening-log.csv`.

**Column `priority_band`:**

| Band | n | Citation |
|---|---:|---|
| `new_work` | 7798 | count where `priority_band=new_work` |
| `confirmation` | 7701 | count where `priority_band=confirmation` |
| `unknown_year` | 19 | count where `priority_band=unknown_year` |

**Column `year` (calendar split):**

| Band | n | Citation |
|---|---:|---|
| 2019-2023 | 7701 | `year` integer in [2019, 2023] |
| 2024+ | 7798 | `year` >= 2024 |
| missing year | 19 | empty `year` |

### B.6 Per band: automated / human / pending

From `screening/screening-log.csv` columns `priority_band`, `screener`, `decision`, `stage_reached`.

#### `new_work` (n=7798)

| Category | n | Detail |
|---|---:|---|
| Automated classifier decision | 7621 | `screener=automated`: include 2976, exclude 4645 |
| LLM-assisted decision | 130 | `screener=llm_assisted` |
| Author decision | 27 | `screener=author` |
| Metadata exclusion | 20 | `screener=metadata` |
| Pending (empty `decision`) | 0 | |

Band totals after all screeners: include **3011**, exclude **4787** (`decision` column).

#### `confirmation` (n=7701)

| Category | n | Citation |
|---|---:|---|
| Automated classifier | 0 | no `screener=automated` |
| Metadata exclusion | 2 | `decision=exclude`, `screener=metadata` |
| Pending empty decision, trigger met | 3142 | empty `decision`, `stage_reached=stage_1_pending` |
| Pending empty decision, no trigger | 4557 | empty `decision`, `stage_reached=stage_1_not_screened` |

#### `unknown_year` (n=19)

| Category | n |
|---|---:|
| With decision | 19 (include 14, exclude 4, hold 1) |
| Screener mix | `llm_assisted` 16, `author` 2, `metadata` 1 |

### B.7 Calibration sample (150) and agreement stats

| Item | Value | Citation |
|---|---|---|
| Records in calibration sample | 150 | `screening/decisions/stage1_new_work_001.json` -> `decisions` length |
| Original decisions in that file | include 54, exclude 96 | Counter on `decision` |
| Agreement rates | table below | `screening/reviews/new-work-batch-001-reconciliation.md` section "Agreement rates" |

| Comparison | n | agree | disagree | rate |
|---|---:|---:|---:|---|
| Original packet vs Cursor (before the 7 catches) | 100 | 87 | 13 | 87% |
| Original packet vs the fully encoded rule | 100 | 80 | 20 | 80% |
| Author verdicts after resolutions vs encoded rule | 100 | 100 | 0 | 100% |
| Cursor original vs encoded rule, full batch of 150 | 150 | 130 | 20 | 87% |

### B.8 Shortlist / full text / finally included

| Item | Value | Citation |
|---|---|---|
| Records on shortlist | 30 | `screening/reviews/reference-shortlist.md` headings `### 1.` through `### 30.` |
| Selected for insertion | 13 | same file; 13 lines with `**selected` |
| Stage 2 pending | 3025 | `screening-log.csv` where `stage_reached=stage_2_pending` |
| Full-text assessed (completed Stage 2) | TBD / 0 completed files | `screening/prisma-counts.md` line: `Full text assessed (Stage 2) \| TBD`; no Stage 2 decision JSON |
| Extraction rows | 0 | `data/included-papers.csv` is header + status comment only |
| Narrative manuscript corpus | 55 (= 42 + 13) | `protocol/CHANGELOG.md` "Cited corpus 42 -> 55" |

### B.9 Original 42 vs shortlist additions

| Item | Value | Citation |
|---|---|---|
| Original curated set | 42 | `search/existing-references.yaml` -> `n_references: 42` |
| From search shortlist | 13 | `reference-shortlist.md`; CHANGELOG manuscript insertion of the verified 13 |
| Split inside `data/included-papers.csv` | UNKNOWN | file is Phase 4 placeholder |

---

## C. Inconsistency scan (summary tables)

### C.10 Number / phrase hits (path:line)

Canonical current pool size **15,518** / **15518** appears in: `README.md` (41, 66, 76); `search/dedupe-summary.json` (6); `search/search-log.md` (1769); `search/coverage-diagnostic.md` (3, 190); `protocol/screening-procedure.md` (12); `protocol/CHANGELOG.md` (94, 141); `screening/prisma-counts.md` (21, 61, 70, 71, 74).

Pre-v1.3 figure **10,333** appears labelled as historical in: `README.md` (66, 76); `search/coverage-diagnostic.md` (3, 110, 190); `protocol/CHANGELOG.md` (94, 238).

**10,938** Stage 1 judgement target appears in: `README.md` (41, 84); `protocol/screening-procedure.md` (50); `protocol/CHANGELOG.md` (126); `screening/prisma-counts.md` (81, 85, 102).

**7,628** automated-pass size appears in: `protocol/screening-procedure.md` (210); `protocol/CHANGELOG.md` (180, 187).

**2,982** appears in: `protocol/CHANGELOG.md` (187) as the automated-pass include count before later edits.

**PRISMA** / **systematic review** / **comprehensive** hits: see Phase 0 report section C.10 for full lines (README, docs, protocol, screening scripts and calibration titles). Framing in protocol files is "PRISMA-informed" / "not a registered systematic review".

### C.11 Sources named in README.md and docs/

**README.md (executed / checklist):** arXiv; Semantic Scholar (incl. v1.3 backfill); OpenReview (venue check only on checklist); OpenAlex; OpenAlex ACM-filtered; IEEE Xplore metadata API; DBLP; Google Scholar (manual); Hugging Face (reference; zero records).

**docs/:** same set plus Crossref as verification; ACM via OpenAlex/Crossref; Papers With Code mentioned as a gap in the build guide.

---

## Reconciliations

### 7,628 automated decisions vs 7,621 with `screener=automated`

| Quantity | Value | Citation |
|---|---:|---|
| Decisions in automated file | 7628 | `screening/decisions/stage1_new_work_automated.json` -> `n_records` and `len(decisions)` |
| Log rows with `screener=automated` | 7621 | `screening/screening-log.csv` column `screener` |
| Gap | 7 | 7628 - 7621 |

Those 7 IDs appear in the automated decisions file but currently have `screener=author` in `screening/screening-log.csv` (post-hoc author overrides):

| ID | Current `decision` | Title (truncated from log) |
|---|---|---|
| `C-2237f357ff` | include | LoRA-XS: Low-Rank Adaptation with Extremely Small Number of ... |
| `C-3b4f1737c6` | exclude | An Emotion Text Classification Model Based on Llama3-8b ... |
| `C-3c82c940b7` | exclude | Harnessing Earnings Reports for Stock Predictions: A QLoRA-E ... |
| `C-541eb63c42` | exclude | BioMistral: A Collection of Open-Source Pretrained Large Lan ... |
| `C-61b96120af` | exclude | LongVILA: Scaling Long-Context Visual Language Models ... |
| `C-80ade0780f` | exclude | Break the Sequential Dependency of LLM Inference Using Looka ... |
| `C-81185e06f7` | exclude | Bi-directional Adapter for Multimodal Tracking |

Both 7628 and 7621 are correct: 7628 is the automated pass size; 7621 is the count still labelled automated after 7 author overrides.

### 2,982 / 4,646 vs 3,011 / 4,787

From `protocol/CHANGELOG.md` (2026-08-17 automated-pass and shortlist entries):

1. Automated pass on remaining 7,628: **2,982 include / 4,646 exclude** (CHANGELOG lines describing Outcome on the 7,628).
2. Combined with batch 001: **3,016 include / 4,782 exclude**.
3. After shortlist author review and LoRA-XS overturn: **3,011 include / 4,787 exclude**.

Current `screening/screening-log.csv` for `priority_band=new_work`: **3011 include / 4787 exclude** (matches step 3). Prisma lines for new-work includes/excludes match 3,011 / 4,787.

---

## Search sources: discovery vs verification

### Discovery sources (records in the de-duplicated pool)

| Source | Raw count (`raw_by_source`) |
|---|---:|
| arXiv | 11841 |
| Semantic Scholar (unsliced) | 3500 |
| Semantic Scholar backfill | 6775 |
| OpenAlex | 900 |
| OpenAlex-ACM | 636 |
| IEEE Xplore | 705 |
| Google Scholar | 597 |
| DBLP | 164 |
| Supplementary | 5 |
| **Total raw** | **25123** |

### Verification-only services

| Service | Role | File showing the use |
|---|---|---|
| OpenReview | Venue check of existing manuscript references; not a discovery contributor to `raw_by_source` | `search/raw/openreview/existing_references_venue_check.json` (`mode=existing_references_venue_check`, `n_references=42`); script `search/scripts/search_openreview.py` / venue-check path |
| Crossref | DOI / published-venue verification | `search/scripts/venue_check.py` (Crossref API calls); outputs summarized in `docs/reference-corrections.md`; protocol table in `protocol/search-protocol.md` lists Crossref as "DOI resolution and published-venue verification" |

---

## Stage summary

| Stage | n | Citation (from section B) |
|---|---:|---|
| Retrieved | 25123 | `dedupe-summary.json` -> `raw_records` |
| De-duplicated | 15518 | `unique_candidates` |
| In-protocol | 15497 | `unique_for_screening` |
| Automated decision | 7621 | `screening-log.csv` `screener=automated` |
| LLM-assisted decision | 146 | `screener=llm_assisted` (all bands: new_work 130 + unknown_year 16) |
| Author decision | 29 | `screener=author` |
| Metadata exclusion | 23 | `screener=metadata` |
| Confirmation band pending (trigger met, unscreened) | 3142 | `priority_band=confirmation` and `stage_reached=stage_1_pending` |
| Confirmation band not screened (no trigger) | 4557 | `stage_reached=stage_1_not_screened` |
| Check: automated + LLM-assisted + author + metadata + confirmation pending + not screened | 15518 | 7621 + 146 + 29 + 23 + 3142 + 4557 = 15518 (equals `unique_candidates`) |
| Stage 2 pending | 3025 | `stage_reached=stage_2_pending` |
| Full-text assessed | 0 | prisma TBD; no completed Stage 2 decision files |
| Extraction rows | 0 | `data/included-papers.csv` data rows |

---

## Decision confidence

Counts from `screening/screening-log.csv` for rows with a non-empty `decision`, grouped by `priority_band` x `screener` x `decision` x `confidence`. Total non-empty decisions: **7819**.

| priority_band | screener | decision | confidence | n |
|---|---|---|---|---:|
| confirmation | metadata | exclude | high | 2 |
| new_work | author | exclude | high | 26 |
| new_work | author | include | high | 1 |
| new_work | automated | exclude | high | 3924 |
| new_work | automated | exclude | low | 721 |
| new_work | automated | include | high | 2076 |
| new_work | automated | include | low | 900 |
| new_work | llm_assisted | exclude | high | 70 |
| new_work | llm_assisted | exclude | low | 26 |
| new_work | llm_assisted | include | high | 27 |
| new_work | llm_assisted | include | low | 7 |
| new_work | metadata | exclude | high | 20 |
| unknown_year | author | exclude | low | 1 |
| unknown_year | author | hold | low | 1 |
| unknown_year | llm_assisted | exclude | high | 2 |
| unknown_year | llm_assisted | include | high | 7 |
| unknown_year | llm_assisted | include | low | 7 |
| unknown_year | metadata | exclude | high | 1 |

Automated subset (`screener=automated`, non-empty decision): high exclude 3924; high include 2076; low include 900; low exclude 721; total low-confidence automated = 1621.

---

## End notes

- Branch for all citations: `revision-3` @ `dce6da7` unless a historical CHANGELOG line is quoted.
- AMBIGUOUS items from Phase 0 that remain explained above: 7628 vs 7621; Google Scholar 602 vs 597 (resolved).
