# Proyecto Práctico: Pipeline ETL de Ventas de E-commerce

**Nivel**: Intermedio ⭐⭐
**Estado**: ✅ **COMPLETADO Y VALIDADO**
**Cobertura**: 96.23% (64 tests pasando)
**Calidad**: 0 errores de linting

---

## 📋 Descripción del Proyecto

Pipeline **ETL completo y productivo** para procesar ventas del e-commerce **TechStore**. El proyecto implementa:

1. **Extracción** de datos desde archivos CSV (ventas, productos, clientes)
2. **Validación** exhaustiva de calidad de datos
3. **Transformación** con enriquecimiento de información
4. **Carga** idempotente en base de datos SQLite
5. **Logging** detallado de cada operación
6. **Métricas** de rendimiento (tiempo, throughput)
7. **Manejo robusto de errores** con reintentos

---

## 🎯 Objetivos de Aprendizaje

Al estudiar este proyecto, aprenderás:

- ✅ Diseñar pipelines ETL end-to-end con arquitectura limpia
- ✅ Aplicar TDD (Test-Driven Development) estricto
- ✅ Implementar idempotencia (operaciones repetibles sin duplicados)
- ✅ Manejar errores y logging profesional
- ✅ Calcular métricas de ejecución
- ✅ Validar calidad de datos
- ✅ Escribir código modular, funcional y bien testeado

---

## 📚 Conceptos Clave

### Concepto 1: Pipeline ETL
Proceso de **Extract → Transform → Load** que mueve datos desde fuentes hacia destinos, aplicando transformaciones.

**Analogía**: Como una línea de producción en una fábrica: materias primas (Extract) → procesamiento (Transform) → producto final (Load).

**Aplicación en Data Engineering**: Base de todo sistema de datos. Permite integrar datos de múltiples fuentes en un formato consistente para análisis.

### Concepto 2: Idempotencia
Propiedad que garantiza que ejecutar una operación múltiples veces produce el mismo resultado que ejecutarla una vez.

**Analogía**: Como un interruptor de luz: presionarlo varias veces cuando ya está encendido no cambia nada.

**Aplicación en Data Engineering**: Permite reprocesar datos históricos sin crear duplicados. Implementado con `DELETE` antes de `INSERT`.

### Concepto 3: TDD (Test-Driven Development)
Metodología donde escribes los tests **antes** del código de producción.

**Aplicación en Data Engineering**: Garantiza que cada función hace exactamente lo que debe, con casos de éxito y fallo cubiertos.

---

## 📁 Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── extraccion.py         ← 100% cobertura (42 statements, 12 tests)
│   ├── validacion.py         ← 96% cobertura (48 statements, 15 tests)
│   ├── transformacion.py     ← 100% cobertura (34 statements, 9 tests)
│   ├── carga.py              ← 100% cobertura (28 statements, 9 tests)
│   ├── utilidades.py         ← 90% cobertura (30 statements, 13 tests)
│   └── pipeline.py           ← 94% cobertura (82 statements, 6 tests)
│
├── tests/
│   ├── __init__.py
│   ├── test_extraccion.py    ← 12 tests
│   ├── test_validacion.py    ← 15 tests
│   ├── test_transformacion.py ← 9 tests
│   ├── test_carga.py         ← 9 tests
│   ├── test_utilidades.py    ← 13 tests
│   └── test_pipeline.py      ← 6 tests
│
├── datos/
│   ├── ventas.csv            ← Datos de ventas (5 registros de ejemplo)
│   ├── productos.csv         ← Catálogo de productos (5 productos)
│   └── clientes.csv          ← Información de clientes (4 clientes)
│
├── ejemplos/
│   └── ejecutar_pipeline.py  ← Script de demostración completo
│
├── htmlcov/                  ← Reporte de cobertura HTML (generado)
├── README.md                 ← Este archivo
└── requirements.txt          ← Dependencias (pandas, pytest, black, flake8)
```

---

## 🚀 Instalación

### Paso 1: Clonar o navegar al proyecto

```bash
cd modulo-03-ingenieria-datos/tema-1-conceptos-etl/04-proyecto-practico
```

### Paso 2: Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

**Dependencias instaladas**:
- `pandas`: Manipulación de datos
- `pytest`: Framework de testing
- `pytest-cov`: Cobertura de código
- `black`: Formateador de código
- `flake8`: Linter

---

## ✅ Ejecutar Tests

### Todos los tests

```bash
pytest
```

**Resultado esperado**: `64 passed in 3.17s` ✅

### Con cobertura de código

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

**Resultado esperado**:
```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/carga.py               28      0   100%
src/extraccion.py          42      0   100%
src/transformacion.py      34      0   100%
src/validacion.py          48      2    96%   152-153
src/pipeline.py            82      5    94%   157-161
src/utilidades.py          30      3    90%   72, 111, 123
-----------------------------------------------------
TOTAL                     265     10    96%
```

### Ver reporte HTML de cobertura

```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

### Ejecutar linters

```bash
# Black (formateo)
black --check src/ tests/ ejemplos/

# Flake8 (linting)
flake8 src/ tests/ ejemplos/ --max-line-length=88 --extend-ignore=E203
```

**Resultado esperado**: `0 errores` ✅

---

## 📦 Funciones Implementadas

### Módulo: `src/extraccion.py`

#### `leer_csv`

```python
def leer_csv(ruta: str) -> list[dict[str, str]]:
    """Lee un archivo CSV y retorna una lista de diccionarios."""
```

**Descripción**: Lee un archivo CSV utilizando `csv.DictReader` y retorna cada fila como un diccionario.

**Parámetros**:
- `ruta` (str): Ruta al archivo CSV

**Retorna**:
- `list[dict[str, str]]`: Lista de diccionarios donde cada diccionario es una fila

**Lanza**:
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si el archivo está vacío (solo header)
- `TypeError`: Si ruta es `None`

**Ejemplo**:
```python
>>> from src.extraccion import leer_csv
>>> datos = leer_csv("datos/ventas.csv")
>>> print(datos[0])
{'venta_id': '1', 'fecha': '2025-10-01', ...}
```

---

#### `extraer_ventas`

```python
def extraer_ventas(ruta: str) -> list[dict[str, Any]]:
    """Extrae ventas desde un archivo CSV y convierte los tipos de datos."""
```

**Descripción**: Lee el archivo de ventas y convierte los tipos de datos a `int` y `float` donde corresponde.

**Parámetros**:
- `ruta` (str): Ruta al archivo CSV de ventas

**Retorna**:
- `list[dict[str, Any]]`: Lista de diccionarios con tipos correctos

**Lanza**:
- `FileNotFoundError`: Si el archivo no existe
- `ValueError`: Si faltan columnas requeridas

**Ejemplo**:
```python
>>> from src.extraccion import extraer_ventas
>>> ventas = extraer_ventas("datos/ventas.csv")
>>> print(ventas[0]["venta_id"])  # Es int, no str
1
```

---

#### `extraer_productos`

```python
def extraer_productos(ruta: str) -> list[dict[str, Any]]:
    """Extrae productos desde un archivo CSV y convierte los tipos de datos."""
```

**Descripción**: Lee el archivo de productos y convierte `producto_id` y `stock` a enteros.

---

#### `extraer_clientes`

```python
def extraer_clientes(ruta: str) -> list[dict[str, Any]]:
    """Extrae clientes desde un archivo CSV y convierte los tipos de datos."""
```

**Descripción**: Lee el archivo de clientes y convierte `cliente_id` a entero.

---

### Módulo: `src/validacion.py`

#### `validar_no_vacia`

```python
def validar_no_vacia(datos: list[dict], nombre: str) -> None:
    """Valida que una lista de datos no esté vacía."""
```

**Descripción**: Verifica que la lista contenga al menos un elemento. Útil para garantizar que se extrajo información.

**Lanza**: `ValueError` si la lista está vacía.

---

#### `validar_columnas_requeridas`

```python
def validar_columnas_requeridas(datos: list[dict], columnas: list[str]) -> None:
    """Valida que todas las filas tengan las columnas requeridas."""
```

**Descripción**: Verifica que cada diccionario en la lista contenga todas las columnas especificadas.

**Lanza**: `ValueError` si faltan columnas en alguna fila.

---

#### `validar_tipos_ventas`

```python
def validar_tipos_ventas(ventas: list[dict]) -> None:
    """Valida que los campos de ventas tengan los tipos correctos."""
```

**Descripción**: Verifica que:
- `venta_id`, `producto_id`, `cliente_id`, `cantidad` sean `int`
- `precio_unitario` sea `float`

**Lanza**: `TypeError` si los tipos no coinciden.

---

#### `validar_valores_positivos`

```python
def validar_valores_positivos(ventas: list[dict]) -> None:
    """Valida que cantidad y precio_unitario sean mayores a cero."""
```

**Descripción**: Verifica reglas de negocio: no se pueden vender 0 unidades o tener precios negativos.

**Lanza**: `ValueError` si hay valores ≤ 0.

---

#### `validar_datos`

```python
def validar_datos(ventas: list[dict]) -> tuple[bool, list[str]]:
    """Ejecuta todas las validaciones y retorna resultado."""
```

**Descripción**: Orquestador que ejecuta todas las validaciones anteriores y retorna si los datos son válidos.

**Retorna**:
- `tuple[bool, list[str]]`: `(True, [])` si válido, `(False, [errores])` si inválido

---

### Módulo: `src/transformacion.py`

#### `calcular_total_venta`

```python
def calcular_total_venta(venta: dict) -> dict:
    """Calcula el total de una venta (cantidad * precio_unitario)."""
```

**Descripción**: Añade el campo `total` a la venta. No modifica el diccionario original (función pura).

**Retorna**: Nuevo diccionario con campo `total` añadido.

**Ejemplo**:
```python
>>> from src.transformacion import calcular_total_venta
>>> venta = {"cantidad": 2, "precio_unitario": 100.0}
>>> resultado = calcular_total_venta(venta)
>>> print(resultado["total"])
200.0
```

---

#### `enriquecer_venta_con_producto`

```python
def enriquecer_venta_con_producto(venta: dict, productos: list[dict]) -> dict:
    """Añade información del producto a la venta."""
```

**Descripción**: Busca el producto por `producto_id` y añade `nombre_producto` y `categoria` a la venta.

**Lanza**: `ValueError` si el producto no se encuentra.

---

#### `enriquecer_venta_con_cliente`

```python
def enriquecer_venta_con_cliente(venta: dict, clientes: list[dict]) -> dict:
    """Añade información del cliente a la venta."""
```

**Descripción**: Busca el cliente por `cliente_id` y añade `nombre_cliente` y `ciudad` a la venta.

**Lanza**: `ValueError` si el cliente no se encuentra.

---

#### `transformar_ventas`

```python
def transformar_ventas(
    ventas: list[dict],
    productos: list[dict],
    clientes: list[dict]
) -> list[dict]:
    """Aplica todas las transformaciones a cada venta."""
```

**Descripción**: Orquestador que aplica `calcular_total_venta`, `enriquecer_venta_con_producto` y `enriquecer_venta_con_cliente` a todas las ventas.

**Ejemplo**:
```python
>>> from src.transformacion import transformar_ventas
>>> ventas_enriquecidas = transformar_ventas(ventas, productos, clientes)
>>> print(ventas_enriquecidas[0].keys())
dict_keys(['venta_id', 'fecha', 'producto_id', 'cliente_id', 'cantidad',
           'precio_unitario', 'total', 'nombre_producto', 'categoria',
           'nombre_cliente', 'ciudad'])
```

---

### Módulo: `src/carga.py`

#### `crear_tabla_ventas`

```python
def crear_tabla_ventas(db_path: str) -> None:
    """Crea la tabla ventas_procesadas si no existe."""
```

**Descripción**: Crea tabla SQLite con esquema completo (11 columnas). Usa `IF NOT EXISTS` para idempotencia.

---

#### `cargar_ventas_idempotente`

```python
def cargar_ventas_idempotente(
    ventas: list[dict],
    fecha: str,
    db_path: str
) -> int:
    """Carga ventas en la base de datos de forma idempotente."""
```

**Descripción**: Implementa idempotencia con patrón `DELETE + INSERT`:
1. Borra todas las ventas de la fecha especificada
2. Inserta las nuevas ventas

**Retorna**: Número de filas insertadas.

**Ejemplo**:
```python
>>> from src.carga import cargar_ventas_idempotente
>>> num_cargadas = cargar_ventas_idempotente(ventas, "2025-10-01", "ventas.db")
>>> print(f"Se cargaron {num_cargadas} ventas")
Se cargaron 2 ventas
```

---

#### `consultar_ventas_por_fecha`

```python
def consultar_ventas_por_fecha(fecha: str, db_path: str) -> list[dict]:
    """Consulta ventas de una fecha específica."""
```

**Descripción**: Retorna todas las ventas de una fecha como lista de diccionarios.

---

### Módulo: `src/utilidades.py`

#### `configurar_logging`

```python
def configurar_logging(nivel: str = "INFO") -> None:
    """Configura logging para el pipeline."""
```

**Descripción**: Configura logger con formato profesional y nivel especificado.

**Niveles válidos**: `"DEBUG"`, `"INFO"`, `"WARNING"`, `"ERROR"`, `"CRITICAL"`

---

#### `calcular_metricas_pipeline`

```python
def calcular_metricas_pipeline(tiempo_inicio: float, num_filas: int) -> dict:
    """Calcula métricas de ejecución del pipeline."""
```

**Descripción**: Calcula tiempo transcurrido y throughput (filas/segundo).

**Retorna**:
```python
{
    'tiempo_segundos': 0.15,
    'filas_por_segundo': 66.67
}
```

---

#### `formatear_fecha`

```python
def formatear_fecha(fecha_str: str) -> str:
    """Valida y formatea una fecha en formato YYYY-MM-DD."""
```

**Descripción**: Verifica que la fecha sea válida (formato y existencia).

**Lanza**:
- `ValueError`: Si el formato es incorrecto o la fecha no existe (ej: 2025-02-30)
- `TypeError`: Si se pasa `None`

---

### Módulo: `src/pipeline.py`

#### `pipeline_etl`

```python
def pipeline_etl(
    fecha: str,
    directorio_datos: str = "datos",
    db_path: str = "ventas.db"
) -> dict:
    """Ejecuta el pipeline ETL completo para una fecha específica."""
```

**Descripción**: Orquesta todo el proceso ETL:

1. **Extract**: Lee ventas, productos, clientes
2. **Filter**: Filtra ventas por fecha
3. **Validate**: Valida calidad de datos
4. **Transform**: Enriquece ventas
5. **Load**: Carga en DB (idempotente)
6. **Logging**: Registra cada paso
7. **Metrics**: Calcula tiempo y throughput

**Retorna**:
```python
{
    'fecha': '2025-10-01',
    'filas_extraidas': 2,
    'filas_validas': 2,
    'filas_cargadas': 2,
    'tiempo_segundos': 0.15,
    'estado': 'EXITOSO',  # o 'ERROR', 'SIN_DATOS'
    'errores': []
}
```

**Ejemplo**:
```python
>>> from src.pipeline import pipeline_etl
>>> metricas = pipeline_etl(fecha="2025-10-01")
>>> print(f"Estado: {metricas['estado']}")
Estado: EXITOSO
>>> print(f"Filas cargadas: {metricas['filas_cargadas']}")
Filas cargadas: 2
```

---

#### `pipeline_etl_con_reintentos`

```python
def pipeline_etl_con_reintentos(
    fecha: str,
    directorio_datos: str = "datos",
    db_path: str = "ventas.db",
    max_intentos: int = 3
) -> dict:
    """Ejecuta pipeline_etl con reintentos automáticos."""
```

**Descripción**: Wrapper de `pipeline_etl` que implementa:
- Reintentos automáticos en caso de fallo
- Exponential backoff (2^intento segundos de espera)
- Logging de cada intento

**Lanza**: Excepción si todos los intentos fallan.

**Ejemplo**:
```python
>>> from src.pipeline import pipeline_etl_con_reintentos
>>> metricas = pipeline_etl_con_reintentos(
...     fecha="2025-10-01",
...     max_intentos=3
... )
```

---

## 🎓 Ejemplos de Uso

### Ejemplo 1: Ejecutar Pipeline para Una Fecha

```python
from src.pipeline import pipeline_etl

# Ejecutar pipeline para una fecha específica
metricas = pipeline_etl(
    fecha="2025-10-01",
    directorio_datos="datos",
    db_path="ventas.db"
)

# Mostrar resultados
print(f"Estado: {metricas['estado']}")
print(f"Filas procesadas: {metricas['filas_cargadas']}")
print(f"Tiempo: {metricas['tiempo_segundos']}s")

# Salida esperada:
# Estado: EXITOSO
# Filas procesadas: 2
# Tiempo: 0.15s
```

---

### Ejemplo 2: Pipeline con Reintentos

```python
from src.pipeline import pipeline_etl_con_reintentos

# Ejecutar con reintentos automáticos
try:
    metricas = pipeline_etl_con_reintentos(
        fecha="2025-10-01",
        max_intentos=3
    )
    print(f"✅ Pipeline exitoso: {metricas['filas_cargadas']} filas")
except Exception as e:
    print(f"❌ Pipeline falló después de 3 intentos: {e}")
```

---

### Ejemplo 3: Procesar Múltiples Fechas

```python
from src.pipeline import pipeline_etl

fechas = ["2025-10-01", "2025-10-02", "2025-10-03"]

for fecha in fechas:
    print(f"\nProcesando {fecha}...")
    metricas = pipeline_etl(fecha=fecha)

    if metricas["estado"] == "EXITOSO":
        print(f"✅ {metricas['filas_cargadas']} filas cargadas")
    elif metricas["estado"] == "SIN_DATOS":
        print("⚠️ Sin datos para esta fecha")
    else:
        print(f"❌ Error: {metricas['errores']}")

# Salida esperada:
# Procesando 2025-10-01...
# ✅ 2 filas cargadas
#
# Procesando 2025-10-02...
# ✅ 2 filas cargadas
#
# Procesando 2025-10-03...
# ✅ 1 filas cargadas
```

---

### Ejemplo 4: Consultar Ventas Cargadas

```python
from src.carga import consultar_ventas_por_fecha

# Consultar ventas de una fecha
ventas = consultar_ventas_por_fecha("2025-10-01", "ventas.db")

# Mostrar resultados
for venta in ventas:
    print(f"Cliente: {venta['nombre_cliente']}")
    print(f"Producto: {venta['nombre_producto']}")
    print(f"Total: ${venta['total']:.2f}")
    print("---")

# Salida esperada:
# Cliente: Juan Perez
# Producto: Laptop
# Total: $1799.98
# ---
# Cliente: Maria Garcia
# Producto: Mouse Logitech
# Total: $149.95
# ---
```

---

### Ejemplo 5: Script Completo (ver `ejemplos/ejecutar_pipeline.py`)

```bash
python ejemplos/ejecutar_pipeline.py
```

**Salida esperada**:
```
============================================================
Pipeline ETL de Ventas de E-commerce
============================================================

📂 Directorio de datos: E:\...\datos
💾 Base de datos: E:\...\ventas.db
📅 Fechas a procesar: 5

------------------------------------------------------------

[1/5] Procesando fecha: 2025-10-01
----------------------------------------

✅ Estado: EXITOSO
📊 Filas extraídas: 2
✓ Filas válidas: 2
💾 Filas cargadas: 2
⏱️ Tiempo: 0.15s

[2/5] Procesando fecha: 2025-10-02
...

============================================================
RESUMEN FINAL
============================================================

📊 Total de fechas: 5
✅ Exitosas: 5
⚠️ Sin datos: 0
❌ Con errores: 0

💾 Total de filas cargadas: 5
⏱️ Tiempo total: 0.75s
🚀 Throughput: 6.67 filas/s

============================================================
Pipeline completado!
============================================================
```

---

## 🐛 Troubleshooting

### Problema: `FileNotFoundError: El archivo datos/ventas.csv no existe`

**Causa**: Los archivos de datos no están en la ubicación correcta.

**Solución**:
1. Verifica que estás ejecutando el script desde el directorio correcto:
   ```bash
   cd modulo-03-ingenieria-datos/tema-1-conceptos-etl/04-proyecto-practico
   ```
2. Verifica que existan los archivos:
   ```bash
   ls datos/
   # Debe mostrar: ventas.csv, productos.csv, clientes.csv
   ```

---

### Problema: `ValueError: La lista de ventas está vacía`

**Causa**: No hay ventas para la fecha especificada.

**Solución**:
- Verifica que la fecha exista en `datos/ventas.csv`
- Usa una fecha válida: `2025-10-01`, `2025-10-02`, o `2025-10-03`

---

### Problema: `sqlite3.OperationalError: unable to open database file`

**Causa**: No tienes permisos de escritura en el directorio.

**Solución**:
1. Verifica permisos del directorio:
   ```bash
   # Windows:
   icacls .
   # Linux/Mac:
   ls -la
   ```
2. O especifica otra ruta para la base de datos:
   ```python
   pipeline_etl(fecha="2025-10-01", db_path="/tmp/ventas.db")
   ```

---

### Problema: Tests fallan con `UnicodeDecodeError`

**Causa**: Problema de encoding en Windows.

**Solución**: Los tests ya manejan UTF-8 explícitamente. Si persiste:
```python
# En test, usar:
archivo.write_text("contenido", encoding="utf-8")
```

---

### Problema: `ImportError: No module named 'src'`

**Causa**: Python no encuentra el paquete `src`.

**Solución**:
1. Ejecuta desde el directorio raíz del proyecto:
   ```bash
   cd modulo-03-ingenieria-datos/tema-1-conceptos-etl/04-proyecto-practico
   ```
2. O añade al `PYTHONPATH`:
   ```bash
   # Windows:
   $env:PYTHONPATH = "."
   # Linux/Mac:
   export PYTHONPATH=.
   ```

---

## 📊 Métricas de Calidad Alcanzadas

### Cobertura de Tests
- ✅ **96.23% de cobertura** (objetivo: >80%)
- ✅ **64 tests pasando** (100% success rate)
- ✅ **3.17s de ejecución** (pipeline eficiente)

### Cobertura por Módulo
| Módulo              | Cobertura | Estado      |
| ------------------- | --------- | ----------- |
| `carga.py`          | 100%      | ✅ Excelente |
| `extraccion.py`     | 100%      | ✅ Excelente |
| `transformacion.py` | 100%      | ✅ Excelente |
| `validacion.py`     | 96%       | ✅ Excelente |
| `pipeline.py`       | 94%       | ✅ Muy bueno |
| `utilidades.py`     | 90%       | ✅ Muy bueno |

### Calidad de Código
- ✅ **0 errores de flake8** (linting perfecto)
- ✅ **Formateado con black** (PEP 8)
- ✅ **Type hints completos** (todas las funciones)
- ✅ **Docstrings exhaustivos** (todas las funciones)
- ✅ **Funciones puras** (sin side effects)

### Complejidad
- ✅ **Funciones cortas**: Promedio 15 líneas
- ✅ **Sin bucles anidados**
- ✅ **Arquitectura modular**: 6 módulos independientes

---

## 📚 Recursos Adicionales

### Documentación del Tema
- [01-TEORIA.md](../01-TEORIA.md) - Teoría completa de conceptos ETL/ELT
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - 5 ejemplos trabajados paso a paso
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - 15 ejercicios con soluciones

### Herramientas Utilizadas
- [pytest](https://docs.pytest.org/) - Framework de testing
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Cobertura de código
- [black](https://black.readthedocs.io/) - Formateador de código
- [flake8](https://flake8.pycqa.org/) - Linter

### Conceptos Avanzados
- [Best Practices de ETL](https://www.integrate.io/blog/etl-best-practices/)
- [Idempotencia en Data Engineering](https://en.wikipedia.org/wiki/Idempotence)
- [Test-Driven Development](https://testdriven.io/blog/modern-tdd/)

---

## 📄 Licencia

Proyecto educativo del **Master en Ingeniería de Datos con IA**.

---

## 🎓 Próximos Pasos

Después de completar este proyecto, te recomendamos:

1. **Tema 2**: Extracción de Datos (APIs, Web Scraping)
2. **Tema 3**: Transformación con Pandas (DataFrames, Joins)
3. **Tema 4**: Calidad de Datos (Great Expectations)
4. **Proyecto Integrador**: Pipeline completo con todas las técnicas aprendidas

---

**¡Felicidades por completar este proyecto!** 🎉

Has implementado un pipeline ETL robusto, bien testeado y productivo. Este proyecto puede ser parte de tu portafolio profesional.

**Última actualización**: 2025-10-23
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Extracción - 01 Teoria](../../tema-2-extraccion/01-TEORIA.md)
