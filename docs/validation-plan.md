# Screening validation plan, revision 3
Registered on 2026-11-02, before any sample was drawn.

## Purpose

Execute the author-verification duties in `protocol/screening-procedure.md` section 6 that were not run (see `docs/protocol-deviations.md` entries 7 and 8): the stratified random audit of confident exclusions, and author review of every `confidence: low` decision.

## Populations

Counts computed from `screening/screening-log.csv` (column filters cited). Joined fields for stratification come from `search/candidate-pool.csv` on `id = candidate_id`.

| Pop | Definition | Treatment | n |
|---|---|---|---:|
| A | `screener=automated`, `decision=exclude`, `confidence=low` | Reviewed in full | 721 |
| B | `screener` in `{automated, llm_assisted}`, `decision=exclude`, `confidence=high` | Section 6 audit sample of 300 | 3996 |
| C | `screener=automated`, `decision=include`, `confidence=low` | Reviewed in full (Part 2) | 900 |
| D1 | `screener=automated`, `decision=include`, `confidence=high` | 100 random blinding rows for Part 1 | 2076 (draw 100) |
| D2 | Population B rows not drawn into the B sample | 100 random blinding rows for Part 2 | 3696 after B draw (draw 100) |

Population A is required (entry 8). Population B is the section 6 audit (entry 7). Population C completes the section 6 requirement that every confidence: low decision be author-reviewed, for inclusions; it is scheduled as Part 2. D1 and D2 exist only for blinding.

## Sampling for B

Stratified by:

1. **Year band:** `year` in {2024, 2025, 2026}, else `missing`.
2. **`canonical_source`:** from `search/candidate-pool.csv`.
3. **Query block:** first token of `parent_query` before the first underscore, from `search/candidate-pool.csv`; empty or missing `parent_query` is coded `missing`.

Allocation: proportional to stratum size within B, largest-remainder (Hamilton) rounding, total exactly **300**. Within each stratum, rows are shuffled with `random.Random(20261102)` and the first `n_stratum` are taken. If a provisional quota exceeds stratum size, the quota is capped at the stratum size and remaining seats are redistributed by largest fractional parts among strata with remaining capacity.

**Deterministic order:** before every random step, candidate rows are sorted by `record_id` and strata are processed in sorted stratum-key order, so the draw is identical across machines.

**Seed:** `20261102` for every random step (B within-stratum draws, D1, D2, Part 1 shuffle, Part 2 shuffle).

## Blind files and keys

| Part | Contents | Blind file | Key file | Key hash file |
|---|---|---|---|---|
| Part 1 | A + B sample + D1, shuffled | `validation/part1_blind.csv` | `validation/part1_key.csv` | `validation/part1_key.sha256` |
| Part 2 | C + D2, shuffled | `validation/part2_blind.csv` | `validation/part2_key.csv` | `validation/part2_key.sha256` |

Each blind file shows only: `sample_id`, `title`, `abstract`, `year`, `venue`, plus blank columns `decision`, `reason_code`, `note` for the author. Classifier decisions, populations, and confidence go only in the key file for that part (`sample_id`, `record_id`, `population`, `stratum`, `classifier_decision`, `classifier_confidence`, `screener`).

The SHA-256 of each key file is committed before screening. The key files themselves are committed only after the author's decisions for that part are committed.

## Reference standard

The author's own decision applying `protocol/inclusion-exclusion.md` at commit 839f425, with one reason code per exclusion (I1-I5 or E1-E6 as listed in `validation/criteria-sheet.md`), applied at Stage 1 scope as stated in validation/criteria-sheet.md, matching the criteria the classifier applied. No AI tool is used for these decisions.

## Outcomes

Per population: author vs classifier agreement.

- **B:** disagreement rate with a Wilson 95% interval, compared against the **5%** threshold fixed in section 6. A disagreement is a record the classifier excluded that the author includes. The 5% threshold is applied to the point estimate of the disagreement rate, as worded in section 6; the Wilson interval is reported alongside.
- **A and C:** counts and percentages overturned, with Wilson intervals.
- Every disagreement listed.

If the B disagreement rate exceeds 5%, section 6 requires re-screening the affected stratum; that requirement and its status will be reported.

## Completion rule

Part 1 must be completed in full before any result is computed. Part 2 is an extension; if not completed, results are reported for the completed rows with the number completed, and the remainder are reported as not reviewed.

All outcomes are reported in the manuscript regardless of result.

## Draw script

`scripts/draw_validation_sample.py` implements this plan. It is not run until this plan file is committed.
