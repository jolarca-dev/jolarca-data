# Data Quality — every mart has expectations

Doctrine:

1. **Every mart has expectations.** A model without declared
   expectations is a debt item, tracked in the scorecard.
2. **Failed expectation = blocked pipeline.** Quality gates run before
   downstream refresh (`make quality`, `data-quality.yml`); a failing
   expectation blocks the consumer refresh, not just warns.
3. **Anomalies are rules, not vibes.** Volume/distribution anomalies
   are declared in `anomaly-rules/` with thresholds and owners.
4. **Scorecards feed management review.** Weekly quality scores per
   domain live in `scorecards/` and are input to the governance review
   cadence (`governance/README.md`).

## Layout

| Path | Content |
|------|---------|
| `expectations/` | Great Expectations-style suites: orders, products, vat |
| `anomaly-rules/` | Volume/distribution anomaly rules per critical table |
| `scorecards/` | Weekly data-quality score per domain |

Expectations execute via `make quality` (dbt tests + GE suites against
the staging warehouse); dbt tests in `warehouse/tests/` are the first
line, these suites are the second.
