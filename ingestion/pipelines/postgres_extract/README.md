# postgres_extract — read replica → pseudonymized landing

Batch/CDC extraction from the `jol-m-marketplace` **read replica**.

- Connection: read-only role, table-scoped grants (see
  `extract-role.sql` — applied by `jol-m-infrastructure`, not here).
- Cadence: nightly batch at scaffold; CDC upgrade path is documented
  when order volume justifies it.
- Output goes through `../pseudonymizer/` before any landing write.

## Invariant

This job has NO write path to production and NO access to fields
outside `../contracts/postgres.yml`. If the contract and the code
disagree, the contract wins and the job fails closed.
