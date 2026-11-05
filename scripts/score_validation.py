#!/usr/bin/env python3
"""Score the pre-registered screening validation (docs/validation-plan.md).

Verifies each key's SHA-256 against validation/partN_key.sha256, joins blind and key
files on sample_id, and writes validation/results.md (tables only) and
validation/disagreements.csv.
"""
import csv, hashlib, math, sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(sys.maxsize)
REPO = Path(__file__).resolve().parents[1]
V = REPO / "validation"


def read(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def main():
    log = {r["id"]: r for r in read(REPO / "screening" / "screening-log.csv")}
    joined = []
    for part in ("1", "2"):
        key_path = V / f"part{part}_key.csv"
        expected = (V / f"part{part}_key.sha256").read_text().split()[0]
        actual = hashlib.sha256(key_path.read_bytes()).hexdigest()
        if actual != expected:
            sys.exit(f"MISMATCH: part{part}_key.csv hash {actual} != {expected}")
        blind = {r["sample_id"]: r for r in read(V / f"part{part}_blind.csv")}
        for k in read(key_path):
            b = blind[k["sample_id"]]
            if b["decision"] not in ("INCLUDE", "EXCLUDE"):
                sys.exit(f"undecided row {k['sample_id']}")
            joined.append((k, b))

    lines = ["# Screening validation results", "",
             "Computed by scripts/score_validation.py from committed blind and key files. Key hashes verified.", "",
             "A disagreement is a row where the author decision differs from the classifier decision.", "",
             "| Population | n | Classifier decision | Author disagrees | Rate | Wilson 95% CI |",
             "|---|---:|---|---:|---:|---|"]
    by_pop = defaultdict(list)
    for k, b in joined:
        by_pop[k["population"]].append((k, b))
    for pop in sorted(by_pop):
        rows = by_pop[pop]
        cls = Counter(k["classifier_decision"] for k, _ in rows)
        dis = sum(1 for k, b in rows if k["classifier_decision"].upper() != b["decision"])
        lo, hi = wilson(dis, len(rows))
        lines.append(f"| {pop} | {len(rows)} | {', '.join(f'{c} {n}' for c, n in sorted(cls.items()))} | "
                     f"{dis} | {dis / len(rows):.1%} | {lo:.1%} to {hi:.1%} |")
    for label, idx in (("year", 0), ("canonical source", 1)):
        lines += ["", f"## Population B by {label}", "", "| Stratum | n | Author includes | Rate |", "|---|---:|---:|---:|"]
        g = defaultdict(lambda: [0, 0])
        for k, b in by_pop["B"]:
            s = k["stratum"].split("|")[idx]
            g[s][0] += 1; g[s][1] += b["decision"] == "INCLUDE"
        for s in sorted(g):
            n, i = g[s]
            lines.append(f"| {s} | {n} | {i} | {i / n:.1%} |")
    (V / "results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    with open(V / "disagreements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "record_id", "population", "title", "classifier_decision",
                    "classifier_exclusion_reason", "author_decision", "author_reason_code"])
        for k, b in sorted(joined, key=lambda kb: kb[0]["sample_id"]):
            if k["classifier_decision"].upper() != b["decision"]:
                w.writerow([k["sample_id"], k["record_id"], k["population"], b["title"], k["classifier_decision"],
                            log.get(k["record_id"], {}).get("exclusion_reason", ""), b["decision"], b["reason_code"]])
    print("\n".join(lines))


if __name__ == "__main__":
    main()
