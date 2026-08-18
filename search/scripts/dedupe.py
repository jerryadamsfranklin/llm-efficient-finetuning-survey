#!/usr/bin/env python3
"""Deduplicate Phase 2 search results into a unique candidate pool.

Match priority (protocol): DOI → arXiv ID → normalized title
(exact, then fuzzy ratio ≥ 0.95 via rapidfuzz).

When preprint and published versions collide, keep the published record and
record the arXiv ID as superseded.

Outputs:
  search/candidate-pool.csv
  search/dedupe-summary.json
  appends a section to search/search-log.md
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

from rapidfuzz import fuzz

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import REPO_ROOT, SEARCH_LOG_PATH, utc_now_iso  # noqa: E402

RAW_ROOT = REPO_ROOT / "search" / "raw"
POOL_PATH = REPO_ROOT / "search" / "candidate-pool.csv"
SUMMARY_PATH = REPO_ROOT / "search" / "dedupe-summary.json"

FUZZY_THRESHOLD = 95  # rapidfuzz ratio is 0–100
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+", re.I)
ARXIV_RE = re.compile(r"(?:arxiv(?:\.org/(?:abs|pdf))/)?(\d{4}\.\d{4,5})(?:v\d+)?", re.I)


def norm_doi(value: Any) -> str | None:
    if not value:
        return None
    s = str(value).strip()
    if s.startswith("https://doi.org/"):
        s = s[len("https://doi.org/") :]
    if s.startswith("http://doi.org/"):
        s = s[len("http://doi.org/") :]
    m = DOI_RE.search(s)
    if not m:
        return None
    doi = m.group(0).rstrip(").,;")
    return doi.lower()


def norm_arxiv(value: Any) -> str | None:
    if not value:
        return None
    s = str(value).strip()
    m = ARXIV_RE.search(s)
    if not m:
        return None
    return m.group(1)


def norm_title(value: Any) -> str:
    s = str(value or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def invert_abstract(index: Any) -> str:
    """Rebuild plain text from an OpenAlex abstract_inverted_index."""
    if not isinstance(index, dict) or not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, locs in index.items():
        if not isinstance(locs, list):
            continue
        for loc in locs:
            if isinstance(loc, int):
                positions.append((loc, word))
    positions.sort()
    return " ".join(word for _, word in positions)


def to_int(value: Any) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return 0


def authors_to_str(authors: Any) -> str:
    if authors is None:
        return ""
    if isinstance(authors, str):
        return authors
    if isinstance(authors, list):
        names = []
        for a in authors:
            if isinstance(a, str):
                names.append(a)
            elif isinstance(a, dict):
                names.append(a.get("name") or a.get("text") or a.get("full_name") or "")
        return "; ".join(n for n in names if n)
    if isinstance(authors, dict):
        # IEEE: {"authors": [{"full_name": ...}, ...]}
        inner = authors.get("authors") or authors.get("author")
        return authors_to_str(inner)
    return str(authors)


@dataclass
class Record:
    source: str
    source_query: str
    title: str
    authors: str = ""
    year: str = ""
    venue: str = ""
    doi: str | None = None
    arxiv_id: str | None = None
    abstract: str = ""
    extra_id: str = ""
    is_published: bool = False  # has DOI / non-preprint venue signal
    title_norm: str = ""
    parent_query: str = ""
    citations: int = 0  # inclusion criterion 3 (adoption bar)
    language: str = ""  # inclusion criterion 4
    work_type: str = ""  # exclusion criterion 6 (non-archival material)

    def __post_init__(self) -> None:
        self.title_norm = norm_title(self.title)
        self.doi = norm_doi(self.doi)
        self.arxiv_id = norm_arxiv(self.arxiv_id)
        if self.doi:
            self.is_published = True


class UnionFind:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))
        self.r = [0] * n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.r[ra] < self.r[rb]:
            self.p[ra] = rb
        elif self.r[ra] > self.r[rb]:
            self.p[rb] = ra
        else:
            self.p[rb] = ra
            self.r[ra] += 1


def load_arxiv() -> list[Record]:
    out: list[Record] = []
    for path in sorted((RAW_ROOT / "arxiv").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        q = data.get("protocol_query") or data.get("search_query") or path.stem
        for e in data.get("entries") or []:
            out.append(
                Record(
                    source="arxiv",
                    source_query=str(q),
                    title=e.get("title") or "",
                    authors=authors_to_str(e.get("authors")),
                    year=(e.get("published") or "")[:4],
                    venue="arXiv",
                    arxiv_id=e.get("arxiv_id") or e.get("id"),
                    abstract=e.get("summary") or "",
                    extra_id=e.get("id") or "",
                    is_published=False,
                )
            )
    return out


def load_semanticscholar(source_dir: str = "semanticscholar") -> list[Record]:
    out: list[Record] = []
    root = RAW_ROOT / source_dir
    if not root.exists():
        return out
    for path in sorted(root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        q = data.get("protocol_query") or data.get("query") or path.stem
        for p in data.get("papers") or []:
            ext = p.get("externalIds") or {}
            out.append(
                Record(
                    source=source_dir,
                    source_query=str(q),
                    title=p.get("title") or "",
                    authors=authors_to_str(p.get("authors")),
                    year=str(p.get("year") or ""),
                    venue=p.get("venue") or "",
                    doi=ext.get("DOI"),
                    arxiv_id=ext.get("ArXiv"),
                    abstract=p.get("abstract") or "",
                    extra_id=p.get("paperId") or "",
                    is_published=bool(ext.get("DOI")),
                    citations=to_int(p.get("citationCount")),
                )
            )
    return out


def load_openalex(source_dir: str) -> list[Record]:
    out: list[Record] = []
    root = RAW_ROOT / source_dir
    if not root.exists():
        return out
    for path in sorted(root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        q = data.get("query") or path.stem
        for w in data.get("results") or []:
            ids = w.get("ids") or {}
            loc = w.get("primary_location") or {}
            src = (loc.get("source") or {}) if isinstance(loc, dict) else {}
            venue = ""
            if isinstance(src, dict):
                venue = src.get("display_name") or ""
            arxiv = None
            for k, v in ids.items():
                if "arxiv" in k.lower():
                    arxiv = v
            if not arxiv:
                # arXiv landing pages appear as alternate locations, not always in ids
                for loc_item in w.get("locations") or []:
                    if not isinstance(loc_item, dict):
                        continue
                    src_name = ((loc_item.get("source") or {}) or {}).get("display_name") or ""
                    url = loc_item.get("landing_page_url") or ""
                    if "arxiv" in src_name.lower() or "arxiv.org" in url.lower():
                        arxiv = url or src_name
                        break
            openalex_id = w.get("id") or ""
            out.append(
                Record(
                    source=source_dir,
                    source_query=str(q),
                    title=w.get("title") or w.get("display_name") or "",
                    authors=authors_to_str(
                        [
                            (a.get("author") or {}).get("display_name")
                            for a in (w.get("authorships") or [])
                        ]
                    ),
                    year=str(w.get("publication_year") or ""),
                    venue=venue,
                    doi=w.get("doi") or ids.get("doi"),
                    arxiv_id=arxiv,
                    abstract=invert_abstract(w.get("abstract_inverted_index")),
                    extra_id=openalex_id,
                    is_published=bool(w.get("doi") or ids.get("doi")),
                    citations=to_int(w.get("cited_by_count")),
                    language=str(w.get("language") or ""),
                    work_type=str(w.get("type") or ""),
                )
            )
    return out


def load_ieee() -> list[Record]:
    out: list[Record] = []
    for path in sorted((RAW_ROOT / "ieee").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        q = data.get("query") or path.stem
        for a in data.get("articles") or []:
            out.append(
                Record(
                    source="ieee",
                    source_query=str(q),
                    title=a.get("title") or "",
                    authors=authors_to_str(a.get("authors")),
                    year=str(a.get("publication_year") or ""),
                    venue=a.get("publication_title") or "",
                    doi=a.get("doi"),
                    arxiv_id=None,
                    abstract=a.get("abstract") or "",
                    extra_id=str(a.get("article_number") or ""),
                    is_published=True,
                    citations=to_int(a.get("citing_paper_count")),
                    work_type=str(a.get("content_type") or ""),
                )
            )
    return out


def load_dblp() -> list[Record]:
    out: list[Record] = []
    for path in sorted((RAW_ROOT / "dblp").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        q = data.get("query") or path.stem
        for h in data.get("hits") or []:
            info = h.get("info") or {}
            authors = info.get("authors") or {}
            out.append(
                Record(
                    source="dblp",
                    source_query=str(q),
                    title=info.get("title") or "",
                    authors=authors_to_str(authors.get("author") if isinstance(authors, dict) else authors),
                    year=str(info.get("year") or ""),
                    venue=str(info.get("venue") or ""),
                    doi=info.get("doi"),
                    arxiv_id=None,
                    abstract="",
                    extra_id=str(info.get("key") or h.get("@id") or ""),
                    is_published=bool(info.get("doi")),
                )
            )
    return out


def load_google_scholar() -> list[Record]:
    path = RAW_ROOT / "google_scholar" / "google_scholar_candidates.csv"
    if not path.exists():
        return []
    out: list[Record] = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pq = (row.get("parent_query") or "").strip()
            if pq in {"NOISE_UI", "DUPLICATE"}:
                continue
            out.append(
                Record(
                    source="google_scholar",
                    source_query=pq or row.get("bucket") or "",
                    title=row.get("title") or "",
                    authors=row.get("authors") or "",
                    year=str(row.get("year") or ""),
                    venue=row.get("venue") or "",
                    doi=None,
                    arxiv_id=None,
                    abstract="",
                    extra_id=row.get("id") or "",
                    is_published=False,
                    parent_query=pq,
                    citations=to_int(row.get("cited_by")),
                )
            )
    return out


def load_supplementary() -> list[Record]:
    """Protocol v1.3 known-corpus verification lookups (search/raw/supplementary/).

    These are references the manuscript already cites that Phase 2 did not retrieve. They
    enter the pool so they can be screened on the same criteria as every other candidate.
    A lookup whose matched title is not identical to the cited title is NOT loaded: it may
    be a different work, and admitting it would silently substitute one paper for another.
    """
    path = RAW_ROOT / "supplementary" / "known_corpus_misses.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    out: list[Record] = []
    for item in data.get("results") or []:
        rec = item.get("record")
        if not rec or item.get("lookup_status") != "matched":
            continue
        if norm_title(rec.get("title")) != norm_title(item.get("reference_title")):
            print(
                f"  supplementary: SKIP {item.get('reference_key')} — matched title differs "
                f"from cited title (possible different work)",
                flush=True,
            )
            continue
        ext = rec.get("externalIds") or {}
        authors = rec.get("authors")
        # Criterion 5 reads "published (or first posted, for preprints)". For these records
        # the manuscript's verified publication year governs: Semantic Scholar reports the
        # preprint posting year (GPipe 2018, AdamW 2017), which would otherwise date a paper
        # published at NeurIPS/ICLR 2019 to outside the coverage window.
        year = str(item.get("reference_year") or rec.get("year") or "")
        out.append(
            Record(
                source="supplementary",
                source_query=f"known_corpus:{item.get('reference_key')}",
                title=rec.get("title") or "",
                authors=authors_to_str(authors),
                year=year,
                venue=rec.get("venue") or item.get("reference_venue") or "",
                doi=ext.get("DOI") or rec.get("doi"),
                arxiv_id=ext.get("ArXiv"),
                abstract=rec.get("abstract") or "",
                extra_id=str(rec.get("paperId") or ""),
                is_published=bool(ext.get("DOI") or rec.get("doi")),
                citations=to_int(rec.get("citationCount")),
                parent_query=f"known_corpus:{item.get('reference_key')}",
            )
        )
    return out


def prefer(a: Record, b: Record) -> Record:
    """Choose canonical record: published > has DOI > has arxiv > longer abstract."""
    def score(r: Record) -> tuple:
        return (
            1 if r.is_published else 0,
            1 if r.doi else 0,
            0 if r.source == "arxiv" else 1,  # prefer non-arxiv when tied
            1 if r.arxiv_id else 0,
            len(r.abstract or ""),
            len(r.venue or ""),
            len(r.title or ""),
        )

    return a if score(a) >= score(b) else b


def merge_cluster(recs: list[Record]) -> dict[str, Any]:
    canon = recs[0]
    for r in recs[1:]:
        canon = prefer(canon, r)
    dois = sorted({r.doi for r in recs if r.doi})
    arxivs = sorted({r.arxiv_id for r in recs if r.arxiv_id})
    sources = sorted({r.source for r in recs})
    queries = sorted({r.source_query for r in recs if r.source_query})
    superseded = [a for a in arxivs if a != canon.arxiv_id]
    scholar_only = sources == ["google_scholar"]
    oop = scholar_only and canon.parent_query == "OUT_OF_PROTOCOL"
    # Screening needs the richest metadata in the cluster, not only the canonical
    # record's: the preferred (published) record often lacks an abstract that the
    # merged preprint carries, and citation counts differ per source.
    best_abstract = max((r.abstract or "" for r in recs), key=len)
    cited = max(recs, key=lambda r: r.citations)
    language = next((r.language for r in recs if r.language), "")
    work_type = next((r.work_type for r in recs if r.work_type), "")
    return {
        "title": canon.title,
        "authors": canon.authors,
        "year": canon.year or next((r.year for r in recs if r.year), ""),
        "venue": canon.venue or next((r.venue for r in recs if r.venue), ""),
        "doi": canon.doi or (dois[0] if dois else ""),
        "arxiv_id": canon.arxiv_id or (arxivs[0] if arxivs else ""),
        "abstract": best_abstract[:2000],
        "citations": cited.citations,
        "citations_source": cited.source if cited.citations else "",
        "language": language,
        "work_type": work_type,
        "canonical_source": canon.source,
        "sources": "|".join(sources),
        "n_sources": len(sources),
        "n_records_merged": len(recs),
        "source_queries": "|".join(queries)[:500],
        "superseded_arxiv_ids": "|".join(superseded),
        "parent_query": canon.parent_query,
        "is_published": canon.is_published or bool(canon.doi),
        "out_of_protocol": oop,
    }


def dedupe(records: list[Record], fuzzy: bool = True) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    n = len(records)
    uf = UnionFind(n)

    doi_index: dict[str, int] = {}
    arxiv_index: dict[str, int] = {}
    title_index: dict[str, int] = {}

    match_counts = Counter()

    for i, r in enumerate(records):
        if r.doi:
            if r.doi in doi_index:
                uf.union(i, doi_index[r.doi])
                match_counts["doi"] += 1
            else:
                doi_index[r.doi] = i
        if r.arxiv_id:
            if r.arxiv_id in arxiv_index:
                uf.union(i, arxiv_index[r.arxiv_id])
                match_counts["arxiv"] += 1
            else:
                arxiv_index[r.arxiv_id] = i
        if r.title_norm and len(r.title_norm) >= 10:
            if r.title_norm in title_index:
                uf.union(i, title_index[r.title_norm])
                match_counts["title_exact"] += 1
            else:
                title_index[r.title_norm] = i

    fuzzy_links = 0
    if fuzzy:
        # Block by first 4 chars of normalized title + length bucket to keep runtime sane.
        blocks: dict[tuple[str, int], list[int]] = defaultdict(list)
        for i, r in enumerate(records):
            if not r.title_norm or len(r.title_norm) < 15:
                continue
            key = (r.title_norm[:4], len(r.title_norm) // 10)
            blocks[key].append(i)

        for idxs in blocks.values():
            if len(idxs) < 2 or len(idxs) > 800:
                # huge blocks: only compare within same year if available
                if len(idxs) > 800:
                    by_year: dict[str, list[int]] = defaultdict(list)
                    for i in idxs:
                        by_year[records[i].year or ""].append(i)
                    groups = list(by_year.values())
                else:
                    groups = [idxs]
            else:
                groups = [idxs]
            for group in groups:
                if len(group) < 2:
                    continue
                # Compare each to others with higher index; skip if already same component
                for a in range(len(group)):
                    ia = group[a]
                    ta = records[ia].title_norm
                    for b in range(a + 1, len(group)):
                        ib = group[b]
                        if uf.find(ia) == uf.find(ib):
                            continue
                        tb = records[ib].title_norm
                        # cheap length gate
                        if abs(len(ta) - len(tb)) > max(8, int(0.15 * max(len(ta), len(tb)))):
                            continue
                        score = fuzz.ratio(ta, tb)
                        if score >= FUZZY_THRESHOLD:
                            uf.union(ia, ib)
                            fuzzy_links += 1
                            match_counts["title_fuzzy"] += 1

    clusters: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        clusters[uf.find(i)].append(i)

    pool = [merge_cluster([records[i] for i in members]) for members in clusters.values()]
    # stable sort
    pool.sort(key=lambda r: (r.get("year") or "", r.get("title") or ""))

    summary = {
        "fetched_at": utc_now_iso(),
        "protocol_rule": "DOI > arXiv ID > normalized title (exact then fuzzy ≥ 0.95)",
        "fuzzy_threshold": FUZZY_THRESHOLD,
        "raw_records": n,
        "unique_candidates": len(pool),
        "match_events": dict(match_counts),
        "fuzzy_links": fuzzy_links,
        "by_canonical_source": dict(Counter(r["canonical_source"] for r in pool)),
        "multi_source_candidates": sum(1 for r in pool if r["n_sources"] > 1),
        "with_doi": sum(1 for r in pool if r.get("doi")),
        "with_arxiv": sum(1 for r in pool if r.get("arxiv_id")),
        "with_abstract": sum(1 for r in pool if (r.get("abstract") or "").strip()),
        "with_citation_data": sum(1 for r in pool if r.get("citations")),
        "at_or_above_50_citations": sum(1 for r in pool if (r.get("citations") or 0) >= 50),
        "out_of_protocol": sum(1 for r in pool if r.get("out_of_protocol")),
    }
    return pool, summary


def candidate_id(row: dict[str, Any]) -> str:
    """Content-derived, stable candidate id.

    Positional ids (C00001 by sort order) shift whenever the pool is regenerated, which
    would silently reassign screening decisions recorded against them. Deriving the id from
    the strongest available identifier keeps it stable across re-runs, so the pool can be
    refreshed mid-screening without corrupting `screening/screening-log.csv`.
    """
    key = row.get("doi") or row.get("arxiv_id") or norm_title(row.get("title"))
    digest = hashlib.sha1(str(key).encode("utf-8")).hexdigest()[:10]
    return f"C-{digest}"


def write_pool(pool: list[dict[str, Any]], path: Path = POOL_PATH) -> None:
    fields = [
        "candidate_id",
        "title",
        "authors",
        "year",
        "venue",
        "doi",
        "arxiv_id",
        "canonical_source",
        "sources",
        "n_sources",
        "n_records_merged",
        "is_published",
        "citations",
        "citations_source",
        "language",
        "work_type",
        "out_of_protocol",
        "superseded_arxiv_ids",
        "parent_query",
        "source_queries",
        "abstract",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    seen: dict[str, int] = {}
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in pool:
            out = {k: row.get(k, "") for k in fields}
            cid = candidate_id(row)
            # Disambiguate the rare hash collision deterministically rather than silently
            # merging two distinct candidates under one id.
            if cid in seen:
                seen[cid] += 1
                cid = f"{cid}-{seen[cid]}"
            else:
                seen[cid] = 0
            out["candidate_id"] = cid
            out["is_published"] = "yes" if row.get("is_published") else "no"
            out["out_of_protocol"] = "yes" if row.get("out_of_protocol") else "no"
            w.writerow(out)


def append_log(summary: dict[str, Any], by_source_raw: dict[str, int]) -> None:
    lines = [
        "### dedupe — Phase 2 candidate pool",
        f"- **Date run:** {summary['fetched_at']}",
        f"- **Raw records loaded:** {summary['raw_records']}",
        f"- **Unique candidates:** {summary['unique_candidates']}",
        f"- **Multi-source merges:** {summary['multi_source_candidates']}",
        f"- **With DOI / arXiv:** {summary['with_doi']} / {summary['with_arxiv']}",
        f"- **With abstract:** {summary['with_abstract']}",
        f"- **With citation count / ≥ 50 citations:** "
        f"{summary['with_citation_data']} / {summary['at_or_above_50_citations']}",
        f"- **Out-of-protocol (Scholar):** {summary['out_of_protocol']}",
        f"- **Match events:** {summary['match_events']}",
        f"- **Raw by source:** {by_source_raw}",
        f"- **Canonical-source mix:** {summary['by_canonical_source']}",
        f"- **Outputs:** `search/candidate-pool.csv`, `search/dedupe-summary.json`",
        "- **Notes:** Match priority DOI → arXiv ID → normalized title "
        f"(exact then fuzzy ≥ {FUZZY_THRESHOLD / 100:.2f}). "
        "Published/DOI records preferred over arXiv-only when merged. "
        "Scholar NOISE_UI and DUPLICATE rows excluded from load.",
        "",
    ]
    text = SEARCH_LOG_PATH.read_text(encoding="utf-8") if SEARCH_LOG_PATH.exists() else ""
    marker = "### dedupe — Phase 2 candidate pool"
    entry = "\n".join(lines)
    if marker in text:
        pattern = re.compile(rf"^{re.escape(marker)}\n(?:.*\n)*?(?=^### |\Z)", re.MULTILINE)
        text = pattern.sub(entry + "\n", text, count=1)
        SEARCH_LOG_PATH.write_text(text.rstrip() + "\n", encoding="utf-8")
    else:
        SEARCH_LOG_PATH.write_text(text.rstrip() + "\n\n" + entry, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deduplicate Phase 2 search results.")
    parser.add_argument("--no-fuzzy", action="store_true", help="Skip fuzzy title matching.")
    args = parser.parse_args()

    loaders = [
        ("arxiv", load_arxiv),
        ("semanticscholar", load_semanticscholar),
        # v1.3 additions: date-sliced confirmation-band backfill and known-corpus lookups.
        ("semanticscholar_backfill", lambda: load_semanticscholar("semanticscholar_backfill")),
        ("openalex", lambda: load_openalex("openalex")),
        ("openalex_acm", lambda: load_openalex("openalex_acm")),
        ("ieee", load_ieee),
        ("dblp", load_dblp),
        ("google_scholar", load_google_scholar),
        ("supplementary", load_supplementary),
    ]
    records: list[Record] = []
    by_source_raw: dict[str, int] = {}
    for name, fn in loaders:
        batch = fn()
        # drop empty titles
        batch = [r for r in batch if r.title_norm]
        by_source_raw[name] = len(batch)
        print(f"loaded {name}: {len(batch)}", flush=True)
        records.extend(batch)

    print(f"total raw: {len(records)}; deduping…", flush=True)
    pool, summary = dedupe(records, fuzzy=not args.no_fuzzy)
    summary["raw_by_source"] = by_source_raw
    # screening-oriented count excludes out-of-protocol-only scholar leftovers
    summary["unique_for_screening"] = sum(1 for r in pool if not r.get("out_of_protocol"))

    write_pool(pool)
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    append_log(summary, by_source_raw)

    print(json.dumps({k: summary[k] for k in (
        "raw_records", "unique_candidates", "unique_for_screening",
        "multi_source_candidates", "with_doi", "with_arxiv", "match_events"
    )}, indent=2))
    print(f"wrote {POOL_PATH}")
    print(f"wrote {SUMMARY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
