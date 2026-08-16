-- seller_health — per-seller health aggregates (CONFIDENTIAL).
-- Pseudonymous keys only; feeds marketplace ops dashboards.
with lifecycle as (

    select * from {{ ref('int_seller_lifecycle') }}

),

refunds as (

    select
        seller_key,
        count(*) filter (where status = 'refunded') as refund_count,
        count(*) as total_count
    from {{ ref('stg_orders') }}
    group by seller_key

)

select
    lifecycle.seller_key,
    lifecycle.country_code,
    lifecycle.lifecycle_stage,
    lifecycle.order_count,
    lifecycle.lifetime_gmv_eur,
    lifecycle.first_order_at,
    lifecycle.last_order_at,
    coalesce(refunds.refund_count, 0) as refund_count,
    case
        when coalesce(refunds.total_count, 0) = 0 then 0.0
        else round(refunds.refund_count::numeric / refunds.total_count, 4)
    end as refund_rate
from lifecycle
left join refunds
    on lifecycle.seller_key = refunds.seller_key
