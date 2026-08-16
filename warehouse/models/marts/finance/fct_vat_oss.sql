-- fct_vat_oss — VAT OSS reporting support: net/VAT amounts per
-- destination country per quarter per rate. CONFIDENTIAL; statutory
-- retention (governance/retention-map.md). Not a filing — supports the
-- filing prepared by finance/jol-m-compliance.
with orders as (

    select * from {{ ref('fct_orders') }}
    where is_revenue

)

select
    order_quarter,
    buyer_country_code as destination_country,
    vat_rate_pct,
    count(*) as order_count,
    round(sum(net_amount_eur), 2) as net_amount_eur,
    round(sum(vat_amount_eur), 2) as vat_amount_eur,
    round(sum(amount_eur), 2) as gross_amount_eur
from orders
group by order_quarter, buyer_country_code, vat_rate_pct
