# Ejercicios Prácticos: dbt (data build tool)

## Introducción

Estos ejercicios te permitirán practicar dbt con **FinTech Analytics**, la empresa fintech del Tema 2. Como Data Engineer en **DataFlow Industries**, ayudarás a este cliente con su Data Warehouse. Cada ejercicio tiene:
- 🎯 **Contexto**: Problema de negocio real
- 📊 **Datos**: Tablas de entrada
- ❓ **Pregunta**: Qué debes construir
- 💡 **Pista**: Ayuda sutil sin dar la solución
- ✅ **Solución**: Código completo con explicación

**Recomendación**: Intenta resolver cada ejercicio sin mirar la solución primero. Usa las pistas solo si te atascas.

---

## Ejercicios Básicos

### Ejercicio 1: Staging de Productos

**Dificultad**: ⭐ Básico

**Contexto**:

FinTech Analytics tiene una tabla `raw.products` con datos de productos importados de su sistema ERP. Los datos tienen problemas:
- SKUs en mayúsculas inconsistentes
- Descripciones con espacios extra
- Precios negativos (errores de carga)
- Categorías con typos

**Datos** (`raw.products`):

| product_id | sku | name | description | price | category |
|---|---|---|---|---|---|
| 1 | LAPTOP-001 | Dell XPS 15 |   High performance laptop   | 1299.99 | electronics |
| 2 | mouse-002 | Logitech MX | Wireless mouse | 79.99 | ELECTRONICS |
| 3 | KB-003 | Keyboard Mech | Mechanical keyboard | -50.00 | accesories |

**Pregunta**:

Crea un modelo de staging `stg_products.sql` que:
1. Normalice SKUs a mayúsculas
2. Limpie espacios en `description`
3. Filtre productos con precio <= 0
4. Normalice categorías a lowercase

**Pista**:

Usa `UPPER()`, `TRIM()`, `LOWER()` y `WHERE` para filtrar.

---

### Ejercicio 2: Tests de Calidad Básicos

**Dificultad**: ⭐ Básico

**Contexto**:

Después de crear `stg_products`, necesitas asegurar la calidad de datos con tests automáticos.

**Pregunta**:

Crea un archivo `schema.yml` que defina tests para `stg_products`:
1. `product_id` debe ser único y no nulo
2. `sku` debe ser único
3. `category` solo puede ser: 'electronics', 'accessories', 'clothing'
4. `price` debe ser mayor a 0 (test personalizado)

**Pista**:

Usa `unique`, `not_null`, `accepted_values` en `schema.yml`. Para el test custom, crea un archivo en `tests/`.

---

### Ejercicio 3: Referencias entre Modelos

**Dificultad**: ⭐ Básico

**Contexto**:

Necesitas crear una tabla `dim_products` que use `stg_products` y agregue información calculada.

**Datos adicionales** (`raw.product_reviews`):

| review_id | product_id | rating | review_date |
|---|---|---|---|
| 1 | 1 | 5 | 2024-11-01 |
| 2 | 1 | 4 | 2024-11-02 |
| 3 | 2 | 5 | 2024-11-03 |

**Pregunta**:

Crea `dim_products.sql` que:
1. Use `{{ ref('stg_products') }}` como base
2. Agregue `average_rating` (promedio de ratings)
3. Agregue `total_reviews` (cantidad de reviews)
4. Incluya productos sin reviews (usa LEFT JOIN, rating = NULL)

**Pista**:

Usa `{{ ref('modelo') }}` para referenciar. Recuerda `GROUP BY` y `LEFT JOIN`.

---

### Ejercicio 4: Source Definitions

**Dificultad**: ⭐ Básico

**Contexto**:

En vez de referenciar `raw.products` directamente en SQL, quieres definirlo como un source para que dbt lo valide.

**Pregunta**:

Crea `models/staging/sources.yml` que:
1. Defina un source llamado `raw`
2. Incluya la tabla `products` con descripción
3. Agregue un test `not_null` en la columna `product_id`
4. Modifica `stg_products.sql` para usar `{{ source('raw', 'products') }}`

**Pista**:

```yaml
sources:
  - name: raw
    tables:
      - name: products
        columns:
          - name: product_id
            tests:
              - not_null
```

---

## Ejercicios Intermedios

### Ejercicio 5: Macro para Formateo de Nombres

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:

FinTech Analytics tiene varias tablas con nombres de personas (customers, employees, vendors) y quieres una función reutilizable para formatearlos consistentemente.

**Pregunta**:

Crea un macro `macros/format_name.sql` que:
1. Reciba `first_name` y `last_name`
2. Retorne nombre completo en formato "Apellido, Nombre" (Title Case)
3. Ejemplo: `format_name('john', 'SMITH')` → "Smith, John"

Úsalo en un modelo `dim_customers.sql`.

**Pista**:

```sql
{% macro format_name(first, last) %}
    CONCAT(INITCAP(TRIM({{ last }})), ', ', INITCAP(TRIM({{ first }})))
{% endmacro %}
```

---

### Ejercicio 6: Modelo con CTEs Complejos

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:

Necesitas crear `fct_daily_sales` que agregue ventas por día, producto y categoría.

**Datos** (`raw.order_items`):

| order_item_id | order_id | product_id | quantity | unit_price | order_date |
|---|---|---|---|---|---|
| 1 | 101 | 1 | 2 | 1299.99 | 2024-11-01 |
| 2 | 101 | 2 | 1 | 79.99 | 2024-11-01 |
| 3 | 102 | 1 | 1 | 1299.99 | 2024-11-02 |

**Pregunta**:

Crea `fct_daily_sales.sql` con múltiples CTEs:
1. **CTE 1** (`order_items_enriched`): JOIN con `dim_products` para obtener categoría
2. **CTE 2** (`daily_aggregates`): Agrupar por fecha, producto, categoría
3. **SELECT final**: Calcular `total_revenue` (quantity * unit_price), `total_units`

**Pista**:

```sql
WITH cte1 AS (...),
     cte2 AS (...)
SELECT ... FROM cte2
```

---

### Ejercicio 7: Test Personalizado de Lógica de Negocio

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:

FinTech Analytics tiene una regla: Todas las órdenes deben tener al menos 1 item. Quieres un test que valide esto.

**Pregunta**:

Crea un test `tests/assert_orders_have_items.sql` que:
1. Identifique órdenes en `fct_orders` que no tienen items en `fct_order_items`
2. El test debe FALLAR si encuentra órdenes huérfanas

**Pista**:

Los tests en dbt fallan cuando el SELECT retorna filas. Usa `NOT IN` o `LEFT JOIN ... WHERE ... IS NULL`.

---

### Ejercicio 8: Jinja para Generar Múltiples Columnas

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:

Quieres crear un reporte de ventas por mes para los últimos 12 meses, pero no quieres escribir 12 columnas manualmente.

**Pregunta**:

Crea `models/reports/monthly_sales_pivot.sql` que:
1. Use un loop de Jinja para generar columnas `month_1`, `month_2`, ..., `month_12`
2. Cada columna debe sumar ventas de ese mes usando `CASE WHEN`

**Ejemplo de output esperado:**

| product_id | month_1 | month_2 | month_3 | ... | month_12 |
|---|---|---|---|---|---|
| 1 | 5000 | 6000 | 5500 | ... | 7000 |

**Pista**:

```sql
{% for month in range(1, 13) %}
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = {{ month }} THEN revenue ELSE 0 END) AS month_{{ month }}
    {{- "," if not loop.last }}
{% endfor %}
```

---

### Ejercicio 9: Documentación Completa de un Modelo

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:

El modelo `dim_customers` es crítico y necesita documentación completa para que otros lo entiendan.

**Pregunta**:

Crea/actualiza `schema.yml` para `dim_customers` con:
1. Descripción del modelo (qué hace, fuentes, frecuencia de actualización)
2. Descripción de cada columna
3. Tests en `customer_id` (unique, not_null)
4. Test en `segment` (accepted_values: Bronze, Silver, Gold, Platinum)
5. Test de relación: `customer_id` existe en `stg_customers`

**Pista**:

```yaml
models:
  - name: dim_customers
    description: |
      Tabla dimensional de clientes...

      **Fuentes**: stg_customers, stg_orders
      **Frecuencia**: Diaria

    columns:
      - name: customer_id
        description: "Primary key..."
        tests: [unique, not_null]
```

---

### Ejercicio 10: Materialización Mixta

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:

Quieres configurar tu proyecto para que:
- Modelos en `staging/` sean views (rápidos de reconstruir)
- Modelos en `marts/` sean tables (para performance de queries)

**Pregunta**:

Modifica `dbt_project.yml` para configurar materializaciones por carpeta:

**Pista**:

```yaml
models:
  mi_proyecto:
    staging:
      +materialized: view
    marts:
      +materialized: table
```

---

## Ejercicios Avanzados

### Ejercicio 11: Modelo Incremental con Estrategia Merge

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:

FinTech Analytics tiene una tabla `raw.customer_sessions` que crece diariamente con millones de filas. Necesitas un modelo incremental que:
- Inserte sesiones nuevas
- Actualice sesiones existentes si cambian (ej: duración actualizada)

**Datos** (`raw.customer_sessions`):

| session_id | customer_id | start_time | end_time | page_views |
|---|---|---|---|---|
| s1 | 101 | 2024-11-01 10:00 | 2024-11-01 10:30 | 5 |
| s2 | 102 | 2024-11-01 11:00 | 2024-11-01 11:15 | 3 |

**Pregunta**:

Crea `fct_customer_sessions.sql` que:
1. Use `materialized='incremental'`
2. Use estrategia `merge` con `unique_key='session_id'`
3. Solo procese sesiones del último día en runs incrementales
4. Calcule `duration_minutes` (diferencia entre end_time y start_time)

**Pista**:

```sql
{{ config(
    materialized='incremental',
    unique_key='session_id',
    incremental_strategy='merge'
) }}

SELECT ...
FROM {{ source('raw', 'customer_sessions') }}

{% if is_incremental() %}
WHERE start_time >= CURRENT_DATE - INTERVAL '1 day'
{% endif %}
```

---

### Ejercicio 12: Snapshot con Hard Deletes

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:

Los precios de productos cambian constantemente y a veces productos se discontinúan (eliminados de `raw.products`). Quieres histórico completo incluyendo productos eliminados.

**Pregunta**:

Crea `snapshots/products_price_history.sql` que:
1. Use strategy `timestamp` con columna `updated_at`
2. Habilite `invalidate_hard_deletes=True` (marca como inválidos productos eliminados)
3. Incluya todas las columnas de `raw.products`

Luego crea una consulta SQL que muestre:
- Productos que tuvieron cambio de precio
- Precio anterior y precio nuevo
- Fecha del cambio

**Pista**:

```sql
{% snapshot products_price_history %}
{{ config(
    target_schema='snapshots',
    unique_key='product_id',
    strategy='timestamp',
    updated_at='updated_at',
    invalidate_hard_deletes=True
) }}

SELECT * FROM {{ source('raw', 'products') }}
{% endsnapshot %}
```

**Query para detectar cambios:**
```sql
WITH current_prices AS (
    SELECT product_id, price, dbt_valid_from
    FROM snapshots.products_price_history
    WHERE dbt_valid_to IS NULL
),
previous_prices AS (
    SELECT
        product_id,
        price AS previous_price,
        dbt_valid_to AS change_date
    FROM snapshots.products_price_history
    WHERE dbt_valid_to IS NOT NULL
)

SELECT
    c.product_id,
    p.previous_price,
    c.price AS current_price,
    p.change_date
FROM current_prices c
INNER JOIN previous_prices p ON c.product_id = p.product_id
WHERE c.price != p.previous_price
```

---

### Ejercicio 13: dbt-utils y Macros Avanzados

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:

Quieres usar el paquete `dbt-utils` para funciones avanzadas.

**Pregunta**:

1. Instala `dbt-utils` creando `packages.yml`:
   ```yaml
   packages:
     - package: dbt-labs/dbt_utils
       version: 1.1.0
   ```

2. Ejecuta `dbt deps`

3. Crea `dim_products_enhanced.sql` que use:
   - `generate_surrogate_key()` para crear una surrogate key combinando `product_id` y `category`
   - `pivot()` para pivotar ratings por estrella (1-5 estrellas)

**Pista**:

```sql
SELECT
    {{ dbt_utils.generate_surrogate_key(['product_id', 'category']) }} AS product_key,
    product_id,
    category,
    {{ dbt_utils.pivot(
        column='rating',
        values=[1, 2, 3, 4, 5],
        agg='count',
        then_value='1'
    ) }}
FROM ...
```

---

### Ejercicio 14: Debugging de Modelo que Falla

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:

Un colega creó este modelo pero falla con error `column "total_revenue" does not exist`:

```sql
{{ config(materialized='table') }}

WITH order_totals AS (
    SELECT
        order_id,
        SUM(quantity * price) AS total_revenue
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
)

SELECT
    customer_id,
    SUM(total_revenue) AS customer_lifetime_value
FROM {{ ref('stg_orders') }} o
INNER JOIN order_totals ot ON o.order_id = ot.order_id
GROUP BY customer_id
ORDER BY customer_lifetime_value DESC
```

**Pregunta**:

1. Identifica el error
2. Corrígelo
3. Explica por qué fallaba

**Pista**:

El problema está en el SELECT final. ¿De dónde viene `total_revenue`?

---

### Ejercicio 15: Pipeline Completo end-to-end

**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:

Diseña un pipeline completo de dbt para FinTech Analytics que transforme datos crudos en tablas analíticas.

**Pregunta**:

Crea un pipeline con esta estructura:

```
raw.customers
raw.products
raw.orders
raw.order_items
    ↓ (staging)
stg_customers
stg_products
stg_orders
stg_order_items
    ↓ (intermediate - opcional)
int_orders_with_items
    ↓ (marts)
dim_customers
dim_products
dim_date
fct_orders
```

**Requisitos**:
1. Todos los modelos staging deben ser views
2. Todos los modelos marts deben ser tables
3. `dim_customers` debe incluir segmentación por lifetime value
4. `fct_orders` debe incluir revenue total por orden
5. Agregar tests a todas las primary keys
6. Documentar todos los modelos en `schema.yml`

**Pista**:

Empieza por los modelos staging, luego avanza hacia marts. Usa `{{ ref() }}` para dependencias.

---

## Soluciones

### Solución Ejercicio 1

**Archivo**: `models/staging/stg_products.sql`

```sql
{{ config(materialized='view') }}

SELECT
    product_id,
    UPPER(TRIM(sku)) AS sku,
    TRIM(name) AS name,
    TRIM(description) AS description,
    price,
    LOWER(TRIM(category)) AS category,
    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM {{ source('raw', 'products') }}
WHERE price > 0  -- Filtrar precios inválidos
```

**Explicación**:
- `UPPER(sku)`: Normaliza SKUs a mayúsculas
- `TRIM()`: Elimina espacios extra
- `LOWER(category)`: Normaliza categorías
- `WHERE price > 0`: Filtra el producto con precio -50.00

**Resultado esperado**:

| product_id | sku | name | description | price | category |
|---|---|---|---|---|---|
| 1 | LAPTOP-001 | Dell XPS 15 | High performance laptop | 1299.99 | electronics |
| 2 | MOUSE-002 | Logitech MX | Wireless mouse | 79.99 | electronics |

(El producto 3 fue filtrado por precio negativo)

---

### Solución Ejercicio 2

**Archivo**: `models/staging/schema.yml`

```yaml
version: 2

models:
  - name: stg_products
    description: "Productos limpios de la base transaccional"

    columns:
      - name: product_id
        description: "Primary key del producto"
        tests:
          - unique
          - not_null

      - name: sku
        description: "SKU normalizado (mayúsculas)"
        tests:
          - unique

      - name: category
        description: "Categoría del producto"
        tests:
          - accepted_values:
              values: ['electronics', 'accessories', 'clothing']

      - name: price
        description: "Precio del producto (debe ser > 0)"
```

**Archivo**: `tests/assert_positive_price.sql`

```sql
-- Test personalizado: precio debe ser positivo
SELECT *
FROM {{ ref('stg_products') }}
WHERE price <= 0
```

**Ejecutar**:
```bash
dbt test --select stg_products

# ✓ unique_stg_products_product_id ......... PASS
# ✓ not_null_stg_products_product_id ....... PASS
# ✓ unique_stg_products_sku ................ PASS
# ✓ accepted_values_stg_products_category .. PASS
# ✓ assert_positive_price .................. PASS
```

---

### Solución Ejercicio 3

**Archivo**: `models/staging/stg_product_reviews.sql`

```sql
{{ config(materialized='view') }}

SELECT
    review_id,
    product_id,
    rating,
    review_date
FROM {{ source('raw', 'product_reviews') }}
```

**Archivo**: `models/marts/dim_products.sql`

```sql
{{ config(materialized='table') }}

WITH review_stats AS (
    SELECT
        product_id,
        AVG(rating)::NUMERIC(3,2) AS average_rating,
        COUNT(*) AS total_reviews
    FROM {{ ref('stg_product_reviews') }}
    GROUP BY product_id
)

SELECT
    p.product_id,
    p.sku,
    p.name,
    p.description,
    p.price,
    p.category,

    -- Métricas de reviews (NULL si no tiene reviews)
    r.average_rating,
    COALESCE(r.total_reviews, 0) AS total_reviews,

    CURRENT_TIMESTAMP AS dbt_loaded_at
FROM {{ ref('stg_products') }} p
LEFT JOIN review_stats r
    ON p.product_id = r.product_id
```

**Resultado esperado**:

| product_id | sku | name | average_rating | total_reviews |
|---|---|---|---|---|
| 1 | LAPTOP-001 | Dell XPS 15 | 4.50 | 2 |
| 2 | MOUSE-002 | Logitech MX | 5.00 | 1 |

---

### Solución Ejercicio 4

**Archivo**: `models/staging/sources.yml`

```yaml
version: 2

sources:
  - name: raw
    description: "Esquema de datos crudos"
    schema: raw_data

    tables:
      - name: products
        description: "Productos desde el sistema ERP"
        columns:
          - name: product_id
            description: "Primary key"
            tests:
              - not_null
          - name: sku
            tests:
              - unique
```

**Modificar**: `models/staging/stg_products.sql`

```sql
-- Cambiar:
FROM raw.products

-- Por:
FROM {{ source('raw', 'products') }}
```

**Ventaja**: Ahora dbt puede testear que la tabla fuente existe antes de ejecutar modelos.

---

### Solución Ejercicio 5

**Archivo**: `macros/format_name.sql`

```sql
{% macro format_name(first_name, last_name) %}
{#
    Formatea nombre completo como "Apellido, Nombre" en Title Case.

    Args:
        first_name: Columna con nombre
        last_name: Columna con apellido

    Returns:
        String formateado

    Example:
        {{ format_name('first_name', 'last_name') }}
#}
    CONCAT(
        INITCAP(TRIM({{ last_name }})),
        ', ',
        INITCAP(TRIM({{ first_name }}))
    )
{% endmacro %}
```

**Uso en**: `models/marts/dim_customers.sql`

```sql
{{ config(materialized='table') }}

SELECT
    customer_id,
    email,
    {{ format_name('first_name', 'last_name') }} AS full_name_formatted,
    phone,
    created_at
FROM {{ ref('stg_customers') }}
```

**Resultado**:

| customer_id | email | full_name_formatted |
|---|---|---|
| 1 | john@gmail.com | Smith, John |
| 2 | sarah@yahoo.com | Johnson, Sarah |

---

### Solución Ejercicio 6

**Archivo**: `models/marts/fct_daily_sales.sql`

```sql
{{ config(materialized='table') }}

WITH order_items_enriched AS (
    -- CTE 1: Enriquecer order items con info de producto
    SELECT
        oi.order_item_id,
        oi.order_id,
        oi.product_id,
        oi.quantity,
        oi.unit_price,
        oi.order_date,
        p.category
    FROM {{ ref('stg_order_items') }} oi
    INNER JOIN {{ ref('dim_products') }} p
        ON oi.product_id = p.product_id
),

daily_aggregates AS (
    -- CTE 2: Agregar por día, producto, categoría
    SELECT
        order_date,
        product_id,
        category,
        SUM(quantity) AS total_units,
        SUM(quantity * unit_price) AS total_revenue
    FROM order_items_enriched
    GROUP BY order_date, product_id, category
)

SELECT
    order_date,
    product_id,
    category,
    total_units,
    total_revenue,
    ROUND(total_revenue / NULLIF(total_units, 0), 2) AS avg_unit_price
FROM daily_aggregates
ORDER BY order_date DESC, total_revenue DESC
```

**Explicación**:
- **CTE 1**: JOIN con dim_products para obtener categoría
- **CTE 2**: GROUP BY para agregar métricas
- **SELECT final**: Calcula precio promedio por unidad
- `NULLIF(total_units, 0)`: Previene división por cero

---

### Solución Ejercicio 7

**Archivo**: `tests/assert_orders_have_items.sql`

```sql
-- Test: Todas las órdenes deben tener al menos 1 item
SELECT
    o.order_id
FROM {{ ref('fct_orders') }} o
WHERE o.order_id NOT IN (
    SELECT DISTINCT order_id
    FROM {{ ref('fct_order_items') }}
)
```

**Explicación**:
- Busca órdenes en `fct_orders` que NO están en `fct_order_items`
- Si el SELECT retorna filas → Test FALLA
- Si retorna vacío → Test PASA

**Alternativa con LEFT JOIN:**
```sql
SELECT o.order_id
FROM {{ ref('fct_orders') }} o
LEFT JOIN {{ ref('fct_order_items') }} oi
    ON o.order_id = oi.order_id
WHERE oi.order_id IS NULL
```

---

### Solución Ejercicio 8

**Archivo**: `models/reports/monthly_sales_pivot.sql`

```sql
{{ config(materialized='table') }}

SELECT
    product_id,

    {% for month in range(1, 13) %}
    SUM(
        CASE
            WHEN EXTRACT(MONTH FROM order_date) = {{ month }}
            THEN revenue
            ELSE 0
        END
    ) AS month_{{ month }}
    {{- "," if not loop.last }}
    {% endfor %}

FROM {{ ref('fct_daily_sales') }}
GROUP BY product_id
```

**SQL Compilado (ver con `dbt compile`):**

```sql
SELECT
    product_id,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 1 THEN revenue ELSE 0 END) AS month_1,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 2 THEN revenue ELSE 0 END) AS month_2,
    -- ... hasta month_12
FROM analytics.fct_daily_sales
GROUP BY product_id
```

---

### Solución Ejercicio 11

**Archivo**: `models/marts/fct_customer_sessions.sql`

```sql
{{
    config(
        materialized='incremental',
        unique_key='session_id',
        incremental_strategy='merge',
        on_schema_change='fail'
    )
}}

SELECT
    session_id,
    customer_id,
    start_time,
    end_time,
    page_views,

    -- Calcular duración en minutos
    EXTRACT(EPOCH FROM (end_time - start_time)) / 60.0 AS duration_minutes,

    CURRENT_TIMESTAMP AS dbt_loaded_at

FROM {{ source('raw', 'customer_sessions') }}

{% if is_incremental() %}
    -- Solo procesar sesiones del último día
    WHERE DATE(start_time) >= CURRENT_DATE - INTERVAL '1 day'
{% endif %}
```

**Explicación**:
- **Primera ejecución**: Carga todas las sesiones históricas
- **Siguientes ejecuciones**: Solo sesiones del último día
- **Estrategia merge**: Si `session_id` ya existe → UPDATE, si no → INSERT
- `EXTRACT(EPOCH ...)`: Calcula diferencia en segundos, divide por 60 para minutos

**Probar**:
```bash
# Primera ejecución (full)
dbt run --select fct_customer_sessions

# Segunda ejecución (solo nuevos)
dbt run --select fct_customer_sessions

# Forzar full refresh
dbt run --select fct_customer_sessions --full-refresh
```

---

### Solución Ejercicio 14

**Error Identificado**:

El problema está en esta línea:
```sql
SUM(total_revenue) AS customer_lifetime_value
```

`total_revenue` está en el CTE `order_totals`, pero el SELECT final hace JOIN con `stg_orders` y no selecciona `total_revenue` en el JOIN.

**Corrección**:

```sql
{{ config(materialized='table') }}

WITH order_totals AS (
    SELECT
        order_id,
        SUM(quantity * price) AS total_revenue
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
)

SELECT
    o.customer_id,  -- Prefijo 'o.' para claridad
    SUM(ot.total_revenue) AS customer_lifetime_value  -- Prefijo 'ot.'
FROM {{ ref('stg_orders') }} o
INNER JOIN order_totals ot ON o.order_id = ot.order_id
GROUP BY o.customer_id
ORDER BY customer_lifetime_value DESC
```

**Explicación del error**:
Cuando haces JOIN entre tablas, debes especificar de qué tabla viene cada columna usando alias (`o.customer_id`, `ot.total_revenue`). El SQL original no tenía el prefijo `ot.` en `total_revenue`.

---

## Resumen de Ejercicios

| Ejercicio | Concepto | Dificultad | Archivos Creados |
|---|---|---|---|
| 1. Staging de productos | Models, transformaciones | ⭐ | stg_products.sql |
| 2. Tests básicos | Tests genéricos y custom | ⭐ | schema.yml, test SQL |
| 3. Referencias | refs, JOINs | ⭐ | dim_products.sql |
| 4. Sources | source(), validación | ⭐ | sources.yml |
| 5. Macros | Funciones reutilizables | ⭐⭐ | macros/format_name.sql |
| 6. CTEs complejos | WITH, agregaciones | ⭐⭐ | fct_daily_sales.sql |
| 7. Tests custom | Lógica de negocio | ⭐⭐ | assert_orders_have_items.sql |
| 8. Jinja loops | Templating dinámico | ⭐⭐ | monthly_sales_pivot.sql |
| 9. Documentación | schema.yml completo | ⭐⭐ | schema.yml |
| 10. Configuración | dbt_project.yml | ⭐⭐ | dbt_project.yml |
| 11. Incremental merge | Modelos incrementales | ⭐⭐⭐ | fct_customer_sessions.sql |
| 12. Snapshots | SCD Type 2 | ⭐⭐⭐ | products_price_history.sql |
| 13. dbt-utils | Paquetes externos | ⭐⭐⭐ | packages.yml |
| 14. Debugging | Resolución de errores | ⭐⭐⭐ | N/A |
| 15. Pipeline completo | Arquitectura end-to-end | ⭐⭐⭐ | Múltiples archivos |

---

## Próximos Pasos

¡Felicidades por completar los ejercicios! Ahora estás listo para:

1. **Proyecto Práctico**: Implementar un pipeline dbt completo en `04-proyecto-practico/`
2. **Práctica Real**: Configurar dbt en tu propio Data Warehouse
3. **Avanzar**: Aprender dbt Cloud, Airflow + dbt, CI/CD con GitHub Actions

**Recuerda**:
- Practica creando tus propios modelos
- Usa `dbt docs generate` para ver el lineage graph
- Ejecuta `dbt test` frecuentemente
- Lee la [documentación oficial de dbt](https://docs.getdbt.com/)

---

**¡Excelente trabajo!** 🎉 Ahora dominas dbt desde básico hasta avanzado.

**Siguiente paso**: [`04-proyecto-practico/`](./04-proyecto-practico/) - Pipeline completo de Data Warehouse con dbt.
