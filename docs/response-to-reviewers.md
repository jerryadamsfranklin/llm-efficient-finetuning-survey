# Response to reviewers (PeerJ Computer Science draft)

**Manuscript:** Fine-Tuning Large Language Models in Resource-Constrained Environments: Methods and Trade-offs  
**Date:** 17 August 2026

This letter maps the revision to the review comments. Line-level page numbers will shift in the typeset PDF; section numbers refer to the revised manuscript.

---

## Reviewer 2 — coverage of 2024–2025 methods

We agree that the original 42-paper corpus under-represented work after 2023, especially in federated LoRA and training-time memory. We ran a structured, protocol-driven search of the 2024–2026 band (companion repository `llm-efficient-finetuning-survey`) and inserted **13** in-scope, non-duplicate papers. Authors, venues, and years were checked against primary sources. Each addition carries a one-clause critical mention (limitation, cost, or scope), not a bare citation:

| Section | Additions |
|---|---|
| I related surveys | Mao et al. (2025), LoRA survey with a federated-LoRA chapter |
| IV LoRA variants | HydraLoRA (Tian et al., 2024); LoRA-GA (Wang, Yu, & Li, 2024); PiSSA (Meng, Wang, & Zhang, 2024); LISA (Pan et al., 2024) |
| IV QLoRA | IR-QLoRA (Qin et al., 2024) |
| V PTQ vs QAT | SpinQuant (Liu et al., 2025) as recent PTQ; EfficientQAT (Chen et al., 2025) as a practical QAT recipe |
| VI memory | GaLore (Zhao et al., 2024); AdaRankGrad (Refael et al., 2025) — new §6.4 |
| VII federated | FlexLoRA (Bai et al., 2024); FFA-LoRA (Sun et al., 2024); OpenFedLLM (Ye et al., 2024) |

We did not add domain applications that merely use LoRA; the same inclusion test applied in screening. SLTrain was considered and dropped because it is pretraining-only.

The federated FlexLoRA discussion is now Bai et al. (2024), the NeurIPS heterogeneous-rank method. The manuscript still lists Bayati et al. (2023), a differently authored preprint that shares the FlexLoRA name; §7.3 now distinguishes the two so the federated claim is no longer attached to the wrong paper.

---

## Reviewer 2 — PTQ versus QAT

Section 5.3 now treats the choice as a decision among training budget, target bit-width, and accuracy tolerance. SpinQuant is placed on the PTQ side: learned rotations, no QAT run. EfficientQAT is placed on the QAT side as evidence that the “QAT means a full training run” objection is weaker than it was, while still costing far more than a GPTQ, AWQ, or SpinQuant calibration pass.

---

## Methodology / search transparency

Section II no longer claims a direct ACM Digital Library search. ACM content was retrieved via OpenAlex and Crossref. The coverage window is 1 January 2019 – 30 June 2026.

Title-and-abstract screening of the 2024–2026 band used a rule-encoded classifier calibrated to an author-resolved 150-record sample; human verification for that band was applied to a ranked shortlist of includes, not to every include. 2019–2023 records received a targeted confirmation pass, not an exhaustive screen. Unexamined records are reported as a separate count in the companion repository and are not described as screened. This is a structured, protocol-driven search, not a registered systematic review and not dual independent screening. The same wording appears in Section 10.4.

---

## Venue upgrades of existing citations

Three previously arXiv-cited items are now given their published venues, checked against primary sources:

- Dao, FlashAttention-2: **ICLR 2024** (in-text year updated to 2024).
- Wang et al., PEFT survey: ***Artificial Intelligence Review* 58:227 (2025)**, DOI 10.1007/s10462-025-11236-4. The published title adds “language” (“large language models”).
- Yang et al., FedLoRA survey: **IJCAI 2025**, DOI 10.24963/ijcai.2025/1196, pages 10779–10787. An earlier Crossref path (`ijcai.2024/1196`) was a year collision and was not used.

---

## Corpus size

The cited corpus is now **55** (original 42 + 13). Query strings, screening decisions, and PRISMA-style counts remain in the companion repository.

We thank the reviewers for the comments that drove this revision.
