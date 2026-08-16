-- fct_commission — platform commission per revenue order. Until the
-- fee engine emits real figures, commission is derived at the
-- commission_rate_pct var on the net amount.
with orders as (

    select * from {{ ref('fct_orders') }}
    where is_revenue

)

select
    order_key,
    seller_key,
    order_date,
    order_quarter,
    buyer_country_code,
    net_amount_eur,
    round(net_amount_eur * {{ var('commission_rate_pct') }} / 100.0, 2) as commission_eur,
    {{ var('commission_rate_pct') }} as commission_rate_pct
from orders
