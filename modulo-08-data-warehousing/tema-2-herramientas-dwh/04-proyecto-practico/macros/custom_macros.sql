/*
Macros personalizados para TechMart Analytics
Funciones SQL reutilizables en todo el proyecto
*/

-- ==============================================
-- Macro: Convertir centavos a dólares
-- ==============================================
{% macro cents_to_dollars(column_name, precision=2) %}
    ROUND(({{ column_name }} / 100.0)::NUMERIC, {{ precision }})
{% endmacro %}


-- ==============================================
-- Macro: Calcular edad en años desde una fecha
-- ==============================================
{% macro age_in_years(date_column) %}
    DATE_PART('year', AGE(CURRENT_DATE, {{ date_column }}::DATE))
{% endmacro %}


-- ==============================================
-- Macro: Clasificar valores en percentiles
-- ==============================================
{% macro percentile_rank(column_name, partition_by=none) %}
    PERCENT_RANK() OVER (
        {% if partition_by %}
        PARTITION BY {{ partition_by }}
        {% endif %}
        ORDER BY {{ column_name }}
    )
{% endmacro %}


-- ==============================================
-- Macro: Generar columnas pivoteadas para métodos de pago
-- ==============================================
{% macro pivot_payment_methods() %}
    {% set payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer'] %}

    {% for method in payment_methods %}
    SUM(CASE WHEN payment_method = '{{ method }}' THEN total_amount ELSE 0 END) AS {{ method }}_revenue,
    COUNT(CASE WHEN payment_method = '{{ method }}' THEN 1 END) AS {{ method }}_count
    {{- "," if not loop.last else "" }}
    {% endfor %}
{% endmacro %}


-- ==============================================
-- Macro: Generar columnas pivoteadas para categorías
-- ==============================================
{% macro pivot_categories() %}
    {% set categories = ['electronics', 'accessories', 'clothing'] %}

    {% for category in categories %}
    SUM(CASE WHEN product_category = '{{ category }}' THEN total_amount ELSE 0 END) AS {{ category }}_revenue,
    COUNT(CASE WHEN product_category = '{{ category }}' THEN 1 END) AS {{ category }}_orders
    {{- "," if not loop.last else "" }}
    {% endfor %}
{% endmacro %}


-- ==============================================
-- Macro: Crear rangos de fechas dinámicos
-- ==============================================
{% macro date_range(start_date_column, end_date_column=none) %}
    {% if end_date_column %}
        DATE_PART('day', {{ end_date_column }}::DATE - {{ start_date_column }}::DATE)
    {% else %}
        DATE_PART('day', CURRENT_DATE - {{ start_date_column }}::DATE)
    {% endif %}
{% endmacro %}


-- ==============================================
-- Macro: Normalizar texto (trim + lowercase)
-- ==============================================
{% macro normalize_text(column_name) %}
    LOWER(TRIM({{ column_name }}))
{% endmacro %}


-- ==============================================
-- Macro: Formatear nombres (Title Case)
-- ==============================================
{% macro format_name(column_name) %}
    INITCAP(TRIM({{ column_name }}))
{% endmacro %}


-- ==============================================
-- Macro: Detectar outliers usando IQR method
-- ==============================================
{% macro is_outlier(column_name, multiplier=1.5) %}
    {{ column_name }} < (
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY {{ column_name }}) -
        {{ multiplier }} * (
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY {{ column_name }}) -
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY {{ column_name }})
        )
    )
    OR
    {{ column_name }} > (
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY {{ column_name }}) +
        {{ multiplier }} * (
            PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY {{ column_name }}) -
            PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY {{ column_name }})
        )
    )
{% endmacro %}


-- ==============================================
-- Macro: Generar hash MD5 para claves surrogate
-- ==============================================
{% macro generate_surrogate_key(columns) %}
    MD5(
        {% for column in columns %}
        COALESCE(CAST({{ column }} AS TEXT), '')
        {{- "|| '|' ||" if not loop.last else "" }}
        {% endfor %}
    )
{% endmacro %}


-- ==============================================
-- Macro: Convertir NULL a valor por defecto
-- ==============================================
{% macro null_to_default(column_name, default_value) %}
    COALESCE({{ column_name }}, {{ default_value }})
{% endmacro %}
