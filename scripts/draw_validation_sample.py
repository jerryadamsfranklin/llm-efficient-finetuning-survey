#!/usr/bin/env python3
"""Draw revision-3 screening validation samples per docs/validation-plan.md.

Read-only inputs:
  screening/screening-log.csv
  search/candidate-pool.csv  (joined on id = candidate_id)

Writes (under validation/):
  part1_blind.csv, part1_key.csv, part1_key.sha256
  part2_blind.csv, part2_key.csv, part2_key.sha256

Seed: random.Random(20261102) for every random step.
Does not modify the screening log or candidate pool.
"""

from __future__ import annotations

import csv
import hashlib
import platform
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LOG_PATH = REPO / "screening" / "screening-log.csv"
POOL_PATH = REPO / "search" / "candidate-pool.csv"
OUT_DIR = REPO / "validation"

SEED = 20261102
B_SAMPLE_SIZE = 300
D1_SIZE = 100
D2_SIZE = 100

csv.field_size_limit(10**9)


def year_band(year: str) -> str:
    y = (year or "").strip()
    if y in {"2024", "2025", "2026"}:
        return y
    return "missing"


def query_block(parent_query: str) -> str:
    pq = (parent_query or "").strip()
    if not pq:
        return "missing"
    return pq.split("_", 1)[0]


def stratum_key(year: str, canonical_source: str, parent_query: str) -> str:
    src = (canonical_source or "").strip() or "missing"
    return f"{year_band(year)}|{src}|{query_block(parent_query)}"


def largest_remainder_allocation(
    sizes: dict[str, int], total: int
) -> dict[str, int]:
    """Proportional allocation with largest-remainder rounding; quotas capped at size."""
    N = sum(sizes.values())
    if N == 0 or total == 0:
        return {k: 0 for k in sizes}
    if total > N:
        raise ValueError(f"Cannot sample {total} from population of {N}")

    quotas = {k: sizes[k] * total / N for k in sizes}
    alloc = {k: min(sizes[k], int(quotas[k])) for k in sizes}
    remaining = total - sum(alloc.values())
    # fractional parts among strata with spare capacity
    while remaining > 0:
        candidates = [
            k
            for k in sizes
            if alloc[k] < sizes[k]
        ]
        if not candidates:
            raise ValueError("Unable to place remaining seats under stratum caps")
        # after caps, prefer largest (quota - alloc) among those with room
        candidates.sort(
            key=lambda k: (
                -(quotas[k] - alloc[k]),
                -sizes[k],
                k,
            )
        )
        alloc[candidates[0]] += 1
        remaining -= 1
    return alloc


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def write_sha256(target: Path, sha_path: Path) -> str:
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    sha_path.write_text(f"{digest}  {target.name}\n", encoding="ascii")
    return digest


def main() -> None:
    print(sys.version)
    print(platform.python_implementation())
    rng = random.Random(SEED)

    with LOG_PATH.open(newline="", encoding="utf-8") as f:
        log_rows = list(csv.DictReader(f))
    with POOL_PATH.open(newline="", encoding="utf-8") as f:
        pool_rows = list(csv.DictReader(f))

    pool_by_id = {r["candidate_id"]: r for r in pool_rows}

    def enrich(log_row: dict) -> dict:
        pid = log_row["id"]
        pool = pool_by_id.get(pid, {})
        return {
            "record_id": pid,
            "title": pool.get("title") or log_row.get("title") or "",
            "abstract": pool.get("abstract") or log_row.get("abstract") or "",
            "year": pool.get("year") or log_row.get("year") or "",
            "venue": pool.get("venue") or log_row.get("venue") or "",
            "canonical_source": pool.get("canonical_source") or "",
            "parent_query": pool.get("parent_query") or "",
            "screener": log_row.get("screener") or "",
            "decision": log_row.get("decision") or "",
            "confidence": log_row.get("confidence") or "",
        }

    pop_A = [
        enrich(r)
        for r in log_rows
        if r.get("screener") == "automated"
        and r.get("decision") == "exclude"
        and r.get("confidence") == "low"
    ]
    pop_B = [
        enrich(r)
        for r in log_rows
        if r.get("screener") in {"automated", "llm_assisted"}
        and r.get("decision") == "exclude"
        and r.get("confidence") == "high"
    ]
    pop_C = [
        enrich(r)
        for r in log_rows
        if r.get("screener") == "automated"
        and r.get("decision") == "include"
        and r.get("confidence") == "low"
    ]
    pop_D1_pool = [
        enrich(r)
        for r in log_rows
        if r.get("screener") == "automated"
        and r.get("decision") == "include"
        and r.get("confidence") == "high"
    ]

    # --- B stratified sample ---
    by_stratum: dict[str, list[dict]] = defaultdict(list)
    for row in pop_B:
        sk = stratum_key(row["year"], row["canonical_source"], row["parent_query"])
        row["stratum"] = sk
        by_stratum[sk].append(row)

    sizes = {k: len(v) for k, v in sorted(by_stratum.items())}
    alloc = largest_remainder_allocation(sizes, B_SAMPLE_SIZE)

    print("=== Population B stratum allocation (n=300) ===")
    print(f"{'stratum':<48} {'size':>6} {'alloc':>6}")
    for k in sorted(sizes):
        print(f"{k:<48} {sizes[k]:6d} {alloc[k]:6d}")
    print(f"{'TOTAL':<48} {sum(sizes.values()):6d} {sum(alloc.values()):6d}")

    b_sample: list[dict] = []
    b_sample_ids: set[str] = set()
    for sk in sorted(by_stratum):
        members = sorted(by_stratum[sk], key=lambda r: r["record_id"])
        rng.shuffle(members)
        take = alloc[sk]
        chosen = members[:take]
        for row in chosen:
            row = dict(row)
            row["population"] = "B"
            b_sample.append(row)
            b_sample_ids.add(row["record_id"])

    # --- D1 ---
    d1_pool = sorted(pop_D1_pool, key=lambda r: r["record_id"])
    rng.shuffle(d1_pool)
    d1 = []
    for row in d1_pool[:D1_SIZE]:
        row = dict(row)
        row["population"] = "D1"
        row["stratum"] = ""
        d1.append(row)

    # --- D2 from B not in sample ---
    b_remainder = sorted(
        [r for r in pop_B if r["record_id"] not in b_sample_ids],
        key=lambda r: r["record_id"],
    )
    rng.shuffle(b_remainder)
    d2 = []
    for row in b_remainder[:D2_SIZE]:
        row = dict(row)
        row["population"] = "D2"
        row["stratum"] = stratum_key(
            row["year"], row["canonical_source"], row["parent_query"]
        )
        d2.append(row)

    # --- A and C tagged ---
    a_rows = []
    for row in sorted(pop_A, key=lambda r: r["record_id"]):
        row = dict(row)
        row["population"] = "A"
        row["stratum"] = ""
        a_rows.append(row)

    c_rows = []
    for row in sorted(pop_C, key=lambda r: r["record_id"]):
        row = dict(row)
        row["population"] = "C"
        row["stratum"] = ""
        c_rows.append(row)

    # --- Assemble and shuffle parts ---
    part1 = a_rows + b_sample + d1
    part1 = sorted(part1, key=lambda r: r["record_id"])
    rng.shuffle(part1)
    part2 = c_rows + d2
    part2 = sorted(part2, key=lambda r: r["record_id"])
    rng.shuffle(part2)

    def assign_sample_ids(rows: list[dict], prefix: str) -> None:
        for i, row in enumerate(rows, start=1):
            row["sample_id"] = f"{prefix}-{i:04d}"

    assign_sample_ids(part1, "P1")
    assign_sample_ids(part2, "P2")

    blind_fields = [
        "sample_id",
        "title",
        "abstract",
        "year",
        "venue",
        "decision",
        "reason_code",
        "note",
    ]
    key_fields = [
        "sample_id",
        "record_id",
        "population",
        "stratum",
        "classifier_decision",
        "classifier_confidence",
        "screener",
    ]

    def blind_row(row: dict) -> dict:
        return {
            "sample_id": row["sample_id"],
            "title": row["title"],
            "abstract": row["abstract"],
            "year": row["year"],
            "venue": row["venue"],
            "decision": "",
            "reason_code": "",
            "note": "",
        }

    def key_row(row: dict) -> dict:
        return {
            "sample_id": row["sample_id"],
            "record_id": row["record_id"],
            "population": row["population"],
            "stratum": row.get("stratum") or "",
            "classifier_decision": row["decision"],
            "classifier_confidence": row["confidence"],
            "screener": row["screener"],
        }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p1_blind = OUT_DIR / "part1_blind.csv"
    p1_key = OUT_DIR / "part1_key.csv"
    p2_blind = OUT_DIR / "part2_blind.csv"
    p2_key = OUT_DIR / "part2_key.csv"

    write_csv(p1_blind, blind_fields, [blind_row(r) for r in part1])
    write_csv(p1_key, key_fields, [key_row(r) for r in part1])
    write_csv(p2_blind, blind_fields, [blind_row(r) for r in part2])
    write_csv(p2_key, key_fields, [key_row(r) for r in part2])

    h1 = write_sha256(p1_key, OUT_DIR / "part1_key.sha256")
    h2 = write_sha256(p2_key, OUT_DIR / "part2_key.sha256")

    print()
    print("=== Population and part counts ===")
    print(f"A (low-conf automated excludes, full): {len(pop_A)}")
    print(f"B (confident machine excludes, pool):  {len(pop_B)}")
    print(f"B sample:                              {len(b_sample)}")
    print(f"C (low-conf automated includes, full): {len(pop_C)}")
    print(f"D1 blinding (from high-conf includes): {len(d1)}")
    print(f"D2 blinding (from B not in sample):    {len(d2)}")
    print(f"Part 1 rows (A + B sample + D1):       {len(part1)}")
    print(f"Part 2 rows (C + D2):                  {len(part2)}")
    print()
    print("Part 1 population mix:", dict(Counter(r["population"] for r in part1)))
    print("Part 2 population mix:", dict(Counter(r["population"] for r in part2)))
    print(f"part1_key.sha256: {h1}")
    print(f"part2_key.sha256: {h2}")


if __name__ == "__main__":
    main()
