# Proyecto Práctico: Dashboard de Analytics y BI

Sistema completo de Analytics y Business Intelligence con dashboard interactivo Streamlit conectado al Data Warehouse del Tema 1.

## Objetivos

- Visualizar KPIs de negocio en tiempo real
- Analizar ventas por producto, categoría y tiempo
- Segmentar clientes y calcular métricas RFM
- Evaluar performance del equipo comercial
- Exportar métricas a formatos compatibles con herramientas BI

## Conceptos Clave

### Dashboard Interactivo

El dashboard incluye 4 secciones principales:

| Sección | Descripción | Visualizaciones |
|---------|-------------|-----------------|
| **Overview** | KPIs ejecutivos y vista general | Métricas, tendencias, distribución |
| **Análisis de Ventas** | Detalle por producto y tiempo | Series temporales, top productos, treemap |
| **Análisis de Clientes** | Segmentación y valor | RFM, distribución, top clientes |
| **Performance Vendedores** | Métricas del equipo | Rankings, evolución, comisiones |

### KPIs Implementados

| KPI | Descripción | Fórmula |
|-----|-------------|---------|
| Revenue Total | Suma de ventas netas | `SUM(monto_neto)` |
| Ticket Promedio | Venta promedio por transacción | `Revenue / Transacciones` |
| AOV | Average Order Value | `Revenue / Orders` |
| CAC | Customer Acquisition Cost | `Marketing Spend / New Customers` |
| LTV | Customer Lifetime Value | `AOV * Frequency * Lifespan` |

### Análisis RFM

El módulo de análisis de clientes incluye segmentación RFM:
- **Recency**: Días desde la última compra
- **Frequency**: Número de transacciones
- **Monetary**: Valor total de compras

## Estructura del Proyecto

```
04-proyecto-practico/
├── dashboard/                    # Aplicación Streamlit
│   ├── __init__.py
│   ├── app.py                   # Aplicación principal
│   ├── database.py              # Conexión al DWH
│   └── queries.py               # Consultas SQL
├── src/                         # Módulos de análisis
│   ├── __init__.py
│   ├── kpis.py                  # Cálculo de KPIs
│   ├── cohorts.py               # Análisis de cohortes
│   ├── anomaly_detection.py     # Detección de anomalías
│   └── exporters.py             # Exportación a JSON/CSV
├── tests/                       # Tests unitarios
│   ├── test_kpis.py
│   ├── test_cohorts.py
│   ├── test_anomaly_detection.py
│   └── test_exporters.py
├── README.md
├── requirements.txt
├── CHANGELOG.md
└── .gitignore
```

## Instalación

### Requisitos Previos

1. **Python 3.11+** instalado
2. **Data Warehouse** del Tema 1 creado (ejecutar primero ese proyecto)

### Pasos de Instalación

```bash
# 1. Navegar al directorio del proyecto
cd modulo-08-data-warehousing/tema-3-analytics-bi/04-proyecto-practico

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 3. Activar entorno (Windows CMD)
.\venv\Scripts\activate.bat

# 3. Activar entorno (Linux/Mac)
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

### Verificar Data Warehouse

El dashboard requiere el archivo `data_warehouse.db` del Tema 1:

```bash
# Si no existe, ejecutar primero:
cd ../tema-1-dimensional-modeling/04-proyecto-practico
python main.py

# Verificar que existe:
ls output/data_warehouse.db
```

## Ejecutar el Dashboard

```bash
# Desde el directorio 04-proyecto-practico
cd dashboard
streamlit run app.py

# El dashboard se abrirá en: http://localhost:8501
```

### Opciones de Ejecución

```bash
# Puerto personalizado
streamlit run dashboard/app.py --server.port 8080

# Sin abrir navegador automáticamente
streamlit run dashboard/app.py --server.headless true

# Modo desarrollo (recarga automática)
streamlit run dashboard/app.py --server.runOnSave true
```

## Ejecutar Tests

```bash
# Tests con cobertura
pytest -v --cov=src --cov-report=term-missing --cov-report=html

# Solo tests del dashboard
pytest tests/ -v

# Tests de un módulo específico
pytest tests/test_kpis.py -v

# Cobertura mínima 80%
pytest --cov=src --cov-fail-under=80
```

## Funciones Implementadas

### Módulo dashboard/queries.py

```python
from dashboard.queries import (
    get_kpis_principales,
    get_ventas_por_mes,
    get_ventas_por_categoria,
    get_top_productos,
    get_clientes_por_segmento,
    get_performance_vendedores
)

# Obtener KPIs principales
kpis = get_kpis_principales()
print(f"Revenue: ${kpis['total_revenue']:,.2f}")

# Top productos
df_top = get_top_productos(limit=10, categoria='Electrónica')
print(df_top)
```

### Módulo src/kpis.py

```python
from src.kpis import calculate_aov, calculate_cac, calculate_ltv

# Calcular AOV
result = calculate_aov(total_revenue=10000.0, total_orders=200)
print(f"AOV: ${result.value:.2f}")  # AOV: $50.00

# Calcular LTV
result = calculate_ltv(
    avg_order_value=50.0,
    purchase_frequency=4.0,
    customer_lifespan=3.0,
    gross_margin=0.3
)
print(f"LTV: ${result.value:.2f}")  # LTV: $180.00
```

### Módulo src/cohorts.py

```python
from datetime import date
from src.cohorts import CohortAnalysis, UserEvent

# Crear eventos
events = [
    UserEvent(user_id=1, event_date=date(2024, 1, 1), event_type="signup"),
    UserEvent(user_id=1, event_date=date(2024, 1, 8), event_type="login"),
    # ... más eventos
]

# Análisis de cohortes
analysis = CohortAnalysis.from_events(events, retention_days=[7, 14, 30])
retention = analysis.get_retention_matrix()
```

## Visualizaciones del Dashboard

### 1. Overview (10 visualizaciones)
- 5 métricas KPI con indicadores
- Gráfico de tendencia mensual (línea con área)
- Gráfico de pie por categoría
- Gráfico de barras por región
- Gráfico de barras de transacciones

### 2. Análisis de Ventas (4 visualizaciones)
- Series temporales de ventas diarias
- Top 10 productos (barras horizontales)
- Treemap de subcategorías
- Heatmap día de semana vs mes

### 3. Análisis de Clientes (4 visualizaciones)
- Distribución por segmento (pie)
- Revenue por segmento (barras)
- Scatter plot RFM
- Histograma de recency

### 4. Performance Vendedores (4 visualizaciones)
- Ranking de vendedores (barras)
- Ventas por región (barras con color)
- Tabla de performance detallada
- Evolución mensual (líneas)

**Total: 22+ visualizaciones interactivas**

## Troubleshooting

### Error: Data Warehouse no encontrado

```
⚠️ Data Warehouse no encontrado
```

**Solución:** Ejecutar primero el proyecto del Tema 1:

```bash
cd ../tema-1-dimensional-modeling/04-proyecto-practico
python main.py
```

### Error: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'streamlit'
```

**Solución:** Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Error: Puerto en uso

```
Port 8501 is in use
```

**Solución:** Usar otro puerto:

```bash
streamlit run dashboard/app.py --server.port 8502
```

### Error: Conexión a base de datos

```
sqlite3.OperationalError: unable to open database file
```

**Solución:** Verificar que la ruta al DWH es correcta y el archivo existe.

## Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.11+ | Lenguaje principal |
| Streamlit | 1.28+ | Framework de dashboard |
| Plotly | 5.18+ | Visualizaciones interactivas |
| Pandas | 2.0+ | Procesamiento de datos |
| SQLite | 3 | Base de datos del DWH |
| pytest | 8.0+ | Testing |

## Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md) - Conceptos de Analytics y BI
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - Ejemplos prácticos con Plotly
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - Ejercicios con soluciones
- [Streamlit Docs](https://docs.streamlit.io/) - Documentación oficial
- [Plotly Docs](https://plotly.com/python/) - Documentación de Plotly

## Licencia

Material del Master en Ingeniería de Datos con IA.
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md)
