# Extraction Schema

**Protocol version:** 1.0  
**Status:** Locked for Phase 1 — committed before search execution  
**Output file:** `data/included-papers.csv`  
**Related:** [`search-protocol.md`](search-protocol.md), [`inclusion-exclusion.md`](inclusion-exclusion.md)

For each **included** paper, populate every field below. Empty cells are allowed only when the source truly does not report the quantity; use `notes` to explain missing critical fields.

---

## Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `key` | string | yes | BibTeX citation key |
| `authors` | string | yes | Full author list in published order; resolve via Crossref / arXiv API — do not hand-type |
| `year` | int | yes | Publication year (published venue preferred over preprint year when upgraded) |
| `title` | string | yes | Exact title |
| `venue` | string | yes | Published venue name, or `arXiv preprint` if unpublished |
| `doi_or_arxiv` | string | yes | DOI and/or arXiv ID |
| `category` | enum | yes | One of: `PEFT`, `quantization`, `memory`, `distributed`, `survey`, `foundational` |
| `subcategory` | string | yes | e.g. additive, reparameterized, selective, PTQ, QAT, attention, offloading, federated-LoRA |
| `mechanism` | text | yes | One-sentence theoretical / algorithmic mechanism |
| `model_scales` | string | preferred | Parameter counts evaluated (e.g. `7B, 13B, 70B`) |
| `model_families` | string | preferred | e.g. LLaMA, GPT, BERT, T5, Mistral |
| `memory_reduction` | string | preferred | As reported, with units and baseline |
| `accuracy_retention` | string | preferred | As reported, with benchmark named |
| `benchmarks_used` | string | **yes** | Named benchmarks (GLUE, MMLU, MATH, etc.). Required for documenting benchmark heterogeneity |
| `compute_overhead` | string | preferred | As reported (training time, FLOPs, communication, etc.) |
| `implementation_url` | string | if available | Official or reference implementation |
| `notes` | text | as needed | Caveats, conflicting results, limitations, preprint→published upgrades |

---

## Category enum definitions

| Value | Use when |
|---|---|
| `PEFT` | Parameter-efficient fine-tuning methods (adapters, LoRA-family, prompt/prefix, BitFit, etc.) |
| `quantization` | PTQ, QAT, low-bit training/fine-tuning (GPTQ, AWQ, QLoRA, etc.) |
| `memory` | Activation/optimizer/attention memory reductions (checkpointing, FlashAttention, ZeRO, offloading) |
| `distributed` | Distributed or federated fine-tuning / communication-efficient adaptation |
| `survey` | Surveys or systematic overviews of the above |
| `foundational` | Foundational technique papers later applied at LLM scale (may predate widespread 1B+ evals) |

---

## Verification requirements (Phase 4)

Before treating a row as final:

1. Confirm author list, year, venue, and DOI/arXiv against Crossref, arXiv API, or publisher page.
2. Prefer the **published** venue over “arXiv preprint” when acceptance/publication is verified.
3. Log citation corrections in `docs/reference-corrections.md` (created in Phase 4).

---

## CSV header (canonical)

```text
key,authors,year,title,venue,doi_or_arxiv,category,subcategory,mechanism,model_scales,model_families,memory_reduction,accuracy_retention,benchmarks_used,compute_overhead,implementation_url,notes
```

This header matches `data/included-papers.csv`.
