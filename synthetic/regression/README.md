# Regression — golden datasets for dbt/pipeline regression testing

Golden inputs + expected outputs for regression coverage of:

1. **dbt model logic** — synthetic raw rows (subset of the dbt-ci raw
   schema) with hand-computed expected mart rows (VAT decomposition,
   commission, funnel counts).
2. **Pseudonymizer behavior** — input records with expected landed
   shape; doubles as documentation of fail-closed semantics
   (`ingestion/pipelines/pseudonymizer/test_pseudonymizer.py` runs the
   live assertions).

## Rules

- Goldens are committed YAML derived from `seed/fixtures/` — never
  production data, never generated at test time (drift detection
  requires stable goldens).
- A golden change is a behavior declaration: the PR must explain which
  metric definition changed (see `docs/metrics-dictionary.md`).
- Run via dbt-ci (ephemeral warehouse) and `make check` (pure-Python
  suites); no credentials required.
