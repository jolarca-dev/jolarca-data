# ADR-0001: Pseudonymize at ingestion

- Status: Accepted
- Date: 2026-08-15
- Deciders: data platform owner, DPO

## Context

The marketplace needs analytics (seller health, VAT-OSS support,
search relevance) over data that is personal at source. GDPR Art. 25
(data protection by design) and Art. 32 (security of processing)
require minimization and pseudonymization; a warehouse holding
cleartext identities would make every analytics incident a personal
data breach and expand DSAR/erasure surface to every mart.

## Decision

Personal identifiers are pseudonymized **at the ingestion boundary** —
before landing in the analytics warehouse:

1. Numeric subject ids are salted hashes (`hash_id`); free-text
   identifiers are dropped or hashed (`pseudonymizer/rules.yml`,
   fail-closed default: drop).
2. Names, emails, phones, registry codes never leave the source
   (contract allow-lists in `ingestion/contracts/`).
3. The hash salt is held outside the warehouse; re-identification
   requires collusion across system boundaries.

## Consequences

- The warehouse cannot answer "who" questions — by design; identity
  questions route back to the product boundary (DSAR process).
- Joins across marts stay possible (stable pseudonymous keys).
- Every new source field needs an explicit rule/allow-list entry —
  friction by intent; the alternative is silent PII landing.
- Erasure becomes verifiable: `lifecycle/anonymization/` checks that
  nothing attributable to an erased subject remains.
