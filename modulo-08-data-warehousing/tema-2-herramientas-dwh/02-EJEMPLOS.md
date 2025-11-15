# Ejemplos Prácticos: dbt (data build tool)

## Introducción a los Ejemplos

En esta sección trabajaremos con **TechMart**, una empresa ficticia de e-commerce de electrónica. TechMart tiene:
- Sistema transaccional en PostgreSQL con ventas en tiempo real
- Necesidad de reportes analíticos para el equipo de negocio
- Múltiples fuentes de datos que necesitan consolidarse

Vamos a construir un Data Warehouse usando dbt, progresando desde transformaciones básicas hasta pipelines complejos.

---

## Ejemplo 1: Primer Modelo dbt - Limpieza Básica de Clientes

### Contexto

TechMart tiene una tabla `raw.customers` con datos de clientes que vienen directamente de su aplicación web. Los datos tienen problemas de calidad:
- Emails en mayúsculas/minúsculas inconsistentes
- Nombres con espacios extra
- Registros con email NULL
- Teléfonos en diferentes formatos

Necesitamos crear una tabla limpia `staging.stg_customers` que los analistas puedan usar.

### Datos de Entrada

**Tabla: `raw.customers`**

| customer_id | email | first_name | last_name | phone | created_at |
|---|---|---|---|---|---|
| 1 | JOHN@GMAIL.COM | john  | Smith | (555) 123-4567 | 2024-01-15 |
| 2 | sarah@YAHOO.com | Sarah | Johnson | 555-234-5678 | 2024-02-20 |
| 3 | NULL | Mike | Brown | 555.345.6789 | 2024-03-10 |
| 4 | bob@email.com  | Bob  | Wilson | 5554567890 | 2024-04-05 |

### Paso 1: Estructura del Proyecto

```bash
# Estructura inicial
techmart_dbt/
├── dbt_project.yml
├── models/
│   └── staging/
│       └── stg_customers.sql
```

### Paso 2: Configuración del Proyecto

**Archivo: `dbt_project.yml`**

```yaml
name: 'techmart_analytics'
version: '1.0.0'
config-version: 2

profile: 'techmart'

model-paths: ["models"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]

models:
  techmart_analytics:
    staging:
      +materialized: view
      +schema: staging
```

### Paso 3: Crear el Modelo de Staging

**Archivo: `models/staging/stg_customers.sql`**

```sql
/*
  Staging: Limpieza básica de clientes

  Transformaciones aplicadas:
  - Email normalizado (lowercase, trimmed)
  - Nombres en formato título (Initcap)
  - Filtrar registros sin email
  - Teléfono estandarizado (solo dígitos)
*/

{{ config(
    materialized='view',
    tags=['staging', 'customers']
) }}

SELECT
    customer_id,

    -- Email limpio
    LOWER(TRIM(email)) AS email,

    -- Nombres en formato correcto
    INITCAP(TRIM(first_name)) AS first_name,
    INITCAP(TRIM(last_name)) AS last_name,
    CONCAT(INITCAP(TRIM(first_name)), ' ', INITCAP(TRIM(last_name))) AS full_name,

    -- Teléfono: solo dígitos (remover caracteres especiales)
    REGEXP_REPLACE(phone, '[^0-9]', '', 'g') AS phone_cleaned,

    -- Metadata
    created_at,
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM {{ source('raw', 'customers') }}

-- Filtrar registros sin email (requisito de negocio)
WHERE email IS NOT NULL
```

### Paso 4: Definir Source

**Archivo: `models/staging/sources.yml`**

```yaml
version: 2

sources:
  - name: raw
    description: "Datos crudos de la base transaccional"
    schema: raw_data
    tables:
      - name: customers
        description: "Tabla de clientes desde la aplicación"
        columns:
          - name: customer_id
            description: "Primary key"
            tests:
              - not_null
              - unique
          - name: email
            description: "Email del cliente"
```

### Paso 5: Ejecutar el Modelo

```bash
# Compilar el SQL (ver qué SQL se generará)
dbt compile --select stg_customers

# Ejecutar el modelo (crear la vista)
dbt run --select stg_customers

# Ver logs
# dbt ejecuta internamente:
# CREATE OR REPLACE VIEW staging.stg_customers AS
# SELECT ...
```

### Resultado Esperado

**Tabla generada: `staging.stg_customers`**

| customer_id | email | first_name | last_name | full_name | phone_cleaned | created_at |
|---|---|---|---|---|---|---|
| 1 | john@gmail.com | John | Smith | John Smith | 5551234567 | 2024-01-15 |
| 2 | sarah@yahoo.com | Sarah | Johnson | Sarah Johnson | 5552345678 | 2024-02-20 |
| 4 | bob@email.com | Bob | Wilson | Bob Wilson | 5554567890 | 2024-04-05 |

**Nota**: El customer_id=3 fue filtrado porque tenía email NULL.

### ✅ Qué Aprendimos

1. **config()**: Definir materialización y tags en el modelo
2. **source()**: Referenciar tablas crudas (no modelos dbt)
3. **Limpieza básica**: LOWER, TRIM, INITCAP, REGEXP_REPLACE
4. **WHERE**: Filtrar datos de mala calidad
5. **Metadata**: Agregar timestamp de cuándo se cargó

---

## Ejemplo 2: Referencias entre Modelos y Tests

### Contexto

Ahora TechMart necesita una tabla dimensional de clientes (`dim_customers`) que:
- Use los datos limpios de `stg_customers`
- Agregue segmentación por valor de lifetime
- Incluya tests automáticos de calidad

### Datos Adicionales

**Tabla: `raw.orders`**

| order_id | customer_id | order_date | total_amount |
|---|---|---|---|
| 101 | 1 | 2024-01-20 | 150.00 |
| 102 | 1 | 2024-02-15 | 300.00 |
| 103 | 2 | 2024-02-25 | 75.00 |
| 104 | 4 | 2024-04-10 | 500.00 |

### Paso 1: Crear Modelo de Órdenes en Staging

**Archivo: `models/staging/stg_orders.sql`**

```sql
{{ config(materialized='view') }}

SELECT
    order_id,
    customer_id,
    order_date,
    total_amount,
    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM {{ source('raw', 'orders') }}
WHERE total_amount > 0  -- Filtrar órdenes inválidas
```

### Paso 2: Crear Dimensión de Clientes

**Archivo: `models/marts/dim_customers.sql`**

```sql
/*
  Dimensión de Clientes con Segmentación

  Lógica de negocio:
  - Bronze: Lifetime Value < $100
  - Silver: $100 - $500
  - Gold: $500 - $1,000
  - Platinum: > $1,000
*/

{{ config(
    materialized='table',
    tags=['marts', 'dimensions']
) }}

WITH customer_orders AS (
    -- Calcular lifetime value por cliente
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        SUM(total_amount) AS lifetime_value,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS last_order_date
    FROM {{ ref('stg_orders') }}
    GROUP BY customer_id
),

customer_segments AS (
    SELECT
        customer_id,
        total_orders,
        lifetime_value,
        first_order_date,
        last_order_date,

        -- Segmentación
        CASE
            WHEN lifetime_value >= 1000 THEN 'Platinum'
            WHEN lifetime_value >= 500 THEN 'Gold'
            WHEN lifetime_value >= 100 THEN 'Silver'
            ELSE 'Bronze'
        END AS segment
    FROM customer_orders
)

SELECT
    c.customer_id,
    c.email,
    c.first_name,
    c.last_name,
    c.full_name,
    c.phone_cleaned,
    c.created_at,

    -- Métricas agregadas
    COALESCE(s.total_orders, 0) AS total_orders,
    COALESCE(s.lifetime_value, 0) AS lifetime_value,
    s.first_order_date,
    s.last_order_date,

    -- Segmento (Bronze si no tiene órdenes)
    COALESCE(s.segment, 'Bronze') AS segment,

    -- Metadata
    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM {{ ref('stg_customers') }} c
LEFT JOIN customer_segments s
    ON c.customer_id = s.customer_id
```

### Paso 3: Agregar Tests

**Archivo: `models/marts/schema.yml`**

```yaml
version: 2

models:
  - name: dim_customers
    description: "Tabla dimensional de clientes con segmentación"

    columns:
      - name: customer_id
        description: "Primary key única"
        tests:
          - unique
          - not_null

      - name: email
        description: "Email normalizado del cliente"
        tests:
          - unique
          - not_null

      - name: segment
        description: |
          Segmento del cliente basado en lifetime value:
          - Bronze: < $100
          - Silver: $100 - $500
          - Gold: $500 - $1,000
          - Platinum: > $1,000
        tests:
          - accepted_values:
              values: ['Bronze', 'Silver', 'Gold', 'Platinum']

      - name: lifetime_value
        description: "Suma total de todas las órdenes"
        tests:
          - not_null

      - name: total_orders
        description: "Cantidad de órdenes del cliente"
```

### Paso 4: Ejecutar y Testear

```bash
# Ejecutar todos los modelos en orden correcto
dbt run

# dbt automáticamente ejecuta en este orden:
# 1. stg_customers (porque dim_customers depende de él)
# 2. stg_orders
# 3. dim_customers

# Ejecutar tests
dbt test --select dim_customers

# Output esperado:
# ✓ unique_dim_customers_customer_id ................ PASS
# ✓ not_null_dim_customers_customer_id .............. PASS
# ✓ unique_dim_customers_email ...................... PASS
# ✓ not_null_dim_customers_email .................... PASS
# ✓ accepted_values_dim_customers_segment ........... PASS
# ✓ not_null_dim_customers_lifetime_value ........... PASS
```

### Resultado Esperado

**Tabla: `marts.dim_customers`**

| customer_id | email | full_name | total_orders | lifetime_value | segment |
|---|---|---|---|---|---|
| 1 | john@gmail.com | John Smith | 2 | 450.00 | Silver |
| 2 | sarah@yahoo.com | Sarah Johnson | 1 | 75.00 | Bronze |
| 4 | bob@email.com | Bob Wilson | 1 | 500.00 | Gold |

### ✅ Qué Aprendimos

1. **ref()**: Referenciar otros modelos dbt (crea dependencias automáticas)
2. **WITH (CTEs)**: Estructurar SQL complejo de forma legible
3. **LEFT JOIN**: Incluir clientes sin órdenes
4. **COALESCE**: Manejar NULLs correctamente
5. **Tests**: Validar calidad de datos automáticamente
6. **schema.yml**: Documentar y testear modelos

---

## Ejemplo 3: Macros Reutilizables con Jinja

### Contexto

TechMart tiene múltiples columnas de dinero almacenadas en centavos (para evitar problemas de decimales). Queremos una función reutilizable para convertir centavos a dólares.

Además, tienen varios reportes que necesitan pivotar métodos de pago.

### Paso 1: Crear Macro para Centavos a Dólares

**Archivo: `macros/currency.sql`**

```sql
{% macro cents_to_dollars(column_name, precision=2) %}
{#
    Convierte una columna de centavos a dólares.

    Args:
        column_name: Nombre de la columna en centavos
        precision: Decimales a mostrar (default: 2)

    Returns:
        Expresión SQL que convierte centavos a dólares

    Example:
        {{ cents_to_dollars('amount_cents') }}
        {{ cents_to_dollars('tax_cents', precision=4) }}
#}
    ({{ column_name }} / 100.0)::NUMERIC(12, {{ precision }})
{% endmacro %}
```

### Paso 2: Crear Macro para Pivotar Métodos de Pago

**Archivo: `macros/pivot_payment_methods.sql`**

```sql
{% macro pivot_payment_methods() %}
{#
    Genera columnas pivotadas para cada método de pago.

    Métodos soportados:
    - credit_card
    - debit_card
    - paypal
    - bank_transfer
#}
{% set payment_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer'] %}

{% for method in payment_methods %}
    SUM(CASE WHEN payment_method = '{{ method }}' THEN amount ELSE 0 END) AS {{ method }}_total
    {{- "," if not loop.last }}
{% endfor %}

{% endmacro %}
```

### Paso 3: Usar Macros en Modelo

**Datos: `raw.payments`**

| payment_id | order_id | payment_method | amount_cents |
|---|---|---|---|
| 1 | 101 | credit_card | 15000 |
| 2 | 102 | paypal | 30000 |
| 3 | 103 | debit_card | 7500 |
| 4 | 104 | credit_card | 50000 |

**Archivo: `models/marts/fct_payments_summary.sql`**

```sql
{{ config(materialized='table') }}

WITH payments AS (
    SELECT
        payment_id,
        order_id,
        payment_method,
        -- Usar macro para convertir centavos a dólares
        {{ cents_to_dollars('amount_cents') }} AS amount_dollars
    FROM {{ source('raw', 'payments') }}
)

SELECT
    'Total' AS metric,

    -- Usar macro para pivotar métodos de pago
    {{ pivot_payment_methods() }}

FROM payments
```

### Paso 4: Compilar y Ver SQL Generado

```bash
dbt compile --select fct_payments_summary

# Ver el SQL compilado en target/compiled/...
```

**SQL Generado (lo que realmente se ejecuta):**

```sql
WITH payments AS (
    SELECT
        payment_id,
        order_id,
        payment_method,
        (amount_cents / 100.0)::NUMERIC(12, 2) AS amount_dollars
    FROM raw_data.payments
)

SELECT
    'Total' AS metric,

    SUM(CASE WHEN payment_method = 'credit_card' THEN amount ELSE 0 END) AS credit_card_total,
    SUM(CASE WHEN payment_method = 'debit_card' THEN amount ELSE 0 END) AS debit_card_total,
    SUM(CASE WHEN payment_method = 'paypal' THEN amount ELSE 0 END) AS paypal_total,
    SUM(CASE WHEN payment_method = 'bank_transfer' THEN amount ELSE 0 END) AS bank_transfer_total

FROM payments
```

### Resultado Esperado

| metric | credit_card_total | debit_card_total | paypal_total | bank_transfer_total |
|---|---|---|---|---|
| Total | 650.00 | 75.00 | 300.00 | 0.00 |

### ✅ Qué Aprendimos

1. **Macros**: Crear funciones SQL reutilizables
2. **Jinja loops**: Generar código dinámicamente
3. **Documentación en macros**: Usar comentarios `{# #}`
4. **Parámetros**: Macros pueden recibir argumentos
5. **dbt compile**: Ver el SQL final antes de ejecutarlo
6. **DRY**: No repetir lógica de conversión en cada modelo

---

## Ejemplo 4: Modelo Incremental para Logs de Eventos

### Contexto

TechMart tiene una tabla `raw.page_views` que recibe millones de eventos diarios. Reconstruir toda la tabla cada día es imposible (tardaría horas). Necesitamos un modelo incremental que solo procese eventos nuevos.

### Datos de Entrada

**Tabla: `raw.page_views` (crece constantemente)**

| event_id | user_id | page_url | event_timestamp |
|---|---|---|---|
| 1 | 101 | /home | 2024-11-01 10:00:00 |
| 2 | 102 | /products | 2024-11-01 10:05:00 |
| 3 | 101 | /cart | 2024-11-01 10:10:00 |
| ... | ... | ... | ... |
| 1000000 | 555 | /checkout | 2024-11-12 23:59:00 |

### Paso 1: Crear Modelo Incremental

**Archivo: `models/marts/fct_page_views.sql`**

```sql
{{
    config(
        materialized='incremental',
        unique_key='event_id',
        on_schema_change='fail',
        tags=['facts', 'incremental']
    )
}}

SELECT
    event_id,
    user_id,
    page_url,
    event_timestamp,
    DATE(event_timestamp) AS event_date,
    EXTRACT(HOUR FROM event_timestamp) AS event_hour,

    -- Clasificar tipo de página
    CASE
        WHEN page_url IN ('/checkout', '/payment') THEN 'conversion'
        WHEN page_url LIKE '/product/%' THEN 'product'
        WHEN page_url = '/cart' THEN 'cart'
        ELSE 'other'
    END AS page_type,

    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM {{ source('raw', 'page_views') }}

{% if is_incremental() %}
    -- En ejecuciones posteriores, solo procesar eventos nuevos
    -- desde el último evento que ya tenemos
    WHERE event_timestamp > (
        SELECT MAX(event_timestamp)
        FROM {{ this }}
    )
{% endif %}
```

### Paso 2: Primera Ejecución (Full Refresh)

```bash
# Primera ejecución: Carga TODOS los datos históricos
dbt run --select fct_page_views

# Internamente dbt ejecuta:
# CREATE TABLE marts.fct_page_views AS
# SELECT ... FROM raw.page_views
# (sin el filtro WHERE porque is_incremental() = False)
```

**Resultado**: Tabla con 1,000,000 registros creada.

### Paso 3: Ejecución Incremental (Al Día Siguiente)

Supongamos que al día siguiente hay 50,000 eventos nuevos.

```bash
# Segunda ejecución: Solo carga eventos nuevos
dbt run --select fct_page_views

# Internamente dbt ejecuta:
# INSERT INTO marts.fct_page_views
# SELECT ... FROM raw.page_views
# WHERE event_timestamp > '2024-11-12 23:59:00'
# (porque is_incremental() = True ahora)
```

**Resultado**: Solo 50,000 registros nuevos insertados (en segundos, no horas).

### Paso 4: Force Full Refresh si es Necesario

```bash
# Si necesitas reconstruir toda la tabla desde cero
dbt run --select fct_page_views --full-refresh

# Esto hace DROP TABLE y CREATE TABLE con todos los datos
```

### Paso 5: Agregar Test de Duplicados

**Archivo: `models/marts/schema.yml`**

```yaml
models:
  - name: fct_page_views
    description: "Tabla de hechos de page views (incremental)"

    columns:
      - name: event_id
        description: "Primary key del evento"
        tests:
          - unique
          - not_null

      - name: event_timestamp
        tests:
          - not_null
```

### ✅ Qué Aprendimos

1. **materialized='incremental'**: Procesar solo datos nuevos
2. **unique_key**: Identificar registros únicos para UPSERT
3. **is_incremental()**: Lógica diferente en primera vs siguientes ejecuciones
4. **{{ this }}**: Referencia a la tabla actual
5. **--full-refresh**: Flag para reconstruir todo desde cero
6. **on_schema_change='fail'**: Protección contra cambios de schema accidentales

---

## Ejemplo 5: Snapshot (SCD Type 2) - Histórico de Precios

### Contexto

TechMart quiere analizar cómo cambian los precios de productos a lo largo del tiempo. Si un producto cuesta $100 hoy y mañana sube a $120, queremos guardar ambos registros históricos.

Esto es **Slowly Changing Dimension Type 2**, que dbt puede hacer automáticamente con snapshots.

### Datos de Entrada

**Tabla: `raw.products` (se actualiza diariamente)**

**Día 1 (2024-11-01):**

| product_id | product_name | price | updated_at |
|---|---|---|---|
| 1 | Laptop Dell | 999.99 | 2024-11-01 |
| 2 | Mouse Logitech | 29.99 | 2024-11-01 |

**Día 2 (2024-11-02) - El precio del laptop cambió:**

| product_id | product_name | price | updated_at |
|---|---|---|---|
| 1 | Laptop Dell | 1099.99 | 2024-11-02 |
| 2 | Mouse Logitech | 29.99 | 2024-11-01 |

### Paso 1: Crear Snapshot

**Archivo: `snapshots/products_snapshot.sql`**

```sql
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

SELECT
    product_id,
    product_name,
    price,
    updated_at
FROM {{ source('raw', 'products') }}

{% endsnapshot %}
```

### Paso 2: Primera Ejecución del Snapshot (Día 1)

```bash
dbt snapshot

# dbt crea la tabla snapshots.products_snapshot
```

**Resultado Día 1:**

| product_id | product_name | price | updated_at | dbt_valid_from | dbt_valid_to | dbt_scd_id |
|---|---|---|---|---|---|---|
| 1 | Laptop Dell | 999.99 | 2024-11-01 | 2024-11-01 | NULL | abc123 |
| 2 | Mouse Logitech | 29.99 | 2024-11-01 | 2024-11-01 | NULL | def456 |

- `dbt_valid_from`: Cuándo este registro se volvió válido
- `dbt_valid_to`: Cuándo dejó de ser válido (NULL = aún válido)
- `dbt_scd_id`: ID único del snapshot

### Paso 3: Segunda Ejecución (Día 2 - Después del Cambio)

```bash
# Al día siguiente, ejecutar snapshot nuevamente
dbt snapshot
```

**Resultado Día 2:**

| product_id | product_name | price | updated_at | dbt_valid_from | dbt_valid_to | dbt_scd_id |
|---|---|---|---|---|---|---|
| 1 | Laptop Dell | 999.99 | 2024-11-01 | 2024-11-01 | **2024-11-02** | abc123 |
| 1 | **Laptop Dell** | **1099.99** | **2024-11-02** | **2024-11-02** | **NULL** | **xyz789** |
| 2 | Mouse Logitech | 29.99 | 2024-11-01 | 2024-11-01 | NULL | def456 |

**¿Qué pasó?**
1. dbt detectó que `product_id=1` cambió (comparó `updated_at`)
2. Marcó el registro viejo como inválido (`dbt_valid_to = 2024-11-02`)
3. Insertó un nuevo registro con el precio nuevo

### Paso 4: Consultar Histórico

**Query: Ver precio del laptop en cualquier fecha**

```sql
-- ¿Cuál era el precio del laptop el 2024-11-01?
SELECT product_name, price
FROM snapshots.products_snapshot
WHERE product_id = 1
  AND dbt_valid_from <= '2024-11-01'
  AND (dbt_valid_to > '2024-11-01' OR dbt_valid_to IS NULL)
-- Resultado: $999.99

-- ¿Cuál es el precio actual?
SELECT product_name, price
FROM snapshots.products_snapshot
WHERE product_id = 1
  AND dbt_valid_to IS NULL
-- Resultado: $1099.99
```

### Paso 5: Crear Vista Helper para "Current State"

**Archivo: `models/marts/dim_products_current.sql`**

```sql
{{ config(materialized='view') }}

-- Vista que solo muestra registros actuales del snapshot
SELECT
    product_id,
    product_name,
    price AS current_price,
    updated_at
FROM {{ ref('products_snapshot') }}
WHERE dbt_valid_to IS NULL
```

### ✅ Qué Aprendimos

1. **snapshot**: SCD Type 2 automático con dbt
2. **strategy='timestamp'**: Detectar cambios por columna de timestamp
3. **unique_key**: Identificar qué registros comparar
4. **dbt_valid_from/to**: Columnas automáticas de validez temporal
5. **invalidate_hard_deletes**: Marcar como inválidos registros eliminados
6. **Queries históricas**: Consultar datos "as of" cualquier fecha

---

## Resumen de los Ejemplos

| Ejemplo | Concepto Principal | Materialización | Dificultad |
|---|---|---|---|
| 1. Limpieza de clientes | Models, sources, transformaciones básicas | view | ⭐ Básico |
| 2. Dimensión con tests | refs, tests, documentación | table | ⭐⭐ Básico-Intermedio |
| 3. Macros reutilizables | Jinja, macros, DRY | table | ⭐⭐ Intermedio |
| 4. Logs incrementales | Modelos incrementales, `is_incremental()` | incremental | ⭐⭐⭐ Intermedio-Avanzado |
| 5. Snapshot de precios | SCD Type 2, snapshots, históricos | snapshot | ⭐⭐⭐ Avanzado |

### Próximos Pasos

Ahora que has visto ejemplos prácticos:

1. **Practica**: Crea tu propio proyecto dbt con datos similares
2. **Ejercicios**: Resuelve los ejercicios en `03-EJERCICIOS.md`
3. **Proyecto**: Implementa el pipeline completo en `04-proyecto-practico/`

**Tips para practicar:**
- Instala PostgreSQL localmente o usa Docker
- Crea tablas `raw.*` con datos de ejemplo
- Ejecuta cada ejemplo paso a paso
- Usa `dbt docs generate` para ver el lineage graph
- Experimenta modificando los modelos

---

**¡Excelente trabajo!** 🎉 Ahora dominas los fundamentos de dbt con ejemplos prácticos.

**Siguiente paso**: [`03-EJERCICIOS.md`](./03-EJERCICIOS.md) - Ejercicios para practicar tus habilidades de dbt.
