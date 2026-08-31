# Runbook — restore analytics (warehouse rebuild)

**Key property: analytics is rebuildable from sources.** Production
backups are NOT in this repository (they live in
`jolarca-infrastructure`); a full warehouse loss is a rebuild, not a
restore-from-backup.

## Rebuild procedure

1. Provision an empty EU-region Postgres (`jolarca-infrastructure`
   change management); apply encryption and access baseline.
2. Provide env vars per `.envrc.example`; write `warehouse/profiles.yml`
   from `profiles.yml.example`.
3. Recreate the raw landing schema and extract-role grants
   (`ingestion/pipelines/postgres_extract/extract-role.sql`).
4. Re-run extraction from the read replica + Stripe for the retention
   window required by `governance/retention-map.md` — no further back:
   the rebuild must respect retention, not undo it.
5. `dbt deps && dbt build` — seeds, staging, intermediate, marts.
6. Run quality gates: `make quality` + freshness report; all blocking
   expectations green before consumers reconnect.
7. Re-run erasure verification (`make anonymize-verify`) — a rebuild
   must not resurrect erased subjects; any hit is a severity-1 class
   incident (previous runbook).

## Boundaries

- Do not rebuild beyond the retention horizon "for completeness".
- Legal holds apply to the rebuild too: held entities' data follows
  the hold rules from day one.
- Record the rebuild in `audits/` (scope, window, verification
  results).
