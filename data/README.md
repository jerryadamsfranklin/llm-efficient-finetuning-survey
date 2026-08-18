# Data artifacts (Phase 4 — not yet populated)

These files are **header-only templates**. Extraction against
`protocol/extraction-schema.md` has not started.

| File | Purpose |
|---|---|
| `included-papers.csv` | Final included corpus with extraction fields |
| `references.bib` | BibTeX generated from `included-papers.csv` |
| `table1_adapters.csv` … `table5_configurations.csv` | Manuscript comparison tables |

Each CSV begins with a `# Status:` comment line visible in a text editor. CSV parsers
should skip lines starting with `#` when these files are populated in Phase 4.
