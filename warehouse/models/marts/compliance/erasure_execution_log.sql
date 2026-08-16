-- erasure_execution_log — erasure execution aggregates (RESTRICTED).
-- AGGREGATES ONLY — proofs of erasure propagation live in
-- lifecycle/verification; this mart exposes monthly aggregates for
-- compliance dashboards. SCAFFOLD empty set until retention jobs write
-- the execution table.
select
    cast(null as date) as execution_month,
    cast(null as integer) as erasures_executed,
    cast(null as integer) as propagations_verified,
    cast(null as numeric(5, 4)) as verification_pass_rate
where 1 = 0
