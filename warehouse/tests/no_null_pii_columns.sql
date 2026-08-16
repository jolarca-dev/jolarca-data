-- no-null-pii-columns: pseudonymous subject keys are the ONLY trace of
-- subjects in the warehouse; a null key means either a broken hash at
-- ingestion or a silently dropped identifier. Both are defects.
{% set checks %}
    select order_key as subject_key from {{ ref('fct_orders') }}
    union all
    select seller_key from {{ ref('fct_orders') }}
    union all
    select buyer_key from {{ ref('fct_orders') }}
    union all
    select seller_key from {{ ref('dim_sellers') }}
{% endset %}

select subject_key
from ({{ checks }}) as keys
where subject_key is null
