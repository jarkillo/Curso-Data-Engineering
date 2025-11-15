/*
Staging: Productos
Limpieza y estandarización de catálogo de productos
*/

{{ config(
    materialized='view',
    tags=['staging', 'products']
) }}

WITH source_data AS (
    SELECT * FROM {{ ref('raw_products') }}
),

-- Deduplicar productos (mantener versión más reciente)
deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY product_id
            ORDER BY updated_at DESC
        ) AS row_num
    FROM source_data
)

SELECT
    product_id,

    -- SKU: uppercase para estandarizar
    UPPER(TRIM(sku)) AS sku,

    -- Nombre y descripción: trim espacios
    TRIM(name) AS name,
    TRIM(description) AS description,

    -- Precio: convertir a NUMERIC(10,2)
    ROUND(price::NUMERIC, 2) AS price,

    -- Categoría: lowercase para consistencia
    LOWER(TRIM(category)) AS category,

    -- Stock
    stock,

    -- Timestamp de última actualización
    updated_at,

    -- Metadatos
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM deduplicated

-- Solo la versión más reciente de cada producto
WHERE row_num = 1

  -- Filtrar productos inválidos
  AND price > 0
  AND stock >= 0
