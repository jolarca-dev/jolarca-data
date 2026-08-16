{% macro hash_id(column) %}
{#-
    Deterministic pseudonymous key for a numeric subject identifier.
    Salted via the hash_salt var (HASH_SALT env var in production).
    Output: 32-char lowercase hex — asserted by assert_id_hash_format.
-#}
    md5({{ column }}::text || '{{ var("hash_salt") }}')
{% endmacro %}
