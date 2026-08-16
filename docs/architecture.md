# Architecture — jol-m-data

Template-inherited baseline, extended with the platform data flow.

## Position in the fleet

| Repo | Relationship |
|------|--------------|
| `jol-m-marketplace` | Source of truth (production); this repo reads a pseudonymized copy, never writes |
| `jol-m-compliance` | Retention policy, RoPA, GDPR evidence; this repo executes policy as code |
| `jol-m-legal` | Legal glossary (translation-memory sync), DSA transparency data requests |
| `jol-m-infrastructure` | Warehouse hosting, secrets, network planes; runs extract-role grants |

## Data flow (prod → pseudonymized → marts)

```mermaid
flowchart LR
  subgraph PROD [jol-m-marketplace production]
    P[(orders/products/users)] --> R[(read replica)]
  end
  subgraph BOUNDARY [pseudonymization boundary — ADR-0001]
    R --> EX[postgres_extract\nread-only role]
    S[Stripe API] --> SE[stripe_extract\nmetadata only, never PAN]
    EX --> PZ[pseudonymizer\nfail-closed rules]
    SE --> PZ
  end
  PZ --> RAW[(warehouse raw\nEU region)]
  RAW --> STG[staging — PII stripped]
  STG --> INT[intermediate]
  INT --> MARTS[marts: core / finance / marketplace / compliance]
  MARTS --> C1[dashboards]
  MARTS --> C2[VAT-OSS filing support]
  MARTS --> C3[ai_service_app embeddings]
```

The boundary is the design: nothing downstream of the pseudonymizer can
re-identify a subject without external collusion (salt held outside the
warehouse, keys held in the product boundary).

## Key components

- **Governance catalog** (`governance/`) — registration, ownership,
  classification, retention for every dataset; CI blocks orphans.
- **Seed & taxonomy** (`seed/`) — the marketplace domain model and
  synthetic fixtures; schema-validated.
- **Warehouse** (`warehouse/`) — dbt models from staging to marts;
  custom tests encode pseudonymization/EUR/VAT invariants.
- **Lifecycle machinery** (`lifecycle/`) — retention jobs, erasure
  verification, legal holds, adversarial re-identification sampling.

## Constraints

1. EU region only for warehouse storage and processing.
2. No production credentials in analytics (ADR-0002).
3. Compliance marts are aggregates only.
4. Analytics is rebuildable from sources; production backups live in
   `jol-m-infrastructure`, not here.
