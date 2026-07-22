# Protocol Changelog

## v1.2 — 2026-07-22

Phase 2b source-substitution amendment. Triggered because v1.0/v1.1 classified
IEEE Xplore and ACM Digital Library as manual-only, which was partly incorrect.

### Change: programmatic retrieval for IEEE and ACM coverage

- **IEEE Xplore:** official Metadata Search API (`ieeexploreapi.ieee.org`) with
  free key registration. Boolean queries, year filter, abstracts. Cap:
  **top 50 by relevance per query** (equivalent to the manual stopping rule).
- **ACM Digital Library:** no public search API. ACM-published works retrieved
  via **OpenAlex** (and Crossref for DOI/venue verification), including an
  ACM publisher-filtered OpenAlex run. Keyword `s2_queries` variants; cap 50.
- **OpenAlex (general index):** same keyword queries and 50-cap, for broader
  coverage beyond ACM.
- **ACM publisher ID:** amendment draft cited `P4310320503`; OpenAlex lookup
  confirmed **Association for Computing Machinery** as `P4310319798` (recorded
  in `search/queries.yaml`). Scripts verify the publisher display name before
  the ACM-filtered run.
- **DBLP (optional):** CS-venue completeness check; same 50-cap. Adopted for
  venue-string quality without expanding screening burden beyond the cap.
- **Google Scholar:** unchanged — still manual; no scraping.

### Unchanged from v1.1 / v1.0

Coverage window, inclusion/exclusion, extraction schema, arXiv/S2/OpenReview
decisions, 200-cap date-slicing for arXiv, prohibition on Scholar scraping,
single-author non-PRISMA framing. This is a **retrieval-mechanism** change,
not a scope change.

### Sequencing

v1.2 protocol text must be committed **before** IEEE / OpenAlex / DBLP runs.

---

## v1.1 — 2026-07-21

Triggered by execution of v1.0 (commit d7313cd). Three defects identified.

### Defect 1: Operator precedence error in B3_memory_3

v1.0 string: `"ZeRO" OR "DeepSpeed" OR "offloading" AND "model training"`  
Boolean precedence binds AND tighter than OR, parsing this as
`ZeRO OR DeepSpeed OR (offloading AND "model training")`. Unbounded on the
first two terms. Evidence: arXiv totalReported approximately 17,852.  
Fix: explicit parentheses. See `docs/PROTOCOL_V1.1_AMENDMENT.md` section 3.1
(local amendment guide) / corrected string in `search/queries.yaml`.

### Defect 2: Query syntax incompatible with Semantic Scholar API

v1.0 specified one boolean syntax for all sources. The Semantic Scholar
`query=` parameter performs relevance keyword matching, not boolean
evaluation. Evidence: B2_quantization_2 returned 0 results,
B3_memory_2 returned 0, B1_peft_2 returned 1.  
Fix: source-specific `s2_queries` keyword variants in `search/queries.yaml`.

### Defect 3: Retrieval cap reached without coverage strategy

9 of 18 arXiv queries reached the 200-result cap with larger totals
reported. v1.0 stated "narrow the query and record the change" but did
not specify a method preserving search intent.  
Fix: date-slicing plus explicit stopping rule (amendment sections 4–5).
Implementation of `--slice-by-year` follows after this amendment is committed
and confirmed.

### Unchanged from v1.0

Coverage window, inclusion/exclusion criteria, extraction schema,
manual stopping rule (first 50 by relevance), prohibition on scraping
Google Scholar, single-author non-PRISMA framing.

### Artifact handling

- v1.0 raw API responses preserved under `search/raw_v1.0/` (not deleted).
- Fresh v1.1 runs will write to `search/raw/` after owner confirmation.
