# Extraction Schema

**Status:** Placeholder — Phase 1 content to be finalized and committed before searching.

For each included paper, extract:

| Field | Type | Notes |
|---|---|---|
| `key` | string | BibTeX key |
| `authors` | string | full author list |
| `year` | int | |
| `title` | string | |
| `venue` | string | published venue, or "arXiv preprint" |
| `doi_or_arxiv` | string | |
| `category` | enum | PEFT / quantization / memory / distributed / survey / foundational |
| `subcategory` | string | e.g. additive, reparameterized, PTQ, QAT |
| `mechanism` | text | one-sentence theoretical mechanism |
| `model_scales` | string | parameter counts evaluated |
| `model_families` | string | LLaMA, GPT, BERT, etc. |
| `memory_reduction` | string | as reported, with units and baseline |
| `accuracy_retention` | string | as reported, with benchmark named |
| `benchmarks_used` | string | GLUE, MMLU, MATH, etc. |
| `compute_overhead` | string | as reported |
| `implementation_url` | string | if available |
| `notes` | text | caveats, conflicting results, limitations |

`benchmarks_used` is required for addressing benchmark-heterogeneity criticism with evidence.
