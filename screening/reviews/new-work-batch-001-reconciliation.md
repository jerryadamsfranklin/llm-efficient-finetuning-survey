# Batch 001 reconciliation (updated) — zero remaining contradictions

**Status:** calibration gate closed. Encoded rule and author verdicts agree on every reviewed record.
Batch 002 may start under this rule. Block size 375.

Encoded research-question test (`inclusion-exclusion.md`, v1.3 clarification, not change):

> A paper is in scope if its research question is about the fine-tuning-efficiency method itself
> (its performance, applicability, or improvement), including comparative evaluations of the
> method. It is out of scope if its research question is about a task or system and the
> efficiency method is only the tool used to build it.
>
> Vision / speech / graph / audio / multimodal / general-ML work fails **criterion 2** unless the
> method is general and demonstrated on an LLM (language-model efficiency surveys, including
> SLM surveys, remain eligible). Domain applications on LLMs fail **inclusion 1**.

---

## Final batch 001 outcomes

| | Cursor original | After author calibration |
|---|---:|---:|
| Include | 54 | **34** |
| Exclude | 96 | **116** |
| Author overturns (include → exclude) | — | **20** |

Of the 20 overturns: 13 original disagreements + 7 further reclassifications (A.19, A.1, A.2, A.39, A.5, A.15, A.25). All 20 are in the log as `screener: author` with the numbered criterion.

Kept as include under the research-question test: **A.4** (SLM survey), **A.28** (PEFT eval on program repair), **A.29** (PEFT eval on code smell), **A.35** (customization techniques for LLMs). Unchanged; still `llm_assisted` / `stage_2_pending`.

Held record 3 stays held. Held record 8 remains exclusion 6.

---

## Agreement rates

| Comparison | n | agree | disagree | rate |
|---|---:|---:|---:|---:|
| Original packet vs Cursor (before the 7 catches) | 100 | 87 | 13 | 87% |
| Original packet vs the *fully encoded* rule | 100 | 80 | 20 | **80%** |
| Author verdicts *after resolutions* vs encoded rule | 100 | 100 | 0 | **100%** |
| Cursor original vs encoded rule, full batch of 150 | 150 | 130 | 20 | 87% |
| False excludes (Cursor or author) vs encoded rule | — | — | 0 | — |

All 20 disagreements with the encoded rule were false includes (domain-boundary or machinery-application). Zero false excludes. The 7 extra reclassifications are the calibration gate doing its job, not a screening failure.

**Remaining contradictions between author verdicts and encoded rule: none.**

---

## The 20 author excludes (all match the rule)

### Original 13 disagreements

| # | id | short title | Criterion |
|---|---|---|---|
| A.6 | `C-eabd183905` | Federated PEFT of SAM | 2 vision |
| A.7 | `C-1f69bb5c6f` | Med-VTAB / ViT | 2 vision |
| A.9 | `C-73feb84f4d` | Graph prompt tuning | 2 graph |
| A.11 | `C-90fc511d61` | PEFT Japanese dialect ASR | 2 speech |
| A.12 | `C-27a90d06c5` | PEFT multilingual ASR | 2 speech |
| A.13 | `C-8081e358c7` | LoRA for diffusion T2I | 2 vision |
| A.17 | `C-fc2b996b81` | HVAC adapter transfer | 2 non-language |
| A.18 | `C-8f2ee64cc1` | Audio Transformer adapters | 2 audio |
| A.20 | `C-68c85fdb46` | APrompt4EM entity matching | 1 domain app |
| A.21 | `C-437e4fc9a8` | ASR domain prompt tuning | 2 speech |
| A.22 | `C-1a0ec2ecf9` | ATFLRec LoRA recommender | 1 domain app |
| A.23 | `C-0f3972344a` | AV-PEA audio-visual | 2 multimodal |
| A.24 | `C-84a30630d1` | Audio summarization via LoRA | 1 domain app |

### Further 7 (contradictions caught by reconciliation)

| # | id | short title | Criterion | Why |
|---|---|---|---|---|
| A.19 | `C-67fa715de7` | ADAPT Vision Transformers | 2 | Same class as Med-VTAB |
| A.1 | `C-3fef54df25` | Financial text classification | 1 | Finance classifier; method not the contribution |
| A.2 | `C-203fc69734` | LLMs on ABSA | 1 | Task is the subject; PEFT is a baseline |
| A.39 | `C-f267e4b7cc` | RAG system with QLoRA | 1 | Research question is the RAG system |
| A.5 | `C-14495abbe7` | TEE security + LoRA | 1 | Contribution is a security architecture |
| A.15 | `C-6d4690a604` | General-ML compression survey | 2 | Not LLM-specific |
| A.25 | `C-d45c0544b4` | Federated ZO optimization | 2 | Not demonstrated on an LLM |

### Gray zone resolved — stay include (no contradiction)

| # | id | short title | Test application |
|---|---|---|---|
| A.4 | `C-bed03b2915` | SLM efficiency survey | Survey route of criterion 2; language-model efficiency literature |
| A.28 | `C-bd76aae186` | PEFT eval on program repair | Research question is how PEFT performs; task is the testbed |
| A.29 | `C-568fced344` | PEFT eval on code smell | Same: method evaluation |
| A.35 | `C-7975fb9289` | Text classification in the age of LLMs | Subject is the customization techniques (LoRA, prefix, quantization) |

---

## Log integrity

- 20 rows: `screener=author`, prior machine decision in `screener_original`
- Exclusion criterion present on every exclude
- Stage 2 pending for batch 001: 34 includes
- `C-3187c706f6` remains `hold` / `stage_1_held`
- `C-34a4a73f19` remains exclude / Exclusion 6
