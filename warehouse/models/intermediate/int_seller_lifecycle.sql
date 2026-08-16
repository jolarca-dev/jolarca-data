-- int_seller_lifecycle — per-seller activity spine used by
-- seller_health and dim_sellers. Pseudonymous keys only.
with sellers as (

    select * from {{ ref('stg_users') }}
    where role = 'seller'

),

order_activity as (

    select
        seller_key,
        count(*) as order_count,
        sum(amount_eur) as lifetime_gmv_eur,
        min(created_at) as first_order_at,
        max(created_at) as last_order_at
    from {{ ref('stg_orders') }}
    where status in ('paid', 'shipped', 'delivered')
    group by seller_key

)

select
    sellers.user_key as seller_key,
    sellers.country_code,
    sellers.created_at as joined_at,
    order_activity.first_order_at,
    order_activity.last_order_at,
    coalesce(order_activity.order_count, 0) as order_count,
    coalesce(order_activity.lifetime_gmv_eur, 0) as lifetime_gmv_eur,
    case
        when order_activity.first_order_at is null then 'onboarded'
        when order_activity.last_order_at < current_date - interval '90 days' then 'dormant'
        else 'active'
    end as lifecycle_stage
from sellers
left join order_activity
    on sellers.user_key = order_activity.seller_key
