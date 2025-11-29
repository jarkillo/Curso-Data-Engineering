# Ejemplos Prácticos: Analytics y Business Intelligence

En este documento trabajaremos 4 ejemplos progresivos que te mostrarán cómo aplicar los conceptos de Analytics y BI en situaciones reales.

---

## Ejemplo 1: Definir KPIs para E-commerce - Nivel: Básico

### Contexto

**RestaurantData Co.** ha decidido expandirse al delivery online. El CEO te pide que definas los KPIs principales para medir el éxito de esta nueva línea de negocio.

Tienes acceso a los siguientes datos en tu Data Warehouse:

```sql
-- Tabla de pedidos
CREATE TABLE fact_orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    delivery_fee DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    status VARCHAR(20),  -- 'completed', 'cancelled', 'refunded'
    delivery_time_minutes INT,
    channel VARCHAR(20)  -- 'web', 'app', 'phone'
);

-- Tabla de clientes
CREATE TABLE dim_customers (
    customer_id INT,
    first_order_date DATE,
    customer_segment VARCHAR(20),  -- 'new', 'returning', 'vip'
    acquisition_channel VARCHAR(20)
);

-- Tabla de productos
CREATE TABLE dim_products (
    product_id INT,
    product_name VARCHAR(100),
    category VARCHAR(50),
    cost DECIMAL(10,2),
    price DECIMAL(10,2)
);
```

### Paso 1: Identificar Objetivos de Negocio

Antes de definir KPIs, debemos entender qué quiere lograr el negocio:

| Objetivo de Negocio | Pregunta Clave |
|---------------------|----------------|
| Crecimiento | ¿Estamos vendiendo más? |
| Rentabilidad | ¿Estamos ganando dinero? |
| Satisfacción | ¿Los clientes están contentos? |
| Eficiencia | ¿Operamos bien? |

### Paso 2: Definir KPIs por Objetivo

**Objetivo 1: Crecimiento**

| KPI | Fórmula | Objetivo | Frecuencia |
|-----|---------|----------|------------|
| Revenue Total | `SUM(total_amount) WHERE status = 'completed'` | +20% MoM | Diario |
| Número de Pedidos | `COUNT(DISTINCT order_id) WHERE status = 'completed'` | +15% MoM | Diario |
| Nuevos Clientes | `COUNT(DISTINCT customer_id) WHERE first_order_date = current_month` | +500/mes | Semanal |

**Objetivo 2: Rentabilidad**

| KPI | Fórmula | Objetivo | Frecuencia |
|-----|---------|----------|------------|
| Ticket Promedio (AOV) | `Revenue / Número de Pedidos` | >$45 | Diario |
| Margen Bruto | `(Revenue - Costo) / Revenue * 100` | >35% | Semanal |
| CAC | `Gasto Marketing / Nuevos Clientes` | <$25 | Mensual |

**Objetivo 3: Satisfacción**

| KPI | Fórmula | Objetivo | Frecuencia |
|-----|---------|----------|------------|
| Tiempo de Entrega Promedio | `AVG(delivery_time_minutes)` | <40 min | Diario |
| Tasa de Cancelación | `Pedidos Cancelados / Total Pedidos * 100` | <5% | Diario |
| Tasa de Recompra | `Clientes con >1 pedido / Total Clientes * 100` | >30% | Mensual |

### Paso 3: Implementar en SQL

```sql
-- KPIs de Crecimiento - Resumen Diario
SELECT
    order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount) AS revenue,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(total_amount) / NULLIF(COUNT(DISTINCT order_id), 0) AS avg_order_value
FROM fact_orders
WHERE status = 'completed'
  AND order_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY order_date
ORDER BY order_date;

-- Resultado esperado:
-- order_date  | total_orders | revenue    | unique_customers | avg_order_value
-- 2024-03-01  | 145          | 7,250.50   | 132              | 50.00
-- 2024-03-02  | 168          | 8,568.00   | 155              | 51.00
-- ...
```

```sql
-- KPI de Satisfacción - Tiempo de Entrega
SELECT
    order_date,
    AVG(delivery_time_minutes) AS avg_delivery_time,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY delivery_time_minutes) AS median_delivery,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY delivery_time_minutes) AS p95_delivery,
    COUNT(*) FILTER (WHERE delivery_time_minutes > 45) * 100.0 / COUNT(*) AS pct_late_deliveries
FROM fact_orders
WHERE status = 'completed'
  AND order_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY order_date
ORDER BY order_date;

-- Resultado esperado:
-- order_date  | avg_delivery_time | median_delivery | p95_delivery | pct_late_deliveries
-- 2024-03-08  | 32.5              | 30              | 52           | 12.3%
-- 2024-03-09  | 35.2              | 33              | 58           | 15.1%
```

### Paso 4: Definir Umbrales de Alerta

```python
# Configuración de alertas para el dashboard
kpi_thresholds = {
    "avg_order_value": {
        "green": {"min": 45, "max": None},
        "yellow": {"min": 35, "max": 45},
        "red": {"min": None, "max": 35}
    },
    "avg_delivery_time": {
        "green": {"min": None, "max": 35},
        "yellow": {"min": 35, "max": 45},
        "red": {"min": 45, "max": None}
    },
    "cancellation_rate": {
        "green": {"min": None, "max": 3},
        "yellow": {"min": 3, "max": 5},
        "red": {"min": 5, "max": None}
    }
}
```

### Interpretación

Con estos KPIs definidos, RestaurantData Co. puede:

1. **Monitorear crecimiento diario** con revenue y pedidos
2. **Alertar cuando hay problemas** con umbrales claros
3. **Investigar causas raíz** usando dimensiones (canal, categoría, zona)
4. **Tomar acciones** basadas en datos concretos

---

## Ejemplo 2: Diseñar Dashboard Ejecutivo - Nivel: Intermedio

### Contexto

El CFO de **FinTech Analytics** necesita un dashboard ejecutivo para la reunión semanal del board. Quiere ver el estado general del negocio en una sola pantalla.

### Paso 1: Entender la Audiencia

| Aspecto | Detalle |
|---------|---------|
| Usuario | CFO y board de directores |
| Frecuencia de uso | Semanal (reunión de lunes) |
| Tiempo disponible | 10 minutos máximo |
| Nivel técnico | Bajo - necesitan claridad |
| Decisiones que toman | Estratégicas: inversión, hiring, prioridades |

### Paso 2: Seleccionar KPIs (Regla del 5)

Solo 5 KPIs máximo para nivel ejecutivo:

1. **MRR (Monthly Recurring Revenue)**: Salud financiera
2. **Net Revenue Retention (NRR)**: Crecimiento de clientes existentes
3. **CAC Payback Period**: Eficiencia de adquisición
4. **Gross Margin**: Rentabilidad operativa
5. **Runway**: Meses de operación restantes

### Paso 3: Diseñar el Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FINTECH ANALYTICS - EXECUTIVE DASHBOARD           Semana del 11 Mar   │
│  Última actualización: Hoy 09:00 AM                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│  │ 💰 MRR      │ │ 📈 NRR      │ │ ⏱️ CAC      │ │ 📊 Margen   │        │
│  │             │ │             │ │ Payback     │ │ Bruto       │        │
│  │  $2.4M      │ │   112%      │ │  8 meses    │ │   72%       │        │
│  │  ↑ 8% MoM   │ │   ↑ 3pp     │ │   ↓ 2 meses │ │   → 0pp     │        │
│  │  🟢 On Track│ │  🟢 Strong  │ │  🟡 Atención│ │  🟢 Healthy │        │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘        │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   MRR TREND - ÚLTIMOS 12 MESES                    RUNWAY: 18 meses     │
│   $3M ┤                                   ╭──     ████████████████████░░│
│       │                              ╭────╯                              │
│   $2M ┤                    ╭─────────╯                                   │
│       │         ╭──────────╯                    Cash: $8.2M             │
│   $1M ┤  ╭──────╯                               Burn: $456K/mes         │
│       │──╯                                                               │
│    $0 ┼──────────────────────────────────                               │
│        Mar  May  Jul  Sep  Nov  Jan  Mar                                │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ⚠️ ALERTAS ACTIVAS                          📋 NOTAS DE LA SEMANA     │
│   ─────────────────                          ────────────────────        │
│   🟡 CAC subió 15% por campaña Q1           • Cerramos deal Enterprise  │
│   🟢 NRR récord histórico                    • Churn bajo control        │
│   🟢 Pipeline Q2 +40% vs Q1                  • Hiring: 3 engineers       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Paso 4: Implementar Queries

```sql
-- MRR (Monthly Recurring Revenue)
WITH mrr_by_month AS (
    SELECT
        DATE_TRUNC('month', subscription_date) AS month,
        SUM(monthly_amount) AS mrr
    FROM subscriptions
    WHERE status = 'active'
    GROUP BY 1
)
SELECT
    month,
    mrr,
    LAG(mrr) OVER (ORDER BY month) AS prev_mrr,
    (mrr - LAG(mrr) OVER (ORDER BY month)) /
        NULLIF(LAG(mrr) OVER (ORDER BY month), 0) * 100 AS growth_pct
FROM mrr_by_month
ORDER BY month DESC
LIMIT 12;

-- Net Revenue Retention (NRR)
-- NRR = (MRR inicio - Churn - Contraction + Expansion) / MRR inicio * 100
WITH cohort_mrr AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', first_subscription_date) AS cohort_month,
        SUM(CASE WHEN month = cohort_month THEN monthly_amount ELSE 0 END) AS starting_mrr,
        SUM(CASE WHEN month = cohort_month + INTERVAL '12 months'
                 THEN monthly_amount ELSE 0 END) AS ending_mrr
    FROM subscription_history
    GROUP BY 1, 2
)
SELECT
    cohort_month,
    SUM(ending_mrr) / NULLIF(SUM(starting_mrr), 0) * 100 AS nrr_12_month
FROM cohort_mrr
GROUP BY cohort_month
ORDER BY cohort_month DESC;

-- CAC Payback Period (en meses)
-- Payback = CAC / (ARPU * Gross Margin)
SELECT
    DATE_TRUNC('month', acquisition_date) AS month,
    AVG(acquisition_cost) AS avg_cac,
    AVG(monthly_revenue) AS avg_arpu,
    0.72 AS gross_margin,  -- 72% margen
    AVG(acquisition_cost) / NULLIF(AVG(monthly_revenue) * 0.72, 0) AS payback_months
FROM customers c
JOIN customer_revenue cr ON c.customer_id = cr.customer_id
GROUP BY 1
ORDER BY 1 DESC;
```

### Paso 5: Documentar el Dashboard

```yaml
# dashboard_spec.yaml
name: "Executive Dashboard"
owner: "Data Team"
refresh_frequency: "Daily 6 AM UTC"
audience: "C-Level, Board"

kpis:
  - name: "MRR"
    definition: "Sum of monthly recurring revenue from active subscriptions"
    source_table: "analytics.mrr_daily"
    thresholds:
      green: "MoM growth >= 5%"
      yellow: "MoM growth between 0% and 5%"
      red: "MoM growth < 0%"

  - name: "NRR"
    definition: "Revenue from existing customers after 12 months / Starting revenue"
    source_table: "analytics.cohort_retention"
    thresholds:
      green: ">= 100%"
      yellow: "90% - 100%"
      red: "< 90%"

  - name: "CAC Payback"
    definition: "Months to recover customer acquisition cost"
    source_table: "analytics.unit_economics"
    thresholds:
      green: "<= 12 months"
      yellow: "12 - 18 months"
      red: "> 18 months"

alerts:
  - condition: "mrr_growth < 0"
    severity: "critical"
    notify: ["cfo@company.com", "ceo@company.com"]

  - condition: "nrr < 90"
    severity: "warning"
    notify: ["cfo@company.com"]
```

### Interpretación

Este dashboard permite al CFO:
- **Ver la salud del negocio en 30 segundos** (KPIs arriba)
- **Entender tendencias** (gráfico de MRR)
- **Actuar sobre problemas** (alertas con contexto)
- **Preparar discusión** (notas de la semana)

---

## Ejemplo 3: Métricas de Producto (Engagement, Retention) - Nivel: Intermedio

### Contexto

**CloudAPI Systems** quiere entender mejor cómo los usuarios interactúan con su plataforma SaaS. El Head of Product necesita métricas de engagement y retention.

### Paso 1: Definir el Framework de Métricas de Producto

Usaremos el framework **HEART** de Google:

| Dimensión | Pregunta | Métrica |
|-----------|----------|---------|
| **H**appiness | ¿Están satisfechos? | NPS, CSAT |
| **E**ngagement | ¿Lo usan activamente? | DAU/MAU, Session Duration |
| **A**doption | ¿Adoptan nuevas features? | Feature Adoption Rate |
| **R**etention | ¿Vuelven? | D1, D7, D30 Retention |
| **T**ask Success | ¿Completan tareas? | Task Completion Rate |

### Paso 2: Calcular Ratio DAU/MAU (Stickiness)

```sql
-- DAU/MAU Ratio (Stickiness)
-- Indica qué porcentaje de usuarios mensuales usa el producto diariamente
-- Benchmark SaaS: 10-20% es bueno, >25% es excelente

WITH daily_users AS (
    SELECT
        event_date,
        COUNT(DISTINCT user_id) AS dau
    FROM user_events
    WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY event_date
),
monthly_users AS (
    SELECT
        COUNT(DISTINCT user_id) AS mau
    FROM user_events
    WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT
    d.event_date,
    d.dau,
    m.mau,
    ROUND(d.dau * 100.0 / NULLIF(m.mau, 0), 1) AS stickiness_pct
FROM daily_users d
CROSS JOIN monthly_users m
ORDER BY d.event_date;

-- Resultado esperado:
-- event_date  | dau    | mau     | stickiness_pct
-- 2024-03-01  | 8,500  | 45,000  | 18.9%
-- 2024-03-02  | 7,200  | 45,000  | 16.0%
-- 2024-03-03  | 3,100  | 45,000  | 6.9%   <- Fin de semana
```

### Paso 3: Análisis de Cohortes de Retención

```sql
-- Retention por Cohorte (D1, D7, D30)
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('week', MIN(event_date)) AS cohort_week,
        MIN(event_date) AS first_activity_date
    FROM user_events
    GROUP BY user_id
),
user_activities AS (
    SELECT
        uc.user_id,
        uc.cohort_week,
        uc.first_activity_date,
        ue.event_date,
        ue.event_date - uc.first_activity_date AS days_since_first
    FROM user_cohorts uc
    JOIN user_events ue ON uc.user_id = ue.user_id
)
SELECT
    cohort_week,
    COUNT(DISTINCT user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN days_since_first = 1 THEN user_id END) * 100.0 /
        COUNT(DISTINCT user_id) AS d1_retention,
    COUNT(DISTINCT CASE WHEN days_since_first = 7 THEN user_id END) * 100.0 /
        COUNT(DISTINCT user_id) AS d7_retention,
    COUNT(DISTINCT CASE WHEN days_since_first = 30 THEN user_id END) * 100.0 /
        COUNT(DISTINCT user_id) AS d30_retention
FROM user_activities
GROUP BY cohort_week
ORDER BY cohort_week DESC
LIMIT 8;

-- Resultado esperado:
-- cohort_week | cohort_size | d1_retention | d7_retention | d30_retention
-- 2024-W10    | 1,250       | 45.2%        | 28.4%        | NULL
-- 2024-W09    | 1,180       | 48.1%        | 30.2%        | 18.5%
-- 2024-W08    | 1,320       | 42.8%        | 26.1%        | 15.2%
```

### Paso 4: Feature Adoption Funnel

```sql
-- Feature Adoption: API Integration
-- Paso 1: Visit docs → Paso 2: Create API key → Paso 3: First API call → Paso 4: 10+ calls

WITH feature_funnel AS (
    SELECT
        user_id,
        MAX(CASE WHEN event_name = 'docs_visited' THEN 1 ELSE 0 END) AS step1_docs,
        MAX(CASE WHEN event_name = 'api_key_created' THEN 1 ELSE 0 END) AS step2_key,
        MAX(CASE WHEN event_name = 'first_api_call' THEN 1 ELSE 0 END) AS step3_first_call,
        MAX(CASE WHEN event_name = 'api_power_user' THEN 1 ELSE 0 END) AS step4_power_user
    FROM user_events
    WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT
    COUNT(*) AS total_users,
    SUM(step1_docs) AS visited_docs,
    SUM(step2_key) AS created_key,
    SUM(step3_first_call) AS made_first_call,
    SUM(step4_power_user) AS power_users,
    -- Conversion rates
    ROUND(SUM(step1_docs) * 100.0 / COUNT(*), 1) AS pct_docs,
    ROUND(SUM(step2_key) * 100.0 / NULLIF(SUM(step1_docs), 0), 1) AS docs_to_key,
    ROUND(SUM(step3_first_call) * 100.0 / NULLIF(SUM(step2_key), 0), 1) AS key_to_call,
    ROUND(SUM(step4_power_user) * 100.0 / NULLIF(SUM(step3_first_call), 0), 1) AS call_to_power
FROM feature_funnel;

-- Resultado esperado:
-- total_users | visited_docs | created_key | made_first_call | power_users
-- 5,000       | 2,500        | 1,200       | 800             | 320
--
-- pct_docs | docs_to_key | key_to_call | call_to_power
-- 50.0%    | 48.0%       | 66.7%       | 40.0%
```

### Paso 5: Dashboard de Producto

```
┌──────────────────────────────────────────────────────────────────────┐
│  CLOUDAPI SYSTEMS - PRODUCT METRICS                     Marzo 2024  │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ENGAGEMENT                                     RETENTION             │
│  ───────────                                    ─────────             │
│  DAU: 8,500                                     D1: 45% ████████░░   │
│  MAU: 45,000                                    D7: 28% █████░░░░░   │
│  Stickiness: 18.9% ████████░░                   D30: 18% ███░░░░░░░  │
│                                                                       │
│  Avg Session: 12.4 min                          Benchmark D7: 25%    │
│  Sessions/User: 3.2/week                        Status: 🟢 Above     │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  FEATURE ADOPTION: API INTEGRATION                                   │
│                                                                       │
│  Visit Docs ──────► Create Key ──────► First Call ──────► Power User │
│    2,500              1,200               800               320       │
│    (50%)             (48%)               (67%)             (40%)     │
│                                                                       │
│  ⚠️ Mayor drop-off: Docs → Key (52% abandono)                        │
│  💡 Acción: Simplificar proceso de creación de API key               │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│  COHORT RETENTION - ÚLTIMAS 8 SEMANAS                                │
│                                                                       │
│  W10 ████████░░░░░░░░░░░░  45% D1                                    │
│  W09 █████████░░░░░░░░░░░  48% D1  →  ███░░░░░░  18% D30            │
│  W08 ███████░░░░░░░░░░░░░  43% D1  →  ███░░░░░░  15% D30            │
│  W07 ████████░░░░░░░░░░░░  46% D1  →  ████░░░░░  20% D30            │
│                                                                       │
│  📈 Tendencia: D1 mejorando +5pp desde W08                           │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

### Interpretación

Este análisis permite al equipo de producto:
- **Identificar cuellos de botella** en la adopción (Docs → Key)
- **Medir impacto de cambios** comparando cohortes
- **Priorizar mejoras** basándose en datos de engagement
- **Alertar sobre problemas** de retención temprano

---

## Ejemplo 4: Sistema Completo de Métricas (OKRs) - Nivel: Avanzado

### Contexto

**DataFlow Industries** está implementando OKRs (Objectives and Key Results) para Q2. El CEO quiere un dashboard que conecte OKRs de empresa → equipo → individuo.

### Paso 1: Definir Estructura de OKRs

```
EMPRESA: DataFlow Industries - Q2 2024

OBJETIVO 1: Acelerar crecimiento de revenue
├── KR1.1: Aumentar MRR de $2M a $2.8M (+40%)
├── KR1.2: Cerrar 5 deals Enterprise (>$50K ARR)
└── KR1.3: Reducir churn de 4% a 2%

OBJETIVO 2: Mejorar eficiencia operativa
├── KR2.1: Reducir CAC de $100 a $75 (-25%)
├── KR2.2: Aumentar NPS de 42 a 55 (+13 puntos)
└── KR2.3: Reducir tiempo de onboarding de 14 a 7 días

OBJETIVO 3: Escalar el equipo de datos
├── KR3.1: Contratar 3 Data Engineers
├── KR3.2: Implementar Data Catalog con 100% de tablas documentadas
└── KR3.3: Reducir tiempo de creación de dashboards de 5 a 2 días
```

### Paso 2: Mapear KRs a Métricas Técnicas

```sql
-- Tabla de definición de OKRs
CREATE TABLE okr_definitions (
    okr_id VARCHAR(10) PRIMARY KEY,
    objective_id INT,
    objective_name VARCHAR(200),
    key_result_name VARCHAR(200),
    metric_name VARCHAR(100),
    baseline_value DECIMAL(10,2),
    target_value DECIMAL(10,2),
    unit VARCHAR(20),
    owner_team VARCHAR(50),
    source_query TEXT
);

-- Insertar definiciones
INSERT INTO okr_definitions VALUES
('KR1.1', 1, 'Acelerar crecimiento de revenue',
 'Aumentar MRR de $2M a $2.8M', 'mrr', 2000000, 2800000, 'USD', 'Sales',
 'SELECT SUM(monthly_amount) FROM subscriptions WHERE status = ''active'''),

('KR1.2', 1, 'Acelerar crecimiento de revenue',
 'Cerrar 5 deals Enterprise', 'enterprise_deals', 0, 5, 'count', 'Sales',
 'SELECT COUNT(*) FROM deals WHERE arr >= 50000 AND closed_date >= ''2024-04-01'''),

('KR1.3', 1, 'Acelerar crecimiento de revenue',
 'Reducir churn de 4% a 2%', 'churn_rate', 4.0, 2.0, 'percent', 'Success',
 'SELECT churned_mrr / starting_mrr * 100 FROM mrr_movements WHERE month = current_month');
```

### Paso 3: Crear Tabla de Progreso de OKRs

```sql
-- Tracking diario de OKRs
CREATE TABLE okr_progress (
    date DATE,
    okr_id VARCHAR(10),
    current_value DECIMAL(10,2),
    progress_pct DECIMAL(5,2),  -- 0-100, puede superar 100
    on_track BOOLEAN,  -- ¿Vamos bien según proyección lineal?
    PRIMARY KEY (date, okr_id)
);

-- Query para calcular progreso
WITH okr_current AS (
    SELECT
        CURRENT_DATE AS date,
        'KR1.1' AS okr_id,
        (SELECT SUM(monthly_amount) FROM subscriptions WHERE status = 'active') AS current_value
    UNION ALL
    SELECT
        CURRENT_DATE,
        'KR1.2',
        (SELECT COUNT(*) FROM deals WHERE arr >= 50000 AND closed_date >= '2024-04-01')
    UNION ALL
    SELECT
        CURRENT_DATE,
        'KR1.3',
        (SELECT churned_mrr / NULLIF(starting_mrr, 0) * 100
         FROM mrr_movements WHERE month = DATE_TRUNC('month', CURRENT_DATE))
)
SELECT
    oc.date,
    oc.okr_id,
    od.key_result_name,
    od.baseline_value,
    oc.current_value,
    od.target_value,
    -- Calcular progreso (manejar caso donde menor es mejor, ej: churn)
    CASE
        WHEN od.target_value > od.baseline_value THEN
            (oc.current_value - od.baseline_value) /
            NULLIF(od.target_value - od.baseline_value, 0) * 100
        ELSE
            (od.baseline_value - oc.current_value) /
            NULLIF(od.baseline_value - od.target_value, 0) * 100
    END AS progress_pct,
    -- ¿Estamos on track? (proyección lineal basada en días transcurridos del Q)
    CASE
        WHEN (CURRENT_DATE - '2024-04-01'::date) / 91.0 * 100 <=
             CASE
                 WHEN od.target_value > od.baseline_value THEN
                     (oc.current_value - od.baseline_value) /
                     NULLIF(od.target_value - od.baseline_value, 0) * 100
                 ELSE
                     (od.baseline_value - oc.current_value) /
                     NULLIF(od.baseline_value - od.target_value, 0) * 100
             END
        THEN TRUE
        ELSE FALSE
    END AS on_track
FROM okr_current oc
JOIN okr_definitions od ON oc.okr_id = od.okr_id;
```

### Paso 4: Dashboard de OKRs

```
┌──────────────────────────────────────────────────────────────────────────┐
│  DATAFLOW INDUSTRIES - OKR DASHBOARD Q2 2024                             │
│  Semana 6 de 13 (46% del trimestre)                   Actualizado: Hoy   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  RESUMEN EJECUTIVO                                                       │
│  ─────────────────                                                       │
│  Objetivos: 3    Key Results: 9    On Track: 6/9 (67%)                  │
│                                                                           │
│  [██████████████████░░░░░░░░░░░░] 67% objetivos en verde                │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  OBJETIVO 1: Acelerar crecimiento de revenue                             │
│  Owner: VP Sales | Status: 🟡 At Risk                                    │
│  ──────────────────────────────────────────────────────────────────────  │
│                                                                           │
│  KR1.1: MRR $2M → $2.8M                                                  │
│  Current: $2.32M | Progress: 40% | Expected: 46%                         │
│  [████████████████░░░░░░░░░░░░░░░░░░░░] 🟡 Slightly Behind              │
│                                                                           │
│  KR1.2: 5 Enterprise Deals                                               │
│  Current: 3 | Progress: 60% | Expected: 46%                              │
│  [████████████████████████░░░░░░░░░░░░] 🟢 Ahead                         │
│                                                                           │
│  KR1.3: Churn 4% → 2%                                                    │
│  Current: 3.8% | Progress: 10% | Expected: 46%                           │
│  [████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 🔴 At Risk                       │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  OBJETIVO 2: Mejorar eficiencia operativa                                │
│  Owner: VP Ops | Status: 🟢 On Track                                     │
│  ──────────────────────────────────────────────────────────────────────  │
│                                                                           │
│  KR2.1: CAC $100 → $75                                                   │
│  [████████████████████░░░░░░░░░░░░░░░░] 50% 🟢                           │
│                                                                           │
│  KR2.2: NPS 42 → 55                                                      │
│  [████████████████████████░░░░░░░░░░░░] 62% 🟢                           │
│                                                                           │
│  KR2.3: Onboarding 14 → 7 días                                           │
│  [██████████████░░░░░░░░░░░░░░░░░░░░░░] 35% 🟡                           │
│                                                                           │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ⚠️ ITEMS QUE REQUIEREN ATENCIÓN                                         │
│  ──────────────────────────────────                                      │
│  🔴 KR1.3 (Churn): -36pp vs. esperado. Acción: Reunión con Success      │
│  🟡 KR1.1 (MRR): -6pp vs. esperado. Pipeline Q2 fuerte, monitorear      │
│  🟡 KR2.3 (Onboarding): Iniciativa de automatización en progreso        │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Paso 5: Drill-Down por Equipo

```sql
-- Desglose de KR por contribución de equipo
WITH team_contributions AS (
    SELECT
        'KR1.1' AS okr_id,
        sales_rep_team AS team,
        SUM(monthly_amount) AS contributed_mrr
    FROM subscriptions s
    JOIN sales_reps sr ON s.sales_rep_id = sr.id
    WHERE s.created_date >= '2024-04-01'
      AND s.status = 'active'
    GROUP BY sales_rep_team
)
SELECT
    team,
    contributed_mrr,
    contributed_mrr / 800000.0 * 100 AS pct_of_target,  -- Target = $800K new MRR
    RANK() OVER (ORDER BY contributed_mrr DESC) AS rank
FROM team_contributions
ORDER BY contributed_mrr DESC;

-- Resultado:
-- team       | contributed_mrr | pct_of_target | rank
-- Enterprise | $180,000        | 22.5%         | 1
-- Mid-Market | $95,000         | 11.9%         | 2
-- SMB        | $45,000         | 5.6%          | 3
```

### Interpretación

Este sistema de OKRs permite:

1. **Alineación vertical**: De empresa → equipo → individuo
2. **Transparencia**: Todos ven el progreso en tiempo real
3. **Acción temprana**: Alertas cuando algo está off-track
4. **Accountability**: Cada KR tiene un owner claro
5. **Aprendizaje**: Histórico para mejorar estimaciones futuras

---

## Resumen de Ejemplos

| Ejemplo | Nivel | Concepto Principal | Aplicación |
|---------|-------|-------------------|------------|
| 1 | Básico | Definición de KPIs | E-commerce delivery |
| 2 | Intermedio | Dashboard ejecutivo | Board meeting |
| 3 | Intermedio | Métricas de producto | SaaS engagement |
| 4 | Avanzado | Sistema OKRs | Tracking organizacional |

Estos ejemplos muestran la progresión desde KPIs simples hasta sistemas completos de métricas que alinean toda la organización.

---

**Siguiente paso**: [03-EJERCICIOS.md](03-EJERCICIOS.md) - Practica diseñando tus propios KPIs y dashboards
