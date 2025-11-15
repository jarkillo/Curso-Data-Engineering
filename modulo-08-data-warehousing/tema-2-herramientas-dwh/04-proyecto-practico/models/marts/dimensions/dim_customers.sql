/*
Dimensión: Clientes
Tabla dimensional de clientes con métricas agregadas y segmentación
*/

{{ config(
    materialized='table',
    tags=['marts', 'dimensions', 'customers']
) }}

WITH customer_base AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(total_amount) AS lifetime_value,
        AVG(total_amount) AS avg_order_value,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date,
        MAX(CASE WHEN is_delivered THEN order_date END) AS last_delivered_date
    FROM {{ ref('stg_orders') }}
    WHERE NOT is_cancelled  -- Excluir pedidos cancelados
    GROUP BY customer_id
),

customer_segments AS (
    SELECT
        customer_id,
        total_orders,
        lifetime_value,
        avg_order_value,
        first_order_date,
        last_order_date,
        last_delivered_date,

        -- Segmentación por valor de vida (Customer Lifetime Value)
        CASE
            WHEN lifetime_value >= {{ var('customer_segments')['platinum_threshold'] }} THEN 'Platinum'
            WHEN lifetime_value >= {{ var('customer_segments')['gold_threshold'] }} THEN 'Gold'
            WHEN lifetime_value >= {{ var('customer_segments')['silver_threshold'] }} THEN 'Silver'
            ELSE 'Bronze'
        END AS customer_segment,

        -- Clasificación por frecuencia de compra
        CASE
            WHEN total_orders >= 10 THEN 'Very High'
            WHEN total_orders >= 5 THEN 'High'
            WHEN total_orders >= 2 THEN 'Medium'
            ELSE 'Low'
        END AS purchase_frequency,

        -- Días desde última compra (recencia)
        DATE_PART('day', CURRENT_DATE - last_order_date::DATE) AS days_since_last_order,

        -- Clasificación RFM simplificada
        CASE
            WHEN DATE_PART('day', CURRENT_DATE - last_order_date::DATE) <= 30 THEN 'Active'
            WHEN DATE_PART('day', CURRENT_DATE - last_order_date::DATE) <= 90 THEN 'At Risk'
            ELSE 'Inactive'
        END AS customer_status

    FROM customer_orders
)

SELECT
    -- Identificadores
    c.customer_id,

    -- Información demográfica
    c.email,
    c.first_name,
    c.last_name,
    c.full_name,
    c.phone_cleaned,
    c.country,
    c.created_at,

    -- Métricas de compra
    COALESCE(s.total_orders, 0) AS total_orders,
    COALESCE(s.lifetime_value, 0) AS lifetime_value,
    COALESCE(s.avg_order_value, 0) AS avg_order_value,

    -- Fechas clave
    s.first_order_date,
    s.last_order_date,
    s.last_delivered_date,
    s.days_since_last_order,

    -- Segmentación
    COALESCE(s.customer_segment, 'Bronze') AS customer_segment,
    COALESCE(s.purchase_frequency, 'Low') AS purchase_frequency,
    COALESCE(s.customer_status, 'Inactive') AS customer_status,

    -- Flag: ¿Ha realizado al menos un pedido?
    s.total_orders > 0 AS has_purchased,

    -- Metadatos
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM customer_base c
LEFT JOIN customer_segments s
    ON c.customer_id = s.customer_id
