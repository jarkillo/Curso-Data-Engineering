/*
Dimensión: Productos
Catálogo de productos enriquecido con métricas de ventas
*/

{{ config(
    materialized='table',
    tags=['marts', 'dimensions', 'products']
) }}

WITH product_base AS (
    SELECT * FROM {{ ref('stg_products') }}
),

product_sales AS (
    SELECT
        product_id,
        COUNT(DISTINCT order_id) AS times_ordered,
        SUM(quantity) AS total_units_sold,
        SUM(total_amount) AS total_revenue,
        AVG(unit_price) AS avg_selling_price,
        MAX(order_date) AS last_order_date
    FROM {{ ref('stg_orders') }}
    WHERE NOT is_cancelled
    GROUP BY product_id
),

product_performance AS (
    SELECT
        product_id,
        times_ordered,
        total_units_sold,
        total_revenue,
        avg_selling_price,
        last_order_date,

        -- Clasificación por popularidad
        CASE
            WHEN times_ordered >= 5 THEN 'Best Seller'
            WHEN times_ordered >= 2 THEN 'Popular'
            WHEN times_ordered >= 1 THEN 'Normal'
            ELSE 'No Sales'
        END AS popularity_tier,

        -- Clasificación por ingresos
        CASE
            WHEN total_revenue >= 2000 THEN 'High Revenue'
            WHEN total_revenue >= 500 THEN 'Medium Revenue'
            WHEN total_revenue > 0 THEN 'Low Revenue'
            ELSE 'No Revenue'
        END AS revenue_tier

    FROM product_sales
)

SELECT
    -- Identificadores
    p.product_id,
    p.sku,

    -- Información del producto
    p.name,
    p.description,
    p.price AS current_price,
    p.category,
    p.stock AS current_stock,
    p.updated_at AS last_updated,

    -- Métricas de ventas
    COALESCE(perf.times_ordered, 0) AS times_ordered,
    COALESCE(perf.total_units_sold, 0) AS total_units_sold,
    COALESCE(perf.total_revenue, 0) AS total_revenue,
    COALESCE(perf.avg_selling_price, 0) AS avg_selling_price,
    perf.last_order_date,

    -- Clasificaciones
    COALESCE(perf.popularity_tier, 'No Sales') AS popularity_tier,
    COALESCE(perf.revenue_tier, 'No Revenue') AS revenue_tier,

    -- Flags útiles
    perf.times_ordered > 0 AS has_sales,
    p.stock = 0 AS is_out_of_stock,
    p.stock < 50 AS is_low_stock,

    -- Metadatos
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM product_base p
LEFT JOIN product_performance perf
    ON p.product_id = perf.product_id
