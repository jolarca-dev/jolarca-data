# Anonymization — erasure propagation verification

When `jolarca` executes a DSAR erasure (subject anonymized in
the product DB), the warehouse must follow: every model keyed by that
subject's pseudonymous key must be purged or re-aggregated so that no
row attributable to the subject remains.

## Verification job

Input: erasure events from the compliance DSAR log (subject → hashed
key mapping happens inside the product boundary; this job receives the
hashed key only).

Steps:

1. For each hashed key, query every model in
   `warehouse/models/` that carries subject keys (fct_orders,
   dim_sellers, seller_health, …).
2. Assert: zero rows for per-subject models; aggregates unchanged in
   shape (no per-subject residue).
3. Record the proof in `../verification/` (run id, models checked,
   result, timestamp).

A failed check opens a `pii_incident` issue and pauses downstream
refresh — see `docs/runbooks/pii-detected-in-warehouse.md`.
