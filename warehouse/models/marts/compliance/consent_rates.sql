-- consent_rates — marketing consent opt-in aggregates (RESTRICTED).
-- AGGREGATES ONLY: no per-subject rows. Consent flag comes from the
-- pseudonymous landing; the flag travels, the identity never does.
with buyers as (

    select * from {{ ref('stg_users') }}
    where role = 'buyer'

)

select
    country_code,
    date_trunc('month', created_at)::date as cohort_month,
    count(*) as accounts_in_cohort,
    count(*) filter (where consent_marketing) as opted_in,
    round(
        count(*) filter (where consent_marketing)::numeric
        / nullif(count(*), 0),
        4
    ) as consent_rate
from buyers
group by date_trunc('month', created_at), country_code
