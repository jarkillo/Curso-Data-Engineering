# Proyecto Práctico: Pipeline dbt Completo - FinTech Analytics

Pipeline de transformación ELT completo usando **dbt (data build tool)** para **FinTech Analytics**, empresa ficticia del sector fintech. Como Data Engineer en **DataFlow Industries**, implementarás este Data Warehouse para tu cliente. Este proyecto demuestra todas las capacidades de dbt: staging, dimensiones, hechos, tests, macros, snapshots y documentación.

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, aprenderás a:

- ✅ Configurar un proyecto dbt desde cero
- ✅ Cargar datos desde seeds (CSV)
- ✅ Crear modelos de staging (limpieza inicial)
- ✅ Diseñar modelos dimensionales (star schema)
- ✅ Implementar tests de calidad de datos
- ✅ Crear macros reutilizables con Jinja
- ✅ Implementar snapshots (SCD Type 2)
- ✅ Generar documentación automática
- ✅ Ejecutar un pipeline completo de transformación

---

## 📚 Conceptos Clave

### ¿Qué es dbt?

**dbt (data build tool)** es una herramienta de transformación moderna que permite:

- Escribir transformaciones en **SQL puro**
- Aplicar **ingeniería de software** a analytics (versionado, tests, docs)
- Ejecutar transformaciones en el **warehouse** (ELT, no ETL)
- Mantener **dependencias automáticas** entre modelos

**Analogía**: Si SQL es como escribir código suelto en archivos `.txt`, dbt es como tener un IDE completo con tests, documentación, control de versiones y ejecución automática.

### Filosofía ELT vs ETL

**ETL tradicional** (Extract-Transform-Load):
1. **Extract**: Obtener datos de fuentes
2. **Transform**: Transformar en servidor intermedio
3. **Load**: Cargar en warehouse

**ELT moderno** (Extract-Load-Transform):
1. **Extract**: Obtener datos de fuentes
2. **Load**: Cargar RAW en warehouse
3. **Transform**: Transformar DENTRO del warehouse (aquí entra dbt)

**Ventaja de ELT**: Aprovecha el poder de cómputo del warehouse moderno (Snowflake, BigQuery, Redshift, etc.) en lugar de un servidor ETL limitado.

---

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── dbt_project.yml           # Configuración del proyecto dbt
├── profiles.yml              # Configuración de conexión (ejemplo)
├── packages.yml              # Dependencias (dbt-utils)
├── requirements.txt          # Dependencias Python
│
├── models/                   # Modelos de transformación
│   ├── staging/              # Capa 1: Limpieza y estandarización
│   │   ├── stg_customers.sql
│   │   ├── stg_products.sql
│   │   ├── stg_orders.sql
│   │   └── schema.yml        # Tests y docs de staging
│   │
│   ├── intermediate/         # Capa 2: Transformaciones intermedias
│   │   ├── int_orders_enriched.sql
│   │   └── schema.yml        # Tests y docs de intermediate
│   │
│   └── marts/                # Capa 3: Modelos analíticos
│       ├── dimensions/       # Tablas dimensionales
│       │   ├── dim_customers.sql
│       │   └── dim_products.sql
│       │
│       ├── facts/            # Tablas de hechos
│       │   ├── fct_orders.sql
│       │   └── fct_daily_revenue.sql
│       │
│       └── schema.yml        # Tests y docs de marts
│
├── macros/                   # Funciones SQL reutilizables
│   └── custom_macros.sql     # Macros personalizados
│
├── seeds/                    # Datos CSV de entrada
│   ├── raw_customers.csv
│   ├── raw_products.csv
│   └── raw_orders.csv
│
├── snapshots/                # SCD Type 2
│   ├── products_snapshot.sql
│   └── customers_snapshot.sql
│
├── tests/                    # Tests personalizados
│   ├── assert_positive_order_amounts.sql
│   ├── assert_order_total_matches_calculation.sql
│   ├── assert_shipped_orders_have_shipped_date.sql
│   └── assert_lifetime_value_consistency.sql
│
├── ejemplos/
│   └── example_usage.py      # Script de demostración
│
└── README.md                 # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.8+**
- **PostgreSQL 13+** o **DuckDB** (más simple para desarrollo)
- **Git**

### Paso 1: Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows)
.\venv\Scripts\Activate.ps1
```

### Paso 2: Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 3: Configurar conexión a base de datos

**Opción A: DuckDB (recomendado para práctica)**

Crear archivo `~/.dbt/profiles.yml`:

```yaml
fintech_analytics:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: fintech.duckdb
      threads: 4
```

**Opción B: PostgreSQL**

```yaml
fintech_analytics:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: dataeng_user
      password: "{{ env_var('DBT_PASSWORD') }}"
      dbname: fintech_dw
      schema: dbt_dev
      threads: 4
```

Configurar variable de entorno:

```bash
# Linux/Mac
export DBT_PASSWORD='tu_password'

# Windows
$env:DBT_PASSWORD='tu_password'
```

### Paso 4: Verificar instalación

```bash
# Verificar versión de dbt
dbt --version

# Verificar conexión
dbt debug
```

---

## ✅ Ejecución del Pipeline

### Flujo Completo (Recomendado)

```bash
# 1. Instalar paquetes de dbt (dbt-utils)
dbt deps

# 2. Cargar seeds (CSV → Tablas)
dbt seed

# 3. Ejecutar modelos (staging + marts)
dbt run

# 4. Ejecutar tests de calidad
dbt test

# 5. Generar documentación
dbt docs generate

# 6. Servir documentación (abre navegador)
dbt docs serve

# 7. Crear snapshots (SCD Type 2)
dbt snapshot
```

### Comandos Útiles

```bash
# Ejecutar solo staging
dbt run --select staging

# Ejecutar solo marts
dbt run --select marts

# Ejecutar modelo específico y sus dependencias
dbt run --select +dim_customers

# Ejecutar modelo específico y sus descendientes
dbt run --select dim_customers+

# Ejecutar tests de un modelo específico
dbt test --select dim_customers

# Compilar modelos sin ejecutar
dbt compile

# Limpiar archivos generados
dbt clean

# Refrescar snapshot específico
dbt snapshot --select products_snapshot

# Ejecutar en modo full-refresh (reconstruir todo)
dbt run --full-refresh
```

---

## 📦 Modelos Implementados

### Capa Staging (Vistas)

#### `stg_customers`

Limpieza y estandarización de clientes.

**Transformaciones**:
- Email → lowercase, trimmed
- Nombres → formato título
- Teléfono → solo dígitos
- País → uppercase

**Ejemplo de uso**:
```sql
SELECT * FROM dbt_dev.stg_customers
WHERE country = 'ES'
LIMIT 5;
```

#### `stg_products`

Catálogo de productos deduplicado.

**Transformaciones**:
- Deduplicación por `updated_at` (versión más reciente)
- SKU → uppercase
- Precio → NUMERIC(10,2)
- Categoría → lowercase

**Ejemplo de uso**:
```sql
SELECT product_id, name, price, category
FROM dbt_dev.stg_products
WHERE category = 'electronics'
ORDER BY price DESC;
```

#### `stg_orders`

Pedidos con métricas calculadas.

**Transformaciones**:
- Cálculo de `days_to_ship`
- Flags: `is_shipped`, `is_delivered`, `is_cancelled`
- Validación: quantity > 0, total_amount > 0

**Ejemplo de uso**:
```sql
SELECT order_id, customer_id, total_amount, days_to_ship
FROM dbt_dev.stg_orders
WHERE is_delivered
  AND days_to_ship <= 2;  -- Envíos rápidos
```

### Capa Marts (Tablas)

#### `dim_customers` (Dimensión)

Clientes con segmentación RFM.

**Segmentación**:
- **Bronze**: Lifetime value < $100
- **Silver**: $100 - $499
- **Gold**: $500 - $999
- **Platinum**: >= $1,000

**Purchase Frequency**:
- Low (1 pedido), Medium (2-4), High (5-9), Very High (10+)

**Customer Status**:
- Active (última compra < 30 días)
- At Risk (30-90 días)
- Inactive (> 90 días)

**Ejemplo de uso**:
```sql
-- Clientes Platinum activos
SELECT
    full_name,
    lifetime_value,
    total_orders,
    days_since_last_order
FROM dbt_dev.dim_customers
WHERE customer_segment = 'Platinum'
  AND customer_status = 'Active';
```

#### `dim_products` (Dimensión)

Productos con clasificación por ventas.

**Popularity Tier**:
- No Sales, Normal (1), Popular (2-4), Best Seller (5+)

**Revenue Tier**:
- No Revenue, Low (<$500), Medium ($500-$1,999), High ($2,000+)

**Ejemplo de uso**:
```sql
-- Top 5 productos por ingresos
SELECT
    name,
    category,
    total_revenue,
    total_units_sold,
    popularity_tier
FROM dbt_dev.dim_products
WHERE has_sales
ORDER BY total_revenue DESC
LIMIT 5;
```

#### `fct_orders` (Hecho)

Pedidos con dimensiones desnormalizadas.

**Métricas adicionales**:
- Diferencia de precio vs precio actual
- Dimensiones de tiempo (año, mes, trimestre, semana)
- Flags: `is_high_value_order`, `is_fast_shipping`

**Ejemplo de uso**:
```sql
-- Revenue mensual por categoría
SELECT
    order_year,
    order_month,
    product_category,
    SUM(total_amount) AS monthly_revenue,
    COUNT(*) AS num_orders
FROM dbt_dev.fct_orders
WHERE NOT is_cancelled
GROUP BY 1, 2, 3
ORDER BY 1, 2, 4 DESC;
```

#### `fct_daily_revenue` (Análisis)

Ingresos diarios con pivote de métodos de pago y categorías.

**Demuestra**: Uso de macros `pivot_payment_methods()` y `pivot_categories()`

**Ejemplo de uso**:
```sql
SELECT
    order_date,
    total_revenue,
    credit_card_revenue,
    paypal_revenue,
    electronics_revenue,
    accessories_revenue
FROM dbt_dev.fct_daily_revenue
ORDER BY order_date DESC
LIMIT 7;  -- Última semana
```

---

## 🧪 Tests Implementados

### Tests Genéricos (schema.yml)

- **unique**: `customer_id`, `product_id`, `order_id`, `email`, `sku`
- **not_null**: Todos los IDs, emails, nombres
- **accepted_values**: Categorías, métodos de pago, estados, segmentos
- **relationships**: Foreign keys (customer_id, product_id)
- **dbt_utils.expression_is_true**: Valores positivos, rangos válidos

**Total**: ~40 tests genéricos

### Tests Personalizados (tests/)

1. **assert_positive_order_amounts.sql**: Todos los montos > 0
2. **assert_order_total_matches_calculation.sql**: total_amount = quantity × unit_price
3. **assert_shipped_orders_have_shipped_date.sql**: Estado vs fecha consistente
4. **assert_lifetime_value_consistency.sql**: lifetime_value y total_orders coherentes

**Ejecutar tests**:
```bash
# Todos los tests
dbt test

# Solo tests genéricos
dbt test --exclude test_type:singular

# Solo tests personalizados
dbt test --select test_type:singular
```

---

## 🔧 Macros Implementadas

### `cents_to_dollars(column_name, precision=2)`

Convierte centavos a dólares.

```sql
SELECT
    product_id,
    {{ cents_to_dollars('price_in_cents', 2) }} AS price_dollars
FROM products;
```

### `pivot_payment_methods()`

Pivotea métodos de pago en columnas.

```sql
SELECT
    order_date,
    {{ pivot_payment_methods() }}
FROM orders
GROUP BY order_date;

-- Resultado:
-- order_date | credit_card_revenue | credit_card_count | paypal_revenue | ...
```

### `pivot_categories()`

Pivotea categorías de productos.

### `age_in_years(date_column)`

Calcula edad en años desde una fecha.

### `generate_surrogate_key(columns)`

Genera hash MD5 para claves surrogate.

**Ver todas las macros**: `macros/custom_macros.sql`

---

## 📸 Snapshots (SCD Type 2)

### `products_snapshot`

Rastrea cambios históricos en productos (especialmente precios).

**Cómo funciona**:

1. **Primera ejecución**: Crea tabla con todas las versiones actuales
2. **Ejecuciones posteriores**: Detecta cambios en `updated_at`
   - Cierra versión anterior (`dbt_valid_to = NOW()`)
   - Inserta nueva versión (`dbt_valid_from = NOW()`)

**Columnas automáticas**:
- `dbt_scd_id`: ID único de versión
- `dbt_valid_from`: Inicio de vigencia
- `dbt_valid_to`: Fin de vigencia (NULL = actual)
- `dbt_updated_at`: Timestamp de actualización

**Ejecutar**:
```bash
dbt snapshot
```

**Consultar historial de precios**:
```sql
-- Precio actual del producto 1
SELECT price
FROM snapshots.products_snapshot
WHERE product_id = 1
  AND dbt_valid_to IS NULL;

-- Historial completo de precios
SELECT
    product_id,
    name,
    price,
    dbt_valid_from,
    dbt_valid_to
FROM snapshots.products_snapshot
WHERE product_id = 1
ORDER BY dbt_valid_from;

-- Precio en fecha específica (2024-03-10)
SELECT price
FROM snapshots.products_snapshot
WHERE product_id = 1
  AND '2024-03-10' BETWEEN dbt_valid_from
  AND COALESCE(dbt_valid_to, '9999-12-31');
```

---

## 📊 Análisis de Ejemplo

### 1. Análisis RFM de Clientes

```sql
SELECT
    customer_segment,
    customer_status,
    COUNT(*) AS num_customers,
    AVG(lifetime_value) AS avg_ltv,
    AVG(total_orders) AS avg_orders,
    AVG(days_since_last_order) AS avg_recency
FROM dbt_dev.dim_customers
GROUP BY 1, 2
ORDER BY 1, 2;
```

### 2. Revenue por Categoría y Mes

```sql
SELECT
    order_year,
    order_month,
    product_category,
    SUM(total_amount) AS revenue,
    COUNT(DISTINCT customer_id) AS unique_customers,
    AVG(total_amount) AS avg_order_value
FROM dbt_dev.fct_orders
WHERE NOT is_cancelled
GROUP BY 1, 2, 3
ORDER BY 1, 2, 4 DESC;
```

### 3. Productos con Bajo Stock pero Alta Demanda

```sql
SELECT
    p.name,
    p.category,
    p.current_stock,
    p.total_units_sold,
    p.popularity_tier,
    p.is_low_stock
FROM dbt_dev.dim_products p
WHERE p.is_low_stock
  AND p.popularity_tier IN ('Popular', 'Best Seller')
ORDER BY p.total_units_sold DESC;
```

### 4. Cohort Analysis (Clientes por mes de primera compra)

```sql
SELECT
    DATE_TRUNC('month', first_order_date) AS cohort_month,
    COUNT(*) AS cohort_size,
    AVG(lifetime_value) AS avg_ltv,
    SUM(CASE WHEN customer_status = 'Active' THEN 1 ELSE 0 END) AS active_count,
    ROUND(
        100.0 * SUM(CASE WHEN customer_status = 'Active' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS retention_rate
FROM dbt_dev.dim_customers
WHERE first_order_date IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

---

## 🐛 Troubleshooting

### Error: "Compilation Error in model X (models/...)"

**Causa**: Error de sintaxis SQL o Jinja

**Solución**:
```bash
# Compilar sin ejecutar para ver el SQL generado
dbt compile --select nombre_modelo

# Revisar archivo compilado en target/compiled/fintech_analytics/models/...
```

### Error: "Database Error in model X"

**Causa**: Error en ejecución SQL (columna no existe, tipo incorrecto, etc.)

**Solución**:
1. Ver logs detallados: `logs/dbt.log`
2. Ejecutar con más verbosidad: `dbt run --debug`
3. Probar SQL compilado manualmente en la DB

### Tests fallan pero deberían pasar

**Causa**: Datos de seeds cambiaron

**Solución**:
```bash
# Recargar seeds
dbt seed --full-refresh

# Re-ejecutar modelos
dbt run

# Re-ejecutar tests
dbt test
```

### "Relation not found" al ejecutar tests

**Causa**: Modelos no se han ejecutado aún

**Solución**:
```bash
# Ejecutar modelos primero
dbt run

# Luego tests
dbt test
```

### Snapshot no detecta cambios

**Causa**: Columna `updated_at` no cambió

**Solución**:
1. Verificar que `updated_at` se actualiza en seeds
2. Recargar seeds: `dbt seed --full-refresh`
3. Re-ejecutar snapshot: `dbt snapshot`

---

## 📚 Recursos Adicionales

### Archivos de Teoría

- [01-TEORIA.md](../01-TEORIA.md) - Conceptos fundamentales de dbt
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - 5 ejemplos prácticos progresivos
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - 15 ejercicios con soluciones

### Documentación Oficial

- [dbt Docs](https://docs.getdbt.com/)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [dbt-utils Package](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)

### Comandos de Referencia

```bash
# Ver comandos disponibles
dbt --help

# Ver opciones de un comando
dbt run --help

# Compilar proyecto
dbt compile

# Ejecutar modelos
dbt run

# Ejecutar tests
dbt test

# Cargar seeds
dbt seed

# Crear snapshots
dbt snapshot

# Generar docs
dbt docs generate

# Servir docs
dbt docs serve

# Limpiar archivos generados
dbt clean

# Listar modelos
dbt list

# Mostrar SQL compilado
dbt show --inline "SELECT * FROM {{ ref('dim_customers') }} LIMIT 5"
```

---

## 🎓 Próximos Pasos

Después de completar este proyecto, puedes:

1. **Extender el modelo de datos**:
   - Agregar más dimensiones (tiempo, geografía)
   - Crear más hechos (devoluciones, inventario)
   - Implementar modelos incrementales

2. **Mejorar la calidad**:
   - Agregar más tests personalizados
   - Usar `dbt-expectations` para tests avanzados
   - Configurar alertas de calidad de datos

3. **Optimizar rendimiento**:
   - Usar materializaciones incrementales
   - Particionar tablas grandes
   - Optimizar queries costosos

4. **Integrar con herramientas**:
   - Conectar con BI (Tableau, Power BI, Looker)
   - Orquestar con Airflow
   - Implementar CI/CD con GitHub Actions

5. **Explorar funcionalidades avanzadas**:
   - Exposures (dashboards, reportes)
   - Metrics (métricas de negocio reutilizables)
   - dbt Cloud (plataforma SaaS)

---

## ✅ Verificación de Completitud

- [x] Configuración de proyecto (dbt_project.yml, profiles.yml)
- [x] Seeds con datos realistas (customers, products, orders)
- [x] Modelos de staging con limpieza (3 modelos)
- [x] Modelos intermediate para transformaciones (1 modelo)
- [x] Dimensiones con métricas agregadas (2 dimensiones)
- [x] Hechos con análisis (2 hechos)
- [x] Tests genéricos en schema.yml (~45 tests)
- [x] Tests personalizados (4 tests custom)
- [x] Macros reutilizables (10 macros)
- [x] Snapshots para SCD Type 2 (2 snapshots)
- [x] Documentación completa (schema.yml + README)
- [x] Ejemplo de uso (example_usage.py)
- [x] 3 capas de transformación: staging → intermediate → marts

---

**Proyecto desarrollado para el Máster en Ingeniería de Datos con IA**

**Módulo 8**: Data Warehousing
**Tema 2**: Herramientas DWH (dbt)

---

¿Dudas? Revisa [01-TEORIA.md](../01-TEORIA.md) o ejecuta `dbt docs serve` para explorar la documentación interactiva.
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Analytics y BI - 01 Teoria](../../tema-3-analytics-bi/01-TEORIA.md)
