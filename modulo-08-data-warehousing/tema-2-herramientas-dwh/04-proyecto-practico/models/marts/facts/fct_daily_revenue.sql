/*
Modelo de análisis: Revenue diario
Agrega ventas por día con pivote de métodos de pago y categorías
Demuestra uso de macros personalizados
*/

{{ config(
    materialized='table',
    tags=['marts', 'facts', 'analytics']
) }}

WITH daily_orders AS (
    SELECT
        order_date_only AS order_date,
        product_category,
        payment_method,
        total_amount,
        order_id,
        customer_segment
    FROM {{ ref('fct_orders') }}
    WHERE NOT is_cancelled
)

SELECT
    order_date,

    -- Métricas básicas
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    MIN(total_amount) AS min_order_value,
    MAX(total_amount) AS max_order_value,

    -- Pivote de métodos de pago usando macro
    {{ pivot_payment_methods() }},

    -- Pivote de categorías usando macro
    {{ pivot_categories() }},

    -- Segmentación de clientes
    COUNT(DISTINCT CASE WHEN customer_segment = 'Platinum' THEN order_id END) AS platinum_orders,
    COUNT(DISTINCT CASE WHEN customer_segment = 'Gold' THEN order_id END) AS gold_orders,
    COUNT(DISTINCT CASE WHEN customer_segment = 'Silver' THEN order_id END) AS silver_orders,
    COUNT(DISTINCT CASE WHEN customer_segment = 'Bronze' THEN order_id END) AS bronze_orders,

    -- Metadatos
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM daily_orders
GROUP BY order_date
ORDER BY order_date DESC
