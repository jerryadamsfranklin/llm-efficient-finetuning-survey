# Stage 2 full-text assessment, inserted set of 13
Recorded on 2026-11-01.
Criterion 2 values were pre-filled from the arXiv full text of each paper and confirmed by the author against his own full-text reading. Criterion 3 venues are copied from screening/reviews/shortlist-13-verification.md.

| candidate_id | short_name | criterion_3_venue | criterion_2_largest_model_evaluated | criterion_2_location | role | note | author_confirmed |
|---|---|---|---|---|---|---|---|
| C-65a13e7929 | HydraLoRA | NeurIPS 2024 | LLaMA2-13B | Table 3 (Section 4.2) | INCLUDED |  | YES |
| C-c5f653cbd2 | LISA | NeurIPS 2024 | LLaMA-2-70B | Table 5 (Section 4.4) | INCLUDED |  | YES |
| C-a80f3cac0d | LoRA-GA | NeurIPS 2024 | Llama 2-7B | Section 4.2 | INCLUDED |  | YES |
| C-93f716cbf0 | PiSSA | NeurIPS 2024 | LLaMA-3-70B | Figure 6 (Section 5.4) | INCLUDED |  | YES |
| C-392a797fca | IR-QLoRA | ICML 2024 | LLaMA-65B | Tables 1 and 2 | INCLUDED |  | YES |
| C-3f09ccfe68 | EfficientQAT | ACL 2025 | Llama-2-70B and Llama-3-70B | Tables 1 and 2 | INCLUDED |  | YES |
| C-15aa63fdab | SpinQuant | ICLR 2025 | Llama-2-70B and Llama-3-70B (quantization only; no fine-tuning) | Table 1 (Section 4.2) | BACKGROUND | Post-training quantization for inference; fails exclusion 2 (inference-only optimization). Cited for the PTQ vs QAT contrast. | YES |
| C-57aa0c8ae7 | GaLore | ICML 2024 | LLaMA-7B (fine-tuning) | Appendix D.3 Table 9; Appendix D.4 Table 10 | INCLUDED | LLaMA 7B in Section 5.3 is pre-training, not fine-tuning. | YES |
| C-05c157f898 | AdaRankGrad | ICLR 2025 | RoBERTa-base and Geneformer only (fine-tuning); LLaMA up to 7B in pre-training only | Section 4.1, Table 2 | BACKGROUND | No fine-tuning evaluation on a model of 1B parameters or more; fails criterion 2 for fine-tuning. Cited descriptively in Section 6.4. | YES |
| C-bc98faf889 | OpenFedLLM | KDD 2024 | Llama2-7B | Sections 4.1 to 4.6 | INCLUDED |  | YES |
| C-aaedc3bee8 | FFA-LoRA | ICLR 2024 | LLaMA-7B | Section 5.3; Appendix A.3 | INCLUDED |  | YES |
| C-a1f9ae845d | FlexLoRA | NeurIPS 2024 | LLaMA-3 8B | Section 4.6; Appendix I Table 12 | INCLUDED | Main experiments use DataJuicer 1.3B. | YES |
| C-64babd74d3 | LoRA survey (Mao et al.) | Front. Comput. Sci. 2025 | None (survey) | n/a | BACKGROUND | Survey with no empirical evaluation; fails criterion 2. Cited to position this survey. | YES |

role values: INCLUDED (meets inclusion criteria on full text) or BACKGROUND (cited for context; reason stated in note).
Counts: INCLUDED 10, BACKGROUND 3.
