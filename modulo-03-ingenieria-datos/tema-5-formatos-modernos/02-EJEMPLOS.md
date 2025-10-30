# Ejemplos Prácticos: Formatos de Datos Modernos

**Objetivo**: Aplicar los conceptos de formatos modernos (JSON, Parquet, JSON Lines) y compresión en casos reales de Data Engineering.

---

## 📋 Índice de Ejemplos

1. [Conversión CSV → Parquet con Particiones](#ejemplo-1-conversión-csv--parquet-con-particiones)
2. [JSON Nested → Parquet con Esquema](#ejemplo-2-json-nested--parquet-con-esquema)
3. [Comparación Tamaño/Velocidad entre Formatos](#ejemplo-3-comparación-tamañovelocidad-entre-formatos)
4. [Pipeline Multi-formato con Compresión](#ejemplo-4-pipeline-multi-formato-con-compresión)

---

## Ejemplo 1: Conversión CSV → Parquet con Particiones

### 📖 Contexto

Tenemos un CSV de ventas históricas (varios GB) que queremos convertir a Parquet particionado por año y mes para optimizar consultas futuras.

### 🎯 Objetivo

- Convertir CSV grande a Parquet
- Aplicar compresión snappy
- Particionar por año y mes
- Comparar tamaños y tiempos

### 💻 Código

```python
import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime, timedelta
import time


def generar_datos_ventas(num_registros: int = 100000) -> pd.DataFrame:
    """
    Genera datos de ventas sintéticos para el ejemplo.

    Args:
        num_registros: Cantidad de registros a generar

    Returns:
        DataFrame con datos de ventas
    """
    np.random.seed(42)

    # Generar fechas aleatorias entre 2020 y 2024
    fecha_inicio = datetime(2020, 1, 1)
    fecha_fin = datetime(2024, 12, 31)
    dias = (fecha_fin - fecha_inicio).days

    fechas = [fecha_inicio + timedelta(days=int(x))
              for x in np.random.randint(0, dias, num_registros)]

    # Generar datos
    datos = {
        'venta_id': range(1, num_registros + 1),
        'fecha': fechas,
        'cliente_id': np.random.randint(1000, 9999, num_registros),
        'producto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor',
                                     'Tablet', 'Auriculares', 'Webcam'], num_registros),
        'cantidad': np.random.randint(1, 10, num_registros),
        'precio_unitario': np.round(np.random.uniform(10, 1000, num_registros), 2),
        'descuento': np.round(np.random.uniform(0, 0.3, num_registros), 2),
        'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], num_registros),
        'vendedor': np.random.choice([f'Vendedor_{i}' for i in range(1, 21)], num_registros)
    }

    df = pd.DataFrame(datos)

    # Calcular total
    df['total'] = df['cantidad'] * df['precio_unitario'] * (1 - df['descuento'])
    df['total'] = df['total'].round(2)

    return df


def obtener_tamanio_archivo(ruta: str) -> float:
    """
    Obtiene el tamaño de un archivo o directorio en MB.

    Args:
        ruta: Ruta del archivo o directorio

    Returns:
        Tamaño en MB
    """
    ruta_path = Path(ruta)

    if ruta_path.is_file():
        return ruta_path.stat().st_size / (1024 * 1024)
    elif ruta_path.is_dir():
        total = sum(f.stat().st_size for f in ruta_path.rglob('*') if f.is_file())
        return total / (1024 * 1024)
    else:
        return 0.0


def convertir_csv_a_parquet_particionado(
    ruta_csv: str,
    ruta_parquet: str,
    columnas_particion: list,
    compresion: str = 'snappy'
) -> dict:
    """
    Convierte CSV a Parquet particionado y compara métricas.

    Args:
        ruta_csv: Ruta del archivo CSV
        ruta_parquet: Ruta del directorio Parquet de salida
        columnas_particion: Columnas para particionar
        compresion: Algoritmo de compresión

    Returns:
        Diccionario con métricas de conversión
    """
    metricas = {}

    # 1. LEER CSV
    print("📖 Leyendo CSV...")
    inicio = time.time()
    df = pd.read_csv(ruta_csv, parse_dates=['fecha'])
    metricas['tiempo_lectura_csv'] = time.time() - inicio
    metricas['tamanio_csv_mb'] = obtener_tamanio_archivo(ruta_csv)
    metricas['num_registros'] = len(df)

    print(f"✅ CSV leído: {len(df):,} registros en {metricas['tiempo_lectura_csv']:.2f}s")
    print(f"   Tamaño CSV: {metricas['tamanio_csv_mb']:.2f} MB")

    # 2. PREPARAR COLUMNAS DE PARTICIÓN
    df['año'] = df['fecha'].dt.year
    df['mes'] = df['fecha'].dt.month

    # 3. ESCRIBIR PARQUET PARTICIONADO
    print(f"\n💾 Escribiendo Parquet particionado por {columnas_particion}...")
    inicio = time.time()
    df.to_parquet(
        ruta_parquet,
        engine='pyarrow',
        compression=compresion,
        partition_cols=columnas_particion,
        index=False
    )
    metricas['tiempo_escritura_parquet'] = time.time() - inicio
    metricas['tamanio_parquet_mb'] = obtener_tamanio_archivo(ruta_parquet)

    print(f"✅ Parquet escrito en {metricas['tiempo_escritura_parquet']:.2f}s")
    print(f"   Tamaño Parquet: {metricas['tamanio_parquet_mb']:.2f} MB")

    # 4. CALCULAR REDUCCIÓN
    metricas['reduccion_tamanio_pct'] = (
        (metricas['tamanio_csv_mb'] - metricas['tamanio_parquet_mb']) /
        metricas['tamanio_csv_mb'] * 100
    )

    # 5. CONTAR PARTICIONES
    num_particiones = len(list(Path(ruta_parquet).rglob('*.parquet')))
    metricas['num_particiones'] = num_particiones

    print(f"\n📊 Reducción de tamaño: {metricas['reduccion_tamanio_pct']:.1f}%")
    print(f"📁 Particiones creadas: {num_particiones}")

    # 6. PROBAR LECTURA SELECTIVA
    print(f"\n🔍 Probando lectura selectiva (año=2024)...")
    inicio = time.time()
    df_2024 = pd.read_parquet(ruta_parquet, filters=[('año', '==', 2024)])
    metricas['tiempo_lectura_filtrada'] = time.time() - inicio
    metricas['registros_filtrados'] = len(df_2024)

    print(f"✅ Leídos {len(df_2024):,} registros en {metricas['tiempo_lectura_filtrada']:.2f}s")

    return metricas


def main():
    """Ejecuta el ejemplo completo."""
    print("=" * 70)
    print("EJEMPLO 1: Conversión CSV → Parquet con Particiones")
    print("=" * 70)

    # Rutas
    ruta_csv = 'ventas.csv'
    ruta_parquet = 'ventas_parquet'

    # 1. Generar datos
    print("\n🔧 Generando datos de ejemplo...")
    df = generar_datos_ventas(num_registros=100000)
    df.to_csv(ruta_csv, index=False)
    print(f"✅ Generados {len(df):,} registros")

    # 2. Convertir
    metricas = convertir_csv_a_parquet_particionado(
        ruta_csv=ruta_csv,
        ruta_parquet=ruta_parquet,
        columnas_particion=['año', 'mes'],
        compresion='snappy'
    )

    # 3. Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE MÉTRICAS")
    print("=" * 70)
    print(f"Registros totales:        {metricas['num_registros']:,}")
    print(f"Tamaño CSV:               {metricas['tamanio_csv_mb']:.2f} MB")
    print(f"Tamaño Parquet:           {metricas['tamanio_parquet_mb']:.2f} MB")
    print(f"Reducción:                {metricas['reduccion_tamanio_pct']:.1f}%")
    print(f"Particiones:              {metricas['num_particiones']}")
    print(f"Tiempo lectura CSV:       {metricas['tiempo_lectura_csv']:.2f}s")
    print(f"Tiempo escritura Parquet: {metricas['tiempo_escritura_parquet']:.2f}s")
    print(f"Tiempo lectura filtrada:  {metricas['tiempo_lectura_filtrada']:.2f}s")


if __name__ == '__main__':
    main()
```

### 📊 Resultados Esperados

```
Registros totales:        100,000
Tamaño CSV:               12.5 MB
Tamaño Parquet:           2.1 MB
Reducción:                83.2%
Particiones:              60 (5 años × 12 meses)
Tiempo lectura CSV:       0.35s
Tiempo escritura Parquet: 0.48s
Tiempo lectura filtrada:  0.08s (solo lee 1 partición)
```

### 🎓 Aprendizajes

1. **Compresión efectiva**: Parquet reduce el tamaño ~83% vs CSV
2. **Particionamiento**: 60 particiones (una por mes)
3. **Lectura selectiva**: 4x más rápida cuando filtramos por partición
4. **Trade-off**: Escritura ligeramente más lenta, pero lectura mucho más rápida

---

## Ejemplo 2: JSON Nested → Parquet con Esquema

### 📖 Contexto

Recibimos datos de pedidos desde una API con estructura nested (items dentro de pedidos). Queremos normalizarlos y guardarlos en Parquet.

### 🎯 Objetivo

- Normalizar JSON anidado
- Definir schema explícito
- Guardar como Parquet con tipos correctos

### 💻 Código

```python
import pandas as pd
import json
from typing import Dict, List
import pyarrow as pa
import pyarrow.parquet as pq


def generar_pedidos_json(num_pedidos: int = 1000) -> List[Dict]:
    """
    Genera datos de pedidos con estructura nested.

    Args:
        num_pedidos: Número de pedidos a generar

    Returns:
        Lista de diccionarios con pedidos
    """
    import numpy as np
    from datetime import datetime, timedelta

    np.random.seed(42)
    pedidos = []

    productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Tablet',
                 'Auriculares', 'Webcam', 'Router', 'Cable HDMI']

    for pedido_id in range(1, num_pedidos + 1):
        # Generar fecha aleatoria
        fecha = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 300))

        # Generar items (1-5 productos por pedido)
        num_items = np.random.randint(1, 6)
        items = []
        total = 0

        for _ in range(num_items):
            producto = np.random.choice(productos)
            cantidad = np.random.randint(1, 5)
            precio = np.round(np.random.uniform(10, 500), 2)
            subtotal = cantidad * precio
            total += subtotal

            items.append({
                'producto': producto,
                'cantidad': int(cantidad),
                'precio_unitario': float(precio),
                'subtotal': float(np.round(subtotal, 2))
            })

        # Crear pedido
        pedido = {
            'pedido_id': pedido_id,
            'fecha': fecha.strftime('%Y-%m-%d'),
            'cliente': {
                'cliente_id': int(np.random.randint(1000, 9999)),
                'nombre': f'Cliente_{np.random.randint(1, 500)}',
                'email': f'cliente{np.random.randint(1, 500)}@email.com'
            },
            'items': items,
            'total': float(np.round(total, 2)),
            'estado': np.random.choice(['Pendiente', 'Enviado', 'Entregado', 'Cancelado']),
            'metodo_pago': np.random.choice(['Tarjeta', 'Transferencia', 'Efectivo'])
        }

        pedidos.append(pedido)

    return pedidos


def normalizar_pedidos(pedidos: List[Dict]) -> tuple:
    """
    Normaliza estructura nested de pedidos en dos DataFrames.

    Args:
        pedidos: Lista de pedidos con estructura nested

    Returns:
        Tupla (df_pedidos, df_items)
    """
    # 1. NORMALIZAR DATOS DE CLIENTE (nested dict)
    pedidos_flat = []

    for p in pedidos:
        pedido_flat = {
            'pedido_id': p['pedido_id'],
            'fecha': p['fecha'],
            'cliente_id': p['cliente']['cliente_id'],
            'cliente_nombre': p['cliente']['nombre'],
            'cliente_email': p['cliente']['email'],
            'total': p['total'],
            'estado': p['estado'],
            'metodo_pago': p['metodo_pago']
        }
        pedidos_flat.append(pedido_flat)

    df_pedidos = pd.DataFrame(pedidos_flat)

    # 2. NORMALIZAR ITEMS (nested array)
    items_flat = []

    for p in pedidos:
        for item in p['items']:
            item_flat = {
                'pedido_id': p['pedido_id'],
                'producto': item['producto'],
                'cantidad': item['cantidad'],
                'precio_unitario': item['precio_unitario'],
                'subtotal': item['subtotal']
            }
            items_flat.append(item_flat)

    df_items = pd.DataFrame(items_flat)

    return df_pedidos, df_items


def guardar_con_schema_explicito(df: pd.DataFrame, ruta: str, schema: pa.Schema) -> None:
    """
    Guarda DataFrame en Parquet con schema explícito de PyArrow.

    Args:
        df: DataFrame a guardar
        ruta: Ruta del archivo Parquet
        schema: Schema de PyArrow
    """
    # Convertir DataFrame a PyArrow Table con schema explícito
    table = pa.Table.from_pandas(df, schema=schema)

    # Escribir con configuración optimizada
    pq.write_table(
        table,
        ruta,
        compression='snappy',
        use_dictionary=True,  # Compresión adicional para strings repetidos
        write_statistics=True,  # Estadísticas para filtros
        row_group_size=50000
    )


def main():
    """Ejecuta el ejemplo completo."""
    print("=" * 70)
    print("EJEMPLO 2: JSON Nested → Parquet con Esquema")
    print("=" * 70)

    # 1. GENERAR DATOS
    print("\n🔧 Generando datos de pedidos con estructura nested...")
    pedidos = generar_pedidos_json(num_pedidos=1000)
    print(f"✅ Generados {len(pedidos)} pedidos")

    # Ejemplo de estructura
    print("\n📄 Ejemplo de estructura JSON:")
    print(json.dumps(pedidos[0], indent=2, ensure_ascii=False))

    # 2. GUARDAR COMO JSON
    with open('pedidos.json', 'w', encoding='utf-8') as f:
        json.dump(pedidos, f, indent=2, ensure_ascii=False)
    print("\n💾 Guardado como pedidos.json")

    # 3. NORMALIZAR
    print("\n🔄 Normalizando estructura nested...")
    df_pedidos, df_items = normalizar_pedidos(pedidos)

    print(f"\n✅ Normalización completada:")
    print(f"   - Pedidos: {len(df_pedidos)} registros")
    print(f"   - Items: {len(df_items)} registros")

    # Mostrar schemas inferidos
    print(f"\n📊 Schema de pedidos:")
    print(df_pedidos.dtypes)

    # 4. DEFINIR SCHEMAS EXPLÍCITOS
    schema_pedidos = pa.schema([
        ('pedido_id', pa.int32()),
        ('fecha', pa.date32()),
        ('cliente_id', pa.int32()),
        ('cliente_nombre', pa.string()),
        ('cliente_email', pa.string()),
        ('total', pa.float32()),
        ('estado', pa.dictionary(pa.int8(), pa.string())),  # Enum eficiente
        ('metodo_pago', pa.dictionary(pa.int8(), pa.string()))
    ])

    schema_items = pa.schema([
        ('pedido_id', pa.int32()),
        ('producto', pa.dictionary(pa.int8(), pa.string())),
        ('cantidad', pa.int16()),
        ('precio_unitario', pa.float32()),
        ('subtotal', pa.float32())
    ])

    print("\n📐 Schemas explícitos definidos con tipos optimizados")

    # 5. PREPARAR DATOS PARA SCHEMA
    df_pedidos['fecha'] = pd.to_datetime(df_pedidos['fecha'])

    # 6. GUARDAR COMO PARQUET
    print("\n💾 Guardando como Parquet con schema explícito...")
    guardar_con_schema_explicito(df_pedidos, 'pedidos.parquet', schema_pedidos)
    guardar_con_schema_explicito(df_items, 'items.parquet', schema_items)

    # 7. COMPARAR TAMAÑOS
    import os
    tamanio_json = os.path.getsize('pedidos.json') / (1024 * 1024)
    tamanio_pedidos = os.path.getsize('pedidos.parquet') / (1024 * 1024)
    tamanio_items = os.path.getsize('items.parquet') / (1024 * 1024)
    tamanio_parquet_total = tamanio_pedidos + tamanio_items

    print("\n📊 COMPARACIÓN DE TAMAÑOS:")
    print(f"   JSON original:        {tamanio_json:.2f} MB")
    print(f"   Parquet pedidos:      {tamanio_pedidos:.2f} MB")
    print(f"   Parquet items:        {tamanio_items:.2f} MB")
    print(f"   Parquet total:        {tamanio_parquet_total:.2f} MB")
    print(f"   Reducción:            {((tamanio_json - tamanio_parquet_total) / tamanio_json * 100):.1f}%")

    # 8. VERIFICAR LECTURA
    print("\n🔍 Verificando lectura...")
    df_pedidos_leido = pd.read_parquet('pedidos.parquet')
    df_items_leido = pd.read_parquet('items.parquet')

    print(f"✅ Pedidos leídos: {len(df_pedidos_leido)}")
    print(f"✅ Items leídos: {len(df_items_leido)}")

    # 9. EJEMPLO DE CONSULTA
    print("\n🔍 Ejemplo de consulta: Pedidos con total > 1000")
    pedidos_altos = df_pedidos_leido[df_pedidos_leido['total'] > 1000]
    print(f"   Encontrados: {len(pedidos_altos)} pedidos")


if __name__ == '__main__':
    main()
```

### 📊 Resultados Esperados

```
JSON original:        1.85 MB
Parquet pedidos:      0.18 MB
Parquet items:        0.12 MB
Parquet total:        0.30 MB
Reducción:            83.8%
```

### 🎓 Aprendizajes

1. **Normalización**: JSON nested se divide en múltiples tablas relacionales
2. **Schemas explícitos**: Uso de tipos eficientes (dictionary para enums)
3. **Compresión**: ~84% de reducción vs JSON
4. **Tipos optimizados**: int32 en lugar de int64, float32 en lugar de float64

---

## Ejemplo 3: Comparación Tamaño/Velocidad entre Formatos

### 📖 Contexto

Queremos comparar CSV, JSON, JSON Lines y Parquet en términos de tamaño en disco, velocidad de escritura y velocidad de lectura.

### 🎯 Objetivo

- Generar dataset de prueba
- Guardar en todos los formatos
- Medir tiempos y tamaños
- Crear tabla comparativa

### 💻 Código

```python
import pandas as pd
import numpy as np
import time
import os
from pathlib import Path


def generar_dataset_benchmark(num_registros: int = 100000) -> pd.DataFrame:
    """
    Genera dataset para benchmark con tipos variados.

    Args:
        num_registros: Número de registros

    Returns:
        DataFrame de prueba
    """
    np.random.seed(42)

    datos = {
        'id': range(1, num_registros + 1),
        'nombre': [f'Usuario_{i}' for i in range(num_registros)],
        'email': [f'user{i}@email.com' for i in range(num_registros)],
        'edad': np.random.randint(18, 80, num_registros),
        'salario': np.round(np.random.uniform(20000, 120000, num_registros), 2),
        'activo': np.random.choice([True, False], num_registros),
        'departamento': np.random.choice(['IT', 'Ventas', 'Marketing', 'RH', 'Finanzas'],
                                        num_registros),
        'fecha_ingreso': pd.date_range('2015-01-01', periods=num_registros, freq='H'),
        'puntuacion': np.round(np.random.uniform(1, 10, num_registros), 1),
        'comentarios': [f'Comentario largo número {i} con algo de texto para ocupar espacio'
                       for i in range(num_registros)]
    }

    return pd.DataFrame(datos)


def medir_escritura(df: pd.DataFrame, formato: str, ruta: str, **kwargs) -> float:
    """
    Mide tiempo de escritura de un DataFrame.

    Args:
        df: DataFrame a escribir
        formato: Tipo de formato ('csv', 'json', 'jsonl', 'parquet')
        ruta: Ruta del archivo
        **kwargs: Argumentos adicionales para el método de escritura

    Returns:
        Tiempo en segundos
    """
    inicio = time.time()

    if formato == 'csv':
        df.to_csv(ruta, index=False, **kwargs)
    elif formato == 'json':
        df.to_json(ruta, orient='records', indent=2, force_ascii=False, **kwargs)
    elif formato == 'jsonl':
        df.to_json(ruta, orient='records', lines=True, force_ascii=False, **kwargs)
    elif formato == 'parquet':
        df.to_parquet(ruta, **kwargs)
    else:
        raise ValueError(f"Formato desconocido: {formato}")

    return time.time() - inicio


def medir_lectura(formato: str, ruta: str, **kwargs) -> tuple:
    """
    Mide tiempo de lectura de un archivo.

    Args:
        formato: Tipo de formato
        ruta: Ruta del archivo
        **kwargs: Argumentos adicionales para el método de lectura

    Returns:
        Tupla (tiempo_segundos, num_registros)
    """
    inicio = time.time()

    if formato == 'csv':
        df = pd.read_csv(ruta, **kwargs)
    elif formato == 'json':
        df = pd.read_json(ruta, **kwargs)
    elif formato == 'jsonl':
        df = pd.read_json(ruta, lines=True, **kwargs)
    elif formato == 'parquet':
        df = pd.read_parquet(ruta, **kwargs)
    else:
        raise ValueError(f"Formato desconocido: {formato}")

    return time.time() - inicio, len(df)


def obtener_tamanio_mb(ruta: str) -> float:
    """Obtiene tamaño del archivo en MB."""
    return os.path.getsize(ruta) / (1024 * 1024)


def ejecutar_benchmark() -> pd.DataFrame:
    """
    Ejecuta benchmark completo de formatos.

    Returns:
        DataFrame con resultados
    """
    print("=" * 70)
    print("EJEMPLO 3: Benchmark de Formatos")
    print("=" * 70)

    # 1. Generar datos
    print("\n🔧 Generando dataset de prueba (100k registros)...")
    df = generar_dataset_benchmark(100000)
    print(f"✅ Dataset generado: {len(df):,} registros, {len(df.columns)} columnas")

    # 2. Configuración de formatos
    formatos = {
        'CSV': ('csv', 'benchmark.csv', {}),
        'CSV (gzip)': ('csv', 'benchmark.csv.gz', {'compression': 'gzip'}),
        'JSON': ('json', 'benchmark.json', {}),
        'JSON Lines': ('jsonl', 'benchmark.jsonl', {}),
        'JSON Lines (gzip)': ('jsonl', 'benchmark.jsonl.gz', {'compression': 'gzip'}),
        'Parquet (snappy)': ('parquet', 'benchmark_snappy.parquet', {'compression': 'snappy'}),
        'Parquet (gzip)': ('parquet', 'benchmark_gzip.parquet', {'compression': 'gzip'}),
        'Parquet (sin compresión)': ('parquet', 'benchmark_none.parquet', {'compression': None})
    }

    resultados = []

    # 3. Probar cada formato
    for nombre, (formato, ruta, kwargs) in formatos.items():
        print(f"\n📊 Probando: {nombre}")
        print(f"   Formato: {formato}, Archivo: {ruta}")

        # Escritura
        tiempo_escritura = medir_escritura(df, formato, ruta, **kwargs)
        print(f"   ⏱️  Escritura: {tiempo_escritura:.3f}s")

        # Tamaño
        tamanio_mb = obtener_tamanio_mb(ruta)
        print(f"   💾 Tamaño: {tamanio_mb:.2f} MB")

        # Lectura completa
        tiempo_lectura, num_registros = medir_lectura(formato, ruta)
        print(f"   ⏱️  Lectura: {tiempo_lectura:.3f}s ({num_registros:,} registros)")

        # Lectura selectiva (solo para Parquet)
        tiempo_lectura_columna = None
        if formato == 'parquet':
            tiempo_lectura_columna, _ = medir_lectura(formato, ruta, columns=['id', 'nombre'])
            print(f"   ⏱️  Lectura 2 columnas: {tiempo_lectura_columna:.3f}s")

        # Guardar resultados
        resultados.append({
            'Formato': nombre,
            'Tamaño (MB)': tamanio_mb,
            'Escritura (s)': tiempo_escritura,
            'Lectura (s)': tiempo_lectura,
            'Lectura Selectiva (s)': tiempo_lectura_columna
        })

        # Limpiar archivo
        os.remove(ruta)

    # 4. Crear DataFrame de resultados
    df_resultados = pd.DataFrame(resultados)

    # Calcular ratios relativos a CSV
    tamanio_csv = df_resultados[df_resultados['Formato'] == 'CSV']['Tamaño (MB)'].values[0]
    df_resultados['Reducción vs CSV (%)'] = (
        (tamanio_csv - df_resultados['Tamaño (MB)']) / tamanio_csv * 100
    ).round(1)

    return df_resultados


def main():
    """Ejecuta el benchmark y muestra resultados."""
    df_resultados = ejecutar_benchmark()

    # Mostrar tabla completa
    print("\n" + "=" * 70)
    print("📊 RESULTADOS DEL BENCHMARK")
    print("=" * 70)
    print()
    print(df_resultados.to_string(index=False))

    # Análisis
    print("\n" + "=" * 70)
    print("🎯 ANÁLISIS")
    print("=" * 70)

    mejor_tamanio = df_resultados.loc[df_resultados['Tamaño (MB)'].idxmin()]
    mejor_escritura = df_resultados.loc[df_resultados['Escritura (s)'].idxmin()]
    mejor_lectura = df_resultados.loc[df_resultados['Lectura (s)'].idxmin()]

    print(f"\n🏆 Mejor tamaño: {mejor_tamanio['Formato']} ({mejor_tamanio['Tamaño (MB)']:.2f} MB)")
    print(f"🏆 Escritura más rápida: {mejor_escritura['Formato']} ({mejor_escritura['Escritura (s)']:.3f}s)")
    print(f"🏆 Lectura más rápida: {mejor_lectura['Formato']} ({mejor_lectura['Lectura (s)']:.3f}s)")

    # Guardar resultados
    df_resultados.to_csv('benchmark_resultados.csv', index=False)
    print(f"\n💾 Resultados guardados en benchmark_resultados.csv")


if __name__ == '__main__':
    main()
```

### 📊 Resultados Esperados

```
Formato                  Tamaño (MB)  Escritura (s)  Lectura (s)  Lectura Selectiva (s)  Reducción vs CSV (%)
CSV                           14.50          0.850        1.200                    -                   0.0
CSV (gzip)                     4.20          2.100        1.450                    -                  71.0
JSON                          22.30          1.950        2.850                    -                 -53.8
JSON Lines                    22.30          1.850        2.450                    -                 -53.8
JSON Lines (gzip)              5.80          3.200        2.900                    -                  60.0
Parquet (snappy)               2.10          0.720        0.380                0.120                  85.5
Parquet (gzip)                 1.80          1.450        0.520                0.140                  87.6
Parquet (sin compresión)       8.50          0.650        0.350                0.110                  41.4
```

### 🎓 Aprendizajes

1. **Parquet gana en tamaño**: 87% de reducción vs CSV
2. **Parquet gana en lectura**: 3-4x más rápido
3. **Lectura selectiva**: 3x más rápida que lectura completa
4. **JSON es el peor**: Más grande y más lento
5. **Trade-off compresión**: Gzip reduce tamaño pero aumenta tiempo

---

## Ejemplo 4: Pipeline Multi-formato con Compresión

### 📖 Contexto

Pipeline real que:
1. Lee datos de múltiples fuentes (CSV, JSON)
2. Transforma y consolida
3. Guarda en Parquet particionado con compresión
4. Genera reporte de metadata

### 🎯 Objetivo

Crear un pipeline completo de conversión multi-formato con logging y validación.

### 💻 Código

```python
import pandas as pd
import json
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class PipelineMultiFormato:
    """Pipeline para consolidar datos de múltiples formatos en Parquet."""

    def __init__(self, directorio_salida: str = 'data_consolidada'):
        """
        Inicializa el pipeline.

        Args:
            directorio_salida: Directorio para guardar resultado
        """
        self.directorio_salida = Path(directorio_salida)
        self.directorio_salida.mkdir(exist_ok=True)
        self.metadata = {
            'timestamp': datetime.now().isoformat(),
            'fuentes': [],
            'transformaciones': [],
            'salida': {}
        }

    def leer_csv(self, ruta: str, **kwargs) -> pd.DataFrame:
        """
        Lee archivo CSV.

        Args:
            ruta: Ruta del archivo CSV
            **kwargs: Argumentos adicionales para read_csv

        Returns:
            DataFrame
        """
        logger.info(f"📖 Leyendo CSV: {ruta}")
        df = pd.read_csv(ruta, **kwargs)

        self.metadata['fuentes'].append({
            'tipo': 'CSV',
            'ruta': ruta,
            'registros': len(df),
            'columnas': list(df.columns)
        })

        logger.info(f"✅ CSV leído: {len(df):,} registros")
        return df

    def leer_json(self, ruta: str, **kwargs) -> pd.DataFrame:
        """
        Lee archivo JSON o JSON Lines.

        Args:
            ruta: Ruta del archivo JSON
            **kwargs: Argumentos adicionales para read_json

        Returns:
            DataFrame
        """
        logger.info(f"📖 Leyendo JSON: {ruta}")

        # Detectar si es JSON Lines
        with open(ruta, 'r', encoding='utf-8') as f:
            primera_linea = f.readline()

        es_jsonlines = not primera_linea.strip().startswith('[')

        if es_jsonlines:
            df = pd.read_json(ruta, lines=True, **kwargs)
            tipo = 'JSON Lines'
        else:
            df = pd.read_json(ruta, **kwargs)
            tipo = 'JSON'

        self.metadata['fuentes'].append({
            'tipo': tipo,
            'ruta': ruta,
            'registros': len(df),
            'columnas': list(df.columns)
        })

        logger.info(f"✅ {tipo} leído: {len(df):,} registros")
        return df

    def transformar_datos(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Transforma y consolida múltiples DataFrames.

        Args:
            dfs: Lista de DataFrames a consolidar

        Returns:
            DataFrame consolidado
        """
        logger.info(f"🔄 Consolidando {len(dfs)} fuentes...")

        # Concatenar todos los DataFrames
        df_consolidado = pd.concat(dfs, ignore_index=True)
        registros_antes = len(df_consolidado)

        logger.info(f"   Registros totales: {registros_antes:,}")

        # Eliminar duplicados
        df_consolidado = df_consolidado.drop_duplicates()
        registros_despues = len(df_consolidado)
        duplicados = registros_antes - registros_despues

        if duplicados > 0:
            logger.info(f"   🗑️  Duplicados eliminados: {duplicados:,}")
            self.metadata['transformaciones'].append({
                'tipo': 'eliminar_duplicados',
                'registros_eliminados': duplicados
            })

        # Ordenar por fecha si existe
        if 'fecha' in df_consolidado.columns:
            df_consolidado['fecha'] = pd.to_datetime(df_consolidado['fecha'])
            df_consolidado = df_consolidado.sort_values('fecha')
            logger.info("   📅 Ordenado por fecha")
            self.metadata['transformaciones'].append({
                'tipo': 'ordenar',
                'columna': 'fecha'
            })

        logger.info(f"✅ Consolidación completada: {len(df_consolidado):,} registros finales")
        return df_consolidado

    def guardar_parquet(
        self,
        df: pd.DataFrame,
        nombre: str = 'datos',
        particionar: bool = True,
        compresion: str = 'snappy'
    ) -> None:
        """
        Guarda DataFrame en Parquet particionado.

        Args:
            df: DataFrame a guardar
            nombre: Nombre base del archivo/directorio
            particionar: Si True, particiona por año/mes
            compresion: Algoritmo de compresión
        """
        logger.info(f"💾 Guardando en Parquet ({compresion})...")

        ruta_salida = self.directorio_salida / nombre

        if particionar and 'fecha' in df.columns:
            # Añadir columnas de partición
            df['año'] = df['fecha'].dt.year
            df['mes'] = df['fecha'].dt.month

            # Guardar particionado
            df.to_parquet(
                ruta_salida,
                engine='pyarrow',
                compression=compresion,
                partition_cols=['año', 'mes'],
                index=False
            )

            num_particiones = len(list(ruta_salida.rglob('*.parquet')))
            logger.info(f"   📁 Particiones creadas: {num_particiones}")

            self.metadata['salida'] = {
                'tipo': 'Parquet particionado',
                'ruta': str(ruta_salida),
                'compresion': compresion,
                'particiones': num_particiones,
                'registros': len(df)
            }
        else:
            # Guardar sin particionar
            ruta_archivo = ruta_salida.with_suffix('.parquet')
            df.to_parquet(
                ruta_archivo,
                engine='pyarrow',
                compression=compresion,
                index=False
            )

            tamanio_mb = ruta_archivo.stat().st_size / (1024 * 1024)
            logger.info(f"   💾 Tamaño: {tamanio_mb:.2f} MB")

            self.metadata['salida'] = {
                'tipo': 'Parquet',
                'ruta': str(ruta_archivo),
                'compresion': compresion,
                'tamanio_mb': tamanio_mb,
                'registros': len(df)
            }

        logger.info(f"✅ Parquet guardado exitosamente")

    def generar_reporte(self) -> Dict:
        """
        Genera reporte de metadata del pipeline.

        Returns:
            Diccionario con metadata
        """
        logger.info("📊 Generando reporte de metadata...")

        # Guardar metadata como JSON
        ruta_reporte = self.directorio_salida / 'metadata.json'
        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Reporte guardado en: {ruta_reporte}")
        return self.metadata


def main():
    """Ejecuta el pipeline completo."""
    print("=" * 70)
    print("EJEMPLO 4: Pipeline Multi-formato con Compresión")
    print("=" * 70)

    # 1. Preparar datos de prueba
    logger.info("🔧 Preparando datos de prueba...")

    # CSV de ventas
    ventas_csv = pd.DataFrame({
        'id': range(1, 501),
        'fecha': pd.date_range('2024-01-01', periods=500, freq='D'),
        'producto': ['Producto_A'] * 250 + ['Producto_B'] * 250,
        'cantidad': [1, 2, 3, 4, 5] * 100,
        'precio': [10.5, 20.3, 15.7, 30.2, 25.8] * 100
    })
    ventas_csv.to_csv('ventas.csv', index=False)
    logger.info("   ✅ ventas.csv creado")

    # JSON de clientes
    clientes_json = [
        {'id': i, 'fecha': f'2024-{i%12+1:02d}-01', 'nombre': f'Cliente_{i}',
         'email': f'cliente{i}@email.com'}
        for i in range(1, 201)
    ]
    with open('clientes.json', 'w') as f:
        json.dump(clientes_json, f)
    logger.info("   ✅ clientes.json creado")

    # JSON Lines de transacciones
    transacciones = pd.DataFrame({
        'id': range(1, 301),
        'fecha': pd.date_range('2024-06-01', periods=300, freq='D'),
        'tipo': ['Venta', 'Devolucion'] * 150,
        'monto': [100, -50] * 150
    })
    transacciones.to_json('transacciones.jsonl', orient='records', lines=True)
    logger.info("   ✅ transacciones.jsonl creado")

    # 2. Ejecutar pipeline
    pipeline = PipelineMultiFormato(directorio_salida='data_consolidada')

    # Leer fuentes
    df_ventas = pipeline.leer_csv('ventas.csv', parse_dates=['fecha'])
    df_clientes = pipeline.leer_json('clientes.json')
    df_transacciones = pipeline.leer_json('transacciones.jsonl')

    # Transformar (aquí solo consolidamos, en real habría más transformaciones)
    df_consolidado = pipeline.transformar_datos([df_ventas, df_clientes, df_transacciones])

    # Guardar
    pipeline.guardar_parquet(
        df_consolidado,
        nombre='datos_consolidados',
        particionar=True,
        compresion='snappy'
    )

    # Generar reporte
    metadata = pipeline.generar_reporte()

    # 3. Mostrar resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL PIPELINE")
    print("=" * 70)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))

    # Limpiar archivos temporales
    logger.info("\n🧹 Limpiando archivos temporales...")
    Path('ventas.csv').unlink()
    Path('clientes.json').unlink()
    Path('transacciones.jsonl').unlink()
    logger.info("✅ Pipeline completado")


if __name__ == '__main__':
    main()
```

### 📊 Resultados Esperados

```json
{
  "timestamp": "2024-10-30T12:00:00",
  "fuentes": [
    {
      "tipo": "CSV",
      "ruta": "ventas.csv",
      "registros": 500,
      "columnas": ["id", "fecha", "producto", "cantidad", "precio"]
    },
    {
      "tipo": "JSON",
      "ruta": "clientes.json",
      "registros": 200,
      "columnas": ["id", "fecha", "nombre", "email"]
    },
    {
      "tipo": "JSON Lines",
      "ruta": "transacciones.jsonl",
      "registros": 300,
      "columnas": ["id", "fecha", "tipo", "monto"]
    }
  ],
  "transformaciones": [
    {
      "tipo": "eliminar_duplicados",
      "registros_eliminados": 0
    },
    {
      "tipo": "ordenar",
      "columna": "fecha"
    }
  ],
  "salida": {
    "tipo": "Parquet particionado",
    "ruta": "data_consolidada/datos_consolidados",
    "compresion": "snappy",
    "particiones": 12,
    "registros": 1000
  }
}
```

### 🎓 Aprendizajes

1. **Pipeline organizado**: Clase reutilizable para conversiones
2. **Logging completo**: Trazabilidad de todo el proceso
3. **Metadata**: Registro de transformaciones y fuentes
4. **Validación**: Eliminación de duplicados y ordenamiento
5. **Flexibilidad**: Soporta múltiples formatos de entrada

---

## 📚 Resumen de Ejemplos

| Ejemplo | Tema Principal | Aprendizaje Clave |
|---------|----------------|-------------------|
| 1 | CSV → Parquet particionado | Compresión 83%, lectura selectiva 4x más rápida |
| 2 | JSON nested → Parquet | Normalización y schemas explícitos |
| 3 | Benchmark de formatos | Parquet gana en tamaño y velocidad |
| 4 | Pipeline multi-formato | Consolidación de fuentes heterogéneas |

---

*Última actualización: 2025-10-30*
