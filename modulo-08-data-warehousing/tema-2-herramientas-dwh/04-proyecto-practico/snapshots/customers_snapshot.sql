/*
Snapshot: Historial de Clientes
Implementa SCD Type 2 para rastrear cambios historicos en clientes
(especialmente cambios de direccion, email, telefono)
*/

{% snapshot customers_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',

      strategy='timestamp',
      updated_at='updated_at',

      invalidate_hard_deletes=True
    )
}}

-- Seleccionar datos actuales de clientes
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    address,
    city,
    country,
    updated_at
FROM {{ ref('raw_customers') }}

{% endsnapshot %}


{#
COMO FUNCIONA ESTE SNAPSHOT:

1. Primera ejecucion (dbt snapshot):
   - Crea tabla snapshots.customers_snapshot
   - Agrega columnas automaticas: dbt_scd_id, dbt_updated_at, dbt_valid_from, dbt_valid_to

2. Ejecuciones posteriores:
   - Detecta cambios comparando updated_at
   - Si cliente cambio (direccion, email, telefono):
     * Marca version anterior: dbt_valid_to = NOW()
     * Inserta nueva version: dbt_valid_from = NOW(), dbt_valid_to = NULL

3. Ejemplo de uso:

   -- Datos actuales del cliente 1
   SELECT *
   FROM snapshots.customers_snapshot
   WHERE customer_id = 1
     AND dbt_valid_to IS NULL;

   -- Historial completo de direcciones del cliente 1
   SELECT
       customer_id,
       address,
       city,
       country,
       dbt_valid_from,
       dbt_valid_to
   FROM snapshots.customers_snapshot
   WHERE customer_id = 1
   ORDER BY dbt_valid_from;

   -- Direccion del cliente en una fecha especifica
   SELECT address, city
   FROM snapshots.customers_snapshot
   WHERE customer_id = 1
     AND '2024-03-01' BETWEEN dbt_valid_from AND COALESCE(dbt_valid_to, '9999-12-31');

4. Ejecutar:
   dbt snapshot

5. Refrescar despues de cambios en raw_customers:
   dbt snapshot --select customers_snapshot
#}
