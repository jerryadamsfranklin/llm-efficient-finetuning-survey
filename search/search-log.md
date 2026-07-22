# Search Log

Human-readable record of every query run.

**Protocol version:** 1.2 (source substitution; v1.1 automated discovery retained)  
**Coverage window:** 2019-01-01 to 2026-06-30  
**Status:** Protocol v1.2 search runs in progress / completed (see entries below).

## Manual sources (owner-filled)

Google Scholar remains manual (no legitimate API). Stopping rule: first 50 by relevance.

**v1.2 note:** IEEE Xplore and ACM DL are no longer manual discovery sources.
IEEE runs via the metadata API (`search/raw/ieee/`); ACM coverage via OpenAlex
(`search/raw/openalex_acm/`). Do not fill the legacy IEEE/ACM placeholders below
unless falling back to manual IEEE because an API key is unavailable.

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

### IEEE Xplore — superseded by v1.2 metadata API
- **Status:** Programmatic under protocol v1.2 (`### ieee — <block> — query N` entries below).
- **Fallback:** If `IEEE_API_KEY` cannot be obtained, restore per-query manual logging here and note the fallback.

### ACM Digital Library — superseded by v1.2 OpenAlex ACM filter
- **Status:** Programmatic under protocol v1.2 (`### openalex_acm — <block> — query N`).
- **Notes:** Do not claim direct ACM DL interface search in the manuscript.

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
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 17
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### arxiv — B2_quantization — query 1
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T20:14:02Z
- **Results returned:** 200
- **Notes:** API totalReported=303; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B2_quantization — query 2
- **Query:** (GPTQ OR AWQ OR SmoothQuant OR QLoRA) AND quantization
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 196
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### arxiv — B2_quantization — query 3
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T20:14:18Z
- **Results returned:** 200
- **Notes:** API totalReported=259; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B2_quantization — query 4
- **Query:** "quantization-aware training" AND transformer
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 55
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### arxiv — B2_quantization — query 5
- **Query:** "low-bit" AND "large language model" AND survey
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 2
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### arxiv — B3_memory — query 1
- **Query:** "gradient checkpointing" AND training AND memory
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 15
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### arxiv — B3_memory — query 2
- **Query:** "FlashAttention" OR "memory-efficient attention"
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 196
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### arxiv — B3_memory — query 3
- **Query:** "ZeRO" OR "DeepSpeed" OR "offloading" AND "model training"
- **Date run:** 2026-07-21T20:14:45Z
- **Results returned:** 200
- **Notes:** API totalReported=17852; in_window=200; HIT_CAP=200 — consider narrowing this query

### arxiv — B3_memory — query 4
- **Query:** "memory optimization" AND "large language model" AND training
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 16
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

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
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 78
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### arxiv — B4_federated — query 4
- **Query:** "federated fine-tuning" AND heterogeneity
- **Date run:** 2026-07-21T21:24:57Z
- **Results returned:** 70
- **Notes:** v1.0-valid (under cap); retained without re-run. Copied to search/raw/arxiv/.

### semanticscholar — B1_peft — query 1
- **Query:** parameter-efficient fine-tuning large language models
- **Date run:** 2026-07-22T05:39:01Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=46565; HIT_CAP=200

### semanticscholar — B1_peft — query 2
- **Query:** low-rank adaptation LoRA language model
- **Date run:** 2026-07-22T05:39:14Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=9931; HIT_CAP=200

### semanticscholar — B1_peft — query 3
- **Query:** adapter modules transformer parameter efficient
- **Date run:** 2026-07-21T21:55:21Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=2358; HIT_CAP=200

### semanticscholar — B1_peft — query 4
- **Query:** prompt tuning prefix tuning soft prompts
- **Date run:** 2026-07-22T05:50:11Z
- **Results returned:** 100
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=15931; stopped early after repeated rate limits / errors

### semanticscholar — B1_peft — query 5
- **Query:** parameter-efficient fine-tuning survey
- **Date run:** 2026-07-22T05:50:45Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=9190; HIT_CAP=200

### semanticscholar — B2_quantization — query 1
- **Query:** quantization large language model fine-tuning
- **Date run:** 2026-07-22T05:50:58Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=68731; HIT_CAP=200

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
- **Query:** post-training quantization LLM GPTQ AWQ
- **Date run:** 2026-07-22T05:51:17Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=483; HIT_CAP=200

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
- **Query:** QLoRA quantized low-rank adaptation
- **Date run:** 2026-07-22T05:51:35Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=432; HIT_CAP=200

### semanticscholar — B2_quantization — query 4
- **Query:** quantization-aware training transformer
- **Date run:** 2026-07-22T05:52:04Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=5822; HIT_CAP=200

### semanticscholar — B2_quantization — query 5
- **Query:** low-bit quantization large language models survey
- **Date run:** 2026-07-22T05:52:33Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=2892; HIT_CAP=200

### semanticscholar — B3_memory — query 1
- **Query:** gradient checkpointing activation memory training
- **Date run:** 2026-07-22T05:52:52Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=508; HIT_CAP=200

### semanticscholar — B3_memory — query 2
- **Query:** FlashAttention memory efficient attention
- **Date run:** 2026-07-22T05:53:11Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=7958; HIT_CAP=200

### semanticscholar — B3_memory — query 3
- **Query:** ZeRO DeepSpeed offloading distributed training memory
- **Date run:** 2026-07-22T05:53:59Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=205; HIT_CAP=200

### semanticscholar — B3_memory — query 4
- **Query:** memory optimization large language model training
- **Date run:** 2026-07-22T05:54:28Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=107084; HIT_CAP=200

### semanticscholar — B4_federated — query 1
- **Query:** federated learning large language models
- **Date run:** 2026-07-22T05:55:23Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=61072; HIT_CAP=200

### semanticscholar — B4_federated — query 2
- **Query:** federated LoRA parameter efficient fine-tuning
- **Date run:** 2026-07-22T05:55:37Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=10866; HIT_CAP=200

### semanticscholar — B4_federated — query 3
- **Query:** communication efficient distributed language model training
- **Date run:** 2026-07-22T05:56:21Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=40738; HIT_CAP=200

### semanticscholar — B4_federated — query 4
- **Query:** federated fine-tuning data heterogeneity non-IID
- **Date run:** 2026-07-22T05:56:39Z
- **Results returned:** 200
- **Notes:** protocol=1.1; s2_keyword_variant (semantic equivalent of boolean query, not identical string); API totalReported=2009; HIT_CAP=200

### arxiv — B1_peft — query 1 — slice 2019
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:18:41Z
- **Results returned:** 0
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=0

### arxiv — B1_peft — query 1 — slice 2020
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:18:44Z
- **Results returned:** 0
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=0

### arxiv — B1_peft — query 1 — slice 2021
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:18:48Z
- **Results returned:** 0
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=0

### arxiv — B1_peft — query 1 — slice 2022
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:18:51Z
- **Results returned:** 3
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=3

### arxiv — B1_peft — query 1 — slice 2023
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:18:55Z
- **Results returned:** 61
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=61

### arxiv — B1_peft — query 1 — slice 2024
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:19:04Z
- **Results returned:** 193
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=193

### arxiv — B1_peft — query 1 — slice 2025
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:19:12Z
- **Results returned:** 200
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=262; HIT_CAP=200; splitting into ['2025-H1', '2025-H2']

### arxiv — B1_peft — query 1 — slice 2026-H1
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:19:20Z
- **Results returned:** 135
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=135

### arxiv — B1_peft — query 1 — slice 2025-H1
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:19:28Z
- **Results returned:** 126
- **Slice:** 2025-H1
- **Notes:** protocol=1.1; slice=2025-H1; API totalReported=126

### arxiv — B1_peft — query 1 — slice 2025-H2
- **Query:** "parameter-efficient fine-tuning" AND "large language model"
- **Date run:** 2026-07-21T21:19:36Z
- **Results returned:** 136
- **Slice:** 2025-H2
- **Notes:** protocol=1.1; slice=2025-H2; API totalReported=136

### arxiv — B1_peft — query 2 — slice 2019
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:31:34Z
- **Results returned:** 0
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=0

### arxiv — B1_peft — query 2 — slice 2020
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:31:38Z
- **Results returned:** 0
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=0

### arxiv — B1_peft — query 2 — slice 2021
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:31:41Z
- **Results returned:** 1
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=1

### arxiv — B1_peft — query 2 — slice 2022
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:31:45Z
- **Results returned:** 3
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=3

### arxiv — B1_peft — query 2 — slice 2023
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:31:49Z
- **Results returned:** 77
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=77

### arxiv — B1_peft — query 2 — slice 2024
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:31:58Z
- **Results returned:** 200
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=333; HIT_CAP=200; splitting into ['2024-H1', '2024-H2']

### arxiv — B1_peft — query 2 — slice 2025
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:32:07Z
- **Results returned:** 200
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=562; HIT_CAP=200; splitting into ['2025-H1', '2025-H2']

### arxiv — B1_peft — query 2 — slice 2026-H1
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:32:16Z
- **Results returned:** 200
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=316; HIT_CAP=200; splitting into ['2026-Q1', '2026-Q2']

### arxiv — B1_peft — query 3 — slice 2019
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:33:47Z
- **Results returned:** 2
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=2

### arxiv — B1_peft — query 3 — slice 2020
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:33:50Z
- **Results returned:** 8
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=8

### arxiv — B1_peft — query 3 — slice 2021
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:33:54Z
- **Results returned:** 10
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=10

### arxiv — B1_peft — query 3 — slice 2022
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:33:57Z
- **Results returned:** 27
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=27

### arxiv — B1_peft — query 3 — slice 2023
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:34:01Z
- **Results returned:** 66
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=66

### arxiv — B1_peft — query 3 — slice 2024
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:34:10Z
- **Results returned:** 123
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=123

### arxiv — B1_peft — query 3 — slice 2025
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:34:18Z
- **Results returned:** 200
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=234; HIT_CAP=200; splitting into ['2025-H1', '2025-H2']

### arxiv — B1_peft — query 3 — slice 2026-H1
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:34:26Z
- **Results returned:** 102
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=102

### arxiv — B1_peft — query 4 — slice 2019
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:34:46Z
- **Results returned:** 0
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=0

### arxiv — B1_peft — query 4 — slice 2020
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:34:49Z
- **Results returned:** 0
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=0

### arxiv — B1_peft — query 4 — slice 2021
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:34:53Z
- **Results returned:** 29
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=29

### arxiv — B1_peft — query 4 — slice 2022
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:01Z
- **Results returned:** 120
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=120

### arxiv — B1_peft — query 4 — slice 2023
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:09Z
- **Results returned:** 200
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=216; HIT_CAP=200; splitting into ['2023-H1', '2023-H2']

### arxiv — B1_peft — query 4 — slice 2024
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:18Z
- **Results returned:** 200
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=234; HIT_CAP=200; splitting into ['2024-H1', '2024-H2']

### arxiv — B1_peft — query 4 — slice 2025
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:26Z
- **Results returned:** 186
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=186

### arxiv — B1_peft — query 4 — slice 2026-H1
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:31Z
- **Results returned:** 75
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=75

### arxiv — B2_quantization — query 1 — slice 2019
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:06Z
- **Results returned:** 0
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=0

### arxiv — B2_quantization — query 1 — slice 2020
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:09Z
- **Results returned:** 0
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=0

### arxiv — B2_quantization — query 1 — slice 2021
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:13Z
- **Results returned:** 0
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=0

### arxiv — B2_quantization — query 1 — slice 2022
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:16Z
- **Results returned:** 1
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=1

### arxiv — B2_quantization — query 1 — slice 2023
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:20Z
- **Results returned:** 29
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=29

### arxiv — B2_quantization — query 1 — slice 2024
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:23Z
- **Results returned:** 93
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=93

### arxiv — B2_quantization — query 1 — slice 2025
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:31Z
- **Results returned:** 116
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=116

### arxiv — B2_quantization — query 1 — slice 2026-H1
- **Query:** "quantization" AND "large language model" AND "fine-tuning"
- **Date run:** 2026-07-21T21:36:35Z
- **Results returned:** 64
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=64

### arxiv — B2_quantization — query 3 — slice 2019
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:36:38Z
- **Results returned:** 0
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=0

### arxiv — B2_quantization — query 3 — slice 2020
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:36:41Z
- **Results returned:** 0
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=0

### arxiv — B2_quantization — query 3 — slice 2021
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:36:45Z
- **Results returned:** 0
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=0

### arxiv — B2_quantization — query 3 — slice 2022
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:36:48Z
- **Results returned:** 1
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=1

### arxiv — B2_quantization — query 3 — slice 2023
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:36:54Z
- **Results returned:** 21
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=21

### arxiv — B2_quantization — query 3 — slice 2024
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:36:57Z
- **Results returned:** 60
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=60

### arxiv — B2_quantization — query 3 — slice 2025
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:37:01Z
- **Results returned:** 96
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=96

### arxiv — B2_quantization — query 3 — slice 2026-H1
- **Query:** "post-training quantization" AND LLM
- **Date run:** 2026-07-21T21:37:05Z
- **Results returned:** 81
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=81

### arxiv — B3_memory — query 3 — slice 2019
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:37:09Z
- **Results returned:** 13
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=13

### arxiv — B3_memory — query 3 — slice 2020
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:37:13Z
- **Results returned:** 26
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=26

### arxiv — B3_memory — query 3 — slice 2021
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:37:17Z
- **Results returned:** 64
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=64

### arxiv — B3_memory — query 3 — slice 2022
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:37:25Z
- **Results returned:** 157
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=157

### arxiv — B3_memory — query 3 — slice 2023
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:37:34Z
- **Results returned:** 200
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=804; HIT_CAP=200; splitting into ['2023-H1', '2023-H2']

### openreview — existing_refs — query 1
- **Query:** venue check (OpenReview + Crossref + arXiv) for manuscript references
- **Date run:** 2026-07-21T21:48:22Z
- **Results returned:** 42
- **Notes:** Wrote search/raw/openreview/existing_references_venue_check.json and docs/reference-corrections.md

### arxiv — B3_memory — query 3 — slice 2024
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:37:43Z
- **Results returned:** 200
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=1345; HIT_CAP=200; splitting into ['2024-H1', '2024-H2']

### arxiv — B3_memory — query 3 — slice 2025
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:37:52Z
- **Results returned:** 200
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=1739; HIT_CAP=200; splitting into ['2025-H1', '2025-H2']

### arxiv — B3_memory — query 3 — slice 2026-H1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:38:02Z
- **Results returned:** 200
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=1154; HIT_CAP=200; splitting into ['2026-Q1', '2026-Q2']

### arxiv — B4_federated — query 1 — slice 2019
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:06Z
- **Results returned:** 0
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=0

### arxiv — B4_federated — query 1 — slice 2020
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:10Z
- **Results returned:** 0
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=0

### arxiv — B4_federated — query 1 — slice 2021
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:13Z
- **Results returned:** 1
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=1

### arxiv — B4_federated — query 1 — slice 2022
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:16Z
- **Results returned:** 1
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=1

### arxiv — B4_federated — query 1 — slice 2023
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:22Z
- **Results returned:** 32
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=32

### arxiv — B4_federated — query 1 — slice 2024
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:26Z
- **Results returned:** 71
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=71

### arxiv — B4_federated — query 1 — slice 2025
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:33Z
- **Results returned:** 119
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=119

### arxiv — B4_federated — query 1 — slice 2026-H1
- **Query:** "federated learning" AND "large language model"
- **Date run:** 2026-07-21T21:41:39Z
- **Results returned:** 61
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=61

### arxiv — B4_federated — query 2 — slice 2019
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:41:42Z
- **Results returned:** 0
- **Slice:** 2019
- **Notes:** protocol=1.1; slice=2019; API totalReported=0

### arxiv — B4_federated — query 2 — slice 2020
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:41:46Z
- **Results returned:** 0
- **Slice:** 2020
- **Notes:** protocol=1.1; slice=2020; API totalReported=0

### arxiv — B4_federated — query 2 — slice 2021
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:41:49Z
- **Results returned:** 0
- **Slice:** 2021
- **Notes:** protocol=1.1; slice=2021; API totalReported=0

### arxiv — B4_federated — query 2 — slice 2022
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:41:53Z
- **Results returned:** 4
- **Slice:** 2022
- **Notes:** protocol=1.1; slice=2022; API totalReported=4

### arxiv — B4_federated — query 2 — slice 2023
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:41:56Z
- **Results returned:** 19
- **Slice:** 2023
- **Notes:** protocol=1.1; slice=2023; API totalReported=19

### arxiv — B4_federated — query 2 — slice 2024
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:42:00Z
- **Results returned:** 65
- **Slice:** 2024
- **Notes:** protocol=1.1; slice=2024; API totalReported=65

### arxiv — B4_federated — query 2 — slice 2025
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:42:07Z
- **Results returned:** 106
- **Slice:** 2025
- **Notes:** protocol=1.1; slice=2025; API totalReported=106

### arxiv — B4_federated — query 2 — slice 2026-H1
- **Query:** "federated" AND (LoRA OR "parameter-efficient")
- **Date run:** 2026-07-21T21:42:11Z
- **Results returned:** 58
- **Slice:** 2026-H1
- **Notes:** protocol=1.1; slice=2026-H1; API totalReported=58

### arxiv — B1_peft — query 2 — slice 2024-H1
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:32:25Z
- **Results returned:** 138
- **Slice:** 2024-H1
- **Notes:** protocol=1.1; slice=2024-H1; API totalReported=138

### arxiv — B1_peft — query 2 — slice 2024-H2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:32:33Z
- **Results returned:** 195
- **Slice:** 2024-H2
- **Notes:** protocol=1.1; slice=2024-H2; API totalReported=195

### arxiv — B1_peft — query 2 — slice 2025-H1
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:32:42Z
- **Results returned:** 200
- **Slice:** 2025-H1
- **Notes:** protocol=1.1; slice=2025-H1; API totalReported=279; HIT_CAP=200; splitting into ['2025-Q1', '2025-Q2']

### arxiv — B1_peft — query 2 — slice 2025-H2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:32:51Z
- **Results returned:** 200
- **Slice:** 2025-H2
- **Notes:** protocol=1.1; slice=2025-H2; API totalReported=283; HIT_CAP=200; splitting into ['2025-Q3', '2025-Q4']

### arxiv — B1_peft — query 2 — slice 2026-Q1
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:33:01Z
- **Results returned:** 144
- **Slice:** 2026-Q1
- **Notes:** protocol=1.1; slice=2026-Q1; API totalReported=144

### arxiv — B1_peft — query 2 — slice 2026-Q2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:33:10Z
- **Results returned:** 172
- **Slice:** 2026-Q2
- **Notes:** protocol=1.1; slice=2026-Q2; API totalReported=172

### arxiv — B1_peft — query 2 — slice 2025-Q1
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:33:18Z
- **Results returned:** 141
- **Slice:** 2025-Q1
- **Notes:** protocol=1.1; slice=2025-Q1; API totalReported=141

### arxiv — B1_peft — query 2 — slice 2025-Q2
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:33:27Z
- **Results returned:** 138
- **Slice:** 2025-Q2
- **Notes:** protocol=1.1; slice=2025-Q2; API totalReported=138

### arxiv — B1_peft — query 2 — slice 2025-Q3
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:33:35Z
- **Results returned:** 151
- **Slice:** 2025-Q3
- **Notes:** protocol=1.1; slice=2025-Q3; API totalReported=151

### arxiv — B1_peft — query 2 — slice 2025-Q4
- **Query:** "low-rank adaptation" AND (LoRA OR AdaLoRA OR DoRA OR VeRA)
- **Date run:** 2026-07-21T21:33:43Z
- **Results returned:** 132
- **Slice:** 2025-Q4
- **Notes:** protocol=1.1; slice=2025-Q4; API totalReported=132

### arxiv — B1_peft — query 3 — slice 2025-H1
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:34:35Z
- **Results returned:** 106
- **Slice:** 2025-H1
- **Notes:** protocol=1.1; slice=2025-H1; API totalReported=106

### arxiv — B1_peft — query 3 — slice 2025-H2
- **Query:** "adapter" AND "transformer" AND "fine-tuning" AND efficient
- **Date run:** 2026-07-21T21:34:42Z
- **Results returned:** 128
- **Slice:** 2025-H2
- **Notes:** protocol=1.1; slice=2025-H2; API totalReported=128

### arxiv — B1_peft — query 4 — slice 2023-H1
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:38Z
- **Results returned:** 108
- **Slice:** 2023-H1
- **Notes:** protocol=1.1; slice=2023-H1; API totalReported=108

### arxiv — B1_peft — query 4 — slice 2023-H2
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:47Z
- **Results returned:** 108
- **Slice:** 2023-H2
- **Notes:** protocol=1.1; slice=2023-H2; API totalReported=108

### arxiv — B1_peft — query 4 — slice 2024-H1
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:35:55Z
- **Results returned:** 122
- **Slice:** 2024-H1
- **Notes:** protocol=1.1; slice=2024-H1; API totalReported=122

### arxiv — B1_peft — query 4 — slice 2024-H2
- **Query:** "prompt tuning" OR "prefix tuning" OR "BitFit"
- **Date run:** 2026-07-21T21:36:02Z
- **Results returned:** 112
- **Slice:** 2024-H2
- **Notes:** protocol=1.1; slice=2024-H2; API totalReported=112

### arxiv — B3_memory — query 3 — slice 2023-H1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:38:11Z
- **Results returned:** 200
- **Slice:** 2023-H1
- **Notes:** protocol=1.1; slice=2023-H1; API totalReported=288; HIT_CAP=200; splitting into ['2023-Q1', '2023-Q2']

### arxiv — B3_memory — query 3 — slice 2023-H2
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:38:20Z
- **Results returned:** 200
- **Slice:** 2023-H2
- **Notes:** protocol=1.1; slice=2023-H2; API totalReported=516; HIT_CAP=200; splitting into ['2023-Q3', '2023-Q4']

### arxiv — B3_memory — query 3 — slice 2024-H1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:38:28Z
- **Results returned:** 200
- **Slice:** 2024-H1
- **Notes:** protocol=1.1; slice=2024-H1; API totalReported=681; HIT_CAP=200; splitting into ['2024-Q1', '2024-Q2']

### arxiv — B3_memory — query 3 — slice 2024-H2
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:38:37Z
- **Results returned:** 200
- **Slice:** 2024-H2
- **Notes:** protocol=1.1; slice=2024-H2; API totalReported=664; HIT_CAP=200; splitting into ['2024-Q3', '2024-Q4']

### arxiv — B3_memory — query 3 — slice 2025-H1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:38:47Z
- **Results returned:** 200
- **Slice:** 2025-H1
- **Notes:** protocol=1.1; slice=2025-H1; API totalReported=844; HIT_CAP=200; splitting into ['2025-Q1', '2025-Q2']

### arxiv — B3_memory — query 3 — slice 2025-H2
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:38:56Z
- **Results returned:** 200
- **Slice:** 2025-H2
- **Notes:** protocol=1.1; slice=2025-H2; API totalReported=894; HIT_CAP=200; splitting into ['2025-Q3', '2025-Q4']

### arxiv — B3_memory — query 3 — slice 2026-Q1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:39:05Z
- **Results returned:** 200
- **Slice:** 2026-Q1
- **Notes:** protocol=1.1; slice=2026-Q1; API totalReported=520; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2026-Q2
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:39:14Z
- **Results returned:** 200
- **Slice:** 2026-Q2
- **Notes:** protocol=1.1; slice=2026-Q2; API totalReported=634; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2023-Q1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:39:19Z
- **Results returned:** 71
- **Slice:** 2023-Q1
- **Notes:** protocol=1.1; slice=2023-Q1; API totalReported=71

### arxiv — B3_memory — query 3 — slice 2023-Q2
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:39:28Z
- **Results returned:** 200
- **Slice:** 2023-Q2
- **Notes:** protocol=1.1; slice=2023-Q2; API totalReported=217; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2023-Q3
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:39:37Z
- **Results returned:** 188
- **Slice:** 2023-Q3
- **Notes:** protocol=1.1; slice=2023-Q3; API totalReported=188

### arxiv — B3_memory — query 3 — slice 2023-Q4
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:39:46Z
- **Results returned:** 200
- **Slice:** 2023-Q4
- **Notes:** protocol=1.1; slice=2023-Q4; API totalReported=328; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2024-Q1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:39:55Z
- **Results returned:** 200
- **Slice:** 2024-Q1
- **Notes:** protocol=1.1; slice=2024-Q1; API totalReported=325; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2024-Q2
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:40:04Z
- **Results returned:** 200
- **Slice:** 2024-Q2
- **Notes:** protocol=1.1; slice=2024-Q2; API totalReported=356; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2024-Q3
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:40:13Z
- **Results returned:** 200
- **Slice:** 2024-Q3
- **Notes:** protocol=1.1; slice=2024-Q3; API totalReported=302; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2024-Q4
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:40:23Z
- **Results returned:** 200
- **Slice:** 2024-Q4
- **Notes:** protocol=1.1; slice=2024-Q4; API totalReported=362; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2025-Q1
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:40:33Z
- **Results returned:** 200
- **Slice:** 2025-Q1
- **Notes:** protocol=1.1; slice=2025-Q1; API totalReported=361; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2025-Q2
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:40:44Z
- **Results returned:** 200
- **Slice:** 2025-Q2
- **Notes:** protocol=1.1; slice=2025-Q2; API totalReported=483; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2025-Q3
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:40:54Z
- **Results returned:** 200
- **Slice:** 2025-Q3
- **Notes:** protocol=1.1; slice=2025-Q3; API totalReported=444; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### arxiv — B3_memory — query 3 — slice 2025-Q4
- **Query:** ("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR "large language model")
- **Date run:** 2026-07-21T21:41:03Z
- **Results returned:** 200
- **Slice:** 2025-Q4
- **Notes:** protocol=1.1; slice=2025-Q4; API totalReported=450; HIT_CAP=200; RESIDUAL_GAP — quarterly slice still at cap; coverage incomplete for this slice (stated stopping rule)

### Residual coverage gap — B3_memory_3

Even after year-level and quarter-level date-slicing, `B3_memory_3`
(`("ZeRO" OR "DeepSpeed" OR "offloading") AND ("model training" OR
"large language model")`) reached the 200-result cap in most quarters
from 2023 through 2026-Q2. This is the finest granularity specified in
Protocol v1.1 section 4.2, and the stop condition has been reached.

**Disposition:** this query is retained as-is rather than narrowed
further. The terms "model training" and "large language model" are too
common in this literature to bound the query without losing intended
recall on ZeRO/DeepSpeed/offloading papers specifically. A residual
coverage gap is acknowledged for this query: only the newest 200
records per capped quarter were retrieved, not the full candidate set.
This is consistent with the stated retrieval-cap stopping rule
(amendment section 5.1) and is disclosed in the manuscript methodology
and in Section 10.4 (Limitations).

### openalex — B1_peft — query 1
- **Query:** parameter-efficient fine-tuning large language models
- **Date run:** 2026-07-22T15:42:34Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=194944; HIT_CAP=50

### openalex — B1_peft — query 2
- **Query:** low-rank adaptation LoRA language model
- **Date run:** 2026-07-22T15:42:34Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=27847; HIT_CAP=50

### openalex — B1_peft — query 3
- **Query:** adapter modules transformer parameter efficient
- **Date run:** 2026-07-22T15:42:35Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=14774; HIT_CAP=50

### openalex — B1_peft — query 4
- **Query:** prompt tuning prefix tuning soft prompts
- **Date run:** 2026-07-22T15:42:36Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=5939; HIT_CAP=50

### openalex — B1_peft — query 5
- **Query:** parameter-efficient fine-tuning survey
- **Date run:** 2026-07-22T15:42:37Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=194307; HIT_CAP=50

### openalex — B2_quantization — query 1
- **Query:** quantization large language model fine-tuning
- **Date run:** 2026-07-22T15:42:38Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=34564; HIT_CAP=50

### openalex — B2_quantization — query 2
- **Query:** post-training quantization LLM GPTQ AWQ
- **Date run:** 2026-07-22T15:42:39Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=1117; HIT_CAP=50

### openalex — B2_quantization — query 3
- **Query:** QLoRA quantized low-rank adaptation
- **Date run:** 2026-07-22T15:42:39Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=3809; HIT_CAP=50

### openalex — B2_quantization — query 4
- **Query:** quantization-aware training transformer
- **Date run:** 2026-07-22T15:42:40Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=27811; HIT_CAP=50

### openalex — B2_quantization — query 5
- **Query:** low-bit quantization large language models survey
- **Date run:** 2026-07-22T15:42:41Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=13411; HIT_CAP=50

### openalex — B3_memory — query 1
- **Query:** gradient checkpointing activation memory training
- **Date run:** 2026-07-22T15:42:42Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=11679; HIT_CAP=50

### openalex — B3_memory — query 2
- **Query:** FlashAttention memory efficient attention
- **Date run:** 2026-07-22T15:42:43Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=4640; HIT_CAP=50

### openalex — B3_memory — query 3
- **Query:** ZeRO DeepSpeed offloading distributed training memory
- **Date run:** 2026-07-22T15:42:44Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=440; HIT_CAP=50

### openalex — B3_memory — query 4
- **Query:** memory optimization large language model training
- **Date run:** 2026-07-22T15:42:45Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=263775; HIT_CAP=50

### openalex — B4_federated — query 1
- **Query:** federated learning large language models
- **Date run:** 2026-07-22T15:42:46Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=52467; HIT_CAP=50

### openalex — B4_federated — query 2
- **Query:** federated LoRA parameter efficient fine-tuning
- **Date run:** 2026-07-22T15:42:47Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=3081; HIT_CAP=50

### openalex — B4_federated — query 3
- **Query:** communication efficient distributed language model training
- **Date run:** 2026-07-22T15:42:48Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=179749; HIT_CAP=50

### openalex — B4_federated — query 4
- **Query:** federated fine-tuning data heterogeneity non-IID
- **Date run:** 2026-07-22T15:42:49Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=3492; HIT_CAP=50

### dblp — ADOPTION — query 0
- **Query:** (meta)
- **Date run:** 2026-07-22T16:01:47Z
- **Results returned:** 0
- **Notes:** protocol=1.2; DBLP ADOPTED as optional CS-venue completeness check; h=50 cap at request time; uses s2_queries keyword variants

### dblp — B1_peft — query 1
- **Query:** parameter-efficient fine-tuning large language models
- **Date run:** 2026-07-22T15:42:57Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=80; in_coverage_window=50 (DBLP has no server-side year filter; window applied post-hoc for notes only); HIT_CAP=50

### dblp — B1_peft — query 2
- **Query:** low-rank adaptation LoRA language model
- **Date run:** 2026-07-22T15:42:59Z
- **Results returned:** 16
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=16; in_coverage_window=16 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B1_peft — query 3
- **Query:** adapter modules transformer parameter efficient
- **Date run:** 2026-07-22T16:01:49Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### openalex_acm — B1_peft — query 1
- **Query:** parameter-efficient fine-tuning large language models
- **Date run:** 2026-07-22T15:46:17Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=1014; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B1_peft — query 2
- **Query:** low-rank adaptation LoRA language model
- **Date run:** 2026-07-22T15:46:18Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=86; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B1_peft — query 3
- **Query:** adapter modules transformer parameter efficient
- **Date run:** 2026-07-22T15:46:19Z
- **Results returned:** 33
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=33; ACM publisher_lineage=P4310319798

### openalex_acm — B1_peft — query 4
- **Query:** prompt tuning prefix tuning soft prompts
- **Date run:** 2026-07-22T15:46:20Z
- **Results returned:** 20
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=20; ACM publisher_lineage=P4310319798

### openalex_acm — B1_peft — query 5
- **Query:** parameter-efficient fine-tuning survey
- **Date run:** 2026-07-22T15:46:20Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=994; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B2_quantization — query 1
- **Query:** quantization large language model fine-tuning
- **Date run:** 2026-07-22T15:46:21Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=227; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B2_quantization — query 2
- **Query:** post-training quantization LLM GPTQ AWQ
- **Date run:** 2026-07-22T15:46:22Z
- **Results returned:** 3
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=3; ACM publisher_lineage=P4310319798

### openalex_acm — B2_quantization — query 3
- **Query:** QLoRA quantized low-rank adaptation
- **Date run:** 2026-07-22T15:46:22Z
- **Results returned:** 14
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=14; ACM publisher_lineage=P4310319798

### openalex_acm — B2_quantization — query 4
- **Query:** quantization-aware training transformer
- **Date run:** 2026-07-22T15:46:23Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=187; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B2_quantization — query 5
- **Query:** low-bit quantization large language models survey
- **Date run:** 2026-07-22T15:46:24Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=206; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B3_memory — query 1
- **Query:** gradient checkpointing activation memory training
- **Date run:** 2026-07-22T15:46:25Z
- **Results returned:** 42
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=42; ACM publisher_lineage=P4310319798

### openalex_acm — B3_memory — query 2
- **Query:** FlashAttention memory efficient attention
- **Date run:** 2026-07-22T15:46:25Z
- **Results returned:** 15
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=15; ACM publisher_lineage=P4310319798

### openalex_acm — B3_memory — query 3
- **Query:** ZeRO DeepSpeed offloading distributed training memory
- **Date run:** 2026-07-22T15:46:26Z
- **Results returned:** 6
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=6; ACM publisher_lineage=P4310319798

### openalex_acm — B3_memory — query 4
- **Query:** memory optimization large language model training
- **Date run:** 2026-07-22T15:46:27Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=1556; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B4_federated — query 1
- **Query:** federated learning large language models
- **Date run:** 2026-07-22T15:46:28Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=349; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B4_federated — query 2
- **Query:** federated LoRA parameter efficient fine-tuning
- **Date run:** 2026-07-22T15:46:29Z
- **Results returned:** 19
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=19; ACM publisher_lineage=P4310319798

### openalex_acm — B4_federated — query 3
- **Query:** communication efficient distributed language model training
- **Date run:** 2026-07-22T15:46:29Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=854; ACM publisher_lineage=P4310319798; HIT_CAP=50

### openalex_acm — B4_federated — query 4
- **Query:** federated fine-tuning data heterogeneity non-IID
- **Date run:** 2026-07-22T15:46:30Z
- **Results returned:** 34
- **Notes:** protocol=1.2; s2_keyword_variant (not boolean); per_page=50 requested (cap at request time); sort=relevance_score:desc; API totalReported=34; ACM publisher_lineage=P4310319798

### dblp — B1_peft — query 4
- **Query:** prompt tuning prefix tuning soft prompts
- **Date run:** 2026-07-22T16:02:01Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B1_peft — query 5
- **Query:** parameter-efficient fine-tuning survey
- **Date run:** 2026-07-22T15:46:40Z
- **Results returned:** 11
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=11; in_coverage_window=11 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B2_quantization — query 1
- **Query:** quantization large language model fine-tuning
- **Date run:** 2026-07-22T15:46:41Z
- **Results returned:** 12
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=12; in_coverage_window=12 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B2_quantization — query 2
- **Query:** post-training quantization LLM GPTQ AWQ
- **Date run:** 2026-07-22T16:02:11Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B2_quantization — query 3
- **Query:** QLoRA quantized low-rank adaptation
- **Date run:** 2026-07-22T16:02:24Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B2_quantization — query 4
- **Query:** quantization-aware training transformer
- **Date run:** 2026-07-22T15:53:53Z
- **Results returned:** 17
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=17; in_coverage_window=17 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B2_quantization — query 5
- **Query:** low-bit quantization large language models survey
- **Date run:** 2026-07-22T16:02:52Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B3_memory — query 1
- **Query:** gradient checkpointing activation memory training
- **Date run:** 2026-07-22T16:03:26Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B3_memory — query 2
- **Query:** FlashAttention memory efficient attention
- **Date run:** 2026-07-22T15:57:23Z
- **Results returned:** 2
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=2; in_coverage_window=2 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B3_memory — query 3
- **Query:** ZeRO DeepSpeed offloading distributed training memory
- **Date run:** 2026-07-22T16:03:32Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B3_memory — query 4
- **Query:** memory optimization large language model training
- **Date run:** 2026-07-22T15:57:37Z
- **Results returned:** 5
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=5; in_coverage_window=5 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B4_federated — query 1
- **Query:** federated learning large language models
- **Date run:** 2026-07-22T15:57:43Z
- **Results returned:** 50
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=73; in_coverage_window=50 (DBLP has no server-side year filter; window applied post-hoc for notes only); HIT_CAP=50

### dblp — B4_federated — query 2
- **Query:** federated LoRA parameter efficient fine-tuning
- **Date run:** 2026-07-22T16:03:36Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B4_federated — query 3
- **Query:** communication efficient distributed language model training
- **Date run:** 2026-07-22T15:57:53Z
- **Results returned:** 1
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=1; in_coverage_window=1 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### dblp — B4_federated — query 4
- **Query:** federated fine-tuning data heterogeneity non-IID
- **Date run:** 2026-07-22T16:03:43Z
- **Results returned:** 0
- **Notes:** protocol=1.2; s2_keyword_variant; h=50 requested (cap at request time); API totalReported=0; in_coverage_window=0 (DBLP has no server-side year filter; window applied post-hoc for notes only)

### openalex_acm — PUBLISHER_VERIFY — query 0
- **Query:** (meta)
- **Date run:** 2026-07-22T16:04:01Z
- **Results returned:** 0
- **Notes:** protocol=1.2; verified OpenAlex publisher P4310319798 = Association for Computing Machinery (amendment draft ID P4310320503 returned 404 and was replaced)

### dblp — ZERO_RESULTS — query 0
- **Query:** (meta)
- **Date run:** 2026-07-22T16:04:01Z
- **Results returned:** 0
- **Notes:** protocol=1.2; 9/18 s2_queries returned total=0 from DBLP after retry — treated as genuine DBLP keyword misses (strict matching), not silent skips; cap h=50 still applied on non-empty queries
