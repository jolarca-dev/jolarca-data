# Quality Scorecards — weekly data-quality score per domain

One file per ISO week: `YYYY-Www.md`, produced from expectation and
anomaly run results (automation lands with the warehouse environment).
Scorecards feed the governance review cadence.

## Score definition

| Component | Weight | Source |
|-----------|--------|--------|
| Blocking expectations pass rate | 50% | quality/expectations runs |
| dbt test pass rate | 25% | dbt-ci / quality runs |
| Freshness SLA adherence | 15% | freshness-monitor |
| Anomaly alerts (absence) | 10% | anomaly-rules |

## Template

```markdown
# Quality scorecard — <YYYY-Www>

| Domain | Score | Blocking failures | Notes |
|--------|-------|-------------------|-------|
| orders |       |                   |       |
| products |     |                   |       |
| vat |          |                   |       |
| compliance |   |                   |       |

Actions carried into next week:
- ...
```
