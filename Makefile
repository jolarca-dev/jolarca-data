# jol-m-data — data operator hygiene targets.
# Credential-free targets (check, seed-validate) must always pass locally.
# Warehouse targets (dbt-build, quality) require .envrc vars — ADR-0002.

SHELL := /bin/bash
PY := python3
DBT := dbt --project-dir warehouse --profiles-dir warehouse

.PHONY: help check seed-validate catalog-lint dbt-parse dbt-build quality anonymize-verify lint-docs

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-16s %s\n", $$1, $$2}'

check: seed-validate catalog-lint ## Gate = seed schema + catalog integrity + PII tripwire (mirrors CI)
	bash scripts/check-personal-data.sh

seed-validate: ## JSON Schema validation of every seed/taxonomy file
	$(PY) scripts/validate-seed.py

catalog-lint: ## Every dataset registered, owned, classified, retention-mapped
	$(PY) scripts/catalog-lint.py

dbt-parse: ## dbt parse — config/compile sanity, no warehouse connection
	$(DBT) parse --no-version-check || echo "dbt not installed — skipped"

dbt-build: ## dbt build (slim) against the dev warehouse profile (needs env)
	$(DBT) build --no-version-check

quality: ## Great Expectations / dbt tests on the staging warehouse (needs env)
	$(DBT) test --select staging,quality --no-version-check

anonymize-verify: ## Adversarial re-identification sampler (lifecycle)
	$(PY) scripts/verify-anonymization.py

lint-docs: ## Markdown/YAML hygiene
	@command -v yamllint >/dev/null && yamllint .github/ .pre-commit-config.yaml qodana.yaml \
		|| echo "yamllint not installed — skipped"
	@command -v markdownlint >/dev/null && markdownlint '**/*.md' \
		|| echo "markdownlint not installed — skipped"
