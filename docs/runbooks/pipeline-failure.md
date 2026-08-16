# Runbook — pipeline failure

**Goal:** restore the affected pipeline, quantify the stale window, and
decide whether downstream consumers must be marked stale.

## Triage per pipeline

| Pipeline | First check | Likely cause | Fix path |
|----------|-------------|--------------|----------|
| postgres_extract | extract role connectivity to replica | replica lag, role grant drift, network plane | verify replica health (`jol-m-infrastructure`), re-run nightly batch |
| stripe_extract | restricted key scope/quota | key rotation, Stripe outage | rotate via `.envrc`, backfill the window |
| pseudonymizer | rule parse errors / fail-closed drop | rules.yml change, unknown field | never "fix" by loosening rules — open DPO-reviewed contract change |
| dbt build | failing test vs failing model | upstream drift, schema change | run `dbt build` locally with dev profile; check `_staging.yml` contract |
| quality gates | which expectation failed | real data issue vs threshold | real issue → bug report; threshold → anomaly-rules review with owner |

## Who to page

- Data platform owner: pipeline/dbt failures.
- DPO: anything where the failure may involve personal data handling
  (pseudonymizer, erasure propagation).
- Finance: VAT-OSS support figures stale during filing window.

## After recovery

1. Backfill the stale window; record it in the freshness report.
2. Mark affected dashboards stale until refresh completes.
3. If the failure exceeded the freshness SLA, the freshness-monitor
   issue is the record; close it with the backfill evidence.
