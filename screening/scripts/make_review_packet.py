#!/usr/bin/env python3
"""Emit an author verification packet for a screened block (procedure §6, §6.1).

A packet carries everything §6 requires the author to see:
  * every `include`, which must be verified before the record reaches Stage 2
  * every `confidence: low` decision, whichever way it went
  * every `hold`
  * a seeded random sample of confident excludes, so false excludes surface too

The exclude sample is drawn with a recorded seed so the same packet can be regenerated.

Usage:
  python3 screening/scripts/make_review_packet.py \
      --decisions screening/decisions/stage1_new_work_001.json \
      --out screening/reviews/new-work-block-01.md --sample 20 --seed 1
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = REPO_ROOT / "screening" / "screening-log.csv"
POOL_PATH = REPO_ROOT / "search" / "candidate-pool.csv"

csv.field_size_limit(10**9)
ABSTRACT_CHARS = 420


def render(row: dict[str, str], pool: dict[str, dict[str, str]], n: int, show_abstract: bool) -> list[str]:
    cand = pool.get(row["id"], {})
    abstract = (cand.get("abstract") or "").strip().replace("\n", " ")
    reason = row.get("exclusion_reason") or ""
    head = f"### {n}. {row['title']}"
    meta = (f"- `{row['id']}` | {row['year'] or 'n/a'} | {row['venue'] or 'no venue'} "
            f"| citations: {row['citations'] or '0'} | confidence: **{row['confidence']}**")
    if reason:
        meta += f" | criterion: **{reason}**"
    out = [head, meta, f"- screener note: {row['notes'] or '_none_'}"]
    if show_abstract:
        out.append(f"- abstract: {abstract[:ABSTRACT_CHARS] + '...' if abstract else '_none available_'}")
    out += ["- **verdict:** ", ""]
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decisions", required=True, help="Decision file defining the block.")
    parser.add_argument("--out", required=True, help="Markdown packet to write.")
    parser.add_argument("--sample", type=int, default=20, help="Confident excludes to sample.")
    parser.add_argument("--seed", type=int, default=1, help="Recorded seed for the exclude sample.")
    parser.add_argument("--title", default="Author verification packet")
    args = parser.parse_args()

    ids = [d["id"] for d in json.loads(Path(args.decisions).read_text(encoding="utf-8"))["decisions"]]
    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        log = {r["id"]: r for r in csv.DictReader(f)}
    with POOL_PATH.open(newline="", encoding="utf-8") as f:
        pool = {r["candidate_id"]: r for r in csv.DictReader(f)}

    rows = [log[i] for i in ids if i in log]
    includes = [r for r in rows if r["decision"] == "include"]
    holds = [r for r in rows if r["decision"] == "hold"]
    low_excl = [r for r in rows if r["decision"] == "exclude" and r["confidence"] == "low"]
    conf_excl = [r for r in rows if r["decision"] == "exclude" and r["confidence"] == "high"]

    rng = random.Random(args.seed)
    sample = sorted(rng.sample(conf_excl, min(args.sample, len(conf_excl))), key=lambda r: r["title"])

    low_inc = sum(1 for r in includes if r["confidence"] == "low")
    lines = [
        f"# {args.title}", "",
        f"Source: `{args.decisions}`. Mark each **verdict** line `agree` / `disagree` / `unsure`.",
        "Screening of the next block is paused until this returns.", "",
        f"- Records in block: **{len(rows)}** — {len(includes)} include, "
        f"{len(low_excl) + len(conf_excl)} exclude, {len(holds)} hold",
        f"- Requiring your review: **{len(includes) + len(low_excl) + len(holds) + len(sample)}** "
        f"({len(includes)} includes, {len(low_excl)} low-confidence excludes, {len(holds)} holds, "
        f"{len(sample)} sampled confident excludes)",
        f"- Low-confidence rate: {low_inc}/{len(includes)} includes, "
        f"{len(low_excl)}/{len(low_excl) + len(conf_excl)} excludes",
        f"- Exclude sample seed: `{args.seed}` (regenerates identically)", "",
        "---", "",
        f"## A. Includes ({len(includes)}) — advance to Stage 2 if you agree", "",
    ]
    for n, r in enumerate(sorted(includes, key=lambda r: (r["confidence"] != "low", r["title"])), 1):
        lines += render(r, pool, n, show_abstract=True)

    if holds:
        lines += ["---", "", f"## B. Holds ({len(holds)}) — unidentifiable, awaiting your direction", ""]
        for n, r in enumerate(sorted(holds, key=lambda r: r["title"]), 1):
            lines += render(r, pool, n, show_abstract=False)

    lines += ["---", "",
              f"## C. Low-confidence excludes ({len(low_excl)}) — the false-exclude risk", ""]
    for n, r in enumerate(sorted(low_excl, key=lambda r: r["title"]), 1):
        lines += render(r, pool, n, show_abstract=True)

    lines += ["---", "",
              f"## D. Sampled confident excludes ({len(sample)} of {len(conf_excl)}, seed {args.seed})", ""]
    for n, r in enumerate(sample, 1):
        lines += render(r, pool, n, show_abstract=False)

    out = Path(args.out)
    if not out.is_absolute():
        out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(REPO_ROOT)}: "
          f"{len(includes)} includes, {len(low_excl)} low-confidence excludes, "
          f"{len(holds)} holds, {len(sample)} sampled excludes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
