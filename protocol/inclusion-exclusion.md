# Inclusion and Exclusion Criteria

**Protocol version:** 1.0  
**Status:** Locked for Phase 1 — committed before search execution  
**Coverage window:** 2019-01-01 through 2026-06-30  
**Related:** [`search-protocol.md`](search-protocol.md), [`extraction-schema.md`](extraction-schema.md)

These criteria are applied consistently to every candidate. Exclusion reasons in `screening/screening-log.csv` must cite the numbered criterion below.

---

## Inclusion criteria

A paper is **INCLUDED** if **all** of the following hold:

1. **Relevance to efficient fine-tuning / adaptation.** It proposes, evaluates, or surveys methods for reducing computational requirements during LLM fine-tuning or adaptation.
2. **Scale or role.** It reports empirical evaluation on transformer models of at least **1 billion parameters**, **OR** it is a survey/review of such methods, **OR** it establishes a foundational technique later applied at that scale.
3. **Publication / adoption bar.** It is published in a peer-reviewed venue, **OR** it is an arXiv preprint with demonstrable community adoption, operationalized as **any one** of:
   - **≥ 50 citations** (citation count from Semantic Scholar or equivalent authoritative source at screening time), **OR**
   - an **official implementation** in a major library (e.g. Hugging Face PEFT / Transformers), **OR**
   - **acceptance recorded on OpenReview** (or equivalent archival conference/journal acceptance record)
4. **Language.** Written in English.
5. **Date.** Published (or first posted, for preprints) between **2019-01-01** and **2026-06-30**.

### Note on criterion 3

The community-adoption threshold is stated explicitly so it can be applied consistently and defended in the manuscript. An arbitrary-looking cutoff invites challenge; a stated, applied-consistently cutoff does not. Citation counts are recorded at the time of screening and noted in the screening log when criterion 3 is the deciding factor.

---

## Exclusion criteria

A paper is **EXCLUDED** if **any** of the following hold:

1. It focuses **exclusively on pre-training efficiency** with no fine-tuning or adaptation component.
2. It focuses **exclusively on inference-time optimization** with no training / fine-tuning component.
3. It addresses **non-transformer architectures only**.
4. It is a **duplicate** or a **superseded preprint** version of an included paper.
5. It reports **only qualitative claims** with no extractable efficiency or quality measures.
6. It is a **blog post, vendor documentation, or non-archival white paper** (these may be consulted as background but are **not** counted in the corpus).

---

## Screening stage mapping

| Stage | Criteria applied | Notes |
|---|---|---|
| Stage 1 — Title/abstract | Inclusion 1, 4, 5; Exclusion 1–3, 6 when obvious from title/abstract | Fast pass |
| Stage 2 — Full text | Inclusion 2, 3; Exclusion 4, 5; confirm Stage 1 | Methods and results required |
| Stage 3 — Synthesis | Category / subcategory; supersession and coverage duplicates | Assign taxonomy labels |

For every exclusion, record which numbered criterion triggered it.

---

## Scope control for this revision search

- Do **not** treat the goal as an exhaustive re-screen of all 2019–2023 literature.
- The existing manuscript corpus (~42 references) is the foundation; the new search **confirms** that coverage and **adds** genuinely new work, weighted toward **January 2024 – June 2026** and reviewer-identified gaps (recent PEFT surveys, quantization degradation, federated LLM work, 2026 currency).
