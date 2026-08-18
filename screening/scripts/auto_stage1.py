#!/usr/bin/env python3
"""Automated Stage 1 screen of the new-work band under the encoded v1.3 rule.

Implements protocol/inclusion-exclusion.md notes on criteria 1, 2, 6 and exclusions 1–3, 6:
  * include only if the model is an LLM (or a language-model efficiency survey) AND
    the research question is the fine-tuning-efficiency method itself
  * vision/speech/graph/audio/multimodal fail criterion 2 unless the method is
    demonstrated on an LLM
  * domain applications that use PEFT/quantization as machinery fail inclusion 1

This pass is a single automated screen of pending new-work rows, not per-block
human verification. Provenance: screener=automated.

Usage:
  python3 screening/scripts/auto_stage1.py --dry-run          # classify, write nothing
  python3 screening/scripts/auto_stage1.py --self-test        # score against batch 001
  python3 screening/scripts/auto_stage1.py                   # write decisions JSON
  python3 screening/scripts/auto_stage1.py --apply           # write JSON and apply to log
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = REPO_ROOT / "screening" / "screening-log.csv"
POOL_PATH = REPO_ROOT / "search" / "candidate-pool.csv"
OUT_PATH = REPO_ROOT / "screening" / "decisions" / "stage1_new_work_automated.json"

csv.field_size_limit(10**9)

LLM_RE = re.compile(
    r"\b(large language model|language model|llms?|plms?|gpt(?:-\d)?|llama|mistral|"
    r"qwen|gemma|phi-\d|bert|t5|roberta|decoder-only|autoregressive)\b",
    re.I,
)
# Non-language model domains — criterion 2 fail unless LLM is clearly the subject.
NON_LLM_RE = re.compile(
    r"\b(vision transformers?|\bvits?\b|visual task|segment anything|\bsam\b|"
    r"stable diffusion|text-to-image|text to image|diffusion models?|"
    r"speech recognition|\basr\b|spoken language|audio transformers?|"
    r"audio prompt|acoustics recognition|graph transformers?|point cloud|"
    r"medical (?:image|visual)|3d segmentation|hvac\b|audio-visual|"
    r"multimodal learning|computer vision|microscopy|aerial land cover|"
    r"prompt tuning vision|sound separation|3d understanding|"
    r"vision-language|category discovery)\b",
    re.I,
)
PEFT_RE = re.compile(
    r"\b(lora|qlora|adalora|dora|vera|lokr|loha|ia3|bitfit|"
    r"low[- ]rank adaptation|low[- ]rank matrices|parameter[- ]efficient|peft|"
    r"prefix[- ]tuning|prompt[- ]tuning|p[- ]tuning|adapter(?:s)?|"
    r"soft prompt)\b",
    re.I,
)
QUANT_FT_RE = re.compile(
    r"\b(qlora|quantized fine[- ]tun|quantization[- ]aware training|qat\b|"
    r"fine[- ]tun\w* of quantized|quantization-based efficient fine[- ]tun)\b",
    re.I,
)
QUANT_ANY_RE = re.compile(r"\b(quantiz\w*|gptq|awq|smoothquant|low[- ]bit|int[48]|binariz\w*)\b", re.I)
MEMORY_RE = re.compile(
    r"\b(zero[- ]?offload|deepspeed|gradient checkpoint\w*|activation (?:re)?materializ|"
        r"memory[- ]efficient.{0,24}(fine[- ]tun|training)|optimizer state shard|"
    r"pipeline parallelism|tensor parallelism|4d parallelism|"
    r"hybrid parallelism|activation rematerialization|flashattention|"
    r"communication-overlapped|sharded (?:llm|optimizer))\b",
    re.I,
)
FED_RE = re.compile(
    r"\b(federated (?:fine[- ]tun|lora|peft|llm|learning)|"
    r"federated learning.{0,60}(lora|peft|llm|foundation model|language model))\b",
    re.I,
)
SURVEY_RE = re.compile(r"\b(survey|systematic review|taxonomy|critical review)\b", re.I)
INFERENCE_RE = re.compile(
    r"\b(post[- ]training quantiz|ptq\b|kv cache|inference(?:[- ]time)?|"
    r"model serving|edge deployment|inference acceleration|speculative decoding)\b",
    re.I,
)
FINETUNE_RE = re.compile(r"\b(fine[- ]tun\w*|peft|lora|adapter|prefix[- ]tun|prompt[- ]tun)\b", re.I)
PRETRAIN_ONLY_RE = re.compile(r"\b(pre[- ]?training|from[- ]scratch)\b", re.I)
BOOK_RE = re.compile(r"^(?:\d+\s+)?(?:chapter\s+\d|llm fine-tuning:)", re.I)
# Research question is the task/system, method is machinery (inclusion 1).
APP_RE = re.compile(
    r"\b(recommender systems?|recommendation|chatbot use case|note generation|"
    r"legal (?:understanding|documents)|mock interviews?|entity matching|"
    r"aspect-based sentiment|financial text classification|"
    r"named entity|clinical text|psychiatric interview|next location|"
    r"robot manipulation|autonomous (?:ai )?agents?|"
    r"machine translation|social data annotation|trusted execution|"
    r"tee\b|retrieval-augmented generation|rag system|"
    r"prompt[- ]tuning tool for|abstractive summarization|"
    r"accelerator design|capacitorless dram|radiology)\b",
    re.I,
)
METHOD_SUBJECT_RE = re.compile(
    r"\b((?:comprehensive )?evaluation of (?:parameter-efficient|quantization|peft)|"
    r"comparison of (?:llm )?fine[- ]?tun\w*|"
    r"comparative (?:analysis|evaluation) of (?:peft|lora|quantization|fine[- ]tun)|"
    r"a (?:note|study|survey) (?:on |of )(?:lora|peft|quantization|optimizations? for fine-tuning)|"
    r"study of optimizations for fine-tuning|"
    r"quantization strategies for large language|"
    r"quantization-based efficient fine[- ]tun|"
    r"parameter-efficient fine-tuning on)",
    re.I,
)
NON_TRANSFORMER_RE = re.compile(r"\b(spiking neural|mamba\b|lstm\b|convolutional neural)\b", re.I)


def _has(rx: re.Pattern[str], *parts: str) -> bool:
    return any(rx.search(p or "") for p in parts)


def assign_section(title: str, abstract: str) -> str:
    blob = f"{title} {abstract}"
    scores = {
        "B4_federated": 2 if FED_RE.search(blob) else 0,
        "B3_memory": 2 if MEMORY_RE.search(blob) else 0,
        "B2_quantization": 2 if QUANT_FT_RE.search(blob) else (1 if QUANT_ANY_RE.search(blob) else 0),
        "B1_peft": 2 if PEFT_RE.search(blob) else 0,
    }
    if QUANT_FT_RE.search(blob) and PEFT_RE.search(blob):
        scores["B2_quantization"] += 1
    best = max(scores, key=lambda k: (scores[k], {"B4_federated": 3, "B3_memory": 2, "B2_quantization": 1, "B1_peft": 0}[k]))
    return best if scores[best] else "B1_peft"


def classify(row: dict[str, str], cand: dict[str, str]) -> dict[str, Any]:
    """Return a decision dict for one record under the encoded v1.3 rule."""
    title = row.get("title") or cand.get("title") or ""
    abstract = (cand.get("abstract") or "")[:1200]
    venue = row.get("venue") or cand.get("venue") or ""
    work_type = (cand.get("work_type") or "").strip()
    blob = f"{title}\n{abstract}"

    cid = row["id"]
    base = {"id": cid}

    if work_type.lower() in {"books", "book", "book-chapter"} or BOOK_RE.search(title):
        venue_l = venue.lower()
        # OpenAlex tags some conference proceedings (e.g. ECAI) as book-chapter.
        if "proceeding" not in venue_l and "conference" not in venue_l:
            return {**base, "decision": "exclude", "exclusion_reason": "Exclusion 6",
                    "confidence": "high",
                    "notes": "[automated_pass] Textbook/tutorial chapter (exclusion 6)."}

    if _has(NON_TRANSFORMER_RE, title, abstract) and not _has(LLM_RE, title, abstract):
        return {**base, "decision": "exclude", "exclusion_reason": "Exclusion 3",
                "confidence": "high",
                "notes": "[automated_pass] Non-transformer architecture only (exclusion 3)."}

    llm = _has(LLM_RE, title, abstract) or bool(re.search(
        r"\b(small language model|language models?)\b", title, re.I))
    non_llm_title = bool(NON_LLM_RE.search(title))
    peft_title = bool(PEFT_RE.search(title))
    peft = peft_title or _has(PEFT_RE, abstract)
    quant_ft = _has(QUANT_FT_RE, title, abstract)
    quant_any = _has(QUANT_ANY_RE, title, abstract)
    memory = _has(MEMORY_RE, title, abstract)
    fed = _has(FED_RE, title, abstract) or (
        re.search(r"\bfederated\b", blob, re.I) and llm and (peft or _has(FINETUNE_RE, title, abstract))
    )
    survey = _has(SURVEY_RE, title)
    methodish = peft or quant_ft or memory or fed
    inference = _has(INFERENCE_RE, title, abstract)
    finetune = _has(FINETUNE_RE, title, abstract)
    method_is_subject = bool(METHOD_SUBJECT_RE.search(title))

    # Criterion 2: a non-language domain in the TITLE is the subject.
    if non_llm_title:
        return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 2",
                "confidence": "high",
                "notes": "[automated_pass] Vision/speech/graph/audio/multimodal is the subject (criterion 2)."}

    # Exclusion 2: inference-only. Skip for surveys (abstracts often mention inference).
    if not survey:
        if inference and not finetune and not quant_ft and not memory:
            return {**base, "decision": "exclude", "exclusion_reason": "Exclusion 2",
                    "confidence": "high",
                    "notes": "[automated_pass] Inference-time optimisation with no fine-tuning component (exclusion 2)."}
        if re.search(r"\bpost[- ]training\b", title, re.I) and re.search(r"\bquantiz", title, re.I):
            return {**base, "decision": "exclude", "exclusion_reason": "Exclusion 2",
                    "confidence": "high",
                    "notes": "[automated_pass] Post-training quantization in the title (exclusion 2)."}

    # Exclusion 1: pre-training only.
    if _has(PRETRAIN_ONLY_RE, title) and not finetune:
        return {**base, "decision": "exclude", "exclusion_reason": "Exclusion 1",
                "confidence": "high",
                "notes": "[automated_pass] Pre-training efficiency only (exclusion 1)."}

    # Surveys: efficiency surveys of language models are in; application and
    # general-ML surveys are out.
    if survey:
        title_method = bool(PEFT_RE.search(title) or QUANT_ANY_RE.search(title) or MEMORY_RE.search(title)
                           or FED_RE.search(title) or re.search(
                               r"\b(low[- ]bit|resource[- ]efficient|parameter[- ]efficient|"
                               r"fine[- ]?tun\w*|in-context learning|small language model)\b", title, re.I))
        if _has(APP_RE, title):
            return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 1",
                    "confidence": "high",
                    "notes": "[automated_pass] Application/task survey; method is not the subject (inclusion 1)."}
        if re.search(r"\b(kv cache|inference)\b", title, re.I):
            return {**base, "decision": "exclude", "exclusion_reason": "Exclusion 2",
                    "confidence": "high",
                    "notes": "[automated_pass] Inference-time survey (exclusion 2)."}
        if title_method and llm:
            return {**base, "decision": "include", "confidence": "high",
                    "notes": f"[automated_pass] Efficiency survey of language models ({assign_section(title, abstract)})."}
        if re.search(r"\bin-context learning\b", title, re.I):
            return {**base, "decision": "include", "confidence": "low",
                    "notes": "[automated_pass] In-context learning survey (adaptation without training; criterion 1)."}
        if re.search(r"\bsmall language model", title, re.I):
            return {**base, "decision": "include", "confidence": "low",
                    "notes": "[automated_pass] Small-language-model efficiency survey (criterion 2 survey route)."}
        if re.search(r"\bfederated\b", title, re.I) and re.search(r"\b(foundation model|language model|llm)\b", blob, re.I):
            return {**base, "decision": "include", "confidence": "high",
                    "notes": "[automated_pass] Federated training of foundation/language models (B4)."}
        if re.search(r"\b(peak performance|resource[- ]efficient)\b", title, re.I) and llm:
            return {**base, "decision": "include", "confidence": "low",
                    "notes": "[automated_pass] LLM performance/efficiency review; subject confirmed at Stage 2."}
        if methodish and not llm:
            return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 2",
                    "confidence": "high",
                    "notes": "[automated_pass] Survey is not LLM-specific (criterion 2)."}
        return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 1",
                "confidence": "high",
                "notes": "[automated_pass] Survey whose subject is not fine-tuning efficiency (inclusion 1)."}

    # Inclusion 1: domain application using a method as machinery.
    if _has(APP_RE, title) and not method_is_subject:
        return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 1",
                "confidence": "high",
                "notes": "[automated_pass] Research question is the task/system; efficiency method is machinery (inclusion 1)."}
    if re.search(r"\b(secure distributed|security architecture)\b", title, re.I) and not method_is_subject:
        return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 1",
                "confidence": "high",
                "notes": "[automated_pass] Security/systems architecture; method is incidental (inclusion 1)."}

    # Include: LLM + method is the contribution.
    if llm and methodish:
        return {**base, "decision": "include", "confidence": "high",
                "notes": f"[automated_pass] LLM fine-tuning-efficiency method ({assign_section(title, abstract)})."}
    # Named PEFT methods whose TITLE is the method (not a domain application).
    if peft_title and not non_llm_title:
        return {**base, "decision": "include", "confidence": "low",
                "notes": f"[automated_pass] Named PEFT method ({assign_section(title, abstract)})."}
    if method_is_subject and (llm or peft or quant_any):
        return {**base, "decision": "include", "confidence": "high",
                "notes": f"[automated_pass] Method evaluation/study ({assign_section(title, abstract)})."}
    if llm and quant_any and not inference:
        return {**base, "decision": "include", "confidence": "low",
                "notes": f"[automated_pass] LLM quantization method; training vs inference checked at Stage 2 ({assign_section(title, abstract)})."}
    # Memory/training systems for LLMs (block B3) may not say "fine-tune" in the title.
    if llm and memory:
        return {**base, "decision": "include", "confidence": "high",
                "notes": "[automated_pass] LLM training-time memory/parallelism (B3)."}
    if fed and llm:
        return {**base, "decision": "include", "confidence": "high",
                "notes": "[automated_pass] Federated fine-tuning of LLMs (B4)."}

    if methodish and not llm:
        return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 2",
                "confidence": "low",
                "notes": "[automated_pass] Efficiency method without an LLM subject (criterion 2)."}

    return {**base, "decision": "exclude", "exclusion_reason": "Inclusion 1",
            "confidence": "high",
            "notes": "[automated_pass] Not a fine-tuning-efficiency method paper (inclusion 1)."}


def load_log_and_pool() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        log = list(csv.DictReader(f))
    with POOL_PATH.open(newline="", encoding="utf-8") as f:
        pool = {r["candidate_id"]: r for r in csv.DictReader(f)}
    return log, pool


def pending_new_work(log: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        r for r in log
        if r.get("priority_band") == "new_work"
        and not (r.get("decision") or "").strip()
        and not (r.get("stage_reached") or "").endswith("not_screened")
    ]


def self_test(log: list[dict[str, str]], pool: dict[str, dict[str, str]]) -> int:
    """Score the classifier against batch 001's author-calibrated labels."""
    gold = [r for r in log if r.get("priority_band") == "new_work" and (r.get("decision") or "").strip()
            and r.get("screener") in {"llm_assisted", "author"}]
    if not gold:
        print("no labelled new_work rows to test against")
        return 1
    pred = {r["id"]: classify(r, pool.get(r["id"], {})) for r in gold}
    agree = sum(1 for r in gold if pred[r["id"]]["decision"] == r["decision"])
    fp = [r for r in gold if r["decision"] == "exclude" and pred[r["id"]]["decision"] == "include"]
    fn = [r for r in gold if r["decision"] == "include" and pred[r["id"]]["decision"] == "exclude"]
    print(f"batch 001 self-test: {agree}/{len(gold)} agree ({100*agree/len(gold):.1f}%)")
    print(f"  false includes (would keep an exclude): {len(fp)}")
    print(f"  false excludes (would drop an include): {len(fn)}")
    for label, rows in (("FALSE INCLUDE", fp[:8]), ("FALSE EXCLUDE", fn[:8])):
        if not rows:
            continue
        print(f"  {label}:")
        for r in rows:
            print(f"    {r['id']} gold={r['decision']} pred={pred[r['id']]['decision']} | {r['title'][:70]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Write JSON and apply to screening-log.csv")
    args = parser.parse_args()

    log, pool = load_log_and_pool()
    if args.self_test:
        return self_test(log, pool)

    pending = pending_new_work(log)
    print(f"pending new_work: {len(pending)}")
    decisions = [classify(r, pool.get(r["id"], {})) for r in pending]
    counts = Counter(d["decision"] for d in decisions)
    reasons = Counter(d.get("exclusion_reason") or "include" for d in decisions)
    print(f"classified: include={counts['include']} exclude={counts['exclude']}")
    print("criteria:", dict(reasons.most_common()))

    payload = {
        "batch": "new_work_automated",
        "band": "new_work",
        "screener": "automated",
        "note": (
            "Single automated Stage 1 pass of remaining new-work records under the encoded "
            "v1.3 rule (criterion 2 LLM-only + research-question test). Not per-block "
            "human-verified; human verification is applied to the ranked shortlist."
        ),
        "n_records": len(decisions),
        "decisions": decisions,
    }
    if args.dry_run:
        print("dry run — no files written")
        return 0

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    if args.apply:
        import subprocess
        rc = subprocess.call(
            ["python3", str(REPO_ROOT / "screening/scripts/apply_decisions.py"),
             "--file", str(OUT_PATH)],
        )
        return rc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
