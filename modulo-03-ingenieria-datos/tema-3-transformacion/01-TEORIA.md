# Tema 3: Transformación de Datos con Pandas

**Duración estimada**: 1-2 semanas
**Nivel**: Intermedio
**Prerrequisitos**: Python básico, conceptos de ETL (Tema 1), extracción de datos (Tema 2)

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

1. **Manipular DataFrames y Series** con Pandas de forma eficiente
2. **Aplicar operaciones de transformación** (filter, map, apply, lambda)
3. **Realizar agregaciones complejas** con GroupBy
4. **Combinar múltiples datasets** usando merge, join y concat
5. **Manejar valores nulos** y datos inconsistentes
6. **Optimizar el rendimiento** de transformaciones en grandes volúmenes de datos
7. **Construir pipelines de transformación** limpios y mantenibles

---

## 📚 Tabla de Contenidos

1. [Introducción a Pandas para Data Engineering](#1-introducción-a-pandas-para-data-engineering)
2. [DataFrames y Series](#2-dataframes-y-series)
3. [Lectura y Escritura de Archivos](#3-lectura-y-escritura-de-archivos)
4. [Operaciones de Transformación](#4-operaciones-de-transformación)
5. [GroupBy y Agregaciones](#5-groupby-y-agregaciones)
6. [Combinación de Datasets](#6-combinación-de-datasets)
7. [Manejo de Valores Nulos](#7-manejo-de-valores-nulos)
8. [Pivoting y Reshape](#8-pivoting-y-reshape)
9. [Optimización de Performance](#9-optimización-de-performance)
10. [Errores Comunes](#10-errores-comunes)
11. [Buenas Prácticas](#11-buenas-prácticas)

---

## 1. Introducción a Pandas para Data Engineering

### ¿Qué es Pandas?

**Pandas** es la librería de Python más utilizada para manipulación y análisis de datos estructurados. En el contexto de Data Engineering, Pandas es la herramienta central para la **fase de Transformación** en pipelines ETL/ELT.

### ¿Por qué Pandas en Data Engineering?

**Ventajas:**
- **Expresividad**: Operaciones complejas en pocas líneas de código
- **Velocidad**: Implementado en C, muy rápido para operaciones vectorizadas
- **Integración**: Compatible con múltiples formatos (CSV, JSON, Parquet, SQL)
- **Memoria eficiente**: Optimiza el uso de memoria con tipos de datos específicos
- **Comunidad**: Amplia documentación y ecosistema de herramientas

**Limitaciones:**
- **Memoria**: Todo en RAM (no ideal para datasets de +10GB)
- **Single-core**: No paraleliza automáticamente (aunque existen alternativas como Dask)
- **Mutabilidad**: Puede generar copias no deseadas si no se usa correctamente

### Cuándo usar Pandas vs SQL vs PySpark

| Herramienta | Cuándo usar                                    | Tamaño de datos          |
| ----------- | ---------------------------------------------- | ------------------------ |
| **Pandas**  | Transformaciones complejas, prototipos rápidos | < 5-10 GB                |
| **SQL**     | Agregaciones simples, joins, filtros           | Cualquier tamaño (en DB) |
| **PySpark** | Big Data, procesamiento distribuido            | > 10 GB                  |

**Regla práctica**: Si cabe en memoria, usa Pandas. Si no, usa PySpark o divide en chunks.

---

## 2. DataFrames y Series

### Series: Estructuras Unidimensionales

Una **Series** es un array unidimensional con etiquetas (índices).

```python
import pandas as pd

# Crear una Series desde una lista
ventas = pd.Series([1500, 2300, 1800, 2100],
                   index=['Lunes', 'Martes', 'Miércoles', 'Jueves'])

print(ventas)
# Lunes        1500
# Martes       2300
# Miércoles    1800
# Jueves       2100
```

**Características clave:**
- Tiene un **índice** (labels) y **valores** (data)
- Todos los valores son del mismo tipo (homogéneo)
- Se comporta como un diccionario + array de NumPy

### DataFrames: Estructuras Bidimensionales

Un **DataFrame** es una tabla bidimensional con filas y columnas etiquetadas.

```python
# Crear DataFrame desde un diccionario
datos = {
    'producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor'],
    'precio': [850.0, 25.0, 75.0, 320.0],
    'stock': [15, 120, 45, 30],
    'categoria': ['Computadoras', 'Accesorios', 'Accesorios', 'Computadoras']
}

df = pd.DataFrame(datos)
print(df)
```

**Estructura de un DataFrame:**
```
      producto  precio  stock      categoria
0       Laptop   850.0     15  Computadoras
1        Mouse    25.0    120   Accesorios
2      Teclado    75.0     45   Accesorios
3      Monitor   320.0     30  Computadoras
```

**Componentes:**
- **Index**: Etiquetas de filas (0, 1, 2, 3 por defecto)
- **Columns**: Nombres de columnas ('producto', 'precio', etc.)
- **Values**: Matriz de datos (puede tener tipos mixtos por columna)

### Acceso a Datos

```python
# Acceder a una columna (devuelve Series)
df['precio']
df.precio  # Atajo (solo si el nombre no tiene espacios)

# Acceder a múltiples columnas (devuelve DataFrame)
df[['producto', 'precio']]

# Acceder a filas por índice
df.iloc[0]  # Primera fila (por posición)
df.loc[0]   # Fila con índice 0 (por etiqueta)

# Filtrado condicional
df[df['precio'] > 100]
```

### Información Básica del DataFrame

```python
# Dimensiones
df.shape  # (4, 4) - 4 filas, 4 columnas

# Tipos de datos
df.dtypes
# producto     object
# precio      float64
# stock         int64
# categoria    object

# Información general
df.info()

# Estadísticas descriptivas
df.describe()

# Primeras/últimas filas
df.head(2)
df.tail(2)
```

---

## 3. Lectura y Escritura de Archivos

### Lectura de CSV

```python
# Lectura básica
df = pd.read_csv('datos.csv')

# Con opciones comunes
df = pd.read_csv(
    'datos.csv',
    sep=';',                    # Separador personalizado
    encoding='utf-8',           # Codificación
    decimal=',',                # Separador decimal
    thousands='.',              # Separador de miles
    na_values=['N/A', 'NULL'],  # Valores nulos personalizados
    parse_dates=['fecha'],      # Convertir columnas a fecha
    dtype={'codigo': str},      # Forzar tipos de datos
    usecols=['id', 'nombre'],   # Leer solo columnas específicas
    nrows=1000                  # Leer solo N filas
)
```

**Best practices para CSV grandes:**

```python
# Leer en chunks (bloques)
chunk_size = 10000
chunks = []

for chunk in pd.read_csv('datos_grandes.csv', chunksize=chunk_size):
    # Procesar cada chunk
    chunk_procesado = chunk[chunk['activo'] == True]
    chunks.append(chunk_procesado)

df_final = pd.concat(chunks, ignore_index=True)
```

### Lectura de otros formatos

```python
# Excel
df = pd.read_excel('datos.xlsx', sheet_name='Ventas')

# JSON
df = pd.read_json('datos.json')

# JSON Lines (cada línea es un JSON)
df = pd.read_json('datos.jsonl', lines=True)

# Parquet (formato columnar eficiente)
df = pd.read_parquet('datos.parquet')

# SQL
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql_query('SELECT * FROM ventas WHERE año = 2024', conn)

# Desde una URL
df = pd.read_csv('https://ejemplo.com/datos.csv')
```

### Escritura de Archivos

```python
# CSV
df.to_csv('salida.csv', index=False)  # index=False evita guardar el índice

# Excel
df.to_excel('salida.xlsx', sheet_name='Resultados', index=False)

# JSON
df.to_json('salida.json', orient='records', lines=True)

# Parquet (recomendado para almacenamiento)
df.to_parquet('salida.parquet', compression='snappy')

# SQL
df.to_sql('tabla_ventas', conn, if_exists='replace', index=False)
# if_exists: 'fail', 'replace', 'append'
```

---

## 4. Operaciones de Transformación

### 4.1. Filtrado (Filter)

```python
# Filtro simple
df_filtrado = df[df['precio'] > 100]

# Múltiples condiciones (AND)
df_filtrado = df[(df['precio'] > 50) & (df['stock'] > 10)]

# Múltiples condiciones (OR)
df_filtrado = df[(df['categoria'] == 'Accesorios') | (df['precio'] < 30)]

# Negación
df_filtrado = df[~(df['categoria'] == 'Computadoras')]

# isin() - pertenencia a una lista
categorias_deseadas = ['Accesorios', 'Periféricos']
df_filtrado = df[df['categoria'].isin(categorias_deseadas)]

# str.contains() - búsqueda de texto
df_filtrado = df[df['producto'].str.contains('Laptop', case=False, na=False)]
```

### 4.2. Transformación de Columnas

```python
# Crear nueva columna con cálculo
df['precio_con_iva'] = df['precio'] * 1.21

# Operaciones entre columnas
df['valor_inventario'] = df['precio'] * df['stock']

# Transformación condicional con np.where
import numpy as np
df['tipo_precio'] = np.where(df['precio'] > 100, 'Caro', 'Económico')

# Múltiples condiciones con np.select
condiciones = [
    df['precio'] < 50,
    (df['precio'] >= 50) & (df['precio'] < 200),
    df['precio'] >= 200
]
valores = ['Económico', 'Medio', 'Premium']
df['rango_precio'] = np.select(condiciones, valores, default='Desconocido')
```

### 4.3. Map - Mapeo de Valores

```python
# Mapeo con diccionario
mapeo_categorias = {
    'Computadoras': 'COMP',
    'Accesorios': 'ACC',
    'Periféricos': 'PERI'
}
df['categoria_codigo'] = df['categoria'].map(mapeo_categorias)

# Map con función
def calcular_descuento(precio: float) -> float:
    if precio > 500:
        return precio * 0.15
    elif precio > 200:
        return precio * 0.10
    return precio * 0.05

df['descuento'] = df['precio'].map(calcular_descuento)
```

### 4.4. Apply - Aplicar Funciones

```python
# Apply a una columna (Series)
df['precio_redondeado'] = df['precio'].apply(round)

# Apply a múltiples columnas (axis=1)
def calcular_urgencia_restock(row):
    if row['stock'] < 10:
        return 'URGENTE'
    elif row['stock'] < 30:
        return 'MEDIO'
    return 'NORMAL'

df['urgencia_restock'] = df.apply(calcular_urgencia_restock, axis=1)

# Apply con lambda (funciones anónimas)
df['precio_formateado'] = df['precio'].apply(lambda x: f'${x:.2f}')

# Apply con argumentos adicionales
def aplicar_impuesto(precio: float, tasa_impuesto: float) -> float:
    return precio * (1 + tasa_impuesto)

df['precio_con_impuesto'] = df['precio'].apply(aplicar_impuesto, tasa_impuesto=0.21)
```

### 4.5. Operaciones Vectorizadas (Más Eficientes)

```python
# ❌ LENTO: Usar apply con operaciones simples
df['total'] = df.apply(lambda row: row['precio'] * row['cantidad'], axis=1)

# ✅ RÁPIDO: Operaciones vectorizadas
df['total'] = df['precio'] * df['cantidad']

# ❌ LENTO: Bucle manual
totales = []
for idx, row in df.iterrows():
    totales.append(row['precio'] * row['cantidad'])
df['total'] = totales

# ✅ RÁPIDO: Operaciones vectorizadas con NumPy
df['total'] = np.multiply(df['precio'].values, df['cantidad'].values)
```

**Regla de oro**: Siempre prefiere operaciones vectorizadas sobre `apply()`, y `apply()` sobre bucles `iterrows()`.

---

## 5. GroupBy y Agregaciones

### 5.1. GroupBy Básico

```python
# Agrupar por una columna y calcular suma
df.groupby('categoria')['precio'].sum()

# Múltiples agregaciones
df.groupby('categoria')['precio'].agg(['sum', 'mean', 'count', 'min', 'max'])

# Agrupar por múltiples columnas
df.groupby(['categoria', 'marca'])['precio'].mean()
```

### 5.2. Agregaciones Personalizadas

```python
# Agregaciones con nombres personalizados
resultado = df.groupby('categoria').agg(
    precio_promedio=('precio', 'mean'),
    precio_total=('precio', 'sum'),
    cantidad_productos=('producto', 'count'),
    stock_total=('stock', 'sum')
).reset_index()

# Función de agregación personalizada
def rango_precios(serie):
    return serie.max() - serie.min()

df.groupby('categoria')['precio'].agg(['mean', rango_precios])
```

### 5.3. Transform - Mantener Dimensionalidad

```python
# Transform: devuelve un valor por cada fila original
df['precio_promedio_categoria'] = df.groupby('categoria')['precio'].transform('mean')

# Ahora cada fila tiene el promedio de su categoría
# Útil para calcular desviaciones, porcentajes, etc.
df['desviacion_precio'] = df['precio'] - df['precio_promedio_categoria']
df['porcentaje_del_promedio'] = (df['precio'] / df['precio_promedio_categoria']) * 100
```

### 5.4. Filter - Filtrar Grupos Completos

```python
# Mantener solo grupos con más de 5 productos
df_filtrado = df.groupby('categoria').filter(lambda x: len(x) > 5)

# Mantener solo categorías con precio promedio > 100
df_filtrado = df.groupby('categoria').filter(lambda x: x['precio'].mean() > 100)
```

---

## 6. Combinación de Datasets

### 6.1. Concat - Concatenación

```python
# Concatenar verticalmente (apilar filas)
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

df_concat = pd.concat([df1, df2], ignore_index=True)
# ignore_index=True resetea el índice

# Concatenar horizontalmente (apilar columnas)
df_concat = pd.concat([df1, df2], axis=1)
```

### 6.2. Merge - Uniones SQL-style

```python
# Datos de ejemplo
ventas = pd.DataFrame({
    'venta_id': [1, 2, 3],
    'producto_id': [101, 102, 103],
    'cantidad': [2, 1, 5]
})

productos = pd.DataFrame({
    'producto_id': [101, 102, 103],
    'nombre': ['Laptop', 'Mouse', 'Teclado'],
    'precio': [850, 25, 75]
})

# INNER JOIN (por defecto)
df_inner = pd.merge(ventas, productos, on='producto_id', how='inner')

# LEFT JOIN (mantiene todas las filas de la izquierda)
df_left = pd.merge(ventas, productos, on='producto_id', how='left')

# RIGHT JOIN (mantiene todas las filas de la derecha)
df_right = pd.merge(ventas, productos, on='producto_id', how='right')

# OUTER JOIN (mantiene todas las filas de ambos)
df_outer = pd.merge(ventas, productos, on='producto_id', how='outer')

# Merge con columnas de diferentes nombres
df_merge = pd.merge(
    ventas,
    productos,
    left_on='producto_id',
    right_on='id_producto'
)

# Merge con múltiples columnas
df_merge = pd.merge(
    df1,
    df2,
    on=['columna1', 'columna2'],
    how='inner'
)
```

### 6.3. Join - Unión por Índice

```python
# Join por índice (similar a merge pero usa índices)
df1 = pd.DataFrame({'A': [1, 2]}, index=['x', 'y'])
df2 = pd.DataFrame({'B': [3, 4]}, index=['x', 'y'])

df_joined = df1.join(df2)

# Join con sufijos para columnas duplicadas
df_joined = df1.join(df2, how='left', lsuffix='_izq', rsuffix='_der')
```

### 6.4. Diferencias: Merge vs Join vs Concat

| Operación    | Cuándo usar                        | Comportamiento                    |
| ------------ | ---------------------------------- | --------------------------------- |
| **merge()**  | Unir por columnas comunes (llaves) | SQL-style joins                   |
| **join()**   | Unir por índices                   | Similar a merge pero usa índices  |
| **concat()** | Apilar DataFrames                  | Concatenación vertical/horizontal |

---

## 7. Manejo de Valores Nulos

### 7.1. Detección de Nulos

```python
# Verificar si hay nulos
df.isnull()  # DataFrame de booleanos
df.isnull().sum()  # Cantidad de nulos por columna

# Verificar si hay valores NO nulos
df.notnull()

# Filtrar filas con cualquier nulo
df_con_nulos = df[df.isnull().any(axis=1)]

# Filtrar filas sin nulos
df_sin_nulos = df.dropna()
```

### 7.2. Eliminación de Nulos

```python
# Eliminar filas con cualquier nulo
df_clean = df.dropna()

# Eliminar filas donde TODAS las columnas son nulas
df_clean = df.dropna(how='all')

# Eliminar filas con nulos en columnas específicas
df_clean = df.dropna(subset=['precio', 'stock'])

# Eliminar columnas con nulos
df_clean = df.dropna(axis=1)
```

### 7.3. Rellenado de Nulos

```python
# Rellenar con un valor constante
df['precio'].fillna(0, inplace=True)

# Rellenar con la media/mediana
df['precio'].fillna(df['precio'].mean(), inplace=True)
df['stock'].fillna(df['stock'].median(), inplace=True)

# Forward fill (propagar último valor válido hacia adelante)
df['categoria'].fillna(method='ffill', inplace=True)

# Backward fill (propagar siguiente valor válido hacia atrás)
df['categoria'].fillna(method='bfill', inplace=True)

# Rellenar con valores diferentes por columna
valores_relleno = {
    'precio': 0,
    'stock': df['stock'].median(),
    'categoria': 'Desconocido'
}
df.fillna(valores_relleno, inplace=True)
```

### 7.4. Interpolación

```python
# Interpolación lineal (útil para series temporales)
df['temperatura'].interpolate(method='linear', inplace=True)

# Interpolación por tiempo
df['valor'].interpolate(method='time', inplace=True)
```

---

## 8. Pivoting y Reshape

### 8.1. Pivot - Tabla Dinámica

```python
# Datos de ejemplo
ventas = pd.DataFrame({
    'fecha': ['2024-01', '2024-01', '2024-02', '2024-02'],
    'producto': ['Laptop', 'Mouse', 'Laptop', 'Mouse'],
    'ventas': [10, 50, 15, 60]
})

# Crear tabla dinámica
pivot = ventas.pivot(index='fecha', columns='producto', values='ventas')
#         Laptop  Mouse
# 2024-01     10     50
# 2024-02     15     60
```

### 8.2. Pivot Table - Con Agregaciones

```python
# Pivot table con agregación
pivot_table = pd.pivot_table(
    ventas,
    values='ventas',
    index='fecha',
    columns='producto',
    aggfunc='sum',  # Puede ser: 'mean', 'count', 'sum', etc.
    fill_value=0    # Reemplazar NaN con 0
)
```

### 8.3. Melt - Formato Largo

```python
# Convertir de formato ancho a largo
df_ancho = pd.DataFrame({
    'producto': ['Laptop', 'Mouse'],
    'ene': [10, 50],
    'feb': [15, 60]
})

df_largo = pd.melt(
    df_ancho,
    id_vars=['producto'],
    value_vars=['ene', 'feb'],
    var_name='mes',
    value_name='ventas'
)
#   producto mes  ventas
# 0   Laptop ene      10
# 1    Mouse ene      50
# 2   Laptop feb      15
# 3    Mouse feb      60
```

### 8.4. Stack y Unstack

```python
# Stack: columnas -> índice (hace el df más largo)
df_stacked = df.stack()

# Unstack: índice -> columnas (hace el df más ancho)
df_unstacked = df.unstack()
```

---

## 9. Optimización de Performance

### 9.1. Tipos de Datos Eficientes

```python
# Verificar uso de memoria
df.info(memory_usage='deep')

# Optimizar tipos numéricos
df['edad'] = df['edad'].astype('int8')  # Si valores 0-127
df['cantidad'] = df['cantidad'].astype('int16')  # Si valores 0-32,767

# Optimizar strings con category
df['categoria'] = df['categoria'].astype('category')
# Ahorro significativo si hay muchos valores repetidos
```

### 9.2. Operaciones Vectorizadas

```python
# ❌ LENTO
resultado = []
for idx, row in df.iterrows():
    resultado.append(row['a'] * row['b'])
df['resultado'] = resultado

# ✅ RÁPIDO
df['resultado'] = df['a'] * df['b']
```

### 9.3. Procesamiento en Chunks

```python
# Para archivos grandes
def procesar_chunk(chunk):
    chunk['total'] = chunk['precio'] * chunk['cantidad']
    return chunk[chunk['total'] > 1000]

chunks_procesados = []
for chunk in pd.read_csv('archivo_grande.csv', chunksize=10000):
    chunks_procesados.append(procesar_chunk(chunk))

df_final = pd.concat(chunks_procesados, ignore_index=True)
```

### 9.4. eval() y query() para Expresiones

```python
# Para operaciones complejas, eval() puede ser más rápido
df['resultado'] = df.eval('(precio * cantidad) + (precio * 0.21)')

# query() para filtrado
df_filtrado = df.query('precio > 100 and stock < 50')
```

### 9.5. Evitar Copias Innecesarias

```python
# ❌ Crea copias
df_temp = df
df_temp['nueva_col'] = 0  # Modifica el original también

# ✅ Copia explícita
df_temp = df.copy()
df_temp['nueva_col'] = 0  # No afecta al original

# ✅ Operación in-place (sin copia)
df.drop('columna', axis=1, inplace=True)
```

---

## 10. Errores Comunes

### Error 1: SettingWithCopyWarning

```python
# ❌ INCORRECTO - Advertencia de copia
df_filtrado = df[df['precio'] > 100]
df_filtrado['descuento'] = 0.1  # ⚠️ Warning!

# ✅ CORRECTO - Copia explícita
df_filtrado = df[df['precio'] > 100].copy()
df_filtrado['descuento'] = 0.1
```

### Error 2: Modificar Durante Iteración

```python
# ❌ INCORRECTO
for idx, row in df.iterrows():
    df.loc[idx, 'nueva_col'] = row['precio'] * 2

# ✅ CORRECTO - Operación vectorizada
df['nueva_col'] = df['precio'] * 2
```

### Error 3: Comparación de Strings sin Normalizar

```python
# ❌ INCORRECTO - Sensible a mayúsculas/espacios
df_filtrado = df[df['categoria'] == 'accesorios']

# ✅ CORRECTO
df_filtrado = df[df['categoria'].str.lower().str.strip() == 'accesorios']
```

### Error 4: No Manejar Valores Nulos en Comparaciones

```python
# ❌ INCORRECTO - NaN no se compara correctamente
df_filtrado = df[df['precio'] > 100]  # Descarta NaN

# ✅ CORRECTO - Manejar nulos explícitamente
df_filtrado = df[(df['precio'] > 100) | (df['precio'].isnull())]
```

### Error 5: Merge sin Verificar Duplicados

```python
# ❌ RIESGO - Puede duplicar filas inesperadamente
df_merged = pd.merge(ventas, productos, on='producto_id')

# ✅ CORRECTO - Verificar antes
print(f"Filas antes: {len(ventas)}")
df_merged = pd.merge(ventas, productos, on='producto_id', validate='m:1')
print(f"Filas después: {len(df_merged)}")
# validate='m:1' asegura que productos no tenga duplicados
```

---

## 11. Buenas Prácticas

### 1. Nombres Descriptivos y Consistentes

```python
# ❌ EVITAR
df1 = pd.read_csv('data.csv')
df2 = df1[df1['x'] > 10]
df3 = df2.groupby('y').sum()

# ✅ MEJOR
ventas_raw = pd.read_csv('ventas.csv')
ventas_filtradas = ventas_raw[ventas_raw['precio'] > 10]
ventas_por_categoria = ventas_filtradas.groupby('categoria').sum()
```

### 2. Validar Datos de Entrada

```python
def transformar_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma datos de ventas."""
    # Validaciones
    columnas_requeridas = ['producto_id', 'precio', 'cantidad']
    columnas_faltantes = set(columnas_requeridas) - set(df.columns)

    if columnas_faltantes:
        raise ValueError(f"Columnas faltantes: {columnas_faltantes}")

    if df.empty:
        raise ValueError("DataFrame vacío")

    # Transformaciones
    df_transformado = df.copy()
    df_transformado['total'] = df_transformado['precio'] * df_transformado['cantidad']

    return df_transformado
```

### 3. Documentar Transformaciones Complejas

```python
def calcular_metricas_cliente(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas agregadas por cliente.

    Args:
        df: DataFrame con columnas ['cliente_id', 'fecha', 'monto']

    Returns:
        DataFrame con métricas por cliente:
        - total_compras: suma de montos
        - promedio_compra: promedio de montos
        - num_compras: cantidad de compras
        - ultima_compra: fecha más reciente
    """
    metricas = df.groupby('cliente_id').agg(
        total_compras=('monto', 'sum'),
        promedio_compra=('monto', 'mean'),
        num_compras=('monto', 'count'),
        ultima_compra=('fecha', 'max')
    ).reset_index()

    return metricas
```

### 4. Usar Method Chaining para Pipelines

```python
# ✅ Pipeline claro y legible
df_procesado = (
    df
    .dropna(subset=['precio', 'cantidad'])
    .assign(total=lambda x: x['precio'] * x['cantidad'])
    .query('total > 100')
    .groupby('categoria')
    .agg({'total': 'sum', 'cantidad': 'sum'})
    .reset_index()
    .sort_values('total', ascending=False)
)
```

### 5. Separar Lógica de Negocio de Transformaciones

```python
# ❌ EVITAR - Todo mezclado
def procesar():
    df = pd.read_csv('ventas.csv')
    df['total'] = df['precio'] * df['cantidad']
    df = df[df['total'] > 100]
    df.to_csv('resultado.csv')

# ✅ MEJOR - Funciones separadas
def cargar_ventas(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def calcular_total(df: pd.DataFrame) -> pd.DataFrame:
    df_copia = df.copy()
    df_copia['total'] = df_copia['precio'] * df_copia['cantidad']
    return df_copia

def filtrar_ventas_mayores(df: pd.DataFrame, umbral: float) -> pd.DataFrame:
    return df[df['total'] > umbral]

def guardar_resultado(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)

# Orquestación clara
def pipeline_ventas():
    df = cargar_ventas('ventas.csv')
    df = calcular_total(df)
    df = filtrar_ventas_mayores(df, umbral=100)
    guardar_resultado(df, 'resultado.csv')
```

### 6. Manejo Explícito de Errores

```python
def procesar_ventas(path: str) -> pd.DataFrame:
    """Procesa archivo de ventas con manejo de errores."""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Archivo vacío: {path}")

    if 'precio' not in df.columns:
        raise ValueError("Columna 'precio' no encontrada en el archivo")

    # Validar tipos de datos
    if not pd.api.types.is_numeric_dtype(df['precio']):
        raise TypeError("La columna 'precio' debe ser numérica")

    return df
```

### 7. Testing de Transformaciones

```python
import pytest

def test_calcular_total():
    """Test de la función calcular_total."""
    # Arrange
    df_input = pd.DataFrame({
        'precio': [100, 200],
        'cantidad': [2, 3]
    })

    # Act
    df_resultado = calcular_total(df_input)

    # Assert
    assert 'total' in df_resultado.columns
    assert df_resultado['total'].tolist() == [200, 600]
    assert len(df_resultado) == 2
```

---

## 📝 Resumen

En este tema has aprendido:

✅ **DataFrames y Series**: Estructuras fundamentales de Pandas
✅ **Operaciones de transformación**: filter, map, apply, lambda
✅ **GroupBy y agregaciones**: Cálculos por grupos
✅ **Combinación de datasets**: merge, join, concat
✅ **Manejo de valores nulos**: Detección, eliminación y rellenado
✅ **Pivoting y reshape**: Cambiar estructura de datos
✅ **Optimización**: Tipos eficientes, vectorización, chunks
✅ **Buenas prácticas**: Código limpio, mantenible y testeable

### Próximos Pasos

1. Revisa los **ejemplos prácticos** en `02-EJEMPLOS.md`
2. Practica con los **ejercicios** en `03-EJERCICIOS.md`
3. Construye el **proyecto práctico** en `04-proyecto-practico/`

---

**Tiempo de lectura estimado**: 45-60 minutos
**Palabras**: ~4,500
**Última actualización**: 2025-10-30
