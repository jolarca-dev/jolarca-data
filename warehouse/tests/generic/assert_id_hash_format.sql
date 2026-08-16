{% test assert_id_hash_format(model, column_name) %}
{#-
    Pseudonymous keys must be 32-char lowercase hex (md5). Any other
    shape means an unhashed identifier leaked through.
-#}
select {{ column_name }}
from {{ model }}
where {{ column_name }} is not null
  and {{ column_name }} !~ '^[0-9a-f]{32}$'
{% endtest %}
