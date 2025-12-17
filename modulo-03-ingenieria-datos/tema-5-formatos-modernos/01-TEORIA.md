# Tema 5: Formatos de Datos Modernos

**Duración estimada**: 1-2 semanas
**Nivel**: Intermedio-Avanzado
**Prerrequisitos**: Python, Pandas, conceptos de ETL, transformación de datos

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

1. **Comprender formatos de datos modernos** y sus diferencias clave (JSON, Parquet, Avro)
2. **Trabajar con JSON y JSON Lines** para APIs, streaming y logs
3. **Utilizar Parquet** para almacenamiento columnar eficiente
4. **Aplicar compresión** (gzip, snappy, zstd) según el caso de uso
5. **Particionar datos grandes** para optimizar consultas
6. **Elegir el formato adecuado** según requisitos de rendimiento y escalabilidad
7. **Convertir entre formatos** de manera eficiente y segura

---

## 📚 Tabla de Contenidos

1. [Introducción a los Formatos Modernos](#1-introducción-a-los-formatos-modernos)
2. [JSON y JSON Lines](#2-json-y-json-lines)
3. [Parquet: Almacenamiento Columnar](#3-parquet-almacenamiento-columnar)
4. [Avro: Schemas Evolutivos](#4-avro-schemas-evolutivos)
5. [Comparación de Formatos](#5-comparación-de-formatos)
6. [Compresión de Datos](#6-compresión-de-datos)
7. [Particionamiento de Datos](#7-particionamiento-de-datos)
8. [Cuándo Usar Cada Formato](#8-cuándo-usar-cada-formato)
9. [Errores Comunes](#9-errores-comunes)
10. [Buenas Prácticas](#10-buenas-prácticas)

---

## 1. Introducción a los Formatos Modernos

### ¿Por qué son importantes los formatos de datos?

En Data Engineering, la **elección del formato de datos** es una decisión arquitectónica crítica que afecta:

- **Rendimiento**: Velocidad de lectura/escritura
- **Almacenamiento**: Tamaño en disco (costos de infraestructura)
- **Escalabilidad**: Capacidad de manejar datasets grandes
- **Compatibilidad**: Interoperabilidad entre sistemas
- **Mantenibilidad**: Facilidad para evolucionar esquemas

### Evolución de los Formatos

**1. CSV (1972)**: Simple, universal, pero limitado
- ✅ Fácil de leer, compatible universalmente
- ❌ Sin tipos de datos, sin compresión eficiente, lento

**2. JSON (2001)**: Estructuras anidadas, legible
- ✅ Flexible, soporta nested data, legible
- ❌ Verboso, consumo alto de memoria, lento para grandes volúmenes

**3. Parquet (2013)**: Columnar, eficiente, comprimido
- ✅ Altamente comprimido, lectura selectiva, esquema embebido
- ❌ No legible por humanos, overhead de escritura

**4. Avro (2009)**: Binario, schema evolutivo
- ✅ Compacto, evolución de schemas, rápido en streaming
- ❌ Menos adoptado que Parquet, necesita decodificador

### El Problema con CSV

CSV ha sido el formato estándar durante décadas, pero tiene **limitaciones críticas**:

```csv
id,nombre,fecha,precio,activo
1,Producto A,2024-01-15,99.99,true
2,Producto B,2024-02-20,149.50,false
```

**Problemas**:
1. **Sin tipos**: Todo es texto, necesita parsing manual
2. **Sin schema**: No hay garantía de estructura
3. **Delimitadores**: Problemas con comas en datos
4. **Sin compresión**: Archivos grandes ocupan mucho espacio
5. **Sin nested data**: Difícil representar estructuras complejas
6. **Performance**: Leer todo el archivo para filtrar una columna

Por esto, los formatos modernos son esenciales en Data Engineering.

---

## 2. JSON y JSON Lines

### 2.1. JSON Estándar

**JSON (JavaScript Object Notation)** es el formato más usado para APIs y configuración.

**Estructura**:

```json
{
  "pedidos": [
    {
      "pedido_id": 1001,
      "cliente": "Juan Pérez",
      "fecha": "2024-01-15",
      "total": 250.50,
      "items": [
        {"producto": "Laptop", "cantidad": 1, "precio": 200.00},
        {"producto": "Mouse", "cantidad": 2, "precio": 25.25}
      ]
    },
    {
      "pedido_id": 1002,
      "cliente": "María López",
      "fecha": "2024-01-16",
      "total": 80.00,
      "items": [
        {"producto": "Teclado", "cantidad": 1, "precio": 80.00}
      ]
    }
  ]
}
```

**Ventajas**:
- ✅ **Legible**: Fácil de leer y debuggear
- ✅ **Flexible**: Soporta estructuras nested y arrays
- ✅ **Tipado**: Distingue números, strings, booleanos, nulls
- ✅ **Universal**: Todos los lenguajes lo soportan

**Desventajas**:
- ❌ **Verboso**: Claves repetidas ocupan espacio
- ❌ **Memoria**: Debe cargarse completo en memoria
- ❌ **Lento**: Parsing es costoso para archivos grandes
- ❌ **No streaming**: No se puede procesar línea por línea

### 2.2. JSON Lines (JSONL / NDJSON)

**JSON Lines** es JSON con **un objeto por línea**, ideal para streaming y logs.

**Estructura**:

```jsonl
{"pedido_id": 1001, "cliente": "Juan Pérez", "fecha": "2024-01-15", "total": 250.50}
{"pedido_id": 1002, "cliente": "María López", "fecha": "2024-01-16", "total": 80.00}
{"pedido_id": 1003, "cliente": "Ana García", "fecha": "2024-01-17", "total": 120.00}
```

**Ventajas sobre JSON estándar**:
- ✅ **Streaming**: Procesar línea por línea sin cargar todo
- ✅ **Append-friendly**: Añadir registros al final es trivial
- ✅ **Robusto**: Un registro corrupto no afecta los demás
- ✅ **Compresión**: Se comprime muy bien con gzip

**Casos de uso**:
- Logs de aplicaciones
- Exportación de datos de APIs (paginadas)
- Streaming de eventos en tiempo real
- Archivos de datos grandes que no caben en memoria

### 2.3. Trabajar con JSON en Pandas

**Leer JSON estándar**:

```python
import pandas as pd

# JSON con array de objetos
df = pd.read_json('datos.json', orient='records')

# JSON con estructura anidada
df = pd.read_json('datos.json')
df_normalizado = pd.json_normalize(df['pedidos'])
```

**Leer JSON Lines**:

```python
# JSON Lines (un objeto por línea)
df = pd.read_json('datos.jsonl', lines=True)

# Streaming de JSON Lines (para archivos grandes)
chunks = []
for chunk in pd.read_json('datos.jsonl', lines=True, chunksize=10000):
    # Procesar chunk
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)
```

**Escribir JSON**:

```python
# JSON estándar
df.to_json('salida.json', orient='records', indent=2, force_ascii=False)

# JSON Lines
df.to_json('salida.jsonl', orient='records', lines=True, force_ascii=False)
```

**Parámetro `orient`**:
- `'records'`: Lista de objetos `[{...}, {...}]` (más común)
- `'split'`: Dict con `{index: [...], columns: [...], data: [...]}`
- `'index'`: Dict con índice como key `{0: {...}, 1: {...}}`
- `'columns'`: Dict por columnas `{col1: {0: val, 1: val}, ...}`
- `'values'`: Solo valores `[[...], [...]]`

---

## 3. Parquet: Almacenamiento Columnar

### 3.1. ¿Qué es Parquet?

**Apache Parquet** es un formato de almacenamiento **columnar** diseñado para Big Data.

**Diferencia clave: Row-based vs Column-based**

**Row-based (CSV, JSON)**:
```
[ID=1, Nombre="Juan", Edad=25, Ciudad="Madrid"]
[ID=2, Nombre="María", Edad=30, Ciudad="Barcelona"]
[ID=3, Nombre="Pedro", Edad=28, Ciudad="Madrid"]
```

**Column-based (Parquet)**:
```
ID:      [1, 2, 3]
Nombre:  ["Juan", "María", "Pedro"]
Edad:    [25, 30, 28]
Ciudad:  ["Madrid", "Barcelona", "Madrid"]
```

### 3.2. Ventajas de Parquet

**1. Compresión eficiente**:
- Columnas del mismo tipo se comprimen mejor
- Ejemplo: `[Madrid, Madrid, Madrid, ...]` → compresión 10-50x

**2. Lectura selectiva** (Column Pruning):
```python
# Solo lee columna 'precio' del disco, ignora el resto
df = pd.read_parquet('ventas.parquet', columns=['precio'])
```

**3. Predicados pushdown** (Row Group Filtering):
```python
# Solo lee row groups que contengan año 2024
df = pd.read_parquet('ventas.parquet', filters=[('año', '==', 2024)])
```

**4. Schema embebido**:
- Tipos de datos preservados automáticamente
- Metadata incluye estadísticas (min, max, null_count)

**5. Optimizado para Big Data**:
- Compatible con Spark, Hive, Presto, Athena
- Particionado nativo

### 3.3. Estructura Interna de Parquet

**Jerarquía**:
```
Archivo Parquet
├── Row Group 1 (chunk de ~128MB)
│   ├── Column Chunk: ID
│   ├── Column Chunk: Nombre
│   └── Column Chunk: Precio
├── Row Group 2
│   ├── Column Chunk: ID
│   ├── Column Chunk: Nombre
│   └── Column Chunk: Precio
└── Footer (metadata + estadísticas)
```

**Metadata** incluye:
- Schema (nombres, tipos)
- Estadísticas por columna (min, max, null_count)
- Codificación y compresión usada
- Ubicación de cada row group

### 3.4. Usar Parquet con Pandas

**Instalar PyArrow** (obligatorio):

```bash
pip install pyarrow
```

**Leer Parquet**:

```python
import pandas as pd

# Leer archivo completo
df = pd.read_parquet('ventas.parquet')

# Leer solo columnas específicas (lectura selectiva)
df = pd.read_parquet('ventas.parquet', columns=['fecha', 'precio'])

# Aplicar filtros (pushdown de predicados)
df = pd.read_parquet('ventas.parquet',
                     filters=[('año', '==', 2024), ('mes', '>', 6)])

# Leer múltiples archivos (particionado)
df = pd.read_parquet('ventas/')  # Lee todos los .parquet en directorio
```

**Escribir Parquet**:

```python
# Escritura básica con compresión snappy (default)
df.to_parquet('salida.parquet')

# Especificar compresión
df.to_parquet('salida.parquet', compression='gzip')

# Sin compresión
df.to_parquet('salida.parquet', compression=None)

# Con PyArrow (más opciones)
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.Table.from_pandas(df)
pq.write_table(table, 'salida.parquet',
               compression='snappy',
               use_dictionary=True,
               compression_level=5)
```

### 3.5. Comparación: CSV vs Parquet

**Ejemplo real** con 1 millón de registros:

| Métrica           | CSV        | Parquet (snappy) | Reducción |
|-------------------|------------|------------------|-----------|
| Tamaño en disco   | 120 MB     | 15 MB            | 87%       |
| Tiempo escritura  | 2.5 seg    | 1.8 seg          | 28%       |
| Tiempo lectura    | 3.2 seg    | 0.8 seg          | 75%       |
| Lectura 1 columna | 3.2 seg    | 0.2 seg          | 94%       |
| Memoria en RAM    | 180 MB     | 95 MB            | 47%       |

**Conclusión**: Parquet es **mucho más eficiente** para datasets grandes.

---

## 4. Avro: Schemas Evolutivos

### 4.1. ¿Qué es Avro?

**Apache Avro** es un formato **binario** con **schema embebido**, diseñado para sistemas distribuidos.

**Características**:
- Formato binario compacto
- Schema incluido en archivo (autodescriptivo)
- Evolución de schemas (backward/forward compatibility)
- Rápido en serialización/deserialización
- Usado en Kafka, Hadoop, sistemas de streaming

### 4.2. Schema de Avro

**Ejemplo de schema**:

```json
{
  "type": "record",
  "name": "Usuario",
  "namespace": "com.empresa.datos",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "nombre", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null},
    {"name": "edad", "type": "int"},
    {"name": "activo", "type": "boolean", "default": true}
  ]
}
```

**Tipos soportados**:
- Primitivos: `null`, `boolean`, `int`, `long`, `float`, `double`, `bytes`, `string`
- Complejos: `record`, `enum`, `array`, `map`, `union`, `fixed`

### 4.3. Evolución de Schemas

**Problema**: ¿Qué pasa cuando el schema cambia?

**Schema v1**:
```json
{"name": "Usuario", "fields": [
  {"name": "id", "type": "int"},
  {"name": "nombre", "type": "string"}
]}
```

**Schema v2** (añade campo):
```json
{"name": "Usuario", "fields": [
  {"name": "id", "type": "int"},
  {"name": "nombre", "type": "string"},
  {"name": "email", "type": ["null", "string"], "default": null}
]}
```

**Compatibilidad**:
- **Backward**: Lector nuevo puede leer datos viejos ✅
- **Forward**: Lector viejo puede leer datos nuevos ✅
- **Full**: Ambas direcciones ✅

**Reglas**:
- Campos nuevos deben tener `default`
- No se pueden eliminar campos sin default
- Tipos no pueden cambiar (int → string ❌)

### 4.4. Usar Avro en Python

**Instalar**:

```bash
pip install fastavro
```

**Escribir Avro**:

```python
from fastavro import writer, parse_schema

schema = {
    'type': 'record',
    'name': 'Usuario',
    'fields': [
        {'name': 'id', 'type': 'int'},
        {'name': 'nombre', 'type': 'string'},
        {'name': 'edad', 'type': 'int'}
    ]
}

registros = [
    {'id': 1, 'nombre': 'Juan', 'edad': 25},
    {'id': 2, 'nombre': 'María', 'edad': 30}
]

parsed_schema = parse_schema(schema)

with open('usuarios.avro', 'wb') as out:
    writer(out, parsed_schema, registros)
```

**Leer Avro**:

```python
from fastavro import reader

with open('usuarios.avro', 'rb') as fo:
    avro_reader = reader(fo)
    for record in avro_reader:
        print(record)
```

**Con Pandas**:

```python
import pandas as pd
from fastavro import reader

with open('usuarios.avro', 'rb') as fo:
    avro_reader = reader(fo)
    registros = [record for record in avro_reader]

df = pd.DataFrame(registros)
```

### 4.5. Parquet vs Avro

| Característica      | Parquet               | Avro                  |
|---------------------|-----------------------|-----------------------|
| Almacenamiento      | Columnar              | Row-based             |
| Caso de uso         | Analytics, queries    | Streaming, eventos    |
| Lectura selectiva   | ✅ Muy eficiente       | ❌ Debe leer todo      |
| Escritura secuencial| ❌ Overhead            | ✅ Muy rápida          |
| Compresión          | Excelente             | Buena                 |
| Schema evolution    | Limitada              | Avanzada              |
| Ecosistema          | Spark, Hive, Athena   | Kafka, Hadoop         |

**Regla**: Usa **Parquet** para análisis, **Avro** para streaming.

---

## 5. Comparación de Formatos

### Tabla Comparativa Completa

| Formato     | Tamaño | Lectura | Escritura | Compresión | Schema | Nested | Humano | Caso de Uso           |
|-------------|--------|---------|-----------|------------|--------|--------|--------|-----------------------|
| **CSV**     | 🔴 Grande | 🟡 Media | 🟢 Rápida | ❌ Pobre | ❌ No | ❌ No | ✅ Sí | Datasets simples, intercambio |
| **JSON**    | 🔴 Grande | 🔴 Lenta | 🟡 Media | ❌ Pobre | ❌ No | ✅ Sí | ✅ Sí | APIs, configs, debugging |
| **JSON Lines** | 🟡 Media | 🟡 Media | 🟢 Rápida | 🟡 Media | ❌ No | ✅ Sí | ✅ Sí | Logs, streaming, eventos |
| **Parquet** | 🟢 Pequeño | 🟢 Muy rápida | 🟡 Media | ✅ Excelente | ✅ Sí | ✅ Sí | ❌ No | Analytics, data lakes, Big Data |
| **Avro**    | 🟢 Pequeño | 🟢 Rápida | 🟢 Rápida | ✅ Buena | ✅ Sí (evolutivo) | ✅ Sí | ❌ No | Streaming, Kafka, evolución |

### Benchmark Real

**Dataset**: 1 millón de registros (10 columnas, mix de tipos)

| Formato     | Tamaño Disco | Tiempo Escritura | Tiempo Lectura | Lectura 1 Columna |
|-------------|--------------|------------------|----------------|-------------------|
| CSV         | 120 MB       | 2.5 seg          | 3.2 seg        | 3.2 seg           |
| JSON        | 185 MB       | 4.1 seg          | 5.8 seg        | 5.8 seg           |
| JSON Lines  | 185 MB       | 3.8 seg          | 4.2 seg        | 4.2 seg           |
| Parquet (snappy) | 15 MB   | 1.8 seg          | 0.8 seg        | 0.2 seg           |
| Parquet (gzip) | 12 MB     | 3.2 seg          | 1.2 seg        | 0.3 seg           |
| Avro        | 18 MB        | 1.5 seg          | 1.1 seg        | 1.1 seg           |

**Conclusiones**:
- Parquet es el más eficiente para almacenamiento y lectura analítica
- Avro es rápido en escritura (ideal para streaming)
- CSV/JSON son lentos e ineficientes para grandes volúmenes
- JSON Lines es mejor que JSON para procesamiento incremental

---

## 6. Compresión de Datos

### 6.1. ¿Por qué comprimir?

**Beneficios**:
1. **Reducción de costos**: Menos almacenamiento en S3/GCS
2. **Velocidad de transferencia**: Menos datos a mover por red
3. **I/O más rápido**: En muchos casos, leer comprimido es más rápido
4. **Backup más eficiente**: Menor tamaño de respaldos

**Trade-off**: CPU (compresión/descompresión) vs I/O (lectura/escritura)

### 6.2. Algoritmos de Compresión

| Algoritmo | Ratio Compresión | Velocidad Compresión | Velocidad Descompresión | Uso en Big Data |
|-----------|------------------|----------------------|-------------------------|-----------------|
| **None**  | 1x (sin compresión) | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡⚡ | Solo desarrollo |
| **Snappy** | 2-4x | ⚡⚡⚡⚡ | ⚡⚡⚡⚡⚡ | ✅ Default en Parquet |
| **LZ4**   | 2-3x | ⚡⚡⚡⚡⚡ | ⚡⚡⚡⚡⚡ | ✅ Más rápido |
| **Gzip**  | 4-8x | ⚡⚡ | ⚡⚡⚡ | ✅ Mejor compresión |
| **Zstd**  | 4-8x | ⚡⚡⚡ | ⚡⚡⚡⚡ | ✅ Balanceado |
| **Brotli** | 5-10x | ⚡ | ⚡⚡ | Archivos estáticos |

**Recomendaciones**:
- **Snappy**: Default, buen balance (uso general)
- **Gzip**: Máxima compresión, datos archivados
- **Zstd**: Mejor que gzip en velocidad, similar ratio
- **LZ4**: Máxima velocidad, streaming en tiempo real

### 6.3. Compresión en Pandas

**Parquet con compresión**:

```python
# Snappy (default, recomendado)
df.to_parquet('datos.parquet', compression='snappy')

# Gzip (mayor compresión)
df.to_parquet('datos.parquet', compression='gzip')

# Sin compresión
df.to_parquet('datos.parquet', compression=None)
```

**CSV con compresión**:

```python
# Gzip
df.to_csv('datos.csv.gz', compression='gzip')

# Leer CSV comprimido (automático)
df = pd.read_csv('datos.csv.gz')
```

**JSON con compresión**:

```python
# Gzip
df.to_json('datos.json.gz', compression='gzip', orient='records', lines=True)

# Leer JSON comprimido
df = pd.read_json('datos.json.gz', lines=True)
```

### 6.4. Cuándo comprimir

**SÍ comprimir**:
- ✅ Datos en reposo (data lakes, archivos históricos)
- ✅ Transferencia por red (upload/download)
- ✅ Backups
- ✅ Datasets grandes (>100 MB)

**NO comprimir** (o usar compresión rápida):
- ❌ Procesamiento en tiempo real (latencia crítica)
- ❌ Datasets pequeños (<10 MB, overhead no vale la pena)
- ❌ CPU limitado (dispositivos embebidos)
- ❌ Lecturas muy frecuentes (cache descomprimido mejor)

---

## 7. Particionamiento de Datos

### 7.1. ¿Qué es particionar?

**Particionamiento** es dividir un dataset grande en múltiples archivos organizados por criterios (fecha, categoría, región).

**Sin particionar**:
```
ventas/
└── ventas.parquet (10 GB)
```

**Particionado por año y mes**:
```
ventas/
├── año=2023/
│   ├── mes=01/
│   │   └── datos.parquet (100 MB)
│   ├── mes=02/
│   │   └── datos.parquet (120 MB)
│   └── ...
└── año=2024/
    ├── mes=01/
    │   └── datos.parquet (150 MB)
    └── ...
```

### 7.2. Beneficios del Particionamiento

**1. Partition Pruning**: Solo lee particiones relevantes

```python
# Query: ventas de enero 2024
# Sin particionar: Lee 10 GB completos
# Particionado: Lee solo 150 MB (partición año=2024/mes=01)
df = pd.read_parquet('ventas/', filters=[('año', '==', 2024), ('mes', '==', 1)])
```

**2. Paralelización**: Spark/Dask procesan particiones en paralelo

**3. Gestión de datos**: Fácil eliminar datos antiguos

```bash
# Eliminar ventas de 2022
rm -rf ventas/año=2022/
```

**4. Optimización de escritura**: Escribir por lotes (batch)

### 7.3. Estrategias de Particionamiento

**Por fecha** (más común):
```
datos/año=2024/mes=01/día=15/datos.parquet
```

**Por categoría**:
```
ventas/region=Europa/pais=España/datos.parquet
ventas/region=America/pais=Mexico/datos.parquet
```

**Por hash** (distribución uniforme):
```
usuarios/hash=00/datos.parquet
usuarios/hash=01/datos.parquet
...
usuarios/hash=ff/datos.parquet
```

**Mixto** (fecha + categoría):
```
logs/año=2024/mes=10/nivel=ERROR/datos.parquet
```

### 7.4. Implementar Particionamiento en Pandas

**Escribir con particiones**:

```python
import pandas as pd

# Cargar datos
df = pd.read_csv('ventas_raw.csv')
df['fecha'] = pd.to_datetime(df['fecha'])
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month

# Escribir particionado
df.to_parquet('ventas/', partition_cols=['año', 'mes'])
```

**Resultado**:
```
ventas/
├── año=2023/
│   ├── mes=1/
│   │   └── xxxxxxxxx.parquet
│   └── mes=2/
│       └── yyyyyyyyy.parquet
└── año=2024/
    └── mes=1/
        └── zzzzzzzzz.parquet
```

**Leer con filtros** (partition pruning):

```python
# Lee solo particiones de 2024
df_2024 = pd.read_parquet('ventas/', filters=[('año', '==', 2024)])

# Lee solo enero 2024
df_ene_2024 = pd.read_parquet('ventas/',
                               filters=[('año', '==', 2024), ('mes', '==', 1)])
```

### 7.5. Buenas Prácticas de Particionamiento

**1. No sobre-particionar**:
- ❌ `año/mes/día/hora/minuto` → Miles de particiones pequeñas (overhead)
- ✅ `año/mes` → Particiones de 100-500 MB

**2. Elegir columnas con baja cardinalidad**:
- ✅ Fecha, región, categoría (pocas opciones)
- ❌ ID único, email (alta cardinalidad)

**3. Orden de particiones**:
- Primera: columna más filtrada (ej: año)
- Segunda: siguiente más filtrada (ej: mes)

**4. Tamaño de particiones**:
- Ideal: **100-500 MB por partición**
- Muy pequeñas (<10 MB): overhead de metadatos
- Muy grandes (>1 GB): difícil de procesar

---

## 8. Cuándo Usar Cada Formato

### Matriz de Decisión

**CSV**: Usar cuando...
- ✅ Necesitas intercambiar datos con Excel o herramientas simples
- ✅ Dataset pequeño (<100 MB)
- ✅ No hay anidación de datos
- ✅ Lectura humana es importante
- ❌ NO usar para Big Data, APIs, o datos anidados

**JSON**: Usar cuando...
- ✅ Datos de APIs REST
- ✅ Configuración de aplicaciones
- ✅ Datos anidados complejos
- ✅ Debugging (legibilidad)
- ❌ NO usar para datasets grandes (>100 MB)

**JSON Lines**: Usar cuando...
- ✅ Logs de aplicaciones
- ✅ Streaming de eventos
- ✅ Procesamiento incremental (append-only)
- ✅ Datasets grandes que necesitan ser legibles
- ❌ NO usar si necesitas consultas analíticas

**Parquet**: Usar cuando...
- ✅ Data lakes y data warehouses
- ✅ Analytics y BI (consultas sobre columnas específicas)
- ✅ Big Data (>1 GB)
- ✅ Necesitas compresión eficiente
- ✅ Integración con Spark, Hive, Athena, BigQuery
- ❌ NO usar para streaming en tiempo real

**Avro**: Usar cuando...
- ✅ Streaming con Kafka
- ✅ Evolución de schemas frecuente
- ✅ Sistemas distribuidos con esquemas versionados
- ✅ Serialización rápida de eventos
- ❌ NO usar para análisis ad-hoc (usa Parquet)

### Flujo Típico en Data Engineering

```
Fuente            Ingestion        Processing        Storage           Analytics
──────            ──────────       ────────────      ─────────         ──────────
APIs (JSON)   →   JSON Lines   →   Parquet       →   Data Lake     →   Parquet
Logs (text)   →   JSON Lines   →   Parquet       →   Data Lake     →   Parquet
Kafka         →   Avro         →   Parquet       →   Data Lake     →   Parquet
CSV legacy    →   CSV          →   Parquet       →   Data Lake     →   Parquet
```

**Patrón recomendado**:
1. **Ingest**: JSON Lines o Avro (streaming)
2. **Transform**: Pandas/Spark (en memoria)
3. **Store**: Parquet particionado + comprimido (data lake)
4. **Query**: Parquet (Athena, BigQuery, Spark SQL)

---

## 9. Errores Comunes

### ❌ Error 1: No considerar el tamaño de memoria con JSON

**Problema**:
```python
# Archivo JSON de 5 GB
df = pd.read_json('datos_enormes.json')  # MemoryError!
```

**Solución**:
```python
# Usar JSON Lines y procesar por chunks
chunks = []
for chunk in pd.read_json('datos_enormes.jsonl', lines=True, chunksize=10000):
    # Procesar chunk
    chunks.append(chunk)
df = pd.concat(chunks, ignore_index=True)
```

### ❌ Error 2: Usar CSV para datos complejos nested

**Problema**:
```csv
pedido_id,items
1,"[{'producto': 'A', 'qty': 2}, {'producto': 'B', 'qty': 1}]"
```

**Solución**: Usar JSON o Parquet con nested structures

```python
# JSON Lines con nested data
df.to_json('pedidos.jsonl', orient='records', lines=True)

# O normalizar antes de CSV
df_items = df.explode('items')
```

### ❌ Error 3: No particionar datasets grandes

**Problema**:
```python
# 50 GB en un solo archivo
df.to_parquet('ventas_historicas.parquet')  # Lento, difícil de consultar
```

**Solución**:
```python
# Particionar por año y mes
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
df.to_parquet('ventas/', partition_cols=['año', 'mes'])
```

### ❌ Error 4: Ignorar la compresión

**Problema**:
```python
# 10 GB sin comprimir
df.to_parquet('datos.parquet', compression=None)
```

**Solución**:
```python
# Con compresión snappy (default, pero explícito es mejor)
df.to_parquet('datos.parquet', compression='snappy')  # ~1.5 GB
```

### ❌ Error 5: No aprovechar lectura columnar

**Problema**:
```python
# Lee todo el archivo para obtener solo una columna
df = pd.read_parquet('ventas.parquet')
precios = df['precio']
```

**Solución**:
```python
# Lee solo la columna necesaria
precios = pd.read_parquet('ventas.parquet', columns=['precio'])
# 10-100x más rápido
```

---

## 10. Buenas Prácticas

### ✅ 1. Elegir formato según caso de uso

```python
# API response → JSON
datos_api = requests.get(url).json()
pd.DataFrame(datos_api).to_json('api_data.json', orient='records')

# Logs → JSON Lines
logs.to_json('logs.jsonl', orient='records', lines=True)

# Analytics → Parquet
df_limpio.to_parquet('data_lake/ventas/', partition_cols=['año', 'mes'])

# Streaming → Avro (si aplica)
# usar librerías específicas de Kafka
```

### ✅ 2. Siempre comprimir datos en reposo

```python
# Default snappy es perfecto para casi todos los casos
df.to_parquet('datos.parquet', compression='snappy')

# Gzip para máxima compresión (datos archivados)
df.to_parquet('historico_2020.parquet', compression='gzip')
```

### ✅ 3. Particionar datos grandes

```python
# Regla: si >1 GB, particionar
if tamaño_dataset > 1_000_000_000:  # 1 GB
    df.to_parquet('datos/', partition_cols=['año', 'mes'])
else:
    df.to_parquet('datos.parquet')
```

### ✅ 4. Documentar esquemas

```python
# Comentar tipos y restricciones
"""
Schema de ventas:
- venta_id: int64 (único, no nulo)
- fecha: datetime64[ns] (rango: 2020-2024)
- monto: float64 (>0, no nulo)
- categoria: str (valores: [A, B, C, D])
- cliente_id: int64 (FK a clientes)
"""
```

### ✅ 5. Testear conversiones

```python
def test_conversion_csv_a_parquet():
    """Verifica que conversión preserve datos."""
    df_original = pd.read_csv('datos.csv')
    df_original.to_parquet('temp.parquet')
    df_convertido = pd.read_parquet('temp.parquet')

    pd.testing.assert_frame_equal(df_original, df_convertido)
```

### ✅ 6. Validar integridad después de conversión

```python
def validar_conversion(df_original, df_convertido):
    """Valida que conversión no perdió datos."""
    assert len(df_original) == len(df_convertido), "Filas no coinciden"
    assert set(df_original.columns) == set(df_convertido.columns), "Columnas no coinciden"
    assert df_original['id'].nunique() == df_convertido['id'].nunique(), "IDs únicos no coinciden"
    print("✅ Conversión validada")
```

### ✅ 7. Usar lectura selectiva con Parquet

```python
# Leer solo columnas necesarias
df_columnas = pd.read_parquet('datos.parquet', columns=['id', 'precio'])

# Aplicar filtros (partition pruning)
df_filtrado = pd.read_parquet('datos/',
                               filters=[('año', '==', 2024)])
```

### ✅ 8. Configurar PyArrow para mejor performance

```python
import pyarrow.parquet as pq

# Escribir con configuración optimizada
pq.write_table(
    pa.Table.from_pandas(df),
    'datos.parquet',
    compression='snappy',
    use_dictionary=True,  # Compresión adicional para strings repetidos
    write_statistics=True,  # Metadata para filtros
    row_group_size=100_000  # Tamaño óptimo de row groups
)
```

---

## 📚 Resumen

### Puntos Clave

1. **Formato importa**: La elección afecta performance, costo y escalabilidad
2. **Parquet para analytics**: Columnar, comprimido, eficiente
3. **JSON Lines para streaming**: Append-only, procesamiento incremental
4. **Comprimir siempre**: Snappy para balance, gzip para máxima compresión
5. **Particionar datasets grandes**: >1 GB debe estar particionado
6. **Lectura selectiva**: Usa `columns` y `filters` con Parquet
7. **Documentar schemas**: Mantén clara la estructura de datos
8. **Testear conversiones**: Validar integridad después de convertir

### Reglas de Oro

| Caso de Uso                 | Formato Recomendado |
|-----------------------------|---------------------|
| Análisis de grandes volúmenes | Parquet (snappy)  |
| Logs y eventos              | JSON Lines (gzip)   |
| API responses               | JSON                |
| Intercambio simple          | CSV                 |
| Streaming evolutivo         | Avro                |
| Data Lake storage           | Parquet particionado |

### Próximos Pasos

- **Práctica**: Convierte datasets entre formatos
- **Benchmark**: Mide diferencias de performance
- **Implementa**: Crea un conversor multi-formato
- **Optimiza**: Particiona y comprime tus datos

---

**Recursos Adicionales**:
- [Documentación Parquet](https://parquet.apache.org/docs/)
- [JSON Lines Spec](https://jsonlines.org/)
- [Apache Avro](https://avro.apache.org/docs/)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)

---

*Última actualización: 2025-10-30*
---

## 🧭 Navegación

⬅️ **Anterior**: [Calidad de Datos - Proyecto Práctico](../tema-4-calidad-datos/04-proyecto-practico/README.md) | ➡️ **Siguiente**: [02 Ejemplos](02-EJEMPLOS.md)
