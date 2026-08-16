# Retention Map — dataset → retention class → enforcement

This is the enforcement-side view of the retention schedule. **Policy
text lives in `jol-m-compliance` (retention schedule)**; this map binds
each dataset in [data-catalog.md](data-catalog.md) to a class and the
mechanism that executes it. Changes require DPO review (CODEOWNERS).

## Retention classes

| Class | Horizon | Meaning |
|-------|---------|---------|
| short-term | ≤ 90 days | Debugging/relevance telemetry; purge window runs monthly |
| operational | ≤ 2 years | Live analytics need; rolling purge yearly |
| statutory | ≤ 10 years | Accounting/tax support (LT VAT OSS: 10y per national rules) |
| indefinite-reference | review every 2y | Synthetic/reference data with no personal data |
| none-synthetic | n/a | 100% synthetic or derived constants; exempt from purge |

## Map

| dataset_id | Class | Enforcement mechanism |
|------------|-------|-----------------------|
| fct_orders | operational | `lifecycle/retention-jobs/` rolling partition drop + re-aggregation |
| dim_products | operational | retention job; tombstoned listings anonymized in place |
| dim_sellers | operational | retention job; seller erasure propagates from product DB (see `lifecycle/anonymization/`) |
| dim_date | none-synthetic | exempt |
| fct_vat_oss | statutory | legal-hold aware; purge only after DPO release |
| fct_commission | statutory | legal-hold aware; purge only after DPO release |
| fct_payouts | statutory | legal-hold aware; purge only after DPO release |
| seller_health | operational | retention job (rolling window) |
| listing_funnel | operational | retention job (rolling window) |
| search_analytics | short-term | monthly purge job |
| dsr_sla_metrics | operational | retention job; aggregates only by construction |
| consent_rates | operational | retention job; aggregates only by construction |
| erasure_execution_log | statutory | legal-hold aware; execution proofs are audit evidence |
| seed_* | none-synthetic | exempt (synthetic by construction) |
| ml_embeddings_products | operational | rebuild on purge; embeddings of erased listings dropped |
| ml_translation_memory | none-synthetic | exempt |

## Enforcement rules

1. **Legal holds suspend, never delete.** A hold flag
   (`lifecycle/legal-hold/`) pauses the job for the affected entities;
   counsel-controlled release.
2. **Erasure propagates.** When the product DB anonymizes a subject
   (`jol-m-marketplace`), `lifecycle/anonymization/` verifies the
   warehouse followed — verification is evidence, kept statutory.
3. **Proofs are sampled.** Post-run proofs + adversarial
   re-identification sampling live in `lifecycle/verification/`.
