# Second-pass verification plan, revision 3
Written on 2026-11-04 and given to the author before any second-pass decision was made. Committed on 2026-11-04, after the second pass was completed, so the commit history does not independently verify that ordering (docs/protocol-deviations.md, entry 12).

## Why

The first-pass adjudication and re-screen (`docs/rescreen-plan.md`; decisions in `validation/adjudication_first_pass.csv` and `validation/rescreen_first_pass.csv`) were reviewed for consistency with the written criteria before use. The review was performed with an AI assistant (Claude, Anthropic). It changed no decision. It found that many first-pass INCLUDE decisions did not meet the written Stage 1 criteria, and that one identical rationale was recorded on all 244 adjudicated INCLUDE decisions. The first pass is kept unchanged in the record and is reported.

## Population

Every first-pass INCLUDE: 244 from adjudication and 1,093 from the re-screen, 1,337 records. First-pass EXCLUDE decisions are not re-examined.

## Procedure

For each record the author answers three questions from the title and abstract, applying `validation/criteria-sheet.md`:

1. Q1: Is the model studied a language model, or is the paper a survey of language-model efficiency methods? (criterion 2 boundary; N gives I2)
2. Q2: Does the paper propose, compare, or survey a way to reduce compute, memory, or trainable parameters when fine-tuning or adapting that model? (criterion 1; N gives I1)
3. Q3: Is it only about inference, or only about pre-training? (exclusions 2 and 1; gives E2 or E1)

INCLUDE only if Q1 is Y, Q2 is Y, and Q3 is No. Otherwise the first failing code applies. Every row carries a row-specific rationale naming the method and the model. Where the title and abstract do not allow an answer, the author answers Y, Y, No and records "ambiguous" with the reason (bias to inclusion only for genuine ambiguity).

Post-training quantization with no fine-tuning component is answered Q3 = "Inference only" (exclusion 2), consistent with the classification of SpinQuant in `screening/reviews/stage2-fulltext-13.md`.

All answers are the author's. No AI tool is used for any answer. Decision and code are derived mechanically from the three answers by `scripts/apply_second_pass.py`, which recomputes them independently of the workbook formulas.

## Recording

Answers are copied to `validation/second_pass_decisions.csv` and committed after each sitting. Rows not yet reviewed are recorded as NOT_REVIEWED.

## Reporting

The pre-registered primary result (population B disagreement 22.7%, `validation/results.md`) is unchanged. Reported in addition: first-pass adjudication and re-screen counts; second-pass counts of first-pass INCLUDE decisions confirmed and reversed, by code; and the final Stage 1 status of every reviewed record, defined as the second-pass decision where one exists and otherwise the first-pass decision. Any rows not reviewed by submission are reported with their number. All outcomes are reported regardless of result.
