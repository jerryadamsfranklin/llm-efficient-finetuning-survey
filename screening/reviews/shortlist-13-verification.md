# Primary-source verification: author-selected 13

Checked 2026-08-17 against OpenReview / NeurIPS / ICML / ICLR / ACL Anthology / ACM / Springer.
Pool strings are what `screening/reviews/reference-shortlist.md` currently shows; **cite the verified row**, not the pool row, if they differ.

Manuscript and bibliography were **not** edited in this pass.

## Scope flags (author call needed before insert)

These two are in the selected 13 and are in-scope *only if* the encoded rule is read the way the existing 42 already reads. They are not metadata typos.

### SLTrain (`C-1d12d2b919`) — Exclusion 1

NeurIPS 2024 paper, authors match. Title and abstract are **pretraining from scratch** (`W = BA + S` for LLM pretraining). The paper explicitly contrasts this with low-rank methods that work for fine-tuning but not pretraining. Strict Exclusion 1 (pre-training efficiency only) would drop it.

If dropped, B3 still has GaLore and AdaRankGrad. LISA (already selected as B1) is a memory-efficient **fine-tuning** method and can carry the third memory mention without adding a new record.

### SpinQuant (`C-15aa63fdab`) — Exclusion 2 vs existing B2

ICLR 2025. The paper is **post-training quantization** with learned rotations (weights, activations, KV cache). It is not QAT and not fine-tuning. The automated classifier included it because "post-training" is not in the title.

The manuscript already cites GPTQ, AWQ, and SmoothQuant, so B2 already covers PTQ. SpinQuant is the same class: a strong recent PTQ method, useful next to EfficientQAT if the PTQ-vs-QAT contrast is the goal. It would fail a strict “no inference-only” reading of Exclusion 2.

## Metadata corrections (must use verified strings)

| # | ID | Issue | Pool / shortlist | Verified |
|---|---|---|---|---|
| 3 | `C-a80f3cac0d` | truncated Scholar authors; truncated venue | `S Wang, L Yu, J Li`; `Advances in Neural Information …, 2024 -` | **Shaowen Wang, Linxi Yu, Jian Li**; NeurIPS 2024 |
| 5 | `C-65a13e7929` | second author; last-author hyphenation | Zhanying Shi; Chengzhong Xu | **Zhan Shi**; **Cheng-Zhong Xu**. NeurIPS 2024 oral. arXiv:2404.19245 |
| 8 | `C-c5f653cbd2` | none material | Pan, Liu, Diao, Pi, Zhang, Han, Zhang; NeurIPS | NeurIPS 2024. arXiv:2403.17919. Authors match |
| 12 | `C-392a797fca` | venue still arXiv | arXiv (Cornell University) | **ICML 2024 oral**. PMLR 235. arXiv:2402.05445. Authors match |
| 14 | `C-15aa63fdab` | year/venue | ICLR, 2024 | **ICLR 2025** (not 2024). Authors match. arXiv:2405.16406 |
| 15 | `C-93f716cbf0` | given name; venue still arXiv; was B2 | Fan-Xu Meng; arXiv | **Fanxu Meng**, Zhaohui Wang, Muhan Zhang; **NeurIPS 2024**. arXiv:2404.02948. PEFT init, not quantization |
| 16 | `C-3f09ccfe68` | year; one author | 2024 ACL; Kai-Chuang Zhang; Yu Qiao listed | **ACL 2025** (Vienna; anthology `2025.acl-long.498`, DOI 10.18653/v1/2025.acl-long.498). Authors: Mengzhao Chen, Wenqi Shao, Peng Xu, Jiahao Wang, Peng Gao, **Kaipeng Zhang**, Ping Luo. **Yu Qiao is not an author.** arXiv:2407.11062 |
| 19 | `C-57aa0c8ae7` | nickname in author string | Zhenyu (Allen) Zhang | **Zhenyu Zhang** (no Allen). ICML 2024 oral. arXiv:2403.03507. Covers pretraining **and** fine-tuning |
| 20 | `C-1d12d2b919` | scope, not names | NeurIPS 2024; authors match | NeurIPS 2024. arXiv:2406.02214. See Exclusion 1 flag |
| 23 | `C-05c157f898` | year | ICLR, 2024 | **ICLR 2025**. Authors match. arXiv:2410.17881. Fine-tuning **and** pretraining |
| 25 | `C-aaedc3bee8` | none material | ICLR 2024; Sun, Li, Li, Ding | ICLR 2024. Method name **FFA-LoRA**. arXiv:2403.12313 |
| 26 | `C-bc98faf889` | venue too short | Knowledge Discovery and Data Mining | **Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining**, 2024, pp. 6137–6147. DOI **10.1145/3637528.3671582**. Authors match. arXiv:2402.06954 |
| 29 | `C-64babd74d3` | volume year | 2024, Frontiers of Computer Science | First published **14 Dec 2024**; journal volume year **2025** (`Front. Comput. Sci. 19, 197605`). DOI **10.1007/s11704-024-40663-9**. Authors match. arXiv:2407.11046. Taxonomy includes a federated-LoRA section, so B4 placement is defensible; it also belongs on the existing-surveys table |

## Clean enough to insert (after the two scope calls)

All 13 exist, are LLM-side, and are not among the 42 keys. Use verified authors/venues above.

Recommended citation years if inserted:

- 2024: HydraLoRA, LISA, LoRA-GA, PiSSA, IR-QLoRA, GaLore, SLTrain (if kept), FFA-LoRA, OpenFedLLM
- 2025: EfficientQAT (ACL 2025), SpinQuant (ICLR 2025), AdaRankGrad (ICLR 2025)
- LoRA survey: 2024 or 2025 — protocol dates peer-reviewed work by publication date (14 Dec 2024); volume is 2025. Pick one and stay consistent.

## Related corpus note (not one of the 13)

Shortlist #27 FLoRA (`C-ddcb80926e`, Wang, Shen, He, et al., NeurIPS 2024) was dropped as a title duplicate of manuscript `zhang2024`. The NeurIPS author list is Wang et al.; the manuscript cites Zhang, Chen, Li, Ding, Xu, Tao on arXiv:2409.05976. `docs/reference-corrections.md` already flagged this author mismatch. Dropping #27 is correct (do not add a second FLoRA). When `zhang2024` is upgraded from preprint, the author string needs a primary-source check — it may be the Wang et al. paper under the wrong names.

## LoRA-XS correction (not in the 13)

`C-2237f357ff` overturned from Exclusion 6 to include. Klaudia Bałazy, Mohammadreza Banaei, Karl Aberer, Jacek Tabor. PEFT method (trainable `r×r` between frozen SVD factors). Pool venue is ECAI 2024; the camera-ready header seen in the EPFL copy says **ECAI 2025**. OpenAlex `work_type=book-chapter` on a conference paper is what triggered the automated exclude. Classifier now skips Exclusion 6 when the venue contains “conference”.
