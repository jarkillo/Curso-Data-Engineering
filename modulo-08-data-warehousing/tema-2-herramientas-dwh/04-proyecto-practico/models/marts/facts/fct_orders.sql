/*
Hecho: Pedidos
Tabla de hechos de pedidos con todas las métricas y dimensiones desnormalizadas
*/

{{ config(
    materialized='table',
    tags=['marts', 'facts', 'orders']
) }}

WITH orders_base AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT
        customer_id,
        full_name,
        country,
        customer_segment
    FROM {{ ref('dim_customers') }}
),

products AS (
    SELECT
        product_id,
        name AS product_name,
        category,
        current_price
    FROM {{ ref('dim_products') }}
)

SELECT
    -- Identificadores
    o.order_id,
    o.customer_id,
    o.product_id,

    -- Dimensiones desnormalizadas (para facilitar análisis)
    c.full_name AS customer_name,
    c.country AS customer_country,
    c.customer_segment,
    p.product_name,
    p.category AS product_category,

    -- Métricas de la orden
    o.quantity,
    o.unit_price,
    o.total_amount,

    -- Análisis de precio
    p.current_price,
    (o.unit_price - p.current_price) AS price_difference,
    CASE
        WHEN p.current_price > 0 THEN
            ROUND(((o.unit_price - p.current_price) / p.current_price * 100)::NUMERIC, 2)
        ELSE 0
    END AS price_change_percentage,

    -- Información de pago
    o.payment_method,

    -- Estado del pedido
    o.order_status,
    o.is_shipped,
    o.is_delivered,
    o.is_cancelled,

    -- Fechas
    o.order_date,
    o.shipped_date,
    o.days_to_ship,

    -- Dimensiones de tiempo para análisis
    DATE(o.order_date) AS order_date_only,
    EXTRACT(YEAR FROM o.order_date) AS order_year,
    EXTRACT(QUARTER FROM o.order_date) AS order_quarter,
    EXTRACT(MONTH FROM o.order_date) AS order_month,
    EXTRACT(DAY FROM o.order_date) AS order_day,
    TO_CHAR(o.order_date, 'Day') AS order_day_of_week,
    EXTRACT(WEEK FROM o.order_date) AS order_week,

    -- Flags de análisis
    o.total_amount >= 1000 AS is_high_value_order,
    o.days_to_ship <= 2 AS is_fast_shipping,

    -- Metadatos
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM orders_base o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN products p ON o.product_id = p.product_id
