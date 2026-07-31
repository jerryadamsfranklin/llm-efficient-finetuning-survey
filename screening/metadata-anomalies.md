# Metadata Anomalies Observed During Screening

Records whose retrieved metadata is internally inconsistent or implausible. Logged
here so that screening decisions relying on that metadata are auditable, per the
principle that citation counts used for inclusion criterion 3 must be defensible.

---

## C01695 — OpenAlex record with mismatched title, DOI, and authors

**Observed:** 2026-07-31, during Phase 3 initialisation.

| Field | Recorded value |
|---|---|
| Title | Inline Hardware KV-Cache Compression for Long-Context Transformer Inference: An Architectural Case for a Memory-Path Compression Engine |
| DOI | `10.4230/lipics.itp.2023.19` |
| Authors | Jakubův, Chvalovský, Goertzel, Kaliszyk, Olšák, Piotrowski, Schulz, Suda |
| Venue | DROPS (Schloss Dagstuhl – Leibniz Center for Informatics) |
| `cited_by_count` | 77,038 |

**Problem:** the three identifiers disagree. The DOI resolves to LIPIcs / ITP 2023
paper 19, and the author list is that of the ENIGMA automated-theorem-proving group —
neither is consistent with a hardware KV-cache compression paper. A citation count of
77,038 for a LIPIcs proceedings paper is not plausible.

**Conclusion:** the OpenAlex work record is corrupt; the citation count cannot be
attributed to the titled work.

**Effect on screening:** none on the final corpus. The titled subject matter is
inference-time optimisation with no fine-tuning component, so the record is excluded
at Stage 1 under **exclusion criterion 2** on relevance grounds, independent of the
citation figure. The count was never used to admit it under inclusion criterion 3.

**Generalisation:** OpenAlex `cited_by_count` is not treated as self-validating. Where
criterion 3 is the deciding factor for inclusion, the citation count is confirmed
against a second source (Semantic Scholar) and the figure and its source are recorded
in `screening-log.csv` (`citations`, `citations_source`).

---

## Note on legitimately high-citation off-topic hits

Several very highly cited records are correctly counted but off-topic for this survey
(e.g. *SciPy 1.0* at 38,522; *Explainable AI (XAI)* at 9,253; *PLS-SEM* at 8,659).
These are keyword-match artifacts of broad queries, not metadata errors, and are
excluded at Stage 1 under inclusion criterion 1. They are recorded here only to
pre-empt the impression that a high citation count implies a screening error.
