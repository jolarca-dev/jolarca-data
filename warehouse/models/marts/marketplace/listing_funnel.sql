-- listing_funnel — category-level funnel: listed -> active -> ordered.
with products as (

    select * from {{ ref('dim_products') }}

),

ordered_products as (

    select distinct category_code
    from {{ ref('fct_orders') }}
    where is_revenue

)

select
    products.category_code,
    count(*) as listed_count,
    count(*) filter (where products.is_active) as active_count,
    count(distinct case
        when ordered.category_code is not null then products.product_key
    end) as ordered_count
from products
left join ordered_products as ordered
    on products.category_code = ordered.category_code
group by products.category_code
