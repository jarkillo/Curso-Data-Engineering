/*
Intermediate Model: Orders Enriched
Combina ordenes con datos de clientes y productos para crear
una vista unificada que facilita la creacion de dimensiones y hechos.

Este modelo representa la capa INTERMEDIATE del pipeline:
  staging -> INTERMEDIATE -> marts
*/

{{ config(
    materialized='view',
    tags=['intermediate']
) }}

WITH orders AS (
    SELECT *
    FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT
        customer_id,
        first_name,
        last_name,
        email,
        country
    FROM {{ ref('stg_customers') }}
),

products AS (
    SELECT
        product_id,
        name AS product_name,
        category AS product_category,
        price AS current_price
    FROM {{ ref('stg_products') }}
)

SELECT
    -- Order info
    o.order_id,
    o.order_date,
    o.quantity,
    o.total_amount,
    o.status,
    o.payment_method,
    o.shipped_date,
    o.delivered_date,
    o.is_shipped,
    o.is_delivered,
    o.is_cancelled,
    o.days_to_ship,

    -- Customer info
    o.customer_id,
    c.first_name AS customer_first_name,
    c.last_name AS customer_last_name,
    c.email AS customer_email,
    c.country AS customer_country,

    -- Product info
    o.product_id,
    p.product_name,
    p.product_category,
    p.current_price,

    -- Calculated fields
    o.total_amount - (o.quantity * p.current_price) AS price_difference,
    CASE
        WHEN o.total_amount >= 500 THEN 'High Value'
        WHEN o.total_amount >= 100 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_value_tier,

    -- Metadata
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN products p ON o.product_id = p.product_id
