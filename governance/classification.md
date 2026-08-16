# Data Classification — four tiers

Every dataset in [data-catalog.md](data-catalog.md) carries exactly one
tier. Tier changes are critical-risk changes: DPO approval required,
CODEOWNERS routes it.

## Tiers

### PUBLIC

Publishable outside the org (typically only via product surfaces).

- Examples: taxonomy structure, synthetic fixtures, calendar dimension.
- Handling: still no secrets, no credentials; review before any
  external publication path.

### INTERNAL

Any org member; not for external distribution.

- Examples: dbt models, dashboards definitions, runbooks, funnel
  aggregates.
- Handling: standard access; no personal data.

### CONFIDENTIAL

Need-to-know: data, finance, and compliance roles.

- Examples: seller/buyer aggregates, commission and VAT figures,
  pseudonymized dimensions whose join key is held elsewhere.
- Handling: no export to personal devices; dashboard access gated;
  quarterly re-attestation.

### RESTRICTED

Personal data or data directly derived from it; DPO-controlled.

- Examples: DSAR SLA metrics, consent rates, erasure execution
  aggregates.
- Handling: aggregates only — never per-subject rows in this
  repository's artifacts; DPO review on every change; access logged;
  retention enforced by `lifecycle/retention-jobs/`.

## Handling rules common to all tiers

1. No credentials, ever (gitleaks enforces).
2. No cleartext personal data, ever — the pseudonymization boundary is
   at ingestion (ADR-0001), and committed fixtures are synthetic.
3. Tier is declared in the catalog at dataset creation; "decide later"
   is not a valid state — undeclared datasets are blocked.
4. When in doubt between two tiers, choose the higher one and raise it
   in the quarterly review.
