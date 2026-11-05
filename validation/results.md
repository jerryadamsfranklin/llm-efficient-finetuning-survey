# Screening validation results

Computed by scripts/score_validation.py from committed blind and key files. Key hashes verified.

A disagreement is a row where the author decision differs from the classifier decision.

| Population | n | Classifier decision | Author disagrees | Rate | Wilson 95% CI |
|---|---:|---|---:|---:|---|
| A | 721 | exclude 721 | 200 | 27.7% | 24.6% to 31.1% |
| B | 300 | exclude 300 | 68 | 22.7% | 18.3% to 27.7% |
| C | 900 | include 900 | 264 | 29.3% | 26.5% to 32.4% |
| D1 | 100 | include 100 | 27 | 27.0% | 19.3% to 36.4% |
| D2 | 100 | exclude 100 | 18 | 18.0% | 11.7% to 26.7% |

## Population B by year

| Stratum | n | Author includes | Rate |
|---|---:|---:|---:|
| 2024 | 107 | 15 | 14.0% |
| 2025 | 127 | 34 | 26.8% |
| 2026 | 66 | 19 | 28.8% |

## Population B by canonical source

| Stratum | n | Author includes | Rate |
|---|---:|---:|---:|
| arxiv | 188 | 38 | 20.2% |
| google_scholar | 8 | 2 | 25.0% |
| ieee | 14 | 2 | 14.3% |
| openalex | 7 | 1 | 14.3% |
| openalex_acm | 12 | 1 | 8.3% |
| semanticscholar | 71 | 24 | 33.8% |
