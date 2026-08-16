# Metrics Dictionary

Business definitions — **ONE definition each, used everywhere**. A
dashboard or model that deviates from these definitions is a bug.
Metric changes are PRs against this file first; the SQL follows.

| Metric | Definition | Implementation | Owner |
|--------|------------|----------------|-------|
| GMV | Gross merchandise value: sum of `amount_eur` over orders with status in (paid, shipped, delivered). Refunds reduce GMV at refund event time. | `fct_orders` filtered by `is_revenue` | data-platform |
| Net GMV | GMV minus refunded amounts within the same reporting period. | `fct_orders` | data-platform |
| Take rate | Commission earned ÷ GMV over the same period, per seller cohort or platform-wide. | `fct_commission` ÷ `fct_orders` | finance |
| Active seller | Seller with ≥ 1 order in (paid, shipped, delivered) in the trailing 90 days. | `int_seller_lifecycle.lifecycle_stage = 'active'` | marketplace-product |
| Conversion | Orders ÷ distinct listing views (search/telemetry source pending — scaffold). | `listing_funnel` proxy until search telemetry lands | marketplace-product |
| Refund rate | Refunded orders ÷ total orders per seller/period. | `seller_health.refund_rate` | marketplace-product |
| Consent rate | Marketing opt-ins ÷ accounts in cohort month, per country. Aggregate only. | `consent_rates` | dpo |
| DSR SLA adherence | DSARs answered within statutory deadline ÷ DSARs received, per month. Aggregate only. | `dsr_sla_metrics` | dpo |
| OSS-support net | Net taxable amount per destination country/quarter/rate (reporting support, not the filing). | `fct_vat_oss` | finance |

## Rules

1. New metrics require: definition here, implementation reference,
   owner — and a catalog entry if backed by a new dataset.
2. Periods are UTC calendar periods; VAT reporting uses calendar
   quarters.
3. Money is EUR, decimal(12,2), converted from integer cents by
   `cents_to_eur` — never floats.
