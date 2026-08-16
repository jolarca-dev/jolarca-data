-- int_order_items_enriched — order facts enriched with the seller's
-- geography and tenure. Stays pseudonymous end to end.
with orders as (

    select * from {{ ref('stg_orders') }}

),

sellers as (

    select * from {{ ref('stg_users') }}
    where role = 'seller'

)

select
    orders.order_key,
    orders.buyer_key,
    orders.seller_key,
    orders.status,
    orders.amount_eur,
    orders.currency,
    orders.category_code,
    orders.country_code as buyer_country_code,
    sellers.country_code as seller_country_code,
    sellers.created_at as seller_joined_at,
    orders.vat_rate_pct,
    orders.created_at
from orders
left join sellers
    on orders.seller_key = sellers.user_key
