# Changelog — jolarca-data

All notable changes to this data-platform repository are documented
here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
commits follow Conventional Commits. Never rewrite released entries.

## [Unreleased]

### Added

- Repository scaffold: governance (catalog, classification, ownership
  register, retention map, lineage), seed (taxonomy + lt/lv/et/en/ru
  translations, geo, tax, synthetic fixtures, JSON Schema validators),
  warehouse (dbt project with staging/intermediate/marts, custom tests,
  macros, static seeds), ingestion (postgres/stripe extracts,
  pseudonymizer, schema contracts), quality (expectations, anomaly
  rules, scorecards), lifecycle (retention jobs, erasure verification,
  legal holds), synthetic (generators, PII canaries, regression goldens),
  ml (embeddings, evaluation, translation memory), docs, scripts.
- Root compliance baseline: README (prime directive, access tiers),
  LICENSE (internal use + synthetic-data exception), SECURITY.md
  (PII incidents = highest severity, DPO first), CONTRIBUTING.md (seed
  doctrine, warehouse doctrine, governance mandate).
- CI/CD: ci + compliance-check gates, dbt-ci (sqlfluff → parse → slim
  build → tests), data-quality, pii-scan (scheduled), freshness-monitor.
- Pre-commit baseline + gitleaks + sqlfluff + PII pattern scan + dbt
  parse check.
- Scripts: validate-seed, scan-warehouse-pii, catalog-lint,
  freshness-report, verify-anonymization, check-personal-data.
- ADR-0001: pseudonymize at ingestion; ADR-0002: no production
  credentials in analytics.
- Metrics dictionary (GMV, take-rate, active seller — one definition
  each), runbooks (pipeline-failure, pii-detected, restore-analytics).
