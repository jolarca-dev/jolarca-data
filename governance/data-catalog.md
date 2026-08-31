# Data Catalog — master index

Every dataset this repository creates, transforms, or serves. One row =
one dataset. The machine-readable mirror is
[ownership-register.csv](ownership-register.csv); `catalog-lint` keeps
them consistent and blocks orphans.

Tiers per [classification.md](classification.md); retention classes per
[retention-map.md](retention-map.md); RoPA purposes live in
`jolarca-compliance` (referenced by id, never restated here).

| dataset_id | Description | Business owner | Technical steward | Classification | RoPA purpose | Retention class |
|------------|-------------|----------------|-------------------|----------------|--------------|-----------------|
| fct_orders | Order facts, pseudonymous keys, EUR amounts | Marketplace product | Data platform | CONFIDENTIAL | ropa-analytics-marketplace | operational |
| dim_products | Product dimension (taxonomy-linked) | Marketplace product | Data platform | INTERNAL | ropa-analytics-marketplace | operational |
| dim_sellers | Seller dimension, pseudonymized | Marketplace product | Data platform | CONFIDENTIAL | ropa-analytics-marketplace | operational |
| dim_date | Calendar dimension (synthetic reference) | Data platform | Data platform | PUBLIC | n/a | none-synthetic |
| fct_vat_oss | VAT OSS reporting support facts | Finance | Data platform | CONFIDENTIAL | ropa-tax-compliance | statutory |
| fct_commission | Commission facts per order | Finance | Data platform | CONFIDENTIAL | ropa-tax-compliance | statutory |
| fct_payouts | Payout facts (Stripe metadata only) | Finance | Data platform | CONFIDENTIAL | ropa-tax-compliance | statutory |
| seller_health | Seller health aggregates | Marketplace product | Data platform | CONFIDENTIAL | ropa-analytics-marketplace | operational |
| listing_funnel | Listing funnel aggregates | Marketplace product | Data platform | INTERNAL | ropa-analytics-marketplace | operational |
| search_analytics | Search relevance aggregates | Marketplace product | Data platform | INTERNAL | ropa-analytics-marketplace | short-term |
| dsr_sla_metrics | DSAR/DSR SLA aggregates | DPO | Data platform | RESTRICTED | ropa-gdpr-operations | operational |
| consent_rates | Consent opt-in aggregates | DPO | Data platform | RESTRICTED | ropa-gdpr-operations | operational |
| erasure_execution_log | Erasure execution aggregates (no subject rows) | DPO | Data platform | RESTRICTED | ropa-gdpr-operations | statutory |
| seed_taxonomy_categories | Marketplace category tree (synthetic reference) | Marketplace product | Data platform | PUBLIC | n/a | none-synthetic |
| seed_geo_references | LT/LV/EE municipalities, parishes, locker refs | Marketplace product | Data platform | PUBLIC | n/a | none-synthetic |
| seed_tax_vat_rates | VAT rate reference per category/country | Finance | Data platform | INTERNAL | n/a | none-synthetic |
| seed_fixtures | Synthetic sellers/products/orders fixtures | Marketplace product | Data platform | PUBLIC | n/a | none-synthetic |
| ml_embeddings_products | Product-description embedding builds | Data platform | Data platform | INTERNAL | ropa-search-relevance | operational |
| ml_translation_memory | Domain glossary pairs lt/lv/et/en | Marketplace product | Data platform | PUBLIC | n/a | none-synthetic |

## Adding a dataset

1. Open a `dataset_request` issue (purpose, classification, retention,
   ownership are mandatory fields).
2. Add the row here **and** in `ownership-register.csv`.
3. Register the retention class in `retention-map.md`.
4. For critical datasets, add a lineage diagram in `lineage.md`.
5. `make catalog-lint` must pass before merge.
