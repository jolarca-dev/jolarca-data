{% macro pseudonymize(column) %}
{#-
    One-way pseudonymization for free-text identifier-like values
    (account handles, external references). Irreversible without the
    salt; the cleartext must not be carried downstream.
-#}
    md5(lower(trim({{ column }})) || '{{ var("hash_salt") }}')
{% endmacro %}
