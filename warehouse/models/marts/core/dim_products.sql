-- dim_products — taxonomy-linked product dimension.
with products as (

    select * from {{ ref('stg_products') }}

)

select
    products.product_key,
    products.seller_key,
    products.category_code,
    products.title,
    products.price_eur,
    products.currency,
    products.status,
    products.status = 'active' as is_active,
    products.created_at::date as listed_date,
    products.created_at
from products
