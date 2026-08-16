-- stg_users — pseudonymous account dimension. Names/emails never land
-- in raw (pseudonymizer drops them); this model keeps role, geo, and
-- consent flag only.
with source as (

    select * from {{ source('jol_marketplace_raw', 'users') }}

)

select
    {{ hash_id('id') }} as user_key,
    role,
    country_code,
    consent_marketing,
    created_at
from source
