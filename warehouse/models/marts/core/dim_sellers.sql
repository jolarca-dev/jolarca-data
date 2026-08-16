-- dim_sellers — pseudonymized seller dimension. Never carries names,
-- contacts, or registry codes; join back to identity is deliberately
-- impossible from this warehouse (ADR-0001).
with lifecycle as (

    select * from {{ ref('int_seller_lifecycle') }}

)

select
    seller_key,
    country_code,
    {{ locale_name('country_code') }} as locale_name,
    joined_at::date as joined_date,
    order_count,
    lifetime_gmv_eur,
    first_order_at,
    last_order_at,
    lifecycle_stage
from lifecycle
