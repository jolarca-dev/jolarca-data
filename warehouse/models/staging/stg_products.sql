-- stg_products — seller id hashed; listing title kept (product content
-- is not personal data; erasure of a listing follows dim_products).
with source as (

    select * from {{ source('jol_marketplace_raw', 'products') }}

)

select
    {{ hash_id('id') }} as product_key,
    {{ hash_id('seller_id') }} as seller_key,
    category_code,
    title,
    {{ cents_to_eur('price_cents') }} as price_eur,
    lower(currency) as currency,
    status,
    created_at
from source
