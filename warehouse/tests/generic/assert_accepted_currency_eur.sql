{% test assert_accepted_currency_eur(model, column_name) %}
{#-
    The warehouse is EUR-only. A non-EUR row means the ingestion
    contract changed without a governance decision.
-#}
select {{ column_name }}
from {{ model }}
where lower({{ column_name }}) <> 'eur'
{% endtest %}
