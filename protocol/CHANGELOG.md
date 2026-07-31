# Protocol Changelog

## Phase 3 entry — 2026-07-31 (artifact regeneration, no protocol change)

The search protocol, queries, coverage window, and inclusion/exclusion criteria are
unchanged. Recorded here because published Phase 2 counts moved slightly.

### Candidate pool regenerated to carry screening metadata

`search/scripts/dedupe.py` discarded three fields the screening criteria depend on.
It now carries them from the raw responses already on disk; **no source was re-queried**
and `search/raw/` is byte-identical to the Phase 2 state.

- **Citation counts** (`citations`, `citations_source`) from Semantic Scholar
  `citationCount`, OpenAlex `cited_by_count`, IEEE `citing_paper_count`, and the
  Scholar `cited_by` column. Inclusion criterion 3 cannot be applied without these.
- **Language** (OpenAlex `language`) for criterion 4, and **record type** for
  exclusion criterion 6.
- **Abstracts** reconstructed from OpenAlex `abstract_inverted_index`, which was
  previously dropped. Abstract coverage rose from 9,000 to 9,899 of the pool, which
  matters because Stage 1 is a title/abstract screen.

Two merge refinements, both narrowing rather than widening the pool:

- arXiv IDs are now also read from OpenAlex alternate `locations`, not `ids` alone.
  This merged one additional preprint/published pair: **unique candidates 10,334 →
  10,333**, arXiv-ID coverage 7,782 → 7,974, multi-source merges 1,538 → 1,537.
- Merged clusters now take the longest abstract and the highest citation count from
  any record in the cluster, rather than only the canonical record's. The canonical
  (published) record frequently carried no abstract while its merged preprint did.

Pre-dedup record count is unchanged at **18,343**, confirming the regeneration did not
alter retrieval. Counts in `screening/prisma-counts.md` are updated accordingly.

### Stray duplicate files removed from the working tree

124 byte-identical `"<name> 2.json"` / `"<name> 2.py"` copies (file-manager artifacts,
never tracked by git) were present under `search/raw/` and `search/scripts/`. They
inflated a dedup run to 28,646 raw records before removal. All were verified identical
to their tracked originals by checksum and moved out of the repository. Tracked files
were untouched.

---

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

### Execution outcome (recorded at Phase 2 close, 2026-07-31)

All v1.2 sources ran to completion: IEEE 18/18 (705 records), OpenAlex general
18/18 (900), OpenAlex ACM-filtered 18/18 (636), DBLP 18/18 (164), Google Scholar
18 protocol queries as 34 manual runs (597 records after removing interface
artifacts and one duplicate).

Deduplication across all seven sources reduced **18,343** retrieved records to
**10,334** unique candidates (**10,313** excluding Scholar out-of-protocol rows).
This exceeds the 6,000–7,000 figure the amendment used when arguing for the
50-record cap. The discrepancy comes from arXiv date-slicing under v1.1 (11,841
records across 119 sliced query files), not from the v1.2 substituted sources,
which contributed 2,405 capped records in total. The cap did what it was intended
to do; the pre-existing arXiv volume was simply larger than the amendment
assumed. Stage 1 screening should be planned against 10,313, not 7,000.

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
