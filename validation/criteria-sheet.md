# Validation criteria sheet

Copied from `protocol/inclusion-exclusion.md` for author decisions under `docs/validation-plan.md`.

Decision rule: INCLUDE only if every inclusion criterion is met and no exclusion applies; otherwise EXCLUDE with the first failing code.
Stage 1 scope (protocol/screening-procedure.md, Stage 1 criteria applied): apply I1, I4, I5, E1, E2, E3, and E6 where obvious from title and abstract, and the criterion 2 LLM boundary when the non-language domain is clear. Do NOT apply I2 scale (1 billion parameters), I3 (publication or adoption bar), E4, or E5; these are Stage 2 criteria. When a record is ambiguous on the Stage 1 criteria, decide INCLUDE (bias to inclusion). Source: protocol/screening-procedure.md lines 88-90 (criteria applied) and lines 103-106 (bias toward inclusion).

---

## Inclusion criteria

A paper is **INCLUDED** if **all** of the following hold:

1. (I1) **Relevance to efficient fine-tuning / adaptation.** It proposes, evaluates, or surveys methods for reducing computational requirements during LLM fine-tuning or adaptation.
2. (I2) **Scale or role.** It reports empirical evaluation on transformer models of at least **1 billion parameters**, **OR** it is a survey/review of such methods, **OR** it establishes a foundational technique later applied at that scale.
3. (I3) **Publication / adoption bar.** It is published in a peer-reviewed venue, **OR** it is an arXiv preprint with demonstrable community adoption, operationalized as **any one** of:
   - **≥ 50 citations** (citation count from Semantic Scholar or equivalent authoritative source at screening time), **OR**
   - an **official implementation** in a major library (e.g. Hugging Face PEFT / Transformers), **OR**
   - **acceptance recorded on OpenReview** (or equivalent archival conference/journal acceptance record)
4. (I4) **Language.** Written in English.
5. (I5) **Date.** Published (or first posted, for preprints) between **2019-01-01** and **2026-06-30**.

### Note on criterion 1 (clarified under v1.3 — clarification, not change)

A paper is in scope only if its **contribution is the fine-tuning-efficiency method itself** — a
new method, a comparative evaluation of methods, or a survey of methods. A domain task that
**applies an existing method** (LoRA, QLoRA, adapters, prompt/prefix tuning, quantization) as
machinery to build a system or to improve a downstream application is **excluded under inclusion
criterion 1**, even when the model is an LLM.

**Distinguishing test (research question):** a paper is in scope if its research question is about
the fine-tuning-efficiency method itself — how it performs, when it works, how to improve it —
including comparative evaluations of the method on a downstream task used as a testbed. It is out
of scope if its research question is about a task or system and the efficiency method is only the
tool used to build it.

### Note on criterion 2 (clarified under v1.3 — clarification, not change)

A paper is in scope only if **(a) the model under study is a large language model** (or it is a
survey of efficiency methods for language models, including small LMs treated as the adjacent
efficiency literature) **and** **(b) the research-question test in the criterion 1 note holds**.
Vision, speech, graph, audio, and multimodal models are **excluded under criterion 2** unless the
method is **general and demonstrated on an LLM**. PEFT, quantization, or memory-optimization
techniques applied as machinery for a non-language domain task fail here when the model is not an
LLM. A general-ML survey or method not demonstrated on an LLM also fails criterion 2.

At Stage 1 this boundary is applied when the non-language domain is clear from the title or
abstract (SAM, ViT, ASR, graph transformers, audio transformers, diffusion). When the domain is
ambiguous, the record may advance under bias-to-inclusion for Stage 2 to confirm.

### Note on criterion 5 (clarified under v1.3 — clarification, not change)

A work that appeared first as a preprint and was later published in a peer-reviewed venue is dated by its **publication date**. The parenthetical "first posted" governs only items that remain unpublished at screening time. A 2018 preprint published at a 2019 venue is therefore in window.

This is the reading the criterion already carried; it is written out because it decides a small number of records at the window boundary — BERT (posted 2018, NAACL 2019) and Experience Replay for Continual Learning among them — and an unstated interpretation is weaker than a recorded one. The alternative reading, dating every work by its earliest public appearance, would exclude those records and is not the convention this review follows.

### Note on criterion 3

The community-adoption threshold is stated explicitly so it can be applied consistently and defended in the manuscript. An arbitrary-looking cutoff invites challenge; a stated, applied-consistently cutoff does not. Citation counts are recorded at the time of screening and noted in the screening log when criterion 3 is the deciding factor.

---

## Exclusion criteria

A paper is **EXCLUDED** if **any** of the following hold:

1. (E1) It focuses **exclusively on pre-training efficiency** with no fine-tuning or adaptation component.
2. (E2) It focuses **exclusively on inference-time optimization** with no training / fine-tuning component.
3. (E3) It addresses **non-transformer architectures only**.
4. (E4) It is a **duplicate** or a **superseded preprint** version of an included paper.
5. (E5) It reports **only qualitative claims** with no extractable efficiency or quality measures.
6. (E6) It is a **blog post, vendor documentation, or non-archival white paper** (these may be consulted as background but are **not** counted in the corpus).

### Note on criterion 6 (clarified under v1.3 — clarification, not change)

**Textbook chapters, tutorial chapters, and pedagogical book chapters** are excluded as non-archival
secondary material under exclusion 6. Peer-reviewed archival papers and conference/journal
publications are retained. Peer-reviewed papers in edited scholarly proceedings remain eligible;
textbook and tutorial chapters do not.

At Stage 1, this applies when the record type, venue, or title indicates book-chapter form (e.g.
"Chapter N: …" in a publisher book series). When form is uncertain, the record may be held or
advanced at low confidence for author review.
