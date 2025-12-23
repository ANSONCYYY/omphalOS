{% macro month_bucket(date_expr) -%}
substr({{ date_expr }}, 1, 7)
{%- endmacro %}
