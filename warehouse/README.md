# Warehouse — analytics warehouse (dbt)

Doctrine:

1. **Pseudonymized landing.** Personal data is pseudonymized at the
   ingestion boundary (ADR-0001); staging models here hash identifiers
   and drop names/emails. A model that re-introduces an identifier is a
   defect of the highest class.
2. **dbt-managed.** Everything downstream of raw is built by dbt;
   manual table edits are prohibited. Every model is documented in
   `models/**/_models.yml` with owner + tests.
3. **EU region only.** The warehouse runs in an EU-region Postgres;
   cross-region replication is prohibited.
4. **No production credentials.** Access is via env vars
   (`profiles.yml.example` documents them); extraction is read-replica
   only, least privilege (ADR-0002).

## Layout

| Path | Content |
|------|---------|
| `models/staging/` | stg_orders, stg_products, stg_users — **PII stripped here** (hashed IDs, no names/emails) + source freshness SLAs |
| `models/intermediate/` | int_order_items_enriched, int_seller_lifecycle |
| `models/marts/core/` | fct_orders, dim_products, dim_sellers (pseudonymized), dim_date |
| `models/marts/finance/` | fct_vat_oss (OSS reporting support), fct_commission, fct_payouts |
| `models/marts/marketplace/` | seller_health, listing_funnel, search_analytics |
| `models/marts/compliance/` | dsr_sla_metrics, consent_rates, erasure_execution_log — **aggregates only** |
| `tests/` | Custom tests: no-null-pii-columns, id-hash-format, eur-only, vat-rate-bounds |
| `macros/` | hash_id(), pseudonymize(), cents_to_eur(), locale dimension helpers |
| `seeds/` | Static dims: countries, currencies, vat_rates snapshot |

## Local usage

```bash
cp .envrc.example ../.envrc   # fill from Vaultwarden, never commit
dbt deps && dbt build         # or: make dbt-build from repo root
```

CI builds against an ephemeral warehouse loaded with the synthetic raw
schema (`.github/workflows/ci-raw-schema.sql`) — staging/production are
never touched by CI.
