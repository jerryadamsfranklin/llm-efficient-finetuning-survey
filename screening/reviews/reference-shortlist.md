# New-work reference shortlist (top 30)

Human-verification target for the automated Stage 1 pass of the 2024–2026 band.
Author review recorded 2026-08-17. Do not treat the ranked 30 as the insertion set.

- New-work includes ranked: **3016** (pre-author shortlist review)
- Shortlist size: **30**
- Ranking: `0.55 * log1p(citations)/log1p(max) + 0.45 * section-fit`, with a boost for
  B3 memory (×1.20) and B4 federated (×1.25) so PEFT volume does not crowd them out.
- Dedup: titles compared to `search/existing-references.yaml` (42 manuscript refs).
- Author outcome: **4 drop** (already in the 42), **6 reject** (encoded-rule fails the
  ranking script warned about), **20 agree** (in-scope, non-duplicate). From the 20,
  **13 selected** for primary-source verification before any manuscript insertion.
- PiSSA (#15) re-sectioned to **B1 PEFT** (initialization method, not quantization).

### Author selected 13 (verify before insert)

| # | Paper | Section |
|---|---|---|
| 5 | HydraLoRA | B1 |
| 8 | LISA | B1 |
| 3 | LoRA-GA | B1 |
| 15 | PiSSA | B1 (was mis-tagged B2) |
| 12 | IR-QLoRA | B2 |
| 16 | EfficientQAT | B2 |
| 14 | SpinQuant | B2 |
| 19 | GaLore | B3 |
| 20 | SLTrain | B3 |
| 23 | AdaRankGrad | B3 |
| 26 | OpenFedLLM | B4 |
| 25 | Improving LoRA in Privacy-preserving FL (FFA-LoRA) | B4 |
| 29 | A survey on LoRA of large language models | B4 / existing-surveys |

Verification against primary sources: `screening/reviews/shortlist-13-verification.md`.
Do not insert until that packet is signed off. Two scope flags in that file (SLTrain,
SpinQuant) need an author call before they touch the manuscript.

---

### 1. LoRA+: Efficient Low Rank Adaptation of Large Models
- `C-c51f12f7c3` | 2024 | arXiv (Cornell University) | citations: **549** | section: **B1 PEFT** | score: 0.818
- authors: Soufiane Hayou; N. C. Ghosh; Bin Yu
- relevance: Named PEFT method (B1_peft)
- existing corpus: **duplicates `hayou2024`**
- **verdict:** drop — already in the 42 (`hayou2024`)

### 2. Heterogeneous LoRA for Federated Fine-tuning of On-Device Foundation Models
- `C-1eb6cfda6c` | 2024 | Conference on Empirical Methods in Natural Language Processing | citations: **218** | section: **B1 PEFT** | score: 0.759
- authors: Yae Jee Cho; Luyang Liu; Zheng Xu; Aldi Fahrezi; Gauri Joshi
- relevance: Named PEFT method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — in-scope, not selected for the 13

### 3. Lora-ga: Low-rank adaptation with gradient approximation
- `C-a80f3cac0d` | 2024 | Advances in Neural Information …, 2024 - | citations: **195** | section: **B1 PEFT** | score: 0.752
- authors: S Wang, L Yu, J Li
- relevance: Named PEFT method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B1)**

### 4. DoRA: Weight-Decomposed Low-Rank Adaptation
- `C-46689cdb94` | 2024 | arXiv (Cornell University) | citations: **1527** | section: **B1 PEFT** | score: 0.739
- authors: Shih-Yang Liu; Chien-Yi Wang; Hongxu Yin; Pavlo Molchanov; Yu-Chiang Frank Wang; Kwang‐Ting Cheng; Min-Hung Chen
- relevance: LLM fine-tuning-efficiency method (B1_peft)
- existing corpus: **duplicates `liu2024`**
- **verdict:** drop — already in the 42 (`liu2024`)

### 5. HydraLoRA: An Asymmetric LoRA Architecture for Efficient Fine-Tuning
- `C-65a13e7929` | 2024 | Neural Information Processing Systems | citations: **157** | section: **B1 PEFT** | score: 0.738
- authors: Chunlin Tian; Zhanying Shi; Zhijiang Guo; Li Li; Chengzhong Xu
- relevance: LLM fine-tuning-efficiency method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B1)**

### 6. MixLoRA: Enhancing Large Language Models Fine-Tuning with LoRA based Mixture of Experts
- `C-4f32bdadfb` | 2024 | arXiv.org | citations: **157** | section: **B1 PEFT** | score: 0.738
- authors: Dengchun Li; Yingzi Ma; Naizheng Wang; Zhiyuan Cheng; Lei Duan; Jie Zuo; Cal Yang; Mingjie Tang
- relevance: LLM fine-tuning-efficiency method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — in-scope, not selected for the 13

### 7. Safe LoRA: the Silver Lining of Reducing Safety Risks when Fine-tuning Large Language Models
- `C-7c0e7f01f0` | 2024 | Neural Information Processing Systems | citations: **143** | section: **B1 PEFT** | score: 0.732
- authors: Chia-Yi Hsu; Yu-Lin Tsai; Chih-Hsun Lin; Pin-Yu Chen; Chia-Mu Yu; Chun-ying Huang
- relevance: LLM fine-tuning-efficiency method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — in-scope, not selected for the 13

### 8. LISA: Layerwise Importance Sampling for Memory-Efficient Large Language Model Fine-Tuning
- `C-c5f653cbd2` | 2024 | Neural Information Processing Systems | citations: **119** | section: **B1 PEFT** | score: 0.721
- authors: Rui Pan; Xiang Liu; Shizhe Diao; Renjie Pi; Jipeng Zhang; Chi Han; Tong Zhang
- relevance: LLM fine-tuning-efficiency method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B1)**

### 9. Bi-directional Adapter for Multimodal Tracking
- `C-81185e06f7` | 2024 | Proceedings of the AAAI Conference on Artificial Intelligence | citations: **101** | section: **B1 PEFT** | score: 0.710
- authors: Bing Cao; Junliang Guo; Pengfei Zhu; Qinghua Hu
- relevance: Named PEFT method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** reject — multimodal tracking (vision). Criterion 2.

### 10. Chain of LoRA: Efficient Fine-tuning of Language Models via Residual Learning
- `C-4ca82738b9` | 2024 | arXiv.org | citations: **101** | section: **B1 PEFT** | score: 0.710
- authors: Wenhan Xia; Chengwei Qin; Elad Hazan
- relevance: LLM fine-tuning-efficiency method (B1_peft)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — in-scope, not selected for the 13

### 11. Awq: Activation-aware weight quantization for on-device llm compression and acceleration
- `C-36af38a73f` | 2024 | … of machine learning …, 2024 - | citations: **2704** | section: **B2 quantization** | score: 0.885
- authors: J Lin, J Tang, H Tang, S Yang…
- relevance: LLM quantization method; training vs inference checked at Stage 2 (B2_quantization)
- existing corpus: **duplicates `lin2024`**
- **verdict:** drop — already in the 42 (`lin2024`)

### 12. Accurate LoRA-Finetuning Quantization of LLMs via Information Retention
- `C-392a797fca` | 2024 | arXiv (Cornell University) | citations: **190** | section: **B2 quantization** | score: 0.856
- authors: Haotong Qin; Xudong Ma; Xingyu Zheng; Xiaoyang Li; Yang Zhang; Shouda Liu; Jie Luo; Xianglong Liu; Michele Magno
- relevance: IR-QLoRA improves LoRA-finetuning quantization of LLMs through information retention; core B1/B2 intersection
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B2)**

### 13. Harnessing Earnings Reports for Stock Predictions: A QLoRA-Enhanced LLM Approach
- `C-3c82c940b7` | 2024 | 2024 6th International Conference on Data-driven Optimization of Complex Systems (DOCS) | citations: **53** | section: **B2 quantization** | score: 0.764
- authors: Haowei Ni; Shuchen Meng; Xupeng Chen; Ziqing Zhao; Andi Chen; Panfeng Li; Shiyao Zhang; Qifu Yin; Yuanqing Wang; Yuxi Chan
- relevance: LLM fine-tuning-efficiency method (B2_quantization)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** reject — finance application; QLoRA is machinery. Inclusion 1.

### 14. SpinQuant: LLM quantization with learned rotations
- `C-15aa63fdab` | 2024 | International Conference on Learning Representations | citations: **439** | section: **B2 quantization** | score: 0.752
- authors: Zechun Liu; Changsheng Zhao; Igor Fedorov; Bilge Soran; Dhruv Choudhary; Raghuraman Krishnamoorthi; Vikas Chandra; Yuandong Tian; Tijmen Blankevoort
- relevance: LLM fine-tuning-efficiency method (B2_quantization)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B2)**; see verification flag (PTQ)

### 15. PiSSA: Principal Singular Values and Singular Vectors Adaptation of Large Language Models
- `C-93f716cbf0` | 2024 | arXiv (Cornell University) | citations: **316** | section: **B1 PEFT** | score: 0.728
- authors: Fan-Xu Meng; Zhaohui Wang; Muhan Zhang
- relevance: PEFT initialization (principal singular values/vectors); same architecture as LoRA, not a quantization method
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B1)**; ranking had mis-sectioned this as B2

### 16. EfficientQAT: Efficient Quantization-Aware Training for Large Language Models
- `C-3f09ccfe68` | 2024 | Annual Meeting of the Association for Computational Linguistics | citations: **226** | section: **B2 quantization** | score: 0.704
- authors: Mengzhao Chen; Wenqi Shao; Peng Xu; Jiahao Wang; Peng Gao; Kai-Chuang Zhang; Yu Qiao; Ping Luo
- relevance: LLM fine-tuning-efficiency method (B2_quantization)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B2)**

### 17. Extreme Compression of Large Language Models via Additive Quantization
- `C-526edc8eb8` | 2024 | International Conference on Machine Learning | citations: **226** | section: **B2 quantization** | score: 0.704
- authors: Vage Egiazarian; Andrei Panferov; Denis Kuznedelev; Elias Frantar; Artem Babenko; Dan Alistarh
- relevance: LLM quantization method; training vs inference checked at Stage 2 (B2_quantization)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — in-scope, not selected for the 13

### 18. BioMistral: A Collection of Open-Source Pretrained Large Language Models for Medical Domains
- `C-541eb63c42` | 2024 | _none_ | citations: **213** | section: **B2 quantization** | score: 0.699
- authors: Yanis Labrak; Adrien Bazoge; Emmanuel Morin; Pierre‐antoine Gourraud; Mickaël Rouvier; Richard Dufour
- relevance: LLM quantization method; training vs inference checked at Stage 2 (B2_quantization)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** reject — medical pretrained-model release, not a fine-tuning-efficiency method. Inclusion 1.

### 19. GaLore: Memory-Efficient LLM Training by Gradient Low-Rank Projection
- `C-57aa0c8ae7` | 2024 | International Conference on Machine Learning | citations: **500** | section: **B3 memory** | score: 1.059
- authors: Jiawei Zhao; Zhenyu (Allen) Zhang; Beidi Chen; Zhangyang Wang; Anima Anandkumar; Yuandong Tian
- relevance: LLM fine-tuning-efficiency method (B3_memory)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B3)**

### 20. SLTrain: a sparse plus low-rank approach for parameter and memory efficient pretraining
- `C-1d12d2b919` | 2024 | Neural Information Processing Systems | citations: **50** | section: **B3 memory** | score: 0.868
- authors: Andi Han; Jiaxiang Li; Wei Huang; Mingyi Hong; Akiko Takeda; Pratik Jawanpuria; Bamdev Mishra
- relevance: LLM fine-tuning-efficiency method (B3_memory)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B3)**; see verification flag (Exclusion 1 / pretraining-only)

### 21. Break the Sequential Dependency of LLM Inference Using Lookahead Decoding
- `C-80ade0780f` | 2024 | International Conference on Machine Learning | citations: **336** | section: **B3 memory** | score: 0.837
- authors: Yichao Fu; Peter Bailis; Ion Stoica; Hao Zhang
- relevance: LLM fine-tuning-efficiency method (B3_memory)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** reject — inference decoding, not training memory. Exclusion 2.

### 22. LongVILA: Scaling Long-Context Visual Language Models for Long Videos
- `C-61b96120af` | 2024 | International Conference on Learning Representations | citations: **306** | section: **B3 memory** | score: 0.829
- authors: Fuzhao Xue; Yukang Chen; Dacheng Li; Qinghao Hu; Ligeng Zhu; Xiuyu Li; Yunhao Fang; Haotian Tang; Shang Yang; Zhijian Liu; Ethan He; Hongxu Yin; Pavlo Molchanov; Jan Kautz; L. Fan; Yuke Zhu; Yao Lu; Song Han
- relevance: LLM fine-tuning-efficiency method (B3_memory)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** reject — visual language models for videos; context scaling, not fine-tuning efficiency. Criterion 2.

### 23. AdaRankGrad: Adaptive Gradient-Rank and Moments for Memory-Efficient LLMs Training and Fine-Tuning
- `C-05c157f898` | 2024 | International Conference on Learning Representations | citations: **17** | section: **B3 memory** | score: 0.781
- authors: Yehonathan Refael; Jonathan Svirsky; Boris Shustin; Wasim Huleihel; Ofir Lindenbaum
- relevance: LLM fine-tuning-efficiency method (B3_memory)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B3)**

### 24. An Emotion Text Classification Model Based on Llama3-8b Using Lora Technique
- `C-3b4f1737c6` | 2024 | 2024 7th International Conference on Computer Information Science and Application Technology (CISAT) | citations: **14** | section: **B3 memory** | score: 0.766
- authors: Hongyi Shui; Yuanjing Zhu; Fan Zhuo; Yibo Sun; Daoyuan Li
- relevance: LLM fine-tuning-efficiency method (B3_memory)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** reject — classification application using LoRA. Inclusion 1.

### 25. Improving LoRA in Privacy-preserving Federated Learning
- `C-aaedc3bee8` | 2024 | International Conference on Learning Representations | citations: **302** | section: **B4 federated** | score: 1.060
- authors: Youbang Sun; Zitao Li; Yaliang Li; Bolin Ding
- relevance: LLM fine-tuning-efficiency method (B4_federated)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B4)**

### 26. OpenFedLLM: Training Large Language Models on Decentralized Private Data via Federated Learning
- `C-bc98faf889` | 2024 | Knowledge Discovery and Data Mining | citations: **227** | section: **B4 federated** | score: 1.035
- authors: Rui Ye; Wenhao Wang; Jingyi Chai; Dihan Li; Zexi Li; Yinda Xu; Yaxin Du; Yanfeng Wang; Siheng Chen
- relevance: LLM fine-tuning-efficiency method (B4_federated)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B4)**

### 27. FLoRA: Federated Fine-Tuning Large Language Models with Heterogeneous Low-Rank Adaptations
- `C-ddcb80926e` | 2024 | Neural Information Processing Systems | citations: **224** | section: **B4 federated** | score: 1.034
- authors: Ziyao Wang; Zheyu Shen; Yexiao He; Guoheng Sun; Hongyi Wang; Lingjuan Lyu; Ang Li
- relevance: LLM fine-tuning-efficiency method (B4_federated)
- existing corpus: **duplicates `zhang2024`** (title match; manuscript author string is Zhang et al. — see verification note)
- **verdict:** drop — already in the 42 (`zhang2024`); do not add a second FLoRA cite

### 28. Federated Fine-tuning of Large Language Models under Heterogeneous Tasks and Client Resources
- `C-a1f9ae845d` | 2024 | Neural Information Processing Systems | citations: **201** | section: **B4 federated** | score: 1.024
- authors: Jiamu Bai; Daoyuan Chen; Bingchen Qian; Liuyi Yao; Yaliang Li
- relevance: LLM fine-tuning-efficiency method (B4_federated)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — in-scope, not selected for the 13

### 29. A survey on LoRA of large language models
- `C-64babd74d3` | 2024 | Frontiers of Computer Science | citations: **163** | section: **B4 federated** | score: 1.006
- authors: Yuren Mao; Yuhang Ge; Yijiang Fan; Wenyi Xu; Yu Mi; Zhonghao Hu; Yunjun Gao
- relevance: 'A survey on LoRA of large language models'; the core PEFT survey for block B1
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — **selected (B4 / existing-surveys table)**

### 30. Selective Aggregation for Low-Rank Adaptation in Federated Learning
- `C-ce6d9165d5` | 2024 | International Conference on Learning Representations | citations: **117** | section: **B4 federated** | score: 0.978
- authors: Pengxin Guo; Shuang Zeng; Yanran Wang; Huijie Fan; Feifei Wang; Liangqiong Qu
- relevance: Named PEFT method (B4_federated)
- existing corpus: no — not in the 42 existing manuscript references
- **verdict:** agree — in-scope, not selected for the 13
