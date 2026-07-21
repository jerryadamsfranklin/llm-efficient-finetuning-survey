# Search Protocol

**Status:** Placeholder — Phase 1 content to be written and committed before any search runs.
**Protocol version:** TBD
**Coverage window:** 2019-01-01 to 2026-06-30 (recommended; finalize before Phase 2)
**Framing:** Structured, protocol-driven search (PRISMA-informed counts; not a registered systematic review)

## Databases

### Automated
- arXiv
- Semantic Scholar
- OpenReview
- Papers With Code (implementation availability)
- Crossref (DOI / venue verification)

### Manual
- Google Scholar
- IEEE Xplore
- ACM Digital Library
- Hugging Face documentation (reference source, not discovery)

## Query blocks

See `search/queries.yaml` (to be written in Phase 1).

## Stopping rule (manual sources)

Screen the first 50 results by relevance per query (defensible, stated rule).

## Search dates

Record actual execution dates in `search/search-log.md`. Do not backdate.
