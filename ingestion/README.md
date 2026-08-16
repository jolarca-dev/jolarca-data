# Ingestion — read-replica → strip identifiers → land pseudonymized

Doctrine:

1. **Read-replica only, least privilege.** Extraction never touches the
   primary; the extract role is read-only and table-scoped (ADR-0002).
2. **The pseudonymizer is the boundary.** Identifiers are stripped or
   hashed BEFORE landing (ADR-0001). The warehouse must be unable to
   re-identify without external collusion — that is a design property,
   not an aspiration.
3. **Contracts are allow-lists.** `contracts/` declares what fields may
   leave each source. Anything not on the allow-list stays at the
   source; widening an allow-list is a DPO-reviewed change.
4. **Never PAN.** The Stripe extract takes charge/payout metadata only;
   the SAQ-A boundary holds in analytics too.

## Layout

| Path | Content |
|------|---------|
| `pipelines/postgres_extract/` | Batch/CDC extract from the read replica (read-only role) |
| `pipelines/stripe_extract/` | Charges/payouts metadata extract |
| `pipelines/pseudonymizer/` | THE critical component: strips/hashes identifiers pre-landing, unit-tested |
| `contracts/` | Schema contracts per source: field allow-lists |

## Adding a source

1. `dataset_request` issue first (governance).
2. Write the contract (allow-list) in `contracts/` — DPO review if any
   field is personal data.
3. Implement the extract + pseudonymizer rules; unit tests mandatory
   for any pseudonymization logic.
4. Register the landed tables in `warehouse/models/staging/_staging.yml`
   with freshness SLAs.
