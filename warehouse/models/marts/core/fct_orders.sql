-- fct_orders — order facts, pseudonymous keys, EUR amounts.
-- Metrics dictionary definitions (GMV, etc.) in docs/metrics-dictionary.md.
with order_items as (

    select * from {{ ref('int_order_items_enriched') }}

)

select
    order_key,
    buyer_key,
    seller_key,
    status,
    status in ('paid', 'shipped', 'delivered') as is_revenue,
    amount_eur,
    currency,
    round(amount_eur * vat_rate_pct / 100.0, 2) as vat_amount_eur,
    round(amount_eur / (1 + vat_rate_pct / 100.0), 2) as net_amount_eur,
    vat_rate_pct,
    category_code,
    buyer_country_code,
    seller_country_code,
    {{ locale_name('buyer_country_code') }} as buyer_locale,
    {{ fiscal_quarter('created_at') }} as order_quarter,
    created_at::date as order_date,
    created_at
from order_items
