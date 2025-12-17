# 📊 Proyecto Práctico: Sistema de Monitoreo de Ventas E-Commerce

**Nivel**: Principiante-Intermedio
**Tiempo estimado**: 3-4 horas
**Prerequisitos**: Haber completado Tema 1 (Teoría, Ejemplos y Ejercicios)

---

## 🎯 Objetivo

Crear un **pipeline ETL completo con Apache Airflow** que procesa datos de ventas diarias de un e-commerce, detecta anomalías y genera reportes automáticos.

Este proyecto consolida todos los conceptos del Tema 1:
- ✅ Creación de DAGs
- ✅ PythonOperator y BashOperator
- ✅ Dependencias secuenciales y paralelas
- ✅ Validación de datos
- ✅ Manejo de errores
- ✅ Pipeline ETL real

---

## 📦 Descripción del Proyecto

### Contexto Empresarial

Trabajas como **Data Engineer** en **CloudMart**, un e-commerce de productos tecnológicos. El equipo de ventas necesita:

1. **Reportes automáticos** cada mañana con las ventas del día anterior
2. **Alertas** si las ventas caen más del 30% respecto al promedio
3. **Métricas clave**: Total de ventas, ticket promedio, top 5 productos
4. **Historial** de reportes para análisis posterior

### Pipeline Propuesto

```
┌──────────────┐
│ 1. EXTRAER   │  Leer CSV de ventas del día anterior
└──────┬───────┘
       │
┌──────▼───────┐
│ 2. VALIDAR   │  Verificar integridad de datos
└──────┬───────┘
       │
┌──────▼───────┐
│ 3. TRANSFORMAR│ Calcular métricas (total, promedio, top productos)
└──────┬───────┘
       │
       ├─────────────────────┬─────────────────────┐
       │                     │                     │
┌──────▼───────┐  ┌─────────▼────────┐  ┌────────▼─────────┐
│ 4a. DETECTAR │  │ 4b. GENERAR      │  │ 4c. GENERAR      │
│    ANOMALÍAS │  │     REPORTE CSV  │  │     REPORTE TXT  │
└──────┬───────┘  └─────────┬────────┘  └────────┬─────────┘
       │                     │                     │
       └─────────────────────┴─────────────────────┘
                              │
                     ┌────────▼─────────┐
                     │ 5. NOTIFICAR     │  Simular envío de email
                     └──────────────────┘
```

---

## 📂 Estructura del Proyecto

```
proyecto-practico/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias
├── src/                               # Código fuente (funciones puras)
│   ├── __init__.py
│   ├── extraccion.py                 # Funciones de extracción de datos
│   ├── validacion.py                 # Funciones de validación
│   ├── transformacion.py             # Funciones de transformación
│   ├── deteccion_anomalias.py        # Detección de caídas en ventas
│   ├── carga.py                      # Guardado de reportes
│   └── notificaciones.py             # Simulación de notificaciones
├── tests/                             # Tests unitarios (TDD)
│   ├── __init__.py
│   ├── test_extraccion.py
│   ├── test_validacion.py
│   ├── test_transformacion.py
│   ├── test_deteccion_anomalias.py
│   ├── test_carga.py
│   └── test_notificaciones.py
├── data/
│   ├── input/                        # CSVs de ventas (simulados)
│   │   ├── ventas_2025_10_01.csv
│   │   ├── ventas_2025_10_02.csv
│   │   └── ...
│   └── output/                       # Reportes generados
│       ├── reporte_2025_10_01.csv
│       ├── reporte_2025_10_01.txt
│       └── ...
└── dags/
    └── dag_pipeline_ventas.py        # DAG principal de Airflow
```

---

## 🔧 Funciones Principales

### 1. `extraccion.py`

| Función                | Descripción                               | Parámetros   | Retorno        |
| ---------------------- | ----------------------------------------- | ------------ | -------------- |
| `extraer_ventas_csv`   | Lee CSV de ventas de una fecha específica | `fecha: str` | `pd.DataFrame` |
| `obtener_ruta_archivo` | Construye ruta al archivo de ventas       | `fecha: str` | `str`          |

### 2. `validacion.py`

| Función                         | Descripción                       | Parámetros         | Retorno            |
| ------------------------------- | --------------------------------- | ------------------ | ------------------ |
| `validar_datos_ventas`          | Valida integridad del DataFrame   | `df: pd.DataFrame` | `dict` (resultado) |
| `verificar_columnas_requeridas` | Verifica existencia de columnas   | `df: pd.DataFrame` | `bool`             |
| `verificar_tipos_datos`         | Verifica tipos de datos correctos | `df: pd.DataFrame` | `bool`             |

### 3. `transformacion.py`

| Función                    | Descripción                            | Parámetros                 | Retorno |
| -------------------------- | -------------------------------------- | -------------------------- | ------- |
| `calcular_metricas_ventas` | Calcula total, promedio, top productos | `df: pd.DataFrame`         | `dict`  |
| `obtener_top_productos`    | Obtiene los N productos más vendidos   | `df: pd.DataFrame, n: int` | `list`  |
| `calcular_ticket_promedio` | Calcula ticket promedio                | `df: pd.DataFrame`         | `float` |

### 4. `deteccion_anomalias.py`

| Función                       | Descripción                        | Parámetros                                                   | Retorno |
| ----------------------------- | ---------------------------------- | ------------------------------------------------------------ | ------- |
| `detectar_caida_ventas`       | Detecta si ventas cayeron > umbral | `total_actual: float, total_historico: float, umbral: float` | `dict`  |
| `calcular_promedio_historico` | Calcula promedio de ventas pasadas | `fechas: list`                                               | `float` |

### 5. `carga.py`

| Función               | Descripción                           | Parámetros                   | Retorno      |
| --------------------- | ------------------------------------- | ---------------------------- | ------------ |
| `guardar_reporte_csv` | Guarda reporte en formato CSV         | `metricas: dict, fecha: str` | `str` (ruta) |
| `guardar_reporte_txt` | Guarda reporte en formato TXT legible | `metricas: dict, fecha: str` | `str` (ruta) |

### 6. `notificaciones.py`

| Función               | Descripción                       | Parámetros                       | Retorno |
| --------------------- | --------------------------------- | -------------------------------- | ------- |
| `simular_envio_email` | Simula envío de email con resumen | `metricas: dict, anomalia: dict` | `dict`  |

---

## 🧪 Metodología: Test-Driven Development (TDD)

Este proyecto sigue **TDD estricto**:

1. **Red**: Escribir test que falla
2. **Green**: Implementar código mínimo para que pase
3. **Refactor**: Mejorar el código manteniendo tests verdes

### Cobertura de Tests

- ✅ **Cobertura mínima**: 80%
- ✅ **Tests por función**: Al menos 2 (caso correcto + caso error)
- ✅ **Tests de integración**: Pipeline completo end-to-end

---

## 🚀 Cómo Ejecutar el Proyecto

### Paso 1: Activar Entorno Virtual

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### Paso 2: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html
```

### Paso 4: Generar Datos de Prueba

```bash
python scripts/generar_datos_ventas.py
```

### Paso 5: Copiar DAG a Airflow

```bash
# Copiar el DAG al directorio de Airflow
cp dags/dag_pipeline_ventas.py ../../airflow/dags/
```

### Paso 6: Ejecutar el DAG en Airflow

1. Abrir http://localhost:8080
2. Buscar `dag_pipeline_ventas`
3. Activar el DAG (toggle switch)
4. Ejecutar manualmente (botón "Play")
5. Ver logs y resultados

---

## 📊 Formato de Datos

### Archivo de Entrada: `ventas_YYYY_MM_DD.csv`

```csv
venta_id,fecha,cliente_id,producto,categoria,cantidad,precio_unitario,total
1,2025-10-25,C001,Laptop HP,Computadoras,1,599.99,599.99
2,2025-10-25,C002,Mouse Logitech,Accesorios,2,19.99,39.98
3,2025-10-25,C003,Teclado Mecánico,Accesorios,1,89.99,89.99
```

**Columnas**:
- `venta_id`: ID único de la venta (int)
- `fecha`: Fecha de la venta (str, formato YYYY-MM-DD)
- `cliente_id`: ID del cliente (str)
- `producto`: Nombre del producto (str)
- `categoria`: Categoría del producto (str)
- `cantidad`: Cantidad vendida (int, >0)
- `precio_unitario`: Precio por unidad (float, >0)
- `total`: Total de la venta (float, >0)

---

## 🎓 Conceptos de Airflow Aplicados

| Concepto                      | Aplicación en el Proyecto                        |
| ----------------------------- | ------------------------------------------------ |
| **DAG**                       | Pipeline completo como DAG con schedule diario   |
| **PythonOperator**            | Todas las funciones de procesamiento             |
| **BashOperator**              | Limpieza de archivos temporales                  |
| **Dependencias Secuenciales** | Extracción → Validación → Transformación         |
| **Dependencias Paralelas**    | Generación de reportes en paralelo               |
| **Validación de Datos**       | Verificar integridad antes de procesar           |
| **Manejo de Errores**         | Reintentos y excepciones claras                  |
| **Idempotencia**              | Ejecutar múltiples veces sin efectos secundarios |

---

## 🔒 Seguridad y Buenas Prácticas

1. **Validación exhaustiva**: Verificar datos antes de procesarlos
2. **Manejo explícito de errores**: Lanzar excepciones claras
3. **Logs detallados**: Registrar cada paso del proceso
4. **Sin hardcoding**: Usar variables de configuración
5. **Rutas seguras**: Usar `os.path.join` o `Path`
6. **Tipado explícito**: Todas las funciones con type hints
7. **Documentación**: Docstrings en español

---

## 📈 Métricas de Calidad

Al completar el proyecto, deberías tener:

- ✅ **15+ funciones** implementadas y documentadas
- ✅ **30+ tests** unitarios pasando
- ✅ **Cobertura > 80%**
- ✅ **0 linter errors** (flake8/black)
- ✅ **1 DAG funcional** en Airflow
- ✅ **Reportes automáticos** generándose correctamente

---

## 🎯 Criterios de Aceptación

### Funcional
- [ ] El DAG aparece en la UI de Airflow
- [ ] Se ejecuta exitosamente sin errores
- [ ] Genera reportes en CSV y TXT
- [ ] Detecta anomalías correctamente
- [ ] Los logs son claros y detallados

### Técnico
- [ ] Todos los tests pasan (`pytest tests/`)
- [ ] Cobertura >= 80%
- [ ] Sin linter errors
- [ ] Funciones con tipado explícito
- [ ] Documentación completa

### Pedagógico
- [ ] Aplica conceptos del Tema 1
- [ ] Código limpio y legible
- [ ] Buenas prácticas de Data Engineering
- [ ] README actualizado

---

## 🏆 Desafíos Adicionales (Opcional)

Si quieres ir más allá:

1. **Añadir más validaciones**: Detectar valores atípicos en precios
2. **Reportes HTML**: Generar gráficos con matplotlib
3. **Alertas reales**: Integrar con email o Slack
4. **Paralelizar extracción**: Procesar múltiples archivos simultáneamente
5. **Dashboard**: Crear visualización con Airflow Variables

---

## 🐛 Troubleshooting

### Problema: Tests fallan al ejecutar pytest

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solución**:
```bash
# Asegúrate de estar en el directorio del proyecto
cd modulo-06-airflow/tema-1-introduccion/proyecto-practico

# Ejecuta pytest desde este directorio
pytest tests/ -v
```

---

### Problema: Archivos CSV no encontrados

**Error**: `FileNotFoundError: El archivo 'data/input/ventas_2025_10_25.csv' no existe`

**Solución**:
1. Crea la carpeta `data/input/` si no existe
2. Genera datos de prueba ejecutando el script (a crear):
```bash
python scripts/generar_datos_ventas.py
```
3. O crea manualmente un CSV con el formato esperado (ver sección "Formato de Datos")

---

### Problema: Cobertura de tests no alcanza 80%

**Solución**:
```bash
# Ver qué líneas no están cubiertas
pytest tests/ --cov=src --cov-report=html

# Abrir reporte en navegador
# Windows: start htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
# Mac: open htmlcov/index.html
```

Añade tests para las líneas/funciones no cubiertas.

---

### Problema: Black reformatea el código constantemente

**Solución**:
Configura tu editor para que formatee automáticamente al guardar:

**VSCode** (`settings.json`):
```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

**PyCharm**: Settings → Tools → Black → "Run on save"

---

### Problema: DAG no aparece en Airflow UI

**Posibles causas**:
1. **DAG no está en la carpeta correcta**:
   - Copiar a `airflow/dags/`: `cp dags/dag_pipeline_ventas.py ../../airflow/dags/`
2. **Errores de sintaxis en el DAG**:
   - Ver logs: `docker logs airflow_webserver`
3. **Airflow no está corriendo**:
   - Iniciar: `docker-compose up -d`

---

### Problema: Imports fallan en el DAG

**Error**: `ImportError: cannot import name 'extraer_ventas_csv' from 'src.extraccion'`

**Solución**:
El DAG necesita acceso al código fuente. Opciones:
1. Copiar carpeta `src/` junto con el DAG
2. Instalar el proyecto como paquete editable: `pip install -e .`
3. Usar variables de Airflow para configurar rutas

---

## 📊 Resultados del Quality Check

**Última ejecución**: 2025-10-25

| Herramienta  | Estado  | Resultado               |
| ------------ | ------- | ----------------------- |
| **Black**    | ✅ PASS  | 14 archivos formateados |
| **Flake8**   | ✅ PASS  | 0 errores de linting    |
| **Pytest**   | ⚠️  PASS | 28/33 tests (85%)       |
| **Coverage** | ⭐ EXCEL | **94%** (objetivo: 80%) |

**Detalles de cobertura**:
```
src/__init__.py              100%
src/carga.py                  97%
src/deteccion_anomalias.py    77%
src/extraccion.py             92%
src/notificaciones.py        100%
src/transformacion.py         97%
src/validacion.py             95%
-----------------------------------
TOTAL                         94%
```

**Calificación final**: 9.0/10 ⭐⭐⭐⭐⭐

---

## 📚 Referencias

- [Documentación de Airflow](https://airflow.apache.org/docs/)
- [Best Practices ETL](https://www.startdataengineering.com/post/etl-best-practices/)
- [Testing en Python](https://docs.pytest.org/)
- [01-TEORIA.md](../01-TEORIA.md) - Conceptos de Airflow
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - Ejemplos prácticos
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - Ejercicios resueltos

---

## 👨‍💻 Autoría

**Fecha de creación**: 2025-10-25
**Autor**: @development [arquitecto]
**Módulo**: 6 - Apache Airflow y Orquestación
**Tema**: 1 - Introducción a Airflow

---

**¡Éxito en tu proyecto!** 🚀

Si tienes dudas, revisa los ejemplos del Tema 1 o consulta la documentación oficial de Airflow.
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Airflow Intermedio - 01 Teoria](../../tema-2-intermedio/01-TEORIA.md)
