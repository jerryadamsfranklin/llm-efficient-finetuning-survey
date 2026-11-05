# Memory model results

Model: LLaMA-2-7B, 6.74B parameters (6.48B in block linear layers). All constants: analysis/memory_assumptions.json. LoRA and QLoRA activations are upper bounds.

## Workload W1: batch 4, sequence 2048

| config | method | rank | targets | DQ | Flash | ckpt | trainable % | model states GB | activations GB | logits GB | total GB |
|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|
| W1-01 | full_ft |  | all (full) |  | no | no | 100.0 | 107.8 | 122.41 | 2.1 | 232.3 |
| W1-02 | full_ft |  | all (full) |  | yes | no | 100.0 | 107.8 | 36.51 | 2.1 | 146.4 |
| W1-03 | full_ft |  | all (full) |  | yes | yes | 100.0 | 107.8 | 3.29 | 2.1 | 113.2 |
| W1-04 | lora | 8 | qv |  | no | no | 0.062 | 13.5 | 122.41 | 2.1 | 138.0 |
| W1-05 | lora | 8 | qv |  | no | yes | 0.062 | 13.5 | 5.97 | 2.1 | 21.6 |
| W1-06 | lora | 8 | qv |  | yes | no | 0.062 | 13.5 | 36.51 | 2.1 | 52.1 |
| W1-07 | lora | 8 | qv |  | yes | yes | 0.062 | 13.5 | 3.29 | 2.1 | 18.9 |
| W1-08 | lora | 16 | qv |  | no | no | 0.124 | 13.6 | 122.41 | 2.1 | 138.1 |
| W1-09 | lora | 16 | qv |  | no | yes | 0.124 | 13.6 | 5.97 | 2.1 | 21.7 |
| W1-10 | lora | 16 | qv |  | yes | no | 0.124 | 13.6 | 36.51 | 2.1 | 52.2 |
| W1-11 | lora | 16 | qv |  | yes | yes | 0.124 | 13.6 | 3.29 | 2.1 | 19.0 |
| W1-12 | lora | 32 | qv |  | no | no | 0.249 | 13.7 | 122.41 | 2.1 | 138.2 |
| W1-13 | lora | 32 | qv |  | no | yes | 0.249 | 13.7 | 5.97 | 2.1 | 21.8 |
| W1-14 | lora | 32 | qv |  | yes | no | 0.249 | 13.7 | 36.51 | 2.1 | 52.3 |
| W1-15 | lora | 32 | qv |  | yes | yes | 0.249 | 13.7 | 3.29 | 2.1 | 19.1 |
| W1-16 | lora | 64 | qv |  | no | no | 0.498 | 14.0 | 122.41 | 2.1 | 138.5 |
| W1-17 | lora | 64 | qv |  | no | yes | 0.498 | 14.0 | 5.97 | 2.1 | 22.1 |
| W1-18 | lora | 64 | qv |  | yes | no | 0.498 | 14.0 | 36.51 | 2.1 | 52.6 |
| W1-19 | lora | 64 | qv |  | yes | yes | 0.498 | 14.0 | 3.29 | 2.1 | 19.4 |
| W1-20 | lora | 128 | qv |  | no | no | 0.996 | 14.6 | 122.41 | 2.1 | 139.1 |
| W1-21 | lora | 128 | qv |  | no | yes | 0.996 | 14.6 | 5.97 | 2.1 | 22.6 |
| W1-22 | lora | 128 | qv |  | yes | no | 0.996 | 14.6 | 36.51 | 2.1 | 53.2 |
| W1-23 | lora | 128 | qv |  | yes | yes | 0.996 | 14.6 | 3.29 | 2.1 | 19.9 |
| W1-24 | lora | 32 | all |  | yes | yes | 1.187 | 14.8 | 3.29 | 2.1 | 20.1 |
| W1-25 | qlora | 16 | qv | no | no | no | 0.124 | 4.3 | 122.41 | 2.1 | 128.8 |
| W1-26 | qlora | 16 | qv | no | no | yes | 0.124 | 4.3 | 5.97 | 2.1 | 12.4 |
| W1-27 | qlora | 16 | qv | no | yes | no | 0.124 | 4.3 | 36.51 | 2.1 | 42.9 |
| W1-28 | qlora | 16 | qv | no | yes | yes | 0.124 | 4.3 | 3.29 | 2.1 | 9.7 |
| W1-29 | qlora | 16 | qv | yes | no | no | 0.124 | 4.0 | 122.41 | 2.1 | 128.5 |
| W1-30 | qlora | 16 | qv | yes | no | yes | 0.124 | 4.0 | 5.97 | 2.1 | 12.1 |
| W1-31 | qlora | 16 | qv | yes | yes | no | 0.124 | 4.0 | 36.51 | 2.1 | 42.6 |
| W1-32 | qlora | 16 | qv | yes | yes | yes | 0.124 | 4.0 | 3.29 | 2.1 | 9.4 |
| W1-33 | qlora | 32 | qv | no | no | no | 0.249 | 4.4 | 122.41 | 2.1 | 128.9 |
| W1-34 | qlora | 32 | qv | no | no | yes | 0.249 | 4.4 | 5.97 | 2.1 | 12.5 |
| W1-35 | qlora | 32 | qv | no | yes | no | 0.249 | 4.4 | 36.51 | 2.1 | 43.0 |
| W1-36 | qlora | 32 | qv | no | yes | yes | 0.249 | 4.4 | 3.29 | 2.1 | 9.8 |
| W1-37 | qlora | 32 | qv | yes | no | no | 0.249 | 4.1 | 122.41 | 2.1 | 128.6 |
| W1-38 | qlora | 32 | qv | yes | no | yes | 0.249 | 4.1 | 5.97 | 2.1 | 12.2 |
| W1-39 | qlora | 32 | qv | yes | yes | no | 0.249 | 4.1 | 36.51 | 2.1 | 42.7 |
| W1-40 | qlora | 32 | qv | yes | yes | yes | 0.249 | 4.1 | 3.29 | 2.1 | 9.5 |
| W1-41 | qlora | 64 | qv | no | no | no | 0.498 | 4.7 | 122.41 | 2.1 | 129.2 |
| W1-42 | qlora | 64 | qv | no | no | yes | 0.498 | 4.7 | 5.97 | 2.1 | 12.8 |
| W1-43 | qlora | 64 | qv | no | yes | no | 0.498 | 4.7 | 36.51 | 2.1 | 43.3 |
| W1-44 | qlora | 64 | qv | no | yes | yes | 0.498 | 4.7 | 3.29 | 2.1 | 10.1 |
| W1-45 | qlora | 64 | qv | yes | no | no | 0.498 | 4.4 | 122.41 | 2.1 | 128.9 |
| W1-46 | qlora | 64 | qv | yes | no | yes | 0.498 | 4.4 | 5.97 | 2.1 | 12.5 |
| W1-47 | qlora | 64 | qv | yes | yes | no | 0.498 | 4.4 | 36.51 | 2.1 | 43.0 |
| W1-48 | qlora | 64 | qv | yes | yes | yes | 0.498 | 4.4 | 3.29 | 2.1 | 9.8 |
| W1-49 | qlora | 64 | all | yes | yes | yes | 2.373 | 6.4 | 3.29 | 2.1 | 11.8 |

## Workload W2: batch 1, sequence 512

| config | method | rank | targets | DQ | Flash | ckpt | trainable % | model states GB | activations GB | logits GB | total GB |
|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|
| W2-01 | full_ft |  | all (full) |  | no | no | 100.0 | 107.8 | 3.62 | 0.13 | 111.6 |
| W2-02 | full_ft |  | all (full) |  | yes | no | 100.0 | 107.8 | 2.28 | 0.13 | 110.2 |
| W2-03 | full_ft |  | all (full) |  | yes | yes | 100.0 | 107.8 | 0.21 | 0.13 | 108.2 |
| W2-04 | lora | 8 | qv |  | no | no | 0.062 | 13.5 | 3.62 | 0.13 | 17.3 |
| W2-05 | lora | 8 | qv |  | no | yes | 0.062 | 13.5 | 0.25 | 0.13 | 13.9 |
| W2-06 | lora | 8 | qv |  | yes | no | 0.062 | 13.5 | 2.28 | 0.13 | 16.0 |
| W2-07 | lora | 8 | qv |  | yes | yes | 0.062 | 13.5 | 0.21 | 0.13 | 13.9 |
| W2-08 | lora | 16 | qv |  | no | no | 0.124 | 13.6 | 3.62 | 0.13 | 17.4 |
| W2-09 | lora | 16 | qv |  | no | yes | 0.124 | 13.6 | 0.25 | 0.13 | 14.0 |
| W2-10 | lora | 16 | qv |  | yes | no | 0.124 | 13.6 | 2.28 | 0.13 | 16.0 |
| W2-11 | lora | 16 | qv |  | yes | yes | 0.124 | 13.6 | 0.21 | 0.13 | 13.9 |
| W2-12 | lora | 32 | qv |  | no | no | 0.249 | 13.7 | 3.62 | 0.13 | 17.5 |
| W2-13 | lora | 32 | qv |  | no | yes | 0.249 | 13.7 | 0.25 | 0.13 | 14.1 |
| W2-14 | lora | 32 | qv |  | yes | no | 0.249 | 13.7 | 2.28 | 0.13 | 16.2 |
| W2-15 | lora | 32 | qv |  | yes | yes | 0.249 | 13.7 | 0.21 | 0.13 | 14.1 |
| W2-16 | lora | 64 | qv |  | no | no | 0.498 | 14.0 | 3.62 | 0.13 | 17.8 |
| W2-17 | lora | 64 | qv |  | no | yes | 0.498 | 14.0 | 0.25 | 0.13 | 14.4 |
| W2-18 | lora | 64 | qv |  | yes | no | 0.498 | 14.0 | 2.28 | 0.13 | 16.4 |
| W2-19 | lora | 64 | qv |  | yes | yes | 0.498 | 14.0 | 0.21 | 0.13 | 14.4 |
| W2-20 | lora | 128 | qv |  | no | no | 0.996 | 14.6 | 3.62 | 0.13 | 18.3 |
| W2-21 | lora | 128 | qv |  | no | yes | 0.996 | 14.6 | 0.25 | 0.13 | 14.9 |
| W2-22 | lora | 128 | qv |  | yes | no | 0.996 | 14.6 | 2.28 | 0.13 | 17.0 |
| W2-23 | lora | 128 | qv |  | yes | yes | 0.996 | 14.6 | 0.21 | 0.13 | 14.9 |
| W2-24 | lora | 32 | all |  | yes | yes | 1.187 | 14.8 | 0.21 | 0.13 | 15.1 |
| W2-25 | qlora | 16 | qv | no | no | no | 0.124 | 4.3 | 3.62 | 0.13 | 8.1 |
| W2-26 | qlora | 16 | qv | no | no | yes | 0.124 | 4.3 | 0.25 | 0.13 | 4.7 |
| W2-27 | qlora | 16 | qv | no | yes | no | 0.124 | 4.3 | 2.28 | 0.13 | 6.7 |
| W2-28 | qlora | 16 | qv | no | yes | yes | 0.124 | 4.3 | 0.21 | 0.13 | 4.6 |
| W2-29 | qlora | 16 | qv | yes | no | no | 0.124 | 4.0 | 3.62 | 0.13 | 7.8 |
| W2-30 | qlora | 16 | qv | yes | no | yes | 0.124 | 4.0 | 0.25 | 0.13 | 4.4 |
| W2-31 | qlora | 16 | qv | yes | yes | no | 0.124 | 4.0 | 2.28 | 0.13 | 6.4 |
| W2-32 | qlora | 16 | qv | yes | yes | yes | 0.124 | 4.0 | 0.21 | 0.13 | 4.3 |
| W2-33 | qlora | 32 | qv | no | no | no | 0.249 | 4.4 | 3.62 | 0.13 | 8.2 |
| W2-34 | qlora | 32 | qv | no | no | yes | 0.249 | 4.4 | 0.25 | 0.13 | 4.8 |
| W2-35 | qlora | 32 | qv | no | yes | no | 0.249 | 4.4 | 2.28 | 0.13 | 6.8 |
| W2-36 | qlora | 32 | qv | no | yes | yes | 0.249 | 4.4 | 0.21 | 0.13 | 4.8 |
| W2-37 | qlora | 32 | qv | yes | no | no | 0.249 | 4.1 | 3.62 | 0.13 | 7.9 |
| W2-38 | qlora | 32 | qv | yes | no | yes | 0.249 | 4.1 | 0.25 | 0.13 | 4.5 |
| W2-39 | qlora | 32 | qv | yes | yes | no | 0.249 | 4.1 | 2.28 | 0.13 | 6.5 |
| W2-40 | qlora | 32 | qv | yes | yes | yes | 0.249 | 4.1 | 0.21 | 0.13 | 4.5 |
| W2-41 | qlora | 64 | qv | no | no | no | 0.498 | 4.7 | 3.62 | 0.13 | 8.5 |
| W2-42 | qlora | 64 | qv | no | no | yes | 0.498 | 4.7 | 0.25 | 0.13 | 5.1 |
| W2-43 | qlora | 64 | qv | no | yes | no | 0.498 | 4.7 | 2.28 | 0.13 | 7.1 |
| W2-44 | qlora | 64 | qv | no | yes | yes | 0.498 | 4.7 | 0.21 | 0.13 | 5.0 |
| W2-45 | qlora | 64 | qv | yes | no | no | 0.498 | 4.4 | 3.62 | 0.13 | 8.2 |
| W2-46 | qlora | 64 | qv | yes | no | yes | 0.498 | 4.4 | 0.25 | 0.13 | 4.8 |
| W2-47 | qlora | 64 | qv | yes | yes | no | 0.498 | 4.4 | 2.28 | 0.13 | 6.8 |
| W2-48 | qlora | 64 | qv | yes | yes | yes | 0.498 | 4.4 | 0.21 | 0.13 | 4.7 |
| W2-49 | qlora | 64 | all | yes | yes | yes | 2.373 | 6.4 | 0.21 | 0.13 | 6.8 |

## Cross-check against a reported measurement

| Source | Reported | Setting | Model row | Modeled |
|---|---:|---|---|---:|
| Dettmers et al. (2023), Appendix G, Figure 6 | 6.9 GB | QLoRA, LLaMA 7B, LoRA on all linear layers (App B.2), batch 1, sequence 512, gradient checkpointing | W2-49 (QLoRA r64, all linear, double quantization, checkpointing) | 6.8 GB |

No constant was adjusted to produce agreement with any reported measurement.
