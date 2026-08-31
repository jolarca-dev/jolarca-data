# Retention jobs — scheduled purge/anonymize per retention-map

Each job implements exactly one retention class from
`governance/retention-map.md`; the class → mechanism mapping is owned
there, execution is owned here. **Warehouse only** — production
retention is owned by `jolarca`.

## Job contract (every job must)

1. Declare the retention class and dataset scope in its header.
2. Respect legal holds (`../legal-hold/holds.yml`) — held entities are
   skipped and counted in the run report.
3. Run destructively only inside an explicit transaction with a prior
   row-count capture (proof input).
4. Write a run proof consumable by `../verification/`.

## Scheduled jobs (planned at scaffold)

| Job | Class | Cadence | Mechanism |
|-----|-------|---------|-----------|
| purge-search-analytics | short-term | monthly | drop partitions > 90d |
| purge-operational | operational | yearly | rolling window + re-aggregation to monthly rollups |
| purge-statutory | statutory | yearly | drop only after horizon + DPO release + no hold |

Jobs land with the warehouse environment; until then this file is the
contract they are built against.
