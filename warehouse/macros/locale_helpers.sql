{% macro locale_name(country_code_column) %}
{#-
    Locale dimension helper: map ISO country to the marketplace locale
    used for translation joins (ml/translation-memory).
-#}
    case {{ country_code_column }}
        when 'LT' then 'lt'
        when 'LV' then 'lv'
        when 'EE' then 'et'
        else 'en'
    end
{% endmacro %}

{% macro fiscal_quarter(date_column) %}
{#-
    Locale dimension helper: reporting quarter label (VAT OSS periods
    are calendar quarters).
-#}
    to_char(date_trunc('quarter', {{ date_column }}), 'IYYY-"Q"IQ')
{% endmacro %}
