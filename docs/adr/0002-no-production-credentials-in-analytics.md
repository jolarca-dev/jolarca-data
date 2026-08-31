# ADR-0002: No production credentials in analytics

- Status: Accepted
- Date: 2026-08-15
- Deciders: data platform owner, security function

## Context

Analytics pipelines historically become the weakest credential
boundary: dashboards, notebooks, and ETL jobs accumulate broad
database access. A compromised analytics credential must not yield a
production path. SOC 2 CC6 (logical access) and least-privilege
practice require separation.

## Decision

1. Analytics never holds production credentials. The warehouse and
   notebooks connect to a dedicated analytics database in the EU
   region; credentials come from environment secrets only
   (`profiles.yml.example`/`.envrc.example` document names, never
   values).
2. Extraction connects to the **read replica** with a read-only,
   table-scoped role (`ingestion/pipelines/postgres_extract/extract-role.sql`);
   no write path to production exists from this repository's tooling.
3. Third-party extracts (Stripe) use restricted-scope keys
   (`ingestion/contracts/stripe.yml`).
4. CI never connects to staging/production — it builds an ephemeral
   warehouse from the synthetic raw schema.

## Consequences

- Analytics cannot "just fix" production data incidents — correct
  behavior; production changes route through `jolarca`
  change management.
- Two credential custody chains exist (infra-owned); rotation follows
  `jolarca-infrastructure` runbooks.
- A leaked analytics credential degrades to analytics scope only.
