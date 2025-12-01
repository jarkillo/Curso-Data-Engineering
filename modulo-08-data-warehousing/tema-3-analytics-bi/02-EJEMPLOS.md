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

## Ejemplo 2: Dashboard de Ventas con Python/Plotly - Nivel: Intermedio

### Contexto

**FinTech Analytics** necesita un dashboard visual para analizar sus ventas de servicios financieros. Como Data Engineer, debes crear visualizaciones interactivas usando Python y Plotly que se puedan integrar fácilmente en cualquier herramienta de BI o página web.

### Paso 1: Preparar los Datos

Primero, creamos datos de ejemplo que simulan las ventas de FinTech Analytics:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generar datos de ventas para FinTech Analytics
np.random.seed(42)

# Crear 12 meses de datos
dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')

# Productos financieros de FinTech Analytics
products = ['Préstamos Personales', 'Inversiones', 'Seguros', 'Tarjetas', 'Cuentas Premium']
channels = ['Web', 'App Móvil', 'Sucursal', 'Teléfono']
regions = ['Norte', 'Sur', 'Centro', 'Este', 'Oeste']

# Generar transacciones
n_transactions = 5000
data = {
    'date': np.random.choice(dates, n_transactions),
    'product': np.random.choice(products, n_transactions, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'channel': np.random.choice(channels, n_transactions, p=[0.4, 0.35, 0.15, 0.1]),
    'region': np.random.choice(regions, n_transactions),
    'revenue': np.random.exponential(500, n_transactions) + 100,
    'customers': np.random.randint(1, 5, n_transactions)
}

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')
df['revenue'] = df['revenue'].round(2)

print(df.head(10))
print(f"\nTotal registros: {len(df)}")
print(f"Revenue total: ${df['revenue'].sum():,.2f}")
```

### Paso 2: Crear Visualización de KPIs con Indicadores

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Calcular KPIs
total_revenue = df['revenue'].sum()
total_customers = df['customers'].sum()
avg_ticket = total_revenue / len(df)
monthly_growth = 8.5  # Simulado

# Crear figura con indicadores (gauge charts)
fig = make_subplots(
    rows=1, cols=4,
    specs=[[{"type": "indicator"}, {"type": "indicator"},
            {"type": "indicator"}, {"type": "indicator"}]],
    subplot_titles=("Revenue Total", "Clientes", "Ticket Promedio", "Crecimiento MoM")
)

# KPI 1: Revenue Total
fig.add_trace(go.Indicator(
    mode="number+delta",
    value=total_revenue,
    number={"prefix": "$", "valueformat": ",.0f"},
    delta={"reference": total_revenue * 0.92, "valueformat": ".1%"},
    title={"text": "Revenue Total"},
    domain={'row': 0, 'column': 0}
), row=1, col=1)

# KPI 2: Total Clientes
fig.add_trace(go.Indicator(
    mode="number+delta",
    value=total_customers,
    number={"valueformat": ","},
    delta={"reference": total_customers * 0.95},
    title={"text": "Clientes Totales"},
), row=1, col=2)

# KPI 3: Ticket Promedio
fig.add_trace(go.Indicator(
    mode="number+delta",
    value=avg_ticket,
    number={"prefix": "$", "valueformat": ".2f"},
    delta={"reference": avg_ticket * 0.98, "valueformat": ".1%"},
    title={"text": "Ticket Promedio"},
), row=1, col=3)

# KPI 4: Crecimiento (Gauge)
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=monthly_growth,
    number={"suffix": "%"},
    title={"text": "Crecimiento MoM"},
    gauge={
        'axis': {'range': [0, 20]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 5], 'color': "lightcoral"},
            {'range': [5, 10], 'color': "lightyellow"},
            {'range': [10, 20], 'color': "lightgreen"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 15  # Objetivo
        }
    }
), row=1, col=4)

fig.update_layout(
    title="FinTech Analytics - Dashboard de KPIs",
    height=300
)
fig.show()
```

### Paso 3: Gráfico de Tendencia de Revenue

```python
import plotly.express as px

# Agrupar por mes
monthly_revenue = df.groupby('month').agg({
    'revenue': 'sum',
    'customers': 'sum'
}).reset_index()
monthly_revenue['month'] = monthly_revenue['month'].astype(str)

# Crear gráfico de línea con área
fig = go.Figure()

# Línea principal de revenue
fig.add_trace(go.Scatter(
    x=monthly_revenue['month'],
    y=monthly_revenue['revenue'],
    mode='lines+markers',
    name='Revenue',
    line=dict(color='#2E86AB', width=3),
    marker=dict(size=10),
    fill='tozeroy',
    fillcolor='rgba(46, 134, 171, 0.2)'
))

# Línea de tendencia (promedio móvil)
monthly_revenue['trend'] = monthly_revenue['revenue'].rolling(window=3, min_periods=1).mean()
fig.add_trace(go.Scatter(
    x=monthly_revenue['month'],
    y=monthly_revenue['trend'],
    mode='lines',
    name='Tendencia (3 meses)',
    line=dict(color='#E94F37', width=2, dash='dash')
))

fig.update_layout(
    title="Tendencia de Revenue Mensual - FinTech Analytics",
    xaxis_title="Mes",
    yaxis_title="Revenue ($)",
    yaxis_tickformat="$,.0f",
    hovermode='x unified',
    template='plotly_white'
)
fig.show()
```

### Paso 4: Gráfico de Barras por Producto y Canal

```python
# Revenue por producto
product_revenue = df.groupby('product')['revenue'].sum().sort_values(ascending=True)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=product_revenue.values,
    y=product_revenue.index,
    orientation='h',
    marker_color=['#A4243B', '#D8C99B', '#D8973C', '#BD632F', '#2E86AB'],
    text=[f"${x:,.0f}" for x in product_revenue.values],
    textposition='outside'
))

fig.update_layout(
    title="Revenue por Producto - FinTech Analytics",
    xaxis_title="Revenue ($)",
    yaxis_title="Producto",
    xaxis_tickformat="$,.0f",
    template='plotly_white',
    height=400
)
fig.show()

# Revenue por canal (pie chart)
channel_revenue = df.groupby('channel')['revenue'].sum()

fig = go.Figure(data=[go.Pie(
    labels=channel_revenue.index,
    values=channel_revenue.values,
    hole=0.4,
    marker_colors=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'],
    textinfo='label+percent',
    textposition='outside'
)])

fig.update_layout(
    title="Distribución de Revenue por Canal",
    annotations=[dict(text='Por Canal', x=0.5, y=0.5, font_size=16, showarrow=False)]
)
fig.show()
```

### Paso 5: Dashboard Completo Combinado

```python
from plotly.subplots import make_subplots

# Preparar datos
monthly_data = df.groupby('month')['revenue'].sum().reset_index()
monthly_data['month'] = monthly_data['month'].astype(str)
product_data = df.groupby('product')['revenue'].sum().sort_values(ascending=False)
channel_data = df.groupby('channel')['revenue'].sum()
region_data = df.groupby('region')['revenue'].sum()

# Crear dashboard con subplots
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Tendencia de Revenue Mensual",
        "Revenue por Producto",
        "Distribución por Canal",
        "Revenue por Región"
    ),
    specs=[
        [{"type": "scatter"}, {"type": "bar"}],
        [{"type": "pie"}, {"type": "bar"}]
    ]
)

# 1. Tendencia mensual (línea)
fig.add_trace(go.Scatter(
    x=monthly_data['month'],
    y=monthly_data['revenue'],
    mode='lines+markers',
    name='Revenue Mensual',
    line=dict(color='#2E86AB', width=2),
    fill='tozeroy'
), row=1, col=1)

# 2. Por producto (barras horizontales)
fig.add_trace(go.Bar(
    x=product_data.values,
    y=product_data.index,
    orientation='h',
    name='Por Producto',
    marker_color='#A23B72'
), row=1, col=2)

# 3. Por canal (pie)
fig.add_trace(go.Pie(
    labels=channel_data.index,
    values=channel_data.values,
    name='Por Canal',
    hole=0.3
), row=2, col=1)

# 4. Por región (barras)
fig.add_trace(go.Bar(
    x=region_data.index,
    y=region_data.values,
    name='Por Región',
    marker_color='#F18F01'
), row=2, col=2)

fig.update_layout(
    title_text="FinTech Analytics - Dashboard de Ventas Completo",
    height=700,
    showlegend=False,
    template='plotly_white'
)

# Formatear ejes
fig.update_yaxes(tickformat="$,.0f", row=1, col=1)
fig.update_xaxes(tickformat="$,.0f", row=1, col=2)
fig.update_yaxes(tickformat="$,.0f", row=2, col=2)

fig.show()

# Guardar como HTML interactivo
fig.write_html("fintech_dashboard.html")
print("Dashboard guardado como 'fintech_dashboard.html'")
```

### Interpretación

Este dashboard con Plotly permite:
- **Visualizar KPIs en tiempo real** con indicadores interactivos
- **Analizar tendencias** con gráficos de línea y promedios móviles
- **Comparar productos/canales** con gráficos de barras y pie
- **Exportar como HTML** para compartir con stakeholders
- **Interactuar** con hover, zoom y filtros nativos de Plotly

---

## Ejemplo 3: Operaciones OLAP con Python - Nivel: Intermedio

### Contexto

**RestaurantData Co.** tiene un Data Warehouse con ventas de su red de restaurantes. El equipo de análisis necesita explorar los datos usando operaciones OLAP (drill-down, roll-up, slice, dice, pivot) para responder preguntas de negocio dinámicamente.

### Paso 1: Crear el Cubo de Datos

```python
import pandas as pd
import numpy as np

# Crear datos de ventas para RestaurantData Co.
np.random.seed(42)

# Dimensiones
years = [2023, 2024]
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
categories = ['Entrantes', 'Platos Principales', 'Postres', 'Bebidas']
regions = ['Norte', 'Sur', 'Centro', 'Este']
restaurants = {
    'Norte': ['Rest-N1', 'Rest-N2', 'Rest-N3'],
    'Sur': ['Rest-S1', 'Rest-S2'],
    'Centro': ['Rest-C1', 'Rest-C2', 'Rest-C3', 'Rest-C4'],
    'Este': ['Rest-E1', 'Rest-E2']
}

# Generar datos
data = []
for year in years:
    for q_idx, quarter in enumerate(quarters):
        for m_idx in range(3):  # 3 meses por trimestre
            month = months[q_idx * 3 + m_idx]
            for region in regions:
                for restaurant in restaurants[region]:
                    for category in categories:
                        # Ventas base con variación
                        base_sales = np.random.randint(5000, 20000)
                        # Más ventas en Q4 (temporada alta)
                        if quarter == 'Q4':
                            base_sales *= 1.3
                        # Centro tiene más ventas
                        if region == 'Centro':
                            base_sales *= 1.2

                        data.append({
                            'year': year,
                            'quarter': quarter,
                            'month': month,
                            'region': region,
                            'restaurant': restaurant,
                            'category': category,
                            'sales': round(base_sales),
                            'orders': np.random.randint(100, 500),
                            'customers': np.random.randint(80, 400)
                        })

df = pd.DataFrame(data)
print("Cubo de datos creado:")
print(f"Dimensiones: {df.shape}")
print(f"\nEjemplo de registros:")
print(df.head(10))
```

### Paso 2: DRILL-DOWN (De lo general a lo específico)

```python
def drill_down(df: pd.DataFrame, levels: list, metric: str = 'sales') -> pd.DataFrame:
    """
    Drill-down: Navegar de lo general a lo específico.

    Ejemplo: Total → Por Región → Por Restaurante → Por Categoría
    """
    results = []

    for i in range(len(levels) + 1):
        if i == 0:
            # Nivel más alto: Total
            total = df[metric].sum()
            results.append({
                'level': 'TOTAL',
                'detail': 'Todas las ventas',
                metric: total
            })
        else:
            # Drill-down por cada nivel
            current_levels = levels[:i]
            grouped = df.groupby(current_levels)[metric].sum().reset_index()
            for _, row in grouped.iterrows():
                detail = ' > '.join([str(row[l]) for l in current_levels])
                results.append({
                    'level': f'Nivel {i}: {current_levels[-1]}',
                    'detail': detail,
                    metric: row[metric]
                })

    return pd.DataFrame(results)

# Ejemplo: Drill-down de Total → Región → Restaurante
print("=" * 60)
print("DRILL-DOWN: Total → Región → Restaurante")
print("=" * 60)

# Nivel 0: Total
print(f"\n🔹 NIVEL 0 - TOTAL")
print(f"   Ventas totales: ${df['sales'].sum():,}")

# Nivel 1: Por Región
print(f"\n🔹 NIVEL 1 - POR REGIÓN")
by_region = df.groupby('region')['sales'].sum().sort_values(ascending=False)
for region, sales in by_region.items():
    print(f"   {region}: ${sales:,}")

# Nivel 2: Por Restaurante (drill-down en región 'Centro')
print(f"\n🔹 NIVEL 2 - DRILL-DOWN EN 'CENTRO'")
centro_df = df[df['region'] == 'Centro']
by_restaurant = centro_df.groupby('restaurant')['sales'].sum().sort_values(ascending=False)
for rest, sales in by_restaurant.items():
    print(f"   {rest}: ${sales:,}")

# Nivel 3: Por Categoría (drill-down en restaurante 'Rest-C1')
print(f"\n🔹 NIVEL 3 - DRILL-DOWN EN 'REST-C1'")
rest_c1 = df[df['restaurant'] == 'Rest-C1']
by_category = rest_c1.groupby('category')['sales'].sum().sort_values(ascending=False)
for cat, sales in by_category.items():
    print(f"   {cat}: ${sales:,}")
```

### Paso 3: ROLL-UP (De lo específico a lo general)

```python
def roll_up(df: pd.DataFrame, from_level: str, to_level: str, metric: str = 'sales') -> pd.DataFrame:
    """
    Roll-up: Agregar datos a un nivel superior.

    Ejemplo: Restaurante → Región → Total
    """
    print(f"\n{'=' * 60}")
    print(f"ROLL-UP: {from_level} → {to_level}")
    print(f"{'=' * 60}")

    if from_level == 'restaurant' and to_level == 'region':
        # Mostrar detalle por restaurante
        print(f"\n📊 Detalle por Restaurante (nivel inferior):")
        by_rest = df.groupby(['region', 'restaurant'])[metric].sum()
        for (region, rest), sales in by_rest.items():
            print(f"   {region} > {rest}: ${sales:,}")

        # Roll-up a región
        print(f"\n📊 Roll-up a Región:")
        by_region = df.groupby('region')[metric].sum().sort_values(ascending=False)
        for region, sales in by_region.items():
            print(f"   {region}: ${sales:,}")

        return by_region.reset_index()

    elif to_level == 'total':
        print(f"\n📊 Roll-up a TOTAL:")
        total = df[metric].sum()
        print(f"   TOTAL: ${total:,}")
        return pd.DataFrame({'total': [total]})

# Ejemplo: Roll-up de restaurante a región
roll_up(df, 'restaurant', 'region')

# Roll-up de región a total
roll_up(df, 'region', 'total')
```

### Paso 4: SLICE (Filtrar por una dimensión)

```python
def slice_cube(df: pd.DataFrame, dimension: str, value: str) -> pd.DataFrame:
    """
    Slice: Filtrar el cubo por UN valor de UNA dimensión.

    Ejemplo: Obtener solo datos del año 2024
    """
    sliced = df[df[dimension] == value].copy()

    print(f"\n{'=' * 60}")
    print(f"SLICE: {dimension} = '{value}'")
    print(f"{'=' * 60}")
    print(f"\n📊 Registros antes del slice: {len(df):,}")
    print(f"📊 Registros después del slice: {len(sliced):,}")
    print(f"📊 Ventas en el slice: ${sliced['sales'].sum():,}")

    return sliced

# Ejemplo 1: Slice por año
slice_2024 = slice_cube(df, 'year', 2024)

# Ejemplo 2: Slice por región
slice_centro = slice_cube(df, 'region', 'Centro')

# Ejemplo 3: Slice por categoría
slice_postres = slice_cube(df, 'category', 'Postres')

# Analizar el slice de postres por región
print("\n📊 Ventas de Postres por Región:")
postres_by_region = slice_postres.groupby('region')['sales'].sum().sort_values(ascending=False)
for region, sales in postres_by_region.items():
    print(f"   {region}: ${sales:,}")
```

### Paso 5: DICE (Filtrar por múltiples dimensiones)

```python
def dice_cube(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Dice: Filtrar por MÚLTIPLES valores de MÚLTIPLES dimensiones.

    Ejemplo: Q3 y Q4 de 2024, solo regiones Norte y Centro
    """
    diced = df.copy()

    print(f"\n{'=' * 60}")
    print(f"DICE: Múltiples filtros")
    print(f"{'=' * 60}")

    for dimension, values in filters.items():
        if isinstance(values, list):
            diced = diced[diced[dimension].isin(values)]
        else:
            diced = diced[diced[dimension] == values]
        print(f"   ✓ {dimension} IN {values}")

    print(f"\n📊 Registros originales: {len(df):,}")
    print(f"📊 Registros después del dice: {len(diced):,}")
    print(f"📊 Ventas en el subcubo: ${diced['sales'].sum():,}")

    return diced

# Ejemplo: Subcubo con Q3 y Q4 de 2024, regiones Norte y Centro
filters = {
    'year': 2024,
    'quarter': ['Q3', 'Q4'],
    'region': ['Norte', 'Centro']
}

subcubo = dice_cube(df, filters)

# Analizar el subcubo
print("\n📊 Análisis del subcubo:")
print("\nPor Trimestre:")
print(subcubo.groupby('quarter')['sales'].sum())
print("\nPor Región:")
print(subcubo.groupby('region')['sales'].sum())
print("\nPor Categoría:")
print(subcubo.groupby('category')['sales'].sum())
```

### Paso 6: PIVOT (Rotar el cubo)

```python
def pivot_cube(df: pd.DataFrame, index: str, columns: str, values: str = 'sales',
               aggfunc: str = 'sum') -> pd.DataFrame:
    """
    Pivot: Cambiar la orientación del análisis.

    Ejemplo: Regiones en filas, Categorías en columnas
    """
    print(f"\n{'=' * 60}")
    print(f"PIVOT: {index} (filas) x {columns} (columnas)")
    print(f"{'=' * 60}")

    pivoted = pd.pivot_table(
        df,
        values=values,
        index=index,
        columns=columns,
        aggfunc=aggfunc,
        fill_value=0
    )

    # Agregar totales
    pivoted['TOTAL'] = pivoted.sum(axis=1)
    pivoted.loc['TOTAL'] = pivoted.sum()

    return pivoted

# Pivot 1: Regiones x Categorías
print("\n📊 Pivot: Regiones x Categorías")
pivot1 = pivot_cube(df, 'region', 'category')
print(pivot1.to_string())

# Pivot 2: Trimestres x Regiones
print("\n📊 Pivot: Trimestres x Regiones")
pivot2 = pivot_cube(df, 'quarter', 'region')
print(pivot2.to_string())

# Pivot 3: Años x Trimestres (para comparar YoY)
print("\n📊 Pivot: Años x Trimestres (comparación interanual)")
pivot3 = pivot_cube(df, 'year', 'quarter')
print(pivot3.to_string())

# Calcular crecimiento YoY
if 2023 in df['year'].values and 2024 in df['year'].values:
    print("\n📊 Crecimiento Year-over-Year:")
    for q in quarters:
        sales_2023 = df[(df['year'] == 2023) & (df['quarter'] == q)]['sales'].sum()
        sales_2024 = df[(df['year'] == 2024) & (df['quarter'] == q)]['sales'].sum()
        growth = ((sales_2024 - sales_2023) / sales_2023) * 100
        print(f"   {q}: {growth:+.1f}%")
```

### Interpretación

Este ejemplo demuestra las 5 operaciones OLAP fundamentales:

| Operación | Uso | Ejemplo de Negocio |
|-----------|-----|-------------------|
| **Drill-down** | De general a específico | "¿Qué restaurante en Centro vende más postres?" |
| **Roll-up** | Agregar a nivel superior | "¿Cuál es el total por región?" |
| **Slice** | Filtrar por una dimensión | "Muéstrame solo datos de 2024" |
| **Dice** | Filtrar por múltiples dimensiones | "Q3-Q4 de Norte y Centro" |
| **Pivot** | Cambiar perspectiva | "Quiero categorías en columnas" |

Estas operaciones permiten a los analistas explorar datos de forma interactiva sin necesidad de escribir queries complejos cada vez.

---

## Ejemplo 4: Dashboard Interactivo con Streamlit - Nivel: Avanzado

### Contexto

**CloudAPI Systems** necesita un dashboard interactivo para que el equipo de producto analice el uso de su API en tiempo real. Como Data Engineer, debes crear una aplicación Streamlit completa con filtros, gráficos y métricas actualizables.

### Paso 1: Estructura del Proyecto

```
cloudapi_dashboard/
├── app.py              # Aplicación principal Streamlit
├── data_generator.py   # Generador de datos de ejemplo
├── requirements.txt    # Dependencias
└── README.md           # Documentación
```

### Paso 2: Generador de Datos (data_generator.py)

```python
# data_generator.py
"""
Generador de datos de uso de API para CloudAPI Systems.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_api_usage_data(days: int = 90) -> pd.DataFrame:
    """
    Genera datos simulados de uso de API.

    Args:
        days: Número de días de datos a generar

    Returns:
        DataFrame con datos de uso de API
    """
    np.random.seed(42)

    # Generar fechas
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')

    # Endpoints de la API
    endpoints = [
        '/api/v1/users',
        '/api/v1/transactions',
        '/api/v1/reports',
        '/api/v1/analytics',
        '/api/v1/webhooks'
    ]

    # Planes de clientes
    plans = ['Free', 'Starter', 'Professional', 'Enterprise']

    # Regiones
    regions = ['US-East', 'US-West', 'EU-West', 'APAC']

    # Generar datos
    n_records = len(dates) * 10  # 10 registros por hora aprox

    data = {
        'timestamp': np.random.choice(dates, n_records),
        'endpoint': np.random.choice(endpoints, n_records, p=[0.35, 0.30, 0.15, 0.12, 0.08]),
        'plan': np.random.choice(plans, n_records, p=[0.40, 0.30, 0.20, 0.10]),
        'region': np.random.choice(regions, n_records, p=[0.35, 0.25, 0.25, 0.15]),
        'response_time_ms': np.random.exponential(100, n_records) + 20,
        'status_code': np.random.choice([200, 201, 400, 401, 404, 500], n_records,
                                        p=[0.85, 0.05, 0.04, 0.03, 0.02, 0.01]),
        'request_size_kb': np.random.exponential(5, n_records) + 1,
        'response_size_kb': np.random.exponential(10, n_records) + 2
    }

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['is_error'] = df['status_code'] >= 400
    df['response_time_ms'] = df['response_time_ms'].round(2)

    return df.sort_values('timestamp').reset_index(drop=True)


def generate_customer_data(n_customers: int = 500) -> pd.DataFrame:
    """
    Genera datos de clientes para CloudAPI Systems.
    """
    np.random.seed(42)

    plans = ['Free', 'Starter', 'Professional', 'Enterprise']
    regions = ['US-East', 'US-West', 'EU-West', 'APAC']

    data = {
        'customer_id': [f'CUST-{i:04d}' for i in range(1, n_customers + 1)],
        'plan': np.random.choice(plans, n_customers, p=[0.40, 0.30, 0.20, 0.10]),
        'region': np.random.choice(regions, n_customers, p=[0.35, 0.25, 0.25, 0.15]),
        'monthly_api_calls': np.random.exponential(10000, n_customers).astype(int),
        'mrr': np.random.choice([0, 29, 99, 499], n_customers, p=[0.40, 0.30, 0.20, 0.10]),
        'signup_date': pd.date_range(end=datetime.now(), periods=n_customers, freq='D'),
        'churn_risk': np.random.uniform(0, 1, n_customers).round(2)
    }

    return pd.DataFrame(data)


if __name__ == "__main__":
    # Generar y guardar datos
    api_data = generate_api_usage_data()
    customer_data = generate_customer_data()

    print(f"API Usage: {len(api_data)} registros")
    print(f"Customers: {len(customer_data)} registros")

    api_data.to_csv('api_usage.csv', index=False)
    customer_data.to_csv('customers.csv', index=False)
```

### Paso 3: Aplicación Streamlit Completa (app.py)

```python
# app.py
"""
Dashboard interactivo de CloudAPI Systems con Streamlit.

Ejecutar con: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Importar generador de datos
from data_generator import generate_api_usage_data, generate_customer_data

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="CloudAPI Systems - Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CARGA DE DATOS (con cache para performance)
# ============================================================
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_data():
    """Carga y cachea los datos."""
    api_data = generate_api_usage_data(days=90)
    customer_data = generate_customer_data(n_customers=500)
    return api_data, customer_data

api_df, customer_df = load_data()

# ============================================================
# SIDEBAR - FILTROS
# ============================================================
st.sidebar.title("🎛️ Filtros")

# Filtro de fechas
st.sidebar.subheader("📅 Rango de Fechas")
min_date = api_df['timestamp'].min().date()
max_date = api_df['timestamp'].max().date()

date_range = st.sidebar.date_input(
    "Seleccionar rango",
    value=(max_date - timedelta(days=30), max_date),
    min_value=min_date,
    max_value=max_date
)

# Filtro de endpoints
st.sidebar.subheader("🔗 Endpoints")
all_endpoints = api_df['endpoint'].unique().tolist()
selected_endpoints = st.sidebar.multiselect(
    "Seleccionar endpoints",
    options=all_endpoints,
    default=all_endpoints
)

# Filtro de planes
st.sidebar.subheader("💳 Planes")
all_plans = api_df['plan'].unique().tolist()
selected_plans = st.sidebar.multiselect(
    "Seleccionar planes",
    options=all_plans,
    default=all_plans
)

# Filtro de regiones
st.sidebar.subheader("🌍 Regiones")
all_regions = api_df['region'].unique().tolist()
selected_regions = st.sidebar.multiselect(
    "Seleccionar regiones",
    options=all_regions,
    default=all_regions
)

# ============================================================
# APLICAR FILTROS
# ============================================================
filtered_df = api_df[
    (api_df['timestamp'].dt.date >= date_range[0]) &
    (api_df['timestamp'].dt.date <= date_range[1]) &
    (api_df['endpoint'].isin(selected_endpoints)) &
    (api_df['plan'].isin(selected_plans)) &
    (api_df['region'].isin(selected_regions))
]

# ============================================================
# HEADER
# ============================================================
st.title("🚀 CloudAPI Systems - API Analytics Dashboard")
st.markdown(f"**Período:** {date_range[0]} a {date_range[1]} | "
            f"**Registros:** {len(filtered_df):,}")

# ============================================================
# KPIs PRINCIPALES
# ============================================================
st.header("📊 Métricas Clave")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_requests = len(filtered_df)
    st.metric(
        label="Total Requests",
        value=f"{total_requests:,}",
        delta=f"+{np.random.randint(5, 15)}% vs período anterior"
    )

with col2:
    avg_response = filtered_df['response_time_ms'].mean()
    st.metric(
        label="Avg Response Time",
        value=f"{avg_response:.1f} ms",
        delta=f"-{np.random.randint(2, 8)}ms"
    )

with col3:
    error_rate = (filtered_df['is_error'].sum() / len(filtered_df)) * 100
    st.metric(
        label="Error Rate",
        value=f"{error_rate:.2f}%",
        delta=f"-{np.random.uniform(0.1, 0.5):.2f}%"
    )

with col4:
    p99_latency = filtered_df['response_time_ms'].quantile(0.99)
    st.metric(
        label="P99 Latency",
        value=f"{p99_latency:.0f} ms",
        delta=f"-{np.random.randint(5, 15)}ms"
    )

with col5:
    uptime = 100 - error_rate
    st.metric(
        label="Uptime",
        value=f"{uptime:.2f}%",
        delta="↑ 0.1%"
    )

# ============================================================
# GRÁFICOS PRINCIPALES
# ============================================================
st.header("📈 Análisis de Tráfico")

# Fila 1: Requests por hora y distribución por endpoint
col1, col2 = st.columns(2)

with col1:
    # Requests por hora
    hourly_requests = filtered_df.groupby(
        filtered_df['timestamp'].dt.floor('H')
    ).size().reset_index(name='requests')

    fig = px.line(
        hourly_requests,
        x='timestamp',
        y='requests',
        title='Requests por Hora',
        labels={'timestamp': 'Fecha/Hora', 'requests': 'Número de Requests'}
    )
    fig.update_traces(fill='tozeroy', line_color='#2E86AB')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Distribución por endpoint
    endpoint_dist = filtered_df.groupby('endpoint').size().reset_index(name='count')

    fig = px.pie(
        endpoint_dist,
        values='count',
        names='endpoint',
        title='Distribución por Endpoint',
        hole=0.4
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# Fila 2: Response time por endpoint y errores por hora
col1, col2 = st.columns(2)

with col1:
    # Response time por endpoint (box plot)
    fig = px.box(
        filtered_df,
        x='endpoint',
        y='response_time_ms',
        title='Response Time por Endpoint',
        labels={'endpoint': 'Endpoint', 'response_time_ms': 'Response Time (ms)'}
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Errores por hora
    error_df = filtered_df[filtered_df['is_error']]
    hourly_errors = error_df.groupby(
        error_df['timestamp'].dt.floor('H')
    ).size().reset_index(name='errors')

    fig = px.bar(
        hourly_errors,
        x='timestamp',
        y='errors',
        title='Errores por Hora',
        labels={'timestamp': 'Fecha/Hora', 'errors': 'Número de Errores'},
        color_discrete_sequence=['#E94F37']
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ANÁLISIS POR SEGMENTO
# ============================================================
st.header("🔍 Análisis por Segmento")

tab1, tab2, tab3 = st.tabs(["Por Plan", "Por Región", "Por Status Code"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        plan_usage = filtered_df.groupby('plan').agg({
            'timestamp': 'count',
            'response_time_ms': 'mean'
        }).reset_index()
        plan_usage.columns = ['Plan', 'Requests', 'Avg Response Time']

        fig = px.bar(
            plan_usage,
            x='Plan',
            y='Requests',
            title='Requests por Plan',
            color='Plan',
            text='Requests'
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            plan_usage,
            x='Plan',
            y='Avg Response Time',
            title='Response Time Promedio por Plan',
            color='Plan',
            text=plan_usage['Avg Response Time'].round(1)
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        region_usage = filtered_df.groupby('region').size().reset_index(name='Requests')

        fig = px.bar(
            region_usage,
            x='region',
            y='Requests',
            title='Requests por Región',
            color='region'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Heatmap: Hora del día x Región
        heatmap_data = filtered_df.groupby(['hour', 'region']).size().unstack(fill_value=0)

        fig = px.imshow(
            heatmap_data.T,
            title='Heatmap: Hora del Día x Región',
            labels=dict(x="Hora", y="Región", color="Requests"),
            aspect="auto"
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    status_dist = filtered_df.groupby('status_code').size().reset_index(name='count')
    status_dist['status_code'] = status_dist['status_code'].astype(str)

    fig = px.bar(
        status_dist,
        x='status_code',
        y='count',
        title='Distribución de Status Codes',
        color='status_code',
        text='count'
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TABLA DE DATOS
# ============================================================
st.header("📋 Datos Detallados")

with st.expander("Ver datos filtrados"):
    st.dataframe(
        filtered_df[['timestamp', 'endpoint', 'plan', 'region',
                     'status_code', 'response_time_ms']].head(1000),
        use_container_width=True
    )

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
**CloudAPI Systems Dashboard** | Creado con Streamlit y Plotly
- 📊 Dashboard actualizado cada hora
- 🔗 Datos simulados para demostración
- 📚 Parte del curso de Data Engineering
""")
```

### Paso 4: Requirements (requirements.txt)

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
```

### Paso 5: Ejecutar la Aplicación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el dashboard
streamlit run app.py

# El dashboard se abrirá en http://localhost:8501
```

### Características del Dashboard

1. **Filtros Interactivos**: Sidebar con filtros de fecha, endpoint, plan y región
2. **KPIs en Tiempo Real**: Métricas clave con deltas vs período anterior
3. **Gráficos Dinámicos**: Se actualizan automáticamente al cambiar filtros
4. **Múltiples Visualizaciones**: Líneas, barras, pie, box plots, heatmaps
5. **Tabs para Segmentos**: Análisis por plan, región y status code
6. **Tabla de Datos**: Acceso a los datos filtrados

### Interpretación

Este dashboard con Streamlit permite:
- **Explorar datos interactivamente** con filtros en tiempo real
- **Identificar patrones** de uso por hora, región y plan
- **Detectar anomalías** en errores y latencia
- **Compartir análisis** como aplicación web accesible
- **Extender fácilmente** con nuevas métricas y visualizaciones

---

## Resumen de Ejemplos

| Ejemplo | Nivel | Concepto Principal | Tecnología | Empresa Ficticia |
|---------|-------|-------------------|------------|------------------|
| 1 | Básico | Definición de KPIs | SQL + Python | RestaurantData Co. |
| 2 | Intermedio | Dashboard de ventas | Python + Plotly | FinTech Analytics |
| 3 | Intermedio | Operaciones OLAP | Python + Pandas | RestaurantData Co. |
| 4 | Avanzado | Dashboard interactivo | Streamlit + Plotly | CloudAPI Systems |

Estos ejemplos muestran la progresión desde KPIs básicos en SQL hasta aplicaciones web interactivas completas con Streamlit.

**Habilidades desarrolladas:**
- Definir y calcular KPIs relevantes para el negocio
- Crear visualizaciones interactivas con Plotly
- Aplicar operaciones OLAP para explorar datos multidimensionales
- Construir dashboards web completos con Streamlit

---

**Siguiente paso**: [03-EJERCICIOS.md](03-EJERCICIOS.md) - Practica diseñando tus propios KPIs y dashboards
