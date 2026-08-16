{% test assert_vat_rate_bounds(model, column_name) %}
{#-
    VAT rates must sit inside the EU-referenced bounds (0–30%).
    Cross-check reference: seed/tax/vat-rates.yml.
-#}
select {{ column_name }}
from {{ model }}
where {{ column_name }} is not null
  and ({{ column_name }} < 0 or {{ column_name }} > 30)
{% endtest %}
