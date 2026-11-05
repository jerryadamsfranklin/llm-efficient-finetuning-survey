# Adjudication and re-screen plan, revision 3
Written on 2026-11-03 and given to the author before any adjudication or re-screen decision was made. Committed on 2026-11-04, after those decisions, so the commit history does not independently verify that ordering (docs/protocol-deviations.md, entry 12).

## Trigger

The pre-registered validation (`docs/validation-plan.md`, results in `validation/results.md`) found that the author would include 68 of 300 sampled confident machine exclusions (population B): a disagreement rate of 22.7% (Wilson 95% CI 18.3% to 27.7%), above the 5% threshold fixed in `protocol/screening-procedure.md` section 6. Section 6 states that above this threshold "the affected stratum is re-screened rather than patched." Disagreements occur in every year band and source, so the affected stratum is all of population B.

The primary outcome (22.7%) is final and is reported unchanged in the manuscript. Nothing in this plan alters it.

## Step 1: adjudication (secondary analysis)

**Population:** every exclusion-side disagreement in the validation: records the classifier excluded and the author included, in populations A (low-confidence exclusions), B (audit sample), and D2 (blinding rows drawn from B). 286 records: A 200, B 68, D2 18.

**Procedure:** unblinded. For each record the author sees the title, abstract, year, venue, the classifier's exclusion reason, and his own original decision, and records a final decision, a reason code for exclusions, and a one-phrase rationale, applying the Stage 1 criteria in `validation/criteria-sheet.md`. The final decision is made on the written criteria, not by deferring to either earlier call.

**Purpose:** to separate classifier error from inconsistency in the reference standard, and to calibrate the author before Step 2.

**Reported:** as a secondary analysis added after the primary result was known. For B: the number of the 68 disagreements the author confirms as INCLUDE, and the resulting adjudicated rate out of 300 with a Wilson 95% interval. The same for A and D2. Include-side disagreements (populations C and D1: classifier included, author excluded) are not adjudicated; they have no effect on recall and are reported as measured.

## Step 2: re-screen of the remaining confident exclusions

**Population:** population B records not reviewed in the validation: 3,996 minus the 300 audit records and the 100 D2 records = 3,596.

**Procedure:** the author decides INCLUDE or EXCLUDE, with a reason code for every exclusion, applying `validation/criteria-sheet.md` at Stage 1 scope with bias to inclusion only where a record is genuinely ambiguous on the written criteria. Not blinded: every record in this population was excluded by the classifier, and this is disclosed. No AI tool is used for any decision.

**Order:** Step 1 is completed and committed before Step 2 begins. Step 2 decisions are committed after each sitting, so progress is dated in the history.

**Completion rule:** results are reported for the rows completed, with the number completed. Any rows not reviewed by submission are reported as not reviewed, and the section 6 requirement is reported as partially met.

## Effect on the screening record

After both steps, the final Stage 1 status of each reviewed record is the author's decision (adjudicated decision where adjudicated). The screening log is updated in a separate, later commit by a script that sets `screener` to `author`, preserves the machine decision in `screener_original`, and records the reason code. No record's original machine decision is deleted.

## Tooling

`scripts/build_rescreen_workbooks.py` builds the working workbook (`validation/rescreen_workbook.xlsx`, gitignored) deterministically from committed files. Decisions are copied from the workbook to committed CSVs by a script that changes no other column.

## Reporting

All outcomes are reported in the manuscript regardless of result.
