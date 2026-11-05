# Activation-term check against a published measurement

Source: Dbouk et al. (2026), arXiv:2606.19528v1, Table 3, row 'BF16 + FP32 (naive)', Llama-3.2 3B.
Setting: LoRA r=16 on query and value, batch 1, FP32 activations, one forward and backward pass, NVIDIA A100 80GB (Section 3, Profiling).

Compare the per-1024-token increase in measured peak memory with the modeled increase (activation term without the attention-score term, as with FlashAttention, plus logits). Fixed costs such as weights cancel in the difference.

| Interval (tokens) | Measured increase (GB) | Measured per 1,024 tokens (GB) | Modeled per 1,024 tokens (GB) | Difference |
|---|---:|---:|---:|---:|
| 512 to 1024 | 3.55 | 7.10 | 7.04 | -0.8% |
| 1024 to 2048 | 7.10 | 7.10 | 7.04 | -0.8% |
| 2048 to 4096 | 14.21 | 7.10 | 7.04 | -0.9% |
| 4096 to 8192 | 28.42 | 7.11 | 7.04 | -0.9% |

Modeled per-token terms: activations 5.85 MB, logits 1.03 MB.
No constant was adjusted to produce this agreement.
