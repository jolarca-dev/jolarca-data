-- search_analytics — search relevance aggregates.
-- SCAFFOLD: search telemetry ingestion is not landed yet (see
-- ingestion/contracts/). The model ships the target contract as an
-- empty set so consumers and tests can build against it; wiring the
-- source swaps the body only.
select
    cast(null as text) as query_hash,
    cast(null as text) as category_code,
    cast(null as date) as search_date,
    cast(null as integer) as search_count,
    cast(null as numeric(5, 4)) as click_through_rate
where 1 = 0
