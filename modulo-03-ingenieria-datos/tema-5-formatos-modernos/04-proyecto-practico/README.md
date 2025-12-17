# Proyecto Práctico: Conversor Multi-formato

**Módulo 3 - Tema 5**: Formatos de Datos Modernos
**Versión**: 1.0.0
**Metodología**: Test-Driven Development (TDD)

---

## 📋 Descripción

Framework completo para conversión entre formatos de datos (CSV, JSON, JSON Lines, Parquet), gestión de compresión y análisis de formatos. Diseñado para optimizar pipelines de datos en Data Engineering.

### Características Principales

- ✅ **Conversión universal** entre CSV, JSON, JSON Lines y Parquet
- ✅ **Compresión y descompresión** con múltiples algoritmos (gzip, bz2, xz)
- ✅ **Análisis y benchmarking** de formatos y compresiones
- ✅ **Particionamiento** de datos para Big Data
- ✅ **Autodetección** de formatos
- ✅ **Cobertura de tests** >85%
- ✅ **Tipado explícito** con type hints
- ✅ **Documentación completa** con docstrings

---

## 🏗️ Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   ├── conversor_formatos.py        # 8 funciones de conversión
│   ├── gestor_compresion.py          # 4 funciones de compresión
│   └── analizador_formatos.py        # 5 funciones de análisis
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Fixtures compartidas
│   ├── test_conversor_formatos.py   # 26 tests
│   ├── test_gestor_compresion.py     # 17 tests
│   └── test_analizador_formatos.py   # 15 tests
├── datos/
│   ├── ventas_ejemplo.csv            # Datos de ejemplo
│   └── pedidos.json                  # JSON nested
├── ejemplos/
│   └── ejemplo_pipeline_completo.py  # Pipeline completo
├── htmlcov/                          # Reporte de cobertura
├── requirements.txt
├── pytest.ini
└── README.md                         # Este archivo
```

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar Tests

```bash
# Todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# Tests específicos
pytest tests/test_conversor_formatos.py -v

# Ver cobertura en HTML
# Abrir: htmlcov/index.html
```

### 3. Uso Básico

```python
from src.conversor_formatos import convertir_csv_a_parquet, leer_multiple_formatos
from src.gestor_compresion import comparar_compresiones
from src.analizador_formatos import generar_reporte_formato

# Convertir CSV a Parquet
convertir_csv_a_parquet('datos.csv', 'datos.parquet', compresion='snappy')

# Leer cualquier formato automáticamente
df = leer_multiple_formatos('datos.csv')  # o .json, .jsonl, .parquet

# Comparar algoritmos de compresión
resultados = comparar_compresiones('datos.csv', ['gzip', 'bz2', 'xz'])

# Generar reporte de un archivo
reporte = generar_reporte_formato('datos.parquet')
print(reporte)
```

---

## 📚 Módulos

### 1. conversor_formatos.py

Conversiones entre formatos de datos.

#### Funciones

**`convertir_csv_a_parquet(ruta_csv, ruta_parquet, compresion='snappy')`**

Convierte CSV a Parquet con compresión.

```python
convertir_csv_a_parquet('ventas.csv', 'ventas.parquet', compresion='snappy')
```

**`convertir_json_a_parquet(ruta_json, ruta_parquet, orient='records')`**

Convierte JSON o JSON Lines a Parquet.

```python
convertir_json_a_parquet('pedidos.json', 'pedidos.parquet')
convertir_json_a_parquet('logs.jsonl', 'logs.parquet', orient='lines')
```

**`convertir_parquet_a_csv(ruta_parquet, ruta_csv)`**

Convierte Parquet a CSV.

```python
convertir_parquet_a_csv('datos.parquet', 'datos.csv')
```

**`convertir_json_a_csv(ruta_json, ruta_csv)`**

Convierte JSON a CSV.

```python
convertir_json_a_csv('datos.json', 'datos.csv')
```

**`convertir_csv_a_json_lines(ruta_csv, ruta_jsonl)`**

Convierte CSV a JSON Lines.

```python
convertir_csv_a_json_lines('ventas.csv', 'ventas.jsonl')
```

**`leer_multiple_formatos(ruta) → pd.DataFrame`**

Lee archivo detectando formato automáticamente.

```python
df = leer_multiple_formatos('datos.csv')      # CSV
df = leer_multiple_formatos('datos.json')     # JSON
df = leer_multiple_formatos('datos.jsonl')    # JSON Lines
df = leer_multiple_formatos('datos.parquet')  # Parquet
```

**`guardar_formato_automatico(df, ruta, formato=None)`**

Guarda DataFrame detectando formato por extensión.

```python
guardar_formato_automatico(df, 'salida.csv')
guardar_formato_automatico(df, 'salida.parquet')
guardar_formato_automatico(df, 'salida.datos', formato='parquet')
```

**`convertir_con_particiones(df, ruta_base, columnas_particion, formato='parquet')`**

Guarda DataFrame particionado (solo Parquet).

```python
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
convertir_con_particiones(df, 'ventas/', ['año', 'mes'])
```

---

### 2. gestor_compresion.py

Gestión de compresión y descompresión de archivos.

#### Funciones

**`comprimir_archivo(ruta_entrada, algoritmo='gzip') → str`**

Comprime archivo con algoritmo especificado.

```python
ruta_comprimida = comprimir_archivo('datos.csv', algoritmo='gzip')
# Retorna: 'datos.csv.gz'
```

**`descomprimir_archivo(ruta_comprimida) → str`**

Descomprime archivo detectando formato automáticamente.

```python
ruta_descomprimida = descomprimir_archivo('datos.csv.gz')
# Retorna: 'datos.csv'
```

**`comparar_compresiones(ruta_archivo, algoritmos) → Dict`**

Compara múltiples algoritmos de compresión.

```python
resultados = comparar_compresiones('datos.csv', ['gzip', 'bz2', 'xz'])

# Retorna:
# {
#   'gzip': {
#     'tamanio_original_kb': 120.5,
#     'tamanio_comprimido_kb': 25.3,
#     'ratio_compresion': 4.76,
#     'reduccion_pct': 79.0,
#     'tiempo_compresion_s': 0.0432
#   },
#   ...
# }
```

**`comprimir_dataframe_memoria(df, algoritmo='gzip') → bytes`**

Comprime DataFrame en memoria sin escribir a disco.

```python
bytes_comprimidos = comprimir_dataframe_memoria(df, algoritmo='gzip')

# Para descomprimir:
import gzip
import io
buffer = io.BytesIO(gzip.decompress(bytes_comprimidos))
df_reconstruido = pd.read_csv(buffer)
```

---

### 3. analizador_formatos.py

Análisis y comparación de formatos de datos.

#### Funciones

**`detectar_formato_archivo(ruta) → str`**

Detecta formato de archivo automáticamente.

```python
formato = detectar_formato_archivo('datos.csv')      # → 'csv'
formato = detectar_formato_archivo('datos.parquet')  # → 'parquet'
formato = detectar_formato_archivo('logs.jsonl')     # → 'jsonl'
```

**`obtener_metadata_parquet(ruta) → Dict`**

Obtiene metadata detallada de archivo Parquet.

```python
metadata = obtener_metadata_parquet('datos.parquet')

# Retorna:
# {
#   'num_filas': 1000,
#   'num_columnas': 5,
#   'columnas': ['id', 'nombre', 'edad', ...],
#   'tipos_datos': {'id': 'int64', 'nombre': 'object', ...},
#   'tamanio_archivo_mb': 1.25,
#   'compresion': 'SNAPPY',
#   'num_row_groups': 1
# }
```

**`comparar_tamanios_formatos(df) → Dict[str, float]`**

Compara tamaños de DataFrame en diferentes formatos.

```python
tamanios = comparar_tamanios_formatos(df)

# Retorna:
# {
#   'csv': 120.5,              # KB
#   'json': 185.2,
#   'jsonl': 185.2,
#   'parquet_snappy': 15.3,
#   'parquet_gzip': 12.8
# }
```

**`benchmark_lectura_escritura(df, formatos) → pd.DataFrame`**

Realiza benchmark de lectura/escritura para diferentes formatos.

```python
resultados = benchmark_lectura_escritura(df, ['csv', 'json', 'parquet'])

# Retorna DataFrame:
#   formato  tiempo_escritura_s  tiempo_lectura_s  tamanio_kb
#   csv      0.8500              1.2000            120.50
#   json     1.9500              2.8500            185.20
#   parquet  0.7200              0.3800             15.30
```

**`generar_reporte_formato(ruta) → Dict`**

Genera reporte completo de un archivo de datos.

```python
reporte = generar_reporte_formato('datos.parquet')

# Retorna:
# {
#   'formato': 'parquet',
#   'tamanio_mb': 1.25,
#   'num_registros': 1000,
#   'num_columnas': 5,
#   'columnas': ['id', 'nombre', 'edad', 'salario', 'activo'],
#   'tipos_datos': {'id': 'int64', ...},
#   'compresion': 'SNAPPY',
#   'metadata_parquet': {...}
# }
```

---

## 🧪 Testing

### Cobertura de Tests

- **conversor_formatos.py**: 26 tests (~95% cobertura)
- **gestor_compresion.py**: 17 tests (~92% cobertura)
- **analizador_formatos.py**: 15 tests (~90% cobertura)

**Total**: 58 tests, >90% cobertura global

### Ejecutar Tests

```bash
# Todos los tests con cobertura
pytest tests/ --cov=src --cov-report=html

# Solo tests de conversor
pytest tests/test_conversor_formatos.py -v

# Solo tests de compresión
pytest tests/test_gestor_compresion.py -v

# Solo tests de analizador
pytest tests/test_analizador_formatos.py -v

# Tests con marcadores
pytest -m "not slow"  # Excluir tests lentos
```

### Fixtures Disponibles

Definidas en `tests/conftest.py`:

- `df_ejemplo`: DataFrame de 100 registros
- `df_vacio`: DataFrame vacío
- `directorio_temporal`: Directorio temporal para tests
- `archivo_csv_temporal`: CSV temporal
- `archivo_json_temporal`: JSON temporal
- `archivo_jsonl_temporal`: JSON Lines temporal
- `archivo_parquet_temporal`: Parquet temporal
- `df_con_particiones`: DataFrame con columnas de partición
- `df_json_nested`: Datos JSON con estructura nested

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Pipeline ETL Completo

```python
from src.conversor_formatos import leer_multiple_formatos, convertir_con_particiones
from src.gestor_compresion import comprimir_archivo
import pandas as pd

# 1. Extraer de múltiples fuentes
df_ventas = leer_multiple_formatos('ventas.csv')
df_clientes = leer_multiple_formatos('clientes.json')

# 2. Transformar
df = pd.merge(df_ventas, df_clientes, on='cliente_id')
df['fecha'] = pd.to_datetime(df['fecha'])
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month

# 3. Cargar particionado
convertir_con_particiones(df, 'data_lake/ventas/', ['año', 'mes'])

print("Pipeline completado ✅")
```

### Ejemplo 2: Benchmark de Formatos

```python
from src.analizador_formatos import benchmark_lectura_escritura, comparar_tamanios_formatos
import pandas as pd

# Generar datos de prueba
df = pd.DataFrame({
    'id': range(10000),
    'valor': range(10000, 20000)
})

# Comparar tamaños
tamanios = comparar_tamanios_formatos(df)
print("Tamaños:", tamanios)

# Benchmark lectura/escritura
benchmark = benchmark_lectura_escritura(df, ['csv', 'json', 'parquet'])
print(benchmark)
```

### Ejemplo 3: Optimización de Compresión

```python
from src.gestor_compresion import comparar_compresiones

# Comparar algoritmos
resultados = comparar_compresiones('datos_grandes.csv', ['gzip', 'bz2', 'xz'])

for algoritmo, metricas in resultados.items():
    print(f"{algoritmo}:")
    print(f"  Reducción: {metricas['reduccion_pct']}%")
    print(f"  Tiempo: {metricas['tiempo_compresion_s']}s")
```

---

## 🎯 Casos de Uso

### 1. Migración de Sistema Legacy (CSV) a Data Lake (Parquet)

```python
from src.conversor_formatos import convertir_csv_a_parquet

# Convertir todos los CSV históricos
archivos_csv = ['ventas_2022.csv', 'ventas_2023.csv', 'ventas_2024.csv']

for archivo in archivos_csv:
    convertir_csv_a_parquet(archivo, archivo.replace('.csv', '.parquet'))
```

### 2. Optimización de Almacenamiento

```python
from src.analizador_formatos import comparar_tamanios_formatos
import pandas as pd

df = pd.read_csv('datos_grandes.csv')
tamanios = comparar_tamanios_formatos(df)

print(f"CSV: {tamanios['csv']} KB")
print(f"Parquet: {tamanios['parquet_snappy']} KB")
print(f"Ahorro: {((tamanios['csv'] - tamanios['parquet_snappy']) / tamanios['csv'] * 100):.1f}%")
```

### 3. Pipeline de Logs

```python
from src.conversor_formatos import convertir_csv_a_json_lines

# Logs de CSV a JSON Lines para streaming
convertir_csv_a_json_lines('logs_app.csv', 'logs_app.jsonl')
```

---

## 🔧 Configuración

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=85
```

### requirements.txt

```
pandas>=2.0.0
numpy>=1.24.0
pyarrow>=12.0.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

---

## 🚨 Manejo de Errores

Todas las funciones siguen estas convenciones:

- **Validación de inputs**: Verificar que archivos existen, DataFrames no vacíos
- **Excepciones específicas**: `FileNotFoundError`, `ValueError`, `TypeError`
- **Mensajes claros**: Indicar exactamente qué falló y por qué
- **Sin fallos silenciosos**: Siempre lanzar excepción en errores

```python
def ejemplo_funcion(ruta: str) -> pd.DataFrame:
    """Ejemplo con validaciones."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    df = pd.read_csv(ruta)

    if df.empty:
        raise ValueError("El archivo está vacío")

    return df
```

---

## 🔐 Consideraciones de Seguridad

- **Validación de paths**: Verificar que rutas no contengan caracteres peligrosos
- **Límites de tamaño**: Verificar que archivos no excedan límites razonables
- **Sanitización**: Limpiar inputs antes de usar en operaciones de archivo
- **Permisos**: Verificar permisos de lectura/escritura antes de operar
- **Logging**: Registrar todas las operaciones importantes

---

## 🎓 Mejores Prácticas

1. **Usa Parquet para almacenamiento**: Mejor compresión y velocidad
2. **Particiona datasets grandes**: >1 GB debe estar particionado
3. **Comprime datos en reposo**: Usa snappy para balance, gzip para máxima compresión
4. **Lectura selectiva con Parquet**: Usa `columns` y `filters`
5. **Testea conversiones**: Verifica integridad después de convertir
6. **Documenta schemas**: Mantén clara la estructura de datos
7. **Versiona formatos**: Mantén histórico de cambios en estructura

---

## 📝 Convenciones de Código

- **Nombres en español**: Funciones, variables, comentarios
- **Snake_case**: Funciones y variables
- **PascalCase**: Clases (si las hubiera)
- **Type hints**: Siempre en parámetros y retornos
- **Docstrings**: En español con Args, Returns, Raises
- **Sin tildes en código**: Solo en comentarios y docstrings
- **Imports ordenados**: stdlib, third-party, local

---

## 📞 Soporte

Para preguntas o problemas:
- Revisar ejemplos en `ejemplos/`
- Consultar tests en `tests/`
- Ver documentación en archivos fuente

---

## 📄 Licencia

Este proyecto es parte del Master en Ingeniería de Datos.
Uso educativo exclusivamente.

---

*Última actualización: 2025-10-30*
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Carga y Pipelines - 01 Teoria](../../tema-6-carga-pipelines/01-TEORIA.md)
