# New-work batch 001 — calibration sample

Source: `screening/decisions/stage1_new_work_001.json`. Mark each **verdict** line `agree` / `disagree` / `unsure`.
Screening of the next block is paused until this returns.

- Records in block: **150** — 54 include, 96 exclude, 0 hold
- Requiring your review: **100** (54 includes, 26 low-confidence excludes, 0 holds, 20 sampled confident excludes)
- Low-confidence rate: 26/54 includes, 26/96 excludes
- Exclude sample seed: `1` (regenerates identically)

---

## A. Includes (54) — advance to Stage 2 if you agree

### 1. A Comparative Analysis of Instruction Fine-Tuning LLMs for Financial Text Classification
- `C-3fef54df25` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: Instruction fine-tuning of 7-8B LLMs for financial classification. Domain application; efficiency framing is model-size choice rather than a fine-tuning efficiency method. Advanced under bias-to-inclusion for Stage 2 to resolve.
- abstract: Large Language Models (LLMs) have demonstrated impressive capabilities across diverse Natural Language Processing (NLP) tasks, including language understanding, reasoning, and generation. However, general-domain LLMs often struggle with financial tasks due to the technical and specialized nature of financial texts. This study investigates the efficacy of instruction fine-tuning smaller-scale LLMs, including Mistral-7...
- **verdict:**  agree

### 2. A Comprehensive Evaluation of Large Language Models on Aspect-Based Sentiment Analysis
- `C-203fc69734` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: ABSA evaluation that explicitly compares ICL against PEFT. Evaluation of PEFT is in scope, but the paper's subject is the task, not the method.
- abstract: Recently, Large Language Models (LLMs) have garnered increasing attention in the field of natural language processing, revolutionizing numerous downstream tasks with powerful reasoning and generation abilities. For example, In-Context Learning (ICL) introduces a fine-tuning-free paradigm, allowing out-of-the-box LLMs to execute downstream tasks by analogy learning without any fine-tuning. Besides, in a fine-tuning-de...
- **verdict:**  agree

### 3. A Comprehensive Evaluation of Quantization Strategies for Large Language Models
- `C-976e1ca49b` | 2024 | Annual Meeting of the Association for Computational Linguistics | citations: 153 | confidence: **low**
- screener note: Quantization strategies for LLMs including effects on instruction-tuned models. Risk of being inference-only PTQ (exclusion 2); the instruction-tuning angle keeps it in for Stage 2.
- abstract: Increasing the number of parameters in large language models (LLMs) usually improves performance in downstream tasks but raises compute and memory costs, making deployment difficult in resource-limited settings. Quantization techniques, which reduce the bits needed for model weights or activations with minimal performance loss, have become popular due to the rise of LLMs. However, most quantization studies use pre-tr...
- **verdict:** agree

### 4. A Comprehensive Survey of Small Language Models in the Era of Large Language Models: Techniques, Enhancements, Applications, Collaboration with LLMs, and Trustworthiness
- `C-bed03b2915` | 2024 | ACM Transactions on Intelligent Systems and Technology | citations: 237 | confidence: **low**
- screener note: Survey of small language models covering compression and fine-tuning cost. Survey route of criterion 2 applies, but the SLM focus may fall outside the LLM boundary at Stage 2.
- abstract: Large language models (LLMs) have demonstrated emergent abilities in text generation, question answering, and reasoning, facilitating various tasks and domains. Despite their proficiency in various tasks, LLMs like PaLM 540B and Llama-3.1 405B face limitations due to large parameter sizes and computational demands, often requiring cloud API use, which raises privacy concerns, limits real-time applications on edge dev...
- **verdict:** agree

### 5. A Fast, Performant, Secure Distributed Training Framework For Large Language Model
- `C-14495abbe7` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: Secure distributed LLM fine-tuning placing LoRA / P-tuning v2 structures in a TEE. Federated fine-tuning is in scope; the contribution is primarily a security architecture.
- abstract: The distributed (federated) LLM is an important method for co-training the domain-specific LLM using siloed data. However, maliciously stealing model parameters and data from the server or client side has become an urgent problem to be solved. In this paper, we propose a secure distributed LLM based on model slicing. In this case, we deploy the Trusted Execution Environment (TEE) on both the client and server side, a...
- **verdict:**  agree

### 6. A Federated Learning-Friendly Approach for Parameter-Efficient Fine-Tuning of SAM in 3D Segmentation
- `C-eabd183905` | 2024 | ISIC/iMIMIC/EARTH/DeCaF@MICCAI | citations: 20 | confidence: **low**
- screener note: Federated PEFT of SAM for 3D segmentation. PEFT plus federated is in scope, but SAM is a vision model and may fail criterion 2.
- abstract: Adapting foundation models for medical image analysis requires finetuning them on a considerable amount of data because of extreme distribution shifts between natural (source) data used for pretraining and medical (target) data. However, collecting task-specific medical data for such finetuning at a central location raises many privacy concerns. Although Federated learning (FL) provides an effective means for trainin...
- **verdict:** disagree

### 7. A Large-scale Medical Visual Task Adaptation Benchmark
- `C-1f69bb5c6f` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: Med-VTAB visual task adaptation benchmark using learnable layers and tokens, i.e. PEFT for ViTs. Vision domain-boundary case against the LLM scope.
- abstract: Visual task adaptation has been demonstrated to be effective in adapting pre-trained Vision Transformers (ViTs) to general downstream visual tasks using specialized learnable layers or tokens. However, there is yet a large-scale benchmark to fully explore the effect of visual task adaptation on the realistic and important medical domain, particularly across diverse medical visual modalities, such as color images, X-r...
- **verdict:** disagree

### 8. A New 2-bit Model Quantization Method Based on Non-uniform Quantization
- `C-b825a93e20` | 2024 | International Conference on Industrial Technology | citations: 0 | confidence: **low**
- screener note: Non-uniform 2-bit quantization for LLMs, referencing use in both compression and fine-tuning. Likely inference-side (exclusion 2); the fine-tuning reference keeps it in for Stage 2.
- abstract: Recently, quantization of large language models (LLMs) has emerged as a crucial technique for model compression, enabling deployment on edge computing devices and enhancing their efficiency. Techniques such as LLM.int8 are widely utilized in the fields of model compression and fine-tuning. However, as the number of quantization bits decreases, these conventional methods often result in a significant degradation of mo...
- **verdict:**  agree

### 9. A Novel Prompt Tuning for Graph Transformers: Tailoring Prompts to Graph Topologies
- `C-73feb84f4d` | 2024 | Knowledge Discovery and Data Mining | citations: 7 | confidence: **low**
- screener note: Deep graph prompt tuning that cuts training storage. Prompt tuning is in the PEFT family, but graph transformers are outside the language-model boundary.
- abstract: Deep graph prompt tuning (DeepGPT), which only tunes a set of continuous prompts for graph transformers, significantly decreases the storage usage during training. However, DeepGPT is limited by its uniform prompts to input graphs with various structures. This is because different graph structures dictate various feature interactions between nodes, while the uniform prompts are not dynamic to tailor the feature trans...
- **verdict:**  disagree

### 10. A Novel Prompt-tuning Method: Incorporating Scenario-specific Concepts into a Verbalizer
- `C-75da2d81fe` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: Verbalizer construction for prompt tuning. Prompt tuning is a PEFT family member, though the contribution is closer to prompt design than efficiency.
- abstract: The verbalizer, which serves to map label words to class labels, is an essential component of prompt-tuning. In this paper, we present a novel approach to constructing verbalizers. While existing methods for verbalizer construction mainly rely on augmenting and refining sets of synonyms or related words based on class names, this paradigm suffers from a narrow perspective and lack of abstraction, resulting in limited...
- **verdict:**  agree

### 11. A Parameter-Efficient Multi-Step Fine-Tuning of Multilingual and Multi-Task Learning Model for Japanese Dialect Speech Recognition
- `C-90fc511d61` | 2024 | Oriental COCOSDA International Conference on Speech Database and Assessments | citations: 1 | confidence: **low**
- screener note: Parameter-efficient multi-step fine-tuning for Japanese dialect ASR. PEFT method, speech domain-boundary.
- abstract: This paper addresses the challenge of developing a unified spoken language model for Japanese dialects. Due to the limited availability of such speech resources, self-supervised learning (SSL) methods show promise. However, the diversity of Japanese dialects also requires multilingual approaches to language modeling. One of the few related works improved performance through multi-step fine-tuning, using standard Japa...
- **verdict:**  disagree

### 12. A Parameter-efficient Language Extension Framework for Multilingual ASR
- `C-27a90d06c5` | 2024 | Interspeech | citations: 6 | confidence: **low**
- screener note: Parameter-efficient language extension for multilingual ASR. PEFT method, speech domain-boundary.
- abstract: Covering all languages with a multilingual speech recognition model (MASR) is very difficult. Performing language extension on top of an existing MASR is a desirable choice. In this study, the MASR continual learning problem is probabilistically decomposed into language identity prediction (LP) and cross-lingual adaptation (XLA) sub-problems. Based on this, we propose an architecture-based framework for language exte...
- **verdict:**  disagree

### 13. A Study on the Application of Using Hypernetwork and Low Rank Adaptation for Text-to-Image Generation Based on Diffusion Models
- `C-8081e358c7` | 2024 | 2024 6th International Youth Conference on Radio Electronics, Electrical and Power Engineering (REEPE) | citations: 6 | confidence: **low**
- screener note: Hypernetwork plus LoRA for text-to-image diffusion. LoRA method work in a diffusion/vision setting; criterion 2 risk.
- abstract: Recent advances in the field of image generation have attracted attention due to the growing number of diverse data sources and test samples. A primary driver of this evolution is the application of neural networks, particularly for generating high-quality images from textual prompts. Despite the potential of diffusion models in this sector, they typically face computational challenges associated with vast datasets. ...
- **verdict:**  disagree

### 14. A Survey on In-context Learning
- `C-f2a722984e` | 2024 | no venue | citations: 540 | confidence: **low**
- screener note: Survey of in-context learning, a fine-tuning-free adaptation paradigm. In scope only if adaptation without training counts under criterion 1; flagged for that judgement.
- abstract: Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia, Jingjing Xu, Zhiyong Wu, Baobao Chang, Xu Sun, Lei Li, Zhifang Sui. Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing. 2024....
- **verdict:** agree

### 15. A comprehensive review of model compression techniques in machine learning
- `C-6d4690a604` | 2024 | Applied Intelligence | citations: 203 | confidence: **low**
- screener note: Review of model compression techniques. Compression overlaps block B2, but the scope is general ML rather than LLM fine-tuning.
- abstract: Abstract This paper critically examines model compression techniques within the machine learning (ML) domain, emphasizing their role in enhancing model efficiency for deployment in resource-constrained environments, such as mobile devices, edge computing, and Internet of Things (IoT) systems. By systematically exploring compression techniques and lightweight design architectures, it is provided a comprehensive unders...
- **verdict:**  agree

### 16. A comprehensive study on quantization techniques for large language models
- `C-16946e7c21` | 2024 | 2024 4th International conference on …, 2024 - | citations: 146 | confidence: **low**
- screener note: 'A comprehensive study on quantization techniques for large language models', 146 citations, no abstract available. Title cannot separate training-time from inference-only quantization, so confidence stays low.
- abstract: _none available_
- **verdict:**  agree

### 17. A modified transformer and adapter-based transfer learning for fault detection and diagnosis in HVAC systems
- `C-fc2b996b81` | 2024 | Energy Storage and Saving | citations: 20 | confidence: **low**
- screener note: Adapter-based transfer learning for HVAC fault detection. Adapters are in scope as a method, but the models are small and non-language.
- abstract: Fault detection and diagnosis (FDD) of heating, ventilating, and air conditioning (HVAC) systems can help to improve the energy saving in building energy systems. However, most data-driven trained FDD models have limited generalizability and can only be applied to specific systems. The diversity of HVAC systems and the high cost of data acquisition present challenges for the practical application of FDD. Transfer lea...
- **verdict:**  disagree

### 18. AAT: Adapting Audio Transformer for Various Acoustics Recognition Tasks
- `C-8f2ee64cc1` | 2024 | ICASSP 2024 - 2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) | citations: 3 | confidence: **low**
- screener note: AAT adapts audio transformers with adapters instead of full fine-tuning. PEFT method, audio domain-boundary.
- abstract: Recently, Transformers have been introduced into the field of acoustics recognition. They are pre-trained on large-scale datasets using methods such as supervised learning and semi-supervised learning, demonstrating robust generality——It fine-tunes easily to down-stream tasks and shows more robust performance. However, the predominant fine-tuning method currently used is still full fine-tuning, which involves updatin...
- **verdict:**  disagree

### 19. ADAPT to Robustify Prompt Tuning Vision Transformers
- `C-67fa715de7` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: ADAPT robustifies prompt tuning for vision transformers and cites per-task storage of billion-parameter models. PEFT method, vision domain-boundary.
- abstract: The performance of deep models, including Vision Transformers, is known to be vulnerable to adversarial attacks. Many existing defenses against these attacks, such as adversarial training, rely on full-model fine-tuning to induce robustness in the models. These defenses require storing a copy of the entire model, that can have billions of parameters, for each task. At the same time, parameter-efficient prompt tuning ...
- **verdict:**  agree

### 20. APrompt4EM: Augmented Prompt Tuning for Generalized Entity Matching
- `C-68c85fdb46` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: APrompt4EM augmented prompt tuning for entity matching. Prompt tuning of PLMs is in the PEFT family; the subject is the data-management task.
- abstract: Generalized Entity Matching (GEM), which aims at judging whether two records represented in different formats refer to the same real-world entity, is an essential task in data management. The prompt tuning paradigm for pre-trained language models (PLMs), including the recent PromptEM model, effectively addresses the challenges of low-resource GEM in practical applications, offering a robust solution when labeled data...
- **verdict:** disagree

### 21. ASR Model Adaptation with Domain Prompt Tuning
- `C-437e4fc9a8` | 2024 | 2024 International Conference on Asian Language Processing (IALP) | citations: 0 | confidence: **low**
- screener note: Domain-Prompts trains a small set of pluggable domain embeddings for ASR adaptation with low memory overhead. PEFT method, speech domain-boundary.
- abstract: Automatic speech recognition (ASR) systems are already used in many industrial applications and, therefore, they need to be adapted to new domains with small memory and deployment overhead. In this work, we introduce Domain-Prompts, a methodology that involves training a small number of pluggable domain embedding parameters on a base ASR model for fast domain adaptation. On Aishell-1, Aishell-4, Ancient Poetry, and C...
- **verdict:**  disagree

### 22. ATFLRec: A Multimodal Recommender System with Audio-Text Fusion and Low-Rank Adaptation via Instruction-Tuned Large Language Model
- `C-1a0ec2ecf9` | 2024 | arXiv.org | citations: 4 | confidence: **low**
- screener note: ATFLRec uses LoRA on an instruction-tuned LLM for multimodal recommendation. LoRA is machinery for a recommender contribution.
- abstract: Recommender Systems (RS) play a pivotal role in boosting user satisfaction by providing personalized product suggestions in domains such as e-commerce and entertainment. This study examines the integration of multimodal data text and audio into large language models (LLMs) with the aim of enhancing recommendation performance. Traditional text and audio recommenders encounter limitations such as the cold-start problem...
- **verdict:**  disagree

### 23. AV-PEA: Parameter-Efficient Adapter for Audio-Visual Multimodal Learning
- `C-0f3972344a` | 2024 | VISIGRAPP : VISAPP | citations: 4 | confidence: **low**
- screener note: AV-PEA parameter-efficient adapter for audio-visual learning, motivated by trainable-parameter and storage cost. PEFT method, multimodal domain-boundary.
- abstract: : Fine-tuning has emerged as a widely used transfer learning technique for leveraging pre-trained vision trans-formers in various downstream tasks. However, its success relies on tuning a significant number of trainable parameters, which could lead to significant costs in terms of both model training and storage. When it comes to audio-visual multimodal learning, the challenge also lies in effectively incorporating b...
- **verdict:**  disagree

### 24. Abstractive summarization from Audio Transcription
- `C-84a30630d1` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: Abstractive summarization from audio transcription, explicitly motivated by LoRA and quantization to avoid large compute. Efficiency methods are applied rather than advanced.
- abstract: Currently, large language models are gaining popularity, their achievements are used in many areas, ranging from text translation to generating answers to queries. However, the main problem with these new machine learning algorithms is that training such models requires large computing resources that only large IT companies have. To avoid this problem, a number of methods (LoRA, quantization) have been proposed so th...
- **verdict:**disagree

### 25. Achieving Dimension-Free Communication in Federated Learning via Zeroth-Order Optimization
- `C-d45c0544b4` | 2024 | arXiv | citations: 0 | confidence: **low**
- screener note: Dimension-free federated communication via zeroth-order optimization, framed for large-model scenarios. Memory-efficient optimization is in scope; the LLM tie is indirect.
- abstract: Federated Learning (FL) offers a promising framework for collaborative and privacy-preserving machine learning across distributed data sources. However, the substantial communication costs associated with FL significantly challenge its efficiency. Specifically, in each communication round, the communication costs scale linearly with the model's dimension, which presents a formidable obstacle, especially in large mode...
- **verdict:**  agree

### 26. Achieving peak performance for large language models: A systematic review
- `C-1f38e19249` | 2024 | IEEE access, 2024 | citations: 58 | confidence: **low**
- screener note: 'Achieving peak performance for large language models: A systematic review', 58 citations, no abstract available. A systematic review of LLM performance plausibly covers efficiency, but the title cannot confirm the subject.
- abstract: _none available_
- **verdict:**  agree

### 27. A Comparison of LLM Finetuning Methods & Evaluation Metrics with Travel Chatbot Use Case
- `C-7bcd1b0367` | 2024 | arXiv | citations: 0 | confidence: **high**
- screener note: Compares QLoRA, RAFT and RLHF as fine-tuning methods; QLoRA comparison is squarely block B1/B2.
- abstract: This research compares large language model (LLM) fine-tuning methods, including Quantized Low Rank Adapter (QLoRA), Retrieval Augmented fine-tuning (RAFT), and Reinforcement Learning from Human Feedback (RLHF), and additionally compared LLM evaluation methods including End to End (E2E) benchmark method of "Golden Answers", traditional natural language processing (NLP) metrics, RAG Assessment (Ragas), OpenAI GPT-4 ev...
- **verdict:**  agree

### 28. A Comprehensive Evaluation of Parameter-Efficient Fine-Tuning on Automated Program Repair
- `C-bd76aae186` | 2024 | arXiv.org | citations: 4 | confidence: **high**
- screener note: 'A Comprehensive Evaluation of Parameter-Efficient Fine-Tuning on Automated Program Repair'. No abstract, but the title states a PEFT evaluation unambiguously.
- abstract: _none available_
- **verdict:**  agree

### 29. A Comprehensive Evaluation of Parameter-Efficient Fine-Tuning on Code Smell Detection
- `C-568fced344` | 2024 | ACM Transactions on Software Engineering and Methodology | citations: 6 | confidence: **high**
- screener note: PEFT evaluation for code smell detection; explicit PEFT adaptation of LLMs.
- abstract: Code smells are indicators of suboptimal design that negatively impact software quality. However, automated code smell detection remains a persistent challenge: heuristics-based tools suffer from high sensitivity to threshold selection and inherent subjectivity, while Machine Learning (ML) and Deep Learning (DL) models yield unsatisfactory performance. Although Large Language Models (LLMs) offer a promising solution ...
- **verdict:**  agree

### 30. A Framework to Implement 1+N Multi-task Fine-tuning Pattern in LLMs Using the CGC-LORA Algorithm
- `C-be8796dd0e` | 2024 | arXiv | citations: 0 | confidence: **high**
- screener note: CGC-LoRA multi-task fine-tuning framework for LLMs; core LoRA method work.
- abstract: With the productive evolution of large language models (LLMs) in the field of natural language processing (NLP), tons of effort has been made to effectively fine-tune common pre-trained LLMs to fulfill a variety of tasks in one or multiple specific domain. In practice, there are two prevailing ways, in which the adaptation can be achieved: (i) Multiple Independent Models: Pre-trained LLMs are fine-tuned a few times i...
- **verdict:**  agree

### 31. A Note on LoRA
- `C-5b5e0cfe55` | 2024 | arXiv | citations: 0 | confidence: **high**
- screener note: 'A Note on LoRA' extending the original LoRA paper with deployment-at-scale insights; core PEFT.
- abstract: LoRA (Low-Rank Adaptation) has emerged as a preferred method for efficiently adapting Large Language Models (LLMs) with remarkable simplicity and efficacy. This note extends the original LoRA paper by offering new perspectives that were not initially discussed and presents a series of insights for deploying LoRA at scale. Without introducing new experiments, we aim to improve the understanding and application of LoRA...
- **verdict:**  agree

### 32. A Quantization Approach for the Reduced Size of Large Language Models
- `C-30e876bb19` | 2024 | 2024 16th International Conference on Knowledge and Smart Technology (KST) | citations: 14 | confidence: **high**
- screener note: Quantization plus a PEFT library to shrink Llama-2-7B, GPT-J and LLaMA; combines both core blocks.
- abstract: The use of large-language models is widespread in a range of applications, including natural language processing and multimodal tasks. However, these models are computationally intensive. This work presents a novel approach that shows the ability to reduce the size of publicly available LLMs, including Llama-2-7B, GPT-J, and LLaMA. This work uses a parameter-efficient fine-tuning (PEFT) library. The experiment reveal...
- **verdict:**  agree

### 33. A Single Linear Layer Yields Task-Adapted Low-Rank Matrices
- `C-1b86167855` | 2024 | arXiv | citations: 0 | confidence: **high**
- screener note: Analysis of LoRA's low-rank matrices and their relation to pretrained weights; core PEFT theory.
- abstract: Low-Rank Adaptation (LoRA) is a widely used Parameter-Efficient Fine-Tuning (PEFT) method that updates an initial weight matrix $W_0$ with a delta matrix $ΔW$ consisted by two low-rank matrices $A$ and $B$. A previous study suggested that there is correlation between $W_0$ and $ΔW$. In this study, we aim to delve deeper into relationships between $W_0$ and low-rank matrices $A$ and $B$ to further comprehend the behav...
- **verdict:**  agree

### 34. A Study of Optimizations for Fine-tuning Large Language Models
- `C-5ddc66b3d8` | 2024 | arXiv.org | citations: 29 | confidence: **high**
- screener note: 'A Study of Optimizations for Fine-tuning Large Language Models' addressing fine-tuning memory and resource budget; directly in scope.
- abstract: Fine-tuning large language models is a popular choice among users trying to adapt them for specific applications. However, fine-tuning these models is a demanding task because the user has to examine several factors, such as resource budget, runtime, model size and context length among others. A specific challenge is that fine-tuning is memory intensive, imposing constraints on the required hardware memory and contex...
- **verdict:** agree

### 35. A Study on Text Classification in the Age of Large Language Models
- `C-7975fb9289` | 2024 | Machine Learning and Knowledge Extraction | citations: 12 | confidence: **high**
- screener note: Text classification study built on quantization, prefix tuning, LoRA and prompting as customization techniques.
- abstract: Large language models (LLMs) have recently made significant advances, excelling in tasks like question answering, summarization, and machine translation. However, their enormous size and hardware requirements make them less accessible to many in the machine learning community. To address this, techniques such as quantization, prefix tuning, weak supervision, low-rank adaptation, and prompting have been developed to c...
- **verdict:**  agree

### 36. A Survey of Low-bit Large Language Models: Basics, Systems, and Algorithms
- `C-7a503157be` | 2024 | arXiv.org | citations: 38 | confidence: **high**
- screener note: Survey of low-bit LLMs covering basics, systems and algorithms; quantization survey in block B2.
- abstract: Large language models (LLMs) have achieved remarkable advancements in natural language processing, showcasing exceptional performance across various tasks. However, the expensive memory and computational requirements present significant challenges for their practical deployment. Low-bit quantization has emerged as a critical approach to mitigate these challenges by reducing the bit-width of model parameters, activati...
- **verdict:**  agree

### 37. A Survey of Resource-efficient LLM and Multimodal Foundation Models
- `C-efc12cfe27` | 2024 | arXiv (Cornell University) | citations: 32 | confidence: **high**
- screener note: 'A Survey of Resource-efficient LLM and Multimodal Foundation Models' spanning training to deployment; squarely in scope.
- abstract: Large foundation models, including large language models (LLMs), vision transformers (ViTs), diffusion, and LLM-based multimodal models, are revolutionizing the entire machine learning lifecycle, from training to deployment. However, the substantial advancements in versatility and performance these models offer come at a significant cost in terms of hardware resources. To support the growth of these large models in a...
- **verdict:**  agree

### 38. A Survey on Efficient Federated Learning Methods for Foundation Model Training
- `C-b1adacbef7` | 2024 | International Joint Conference on Artificial Intelligence | citations: 74 | confidence: **high**
- screener note: Survey of efficient federated learning for foundation model training; federated fine-tuning block.
- abstract: Federated Learning (FL) has become an established technique to facilitate privacy-preserving collaborative training across a multitude of clients. However, new approaches to FL often discuss their contributions involving small deep-learning models only and focus on training full models on clients. In the wake of Foundation Models (FM), the reality is different for many deep learning applications. Typically, FMs have ...
- **verdict:** agree

### 39. A fine-tuning enhanced RAG system with quantized influence measure as AI judge
- `C-f267e4b7cc` | 2024 | Scientific Reports | citations: 40 | confidence: **high**
- screener note: Fine-tuning-enhanced RAG system built on LoRA and QLoRA; core methods.
- abstract: This study presents an innovative enhancement to retrieval-augmented generation (RAG) systems by seamlessly integrating fine-tuned large language models (LLMs) with vector databases. This integration capitalizes on the combined strengths of structured data retrieval and the nuanced comprehension provided by advanced LLMs. Central to our approach are the LoRA and QLoRA methodologies, which stand at the forefront of mo...
- **verdict:**  agree

### 40. A survey on LoRA of large language models
- `C-64babd74d3` | 2024 | Frontiers of Computer Science | citations: 163 | confidence: **high**
- screener note: 'A survey on LoRA of large language models'; the core PEFT survey for block B1.
- abstract: Low-Rank Adaptation~(LoRA), which updates the dense neural network layers with pluggable low-rank matrices, is one of the best performed parameter efficient fine-tuning paradigms. Furthermore, it has significant advantages in cross-task generalization and privacy-preserving. Hence, LoRA has gained much attention recently, and the number of related literature demonstrates exponential growth. It is necessary to conduct...
- **verdict:** agree

### 41. ACCEPT: Adaptive Codebook for Composite and Efficient Prompt Tuning
- `C-844988640c` | 2024 | Conference on Empirical Methods in Natural Language Processing | citations: 1 | confidence: **high**
- screener note: ACCEPT adaptive codebook for composite prompt tuning; explicit PEFT method.
- abstract: Prompt Tuning has been a popular Parameter-Efficient Fine-Tuning method attributed to its remarkable performance with few updated parameters on various large-scale pretrained Language Models (PLMs). Traditionally, each prompt has been considered indivisible and updated independently, leading the parameters increase proportionally as prompt length grows. To address this issue, we propose Adaptive Codebook for Composit...
- **verdict:**  agree

### 42. ACCO: Accumulate While You Communicate for Communication-Overlapped Sharded LLM Training
- `C-54f4f9aa57` | 2024 | no venue | citations: 5 | confidence: **high**
- screener note: ACCO overlaps communication with computation for sharded LLM training and optimizer state; training-time memory and communication, block B3.
- abstract: Training LLMs relies on distributed implementations using multiple GPUs to compute gradients in parallel with sharded optimizers. However, synchronizing gradients in data parallel setups introduces communication overhead that grows with the number of workers, limiting parallelization efficiency. Local optimization algorithms reduce communications but incur high memory costs as they prevent optimizer state sharding, h...
- **verdict:** agree

### 43. AFLoRA: Adaptive Freezing of Low Rank Adaptation in Parameter Efficient Fine-Tuning of Large Models
- `C-ac10d326c1` | 2024 | Annual Meeting of the Association for Computational Linguistics | citations: 25 | confidence: **high**
- screener note: AFLoRA adaptively freezes low-rank adaptation paths; core PEFT method.
- abstract: We present a novel Parameter-Efficient Fine-Tuning (PEFT) method, dubbed as Adaptive Freezing of Low Rank Adaptation (AFLoRA). Specifically, for each pre-trained frozen weight tensor, we add a parallel path of trainable low-rank matrices, namely a down-projection and an up-projection matrix, each of which is followed by a feature transformation vector. Based on a novel freezing score, we the incrementally freeze thes...
- **verdict:**  agree

### 44. ALLoRA: Adaptive Learning Rate Mitigates LoRA Fatal Flaws
- `C-8199b26603` | 2024 | arXiv | citations: 0 | confidence: **high**
- screener note: ALLoRA addresses LoRA's dropout, initialization and learning-rate flaws; core PEFT method.
- abstract: Low-Rank Adaptation (LoRA) is the bread and butter of Large Language Model (LLM) finetuning. LoRA learns an additive low-rank perturbation, $AB$, of a pretrained matrix parameter $W$ to align the model to a new task or dataset with $W+AB$. We identify three core limitations to LoRA for finetuning--a setting that employs limited amount of data and training steps. First, LoRA employs Dropout to prevent overfitting. We ...
- **verdict:**  agree

### 45. ALoRA: Allocating Low-Rank Adaptation for Fine-tuning Large Language Models
- `C-d743abf753` | 2024 | North American Chapter of the Association for Computational Linguistics | citations: 99 | confidence: **high**
- screener note: ALoRA allocates LoRA rank adaptively for downstream tasks; core PEFT method.
- abstract: Parameter-efficient fine-tuning (PEFT) is widely studied for its effectiveness and efficiency in the era of large language models. Low-rank adaptation (LoRA) has demonstrated commendable performance as a popular and representative method. However, it is implemented with a fixed intrinsic rank that might not be the ideal setting for the downstream tasks. Recognizing the need for more flexible downstream task adaptatio...
- **verdict:**  agree

### 46. APT: Adaptive Prefix-Tuning on Pretrained Models for Code Intelligence
- `C-495e9e0319` | 2024 | 2024 International Joint Conference on Neural Networks (IJCNN) | citations: 3 | confidence: **high**
- screener note: APT adaptive prefix-tuning for code intelligence; explicit PEFT method addressing full-parameter cost.
- abstract: In the field of code intelligence, pretrained models exhibit impressive performance. However, it is imperative to modify all model parameters and maintain full copies for various tasks. Moreover, the effectiveness of fine-tuning a pretrained model depends on the availability of data, which can be constrained in practical settings. Prefix-tuning, a novel approach in NLP for addressing the aforementioned issue, has dem...
- **verdict:** agree

### 47. APT: Adaptive Pruning and Tuning Pretrained Language Models for Efficient Training and Inference
- `C-6f497e04f2` | 2024 | arXiv | citations: 0 | confidence: **high**
- screener note: APT combines adaptive pruning and tuning of pretrained LMs for efficient training and inference; training-time efficiency is central.
- abstract: Fine-tuning and inference with large Language Models (LM) are generally known to be expensive. Parameter-efficient fine-tuning over pretrained LMs reduces training memory by updating a small number of LM parameters but does not improve inference efficiency. Structured pruning improves LM inference efficiency by removing consistent parameter blocks, yet often increases training memory and time. To improve both trainin...
- **verdict:** agree

### 48. AQLoRA: An Adaptive Quantization-Based Efficient Fine-Tuning Method for LLMs
- `C-c25ad5bd63` | 2024 | Springer | citations: 0 | confidence: **high**
- screener note: AQLoRA adaptive quantization-based efficient fine-tuning for LLMs. No abstract, but the title names quantized efficient fine-tuning directly.
- abstract: _none available_
- **verdict:**  agree

### 49. ASLoRA: Adaptive Sharing Low-Rank Adaptation Across Layers
- `C-0826b1abbb` | 2024 | arXiv.org | citations: 5 | confidence: **high**
- screener note: ASLoRA shares low-rank matrices across layers to cut tunable parameters further; core PEFT method.
- abstract: As large language models (LLMs) grow in size, traditional full fine-tuning becomes increasingly impractical due to its high computational and storage costs. Although popular parameter-efficient fine-tuning methods, such as LoRA, have significantly reduced the number of tunable parameters, there is still room for further optimization. In this work, we propose ASLoRA, a cross-layer parameter-sharing strategy combining ...
- **verdict:**  agree

### 50. Accelerating Large Language Model Training with 4D Parallelism and Memory Consumption Estimator
- `C-cd2460dae2` | 2024 | arXiv.org | citations: 3 | confidence: **high**
- screener note: 4D parallelism with a memory consumption estimator for LLM training; training-time memory, block B3.
- abstract: In large language model (LLM) training, several parallelization strategies, including Tensor Parallelism (TP), Pipeline Parallelism (PP), Data Parallelism (DP), as well as Sequence Parallelism (SP) and Context Parallelism (CP), are employed to distribute model parameters, activations, and optimizer states across devices. Identifying the optimal parallelization configuration for each environment while avoiding GPU mem...
- **verdict:** agree

### 51. Accelerating Large Language Model Training with Hybrid GPU-based Compression
- `C-895f48dad7` | 2024 | IEEE/ACM International Symposium on Cluster, Cloud and Internet Computing | citations: 10 | confidence: **high**
- screener note: Hybrid GPU-based compression to accelerate LLM training across DP, TP and PP; training-time efficiency.
- abstract: Data Parallelism (DP), Tensor Parallelism (TP), and Pipeline Parallelism (PP) are the three strategies widely adopted to enable fast and efficient Large Language Model (LLM) training. However, these approaches rely on data-intensive communication routines to collect, aggregate, and re-distribute gradients, activations, and other important model information, which pose significant overhead. Co-designed with GPU-based ...
- **verdict:**  agree

### 52. Accelerating the Training of Large Language Models using Efficient Activation Rematerialization and Optimal Hybrid Parallelism
- `C-f1e87ba0bf` | 2024 | USENIX Annual Technical Conference | citations: 29 | confidence: **high**
- screener note: Activation rematerialization and hybrid parallelism for LLM training. No abstract, but the title names training-time activation memory directly.
- abstract: _none available_
- **verdict:** agree

### 53. Accurate LoRA-Finetuning Quantization of LLMs via Information Retention
- `C-392a797fca` | 2024 | arXiv (Cornell University) | citations: 190 | confidence: **high**
- screener note: IR-QLoRA improves LoRA-finetuning quantization of LLMs through information retention; core B1/B2 intersection.
- abstract: The LoRA-finetuning quantization of LLMs has been extensively studied to obtain accurate yet compact LLMs for deployment on resource-constrained hardware. However, existing methods cause the quantized LLM to severely degrade and even fail to benefit from the finetuning of LoRA. This paper proposes a novel IR-QLoRA for pushing quantized LLMs with LoRA to be highly accurate through information retention. The proposed I...
- **verdict:** agree

### 54. Accurate and Efficient Fine-Tuning of Quantized Large Language Models Through Optimal Balance
- `C-b63b6fb06a` | 2024 | arXiv.org | citations: 2 | confidence: **high**
- screener note: Fine-tuning of quantized LLMs balancing quantization against LoRA degradation; core B1/B2 intersection.
- abstract: Large Language Models (LLMs) have demonstrated impressive performance across various domains. However, the enormous number of model parameters makes fine-tuning challenging, significantly limiting their application and deployment. Existing solutions combine parameter quantization with Low-Rank Adaptation (LoRA), reducing memory usage but causing performance degradation. Additionally, converting fine-tuned models to l...
- **verdict:**  agree

---

## C. Low-confidence excludes (26) — the false-exclude risk

### 1. 2D Matryoshka Training for Information Retrieval
- `C-d3ba14dd77` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Matryoshka embedding training for IR. Targets representation efficiency, not LLM fine-tuning or adaptation cost; boundary call.
- abstract: 2D Matryoshka Training is an advanced embedding representation training approach designed to train an encoder model simultaneously across various layer-dimension setups. This method has demonstrated higher effectiveness in Semantic Text Similarity (STS) tasks over traditional training approaches when using sub-layers for embeddings. Despite its success, discrepancies exist between two published implementations, leadi...
- **verdict:**  agree

### 2. 6 LLM Fine-Tuning: Instruction and Parameter-Efficient Fine-Tuning (PEFT)
- `C-352115b844` | 2024 | Generative AI and LLMs: Natural Language Processing and Generative Adversarial Networks | citations: 0 | confidence: **low** | criterion: **Exclusion 6**
- screener note: '6 LLM Fine-Tuning: Instruction and PEFT' in 'Generative AI and LLMs', record type Books. On-topic but appears to be a textbook chapter rather than primary research. Excluded under exclusion 6 with low confidence; flag if book chapters are to count as archival.
- abstract: In artificial intelligence (AI) generating function the large language model plays an important role in various long data communication. Even though the system has pretrained language model, this large language model (LLM) is going to help the model according to the trained data in various analyses. This system is very useful in many fields like natural language processing, question answering, and GPT to produce bett...
- **verdict:** agree

### 3. 7B Fully Open Source Moxin-LLM/VLM -- From Pretraining to GRPO-based Reinforcement Learning Enhancement
- `C-cc47b7ec15` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Moxin-LLM open-source 7B release covering pretraining through GRPO. Model release, not an efficiency method; engages exclusion 1 in part.
- abstract: Recently, Large Language Models (LLMs) have undergone a significant transformation, marked by a rapid rise in both their popularity and capabilities. Leading this evolution are proprietary LLMs like GPT-4 and GPT-o1, which have captured widespread attention in the AI community due to their remarkable performance and versatility. Simultaneously, open-source LLMs, such as LLaMA, have made great contributions to the eve...
- **verdict:** agree

### 4. A Convex-optimization-based Layer-wise Post-training Pruner for Large Language Models
- `C-db2bb6e246` | 2024 | arXiv.org | citations: 2 | confidence: **low** | criterion: **Exclusion 2**
- screener note: FISTAPruner post-training pruning without retraining; compression for deployment rather than fine-tuning. Boundary against the quantization block.
- abstract: Pruning is a critical strategy for compressing trained large language models (LLMs), aiming at substantial memory conservation and computational acceleration without compromising performance. However, existing pruning methods often necessitate inefficient retraining for billion-scale LLMs or rely on heuristic methods such as the optimal brain surgeon framework, which degrade performance. In this paper, we introduce F...
- **verdict:** agree

### 5. A GEN AI Framework for Medical Note Generation
- `C-b9202c01b6` | 2024 | 2024 6th International Conference on Artificial Intelligence and Computer Applications (ICAICA) | citations: 15 | confidence: **low** | criterion: **Inclusion 1**
- screener note: MediNotes clinical note generation using LLMs and RAG; application, no stated efficiency method.
- abstract: The increasing administrative burden of medical documentation, particularly through Electronic Health Records (EHR), significantly reduces the time available for direct patient care and contributes to physician burnout. To address this issue, we propose MediNotes, an advanced generative AI framework designed to automate the creation of SOAP (Subjective, Objective, Assessment, Plan) notes from medical conversations. M...
- **verdict:** agree

### 6. A Generative Artificial Intelligence Using Multilingual Large Language Models for ChatGPT Applications
- `C-e870e12e58` | 2024 | Applied Sciences | citations: 35 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Multilingual generative AI for SMEs with limited hardware. Resource framing is deployment context, not a fine-tuning efficiency contribution.
- abstract: ChatGPT plays significant roles in the third decade of the 21st Century. Smart cities applications can be integrated with ChatGPT in various fields. This research proposes an approach for developing large language models using generative artificial intelligence models suitable for small- and medium-sized enterprises with limited hardware resources. There are many generative AI systems in operation and in development....
- **verdict:** agree

### 7. A Review on Large Language Models: Architectures, Applications, Taxonomies, Open Issues and Challenges
- `C-dad7bdb5b0` | 2024 | IEEE Access | citations: 737 | confidence: **low** | criterion: **Inclusion 1**
- screener note: General LLM review covering architectures and applications. Broad surveys touch efficiency, but efficiency is not the subject.
- abstract: Large Language Models (LLMs) recently demonstrated extraordinary capability, including natural language processing (NLP), language translation, text generation, question answering, etc. Moreover, LLMs are a new and essential part of computerized language processing, having the ability to understand complex verbal patterns and generate coherent and appropriate replies for the situation. Though this success of LLMs has...
- **verdict:** agree

### 8. A Survey of AI-Driven Mock Interviews Using GenAI and Machine Learning (InterviewX)
- `C-ac4974e674` | 2024 | 2024 4th International Conference on Ubiquitous Computing and Intelligent Information Systems (ICUIS) | citations: 7 | confidence: **low** | criterion: **Inclusion 1**
- screener note: AI-driven mock interview system using RAG and QLoRA. Uses an efficiency method but the subject is the application.
- abstract: With the accelerated demand for assessment tools that work efficiently and at scale, innovations in automated interviewing platforms have proliferated. In this research, InterviewX- a system enabled with artificial intelligence, works on RAG (Retrieval-Augmented Generation) and QLoRA (Quantized Low-Rank Adaptation). InterviewX aims to create an environment for an actual interview where domain-specific questions can b...
- **verdict:** agree

### 9. A Survey of Recent Backdoor Attacks and Defenses in Large Language Models
- `C-499e2b6b05` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Survey of backdoor attacks and defenses. Notes PEFT and outsourced training as context, but the subject is security.
- abstract: Large Language Models (LLMs), which bridge the gap between human language understanding and complex problem-solving, achieve state-of-the-art performance on several NLP tasks, particularly in few-shot and zero-shot settings. Despite the demonstrable efficacy of LLMs, due to constraints on computational resources, users have to engage with open-source language models or outsource the entire training process to third-p...
- **verdict:** agree

### 10. A Survey on Efficient Vision Transformers: Algorithms, Techniques, and Performance Benchmarking
- `C-97483d7353` | 2024 | IEEE Transactions on Pattern Analysis and Machine Intelligence | citations: 108 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Survey of efficient vision transformers. Efficiency-focused but non-language; fails the LLM boundary in criterion 2.
- abstract: Vision Transformer (ViT) architectures are becoming increasingly popular and widely employed to tackle computer vision applications. Their main feature is the capacity to extract global information through the self-attention mechanism, outperforming earlier convolutional neural networks. However, ViT deployment and performance have grown steadily with their size, number of trainable parameters, and operations. Furthe...
- **verdict:** agree

### 11. A review on different techniques used to combat the non-IID and heterogeneous nature of data in FL
- `C-1d53c81900` | 2024 | arXiv.org | citations: 17 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Review of non-IID techniques in federated learning; generic FL without an LLM component.
- abstract: Federated Learning (FL) is a machine-learning approach enabling collaborative model training across multiple decentralized edge devices that hold local data samples, all without exchanging these samples. This collaborative process occurs under the supervision of a central server orchestrating the training or via a peer-to-peer network. The significance of FL is particularly pronounced in industries such as healthcare...
- **verdict:**  agree

### 12. ABSTRACTIVE SUMMARIZATION OF INDIAN LEGAL DOCUMENTS USING T5 & QLoRA
- `C-6c1eb0b78f` | 2024 | International Education and Research Journal | citations: 3 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Legal document summarization with T5 and QLoRA; application. Record type is a conference abstract, which may also engage exclusion 6.
- abstract: This research project aims to develop an abstractive summarization system for Indian legal documents. The system leverages the power of the T5 transformer model, fine-tuned using Quantized Low-Rank Adaptation (QLoRA). The training data comprises two datasets, the Indian Legal Corpus (ILC) and IN-Abs, both containing court cases and their corresponding abstractive summaries.  The system is designed to accept legal tex...
- **verdict:** agree

### 13. ACT-MNMT Auto-Constriction Turning for Multilingual Neural Machine Translation
- `C-f203bcc7e7` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Auto-constriction turning for multilingual MT. Prompt-tuning is used as machinery for a translation contribution.
- abstract: Large language model (LLM) has achieved promising performance in multilingual machine translation tasks through zero/few-shot prompts or prompt-tuning. However, due to the mixture of multilingual data during the pre-training of LLM, the LLM-based translation models face the off-target issue in both prompt-based methods, including a series of phenomena, namely instruction misunderstanding, translation with wrong langu...
- **verdict:** agree

### 14. AFPQ: Asymmetric Floating Point Quantization for LLMs
- `C-844921a68e` | 2024 | arXiv | citations: 16 | confidence: **low** | criterion: **Exclusion 2**
- screener note: AFPQ asymmetric floating-point quantization to save memory and accelerate inference. Inference-side, but quantization of LLMs sits close to block B2.
- abstract: Large language models (LLMs) show great performance in various tasks, but face deployment challenges from limited memory capacity and bandwidth. Low-bit weight quantization can save memory and accelerate inference. Although floating-point (FP) formats show good performance in LLM quantization, they tend to perform poorly with small group sizes or sub-4 bits. We find the reason is that the absence of asymmetry in prev...
- **verdict:** agree

### 15. ALKAFI-LLAMA3: Fine-Tuning LLMs for Precise Legal Understanding in Palestine
- `C-5e62c547ae` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Fine-tuned Llama3 for Palestinian legal understanding; domain application.
- abstract: Large Language Models (LLMs) have demonstrated remarkable potential in diverse domains, yet their application in the legal sector, particularly in low-resource contexts, remains limited. This study addresses the challenges of adapting LLMs to the Palestinian legal domain, where political instability, fragmented legal frameworks, and limited AI resources hinder effective machine-learning applications. We present a fin...
- **verdict:** agree

### 16. ALPS: Improved Optimization for Highly Sparse One-Shot Pruning for Large Language Models
- `C-1f05dce50e` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Exclusion 2**
- screener note: ALPS one-shot pruning for LLMs without retraining; compression for deployment.
- abstract: The impressive performance of Large Language Models (LLMs) across various natural language processing tasks comes at the cost of vast computational resources and storage requirements. One-shot pruning techniques offer a way to alleviate these burdens by removing redundant weights without the need for retraining. Yet, the massive scale of LLMs often forces current pruning approaches to rely on heuristics instead of op...
- **verdict:** agree

### 17. AM-SAM: Automated Prompting and Mask Calibration for Segment Anything Model
- `C-7c56357288` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: AM-SAM automated prompting and mask calibration for SAM; vision segmentation quality, not adaptation cost.
- abstract: Segment Anything Model (SAM) has gained significant recognition in the field of semantic segmentation due to its versatile capabilities and impressive performance. Despite its success, SAM faces two primary limitations: (1) it relies heavily on meticulous human-provided prompts like key points, bounding boxes or text messages, which is labor-intensive; (2) the mask decoder's feature representation is sometimes inaccu...
- **verdict:** agree

### 18. APEER: Automatic Prompt Engineering Enhances Large Language Model Reranking
- `C-bd3e4af6ee` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: APEER automatic prompt engineering for reranking; prompt engineering rather than parameter-efficient tuning.
- abstract: Large Language Models (LLMs) have significantly enhanced Information Retrieval (IR) across various modules, such as reranking. Despite impressive performance, current zero-shot relevance ranking with LLMs heavily relies on human prompt engineering. Existing automatic prompt engineering algorithms primarily focus on language modeling and classification tasks, leaving the domain of IR, particularly reranking, underexpl...
- **verdict:** agree

### 19. APT-Pipe: A Prompt-Tuning Tool for Social Data Annotation using ChatGPT
- `C-d95b4fa30f` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: APT-Pipe prompt-tuning tool for ChatGPT annotation. 'Prompt tuning' here means prompt design, not a PEFT method.
- abstract: Recent research has highlighted the potential of LLM applications, like ChatGPT, for performing label annotation on social computing text. However, it is already well known that performance hinges on the quality of the input prompts. To address this, there has been a flurry of research into prompt tuning -- techniques and guidelines that attempt to improve the quality of prompts. Yet these largely rely on manual effo...
- **verdict:** agree

### 20. APTQ: Attention-aware Post-Training Mixed-Precision Quantization for Large Language Models
- `C-1e3dec9414` | 2024 | Design Automation Conference | citations: 50 | confidence: **low** | criterion: **Exclusion 2**
- screener note: APTQ post-training mixed-precision quantization for edge deployment; inference-side quantization.
- abstract: Large Language Models (LLMs) have greatly advanced the natural language processing paradigm. However, the high computational load and huge model sizes pose a grand challenge for deployment on edge devices. To this end, we propose APTQ (Attention-aware Post-Training Mixed-Precision Quantization) for LLMs, which considers not only the second-order information of each layer’s weights, but also, for the first time, the n...
- **verdict:** agree

### 21. ARB-LLM: Alternating Refined Binarizations for Large Language Models
- `C-2722016ce8` | 2024 | International Conference on Learning Representations | citations: 32 | confidence: **low** | criterion: **Exclusion 2**
- screener note: ARB-LLM binarization for LLM compression and deployment; inference-side compression.
- abstract: Large Language Models (LLMs) have greatly pushed forward advancements in natural language processing, yet their high memory and computational demands hinder practical deployment. Binarization, as an effective compression technique, can shrink model weights to just 1 bit, significantly reducing the high demands on computation and memory. However, current binarization methods struggle to narrow the distribution gap bet...
- **verdict:** agree

### 22. Abstract2Appendix: Academic Reviews Enhance LLM Long-Context Capabilities
- `C-35b1dc81d6` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Compares DPO against SFT for long-context capability. Fine-tuning methods compared for capability, not for resource cost.
- abstract: Large language models (LLMs) have shown remarkable performance across various tasks, yet their ability to handle long-context reading remains challenging. This study explores the effectiveness of leveraging high-quality academic peer review data for fine-tuning LLMs to enhance their long-context capabilities. We compare the Direct Preference Optimization (DPO) method with the Supervised Fine-Tuning (SFT) method, demo...
- **verdict:** agree

### 23. Accelerating Communication-Efficient Federated Multi-Task Learning With Personalization and Fairness
- `C-92ac912ead` | 2024 | IEEE Transactions on Parallel and Distributed Systems | citations: 6 | confidence: **low** | criterion: **Inclusion 1**
- screener note: Communication-efficient federated multi-task learning; efficiency is real but the setting is generic FL, not LLM adaptation.
- abstract: Federated learning techniques provide a promising framework for collaboratively training a machine learning model without sharing users’ data, and delivering a security solution to guarantee privacy during the model training of IoT devices. Nonetheless, challenges posed by data heterogeneity and communication resource constraints make it difficult to develop an efficient federated learning algorithm in terms of the l...
- **verdict:** agree

### 24. Accelerator Design using 3D Stacked Capacitorless DRAM for Large Language Models
- `C-68bbd2c920` | 2024 | International Conference on Artificial Intelligence Circuits and Systems | citations: 9 | confidence: **low** | criterion: **Inclusion 1**
- screener note: 3D stacked capacitorless DRAM accelerator for LLMs; hardware memory technology rather than a training method.
- abstract: Large language models (LLMs) have been immensely useful for natural language processing tasks. However, the current model sizes are increasing exponentially, along with generating large amounts of intermediate data. Here, we propose to use the capacitorless 3D stackable DRAM, which is an emerging memory enabling scaling of DRAM in the vertical direction like 3D NAND Flash. A 3D DRAM can store much larger LLMs compare...
- **verdict:** agree

### 25. Accumulator-Aware Post-Training Quantization for Large Language Models
- `C-5e80ec2790` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Exclusion 2**
- screener note: Accumulator-aware post-training quantization for LLMs; inference platforms by its own framing.
- abstract: When quantizing weights and activations to increasingly narrower representations, the cost of additions begins to dominate that of multiplications in multiply-accumulate (MAC) units. Recent studies show that reducing addition costs via low-precision accumulation improves throughput, power, and area across inference platforms, albeit with an increased risk of overflow. Accumulator-aware quantization research has so fa...
- **verdict:** agree

### 26. Activation Sparsity Opportunities for Compressing General Large Language Models
- `C-8c94f2c7a6` | 2024 | arXiv | citations: 0 | confidence: **low** | criterion: **Exclusion 2**
- screener note: Activation sparsity to compress LLMs for edge deployment; inference-side compression.
- abstract: Deploying local AI models, such as Large Language Models (LLMs), to edge devices can substantially enhance devices' independent capabilities, alleviate the server's burden, and lower the response time. Owing to these tremendous potentials, many big tech companies have released several lightweight Small Language Models (SLMs) to bridge this gap. However, we still have huge motivations to deploy more powerful (LLMs) AI...
- **verdict:** agree

---

## D. Sampled confident excludes (20 of 70, seed 1)

### 1. "I've Heard of You!": Generate Spoken Named Entity Recognition Data for Unseen Entities
- `C-09349fa197` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Spoken NER data generation; no fine-tuning efficiency component.
- **verdict:** agree

### 2. A Causal World Model Underlying Next Token Prediction: Exploring GPT in a Controlled Environment
- `C-4a74c99c49` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Causal interpretation of GPT attention; interpretability.
- **verdict:** agree

### 3. A Comprehensive Guide to Explainable AI: From Classical Models to LLMs
- `C-a5d3dcd65c` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Explainable AI guide; XAI, not efficiency. Also book-form.
- **verdict:** agree

### 4. A Hopfieldian View-based Interpretation for Chain-of-Thought Reasoning
- `C-7c5e6a61c5` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Hopfieldian interpretation of chain-of-thought; interpretability.
- **verdict:** agree

### 5. A LLM-Based Ranking Method for the Evaluation of Automatic Counter-Narrative Generation
- `C-0597a44052` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: LLM-based ranking for counter-narrative evaluation; evaluation method.
- **verdict:**  agree

### 6. A Large Sensor Foundation Model Pretrained on Continuous Glucose Monitor Data for Diabetes Management
- `C-3a78bca898` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Glucose-monitoring sensor foundation model; pretraining in a non-language domain.
- **verdict:** agree

### 7. A Novel Pretrained General-purpose Vision Language Model for the Vietnamese Language
- `C-24ca97e02f` | 2024 | ACM Transactions on Asian and Low-Resource Language Information Processing | citations: 2 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Vietnamese vision-language model; general-purpose model, no efficiency method.
- **verdict:** agree

### 8. A Practical Examination of AI-Generated Text Detectors for Large Language Models
- `C-2395aed41c` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Evaluation of AI-generated text detectors; no efficiency component.
- **verdict:** agree

### 9. A Simple and Effective $L_2$ Norm-Based Strategy for KV Cache Compression
- `C-ea24cc2dbc` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Exclusion 2**
- screener note: KV cache compression via L2 norm; inference-time memory only.
- **verdict:** agree

### 10. A Simple but Effective Approach to Improve Structured Language Model Output for Information Extraction
- `C-188b1505a7` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Structured output for information extraction; application.
- **verdict:** agree

### 11. A Survey of Hallucination Problems Based on Large Language Models
- `C-c301cc14c3` | 2024 | Applied and Computational Engineering | citations: 29 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Survey of LLM hallucination; not efficiency.
- **verdict:** agree

### 12. A Survey on Large Language Model Acceleration based on KV Cache Management
- `C-7423c9c736` | 2024 | Trans. Mach. Learn. Res. | citations: 138 | confidence: **high** | criterion: **Exclusion 2**
- screener note: Survey of KV cache management for LLM acceleration; inference-time.
- **verdict:** agree

### 13. A Training-free Sub-quadratic Cost Transformer Model Serving Framework With Hierarchically Pruned Attention
- `C-1b6cc852c6` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Exclusion 2**
- screener note: Hierarchically pruned attention for model serving; inference-time, explicitly training-free.
- **verdict:** agree

### 14. A Two-dimensional Zero-shot Dialogue State Tracking Evaluation Method using GPT-4
- `C-481197185d` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Dialogue state tracking evaluation with GPT-4; evaluation method.
- **verdict:** agree

### 15. A Zero-Shot Open-Vocabulary Pipeline for Dialogue Understanding
- `C-ff56bfc9fe` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Zero-shot dialogue understanding pipeline; application.
- **verdict:** agree

### 16. A survey of safety and trustworthiness of large language models through the lens of verification and validation
- `C-47883c11f5` | 2024 | Artificial Intelligence Review | citations: 115 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Survey of LLM safety and trustworthiness; not efficiency.
- **verdict:** agree

### 17. ABQ-LLM: Arbitrary-Bit Quantized Inference Acceleration for Large Language Models
- `C-d8dac2fe98` | 2024 | AAAI Conference on Artificial Intelligence | citations: 36 | confidence: **high** | criterion: **Exclusion 2**
- screener note: ABQ-LLM arbitrary-bit quantized inference acceleration; inference-only by title and abstract.
- **verdict:** agree

### 18. AER-LLM: Ambiguity-aware Emotion Recognition Leveraging Large Language Models
- `C-c173e827d9` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Ambiguity-aware emotion recognition with LLMs; application.
- **verdict:** agree

### 19. AM2DN-FL: Adaptive Malicious Model Detection in Non-IID Data Using Federated Learning for IoT System
- `C-8a1c42b9b1` | 2024 | Global Communications Conference | citations: 2 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Malicious model detection in IoT federated learning; security, no LLM.
- **verdict:** agree

### 20. APT: Architectural Planning and Text-to-Blueprint Construction Using Large Language Models for Open-World Agents
- `C-795ba75953` | 2024 | arXiv | citations: 0 | confidence: **high** | criterion: **Inclusion 1**
- screener note: Architectural planning for Minecraft agents; application sharing the APT acronym.
- **verdict:** agree

