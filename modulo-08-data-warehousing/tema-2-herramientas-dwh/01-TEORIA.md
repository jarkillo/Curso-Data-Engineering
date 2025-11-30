# Tema 2: dbt (data build tool) - Transformaciones Modernas en Data Warehouses

## Introducción

### ¿Por qué existe dbt?

Imagina que eres un ingeniero de datos en una empresa de e-commerce. Tienes un Data Warehouse con datos crudos de ventas, productos y clientes. Necesitas transformar esos datos para crear tablas limpias que los analistas puedan consultar. Tradicionalmente, tendrías dos opciones:

**Opción 1**: Escribir scripts Python con Pandas (lo que viste en el Módulo 3)
- ❌ Los analistas no saben Python
- ❌ Difícil de mantener
- ❌ Sin tests automáticos
- ❌ Sin documentación automática

**Opción 2**: Escribir SQL a mano en el Data Warehouse
- ❌ Código duplicado everywhere
- ❌ Sin control de versiones claro
- ❌ Difícil de testear
- ❌ Sin documentación
- ❌ ¿Qué tabla se creó primero? Nadie lo sabe

**dbt es la solución moderna**: Te permite escribir SQL (que todos conocen), pero con:
- ✅ **Tests automáticos** sobre tus datos
- ✅ **Documentación automática** con lineage visual
- ✅ **Versionado con Git** (como código normal)
- ✅ **Reutilización de código** con macros
- ✅ **Dependencias claras** entre tablas
- ✅ **CI/CD** para validar cambios antes de producción

### Contexto Real en Data Engineering

**Caso de uso típico:**

En **DataMart Inc.**, una empresa de analytics, tienen un proceso así:

1. **Extract**: Datos crudos llegan a PostgreSQL cada hora desde múltiples fuentes (Salesforce, Google Analytics, bases de datos transaccionales)

2. **Load**: Los datos crudos se cargan en un esquema `raw` del Data Warehouse sin transformaciones

3. **Transform** (AQUÍ ENTRA dbt): dbt transforma los datos crudos en tablas analíticas:
   - `raw.salesforce_leads` → `analytics.leads_cleaned` → `analytics.leads_scored`
   - `raw.ga_sessions` → `analytics.web_traffic` → `analytics.marketing_attribution`
   - Combina múltiples fuentes en tablas consolidadas

4. **BI Tools**: Metabase/Tableau/Looker consultan las tablas finales

**¿Por qué usar dbt y no Python?**
- Los analistas de negocio saben SQL, no Python
- SQL es más eficiente para transformaciones grandes (se ejecuta en el DWH, no en memoria)
- dbt genera documentación y lineage automáticamente
- Tests sobre datos, no sobre código

### Analogía del Mundo Real

Piensa en dbt como **Git para tu Data Warehouse**:

- **Git** versiona tu código → **dbt** versiona tus transformaciones SQL
- **Git** tiene branches → **dbt** permite desarrollar transformaciones sin romper producción
- **Git** tiene pull requests con tests → **dbt** ejecuta tests antes de deployar cambios
- **Git** documenta cambios → **dbt** documenta automáticamente qué tabla depende de cuál

O piensa en dbt como **"React/Vue para SQL"**:
- React tiene componentes reutilizables → dbt tiene modelos reutilizables
- React tiene props → dbt tiene refs (referencias)
- React renderiza automáticamente cuando hay cambios → dbt reconstruye tablas cuando sus dependencias cambian

---

## Conceptos Fundamentales

### ¿Qué es dbt?

**dbt (data build tool)** es una herramienta de **transformación de datos** que:

1. **Toma como input**: Datos crudos en tu Data Warehouse (PostgreSQL, Snowflake, BigQuery, etc.)
2. **Transforma**: Usando SQL + Jinja templating
3. **Produce como output**: Tablas/vistas limpias y documentadas en tu DWH

**Filosofía central de dbt:**
> "Bring software engineering best practices to analytics"

Esto significa:
- **Modularidad**: Una transformación = Un archivo `.sql`
- **Testing**: Tests automáticos sobre datos
- **Documentación**: Generada automáticamente
- **DRY (Don't Repeat Yourself)**: Macros reutilizables
- **Dependency management**: dbt determina el orden de ejecución

### ELT vs ETL

**ETL tradicional (Extract-Transform-Load)**:
```
1. Extract: Leer datos de fuentes
2. Transform: Transformar EN UN SERVIDOR INTERMEDIO (Airflow worker, script Python)
3. Load: Cargar datos transformados al DWH
```

**ELT moderno (Extract-Load-Transform)**:
```
1. Extract: Leer datos de fuentes
2. Load: Cargar datos CRUDOS directamente al DWH
3. Transform: Transformar DENTRO DEL DWH usando dbt
```

**¿Por qué ELT es mejor para Data Warehouses?**
- ✅ Aprovecha la potencia del DWH (está optimizado para queries SQL complejos)
- ✅ No necesitas un servidor intermedio potente
- ✅ Los datos crudos están siempre disponibles (si la transformación falla, los crudos siguen ahí)
- ✅ Más fácil auditar y rehacer transformaciones

**dbt es la herramienta T en ELT.**

### dbt Core vs dbt Cloud

**dbt Core** (Open Source, Gratis):
- CLI (Command Line Interface)
- Ejecutas `dbt run` desde terminal
- Tú manejas la infraestructura (dónde correrlo, scheduling, logs)
- Ideal para: Desarrollo local, empresas con DevOps fuerte

**dbt Cloud** (SaaS, Pago):
- Interface web visual
- Scheduling incorporado (corre tus dbt jobs automáticamente)
- IDE en el browser
- Logs y monitoreo centralizados
- Ideal para: Empresas que quieren un producto listo, equipos no-técnicos

**En este curso usaremos dbt Core** porque:
- Es gratis
- Te enseña los fundamentos
- Todo lo que aprendas aplica a dbt Cloud

### Estructura de un Proyecto dbt

Un proyecto dbt típico se ve así:

```
mi_proyecto_dbt/
├── dbt_project.yml         # Configuración del proyecto
├── profiles.yml            # Conexiones a bases de datos (NO commitear)
├── models/                 # ⭐ Aquí viven tus transformaciones SQL
│   ├── staging/            #    Capa 1: Datos limpios básicos
│   │   ├── stg_customers.sql
│   │   └── stg_orders.sql
│   ├── intermediate/       #    Capa 2: Transformaciones intermedias
│   │   └── int_order_items_joined.sql
│   ├── marts/              #    Capa 3: Tablas finales para analistas
│   │   ├── dim_customers.sql
│   │   └── fct_orders.sql
│   └── schema.yml          #    Documentación y tests
├── macros/                 # Funciones SQL reutilizables
│   └── cents_to_dollars.sql
├── seeds/                  # Archivos CSV pequeños (datos estáticos)
│   └── country_codes.csv
├── snapshots/              # SCD Type 2 automático
│   └── customers_snapshot.sql
├── tests/                  # Tests personalizados
│   └── assert_positive_revenue.sql
└── analyses/               # Queries ad-hoc (no se ejecutan en dbt run)
    └── monthly_revenue.sql
```

**Conceptos clave:**

**models/**: Cada archivo `.sql` es un "modelo" (una transformación). dbt ejecutará ese SQL y creará una tabla/vista.

**dbt_project.yml**: Define nombre del proyecto, versión, materializations por defecto, etc.

**profiles.yml**: Define DÓNDE conectarse (PostgreSQL local, Snowflake prod, etc.). Este archivo NO se commitea a Git porque tiene credenciales.

---

## Models (Modelos)

### ¿Qué es un Modelo?

Un **modelo** en dbt es simplemente:
- Un archivo `.sql` con un `SELECT` statement
- dbt ejecuta ese SELECT y crea una tabla/vista con el resultado

**Ejemplo básico** (`models/stg_customers.sql`):

```sql
-- Limpiar datos de clientes
SELECT
    customer_id,
    LOWER(TRIM(email)) AS email,
    INITCAP(first_name) AS first_name,
    INITCAP(last_name) AS last_name,
    created_at
FROM raw.customers
WHERE email IS NOT NULL
```

Cuando ejecutas `dbt run`, dbt:
1. Lee ese archivo
2. Ejecuta el SQL en tu Data Warehouse
3. Crea la tabla/vista `analytics.stg_customers` (el schema depende de tu configuración)

### Tipos de Materialización

**Materialización** = Cómo dbt guarda el resultado de tu modelo.

Hay 4 tipos:

#### 1. **view** (Vista)

```sql
-- models/vw_active_customers.sql
{{ config(materialized='view') }}

SELECT * FROM {{ ref('stg_customers') }}
WHERE status = 'active'
```

- **Qué hace**: Crea una VIEW en la base de datos
- **Cuándo usarlo**: Datos que cambian frecuentemente, queries rápidos
- **Ventaja**: No ocupa espacio, siempre actualizado
- **Desventaja**: Cada query ejecuta el SELECT completo (puede ser lento)

#### 2. **table** (Tabla)

```sql
-- models/dim_customers.sql
{{ config(materialized='table') }}

SELECT
    customer_id,
    email,
    full_name,
    segment,
    lifetime_value
FROM {{ ref('stg_customers') }}
```

- **Qué hace**: Crea una TABLE física (hace DROP + CREATE)
- **Cuándo usarlo**: Queries complejos, muchos usuarios consultando
- **Ventaja**: Queries rápidos (los datos ya están materializados)
- **Desventaja**: Ocupa espacio, reconstruye TODO cada vez

#### 3. **incremental** (Incremental)

```sql
-- models/fct_page_views.sql
{{ config(
    materialized='incremental',
    unique_key='event_id'
) }}

SELECT
    event_id,
    user_id,
    page_url,
    event_timestamp
FROM {{ ref('stg_events') }}

{% if is_incremental() %}
-- Solo procesar eventos nuevos
WHERE event_timestamp > (SELECT MAX(event_timestamp) FROM {{ this }})
{% endif %}
```

- **Qué hace**: Primera vez → CREATE TABLE, siguientes veces → INSERT/UPDATE solo registros nuevos
- **Cuándo usarlo**: Tablas grandes que crecen con el tiempo (logs, eventos)
- **Ventaja**: Mucho más rápido que reconstruir la tabla completa
- **Desventaja**: Más complejo, necesitas `unique_key`

**Estrategias incrementales:**
- `append`: Solo hace INSERT (no actualiza registros existentes)
- `merge`: Hace UPSERT (inserta nuevos, actualiza existentes basándose en `unique_key`)
- `delete+insert`: Borra registros que matchean, luego inserta

#### 4. **ephemeral** (Efímero)

```sql
-- models/intermediate/int_order_items.sql
{{ config(materialized='ephemeral') }}

SELECT
    order_id,
    product_id,
    quantity * price AS line_total
FROM {{ ref('stg_order_items') }}
```

- **Qué hace**: NO crea tabla ni vista. El SQL se inserta como CTE en los modelos que lo referencian
- **Cuándo usarlo**: Transformaciones intermedias que solo otro modelo usa
- **Ventaja**: No ocupa espacio, menos objetos en DWH
- **Desventaja**: No puedes queryarlo directamente, puede hacer queries complejos

### Refs y Sources

#### `{{ ref('modelo') }}` - Referencias entre modelos

En vez de escribir:
```sql
SELECT * FROM analytics.stg_customers
```

Escribes:
```sql
SELECT * FROM {{ ref('stg_customers') }}
```

**¿Por qué?**
- dbt sabe que este modelo depende de `stg_customers`
- dbt ejecutará `stg_customers` ANTES que este modelo
- Si cambias el schema de `stg_customers`, dbt actualiza automáticamente la referencia
- El lineage graph muestra la dependencia visualmente

#### `{{ source('schema', 'table') }}` - Datos crudos

Para referenciar tablas crudas (que NO son modelos dbt):

**Definición en schema.yml:**
```yaml
sources:
  - name: raw
    schema: raw_data
    tables:
      - name: customers
      - name: orders
```

**Uso en modelo:**
```sql
SELECT * FROM {{ source('raw', 'customers') }}
```

**Ventaja**: dbt puede testear que la fuente existe antes de ejecutar modelos.

---

## Tests

### ¿Por qué testear datos?

**Datos incorrectos son peores que no tener datos.**

Ejemplos de problemas reales:
- Duplicados en `customer_id` → El dashboard muestra ingresos inflados
- `NULL` en `order_date` → Los reportes mensuales fallan
- `revenue` negativo → El CFO toma decisiones equivocadas

**dbt tests validan automáticamente que tus datos cumplen reglas.**

### Tests Genéricos (Built-in)

dbt incluye 4 tests básicos que puedes aplicar a cualquier columna:

**Definición en `models/schema.yml`:**

```yaml
models:
  - name: dim_customers
    description: "Tabla dimensional de clientes"
    columns:
      - name: customer_id
        description: "Primary key única"
        tests:
          - unique            # ✅ No duplicados
          - not_null          # ✅ No NULLs

      - name: email
        tests:
          - unique

      - name: segment
        tests:
          - accepted_values:  # ✅ Solo valores de esta lista
              values: ['Bronze', 'Silver', 'Gold', 'Platinum']

  - name: fct_orders
    columns:
      - name: customer_id
        tests:
          - relationships:    # ✅ Foreign key válida
              to: ref('dim_customers')
              field: customer_id
```

**Ejecutar tests:**
```bash
dbt test  # Ejecuta todos los tests
dbt test --select dim_customers  # Solo tests de un modelo
```

Si un test falla, dbt devuelve error y muestra qué registros fallaron.

### Tests Personalizados

Para lógica de negocio específica, creas tests custom:

**`tests/assert_positive_revenue.sql`:**
```sql
-- Este test falla si encuentra revenue <= 0
SELECT *
FROM {{ ref('fct_orders') }}
WHERE revenue <= 0
```

**Lógica**: Si el SELECT devuelve filas, el test falla.

**Otro ejemplo:**
```sql
-- Test: Todas las órdenes tienen al menos 1 item
SELECT order_id
FROM {{ ref('fct_orders') }}
WHERE order_id NOT IN (
    SELECT DISTINCT order_id
    FROM {{ ref('fct_order_items') }}
)
```

### Severity de Tests

Por defecto, los tests que fallan causan que `dbt test` retorne error. Puedes cambiar esto:

```yaml
models:
  - name: dim_products
    columns:
      - name: price
        tests:
          - not_null:
              severity: warn  # Solo advertencia, no falla el build
```

**Severities:**
- `error` (default): Falla el build
- `warn`: Muestra advertencia, continúa

---

## Documentación

### Schema.yml - Documentación de Modelos

El archivo `schema.yml` sirve para:
1. Documentar modelos y columnas
2. Definir tests
3. Configurar sources

**Ejemplo completo:**

```yaml
version: 2

models:
  - name: dim_customers
    description: |
      Tabla dimensional de clientes consolidada.

      Esta tabla combina datos de Salesforce y la base transaccional,
      aplicando limpieza y deduplicación.

      **Actualización**: Diaria a las 2 AM UTC
      **Owner**: Equipo Analytics

    columns:
      - name: customer_id
        description: "Surrogate key única del cliente"
        tests:
          - unique
          - not_null

      - name: email
        description: "Email normalizado (lowercase, trimmed)"
        tests:
          - unique
          - not_null

      - name: first_name
        description: "Nombre en formato título (John, no JOHN)"

      - name: segment
        description: |
          Segmento del cliente basado en lifetime value:
          - Bronze: < $1,000
          - Silver: $1,000 - $5,000
          - Gold: $5,000 - $20,000
          - Platinum: > $20,000
        tests:
          - accepted_values:
              values: ['Bronze', 'Silver', 'Gold', 'Platinum']
```

### Generación Automática de Documentación

```bash
dbt docs generate  # Genera la documentación
dbt docs serve     # Abre un servidor web local con la documentación
```

Esto genera un **sitio web interactivo** con:
- 📊 **Lineage Graph**: Diagrama visual de dependencias entre modelos
- 📄 **Catálogo de tablas**: Todas las tablas con sus descripciones
- 📝 **Definiciones de columnas**: Qué significa cada campo
- 🔍 **Búsqueda**: Encuentra rápidamente modelos o columnas
- 📈 **Estadísticas**: Cuántas filas, última ejecución, etc.

**El lineage graph es INCREÍBLE**:
- Ves visualmente cómo fluyen los datos: `raw.customers` → `stg_customers` → `dim_customers` → `fct_orders`
- Click en un modelo para ver su SQL
- Identificas rápidamente qué tablas se romperán si cambias un modelo

---

## Jinja y Macros

### Templating SQL con Jinja

dbt usa **Jinja** (un lenguaje de templating) para hacer tu SQL más dinámico.

**Ejemplo básico - Variables:**

```sql
{% set payment_methods = ['credit_card', 'debit_card', 'bank_transfer'] %}

SELECT
    order_id,
    {% for method in payment_methods %}
    SUM(CASE WHEN payment_method = '{{ method }}' THEN amount ELSE 0 END) AS {{ method }}_amount
    {{ "," if not loop.last }}
    {% endfor %}
FROM {{ ref('stg_payments') }}
GROUP BY 1
```

**Se renderiza como:**
```sql
SELECT
    order_id,
    SUM(CASE WHEN payment_method = 'credit_card' THEN amount ELSE 0 END) AS credit_card_amount,
    SUM(CASE WHEN payment_method = 'debit_card' THEN amount ELSE 0 END) AS debit_card_amount,
    SUM(CASE WHEN payment_method = 'bank_transfer' THEN amount ELSE 0 END) AS bank_transfer_amount
FROM analytics.stg_payments
GROUP BY 1
```

### Macros - Funciones Reutilizables

Un **macro** es una función SQL que puedes reutilizar en múltiples modelos.

**Definición** (`macros/cents_to_dollars.sql`):
```sql
{% macro cents_to_dollars(column_name) %}
    ({{ column_name }} / 100.0)::numeric(10,2)
{% endmacro %}
```

**Uso en modelo:**
```sql
SELECT
    order_id,
    {{ cents_to_dollars('amount_cents') }} AS amount_dollars,
    {{ cents_to_dollars('tax_cents') }} AS tax_dollars
FROM {{ ref('stg_orders') }}
```

**Otro ejemplo útil - Generar surrogate key:**

```sql
{% macro generate_surrogate_key(columns) %}
    MD5(CONCAT(
        {% for col in columns %}
        COALESCE(CAST({{ col }} AS VARCHAR), '')
        {{ "," if not loop.last }}
        {% endfor %}
    ))
{% endmacro %}
```

**Uso:**
```sql
SELECT
    {{ generate_surrogate_key(['customer_id', 'order_date']) }} AS order_key,
    customer_id,
    order_date
FROM {{ ref('stg_orders') }}
```

### Macros de dbt-utils

El paquete `dbt-utils` (oficial) tiene macros súper útiles:

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.0
```

```bash
dbt deps  # Instala los paquetes
```

**Ejemplos:**

```sql
-- Generar surrogate key
SELECT {{ dbt_utils.generate_surrogate_key(['customer_id', 'email']) }} AS customer_key

-- Pivotar columnas
{{ dbt_utils.pivot(
    column='payment_method',
    values=dbt_utils.get_column_values(ref('stg_payments'), 'payment_method'),
    agg='sum',
    then_value='amount'
) }}

-- Union de múltiples modelos
{{ dbt_utils.union_relations(
    relations=[ref('orders_2022'), ref('orders_2023'), ref('orders_2024')]
) }}
```

---

## Incremental Models (Avanzado)

### ¿Cuándo usar modelos incrementales?

**Caso de uso perfecto**: Tienes una tabla de **eventos** que crece constantemente (ej: page views, clicks, logs).

**Problema sin incremental:**
- Cada `dbt run` hace `DROP TABLE` y `CREATE TABLE` con TODOS los datos históricos
- Si tienes 1 billón de filas, esto tarda horas

**Solución con incremental:**
- Primera ejecución: Crea la tabla con todos los datos históricos
- Siguientes ejecuciones: Solo procesa registros nuevos (ej: del último día)

### Implementación

```sql
-- models/fct_page_views.sql
{{ config(
    materialized='incremental',
    unique_key='event_id',
    on_schema_change='fail'
) }}

SELECT
    event_id,
    user_id,
    page_url,
    event_timestamp,
    session_id
FROM {{ ref('stg_events') }}

{% if is_incremental() %}
    -- En runs posteriores, solo procesar datos nuevos
    WHERE event_timestamp > (SELECT MAX(event_timestamp) FROM {{ this }})
{% endif %}
```

**Explicación:**
- `materialized='incremental'`: Activa el modo incremental
- `unique_key='event_id'`: Columna que identifica registros únicos (para UPSERT)
- `is_incremental()`: Función que retorna `True` si la tabla ya existe
- `{{ this }}`: Referencia a la tabla actual (equivale a `analytics.fct_page_views`)

### Estrategias Incrementales

**1. append** (Solo insertar):
```sql
{{ config(
    materialized='incremental',
    incremental_strategy='append'
) }}
```
- Hace `INSERT` de filas nuevas
- NO actualiza registros existentes
- Rápido pero puede causar duplicados si la lógica falla

**2. merge** (UPSERT):
```sql
{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id'
) }}
```
- Si `order_id` ya existe → UPDATE
- Si es nuevo → INSERT
- Más lento pero evita duplicados

**3. delete+insert**:
```sql
{{ config(
    materialized='incremental',
    incremental_strategy='delete+insert',
    unique_key=['date', 'customer_id']
) }}
```
- Borra registros que matchean el `unique_key`
- Inserta todos los registros nuevos

---

## Seeds y Snapshots

### Seeds - Datos Estáticos

**Seeds** son archivos CSV que dbt carga como tablas en tu DWH.

**Caso de uso**: Datos que cambian raramente (ej: códigos de países, categorías de productos, tipos de moneda).

**Archivo** (`seeds/country_codes.csv`):
```csv
country_code,country_name,continent
US,United States,North America
MX,Mexico,North America
BR,Brazil,South America
```

**Carga:**
```bash
dbt seed  # Carga todos los CSVs en seeds/
```

**Uso en modelo:**
```sql
SELECT
    o.order_id,
    o.amount,
    c.country_name,
    c.continent
FROM {{ ref('orders') }} o
LEFT JOIN {{ ref('country_codes') }} c
    ON o.country_code = c.country_code
```

### Snapshots - SCD Type 2 Automático

**Problema**: Tienes una tabla de clientes. El email de un cliente cambió. ¿Cómo guardas el histórico?

**Solución manual**: Implementar SCD Type 2 (lo viste en Tema 1).

**Solución con dbt**: Usar **snapshots**, que implementa SCD Type 2 automáticamente.

**Definición** (`snapshots/customers_snapshot.sql`):
```sql
{% snapshot customers_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at'
    )
}}

SELECT *
FROM {{ source('raw', 'customers') }}

{% endsnapshot %}
```

**Ejecución:**
```bash
dbt snapshot
```

**Resultado**: dbt crea una tabla `snapshots.customers_snapshot` con columnas adicionales:
- `dbt_valid_from`: Cuándo este registro se volvió válido
- `dbt_valid_to`: Cuándo dejó de ser válido (NULL si es actual)
- `dbt_scd_id`: ID único del snapshot
- `dbt_updated_at`: Timestamp del último cambio

**Ejemplo de tabla generada:**

| customer_id | email | updated_at | dbt_valid_from | dbt_valid_to |
|---|---|---|---|---|
| 1 | john@old.com | 2024-01-01 | 2024-01-01 | 2024-06-15 |
| 1 | john@new.com | 2024-06-15 | 2024-06-15 | NULL |

---

## Aplicaciones Prácticas en Data Engineering

### Use Case 1: Pipeline de E-commerce

**Problema**: Tienes ventas crudas en PostgreSQL. Necesitas crear reportes de ingresos por producto, región y mes.

**Solución con dbt:**

```
raw.orders
raw.order_items
raw.products
raw.customers
    ↓
[dbt transforma]
    ↓
analytics.dim_products
analytics.dim_customers
analytics.fct_order_items
    ↓
[BI Tool consume]
```

**Ventajas:**
- Los analistas pueden modificar las transformaciones (saben SQL)
- Tests automáticos validan que no hay productos sin categoría
- Documentación muestra qué significa cada métrica
- Si cambias la lógica de `dim_products`, sabes qué reportes se afectan (lineage)

### Use Case 2: Agregaciones Diarias

**Problema**: Tienes millones de eventos de clickstream. Necesitas reportes diarios de tráfico.

**Solución con modelo incremental:**

```sql
-- models/daily_page_views.sql
{{ config(materialized='incremental', unique_key=['date', 'page_url']) }}

SELECT
    DATE(event_timestamp) AS date,
    page_url,
    COUNT(*) AS page_views,
    COUNT(DISTINCT user_id) AS unique_visitors
FROM {{ ref('stg_events') }}

{% if is_incremental() %}
WHERE DATE(event_timestamp) = CURRENT_DATE - INTERVAL '1 day'
{% endif %}

GROUP BY 1, 2
```

**Ventaja**: Solo procesas el día de ayer, no todos los históricos.

### Use Case 3: Consolidación de Fuentes

**Problema**: Tienes clientes en Salesforce y en tu base transaccional. Necesitas una única fuente de verdad.

**Solución:**

```sql
-- models/dim_customers.sql
WITH salesforce_customers AS (
    SELECT
        sf_id AS customer_id,
        email,
        'salesforce' AS source
    FROM {{ source('raw', 'sf_accounts') }}
),

transactional_customers AS (
    SELECT
        customer_id,
        email,
        'transactional' AS source
    FROM {{ source('raw', 'app_users') }}
),

unioned AS (
    SELECT * FROM salesforce_customers
    UNION ALL
    SELECT * FROM transactional_customers
),

deduplicated AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY email ORDER BY source) AS rn
    FROM unioned
)

SELECT
    customer_id,
    email,
    source AS primary_source
FROM deduplicated
WHERE rn = 1
```

---

## Cloud Data Warehouses: Snowflake vs Redshift vs BigQuery

### ¿Por qué elegir un Cloud DWH?

dbt funciona con cualquier Data Warehouse que soporte SQL. Sin embargo, los tres grandes dominan el mercado empresarial:

**Analogía**: Piensa en los cloud DWH como diferentes marcas de coches deportivos:
- **Snowflake** = Tesla → Innovador, moderno, separación de cómputo y almacenamiento
- **Redshift** = BMW → Integrado con ecosistema AWS, sólido y probado
- **BigQuery** = Mercedes → Serverless total, escalabilidad automática, integrado con Google

### Comparativa Técnica

| Característica | Snowflake | Redshift | BigQuery |
|---|---|---|---|
| **Modelo de precio** | Por segundos de uso | Por hora de cluster | Por TB procesado |
| **Escalado** | Automático (compute separado) | Manual (resize cluster) | Automático (serverless) |
| **Almacenamiento** | Separado de cómputo | Junto con cómputo | Separado (serverless) |
| **Multi-cloud** | ✅ AWS, Azure, GCP | ❌ Solo AWS | ❌ Solo GCP |
| **Data Sharing** | ✅ Nativo (Zero Copy) | ❌ Requiere ETL | ⚠️ Analytics Hub |
| **Formato nativo** | Propio (columnar) | Columnar (Redshift) | Columnar (Capacitor) |
| **dbt Support** | ✅ Excelente | ✅ Excelente | ✅ Excelente |

### ¿Cuándo usar cada uno?

**Snowflake - Ideal para:**
- Empresas multi-cloud o que quieren evitar vendor lock-in
- Cargas de trabajo variables (picos de demanda)
- Data sharing entre organizaciones
- Equipos que necesitan cómputo separado del storage

```sql
-- En dbt, conectarse a Snowflake
-- profiles.yml
snowflake:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xy12345.us-east-1
      user: dbt_user
      warehouse: TRANSFORM_WH
      database: ANALYTICS
      schema: dbt_dev
```

**Redshift - Ideal para:**
- Empresas 100% en AWS
- Cargas de trabajo predecibles (precio fijo)
- Integración con otros servicios AWS (S3, Glue, SageMaker)
- Equipos que ya conocen PostgreSQL (sintaxis similar)

```sql
-- En dbt, conectarse a Redshift
-- profiles.yml
redshift:
  target: dev
  outputs:
    dev:
      type: redshift
      host: my-cluster.abc123.us-east-1.redshift.amazonaws.com
      user: dbt_user
      port: 5439
      dbname: analytics
      schema: dbt_dev
```

**BigQuery - Ideal para:**
- Empresas en GCP o con muchos datos de Google (Analytics, Ads)
- Cargas de trabajo impredecibles (paga por query)
- Equipos pequeños sin tiempo para gestionar infraestructura
- Análisis de datos semi-estructurados (JSON, arrays)

```sql
-- En dbt, conectarse a BigQuery
-- profiles.yml
bigquery:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: my-gcp-project
      dataset: dbt_dev
      location: US
```

### Consideraciones de Costo

| Escenario | Snowflake | Redshift | BigQuery |
|---|---|---|---|
| Pocos queries, mucho storage | 💰 Económico | 💸 Caro (cluster fijo) | 💰 Económico |
| Muchos queries pequeños | ⚠️ Depende | 💰 Económico (cluster fijo) | 💸 Puede ser caro |
| Queries esporádicos grandes | 💰 Económico (escala bajo demanda) | 💸 Cluster subutilizado | 💰 Económico (serverless) |
| 24/7 producción constante | ⚠️ Depende del warehouse size | 💰 Reserved instances | ⚠️ Depende del volumen |

**Consejo práctico**: Comienza con el DWH de tu proveedor cloud principal. Si estás en AWS, prueba Redshift. Si estás en GCP, BigQuery. Si necesitas flexibilidad o multi-cloud, Snowflake.

---

## Errores Comunes

### Error 1: Referencias Circulares

**Problema:**
- `modelo_a` hace `{{ ref('modelo_b') }}`
- `modelo_b` hace `{{ ref('modelo_a') }}`

**Síntoma**: `dbt run` falla con "Circular dependency detected"

**Solución**: Rediseña tus modelos para que el flujo sea unidireccional (A → B → C, nunca C → A).

### Error 2: Olvidar `is_incremental()`

**Problema:**
```sql
{{ config(materialized='incremental') }}

SELECT * FROM {{ ref('stg_events') }}
WHERE event_date > (SELECT MAX(event_date) FROM {{ this }})
```

**Error**: En la primera ejecución, la tabla no existe, entonces `{{ this }}` falla.

**Solución**: Siempre usa `is_incremental()`:
```sql
{% if is_incremental() %}
WHERE event_date > (SELECT MAX(event_date) FROM {{ this }})
{% endif %}
```

### Error 3: No testear sources

**Problema**: Tu modelo asume que `raw.customers` tiene columna `email`, pero un día un dev la renombra.

**Solución**: Testea tus sources:
```yaml
sources:
  - name: raw
    tables:
      - name: customers
        columns:
          - name: email
            tests:
              - not_null
```

### Error 4: Macros sin documentación

**Problema**: Creas un macro complejo, nadie sabe cómo usarlo.

**Solución**: Documenta tus macros:
```sql
{% macro generate_surrogate_key(columns) %}
{#
    Genera una surrogate key usando MD5 de múltiples columnas.

    Args:
        columns (list): Lista de nombres de columnas para incluir en el hash.

    Returns:
        String MD5 hash de las columnas concatenadas.

    Example:
        {{ generate_surrogate_key(['customer_id', 'order_date']) }}
#}
    MD5(CONCAT(
        {% for col in columns %}
        COALESCE(CAST({{ col }} AS VARCHAR), '')
        {{ "," if not loop.last }}
        {% endfor %}
    ))
{% endmacro %}
```

---

## Checklist de Aprendizaje

Antes de continuar al siguiente tema, asegúrate de que puedes:

### Conceptos Básicos
- [ ] Explicar qué es dbt y por qué existe
- [ ] Diferenciar entre ETL y ELT
- [ ] Conocer la diferencia entre dbt Core y dbt Cloud
- [ ] Describir la estructura de un proyecto dbt

### Models
- [ ] Crear un modelo básico (archivo `.sql` con SELECT)
- [ ] Entender los 4 tipos de materialización (view, table, incremental, ephemeral)
- [ ] Usar `{{ ref('modelo') }}` para referenciar otros modelos
- [ ] Definir y usar `{{ source('schema', 'table') }}`

### Tests
- [ ] Aplicar los 4 tests genéricos (unique, not_null, accepted_values, relationships)
- [ ] Crear un test personalizado
- [ ] Ejecutar `dbt test` y entender los resultados

### Documentación
- [ ] Escribir documentación en `schema.yml`
- [ ] Generar y explorar `dbt docs`
- [ ] Interpretar el lineage graph

### Jinja y Macros
- [ ] Usar variables y loops de Jinja en SQL
- [ ] Crear un macro simple
- [ ] Reutilizar un macro en múltiples modelos

### Avanzado
- [ ] Implementar un modelo incremental básico
- [ ] Usar `is_incremental()` correctamente
- [ ] Cargar un seed CSV
- [ ] Crear un snapshot para SCD Type 2

### Buenas Prácticas
- [ ] Organizar modelos en carpetas (staging, intermediate, marts)
- [ ] Nombrar modelos consistentemente (`stg_`, `int_`, `dim_`, `fct_`)
- [ ] Testear todas las primary keys y foreign keys
- [ ] Documentar modelos y columnas importantes

---

**¡Felicidades!** Ahora entiendes los fundamentos de dbt. En la siguiente sección veremos ejemplos prácticos ejecutables.

**Próximo paso**: [`02-EJEMPLOS.md`](./02-EJEMPLOS.md) - Ejemplos progresivos de dbt desde básico hasta avanzado.
