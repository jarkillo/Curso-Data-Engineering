/*
Staging: Pedidos
Limpieza y estandarización de pedidos
*/

{{ config(
    materialized='view',
    tags=['staging', 'orders']
) }}

WITH source_data AS (
    SELECT * FROM {{ ref('raw_orders') }}
)

SELECT
    order_id,
    customer_id,
    product_id,

    -- Cantidades y precios
    quantity,
    ROUND(unit_price::NUMERIC, 2) AS unit_price,
    ROUND(total_amount::NUMERIC, 2) AS total_amount,

    -- Método de pago: lowercase
    LOWER(TRIM(payment_method)) AS payment_method,

    -- Estado del pedido: lowercase
    LOWER(TRIM(order_status)) AS order_status,

    -- Fechas
    order_date,
    shipped_date,

    -- Calcular días hasta envío (si ya fue enviado)
    CASE
        WHEN shipped_date IS NOT NULL THEN
            DATE_PART('day', shipped_date - order_date)
        ELSE NULL
    END AS days_to_ship,

    -- Flags útiles
    shipped_date IS NOT NULL AS is_shipped,
    order_status = 'delivered' AS is_delivered,
    order_status = 'cancelled' AS is_cancelled,

    -- Metadatos
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM source_data

-- Validaciones básicas
WHERE quantity > 0
  AND unit_price > 0
  AND total_amount > 0
