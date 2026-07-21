# Search Log

Human-readable record of every query run.

**Protocol version:** 1.1 (amendment locked; v1.1 re-runs not yet executed)  
**Coverage window:** 2019-01-01 to 2026-06-30  
**Status:** Protocol v1.1 committed. v1.0 automated results preserved under `search/raw_v1.0/`. Awaiting owner confirmation before date-sliced arXiv / S2 keyword re-runs and venue checks.

## Manual sources (owner-filled)

Fill these after running each query in the browser. Stopping rule: first 50 by relevance.

### Google Scholar — B1_peft — query 1
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** TBD
- **Filters:** 2019-2026, English
- **Results reported by interface:** TBD
- **Records screened (first 50 by relevance):** TBD
- **Candidates carried forward:** TBD
- **Notes:**

### Google Scholar — B1_peft — query 2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** TBD
- **Filters:** 2019-2026, English
- **Results reported by interface:** TBD
- **Records screened (first 50 by relevance):** TBD
- **Candidates carried forward:** TBD
- **Notes:**

### Google Scholar — B1_peft — query 3
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** TBD
- **Filters:** 2019-2026, English
- **Results reported by interface:** TBD
- **Records screened (first 50 by relevance):** TBD
- **Candidates carried forward:** TBD
- **Notes:**

### Google Scholar — B1_peft — query 4
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** TBD
- **Filters:** 2019-2026, English
- **Results reported by interface:** TBD
- **Records screened (first 50 by relevance):** TBD
- **Candidates carried forward:** TBD
- **Notes:**

### Google Scholar — B1_peft — query 5
- **Query:** "PEFT" AND survey
- **Date run:** TBD
- **Filters:** 2019-2026, English
- **Results reported by interface:** TBD
- **Records screened (first 50 by relevance):** TBD
- **Candidates carried forward:** TBD
- **Notes:**

### IEEE Xplore — (blocks B1–B4)
- **Queries:** same strings as `search/queries.yaml`
- **Date run:** TBD
- **Filters:** 2019–2026
- **Results / screened / carried forward:** TBD per query
- **Notes:** Log each query as a separate `### IEEE Xplore — <block> — query N` section when run.

### ACM Digital Library — (blocks B1–B4)
- **Queries:** same strings as `search/queries.yaml`
- **Date run:** TBD
- **Filters:** 2019–2026
- **Results / screened / carried forward:** TBD per query
- **Notes:** Log each query as a separate `### ACM DL — <block> — query N` section when run.

### Hugging Face documentation (reference source, not discovery)
- **Pages consulted:** TBD
- **Date consulted:** TBD
- **Notes:**

## Automated runs

### arxiv — B1_peft — query 1
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T20:13:25Z
- **Results returned:** 200
- **Notes:** API totalReported=654; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B1_peft — query 2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T20:13:33Z
- **Results returned:** 200
- **Notes:** API totalReported=1292; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B1_peft — query 3
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T20:13:42Z
- **Results returned:** 200
- **Notes:** API totalReported=572; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B1_peft — query 4
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T20:13:50Z
- **Results returned:** 200
- **Notes:** API totalReported=860; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B1_peft — query 5
- **Query:** "PEFT" AND survey
- **Date run:** 2026-07-21T20:13:54Z
- **Results returned:** 17
- **Notes:** API totalReported=17; in_window=17

### arxiv — B2_quantization — query 1
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T20:14:02Z
- **Results returned:** 200
- **Notes:** API totalReported=303; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B2_quantization — query 2
- **Query:** (GPTQ OR AWQ OR SmoothQuant OR QLoRA) AND quantization
- **Date run:** 2026-07-21T20:14:10Z
- **Results returned:** 196
- **Notes:** API totalReported=196; in_window=196

### arxiv — B2_quantization — query 3
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T20:14:18Z
- **Results returned:** 200
- **Notes:** API totalReported=259; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B2_quantization — query 4
- **Query:** "quantization-aware training" AND transformer
- **Date run:** 2026-07-21T20:14:22Z
- **Results returned:** 55
- **Notes:** API totalReported=55; in_window=55

### arxiv — B2_quantization — query 5
- **Query:** "low-bit" AND "large language model" AND survey
- **Date run:** 2026-07-21T20:14:25Z
- **Results returned:** 2
- **Notes:** API totalReported=2; in_window=2

### arxiv — B3_memory — query 1
- **Query:** "gradient checkpointing" AND training AND memory
- **Date run:** 2026-07-21T20:14:29Z
- **Results returned:** 15
- **Notes:** API totalReported=15; in_window=15

### arxiv — B3_memory — query 2
- **Query:** "FlashAttention" OR "memory-efficient attention"
- **Date run:** 2026-07-21T20:14:37Z
- **Results returned:** 196
- **Notes:** API totalReported=196; in_window=196

### arxiv — B3_memory — query 3
- **Query:** "ZeRO" OR "DeepSpeed" OR "offloading" AND "model training"
- **Date run:** 2026-07-21T20:14:45Z
- **Results returned:** 200
- **Notes:** API totalReported=17852; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B3_memory — query 4
- **Query:** "memory optimization" AND "large language model" AND training
- **Date run:** 2026-07-21T20:14:48Z
- **Results returned:** 16
- **Notes:** API totalReported=16; in_window=16

### arxiv — B4_federated — query 1
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T20:14:57Z
- **Results returned:** 200
- **Notes:** API totalReported=285; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B4_federated — query 2
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T20:15:05Z
- **Results returned:** 200
- **Notes:** API totalReported=252; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B4_federated — query 3
- **Query:** "distributed training" AND "language model" AND communication
- **Date run:** 2026-07-21T20:15:09Z
- **Results returned:** 78
- **Notes:** API totalReported=78; in_window=78

### arxiv — B4_federated — query 4
- **Query:** "federated fine-tuning" AND heterogeneity
- **Date run:** 2026-07-21T20:15:12Z
- **Results returned:** 70
- **Notes:** API totalReported=70; in_window=70

### semanticscholar — B1_peft — query 1
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T19:37:21Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### semanticscholar — B1_peft — query 2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T19:37:30Z
- **Results returned:** 1
- **Notes:** API totalReported=1

### semanticscholar — B1_peft — query 3
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T19:37:31Z
- **Results returned:** 97
- **Notes:** API totalReported=97

### semanticscholar — B1_peft — query 4
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T19:40:36Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### semanticscholar — B1_peft — query 5
- **Query:** "PEFT" AND survey
- **Date run:** 2026-07-21T20:16:27Z
- **Results returned:** 200
- **Notes:** API totalReported=1888; HIT_CAP=200 — consider narrowing this query

### semanticscholar — B2_quantization — query 1
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T19:46:45Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### openreview — B1_peft — query 1
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T19:47:31Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B1_peft — query 2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T19:47:39Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B1_peft — query 3
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T19:47:47Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B1_peft — query 4
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T19:47:52Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B1_peft — query 5
- **Query:** "PEFT" AND survey
- **Date run:** 2026-07-21T19:47:58Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B2_quantization — query 1
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T19:48:39Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B2_quantization — query 2
- **Query:** (GPTQ OR AWQ OR SmoothQuant OR QLoRA) AND quantization
- **Date run:** 2026-07-21T19:48:45Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### semanticscholar — B2_quantization — query 2
- **Query:** (GPTQ OR AWQ OR SmoothQuant OR QLoRA) AND quantization
- **Date run:** 2026-07-21T20:46:03Z
- **Results returned:** 0
- **Notes:** API totalReported=0

### openreview — B2_quantization — query 3
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T19:48:53Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B2_quantization — query 4
- **Query:** "quantization-aware training" AND transformer
- **Date run:** 2026-07-21T19:49:00Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B2_quantization — query 5
- **Query:** "low-bit" AND "large language model" AND survey
- **Date run:** 2026-07-21T19:49:10Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B3_memory — query 1
- **Query:** "gradient checkpointing" AND training AND memory
- **Date run:** 2026-07-21T19:49:49Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B3_memory — query 2
- **Query:** "FlashAttention" OR "memory-efficient attention"
- **Date run:** 2026-07-21T19:49:56Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B3_memory — query 3
- **Query:** "ZeRO" OR "DeepSpeed" OR "offloading" AND "model training"
- **Date run:** 2026-07-21T19:50:05Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B3_memory — query 4
- **Query:** "memory optimization" AND "large language model" AND training
- **Date run:** 2026-07-21T19:50:15Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B4_federated — query 1
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T19:50:25Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B4_federated — query 2
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T19:51:03Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B4_federated — query 3
- **Query:** "distributed training" AND "language model" AND communication
- **Date run:** 2026-07-21T19:51:12Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### openreview — B4_federated — query 4
- **Query:** "federated fine-tuning" AND heterogeneity
- **Date run:** 2026-07-21T19:51:19Z
- **Results returned:** 200
- **Notes:** HIT_CAP=200 — consider narrowing this query

### semanticscholar — B2_quantization — query 3
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T19:51:55Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### semanticscholar — B2_quantization — query 4
- **Query:** "quantization-aware training" AND transformer
- **Date run:** 2026-07-21T19:56:06Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### semanticscholar — B2_quantization — query 5
- **Query:** "low-bit" AND "large language model" AND survey
- **Date run:** 2026-07-21T19:58:11Z
- **Results returned:** 94
- **Notes:** API totalReported=94

### semanticscholar — B3_memory — query 1
- **Query:** "gradient checkpointing" AND training AND memory
- **Date run:** 2026-07-21T20:01:26Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### semanticscholar — B3_memory — query 2
- **Query:** "FlashAttention" OR "memory-efficient attention"
- **Date run:** 2026-07-21T20:04:31Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### semanticscholar — B3_memory — query 3
- **Query:** "ZeRO" OR "DeepSpeed" OR "offloading" AND "model training"
- **Date run:** 2026-07-21T20:25:13Z
- **Results returned:** 0
- **Notes:** API totalReported=0

### semanticscholar — B3_memory — query 4
- **Query:** "memory optimization" AND "large language model" AND training
- **Date run:** 2026-07-21T20:08:27Z
- **Results returned:** 0
- **Notes:** Request failed: Semantic Scholar rate limit persisted after retries

### semanticscholar — B4_federated — query 1
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T20:30:03Z
- **Results returned:** 100
- **Notes:** API totalReported=61533; stopped early after repeated rate limits / errors

### semanticscholar — B4_federated — query 2
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T20:34:17Z
- **Results returned:** 100
- **Notes:** API totalReported=209; stopped early after repeated rate limits / errors

### semanticscholar — B4_federated — query 3
- **Query:** "distributed training" AND "language model" AND communication
- **Date run:** 2026-07-21T20:16:55Z
- **Results returned:** 200
- **Notes:** API totalReported=765; HIT_CAP=200 — consider narrowing this query

### semanticscholar — B4_federated — query 4
- **Query:** "federated fine-tuning" AND heterogeneity
- **Date run:** 2026-07-21T20:38:37Z
- **Results returned:** 100
- **Notes:** API totalReported=355; stopped early after repeated rate limits / errors
