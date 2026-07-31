#!/usr/bin/env python3
"""Venue / publication upgrade check for existing manuscript references (Protocol v1.1).

Queries OpenReview, Crossref, and arXiv for each entry in
search/existing-references.yaml. Updates verified_venue / verified_doi / status
and writes docs/reference-corrections.md.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import requests
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _common import REPO_ROOT, append_search_log, save_json, utc_now_iso  # noqa: E402

EXISTING_REFS = REPO_ROOT / "search" / "existing-references.yaml"
CORRECTIONS_MD = REPO_ROOT / "docs" / "reference-corrections.md"
RAW_OUT = REPO_ROOT / "search" / "raw" / "openreview" / "existing_references_venue_check.json"

OPENREVIEW_SEARCH = "https://api2.openreview.net/notes/search"
CROSSREF = "https://api.crossref.org/works"
ARXIV_API = "http://export.arxiv.org/api/query"


def _get_json(session: requests.Session, url: str, params: dict | None = None) -> dict:
    for attempt in range(6):
        resp = session.get(url, params=params, timeout=45)
        if resp.status_code == 429:
            time.sleep(min(60, 2 ** attempt))
            continue
        if resp.status_code >= 500:
            time.sleep(3 * (attempt + 1))
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Failed GET {url}")


def _norm_title(t: str) -> str:
    return re.sub(r"\W+", " ", t.lower()).strip()


def titles_compatible(a: str, b: str) -> bool:
    """Require strong title overlap to avoid Crossref false matches."""
    na, nb = _norm_title(a), _norm_title(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    # token Jaccard
    ta, tb = set(na.split()), set(nb.split())
    if not ta or not tb:
        return False
    inter = len(ta & tb)
    union = len(ta | tb)
    j = inter / union
    # also require the shorter title's tokens mostly covered
    shorter, longer = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    coverage = len(shorter & longer) / len(shorter)
    return j >= 0.7 or coverage >= 0.85


def crossref_by_title(session: requests.Session, title: str) -> dict[str, Any] | None:
    data = _get_json(
        session,
        CROSSREF,
        {"query.bibliographic": title, "rows": 5},
    )
    items = (data.get("message") or {}).get("items") or []
    for it in items:
        for t in it.get("title") or []:
            if titles_compatible(title, t):
                return it
    return None


def crossref_by_doi(session: requests.Session, doi: str) -> dict[str, Any] | None:
    doi = doi.strip()
    try:
        return _get_json(session, f"{CROSSREF}/{urllib.parse.quote(doi)}")["message"]
    except Exception:
        return None


def arxiv_lookup(session: requests.Session, arxiv_id: str) -> dict[str, Any] | None:
    aid = arxiv_id.strip()
    params = {"id_list": aid, "max_results": 1}
    resp = session.get(ARXIV_API, params=params, timeout=45)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    if entry is None:
        return None
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    title = " ".join((entry.findtext("a:title", default="", namespaces=ns) or "").split())
    published = entry.findtext("a:published", default="", namespaces=ns) or ""
    doi_el = entry.find("arxiv:doi", ns)
    journal = entry.find("arxiv:journal_ref", ns)
    return {
        "title": title,
        "published": published,
        "doi": doi_el.text.strip() if doi_el is not None and doi_el.text else None,
        "journal_ref": journal.text.strip() if journal is not None and journal.text else None,
    }


def _unwrap(val: Any) -> Any:
    if isinstance(val, dict) and "value" in val:
        return val.get("value")
    return val


def openreview_lookup(session: requests.Session, title: str, arxiv_id: str | None) -> list[dict]:
    notes = []
    for term in [t for t in [title, arxiv_id] if t]:
        try:
            data = _get_json(
                session,
                OPENREVIEW_SEARCH,
                {"term": term, "limit": 8, "offset": 0},
            )
            for n in data.get("notes") or []:
                content = n.get("content") or {}
                notes.append(
                    {
                        "id": n.get("id"),
                        "invitation": n.get("invitation"),
                        "title": _unwrap(content.get("title")),
                        "venue": _unwrap(content.get("venue")),
                        "venueid": _unwrap(content.get("venueid")),
                    }
                )
        except Exception as exc:
            notes.append({"error": str(exc), "term": term})
        time.sleep(0.4)
    seen = set()
    uniq = []
    for n in notes:
        nid = n.get("id") or str(n)
        if nid in seen:
            continue
        seen.add(nid)
        uniq.append(n)
    return uniq


def venue_from_crossref(item: dict[str, Any]) -> str:
    container = (item.get("container-title") or [None])[0]
    event = (item.get("event") or {}).get("name")
    type_ = item.get("type")
    issued = item.get("issued", {}).get("date-parts", [[None]])[0]
    year = issued[0] if issued else None
    parts = [p for p in [container or event, str(year) if year else None, type_] if p]
    return " / ".join(parts) if parts else (type_ or "crossref-match")


def author_overlap(ref_authors: str, cr_authors: list[str]) -> bool:
    if not ref_authors or not cr_authors:
        return False
    first = ref_authors.split(",")[0].strip().lower()
    surname = first.split()[0].rstrip(".").lower()
    return surname in " ".join(cr_authors).lower()


def classify(
    ref: dict[str, Any],
    *,
    cr: dict[str, Any] | None,
    arx: dict[str, Any] | None,
    or_notes: list[dict],
) -> dict[str, Any]:
    """Set verified_venue, verified_doi, status."""
    venue_current = (ref.get("venue_current") or "").lower()
    cited_as_arxiv = "arxiv preprint" in venue_current
    verified_doi = ref.get("doi")
    verified_venue = None
    status = "confirmed_preprint" if cited_as_arxiv else "confirmed_published"
    notes = []
    cr_authors: list[str] = []

    if cr:
        cr_authors = [
            f"{a.get('family', '')}, {a.get('given', '')}"
            for a in (cr.get("author") or [])[:12]
        ]
        cr_doi = cr.get("DOI")
        cr_venue = venue_from_crossref(cr)
        cr_type = (cr.get("type") or "").lower()
        publishedish = cr_type in {
            "journal-article",
            "proceedings-article",
            "proceedings",
            "book-chapter",
        } or bool(cr.get("container-title")) or bool((cr.get("event") or {}).get("name"))
        if publishedish and author_overlap(ref.get("authors") or "", cr_authors):
            if cr_doi:
                verified_doi = cr_doi
            verified_venue = cr_venue
            if cited_as_arxiv:
                status = "UPGRADED"
                notes.append(f"Crossref published match: {cr_venue}")
            else:
                status = "confirmed_published"
        elif publishedish and cited_as_arxiv:
            notes.append(
                "Crossref candidate rejected (author mismatch): "
                f"{cr_venue} / {cr_authors[:3]}"
            )

    if arx:
        if arx.get("doi") and not verified_doi:
            verified_doi = arx["doi"]
        if arx.get("journal_ref"):
            if cited_as_arxiv and status != "UPGRADED":
                verified_venue = arx["journal_ref"]
                status = "UPGRADED"
                notes.append(f"arXiv journal_ref: {arx['journal_ref']}")
            elif not verified_venue:
                verified_venue = arx["journal_ref"]

    for n in or_notes:
        v = n.get("venue")
        if not v:
            continue
        v_s = str(v)
        v_l = v_s.lower()
        if "submitted" in v_l or "under review" in v_l:
            continue
        if any(
            x in v_l
            for x in (
                "published", "icml", "neurips", "nips", "iclr", "acl",
                "emnlp", "findings", "tmlr", "mlsys", "poster", "oral",
            )
        ):
            or_title = str(n.get("title") or "")
            if or_title and not titles_compatible(ref.get("title") or "", or_title):
                continue
            if cited_as_arxiv and status != "UPGRADED":
                verified_venue = v_s
                status = "UPGRADED"
                notes.append(f"OpenReview venue: {v_s}")
            break

    if cited_as_arxiv and status == "confirmed_preprint":
        verified_venue = ref.get("venue_current")
        notes.append("No published venue found via Crossref/arXiv journal_ref/OpenReview")

    if not cited_as_arxiv and not verified_venue:
        verified_venue = ref.get("venue_current")

    return {
        "verified_venue": verified_venue,
        "verified_doi": verified_doi,
        "status": status,
        "notes": notes,
        "crossref": {
            "DOI": cr.get("DOI") if cr else None,
            "title": (cr.get("title") or [None])[0] if cr else None,
            "type": cr.get("type") if cr else None,
            "container-title": (cr.get("container-title") or [None])[0] if cr else None,
            "author": cr_authors,
        },
        "arxiv": arx,
        "openreview": or_notes[:5],
    }


def write_corrections_md(refs: list[dict], results: list[dict]) -> None:
    lines = [
        "# Reference Corrections",
        "",
        f"**Generated:** {utc_now_iso()}  ",
        "**Protocol:** v1.1 venue check (OpenReview + Crossref + arXiv)  ",
        f"**Corpus size:** {len(refs)}",
        "",
        "Statuses: `UPGRADED` (preprint → published), `confirmed_preprint`, "
        "`confirmed_published`, `corrected` (metadata fix).",
        "",
        "## Summary",
        "",
    ]
    upgrades = [r for r in results if r.get("status") == "UPGRADED"]
    preprints = [r for r in results if r.get("status") == "confirmed_preprint"]
    lines.append(f"- UPGRADED: **{len(upgrades)}**")
    lines.append(f"- confirmed_preprint: **{len(preprints)}**")
    lines.append(f"- other: **{len(results) - len(upgrades) - len(preprints)}**")
    lines.append("")
    lines.append("## Upgrades (priority)")
    lines.append("")
    if not upgrades:
        lines.append("_No preprint→published upgrades detected in this automated pass._")
        lines.append("")
    for r in upgrades:
        lines.append(f"### {r.get('key')}")
        lines.append(f"- **Title:** {r.get('title')}")
        lines.append(f"- **Manuscript venue:** {r.get('venue_current')}")
        lines.append(f"- **Verified venue:** {r.get('verified_venue')}")
        lines.append(f"- **Verified DOI:** {r.get('verified_doi')}")
        if r.get("check_notes"):
            lines.append(f"- **Notes:** {'; '.join(r['check_notes'])}")
        authors = (r.get("crossref") or {}).get("author") or []
        if authors:
            lines.append(f"- **Crossref authors:** {'; '.join(authors)}")
        lines.append("")

    lines.append("## All HIGH-priority preprint checks")
    lines.append("")
    for r in results:
        if r.get("priority") != "HIGH":
            continue
        lines.append(
            f"- `{r.get('key')}` — **{r.get('status')}** — "
            f"{r.get('verified_venue') or r.get('venue_current')}"
        )
    lines.append("")
    lines.append("## Full table")
    lines.append("")
    lines.append("| key | status | manuscript venue | verified venue | verified DOI |")
    lines.append("|---|---|---|---|---|")
    for r in results:
        lines.append(
            f"| {r.get('key')} | {r.get('status')} | "
            f"{(r.get('venue_current') or '')[:40]} | "
            f"{(r.get('verified_venue') or '')[:40]} | "
            f"{r.get('verified_doi') or ''} |"
        )
    lines.append("")
    CORRECTIONS_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Venue-check existing manuscript references.")
    parser.add_argument("--limit", type=int, default=0, help="Optional cap for smoke tests.")
    args = parser.parse_args()

    bundle = yaml.safe_load(EXISTING_REFS.read_text(encoding="utf-8"))
    refs = bundle.get("references") or []
    if args.limit:
        refs = refs[: args.limit]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "llm-efficient-finetuning-survey/1.1 (mailto:research@local)",
        }
    )

    results_raw = []
    updated_refs = []
    for i, ref in enumerate(refs, start=1):
        title = ref.get("title") or ""
        print(f"[{i}/{len(refs)}] {ref.get('key')}: {title[:70]}", flush=True)
        cr = None
        if ref.get("doi"):
            try:
                cr = crossref_by_doi(session, ref["doi"])
            except Exception as exc:
                print(f"  crossref doi err: {exc}")
        if cr is None and title:
            try:
                cr = crossref_by_title(session, title)
            except Exception as exc:
                print(f"  crossref title err: {exc}")
        time.sleep(0.3)

        arx = None
        if ref.get("arxiv_id"):
            try:
                arx = arxiv_lookup(session, ref["arxiv_id"])
            except Exception as exc:
                print(f"  arxiv err: {exc}")
            time.sleep(3.0)

        or_notes = openreview_lookup(session, title, ref.get("arxiv_id"))

        decision = classify(ref, cr=cr, arx=arx, or_notes=or_notes)
        ref = dict(ref)
        ref["verified_venue"] = decision["verified_venue"]
        ref["verified_doi"] = decision["verified_doi"]
        ref["status"] = decision["status"]
        updated_refs.append(ref)

        row = {
            **{k: ref.get(k) for k in ("key", "title", "year", "venue_current", "priority", "arxiv_id")},
            "verified_venue": decision["verified_venue"],
            "verified_doi": decision["verified_doi"],
            "status": decision["status"],
            "check_notes": decision["notes"],
            "crossref": decision["crossref"],
            "arxiv": decision["arxiv"],
            "openreview": decision["openreview"],
        }
        results_raw.append(row)
        print(f"  -> {decision['status']}: {decision['verified_venue']}", flush=True)

    bundle["references"] = updated_refs
    bundle["venue_check_at"] = utc_now_iso()
    EXISTING_REFS.write_text(
        yaml.dump(bundle, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )

    payload = {
        "mode": "existing_references_venue_check",
        "protocol_version": "1.1",
        "fetched_at": utc_now_iso(),
        "n_references": len(results_raw),
        "results": results_raw,
    }
    save_json(RAW_OUT, payload)
    write_corrections_md(updated_refs, results_raw)
    append_search_log(
        source="openreview",
        block_id="existing_refs",
        query_index=1,
        query="venue check (OpenReview + Crossref + arXiv) for manuscript references",
        n_results=len(results_raw),
        notes=f"Wrote {RAW_OUT.relative_to(REPO_ROOT)} and {CORRECTIONS_MD.relative_to(REPO_ROOT)}",
    )
    print(f"wrote {CORRECTIONS_MD.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
