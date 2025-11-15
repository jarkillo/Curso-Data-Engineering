/*
Staging: Clientes
Limpieza y estandarización inicial de datos de clientes
*/

{{ config(
    materialized='view',
    tags=['staging', 'customers']
) }}

WITH source_data AS (
    SELECT * FROM {{ ref('raw_customers') }}
)

SELECT
    customer_id,

    -- Limpieza de email: lowercase y trim
    LOWER(TRIM(email)) AS email,

    -- Nombres: formato título (First Letter Uppercase)
    INITCAP(TRIM(first_name)) AS first_name,
    INITCAP(TRIM(last_name)) AS last_name,

    -- Nombre completo construido
    CONCAT(
        INITCAP(TRIM(first_name)),
        ' ',
        INITCAP(TRIM(last_name))
    ) AS full_name,

    -- Teléfono: solo dígitos (eliminar caracteres especiales)
    REGEXP_REPLACE(phone, '[^0-9]', '', 'g') AS phone_cleaned,

    -- País: uppercase para estandarizar
    UPPER(TRIM(country)) AS country,

    -- Timestamp original
    created_at,

    -- Metadatos de carga
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM source_data

-- Filtrar registros sin email (dato crítico)
WHERE email IS NOT NULL
  AND TRIM(email) != ''
