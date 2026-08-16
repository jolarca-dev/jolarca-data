{% macro cents_to_eur(column) %}
{#-
    Integer cents -> EUR decimal(12,2). The warehouse is EUR-only
    (assert_accepted_currency_eur); conversion is a fixed-point shift,
    never floating point.
-#}
    round({{ column }} / 100.0, 2)
{% endmacro %}
