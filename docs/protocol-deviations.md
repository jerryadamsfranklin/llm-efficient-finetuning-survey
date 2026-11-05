# Protocol deviations, revision 3
Recorded on 2026-10-24. This file supplements the protocol as committed through b80037a; it does not edit it.

Numbers in "What was done" are copied from `docs/record-ledger.md` (branch `revision-3` @ `dce6da7`). Reason and Effect fields are placeholders for author fill-in.

---

## 1. Automated new-work Stage 1 pass instead of human-verified blocks

**What the protocol specified**

`protocol/screening-procedure.md` lines 168-174 (verification cadence):

> Verification runs **per block of 375 records** in the new-work band (~2.5 batches at size 150), roughly **29 rounds** for the full new-work band. [...] Each block emits a packet to `screening/reviews/` containing every include, every low-confidence decision, and a sample of confident excludes; screening of the next block does not begin until the packet returns.

`protocol/screening-procedure.md` lines 150-153 (author-verification table):

> **Every `include`** is author-verified before the record advances to Stage 2 | 100%

Same file lines 210-218 (departure already noted in-protocol):

> The remaining 7,628 new-work records were screened in a **single automated pass** (`screener: automated`) rather than in 375-record human-verified blocks. [...] Author verification for this pass is the ranked shortlist of 30 includes [...] not 100% of includes in the band.

**What was done**

- Automated decisions file: 7628 records (`screening/decisions/stage1_new_work_automated.json`).
- Log rows still `screener=automated`: 7621; 7 later author overrides (ledger Reconciliation).
- Human verification of the band limited to the 30-record shortlist (`screening/reviews/reference-shortlist.md`); 13 selected for insertion.
- New-work band final Stage 1 counts: 3011 include / 4787 exclude (`screening-log.csv` `priority_band=new_work`).

**Reason**

Adopted on 2026-08-17 to meet the 2026-08-20 resubmission deadline. Block-wise verification of the new-work band (about 29 rounds) could not be completed in the time remaining. Author verification was concentrated on the ranked shortlist from which references were inserted.

**Effect on the manuscript**

The manuscript methodology states that the new-work band was screened in a single automated pass with author verification limited to a 30-record shortlist. The resulting error risk is measured by the revision 3 audit (entry 7) and the low-confidence review (entry 8).

---

## 2. Classifier agreement measured only on the records used to build the rule

**What the protocol specified**

`protocol/screening-procedure.md` lines 243-244 (disclosure text):

> Title-and-abstract screening of records published from January 2024 onward used a rule-encoded classifier calibrated to an author-resolved 150-record sample; human verification for that band was applied to a citation- and section-weighted shortlist of includes rather than to every include.

`protocol/CHANGELOG.md` (automated-pass entry): states the classifier was calibrated to 150/150 agreement against author-resolved batch 001.

The protocol does not state that agreement must be measured on a held-out sample. The deviation is that the reported 100% figure is in-sample relative to the records used to resolve the rule.

**What was done**

From `screening/reviews/new-work-batch-001-reconciliation.md` agreement table:

- Cursor original vs encoded rule, full batch of 150: 130 agree / 20 disagree (87%).
- Author verdicts after resolutions vs encoded rule, n=100: 100 agree / 0 disagree (100%).
- Calibration sample size: 150 (`stage1_new_work_001.json`).

No separate pre-registered held-out agreement sample is recorded in the repo.

**Reason**

The calibration batch was used both to resolve the encoded rule and to report its agreement; a held-out sample was not planned.

**Effect on the manuscript**

The manuscript no longer reports 150/150 agreement as validation. It is described as in-sample calibration; out-of-sample error is reported from the entry 7 audit.

---

## 3. Confirmation band: 3,142 trigger-meeting records left unscreened

**What the protocol specified**

`protocol/screening-procedure.md` lines 48-50 and section 4 (confirmation band): applying the section 4 triggers selects **3,142** confirmation-band records for screening; records not meeting triggers are recorded as not screened (not as exclusions).

`protocol/search-protocol.md` line 158 (v1.3 procedure summary):

> Screening is fully applied to records from 2024-01-01 onward; 2019-2023 records receive a targeted confirmation pass, and records not examined under that bound are reported as a separate count rather than as exclusions.

**What was done**

From `screening/screening-log.csv`:

- `priority_band=confirmation` and `stage_reached=stage_1_pending`: **3142** (trigger met, empty `decision` - unscreened).
- `stage_reached=stage_1_not_screened`: **4557** (no trigger).
- Metadata excludes in confirmation band: **2**.

The 3,142 trigger-meeting confirmation records have not received Stage 1 include/exclude decisions.

**Reason**

The bound itself (4,557 records meeting no trigger, recorded as not screened) is a design choice in protocol v1.3, committed 2026-07-31. The 3,142 trigger-meeting records were left unscreened when screening effort was concentrated on the new-work band on 2026-08-17 to meet the 2026-08-20 deadline.

**Effect on the manuscript**

The manuscript states that 3,142 trigger-meeting 2019-2023 records were not screened and makes no coverage claim for 2019-2023 beyond the existing reference corpus. Revision 3 reports a known-item coverage check.

---

## 4. Stage 2 full-text assessment not performed on 3,025 Stage 2 pending records

**What the protocol specified**

`protocol/screening-procedure.md` lines 225-229:

> **Stage 2 - full text.** Inclusion criteria 2 (scale/role) and 3 (publication/adoption bar); exclusions 4 and 5. Author-conducted on full text; not delegated.

`protocol/screening-procedure.md` lines 150-153:

> **Every record entering the final corpus** is author-verified on full text | 100%

**What was done**

- `stage_reached=stage_2_pending`: **3025** (`screening-log.csv`).
- `screening/prisma-counts.md`: `Full text assessed (Stage 2) | TBD`.
- No Stage 2 decision files exist. The 13 inserted records were verified against primary sources (`screening/reviews/shortlist-13-verification.md`). AUTHOR-TO-CONFIRM: whether that verification applied Stage 2 criteria 2 and 3 on full text.

**Reason**

Primary-source verification on 2026-08-17 checked authors, venues, and years; scale (criterion 2) was not recorded.

**Effect on the manuscript**

Resolved in revision 3 by screening/reviews/stage2-fulltext-13.md: 10 records INCLUDED, 3 BACKGROUND (SpinQuant, AdaRankGrad, Mao et al.). The manuscript distinguishes background citations from included studies.

---

## 5. Data extraction per extraction-schema.md not performed

**What the protocol specified**

`protocol/extraction-schema.md` lines 5-8:

> **Output file:** `data/included-papers.csv`  
> For each **included** paper, populate every field below.

`protocol/search-protocol.md` line 148: Extraction fields: `extraction-schema.md`.

**What was done**

- `data/included-papers.csv`: Phase 4 placeholder; **0** extraction data rows (status comment + header only).
- `data/table*.csv`: header-only placeholders (`data/README.md`).

**Reason**

Extraction was not performed before the 2026-08-20 resubmission.

**Effect on the manuscript**

The manuscript no longer states that data were extracted per the schema. Quantitative claims are instead traced in a claim-level evidence table added in revision 3.

---

## 6. One held record unresolved before counts are final

**What the protocol specified**

`protocol/screening-procedure.md` lines 204-206:

> Held records are neither included nor excluded and **must be resolved before the PRISMA counts are final**.

Same file line 77 notes held record `C-3187c706f6` remains held (unidentifiable).

**What was done**

- Held rows in `screening/screening-log.csv`: **1** (`id=C-3187c706f6`, `decision=hold`, `stage_reached=stage_1_held`).
- PRISMA counts file still carries Stage 2 / synthesis as TBD; held record not resolved to include or exclude.

**Reason**

The record could not be identified in Semantic Scholar, Crossref, or OpenAlex.

**Effect on the manuscript**

Reported as a separate count of 1 unresolved record; it is neither included nor excluded.

---

## 7. Section 6 audit of confident exclusions not run during screening; executed in revision 3

**What the protocol specified**

`protocol/screening-procedure.md` section 6 table row (line 152):

> **Random audit of confident exclusions** - stratified by year band, source, and query block | >= 250 records

`protocol/screening-procedure.md` lines 155-160:

> The audit sample is drawn with a recorded random seed so it is reproducible. The
> **disagreement rate** (author overturns screener) is computed and reported in
> `screening/prisma-counts.md`. If the audit disagreement rate on exclusions exceeds **5%**, the
> LLM-assisted exclusions are not trusted: the affected stratum is re-screened rather than patched.
> That threshold is set in advance, before the audit is run, so it cannot be adjusted to fit the
> result.

`protocol/search-protocol.md` line 158:

> **v1.3 procedure summary.** Stage 1 is conducted with LLM assistance under author supervision; every inclusion is author-verified and a stratified random sample of at least 250 exclusions is audited, with the disagreement rate reported. Screening is fully applied to records from 2024-01-01 onward; 2019-2023 records receive a targeted confirmation pass, and records not examined under that bound are reported as a separate count rather than as exclusions. A keyword pre-filter was tested and **rejected** - it dropped four references the manuscript itself cites. See `screening-procedure.md` for the full specification and the required disclosure wording.

**What was done**

- Automated exclusions with `confidence=high`: **3924** (`screening/screening-log.csv`; `screener=automated`, `decision=exclude`, `confidence=high`; see Decision confidence in `docs/record-ledger.md`).
- Batch 001 sampled 20 confident excludes (`screening/reviews/new-work-batch-001-calibration.md` section D, "Sampled confident excludes (20 of 70, seed 1)"; summary line also lists "20 sampled confident excludes").
- No audit of at least 250 confident exclusions with a recorded seed was run during screening.
- Revision 3 executes this audit with the design in section 6 unchanged, pre-registered in `docs/validation-plan.md` before any sample is drawn.

**Reason**

Not run. When screening switched to a single automated pass on 2026-08-17, the audit step was not rescheduled. This was an omission, not a decision.

**Effect on the manuscript**

Executed in revision 3 under the section 6 design, pre-registered in docs/validation-plan.md. The result is reported regardless of outcome; if the disagreement rate exceeds 5%, the section 6 re-screening requirement applies and its status is reported.

---

## 8. Low-confidence decisions not author-reviewed

**What the protocol specified**

`protocol/screening-procedure.md` section 6 table row (line 151):

> **Every `confidence: low` decision** is author-reviewed | 100%

**What was done**

- Automated low-confidence includes: **900** (`screening-log.csv`; `screener=automated`, `decision=include`, `confidence=low`).
- Automated low-confidence excludes: **721** (`screener=automated`, `decision=exclude`, `confidence=low`).
- Automated low-confidence total: **1621**.
- Agreed batch 001 records keep `screener=llm_assisted`, so author review of non-automated low-confidence rows cannot be counted from the `screener` column alone; that subset is UNKNOWN.

**Reason**

Not run, for the same reason as entry 7. Low-confidence review was tied to the block-wise verification packets, which were dropped on 2026-08-17.

**Effect on the manuscript**

Revision 3 performs blind author review of all 721 low-confidence automated exclusions (required) and, as an extension, all 900 low-confidence automated inclusions, pre-registered in docs/validation-plan.md. Results are reported for each stratum, including any stratum left incomplete.

---

## 9. Section 6 audit stratified by query block only where the field was populated

**What the protocol specified**

`protocol/screening-procedure.md` section 6 table row (line 152):

> **Random audit of confident exclusions** - stratified by year band, source, and query block | >= 250 records

**What was done**

The pre-registered plan (`docs/validation-plan.md`, commit 5439a63) took query block from `parent_query` in `search/candidate-pool.csv`. That field is populated only for Google Scholar records: 110 of the 3,996 records in population B; the remaining 3,886 were coded "missing". The 300-record sample is therefore stratified by year and canonical source for all records, and by query block only within Google Scholar (`validation/draw_output.txt`).

**Reason**

The field's coverage was not checked before the plan was registered.

**Effect on the manuscript**

The audit is reported as a stratified random sample by year and source. The draw was kept rather than repeated, because repeating a committed draw would need its own justification; it was independently reproduced with identical key hashes.

---

## 10. Adjudication not committed before the re-screen began
**What the plan specified:** docs/rescreen-plan.md: "Step 1 is completed and committed before Step 2 begins. Step 2 decisions are committed after each sitting."
**What was done:** Adjudication (286 records) and re-screen (3,596 records) were completed in one working session and committed together in a single commit.
**Reason:** The author worked through both steps continuously.
**Effect on the manuscript:** Reported as stated. The first-pass decisions are retained unchanged.

## 11. Second-pass verification of first-pass INCLUDE decisions
**What the plan specified:** docs/rescreen-plan.md did not include a second pass.
**What was done:** A consistency review, performed with an AI assistant (Claude, Anthropic) that changed no decision, found that many first-pass INCLUDE decisions did not meet the written Stage 1 criteria and that one identical rationale was recorded on all 244 adjudicated INCLUDE decisions. The author re-examined all 1,337 first-pass INCLUDE decisions under docs/second-pass-plan.md.
**Reason:** To make the final Stage 1 decisions consistent with the written criteria.
**Effect on the manuscript:** The pre-registered primary result is unchanged. First-pass and second-pass results are both reported.

## 12. Re-screen and second-pass plans committed after the decisions they govern
**What the plan specified:** docs/validation-plan.md established that procedures are committed before the decisions they govern.
**What was done:** docs/rescreen-plan.md (written 2026-11-03) and docs/second-pass-plan.md (written 2026-11-04) were given to the author before the corresponding decisions, but both were committed on 2026-11-04 after those decisions were made.
**Reason:** Commits were not run between steps.
**Effect on the manuscript:** These two procedures are reported as written in advance but not verifiably pre-registered. Only docs/validation-plan.md (commit 5439a63) and the validation draw are reported as pre-registered.
