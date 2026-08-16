-- stg_orders — PII STRIPPED HERE: subject ids are hashed; no names,
-- emails, or addresses may be added to this model.
with source as (

    select * from {{ source('jol_marketplace_raw', 'orders') }}

)

select
    {{ hash_id('id') }} as order_key,
    {{ hash_id('buyer_id') }} as buyer_key,
    {{ hash_id('seller_id') }} as seller_key,
    status,
    {{ cents_to_eur('amount_cents') }} as amount_eur,
    lower(currency) as currency,
    category_code,
    country_code,
    vat_rate_pct,
    created_at
from source
