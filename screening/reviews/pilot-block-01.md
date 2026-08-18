# Pilot block 1 — author verification packet

Calibration check on the pilot batch. Mark each row `agree` / `disagree` / `unsure`.
Bulk Stage 1 screening is paused until this returns.

- LLM-assisted decisions in this block: **18** (16 include, 2 exclude)
- Band: all **unknown_year** (records with no retrievable year; see caveat at foot)

---

## Includes (16) — these advance to Stage 2 if you agree

### 1. A Theoretical Analysis of Migration Strength Selection in SmoothQuant
- `C-4f1f38f8b0` | source: google_scholar | confidence: **low**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: SmoothQuant analysis; may be inference-only PTQ (exclusion 2). Uncertain from title alone. Date unverified - criterion 5 pending at Stage 2.
- **verdict:** 

### 2. Acceleration of Training for Mixture-of-Experts Models Under Memory Offloading
- `C-4082772124` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: MoE training under memory offloading - training-time memory optimisation (block B3). Date unverified - criterion 5 pending at Stage 2.
- **verdict:** 

### 3. AttentionletIs All You Need!
- `C-3187c706f6` | source: google_scholar | confidence: **low**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Title 'AttentionletIs All You Need!' is garbled and no other metadata exists; possibly a corrupt record. Cannot judge on merits - author review required.
- **verdict:** 

### 4. Comparative Analysis of Post-Quantization Techniques for Small Language Models
- `C-eb0ebb204a` | source: google_scholar | confidence: **low**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Post-training quantization comparison; 'small language models' may fail the 1B-parameter bar (criterion 2) at Stage 2. Date unverified.
- **verdict:** 

### 5. Efficient Adaptation of Pre-trained Models: A Survey of PEFT for Language, Vision, and Multimodal Learning
- `C-79bd4583b8` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: PEFT survey across language, vision, multimodal - squarely in scope as a survey (criterion 2). Date unverified - criterion 5 pending.
- **verdict:** 

### 6. Efficient Fine-Tuning of Quantized LLMs via Three-Stage Optimization
- `C-e6480b533a` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Fine-tuning of quantized LLMs - core subject of the survey. Date unverified - criterion 5 pending.
- **verdict:** 

### 7. Large Language Model Memory Optimization for Long-Context Cybersecurity Tasks
- `C-05630c4c46` | source: google_scholar | confidence: **low**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: LLM memory optimisation, but long-context framing may indicate inference rather than training. Date unverified.
- **verdict:** 

### 8. Large Language Models (LLMs): Quantization
- `C-34a4a73f19` | source: google_scholar | confidence: **low**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Generic title suggests a tutorial or book chapter, which would engage exclusion 6. Needs source check. Date unverified.
- **verdict:** 

### 9. NeuroCache: Budget-Constrained Activation Offloading for Low-VRAM Transformer Training
- `C-cb45b784e5` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Activation offloading for low-VRAM transformer training - training-time memory (block B3). Date unverified.
- **verdict:** 

### 10. ProTrain: Efficient LLM Training via Automatic Memory Management
- `C-ef908e7d28` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Automatic memory management for LLM training (block B3). Date unverified - criterion 5 pending.
- **verdict:** 

### 11. Quantized Visual Geometry Grounded Transformer
- `C-fc3d26ca9b` | source: google_scholar | confidence: **low**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Quantization of a vision geometry transformer; relevance to LLM fine-tuning unclear from title. Date unverified.
- **verdict:** 

### 12. SPARQ: Outlier-free SpeechLM with Fast Adaptation and Robust Quantization
- `C-7a1ca34a27` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Fast adaptation plus quantization for a speech LM - adaptation efficiency in scope. Date unverified.
- **verdict:** 

### 13. THE GEOMETRY OF LLM QUANTIZATION
- `C-3e0d9bf5ed` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: LLM quantization (block B2). Date unverified - criterion 5 pending at Stage 2.
- **verdict:** 

### 14. Towards Quantization-Adversarial Reparameterizations
- `C-66949a65ca` | source: google_scholar | confidence: **low**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Quantization reparameterization; model scale and domain not determinable from title. Date unverified.
- **verdict:** 

### 15. Towards Understanding the Dynamics of Low-Rank Adaptation
- `C-a713fd1c5b` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Theory of low-rank adaptation dynamics - core PEFT subject (block B1). Date unverified.
- **verdict:** 

### 16. ULoRA: Universal Low-Rank Adaptation of Diverse Deep Learning Architectures
- `C-870364d9f9` | source: google_scholar | confidence: **high**
- year: _none_ | venue: _none_ | citations: 0 | abstract: no
- screener note: Universal low-rank adaptation across architectures (block B1). Date unverified - criterion 5 pending.
- **verdict:** 

---

## Excludes (2) — LLM-assisted, for audit

1. **Efficient Attention and Beyond: A Survey of Advances in Optimizing Transformer Inference** (`C-7f8add152d`, conf high)
   - reason: `Exclusion 2` — Survey of transformer inference optimisation; no training or fine-tuning component.
   - **verdict:** 

2. **Towards Lossless Memory-efficient Training of Spiking Neural Networks via Gradient Checkpointin** (`C-671c501faf`, conf high)
   - reason: `Exclusion 3` — Spiking neural networks - non-transformer architecture only.
   - **verdict:** 

---

## Caveat on representativeness

Every record in this block comes from the `unknown_year` band: 19 Google Scholar
records with no year, no abstract, and no citation data. They are the hardest and
least typical records in the pool, so agreement here does not by itself calibrate
the 10,920-record main run. A second calibration sample drawn from `new_work` is
proposed before bulk screening.

---

## Author review outcome — 2026-07-31

Confirmed correct: both excludes (inference-only survey under exclusion 2; spiking
neural networks under exclusion 3) and seven includes — records 2, 5, 6, 9, 10, 15
and 16 (MoE offloading, PEFT survey, quantized-LLM fine-tuning, activation
offloading, ProTrain, LoRA dynamics, ULoRA).

Three corrections were directed and have been applied:

| Record | Action taken |
|---|---|
| 3 — AttentionletIs All You Need! | Metadata recovery attempted against Semantic Scholar, Crossref and OpenAlex on three title variants; no match. Now `hold` / `stage_1_held`. |
| 8 — Large Language Models (LLMs): Quantization | Excluded under exclusion 6 per v1.3 book-chapter clarification (De Gruyter chapter neighbours). Author-directed 2026-08-14. |
| 12 — SPARQ (SpeechLM) | Confidence high → low. Domain-boundary record; decision unchanged. |

Record 13 (THE GEOMETRY OF LLM QUANTIZATION) was lowered to low confidence for
consistency: like record 1, its title cannot separate training-time quantization
from inference-only PTQ. Record 11 (Quantized Visual Geometry Transformer) was
already recorded low and needed no change.

The general rule from this review — confidence reports certainty in the decision,
not enthusiasm for the record — is now written into `protocol/screening-procedure.md`
§6.2, and the handling of unidentifiable records into §6.3.

**Still without a verdict:** records 1, 4, 7, 13 and 14, all low-confidence includes.
They remain `stage_2_pending` and will be resolved at Stage 2 on full text unless you
want them decided here.

