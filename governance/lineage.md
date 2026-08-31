# Lineage — source → ingestion → warehouse → consumer

Per critical dataset. The pseudonymization boundary is the single most
important edge in every diagram: **nothing downstream of it may carry
cleartext identifiers** (ADR-0001).

## Orders (fct_orders)

```mermaid
flowchart LR
  subgraph Production [jolarca production]
    A[(orders table)] --> B[(read replica)]
  end
  B -->|"read-only role\nleast privilege"| C[pseudonymizer\nhash buyer/seller IDs]
  C -->|"pseudonymous landing\n(ingestion contract)"| D[(warehouse raw)]
  D --> E[stg_orders — PII stripped]
  E --> F[int_order_items_enriched]
  F --> G[fct_orders]
  G --> H1[dashboards]
  G --> H2[fct_vat_oss]
```

## Sellers (dim_sellers)

```mermaid
flowchart LR
  A[(users table — sellers)] --> B[(read replica)]
  B --> C[pseudonymizer — hash IDs, drop names/emails]
  C --> D[(warehouse raw.users)]
  D --> E[stg_users — role/country/consent aggregates only]
  E --> F[dim_sellers — pseudonymized]
  F --> G[seller_health]
```

## Payments (fct_payouts)

```mermaid
flowchart LR
  S[Stripe API] -->|"restricted key:\ncharges/payouts metadata only\n(never PAN — SAQ-A)"| C[pseudonymizer — account refs hashed]
  C --> D[(warehouse raw)]
  D --> E[fct_payouts]
  E --> F[fct_commission]
```

## Erasure propagation

```mermaid
flowchart LR
  M[jolarca: DSAR erasure executed] --> V[lifecycle/anonymization verify job]
  V --> W{warehouse rows for hashed subject gone/anonymized?}
  W -->|yes| P[lifecycle/verification: proof recorded]
  W -->|no| I[pii_incident issue → DPO]
```

## Maintenance rule

Any new critical dataset (CONFIDENTIAL/RESTRICTED or feeding finance
reporting) must land with a lineage diagram here in the same PR;
`dataset_request` intake asks for sources explicitly.
