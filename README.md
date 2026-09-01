# jolarca-data — Data Platform Repository

**Private** repository for the Journey of Life marketplace data function
(`jolarca-*` fleet). Seed & reference data, the analytics warehouse (dbt),
ingestion contracts, data quality, retention machinery, synthetic data,
and ML dataset governance live here.

> **Prime directive:** personal data never lands in the warehouse in
> cleartext. Ingestion pseudonymizes at the boundary (ADR-0001); the
> warehouse models aggregates and pseudonymous keys only. If you find
> cleartext PII anywhere downstream of ingestion, that is an incident —
> see [docs/runbooks/pii-detected-in-warehouse.md](docs/runbooks/pii-detected-in-warehouse.md).

## What this repository is

- **Governance catalog is the heart** (`governance/`): every dataset is
  registered, owned, classified, and retention-mapped. Orphan datasets
  are blocked by CI (`catalog-lint.py`).
- **Seed & reference data** (`seed/`): the marketplace taxonomy
  (categories, attributes, translations LT/LV/EE/EN/RU), geo/tax
  references, and 100% synthetic fixtures — the knowledge spine that
  `jolarca` and demo environments load.
- **Analytics warehouse** (`warehouse/`): dbt project; staging strips
  identifiers, marts serve finance (VAT OSS), marketplace, and
  compliance analytics. EU region only.
- **Retention & anonymization as code** (`lifecycle/`): executes the
  retention schedule whose policy text lives in `jolarca-compliance`.

## Access tiers & data classification

Four tiers, handling rules in [governance/classification.md](governance/classification.md):

| Tier | Meaning | Examples here |
|------|---------|---------------|
| PUBLIC | publishable | taxonomy structure (via marketplace), docs in public artifacts |
| INTERNAL | any org member | dashboards definitions, dbt models, runbooks |
| CONFIDENTIAL | data/finance/compliance roles | commission models, seller aggregates, VAT filings support |
| RESTRICTED | personal data / DPO-controlled | erasure logs (aggregates), consent metrics, legal-hold flags |

## Ownership

| Role | Contact | Owns |
|------|---------|------|
| Data platform owner | TBD — fill on onboarding | `warehouse/`, `ingestion/`, `scripts/` |
| DPO (`jolarca-compliance`) | TBD | anything touching RESTRICTED data; CODEOWNERS gate (§3) |
| Marketplace product owner | TBD | `seed/taxonomy/`, `seed/fixtures/` |
| Finance | TBD | `warehouse/models/marts/finance/`, `seed/tax/` |

Cross-repo boundaries: retention **policy** and GDPR evidence (RoPA,
DSAR logs) live in `jolarca-compliance`; this repo executes the policy as
code. Legal texts and glossaries sync from `jolarca-legal`
(`ml/translation-memory/`). Production backups are **not** here —
analytics is rebuildable from sources ([docs/runbooks/restore-analytics.md](docs/runbooks/restore-analytics.md)).

## Repository map

| Path | Purpose |
|------|---------|
| `governance/` | Catalog, classification, ownership register, retention map, lineage |
| `seed/` | Taxonomy + translations, geo/tax references, synthetic fixtures, JSON Schema validators |
| `warehouse/` | dbt project: staging (PII stripped), intermediate, marts, tests, macros, seeds |
| `ingestion/` | Extract pipelines, the pseudonymizer, schema contracts (field allow-lists) |
| `quality/` | Great Expectations suites, anomaly rules, weekly scorecards |
| `lifecycle/` | Retention jobs, erasure verification, legal holds, adversarial re-ID tests |
| `synthetic/` | Generators (lt/lv/et-aware), PII canaries, golden regression datasets |
| `ml/` | Embedding builds, relevance eval sets, translation memory |
| `docs/` | Architecture, ADRs, metrics dictionary, runbooks, DPIA template |
| `scripts/` | Seed validation, PII scan, catalog lint, freshness report, anonymization verify |
| `audits/` | Internal audit records for this repository |

## Quickstart

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -e .
make check           # seed schema validation + catalog lint + PII tripwire (no credentials)
make seed-validate   # JSON Schema validation of every seed/taxonomy file
make quality         # data-quality expectations (staging warehouse, needs env)
make dbt-build       # dbt build against the dev warehouse profile (needs env)
make anonymize-verify # adversarial re-identification sampler (lifecycle)
```

Warehouse/ingestion targets require the environment variables from
[.envrc.example](.envrc.example) (never real credentials in-repo —
ADR-0002). `make check` runs without any credentials.

## Change discipline

Every dataset change carries classification, RoPA purpose, and retention
class (PR template enforces). Commits follow Conventional Commits;
notable changes land in `CHANGELOG.md`. PII detected in committed data
or in the warehouse is a severity-1 class incident with DPO notification
([SECURITY.md](SECURITY.md)).
