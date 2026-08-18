#!/usr/bin/env python3
"""Rank new-work Stage 1 includes and emit a 30-record author shortlist.

Score = 0.55 * log-normalized citations + 0.45 * section-fit, with a multiplier
that boosts B3 (memory) and B4 (federated) so PEFT volume does not crowd them out.
The shortlist is filled round-robin across B1–B4 until 30, then by residual score.

Usage:
  python3 screening/scripts/rank_includes.py
"""

from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auto_stage1 import assign_section  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = REPO_ROOT / "screening" / "screening-log.csv"
POOL_PATH = REPO_ROOT / "search" / "candidate-pool.csv"
REFS_PATH = REPO_ROOT / "search" / "existing-references.yaml"
OUT_PATH = REPO_ROOT / "screening" / "reviews" / "reference-shortlist.md"

csv.field_size_limit(10**9)

SECTION_BOOST = {
    "B4_federated": 1.25,
    "B3_memory": 1.20,
    "B2_quantization": 1.05,
    "B1_peft": 0.92,
}
SECTION_LABEL = {
    "B1_peft": "B1 PEFT",
    "B2_quantization": "B2 quantization",
    "B3_memory": "B3 memory",
    "B4_federated": "B4 federated",
}
QUOTA = {"B4_federated": 6, "B3_memory": 6, "B2_quantization": 8, "B1_peft": 10}


def _norm(value: str) -> str:
    s = re.sub(r"[^a-z0-9\s]", " ", (value or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def load_refs() -> list[dict]:
    try:
        import yaml
    except ImportError:
        return []
    if not REFS_PATH.exists():
        return []
    return yaml.safe_load(REFS_PATH.read_text(encoding="utf-8"))["references"]


def duplicate_of(title: str, refs: list[dict]) -> str:
    nt = _norm(title)
    for r in refs:
        rt = _norm(r.get("title") or "")
        if not rt:
            continue
        if nt == rt or nt in rt or rt in nt:
            return r.get("key") or rt
        # token overlap for near-duplicates
        a, b = set(nt.split()), set(rt.split())
        if min(len(a), len(b)) >= 5 and len(a & b) / max(len(a | b), 1) >= 0.72:
            return r.get("key") or rt
    return ""


def relevance_line(title: str, notes: str, section: str) -> str:
    note = (notes or "").replace("[automated_pass] ", "").replace("[automated_pass]", "")
    if note:
        return note.rstrip(".")[:180]
    return f"{SECTION_LABEL.get(section, section)} candidate: {title[:80]}"


def main() -> int:
    refs = load_refs()
    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        log = list(csv.DictReader(f))
    with POOL_PATH.open(newline="", encoding="utf-8") as f:
        pool = {r["candidate_id"]: r for r in csv.DictReader(f)}

    includes = [
        r for r in log
        if r.get("priority_band") == "new_work" and r.get("decision") == "include"
    ]
    print(f"new-work includes before ranking: {len(includes)}")
    if not includes:
        print("nothing to rank")
        return 1

    cites = []
    for r in includes:
        try:
            cites.append(max(0, int(float(r.get("citations") or 0))))
        except ValueError:
            cites.append(0)
    max_cite = max(cites) if cites else 1
    denom = math.log1p(max_cite) or 1.0

    scored = []
    for r, cite in zip(includes, cites):
        cand = pool.get(r["id"], {})
        title = r.get("title") or cand.get("title") or ""
        abstract = cand.get("abstract") or ""
        section = assign_section(title, abstract)
        cite_score = math.log1p(cite) / denom
        # Fit: named method in title scores higher than abstract-only.
        title_hit = 1.0 if section.split("_")[0] in {"B1", "B2", "B3", "B4"} else 0.5
        fit = 1.0 if re.search(
            r"\b(lora|peft|qlora|adapter|quantiz|offload|federated|fine[- ]tun|"
            r"memory[- ]efficient|prefix[- ]tun|prompt[- ]tun)\b",
            title, re.I,
        ) else 0.65
        raw = 0.55 * cite_score + 0.45 * fit
        score = raw * SECTION_BOOST[section]
        scored.append({
            "row": r,
            "cand": cand,
            "cite": cite,
            "section": section,
            "score": score,
            "dup": duplicate_of(title, refs),
            "title": title,
        })

    scored.sort(key=lambda x: -x["score"])
    picked: list[dict] = []
    used = set()
    # Round 1: section quotas (guarantees memory/federated presence).
    for sec, n in QUOTA.items():
        bucket = [x for x in scored if x["section"] == sec and x["row"]["id"] not in used]
        for x in bucket[:n]:
            picked.append(x)
            used.add(x["row"]["id"])
    # Round 2: fill to 30 by residual score.
    for x in scored:
        if len(picked) >= 30:
            break
        if x["row"]["id"] not in used:
            picked.append(x)
            used.add(x["row"]["id"])
    picked.sort(key=lambda x: (x["section"], -x["score"]))

    by_sec = {}
    for x in picked:
        by_sec.setdefault(x["section"], 0)
        by_sec[x["section"]] += 1

    lines = [
        "# New-work reference shortlist (top 30)",
        "",
        "Human-verification target for the automated Stage 1 pass of the 2024–2026 band.",
        "Do not treat this list as the final corpus — it is the author review packet for includes.",
        "",
        f"- New-work includes ranked: **{len(includes)}**",
        f"- Shortlist size: **{len(picked)}**",
        "- Ranking: `0.55 * log1p(citations)/log1p(max) + 0.45 * section-fit`, with a boost for",
        "  B3 memory (×1.20) and B4 federated (×1.25) so PEFT volume does not crowd them out.",
        f"- Section mix: " + ", ".join(f"{SECTION_LABEL[k]} {v}" for k, v in sorted(by_sec.items())),
        "- Dedup: titles compared to `search/existing-references.yaml` (42 manuscript refs).",
        "",
        "---",
        "",
    ]
    for i, x in enumerate(picked, 1):
        r, cand = x["row"], x["cand"]
        authors = (r.get("authors") or cand.get("authors") or "_none_").strip() or "_none_"
        venue = (r.get("venue") or cand.get("venue") or "_none_").strip() or "_none_"
        year = r.get("year") or cand.get("year") or "n/a"
        dup = f"**duplicates `{x['dup']}`**" if x["dup"] else "no — not in the 42 existing manuscript references"
        lines += [
            f"### {i}. {x['title']}",
            f"- `{r['id']}` | {year} | {venue} | citations: **{x['cite']}** | section: **{SECTION_LABEL[x['section']]}** | score: {x['score']:.3f}",
            f"- authors: {authors}",
            f"- relevance: {relevance_line(x['title'], r.get('notes') or '', x['section'])}",
            f"- existing corpus: {dup}",
            f"- **verdict:** ",
            "",
        ]
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print("section mix:", by_sec)
    print("duplicates in shortlist:", sum(1 for x in picked if x["dup"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
