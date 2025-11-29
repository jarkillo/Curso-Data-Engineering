# Ejercicios Prácticos: Analytics y Business Intelligence

Este documento contiene 15 ejercicios graduados para practicar los conceptos de Analytics y BI.

**Distribución:**
- 5 ejercicios básicos (1-5)
- 6 ejercicios intermedios (6-11)
- 4 ejercicios avanzados (12-15)

---

## Ejercicios Básicos

### Ejercicio 1: Identificar Métricas vs KPIs

**Dificultad**: Fácil

**Contexto**:
Eres el Data Engineer de **LogisticFlow**, una empresa de envíos. Te dan la siguiente lista de indicadores:

```
1. Número total de envíos este mes
2. Tiempo promedio de entrega: 2.3 días (objetivo: <2 días)
3. Paquetes perdidos: 45
4. Tasa de entrega a tiempo: 87% (objetivo: 95%)
5. Kilómetros recorridos: 125,000
6. Costo por envío: $4.50 (objetivo: <$4.00)
7. Conductores activos: 82
8. Satisfacción del cliente (NPS): 38 (objetivo: 50)
```

**Pregunta**:
Clasifica cada indicador como **Métrica** o **KPI**, y justifica tu respuesta.

**Pista**:
Un KPI tiene objetivo, umbral, y está vinculado a una meta de negocio.

---

### Ejercicio 2: Calcular KPIs Básicos de E-commerce

**Dificultad**: Fácil

**Contexto**:
**RestaurantData Co.** te proporciona los siguientes datos de marzo 2024:

```python
datos_marzo = {
    "revenue_total": 450000,  # $450,000
    "numero_pedidos": 12500,
    "clientes_unicos": 8200,
    "clientes_nuevos": 2100,
    "clientes_que_volvieron": 3400,
    "pedidos_cancelados": 375,
    "gasto_marketing": 52500  # $52,500
}
```

**Preguntas**:
1. Calcula el **Ticket Promedio (AOV)**
2. Calcula la **Tasa de Cancelación**
3. Calcula el **CAC (Customer Acquisition Cost)**
4. Calcula la **Tasa de Recompra**

**Pista**:
- AOV = Revenue / Pedidos
- CAC = Gasto Marketing / Clientes Nuevos

---

### Ejercicio 3: Diseñar Umbrales de Alerta

**Dificultad**: Fácil

**Contexto**:
**CloudAPI Systems** tiene los siguientes KPIs para su API:

| KPI | Valor Actual | Benchmark Industria |
|-----|--------------|---------------------|
| Uptime | 99.5% | 99.9% |
| Latencia P95 | 180ms | <200ms |
| Error Rate | 0.8% | <1% |
| API Calls/día | 2.1M | N/A |

**Pregunta**:
Para cada KPI, define umbrales de alerta (Verde/Amarillo/Rojo) basándote en los benchmarks y mejores prácticas.

**Pista**:
- Verde = Cumple o supera objetivo
- Amarillo = Zona de precaución
- Rojo = Requiere acción inmediata

---

### Ejercicio 4: Identificar Antipatrones

**Dificultad**: Fácil

**Contexto**:
Te muestran el siguiente dashboard de **FinTech Analytics**:

```
┌────────────────────────────────────────────────────────────────────┐
│  DASHBOARD GENERAL - TODO EN UNO                                   │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [3D Pie Chart]     [Animated Bar Graph]    [Spinning Globe]       │
│   Revenue by        Sales Trend              Office Locations       │
│   Product           (rainbow colors)                                │
│                                                                     │
│  Users: 45,231      Pageviews: 2.3M         Sessions: 890K         │
│  Revenue: $1.2M     Transactions: 12,453    API Calls: 5.6M        │
│  NPS: 42            CSAT: 4.2               Churn: 3.2%            │
│  CAC: $85           LTV: $1,200             MRR: $890K             │
│  Tickets: 234       Response Time: 2.1h     Resolution: 89%        │
│  Deploys: 45        Incidents: 3            Uptime: 99.8%          │
│                                                                     │
│  [Table with 50 rows of data - needs scrolling]                    │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

**Pregunta**:
Identifica al menos 5 antipatrones presentes en este dashboard y explica por qué son problemáticos.

**Pista**:
Revisa la teoría sobre los 5 antipatrones comunes.

---

### Ejercicio 5: Clasificar en Pirámide de Métricas

**Dificultad**: Fácil

**Contexto**:
**DataFlow Industries** tiene estas métricas:

```
1. Revenue anual
2. Tiempo de respuesta del servidor (ms)
3. Tasa de conversión del funnel de ventas
4. Número de deploys por día
5. Market share
6. Tickets de soporte resueltos por hora
7. Customer Lifetime Value
8. Bugs encontrados por sprint
9. Net Promoter Score
10. Uptime del sistema
```

**Pregunta**:
Clasifica cada métrica en la pirámide:
- **Operativas** (equipos, día a día)
- **Tácticas** (directores, semanal/mensual)
- **Estratégicas** (C-level, trimestral/anual)

**Pista**:
Piensa: ¿Quién usa esta métrica? ¿Con qué frecuencia?

---

## Soluciones Básicas

### Solución Ejercicio 1

| Indicador | Clasificación | Justificación |
|-----------|---------------|---------------|
| 1. Envíos totales | Métrica | Sin objetivo definido |
| 2. Tiempo entrega | **KPI** | Tiene objetivo (<2 días) |
| 3. Paquetes perdidos | Métrica | Número absoluto sin contexto |
| 4. Entrega a tiempo | **KPI** | Tiene objetivo (95%) |
| 5. Kilómetros | Métrica | Sin objetivo, operativo |
| 6. Costo por envío | **KPI** | Tiene objetivo (<$4) |
| 7. Conductores | Métrica | Informativo, sin objetivo |
| 8. NPS | **KPI** | Tiene objetivo (50) |

**Aprendizaje**: Un KPI siempre tiene un objetivo numérico y está vinculado a una meta de negocio.

---

### Solución Ejercicio 2

```python
datos_marzo = {
    "revenue_total": 450000,
    "numero_pedidos": 12500,
    "clientes_unicos": 8200,
    "clientes_nuevos": 2100,
    "clientes_que_volvieron": 3400,
    "pedidos_cancelados": 375,
    "gasto_marketing": 52500
}

# 1. Ticket Promedio (AOV)
aov = datos_marzo["revenue_total"] / datos_marzo["numero_pedidos"]
print(f"AOV: ${aov:.2f}")  # $36.00

# 2. Tasa de Cancelación
tasa_cancelacion = (
    datos_marzo["pedidos_cancelados"] / datos_marzo["numero_pedidos"]
) * 100
print(f"Tasa Cancelación: {tasa_cancelacion:.1f}%")  # 3.0%

# 3. CAC (Customer Acquisition Cost)
cac = datos_marzo["gasto_marketing"] / datos_marzo["clientes_nuevos"]
print(f"CAC: ${cac:.2f}")  # $25.00

# 4. Tasa de Recompra
tasa_recompra = (
    datos_marzo["clientes_que_volvieron"] / datos_marzo["clientes_unicos"]
) * 100
print(f"Tasa Recompra: {tasa_recompra:.1f}%")  # 41.5%
```

**Resultado esperado**:
- AOV: $36.00
- Tasa de Cancelación: 3.0%
- CAC: $25.00
- Tasa de Recompra: 41.5%

---

### Solución Ejercicio 3

| KPI | Verde | Amarillo | Rojo |
|-----|-------|----------|------|
| Uptime | ≥99.9% | 99.5%-99.9% | <99.5% |
| Latencia P95 | <150ms | 150-200ms | >200ms |
| Error Rate | <0.5% | 0.5%-1% | >1% |
| API Calls | N/A | N/A | N/A (solo informativo) |

**Nota**: API Calls no es un KPI porque no tiene objetivo; es una métrica de volumen.

---

### Solución Ejercicio 4

**Antipatrones identificados**:

1. **Dashboard Frankenstein**: Mezcla métricas de ventas, producto, soporte, ingeniería sin coherencia
2. **Exceso visual**: Gráficos 3D, animaciones, colores rainbow que dificultan la lectura
3. **Demasiadas métricas**: 18+ métricas sin jerarquía clara
4. **Sin contexto**: Números sin comparación (¿$1.2M es bueno o malo?)
5. **Vanity metrics mezcladas**: Pageviews y sessions junto con métricas de negocio
6. **Sin audiencia clara**: ¿Es para el CEO? ¿Para soporte? ¿Para producto?
7. **Requiere scroll**: Tabla de 50 filas que esconde información importante

**Cómo mejorarlo**: Crear dashboards separados por audiencia, eliminar 3D, mostrar comparaciones.

---

### Solución Ejercicio 5

**Operativas** (Equipos, día a día):
- 2. Tiempo de respuesta del servidor
- 4. Número de deploys por día
- 6. Tickets resueltos por hora
- 8. Bugs por sprint
- 10. Uptime del sistema

**Tácticas** (Directores, semanal/mensual):
- 3. Tasa de conversión
- 7. Customer Lifetime Value
- 9. Net Promoter Score

**Estratégicas** (C-level, trimestral/anual):
- 1. Revenue anual
- 5. Market share

---

## Ejercicios Intermedios

### Ejercicio 6: Diseñar Dashboard para Equipo de Ventas

**Dificultad**: Media

**Contexto**:
El VP de Ventas de **RestaurantData Co.** necesita un dashboard para su reunión semanal con el equipo comercial.

**Datos disponibles**:
```sql
-- Tablas disponibles
fact_sales (sale_id, date, sales_rep_id, customer_id, amount, status)
dim_sales_reps (rep_id, name, team, region, hire_date)
dim_customers (customer_id, segment, acquisition_date, lifetime_value)
sales_targets (rep_id, month, target_amount)
```

**Preguntas**:
1. Lista los 5 KPIs principales que debe tener este dashboard
2. Diseña el layout del dashboard (ASCII art)
3. Escribe la query SQL para el KPI de "% de cuota alcanzada por representante"

**Pista**:
El VP quiere ver: rendimiento del equipo, pipeline, tendencias, y comparación con objetivos.

---

### Ejercicio 7: Análisis de Cohortes de Retención

**Dificultad**: Media

**Contexto**:
**CloudAPI Systems** quiere analizar la retención de usuarios por cohorte mensual.

**Datos**:
```python
# Eventos de usuarios (user_id, event_date, event_type)
eventos = [
    (1, "2024-01-05", "signup"),
    (1, "2024-01-06", "login"),
    (1, "2024-01-15", "login"),
    (1, "2024-02-03", "login"),
    (2, "2024-01-10", "signup"),
    (2, "2024-01-11", "login"),
    # Usuario 2 no vuelve en febrero
    (3, "2024-02-01", "signup"),
    (3, "2024-02-05", "login"),
    (3, "2024-02-28", "login"),
    (3, "2024-03-10", "login"),
    # ... más usuarios
]
```

**Preguntas**:
1. Escribe la query SQL para calcular retención D7, D14, D30 por cohorte mensual
2. ¿Qué insights puedes obtener de una tabla de cohortes?
3. ¿Cómo identificarías si un cambio de producto mejoró la retención?

**Pista**:
Agrupa usuarios por mes de signup, luego calcula % que vuelven en cada periodo.

---

### Ejercicio 8: Funnel de Conversión

**Dificultad**: Media

**Contexto**:
**FinTech Analytics** tiene un funnel de registro:

```
Paso 1: Visit Landing Page
Paso 2: Click "Start Free Trial"
Paso 3: Complete Email Form
Paso 4: Verify Email
Paso 5: Complete Onboarding
Paso 6: First Active Use
```

**Datos de marzo**:
```python
funnel_marzo = {
    "landing_page": 50000,
    "click_trial": 8500,
    "complete_form": 4200,
    "verify_email": 3150,
    "complete_onboarding": 1890,
    "first_active_use": 945
}
```

**Preguntas**:
1. Calcula la tasa de conversión de cada paso
2. Identifica el "cuello de botella" (mayor drop-off)
3. Si mejoras el cuello de botella en 20%, ¿cuántos usuarios activos más tendrías?
4. Diseña 2 experimentos A/B para mejorar el funnel

**Pista**:
Tasa de conversión = Usuarios paso N / Usuarios paso N-1

---

### Ejercicio 9: Dashboard Mockup con Data Storytelling

**Dificultad**: Media

**Contexto**:
Eres Data Engineer en **LogisticFlow**. Descubriste que los envíos de la Región Norte tienen 35% más retrasos que otras regiones.

**Pregunta**:
Diseña una página de dashboard que cuente esta historia con datos:
1. Estructura la narrativa (Contexto → Problema → Análisis → Recomendación)
2. Crea el layout visual (ASCII art)
3. Especifica qué datos necesitas mostrar en cada sección
4. Propón 2 acciones concretas basadas en los datos

**Pista**:
No solo muestres el problema; guía al usuario hacia la solución.

---

### Ejercicio 10: Métricas de Producto SaaS

**Dificultad**: Media

**Contexto**:
**CloudAPI Systems** quiere implementar el framework AARRR (Pirate Metrics):

| Etapa | Pregunta |
|-------|----------|
| Acquisition | ¿De dónde vienen los usuarios? |
| Activation | ¿Tienen una buena primera experiencia? |
| Retention | ¿Vuelven? |
| Revenue | ¿Pagan? |
| Referral | ¿Nos recomiendan? |

**Pregunta**:
Para cada etapa del framework AARRR:
1. Define 2 métricas específicas
2. Indica cómo las calcularías (query SQL conceptual)
3. Define qué sería "bueno" vs "malo" para esa métrica

**Pista**:
Piensa en qué eventos de usuario indican cada etapa.

---

### Ejercicio 11: Documentar Diccionario de Métricas

**Dificultad**: Media

**Contexto**:
En **DataFlow Industries** hay confusión sobre cómo calcular "Revenue". Marketing, Ventas y Finanzas lo calculan diferente.

**Preguntas**:
1. Diseña una plantilla de documentación de métricas que incluya:
   - Nombre, definición, fórmula
   - Fuente de datos, frecuencia de actualización
   - Owner, historial de cambios
2. Documenta la métrica "MRR (Monthly Recurring Revenue)" usando tu plantilla
3. ¿Cómo implementarías esta definición única en tu Data Warehouse?

**Pista**:
Piensa en cómo dbt semantic layer o Looker LookML resuelven este problema.

---

## Soluciones Intermedias

### Solución Ejercicio 6

**1. KPIs principales**:
- Revenue MTD vs Target
- % Cuota alcanzada por rep
- Pipeline value (oportunidades abiertas)
- Win rate (deals cerrados / total deals)
- Average deal size

**2. Layout**:
```
┌─────────────────────────────────────────────────────────────────┐
│  SALES DASHBOARD - Semana 12                    [Filtro: Marzo] │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  💰 Revenue MTD    🎯 vs Target    📊 Pipeline    🏆 Win Rate   │
│  $320,450          87%             $890K          32%           │
│  ↑ 12% WoW         🟡 At Risk      ↑ 15%          → 0%          │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  PERFORMANCE BY REP                    TREND (últimas 8 semanas)│
│  ───────────────────                   ─────────────────────────│
│  Rep        | Revenue | % Cuota       $400K ┤         ╭──*      │
│  Ana García | $85K    | 112% 🟢             │    ╭────╯         │
│  Carlos Ruiz| $72K    | 95%  🟡       $200K ┤╭───╯              │
│  María López| $45K    | 60%  🔴             │                   │
│  ...        | ...     | ...                 └────────────────── │
│                                              W5 W6 W7 W8 W9 W10 │
└─────────────────────────────────────────────────────────────────┘
```

**3. Query SQL**:
```sql
SELECT
    sr.name AS rep_name,
    sr.team,
    COALESCE(SUM(fs.amount), 0) AS revenue_mtd,
    st.target_amount,
    ROUND(
        COALESCE(SUM(fs.amount), 0) / NULLIF(st.target_amount, 0) * 100,
        1
    ) AS pct_quota
FROM dim_sales_reps sr
LEFT JOIN fact_sales fs
    ON sr.rep_id = fs.sales_rep_id
    AND fs.date >= DATE_TRUNC('month', CURRENT_DATE)
    AND fs.status = 'closed_won'
LEFT JOIN sales_targets st
    ON sr.rep_id = st.rep_id
    AND st.month = DATE_TRUNC('month', CURRENT_DATE)
GROUP BY sr.name, sr.team, st.target_amount
ORDER BY pct_quota DESC;
```

---

### Solución Ejercicio 7

**1. Query de cohortes**:
```sql
WITH user_cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', MIN(event_date)) AS cohort_month,
        MIN(event_date) AS signup_date
    FROM user_events
    WHERE event_type = 'signup'
    GROUP BY user_id
),
user_activity AS (
    SELECT
        uc.user_id,
        uc.cohort_month,
        ue.event_date,
        ue.event_date - uc.signup_date AS days_since_signup
    FROM user_cohorts uc
    JOIN user_events ue ON uc.user_id = ue.user_id
    WHERE ue.event_type = 'login'
)
SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN days_since_signup BETWEEN 1 AND 7
                        THEN user_id END) * 100.0 /
        COUNT(DISTINCT user_id) AS d7_retention,
    COUNT(DISTINCT CASE WHEN days_since_signup BETWEEN 8 AND 14
                        THEN user_id END) * 100.0 /
        COUNT(DISTINCT user_id) AS d14_retention,
    COUNT(DISTINCT CASE WHEN days_since_signup BETWEEN 15 AND 30
                        THEN user_id END) * 100.0 /
        COUNT(DISTINCT user_id) AS d30_retention
FROM user_activity
GROUP BY cohort_month
ORDER BY cohort_month;
```

**2. Insights de tabla de cohortes**:
- Identificar si la retención mejora o empeora con el tiempo
- Comparar cohortes antes/después de cambios de producto
- Detectar estacionalidad (ej: cohortes de diciembre tienen diferente comportamiento)

**3. Identificar mejora de producto**:
- Comparar cohortes pre y post lanzamiento
- Si D7/D30 aumenta en cohortes post-lanzamiento, el cambio funcionó

---

### Solución Ejercicio 8

**1. Tasas de conversión**:
```python
funnel = {
    "landing_page": 50000,
    "click_trial": 8500,
    "complete_form": 4200,
    "verify_email": 3150,
    "complete_onboarding": 1890,
    "first_active_use": 945
}

# Calcular conversiones
conversiones = {
    "landing → click": 8500 / 50000 * 100,      # 17.0%
    "click → form": 4200 / 8500 * 100,           # 49.4%
    "form → verify": 3150 / 4200 * 100,          # 75.0%
    "verify → onboarding": 1890 / 3150 * 100,    # 60.0%
    "onboarding → active": 945 / 1890 * 100      # 50.0%
}
```

**2. Cuello de botella**: Landing → Click (17%)
Es el mayor drop-off absoluto (41,500 usuarios perdidos)

**3. Impacto de mejora 20%**:
```python
# Si mejoramos landing→click de 17% a 20.4%
nuevo_click = 50000 * 0.204  # 10,200
# Manteniendo ratios subsecuentes:
nuevos_activos = 10200 * 0.494 * 0.75 * 0.60 * 0.50  # 1,134
mejora = 1134 - 945  # +189 usuarios activos (+20%)
```

**4. Experimentos A/B**:
- **Landing**: Probar diferentes CTAs, social proof, video explicativo
- **Email verification**: Reducir fricción con magic links, SSO

---

### Solución Ejercicio 9

**Narrativa estructurada**:

```
┌──────────────────────────────────────────────────────────────────────┐
│  📊 ANÁLISIS: RETRASOS EN REGIÓN NORTE                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📍 CONTEXTO                                                         │
│  ─────────                                                           │
│  La Región Norte representa 28% de nuestros envíos pero genera      │
│  45% de las quejas de clientes por retrasos.                        │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ⚠️ EL PROBLEMA                                                      │
│  ─────────────                                                       │
│  Tasa de retraso por región:                                        │
│                                                                       │
│  Norte  [████████████████████] 23.5%   ← 35% más que promedio       │
│  Centro [████████████]        15.2%                                  │
│  Sur    [██████████]          12.8%                                  │
│  Este   [███████████████]     18.1%                                  │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  🔍 ANÁLISIS: ¿POR QUÉ?                                              │
│  ─────────────────────                                               │
│  Desglose de causas en Región Norte:                                │
│                                                                       │
│  1. Rutas mal optimizadas    │ 45% │████████████████████│           │
│  2. Falta de conductores     │ 30% │█████████████│                  │
│  3. Clima adverso            │ 15% │██████│                         │
│  4. Otros                    │ 10% │████│                           │
│                                                                       │
│  💡 El 75% de los retrasos son evitables (rutas + conductores)      │
│                                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ✅ RECOMENDACIONES                                                  │
│  ─────────────────                                                   │
│  1. Implementar software de optimización de rutas                   │
│     Impacto estimado: -8pp en tasa de retrasos                      │
│     Inversión: $15K/mes | ROI: 6 meses                              │
│                                                                       │
│  2. Contratar 5 conductores adicionales para Norte                  │
│     Impacto estimado: -5pp en tasa de retrasos                      │
│     Inversión: $12K/mes | ROI: 3 meses                              │
│                                                                       │
│  📈 Impacto combinado: Reducir retrasos de 23.5% a 10.5%            │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

### Solución Ejercicio 10

**Framework AARRR documentado**:

| Etapa | Métrica 1 | Métrica 2 | Bueno | Malo |
|-------|-----------|-----------|-------|------|
| **Acquisition** | Signups por canal | CAC por canal | CAC < $50 | CAC > $150 |
| **Activation** | % onboarding completo | Time to first value | >60% | <30% |
| **Retention** | D7 retention | DAU/MAU | D7 >40% | D7 <20% |
| **Revenue** | Conversion trial→paid | ARPU | >5% | <2% |
| **Referral** | NPS | K-factor | NPS >50 | NPS <20 |

**Query ejemplo - Activation**:
```sql
SELECT
    DATE_TRUNC('week', signup_date) AS cohort_week,
    COUNT(*) AS total_signups,
    COUNT(*) FILTER (WHERE onboarding_completed) AS completed_onboarding,
    COUNT(*) FILTER (WHERE onboarding_completed) * 100.0 /
        COUNT(*) AS activation_rate,
    AVG(EXTRACT(EPOCH FROM first_value_time - signup_time) / 3600)
        AS avg_hours_to_value
FROM users
WHERE signup_date >= CURRENT_DATE - INTERVAL '8 weeks'
GROUP BY 1
ORDER BY 1;
```

---

### Solución Ejercicio 11

**Plantilla de documentación**:

```yaml
# metric_definition.yaml
metric:
  name: "MRR (Monthly Recurring Revenue)"
  display_name: "MRR"
  description: "Suma de ingresos recurrentes mensuales de suscripciones activas"

  definition:
    formula: "SUM(subscription.monthly_amount) WHERE subscription.status = 'active'"
    unit: "USD"
    aggregation_type: "sum"
    time_grain: "monthly"

  calculation:
    source_table: "analytics.subscriptions"
    sql: |
      SELECT
        DATE_TRUNC('month', calculation_date) AS month,
        SUM(monthly_amount) AS mrr
      FROM analytics.subscriptions
      WHERE status = 'active'
        AND calculation_date = DATE_TRUNC('month', calculation_date) + INTERVAL '1 month' - INTERVAL '1 day'
      GROUP BY 1

  business_context:
    owner: "Finance Team"
    stakeholders: ["CEO", "CFO", "VP Sales"]
    used_in: ["Executive Dashboard", "Board Reports", "Investor Updates"]

  thresholds:
    green: "MoM growth >= 5%"
    yellow: "MoM growth 0-5%"
    red: "MoM growth < 0%"

  data_quality:
    freshness: "Daily at 6 AM UTC"
    source_of_truth: "Stripe subscription data via Fivetran"
    known_issues: "Excludes annual plans paid monthly"

  history:
    - date: "2024-01-15"
      change: "Initial definition"
      author: "Data Team"
    - date: "2024-03-01"
      change: "Added exclusion of paused subscriptions"
      author: "Finance"
```

**Implementación en dbt**:
```sql
-- models/marts/metrics/mrr.sql
{{ config(materialized='table') }}

SELECT
    DATE_TRUNC('month', calculation_date) AS month,
    SUM(monthly_amount) AS mrr,
    COUNT(DISTINCT customer_id) AS paying_customers,
    SUM(monthly_amount) / NULLIF(COUNT(DISTINCT customer_id), 0) AS arpu
FROM {{ ref('stg_subscriptions') }}
WHERE status = 'active'
  AND NOT is_paused  -- Exclusión documentada
GROUP BY 1
```

---

## Ejercicios Avanzados

### Ejercicio 12: Sistema de Alertas Inteligentes

**Dificultad**: Difícil

**Contexto**:
**FinTech Analytics** quiere implementar alertas automáticas basadas en anomalías, no solo umbrales fijos.

**Preguntas**:
1. Diseña un sistema de detección de anomalías para el KPI "Daily Revenue"
2. ¿Qué técnicas estadísticas usarías? (ej: desviación estándar, MAD, modelos ML)
3. ¿Cómo manejarías la estacionalidad (ej: fines de semana siempre tienen menos revenue)?
4. Escribe pseudocódigo para la lógica de alertas
5. ¿Cómo evitarías "alert fatigue"?

**Pista**:
Considera usar rolling averages y bandas de confianza dinámicas.

---

### Ejercicio 13: OKRs Cascading con Drill-Down

**Dificultad**: Difícil

**Contexto**:
**DataFlow Industries** quiere conectar OKRs de empresa con OKRs de equipo y contribuciones individuales.

**Estructura**:
```
EMPRESA: Revenue $10M → $15M (+50%)
├── VENTAS: New ARR $3M
│   ├── Team Enterprise: 10 deals >$100K
│   │   └── Rep Ana: 3 deals
│   └── Team SMB: 500 nuevos clientes
│       └── Rep Carlos: 75 clientes
└── PRODUCTO: Retention 80% → 90%
    ├── Feature Team A: Reduce churn feature X
    └── Feature Team B: Improve onboarding
```

**Preguntas**:
1. Diseña el modelo de datos para almacenar esta jerarquía de OKRs
2. Escribe queries que calculen:
   - Progreso agregado de empresa basado en equipos
   - Contribución de cada individuo al OKR de empresa
3. Diseña el dashboard con drill-down
4. ¿Cómo manejarías OKRs compartidos entre equipos?

**Pista**:
Necesitarás tablas para: objetivos, key_results, contribuciones, y relaciones jerárquicas.

---

### Ejercicio 14: Real-time vs Batch Analytics

**Dificultad**: Difícil

**Contexto**:
**CloudAPI Systems** debate si implementar dashboards real-time o batch para diferentes casos de uso.

**Casos de uso**:
1. Dashboard de uptime y latencia para NOC
2. Dashboard de revenue para CFO
3. Dashboard de feature adoption para PM
4. Alertas de fraude para Risk Team
5. Reportes de fin de mes para Finanzas

**Preguntas**:
1. Para cada caso, indica si debería ser real-time o batch, y justifica
2. ¿Qué arquitectura de datos soportaría ambos? (Lambda, Kappa, etc.)
3. ¿Qué trade-offs hay entre precisión y velocidad?
4. Diseña el stack tecnológico recomendado
5. ¿Cómo asegurarías que métricas batch y real-time sean consistentes?

**Pista**:
Real-time tiene costo (infraestructura, complejidad). Úsalo solo cuando el beneficio lo justifica.

---

### Ejercicio 15: Proyecto Integrador - Dashboard Ejecutivo Completo

**Dificultad**: Difícil

**Contexto**:
Eres el Lead Data Engineer de **LogisticFlow**. El CEO te pide diseñar el sistema completo de analytics para la empresa.

**Requerimientos**:
1. Dashboard ejecutivo para board (trimestral)
2. Dashboard operativo para managers (diario)
3. Alertas automáticas
4. Self-service para analistas
5. Gobernanza de datos (quién ve qué)

**Entregables**:
1. Arquitectura completa del sistema (diagrama)
2. Modelo de datos para métricas (schema SQL)
3. 5 dashboards mockup (diferentes audiencias)
4. Política de refresh (qué se actualiza cuándo)
5. Estrategia de permisos y seguridad
6. Roadmap de implementación (fases)

**Pista**:
Este es un proyecto de diseño completo. No hay una única respuesta correcta.

---

## Soluciones Avanzadas

### Solución Ejercicio 12

**1. Diseño de detección de anomalías**:

```python
# Pseudocódigo para detección de anomalías en Daily Revenue

def detect_anomaly(current_value: float, historical_data: list) -> dict:
    """
    Detecta si el valor actual es anómalo basándose en histórico.
    Maneja estacionalidad comparando con mismo día de semanas anteriores.
    """
    # 1. Obtener valores del mismo día de la semana (últimas 8 semanas)
    same_day_values = get_same_weekday_values(historical_data, weeks=8)

    # 2. Calcular estadísticas robustas (MAD es más robusto que std)
    median = calculate_median(same_day_values)
    mad = calculate_mad(same_day_values)  # Median Absolute Deviation

    # 3. Definir bandas (más conservadoras que z-score)
    # Factor 3 es aproximadamente 99.7% de confianza
    lower_band = median - (3 * mad * 1.4826)  # 1.4826 normaliza MAD a std
    upper_band = median + (3 * mad * 1.4826)

    # 4. Evaluar
    is_anomaly = current_value < lower_band or current_value > upper_band

    # 5. Calcular severidad
    if is_anomaly:
        deviation = abs(current_value - median) / mad
        severity = "critical" if deviation > 5 else "warning"
    else:
        severity = None

    return {
        "is_anomaly": is_anomaly,
        "current_value": current_value,
        "expected_range": (lower_band, upper_band),
        "severity": severity,
        "deviation_mads": (current_value - median) / mad
    }
```

**2. Query SQL**:
```sql
WITH daily_revenue AS (
    SELECT
        date,
        EXTRACT(DOW FROM date) AS day_of_week,
        SUM(amount) AS revenue
    FROM fact_sales
    GROUP BY date
),
same_day_stats AS (
    SELECT
        day_of_week,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY revenue) AS median_revenue,
        -- MAD calculation
        PERCENTILE_CONT(0.5) WITHIN GROUP (
            ORDER BY ABS(revenue - (
                SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY revenue)
                FROM daily_revenue dr2
                WHERE dr2.day_of_week = dr.day_of_week
                  AND dr2.date >= CURRENT_DATE - INTERVAL '56 days'
            ))
        ) AS mad
    FROM daily_revenue dr
    WHERE date >= CURRENT_DATE - INTERVAL '56 days'
    GROUP BY day_of_week
)
SELECT
    dr.date,
    dr.revenue,
    sds.median_revenue,
    sds.median_revenue - (3 * sds.mad * 1.4826) AS lower_band,
    sds.median_revenue + (3 * sds.mad * 1.4826) AS upper_band,
    CASE
        WHEN dr.revenue < sds.median_revenue - (3 * sds.mad * 1.4826)
             OR dr.revenue > sds.median_revenue + (3 * sds.mad * 1.4826)
        THEN TRUE
        ELSE FALSE
    END AS is_anomaly
FROM daily_revenue dr
JOIN same_day_stats sds ON dr.day_of_week = sds.day_of_week
WHERE dr.date = CURRENT_DATE;
```

**5. Evitar alert fatigue**:
- Implementar "cooldown" (no alertar misma métrica en 4 horas)
- Agrupar alertas relacionadas en una sola notificación
- Escalación gradual (email → Slack → pager)
- Review semanal de alertas: eliminar las que no generan acción

---

### Solución Ejercicio 13

**1. Modelo de datos**:

```sql
-- Tabla de objetivos (jerárquica)
CREATE TABLE objectives (
    objective_id SERIAL PRIMARY KEY,
    parent_objective_id INT REFERENCES objectives(objective_id),
    level VARCHAR(20),  -- 'company', 'team', 'individual'
    owner_type VARCHAR(20),  -- 'company', 'team', 'person'
    owner_id INT,  -- FK a teams o people
    name VARCHAR(200),
    period VARCHAR(10)  -- 'Q1-2024'
);

-- Tabla de key results
CREATE TABLE key_results (
    kr_id SERIAL PRIMARY KEY,
    objective_id INT REFERENCES objectives(objective_id),
    name VARCHAR(200),
    metric_name VARCHAR(100),
    baseline_value DECIMAL(12,2),
    target_value DECIMAL(12,2),
    current_value DECIMAL(12,2),
    unit VARCHAR(20),
    weight DECIMAL(3,2) DEFAULT 1.0  -- Para ponderar importancia
);

-- Tabla de contribuciones (para OKRs compartidos)
CREATE TABLE kr_contributions (
    contribution_id SERIAL PRIMARY KEY,
    kr_id INT REFERENCES key_results(kr_id),
    contributor_kr_id INT REFERENCES key_results(kr_id),  -- KR hijo que contribuye
    contribution_weight DECIMAL(3,2),  -- % de contribución al padre
    UNIQUE(kr_id, contributor_kr_id)
);
```

**2. Query de progreso agregado**:
```sql
-- Calcular progreso de empresa basado en equipos
WITH RECURSIVE okr_tree AS (
    -- Base: KRs de nivel empresa
    SELECT
        kr.kr_id,
        kr.objective_id,
        o.level,
        kr.name,
        kr.baseline_value,
        kr.target_value,
        kr.current_value,
        kr.weight,
        1 AS depth,
        ARRAY[kr.kr_id] AS path
    FROM key_results kr
    JOIN objectives o ON kr.objective_id = o.objective_id
    WHERE o.level = 'company'

    UNION ALL

    -- Recursivo: KRs que contribuyen
    SELECT
        child_kr.kr_id,
        child_kr.objective_id,
        child_o.level,
        child_kr.name,
        child_kr.baseline_value,
        child_kr.target_value,
        child_kr.current_value,
        child_kr.weight * contrib.contribution_weight,
        parent.depth + 1,
        parent.path || child_kr.kr_id
    FROM okr_tree parent
    JOIN kr_contributions contrib ON parent.kr_id = contrib.kr_id
    JOIN key_results child_kr ON contrib.contributor_kr_id = child_kr.kr_id
    JOIN objectives child_o ON child_kr.objective_id = child_o.objective_id
    WHERE NOT child_kr.kr_id = ANY(parent.path)  -- Evitar ciclos
),
progress_calc AS (
    SELECT
        kr_id,
        level,
        name,
        CASE
            WHEN target_value > baseline_value THEN
                (current_value - baseline_value) /
                NULLIF(target_value - baseline_value, 0) * 100
            ELSE
                (baseline_value - current_value) /
                NULLIF(baseline_value - target_value, 0) * 100
        END AS progress_pct,
        weight
    FROM okr_tree
)
SELECT
    level,
    name,
    ROUND(progress_pct, 1) AS progress,
    ROUND(SUM(progress_pct * weight) OVER (PARTITION BY level) /
          SUM(weight) OVER (PARTITION BY level), 1) AS weighted_avg_progress
FROM progress_calc
ORDER BY level, progress_pct DESC;
```

---

### Solución Ejercicio 14

**1. Clasificación real-time vs batch**:

| Caso de Uso | Decisión | Justificación |
|-------------|----------|---------------|
| Uptime/Latencia NOC | **Real-time** | Downtime = pérdida inmediata, necesita acción en segundos |
| Revenue CFO | **Batch** | Decisiones estratégicas, no urgentes, precisión > velocidad |
| Feature Adoption PM | **Batch** | Análisis de tendencias, no requiere tiempo real |
| Alertas Fraude | **Real-time** | Cada segundo cuenta para prevenir pérdidas |
| Reportes Fin de Mes | **Batch** | Necesita precisión absoluta, datos reconciliados |

**2. Arquitectura Lambda**:
```
                    ┌─────────────────────────────────────────┐
                    │             SPEED LAYER                 │
                    │  (Kafka → Flink → Redis → Dashboard)    │
                    │  Latencia: segundos                     │
                    │  Precisión: ~95% (aproximada)           │
                    └──────────────────┬──────────────────────┘
                                       │
    Sources ─────►  Kafka  ────────────┼──────────────────────►  Serving
                                       │                         Layer
                    ┌──────────────────┴──────────────────────┐
                    │             BATCH LAYER                 │
                    │  (Kafka → DWH → dbt → Dashboard)        │
                    │  Latencia: horas                        │
                    │  Precisión: 100% (exacta)               │
                    └─────────────────────────────────────────┘
```

**4. Stack recomendado**:
- **Ingesta**: Kafka, Debezium (CDC)
- **Real-time**: Apache Flink, ksqlDB
- **Batch**: Snowflake/BigQuery, dbt
- **Serving**: Redis (real-time), PostgreSQL (batch)
- **BI**: Grafana (real-time), Metabase (batch)
- **Alertas**: PagerDuty, Opsgenie

**5. Consistencia batch/real-time**:
- Usar mismas definiciones de métricas (dbt semantic layer)
- Mostrar "data freshness" en dashboards
- Reconciliación automática: comparar valores RT vs batch, alertar si diff > threshold
- Documentar que real-time es "aproximado" y batch es "oficial"

---

### Solución Ejercicio 15

**1. Arquitectura del Sistema**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        LOGISTICFLOW ANALYTICS PLATFORM                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   SOURCES              INGESTION           STORAGE           SERVING    │
│   ───────              ─────────           ───────           ───────    │
│                                                                          │
│   ┌─────┐             ┌─────────┐        ┌──────────┐     ┌──────────┐ │
│   │ ERP │────────────►│ Fivetran│───────►│ Snowflake│────►│ Metabase │ │
│   └─────┘             └─────────┘        │   DWH    │     │ (BI)     │ │
│                                          └──────────┘     └──────────┘ │
│   ┌─────┐             ┌─────────┐              │                        │
│   │ CRM │────────────►│ Airbyte │──────────────┘          ┌──────────┐ │
│   └─────┘             └─────────┘                         │ Grafana  │ │
│                                                           │ (Real-   │ │
│   ┌─────┐             ┌─────────┐        ┌──────────┐    │  time)   │ │
│   │ GPS │────────────►│  Kafka  │───────►│ ClickHse │────►└──────────┘ │
│   │Trucks│            └─────────┘        │ (RT)     │                   │
│   └─────┘                                └──────────┘     ┌──────────┐ │
│                                                           │PagerDuty │ │
│   ┌─────┐                                                │ (Alerts) │ │
│   │ API │             ┌─────────┐        ┌──────────┐    └──────────┘ │
│   │ Logs│────────────►│ Fluentd │───────►│ OpenSrch │                   │
│   └─────┘             └─────────┘        │ (Logs)   │                   │
│                                          └──────────┘                   │
│                                                                          │
│               TRANSFORMATION                    GOVERNANCE              │
│               ──────────────                    ──────────              │
│                                                                          │
│               ┌─────────┐                      ┌──────────┐             │
│               │   dbt   │                      │ Atlan    │             │
│               │ (ELT)   │                      │ (Catalog)│             │
│               └─────────┘                      └──────────┘             │
│                                                                          │
│               ┌─────────┐                      ┌──────────┐             │
│               │ Airflow │                      │  RBAC    │             │
│               │ (Orch)  │                      │ (Perms)  │             │
│               └─────────┘                      └──────────┘             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**2. Modelo de datos para métricas**:

```sql
-- Schema de métricas en Snowflake
CREATE SCHEMA analytics.metrics;

-- Tabla de definiciones
CREATE TABLE analytics.metrics.metric_definitions (
    metric_id VARCHAR(50) PRIMARY KEY,
    metric_name VARCHAR(100),
    description TEXT,
    formula TEXT,
    source_table VARCHAR(100),
    owner_team VARCHAR(50),
    refresh_frequency VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);

-- Tabla de valores históricos
CREATE TABLE analytics.metrics.metric_values (
    metric_id VARCHAR(50),
    dimension_date DATE,
    dimension_region VARCHAR(50),
    dimension_product VARCHAR(50),
    value DECIMAL(18,4),
    PRIMARY KEY (metric_id, dimension_date, dimension_region, dimension_product)
);

-- Tabla de umbrales
CREATE TABLE analytics.metrics.metric_thresholds (
    metric_id VARCHAR(50),
    threshold_type VARCHAR(10),  -- 'green', 'yellow', 'red'
    min_value DECIMAL(18,4),
    max_value DECIMAL(18,4),
    PRIMARY KEY (metric_id, threshold_type)
);
```

**6. Roadmap de implementación**:

| Fase | Duración | Entregables |
|------|----------|-------------|
| 1. Foundation | 4 semanas | DWH setup, ingesta básica, dbt inicial |
| 2. Core Dashboards | 4 semanas | 3 dashboards principales, alertas básicas |
| 3. Self-Service | 3 semanas | Metabase para analistas, catálogo de datos |
| 4. Advanced | 4 semanas | Real-time para NOC, ML anomaly detection |
| 5. Governance | 2 semanas | RBAC, auditoría, documentación completa |

---

## Resumen de Ejercicios

| Ejercicio | Nivel | Concepto Principal |
|-----------|-------|-------------------|
| 1-5 | Básico | Identificación, cálculo, clasificación de métricas |
| 6-11 | Intermedio | Diseño de dashboards, cohortes, funnels, documentación |
| 12-15 | Avanzado | Alertas ML, OKRs cascading, arquitectura, sistema completo |

---

**Siguiente paso**: [04-proyecto-practico/](04-proyecto-practico/) - Implementa un sistema de métricas completo con TDD
