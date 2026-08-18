# Reference Corrections

**Generated:** 2026-07-21T21:48:22Z  
**Updated:** 2026-08-17 (manuscript upgrades applied; yang2025 is IJCAI **2025**)  
**Protocol:** v1.1 venue check (OpenReview + Crossref + arXiv)  
**Corpus size:** 42 originally; cited corpus is **55** after the 2026-08-17 insertion

Statuses: `UPGRADED` (preprint → published), `confirmed_preprint`, `confirmed_published`, `corrected` (metadata fix), plus reviewed-and-rejected candidates.

## Summary

- UPGRADED (applied): **3** — dao2023, wang2024, yang2025
- Reviewed and REJECTED (kept as manuscript currently has them): **2** —
  lin2024 (MLSys 2024 is correct; GetMobile is a secondary short-form
  venue, not a replacement), bayati2023 (ARR submission is not a
  publication status; no confirmed acceptance found)
- confirmed_preprint: **7** (unchanged, now includes bayati2023's
  disposition explicitly)
- other (confirmed_published, no change needed): **30**

## Upgrades (applied)

### dao2023
- **Title:** FlashAttention-2: Faster attention with better parallelism and work partitioning
- **Manuscript venue (now):** Proceedings of the International Conference on Learning Representations (ICLR), 2024
- **Verified venue:** ICLR 2024 poster
- **Verified DOI:** None
- **Notes:** OpenReview venue: ICLR 2024 poster
- **Status:** UPGRADED (applied 2026-08-17; in-text year 2024)

### wang2024
- **Title:** Parameter-efficient fine-tuning in large models: A survey of methodologies
- **Manuscript venue (now):** Artificial Intelligence Review, 58, 227 (2025)
- **Verified venue:** Artificial Intelligence Review / 2025 / journal-article
- **Verified DOI:** 10.1007/s10462-025-11236-4
- **Notes:** Crossref published match: Artificial Intelligence Review / 2025 / journal-article
- **Crossref authors:** Wang, Luping; Chen, Sheng; Jiang, Linnan; Pan, Shu; Cai, Runze; Yang, Sen; Yang, Fei
- **Status:** UPGRADED (applied 2026-08-17; in-text year 2025; published title adds “language”)

### yang2025
- **Title:** Federated low-rank adaptation for foundation models: A survey
- **Manuscript venue (now):** IJCAI 2025, 10779–10787, DOI 10.24963/ijcai.2025/1196
- **Verified venue:** Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence (IJCAI 2025)
- **Verified DOI:** 10.24963/ijcai.2025/1196
- **Notes:** Primary source is IJCAI **2025** (Montreal; pages 10779–10787). The earlier Crossref hit on `ijcai.2024/1196` was a year-path collision and must not be used.
- **Status:** UPGRADED (applied 2026-08-17; venue year is 2025, not 2024)

## Reviewed and REJECTED

### bayati2023 — REJECTED upgrade, keep as confirmed_preprint

- **Title:** FlexLoRA: Flexible low rank adaptation for large language models
- **Manuscript venue (current):** arXiv preprint arXiv:2310.08151
- **OpenReview finding:** ACL ARR 2024 December Submission
- **Crossref candidate found:** Proceedings of the 63rd Annual Meeting of
  the ACL (2025), authors Wei/Shu/He/Yu — REJECTED at generation time due
  to author mismatch.
- **Decision:** REJECTED. "ARR Submission" is not a publication status.
  ACL Rolling Review submission records indicate a paper entered that
  review cycle, not that it was accepted or published. No confirmed
  acceptance was found for this title under the Bayati/Lin/Zeng/Yin
  author list at any venue. External citations to "FlexLoRA" in the
  federated-LoRA literature attribute it inconsistently (some as
  "Bai et al., 2024"), which further suggests the citation record for
  this specific paper is unsettled.
- **Status:** confirmed_preprint (no change from manuscript). Revisit if
  a clear, author-matched acceptance record is found later.

### lin2024 — REJECTED upgrade, keep as-is

- **Title:** AWQ: Activation-aware weight quantization for LLM compression and acceleration
- **Manuscript venue (current, correct):** Proceedings of Machine Learning and Systems (MLSys 2024)
- **Crossref candidate found:** GetMobile: Mobile Computing and Communications, DOI 10.1145/3714983.3714987
- **Decision:** REJECTED. This paper has two legitimate venues: a short-form
  version in GetMobile and the full paper at MLSys 2024, where it won the
  Best Paper Award. The manuscript's existing MLSys citation is the
  correct, primary academic venue and must be kept. Do not apply the
  GetMobile DOI as a "verified" replacement.
- **Status:** confirmed_published (no change from manuscript)

## Other OpenReview candidate (not in Phase 6 apply list)

### zhang2024
- **Title:** FLoRA: Federated fine-tuning large language models with heterogeneous low-rank adaptations
- **Manuscript venue:** arXiv preprint arXiv:2409.05976
- **Verified venue (OpenReview):** NeurIPS 2024
- **Verified DOI:** None
- **Notes:** Crossref candidate rejected (author mismatch): Advances in Neural Information Processing Systems 37 / 2024 / proceedings-article / Wang/Shen/He et al. OpenReview venue: NeurIPS 2024. Left for human confirmation; not in the Phase 6 applied-upgrade list from the Phase 2 closure corrections.
- **Crossref authors:** Wang, Ziyao; Shen, Zheyu; He, Yexiao; Sun, Guoheng; Wang, Hongyi; Lyu, Lingjuan; Li, Ang

## All HIGH-priority preprint checks

- `bayati2023` — **confirmed_preprint** (REJECTED ARR upgrade) — arXiv preprint arXiv:2310.08151
- `chen2016` — **confirmed_preprint** — arXiv preprint arXiv:1604.06174
- `dao2023` — **UPGRADED** — ICLR 2024 poster
- `gong2024` — **confirmed_preprint** — arXiv preprint arXiv:2409.16694
- `hayou2024` — **confirmed_preprint** — arXiv preprint arXiv:2402.12354
- `hu2021` — **confirmed_preprint** — arXiv preprint arXiv:2106.09685
- `li2025` — **confirmed_preprint** — arXiv preprint arXiv:2501.03035
- `shoeybi2019` — **confirmed_preprint** — arXiv preprint arXiv:1909.08053
- `wang2024` — **UPGRADED** — Artificial Intelligence Review / 2025 / journal-article
- `xu2023` — **confirmed_preprint** — arXiv preprint arXiv:2312.12148
- `yang2025` — **UPGRADED** — IJCAI 2025 (DOI 10.24963/ijcai.2025/1196; the 2024 DOI was a false match)
- `zhang2024` — **OpenReview candidate (not applied)** — NeurIPS 2024

## Full table

| key | status | manuscript venue | verified venue | verified DOI |
|---|---|---|---|---|
| abadi2016 | confirmed_published | Proceedings of the 2016 ACM SIGSAC Confe | Proceedings of the 2016 ACM SIGSAC Confe | 10.1145/2976749.2978318 |
| bayati2023 | confirmed_preprint | arXiv preprint arXiv:2310.08151 | arXiv preprint arXiv:2310.08151 |  |
| chen2016 | confirmed_preprint | arXiv preprint arXiv:1604.06174 | arXiv preprint arXiv:1604.06174 |  |
| dao2023 | UPGRADED | arXiv preprint arXiv:2307.08691 | ICLR 2024 poster |  |
| dao2022 | confirmed_published | Advances in Neural Information Processin | Advances in Neural Information Processin | 10.52202/068431-1189 |
| dettmers2023 | confirmed_published | Advances in Neural Information Processin | Advances in Neural Information Processin | 10.52202/075280-0441 |
| frantar2023 | confirmed_published | Proceedings of the International Confere | Proceedings of the International Confere |  |
| gong2024 | confirmed_preprint | arXiv preprint arXiv:2409.16694 | arXiv preprint arXiv:2409.16694 |  |
| hayou2024 | confirmed_preprint | arXiv preprint arXiv:2402.12354 | arXiv preprint arXiv:2402.12354 |  |
| he2022 | confirmed_published | Proceedings of the International Confere | Proceedings of the International Confere |  |
| houlsby2019 | confirmed_published | Proceedings of the 36th International Co | Proceedings of the 36th International Co |  |
| hu2021 | confirmed_preprint | arXiv preprint arXiv:2106.09685 | arXiv preprint arXiv:2106.09685 |  |
| huang2019 | confirmed_published | Advances in Neural Information Processin | Advances in Neural Information Processin |  |
| jacob2018 | confirmed_published | Proceedings of the IEEE Conference on Co | 2018 IEEE/CVF Conference on Computer Vis | 10.1109/cvpr.2018.00286 |
| jin2024 | confirmed_published | Findings of the Association for Computat | Findings of the Association for Computat | 10.18653/v1/2024.findings-acl.726 |
| kirkpatrick2017 | confirmed_published | Proceedings of the National Academy of S | Proceedings of the National Academy of S | 10.1073/pnas.1611835114 |
| kopiczko2024 | confirmed_published | Proceedings of the International Confere | Proceedings of the International Confere |  |
| lester2021 | confirmed_published | Proceedings of the 2021 Conference on Em | Proceedings of the 2021 Conference on Em | 10.18653/v1/2021.emnlp-main.243 |
| li2021 | confirmed_published | Proceedings of the 59th Annual Meeting o | Proceedings of the 59th Annual Meeting o | 10.18653/v1/2021.acl-long.353 |
| li2025 | confirmed_preprint | arXiv preprint arXiv:2501.03035 | arXiv preprint arXiv:2501.03035 |  |
| lin2024 | confirmed_published | Proceedings of Machine Learning and Syst | Proceedings of Machine Learning and Syst |  |
| liu2022 | confirmed_published | Advances in Neural Information Processin | Advances in Neural Information Processin | 10.52202/068431-0142 |
| liu2024 | confirmed_published | Proceedings of the 41st International Co | Proceedings of the 41st International Co |  |
| loshchilov2019 | confirmed_published | Proceedings of the International Confere | Proceedings of the International Confere |  |
| mahabadi2021 | confirmed_published | Proceedings of the 59th Annual Meeting o | Proceedings of the 59th Annual Meeting o | 10.18653/v1/2021.acl-long.47 |
| mcmahan2017 | confirmed_published | Proceedings of the 20th International Co | Proceedings of the 20th International Co |  |
| micikevicius2018 | confirmed_published | Proceedings of the International Confere | Proceedings of the International Confere |  |
| pfeiffer2020 | confirmed_published | Proceedings of the 16th Conference of th | Proceedings of the 16th Conference of th | 10.18653/v1/2021.eacl-main.39 |
| rafailov2023 | confirmed_published | Advances in Neural Information Processin | Advances in Neural Information Processin | 10.52202/075280-2338 |
| rajbhandari2020 | confirmed_published | Proceedings of the International Confere | SC20: International Conference for High  | 10.1109/sc41405.2020.00024 |
| ren2021 | confirmed_published | Proceedings of the 2021 USENIX Annual Te | Proceedings of the 2021 USENIX Annual Te |  |
| rolnick2019 | confirmed_published | Advances in Neural Information Processin | Advances in Neural Information Processin |  |
| shoeybi2019 | confirmed_preprint | arXiv preprint arXiv:1909.08053 | arXiv preprint arXiv:1909.08053 |  |
| sun2022 | confirmed_published | Proceedings of the ACM Web Conference (W | Proceedings of the ACM Web Conference 20 | 10.1145/3485447.3511942 |
| vaswani2017 | confirmed_published | Advances in Neural Information Processin | Advances in Neural Information Processin |  |
| wang2024 | UPGRADED | arXiv preprint arXiv:2410.19878 | Artificial Intelligence Review / 2025 /  | 10.1007/s10462-025-11236-4 |
| xiao2023 | confirmed_published | Proceedings of the 40th International Co | Proceedings of the 40th International Co |  |
| xu2023 | confirmed_preprint | arXiv preprint arXiv:2312.12148 | arXiv preprint arXiv:2312.12148 |  |
| yang2025 | UPGRADED | arXiv preprint arXiv:2505.13502 | IJCAI 2025 (not 2024) | 10.24963/ijcai.2025/1196 |
| zaken2022 | confirmed_published | Proceedings of the 60th Annual Meeting o | Proceedings of the 60th Annual Meeting o | 10.18653/v1/2022.acl-short.1 |
| zhang2024 | confirmed_preprint | arXiv preprint arXiv:2409.05976 | arXiv preprint arXiv:2409.05976 |  |
| zhang2023 | confirmed_published | Proceedings of the International Confere | Proceedings of the International Confere |  |
