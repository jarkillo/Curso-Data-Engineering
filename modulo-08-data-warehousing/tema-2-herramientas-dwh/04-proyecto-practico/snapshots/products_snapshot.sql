/*
Snapshot: Historial de Productos
Implementa SCD Type 2 para rastrear cambios históricos en productos
(especialmente cambios de precio)
*/

{% snapshot products_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='product_id',

      strategy='timestamp',
      updated_at='updated_at',

      invalidate_hard_deletes=True
    )
}}

-- Seleccionar datos actuales de productos
SELECT
    product_id,
    sku,
    name,
    description,
    price,
    category,
    stock,
    updated_at
FROM {{ ref('raw_products') }}

{% endsnapshot %}


{#
CÓMO FUNCIONA ESTE SNAPSHOT:

1. Primera ejecución (dbt snapshot):
   - Crea tabla snapshots.products_snapshot
   - Agrega columnas automáticas: dbt_scd_id, dbt_updated_at, dbt_valid_from, dbt_valid_to

2. Ejecuciones posteriores:
   - Detecta cambios comparando updated_at
   - Si producto cambió:
     * Marca versión anterior: dbt_valid_to = NOW()
     * Inserta nueva versión: dbt_valid_from = NOW(), dbt_valid_to = NULL

3. Ejemplo de uso:

   -- Precio actual de producto 1
   SELECT price
   FROM snapshots.products_snapshot
   WHERE product_id = 1
     AND dbt_valid_to IS NULL;

   -- Historial completo de precios del producto 1
   SELECT
       product_id,
       price,
       dbt_valid_from,
       dbt_valid_to
   FROM snapshots.products_snapshot
   WHERE product_id = 1
   ORDER BY dbt_valid_from;

   -- Precio en una fecha específica
   SELECT price
   FROM snapshots.products_snapshot
   WHERE product_id = 1
     AND '2024-03-01' BETWEEN dbt_valid_from AND COALESCE(dbt_valid_to, '9999-12-31');

4. Ejecutar:
   dbt snapshot

5. Refrescar después de cambios en raw_products:
   dbt snapshot --select products_snapshot
#}
