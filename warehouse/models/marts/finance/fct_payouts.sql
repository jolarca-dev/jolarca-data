-- fct_payouts — settlement-basis payout periods per seller per month.
-- SCAFFOLD: derives from order facts until stripe_extract lands; then
-- Stripe payout metadata joins here (charge/payout refs only — never
-- PAN; SAQ-A boundary holds in analytics too).
with orders as (

    select * from {{ ref('fct_orders') }}
    where is_revenue

)

select
    seller_key,
    date_trunc('month', order_date)::date as payout_period,
    count(*) as order_count,
    round(sum(net_amount_eur), 2) as net_amount_eur,
    round(sum(vat_amount_eur), 2) as vat_amount_eur,
    round(sum(amount_eur), 2) as gross_amount_eur
from orders
group by seller_key, date_trunc('month', order_date)
