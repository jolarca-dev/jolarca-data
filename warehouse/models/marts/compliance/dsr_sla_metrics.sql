-- dsr_sla_metrics — DSAR/DSR handling SLA aggregates (RESTRICTED).
-- AGGREGATES ONLY: per-subject rows must never exist here. Source is
-- the jol-m-compliance DSAR log extract; SCAFFOLD empty set until that
-- ingestion lands.
select
    cast(null as date) as report_month,
    cast(null as char(2)) as country_code,
    cast(null as integer) as requests_received,
    cast(null as integer) as requests_within_sla,
    cast(null as numeric(5, 4)) as sla_rate
where 1 = 0
