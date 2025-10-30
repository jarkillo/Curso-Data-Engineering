# Ejercicios Prácticos: Formatos de Datos Modernos

**Objetivo**: Practicar las técnicas de conversión, compresión y optimización de formatos de datos en ejercicios progresivos.

**Instrucciones**:
- Intenta resolver cada ejercicio sin mirar la solución
- Prueba tu código con diferentes casos
- Compara tu solución con la proporcionada
- Los ejercicios están ordenados por dificultad (⭐ fácil → ⭐⭐⭐ difícil)

---

## 📋 Índice de Ejercicios

### Básicos (⭐)
1. [Leer JSON y convertir a CSV](#ejercicio-1-leer-json-y-convertir-a-csv-)
2. [Leer CSV y guardar como Parquet](#ejercicio-2-leer-csv-y-guardar-como-parquet-)
3. [Comparar tamaños: CSV vs Parquet](#ejercicio-3-comparar-tamaños-csv-vs-parquet-)
4. [Leer JSON Lines línea por línea](#ejercicio-4-leer-json-lines-línea-por-línea-)
5. [Aplicar compresión gzip a CSV](#ejercicio-5-aplicar-compresión-gzip-a-csv-)

### Intermedios (⭐⭐)
6. [Normalizar JSON nested a tabla plana](#ejercicio-6-normalizar-json-nested-a-tabla-plana-)
7. [Particionar Parquet por columna de fecha](#ejercicio-7-particionar-parquet-por-columna-de-fecha-)
8. [Convertir múltiples CSV a Parquet único](#ejercicio-8-convertir-múltiples-csv-a-parquet-único-)
9. [Leer selectivamente columnas de Parquet](#ejercicio-9-leer-selectivamente-columnas-de-parquet-)

### Avanzados (⭐⭐⭐)
10. [Pipeline: JSON → Transformación → Parquet particionado](#ejercicio-10-pipeline-json--transformación--parquet-particionado-)
11. [Benchmark completo: CSV vs JSON vs Parquet](#ejercicio-11-benchmark-completo-csv-vs-json-vs-parquet-)
12. [Conversor universal con detección automática](#ejercicio-12-conversor-universal-con-detección-automática-)

---

## Ejercicio 1: Leer JSON y convertir a CSV ⭐

### Enunciado

Dado un archivo JSON con datos de productos, conviértelo a CSV.

### Datos de Entrada

Crea un archivo `productos.json`:

```json
[
  {"id": 1, "nombre": "Laptop", "precio": 899.99, "stock": 15},
  {"id": 2, "nombre": "Mouse", "precio": 24.99, "stock": 120},
  {"id": 3, "nombre": "Teclado", "precio": 79.99, "stock": 45}
]
```

### Tarea

Escribe una función que:
1. Lea el archivo JSON
2. Lo convierta a DataFrame
3. Lo guarde como CSV

### Solución

```python
import pandas as pd
from typing import Optional


def json_a_csv(ruta_json: str, ruta_csv: str, incluir_indice: bool = False) -> None:
    """
    Convierte archivo JSON a CSV.

    Args:
        ruta_json: Ruta del archivo JSON
        ruta_csv: Ruta del archivo CSV de salida
        incluir_indice: Si True, incluye el índice en el CSV

    Raises:
        FileNotFoundError: Si el archivo JSON no existe
        ValueError: Si el JSON está vacío o mal formado
    """
    if not pd.io.common.file_exists(ruta_json):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_json}")

    # Leer JSON
    df = pd.read_json(ruta_json)

    if df.empty:
        raise ValueError("El archivo JSON está vacío")

    # Guardar como CSV
    df.to_csv(ruta_csv, index=incluir_indice)

    print(f"✅ Convertido: {len(df)} registros de JSON a CSV")


# Ejemplo de uso
if __name__ == '__main__':
    json_a_csv('productos.json', 'productos.csv')
```

### Verificación

```python
# Verificar que la conversión fue exitosa
df_original = pd.read_json('productos.json')
df_convertido = pd.read_csv('productos.csv')

assert len(df_original) == len(df_convertido)
assert list(df_original.columns) == list(df_convertido.columns)
print("✅ Conversión verificada correctamente")
```

---

## Ejercicio 2: Leer CSV y guardar como Parquet ⭐

### Enunciado

Dado un CSV de ventas, conviértelo a Parquet con compresión snappy.

### Datos de Entrada

```python
import pandas as pd

# Crear CSV de ejemplo
ventas = pd.DataFrame({
    'fecha': ['2024-01-15', '2024-01-16', '2024-01-17'],
    'producto': ['Laptop', 'Mouse', 'Teclado'],
    'cantidad': [2, 5, 3],
    'precio': [899.99, 24.99, 79.99]
})
ventas.to_csv('ventas.csv', index=False)
```

### Tarea

Escribe una función que convierta el CSV a Parquet con compresión.

### Solución

```python
import pandas as pd
import os


def csv_a_parquet(
    ruta_csv: str,
    ruta_parquet: str,
    compresion: str = 'snappy'
) -> dict:
    """
    Convierte archivo CSV a Parquet con compresión.

    Args:
        ruta_csv: Ruta del archivo CSV
        ruta_parquet: Ruta del archivo Parquet de salida
        compresion: Algoritmo de compresión ('snappy', 'gzip', None)

    Returns:
        Diccionario con métricas de conversión

    Raises:
        FileNotFoundError: Si el archivo CSV no existe
        ValueError: Si el CSV está vacío o la compresión es inválida
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_csv}")

    algoritmos_validos = ['snappy', 'gzip', 'brotli', 'zstd', None]
    if compresion not in algoritmos_validos:
        raise ValueError(f"Compresión inválida. Debe ser una de: {algoritmos_validos}")

    # Leer CSV
    df = pd.read_csv(ruta_csv)

    if df.empty:
        raise ValueError("El archivo CSV está vacío")

    # Guardar como Parquet
    df.to_parquet(ruta_parquet, compression=compresion, index=False)

    # Calcular métricas
    tamanio_csv = os.path.getsize(ruta_csv) / 1024  # KB
    tamanio_parquet = os.path.getsize(ruta_parquet) / 1024  # KB
    reduccion = ((tamanio_csv - tamanio_parquet) / tamanio_csv * 100)

    metricas = {
        'registros': len(df),
        'tamanio_csv_kb': round(tamanio_csv, 2),
        'tamanio_parquet_kb': round(tamanio_parquet, 2),
        'reduccion_pct': round(reduccion, 1),
        'compresion': compresion
    }

    print(f"✅ Convertido: {metricas['registros']} registros")
    print(f"   CSV: {metricas['tamanio_csv_kb']} KB")
    print(f"   Parquet: {metricas['tamanio_parquet_kb']} KB")
    print(f"   Reducción: {metricas['reduccion_pct']}%")

    return metricas


# Ejemplo de uso
if __name__ == '__main__':
    metricas = csv_a_parquet('ventas.csv', 'ventas.parquet', compresion='snappy')
```

---

## Ejercicio 3: Comparar tamaños: CSV vs Parquet ⭐

### Enunciado

Genera un dataset de prueba, guárdalo en CSV y Parquet, y compara los tamaños.

### Tarea

Crea una función que:
1. Genere un DataFrame con N registros
2. Guarde en CSV y Parquet
3. Compare tamaños y muestre la reducción

### Solución

```python
import pandas as pd
import numpy as np
import os


def comparar_formatos(num_registros: int = 10000) -> pd.DataFrame:
    """
    Genera datos y compara tamaños entre CSV y Parquet.

    Args:
        num_registros: Número de registros a generar

    Returns:
        DataFrame con resultados de comparación
    """
    # 1. Generar datos
    np.random.seed(42)

    df = pd.DataFrame({
        'id': range(1, num_registros + 1),
        'nombre': [f'Usuario_{i}' for i in range(num_registros)],
        'edad': np.random.randint(18, 80, num_registros),
        'salario': np.round(np.random.uniform(20000, 100000, num_registros), 2),
        'activo': np.random.choice([True, False], num_registros)
    })

    print(f"📊 Dataset generado: {len(df):,} registros")

    # 2. Guardar en diferentes formatos
    df.to_csv('datos.csv', index=False)
    df.to_parquet('datos_snappy.parquet', compression='snappy', index=False)
    df.to_parquet('datos_gzip.parquet', compression='gzip', index=False)
    df.to_parquet('datos_sin.parquet', compression=None, index=False)

    # 3. Medir tamaños
    resultados = []

    for nombre, archivo in [
        ('CSV', 'datos.csv'),
        ('Parquet (snappy)', 'datos_snappy.parquet'),
        ('Parquet (gzip)', 'datos_gzip.parquet'),
        ('Parquet (sin compresión)', 'datos_sin.parquet')
    ]:
        tamanio_kb = os.path.getsize(archivo) / 1024
        resultados.append({
            'Formato': nombre,
            'Tamaño (KB)': round(tamanio_kb, 2)
        })

    df_resultados = pd.DataFrame(resultados)

    # Calcular reducción vs CSV
    tamanio_csv = df_resultados[df_resultados['Formato'] == 'CSV']['Tamaño (KB)'].values[0]
    df_resultados['Reducción vs CSV (%)'] = (
        (tamanio_csv - df_resultados['Tamaño (KB)']) / tamanio_csv * 100
    ).round(1)

    # Limpiar archivos
    for archivo in ['datos.csv', 'datos_snappy.parquet', 'datos_gzip.parquet', 'datos_sin.parquet']:
        os.remove(archivo)

    return df_resultados


# Ejemplo de uso
if __name__ == '__main__':
    resultados = comparar_formatos(num_registros=50000)
    print("\n📊 RESULTADOS:")
    print(resultados.to_string(index=False))
```

### Salida Esperada

```
Formato                    Tamaño (KB)  Reducción vs CSV (%)
CSV                            1250.5                   0.0
Parquet (snappy)                185.3                  85.2
Parquet (gzip)                  162.7                  87.0
Parquet (sin compresión)        450.8                  63.9
```

---

## Ejercicio 4: Leer JSON Lines línea por línea ⭐

### Enunciado

Lee un archivo JSON Lines grande procesándolo línea por línea para no cargar todo en memoria.

### Datos de Entrada

```python
import pandas as pd

# Crear JSON Lines de ejemplo
datos = pd.DataFrame({
    'id': range(1, 1001),
    'valor': range(1000, 2000)
})
datos.to_json('datos.jsonl', orient='records', lines=True)
```

### Tarea

Procesa el archivo línea por línea, filtra registros donde `valor > 1500`, y guarda el resultado.

### Solución

```python
import json
from typing import Generator, Dict


def leer_jsonl_por_chunks(ruta: str, condicion=None) -> Generator[Dict, None, None]:
    """
    Lee JSON Lines línea por línea aplicando filtro opcional.

    Args:
        ruta: Ruta del archivo JSON Lines
        condicion: Función lambda para filtrar (opcional)

    Yields:
        Diccionarios que cumplen la condición
    """
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            registro = json.loads(linea)

            if condicion is None or condicion(registro):
                yield registro


def procesar_jsonl_filtrado(ruta_entrada: str, ruta_salida: str) -> int:
    """
    Procesa JSON Lines filtrando registros y guardando resultado.

    Args:
        ruta_entrada: Ruta del archivo JSON Lines de entrada
        ruta_salida: Ruta del archivo JSON Lines de salida

    Returns:
        Número de registros procesados
    """
    contador = 0

    with open(ruta_salida, 'w', encoding='utf-8') as f_out:
        # Leer y filtrar línea por línea
        for registro in leer_jsonl_por_chunks(ruta_entrada,
                                              condicion=lambda r: r['valor'] > 1500):
            # Escribir al archivo de salida
            f_out.write(json.dumps(registro, ensure_ascii=False) + '\n')
            contador += 1

    print(f"✅ Procesados {contador} registros que cumplen condición")
    return contador


# Ejemplo de uso
if __name__ == '__main__':
    # Procesar
    num_procesados = procesar_jsonl_filtrado('datos.jsonl', 'datos_filtrados.jsonl')

    # Verificar
    import pandas as pd
    df_resultado = pd.read_json('datos_filtrados.jsonl', lines=True)
    print(f"📊 Registros en resultado: {len(df_resultado)}")
    print(f"   Todos cumplen valor > 1500: {(df_resultado['valor'] > 1500).all()}")
```

---

## Ejercicio 5: Aplicar compresión gzip a CSV ⭐

### Enunciado

Guarda un DataFrame en CSV con compresión gzip y compara el tamaño.

### Tarea

1. Crea un DataFrame de ejemplo
2. Guárdalo en CSV sin compresión
3. Guárdalo en CSV con compresión gzip
4. Compara tamaños

### Solución

```python
import pandas as pd
import numpy as np
import os


def guardar_con_compresion(df: pd.DataFrame) -> dict:
    """
    Guarda DataFrame en CSV con y sin compresión y compara.

    Args:
        df: DataFrame a guardar

    Returns:
        Diccionario con métricas de compresión
    """
    # Guardar sin compresión
    df.to_csv('datos.csv', index=False)
    tamanio_sin = os.path.getsize('datos.csv') / 1024  # KB

    # Guardar con compresión gzip
    df.to_csv('datos.csv.gz', compression='gzip', index=False)
    tamanio_con = os.path.getsize('datos.csv.gz') / 1024  # KB

    # Calcular reducción
    reduccion = ((tamanio_sin - tamanio_con) / tamanio_sin * 100)

    metricas = {
        'registros': len(df),
        'tamanio_sin_compresion_kb': round(tamanio_sin, 2),
        'tamanio_con_compresion_kb': round(tamanio_con, 2),
        'reduccion_pct': round(reduccion, 1),
        'ratio': round(tamanio_sin / tamanio_con, 2)
    }

    print("📊 COMPARACIÓN DE COMPRESIÓN")
    print(f"   Sin compresión: {metricas['tamanio_sin_compresion_kb']} KB")
    print(f"   Con gzip:       {metricas['tamanio_con_compresion_kb']} KB")
    print(f"   Reducción:      {metricas['reduccion_pct']}%")
    print(f"   Ratio:          {metricas['ratio']}x")

    # Verificar que se puede leer
    df_leido = pd.read_csv('datos.csv.gz')
    assert len(df_leido) == len(df), "Error: No se leyó correctamente"

    # Limpiar
    os.remove('datos.csv')
    os.remove('datos.csv.gz')

    return metricas


# Ejemplo de uso
if __name__ == '__main__':
    # Generar datos de ejemplo
    np.random.seed(42)
    df = pd.DataFrame({
        'texto': [f'Este es un texto largo número {i} con contenido repetitivo'
                  for i in range(10000)],
        'numero': np.random.randint(0, 100, 10000)
    })

    metricas = guardar_con_compresion(df)
```

---

## Ejercicio 6: Normalizar JSON nested a tabla plana ⭐⭐

### Enunciado

Dado un JSON con estructura anidada, normalizalo a una tabla plana.

### Datos de Entrada

```json
[
  {
    "pedido_id": 1,
    "cliente": {"nombre": "Juan", "email": "juan@email.com"},
    "items": [
      {"producto": "Laptop", "cantidad": 1},
      {"producto": "Mouse", "cantidad": 2}
    ]
  },
  {
    "pedido_id": 2,
    "cliente": {"nombre": "María", "email": "maria@email.com"},
    "items": [
      {"producto": "Teclado", "cantidad": 1}
    ]
  }
]
```

### Tarea

Normaliza la estructura en dos tablas: `pedidos` y `items`.

### Solución

```python
import pandas as pd
import json
from typing import Tuple


def normalizar_pedidos_nested(ruta_json: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Normaliza JSON nested de pedidos en dos DataFrames.

    Args:
        ruta_json: Ruta del archivo JSON con estructura nested

    Returns:
        Tupla (df_pedidos, df_items)
    """
    # Leer JSON
    with open(ruta_json, 'r', encoding='utf-8') as f:
        pedidos = json.load(f)

    # 1. Normalizar nivel de pedidos (cliente nested)
    pedidos_flat = []
    for p in pedidos:
        pedido_flat = {
            'pedido_id': p['pedido_id'],
            'cliente_nombre': p['cliente']['nombre'],
            'cliente_email': p['cliente']['email']
        }
        pedidos_flat.append(pedido_flat)

    df_pedidos = pd.DataFrame(pedidos_flat)

    # 2. Normalizar nivel de items (array nested)
    items_flat = []
    for p in pedidos:
        for item in p['items']:
            item_flat = {
                'pedido_id': p['pedido_id'],
                'producto': item['producto'],
                'cantidad': item['cantidad']
            }
            items_flat.append(item_flat)

    df_items = pd.DataFrame(items_flat)

    print(f"✅ Normalización completada:")
    print(f"   Pedidos: {len(df_pedidos)} registros")
    print(f"   Items: {len(df_items)} registros")

    return df_pedidos, df_items


# Ejemplo de uso
if __name__ == '__main__':
    # Crear JSON de ejemplo
    pedidos = [
        {
            "pedido_id": 1,
            "cliente": {"nombre": "Juan", "email": "juan@email.com"},
            "items": [
                {"producto": "Laptop", "cantidad": 1},
                {"producto": "Mouse", "cantidad": 2}
            ]
        },
        {
            "pedido_id": 2,
            "cliente": {"nombre": "María", "email": "maria@email.com"},
            "items": [
                {"producto": "Teclado", "cantidad": 1}
            ]
        }
    ]

    with open('pedidos_nested.json', 'w', encoding='utf-8') as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=2)

    # Normalizar
    df_pedidos, df_items = normalizar_pedidos_nested('pedidos_nested.json')

    print("\n📊 PEDIDOS:")
    print(df_pedidos)

    print("\n📊 ITEMS:")
    print(df_items)
```

---

## Ejercicio 7: Particionar Parquet por columna de fecha ⭐⭐

### Enunciado

Guarda un DataFrame en Parquet particionado por año y mes.

### Datos de Entrada

```python
import pandas as pd

ventas = pd.DataFrame({
    'id': range(1, 1001),
    'fecha': pd.date_range('2022-01-01', periods=1000, freq='D'),
    'producto': ['A', 'B', 'C'] * 333 + ['A'],
    'monto': range(1000, 2000)
})
```

### Tarea

Guarda el DataFrame particionado por año y mes, luego lee solo los datos de un mes específico.

### Solución

```python
import pandas as pd
from pathlib import Path


def guardar_parquet_particionado(
    df: pd.DataFrame,
    ruta_base: str,
    columnas_particion: list
) -> dict:
    """
    Guarda DataFrame en Parquet particionado.

    Args:
        df: DataFrame a guardar
        ruta_base: Directorio base para particiones
        columnas_particion: Columnas para particionar

    Returns:
        Diccionario con metadata de particiones
    """
    # Validar que columnas existen
    for col in columnas_particion:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en DataFrame")

    # Guardar particionado
    df.to_parquet(
        ruta_base,
        engine='pyarrow',
        compression='snappy',
        partition_cols=columnas_particion,
        index=False
    )

    # Contar particiones
    num_particiones = len(list(Path(ruta_base).rglob('*.parquet')))

    metadata = {
        'registros_totales': len(df),
        'particiones': num_particiones,
        'columnas_particion': columnas_particion
    }

    print(f"✅ Parquet particionado guardado:")
    print(f"   Registros: {metadata['registros_totales']:,}")
    print(f"   Particiones: {metadata['particiones']}")
    print(f"   Columnas partición: {metadata['columnas_particion']}")

    return metadata


def leer_particion_especifica(ruta_base: str, filtros: list) -> pd.DataFrame:
    """
    Lee solo particiones específicas usando filtros.

    Args:
        ruta_base: Directorio base de particiones
        filtros: Lista de tuplas (columna, operador, valor)

    Returns:
        DataFrame con datos filtrados
    """
    df = pd.read_parquet(ruta_base, filters=filtros)

    print(f"✅ Leídos {len(df):,} registros de particiones filtradas")
    return df


# Ejemplo de uso
if __name__ == '__main__':
    # 1. Generar datos
    ventas = pd.DataFrame({
        'id': range(1, 1001),
        'fecha': pd.date_range('2022-01-01', periods=1000, freq='D'),
        'producto': ['A', 'B', 'C'] * 333 + ['A'],
        'monto': range(1000, 2000)
    })

    # Añadir columnas de partición
    ventas['año'] = ventas['fecha'].dt.year
    ventas['mes'] = ventas['fecha'].dt.month

    # 2. Guardar particionado
    metadata = guardar_parquet_particionado(
        ventas,
        'ventas_particionado',
        ['año', 'mes']
    )

    # 3. Leer partición específica (enero 2023)
    df_enero_2023 = leer_particion_especifica(
        'ventas_particionado',
        filtros=[('año', '==', 2023), ('mes', '==', 1)]
    )

    print(f"\n📊 Datos de enero 2023: {len(df_enero_2023)} registros")
    print(df_enero_2023.head())
```

---

## Ejercicio 8: Convertir múltiples CSV a Parquet único ⭐⭐

### Enunciado

Tienes múltiples archivos CSV en un directorio. Consolídalos en un único archivo Parquet.

### Datos de Entrada

```python
import pandas as pd

# Crear múltiples CSV
for i in range(1, 4):
    df = pd.DataFrame({
        'id': range(i*100, (i+1)*100),
        'valor': range(i*1000, (i+1)*1000)
    })
    df.to_csv(f'datos_parte_{i}.csv', index=False)
```

### Tarea

Lee todos los CSV y consolídalos en un único Parquet.

### Solución

```python
import pandas as pd
from pathlib import Path
from typing import List


def consolidar_csvs_a_parquet(
    patron_archivos: str,
    ruta_parquet: str,
    eliminar_duplicados: bool = True
) -> dict:
    """
    Consolida múltiples CSVs en un único Parquet.

    Args:
        patron_archivos: Patrón glob para encontrar archivos (ej: 'datos_*.csv')
        ruta_parquet: Ruta del archivo Parquet de salida
        eliminar_duplicados: Si True, elimina duplicados

    Returns:
        Diccionario con métricas de consolidación
    """
    # Encontrar archivos CSV
    archivos = sorted(Path('.').glob(patron_archivos))

    if not archivos:
        raise FileNotFoundError(f"No se encontraron archivos con patrón: {patron_archivos}")

    print(f"📂 Encontrados {len(archivos)} archivos CSV")

    # Leer y concatenar
    dfs = []
    total_registros_originales = 0

    for archivo in archivos:
        df = pd.read_csv(archivo)
        dfs.append(df)
        total_registros_originales += len(df)
        print(f"   ✅ {archivo.name}: {len(df)} registros")

    # Concatenar
    df_consolidado = pd.concat(dfs, ignore_index=True)

    # Eliminar duplicados si se solicita
    if eliminar_duplicados:
        antes = len(df_consolidado)
        df_consolidado = df_consolidado.drop_duplicates()
        duplicados = antes - len(df_consolidado)
        if duplicados > 0:
            print(f"   🗑️  Eliminados {duplicados} duplicados")

    # Guardar como Parquet
    df_consolidado.to_parquet(ruta_parquet, compression='snappy', index=False)

    import os
    tamanio_parquet = os.path.getsize(ruta_parquet) / 1024  # KB

    metadata = {
        'archivos_procesados': len(archivos),
        'registros_originales': total_registros_originales,
        'registros_finales': len(df_consolidado),
        'duplicados_eliminados': total_registros_originales - len(df_consolidado),
        'tamanio_parquet_kb': round(tamanio_parquet, 2)
    }

    print(f"\n✅ Consolidación completada:")
    print(f"   Archivos: {metadata['archivos_procesados']}")
    print(f"   Registros finales: {metadata['registros_finales']:,}")
    print(f"   Tamaño Parquet: {metadata['tamanio_parquet_kb']} KB")

    return metadata


# Ejemplo de uso
if __name__ == '__main__':
    # 1. Crear archivos de ejemplo
    for i in range(1, 4):
        df = pd.DataFrame({
            'id': range(i*100, (i+1)*100),
            'valor': range(i*1000, (i+1)*1000)
        })
        df.to_csv(f'datos_parte_{i}.csv', index=False)

    # 2. Consolidar
    metadata = consolidar_csvs_a_parquet(
        patron_archivos='datos_parte_*.csv',
        ruta_parquet='datos_consolidados.parquet'
    )

    # 3. Verificar
    df_verificacion = pd.read_parquet('datos_consolidados.parquet')
    print(f"\n🔍 Verificación: {len(df_verificacion)} registros en Parquet")
```

---

## Ejercicio 9: Leer selectivamente columnas de Parquet ⭐⭐

### Enunciado

Dado un Parquet con muchas columnas, practica la lectura selectiva para optimizar rendimiento.

### Datos de Entrada

```python
import pandas as pd
import numpy as np

# Crear Parquet con 20 columnas
df = pd.DataFrame({
    f'columna_{i}': np.random.randint(0, 1000, 10000)
    for i in range(20)
})
df.to_parquet('datos_anchos.parquet', index=False)
```

### Tarea

Mide la diferencia de tiempo entre leer todo vs leer solo 2 columnas.

### Solución

```python
import pandas as pd
import numpy as np
import time


def comparar_lectura_selectiva(ruta_parquet: str, columnas_seleccionadas: list) -> dict:
    """
    Compara tiempos de lectura completa vs selectiva.

    Args:
        ruta_parquet: Ruta del archivo Parquet
        columnas_seleccionadas: Lista de columnas a leer selectivamente

    Returns:
        Diccionario con métricas de comparación
    """
    # 1. Lectura completa
    inicio = time.time()
    df_completo = pd.read_parquet(ruta_parquet)
    tiempo_completo = time.time() - inicio

    memoria_completo = df_completo.memory_usage(deep=True).sum() / (1024 * 1024)  # MB

    print(f"📖 Lectura completa:")
    print(f"   Columnas: {len(df_completo.columns)}")
    print(f"   Tiempo: {tiempo_completo:.4f}s")
    print(f"   Memoria: {memoria_completo:.2f} MB")

    # 2. Lectura selectiva
    inicio = time.time()
    df_selectivo = pd.read_parquet(ruta_parquet, columns=columnas_seleccionadas)
    tiempo_selectivo = time.time() - inicio

    memoria_selectivo = df_selectivo.memory_usage(deep=True).sum() / (1024 * 1024)  # MB

    print(f"\n📖 Lectura selectiva ({len(columnas_seleccionadas)} columnas):")
    print(f"   Columnas: {len(df_selectivo.columns)}")
    print(f"   Tiempo: {tiempo_selectivo:.4f}s")
    print(f"   Memoria: {memoria_selectivo:.2f} MB")

    # 3. Calcular mejoras
    mejora_tiempo = ((tiempo_completo - tiempo_selectivo) / tiempo_completo * 100)
    mejora_memoria = ((memoria_completo - memoria_selectivo) / memoria_completo * 100)

    print(f"\n📊 Mejoras:")
    print(f"   Tiempo: {mejora_tiempo:.1f}% más rápido")
    print(f"   Memoria: {mejora_memoria:.1f}% menos uso")

    return {
        'tiempo_completo_s': tiempo_completo,
        'tiempo_selectivo_s': tiempo_selectivo,
        'mejora_tiempo_pct': mejora_tiempo,
        'memoria_completo_mb': memoria_completo,
        'memoria_selectivo_mb': memoria_selectivo,
        'mejora_memoria_pct': mejora_memoria
    }


# Ejemplo de uso
if __name__ == '__main__':
    # 1. Crear datos anchos
    np.random.seed(42)
    df = pd.DataFrame({
        f'columna_{i}': np.random.randint(0, 1000, 100000)
        for i in range(20)
    })
    df.to_parquet('datos_anchos.parquet', compression='snappy', index=False)
    print(f"✅ Creado Parquet con {len(df):,} filas y {len(df.columns)} columnas\n")

    # 2. Comparar lecturas
    metricas = comparar_lectura_selectiva(
        'datos_anchos.parquet',
        columnas_seleccionadas=['columna_0', 'columna_5']
    )
```

---

## Ejercicio 10: Pipeline: JSON → Transformación → Parquet particionado ⭐⭐⭐

### Enunciado

Crea un pipeline completo que:
1. Lee datos de JSON
2. Aplica transformaciones (limpieza, agregaciones)
3. Guarda en Parquet particionado
4. Genera reporte de metadata

### Solución

```python
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class PipelineETL:
    """Pipeline ETL para conversión JSON → Parquet."""

    def __init__(self, directorio_salida: str = 'pipeline_output'):
        self.directorio_salida = Path(directorio_salida)
        self.directorio_salida.mkdir(exist_ok=True)
        self.metadata = {
            'timestamp': datetime.now().isoformat(),
            'pasos': []
        }

    def extraer(self, ruta_json: str) -> pd.DataFrame:
        """Extrae datos de JSON."""
        print("📖 PASO 1: Extracción")
        df = pd.read_json(ruta_json)

        self.metadata['pasos'].append({
            'paso': 'extraccion',
            'registros': len(df),
            'columnas': list(df.columns)
        })

        print(f"   ✅ Extraídos {len(df):,} registros")
        return df

    def transformar(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica transformaciones."""
        print("\n🔄 PASO 2: Transformación")

        df_transformado = df.copy()
        registros_inicial = len(df_transformado)

        # 1. Eliminar nulos
        df_transformado = df_transformado.dropna()
        nulos_eliminados = registros_inicial - len(df_transformado)
        print(f"   🗑️  Nulos eliminados: {nulos_eliminados}")

        # 2. Eliminar duplicados
        df_transformado = df_transformado.drop_duplicates()
        duplicados_eliminados = registros_inicial - nulos_eliminados - len(df_transformado)
        print(f"   🗑️  Duplicados eliminados: {duplicados_eliminados}")

        # 3. Convertir fecha
        if 'fecha' in df_transformado.columns:
            df_transformado['fecha'] = pd.to_datetime(df_transformado['fecha'])
            df_transformado['año'] = df_transformado['fecha'].dt.year
            df_transformado['mes'] = df_transformado['fecha'].dt.month
            print(f"   📅 Columnas de partición añadidas: año, mes")

        self.metadata['pasos'].append({
            'paso': 'transformacion',
            'registros_entrada': registros_inicial,
            'registros_salida': len(df_transformado),
            'nulos_eliminados': nulos_eliminados,
            'duplicados_eliminados': duplicados_eliminados
        })

        print(f"   ✅ Transformación completada: {len(df_transformado):,} registros")
        return df_transformado

    def cargar(self, df: pd.DataFrame, nombre: str = 'datos') -> None:
        """Carga datos en Parquet particionado."""
        print("\n💾 PASO 3: Carga")

        ruta_salida = self.directorio_salida / nombre

        # Guardar particionado si hay columnas de fecha
        if 'año' in df.columns and 'mes' in df.columns:
            df.to_parquet(
                ruta_salida,
                engine='pyarrow',
                compression='snappy',
                partition_cols=['año', 'mes'],
                index=False
            )

            num_particiones = len(list(ruta_salida.rglob('*.parquet')))
            print(f"   📁 Particiones: {num_particiones}")

            self.metadata['pasos'].append({
                'paso': 'carga',
                'tipo': 'parquet_particionado',
                'particiones': num_particiones,
                'registros': len(df)
            })
        else:
            ruta_archivo = ruta_salida.with_suffix('.parquet')
            df.to_parquet(ruta_archivo, compression='snappy', index=False)

            self.metadata['pasos'].append({
                'paso': 'carga',
                'tipo': 'parquet',
                'registros': len(df)
            })

        print(f"   ✅ Carga completada")

    def generar_reporte(self) -> Dict:
        """Genera reporte de metadata."""
        ruta_reporte = self.directorio_salida / 'metadata.json'

        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        print(f"\n📊 Reporte guardado en: {ruta_reporte}")
        return self.metadata


# Ejemplo de uso
if __name__ == '__main__':
    # 1. Crear datos de ejemplo
    datos = [
        {'id': i, 'fecha': f'2024-{(i%12)+1:02d}-01', 'valor': i*10}
        for i in range(1, 501)
    ]
    # Añadir algunos duplicados y nulos
    datos.extend([datos[0], datos[1]])  # Duplicados
    datos.append({'id': 999, 'fecha': None, 'valor': None})  # Nulos

    with open('datos_raw.json', 'w') as f:
        json.dump(datos, f)

    print("=" * 70)
    print("PIPELINE ETL: JSON → Transformación → Parquet")
    print("=" * 70)

    # 2. Ejecutar pipeline
    pipeline = PipelineETL()

    df = pipeline.extraer('datos_raw.json')
    df_transformado = pipeline.transformar(df)
    pipeline.cargar(df_transformado, nombre='datos_finales')
    metadata = pipeline.generar_reporte()

    # 3. Mostrar metadata
    print("\n" + "=" * 70)
    print("📊 METADATA DEL PIPELINE")
    print("=" * 70)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
```

---

## Ejercicio 11: Benchmark completo: CSV vs JSON vs Parquet ⭐⭐⭐

### Enunciado

Crea un benchmark exhaustivo comparando CSV, JSON, JSON Lines y Parquet (con diferentes compresiones).

### Tarea

Mide:
- Tiempo de escritura
- Tiempo de lectura
- Tamaño en disco
- Memoria en RAM

*(Ver código completo en Ejemplo 3 de 02-EJEMPLOS.md)*

---

## Ejercicio 12: Conversor universal con detección automática ⭐⭐⭐

### Enunciado

Crea una función que detecte automáticamente el formato de un archivo y lo convierta a cualquier otro formato.

### Tarea

Implementa `convertir_archivo(origen, destino)` que:
1. Detecte el formato de origen (por extensión y contenido)
2. Lea el archivo correctamente
3. Lo guarde en el formato de destino

### Solución

```python
import pandas as pd
from pathlib import Path
import json


class ConversorUniversal:
    """Conversor universal entre formatos de datos."""

    FORMATOS_SOPORTADOS = {
        '.csv': 'csv',
        '.json': 'json',
        '.jsonl': 'jsonl',
        '.parquet': 'parquet'
    }

    @staticmethod
    def detectar_formato(ruta: str) -> str:
        """
        Detecta formato de archivo por extensión.

        Args:
            ruta: Ruta del archivo

        Returns:
            Formato detectado
        """
        extension = Path(ruta).suffix.lower()

        # Manejar gz
        if extension == '.gz':
            extension = Path(ruta).stem
            extension = Path(extension).suffix.lower()

        formato = ConversorUniversal.FORMATOS_SOPORTADOS.get(extension)

        if not formato:
            raise ValueError(f"Formato no soportado: {extension}")

        # Detectar JSON vs JSON Lines por contenido
        if formato == 'json':
            with open(ruta, 'r', encoding='utf-8') as f:
                primera_linea = f.readline().strip()
                if not primera_linea.startswith('[') and not primera_linea.startswith('{'):
                    formato = 'jsonl'

        return formato

    @staticmethod
    def leer_archivo(ruta: str, formato: str = None) -> pd.DataFrame:
        """
        Lee archivo en cualquier formato soportado.

        Args:
            ruta: Ruta del archivo
            formato: Formato explícito (opcional, se detecta automáticamente)

        Returns:
            DataFrame
        """
        if formato is None:
            formato = ConversorUniversal.detectar_formato(ruta)

        print(f"📖 Leyendo {formato.upper()}: {ruta}")

        if formato == 'csv':
            df = pd.read_csv(ruta)
        elif formato == 'json':
            df = pd.read_json(ruta)
        elif formato == 'jsonl':
            df = pd.read_json(ruta, lines=True)
        elif formato == 'parquet':
            df = pd.read_parquet(ruta)
        else:
            raise ValueError(f"Formato no soportado: {formato}")

        print(f"   ✅ Leídos {len(df):,} registros")
        return df

    @staticmethod
    def guardar_archivo(df: pd.DataFrame, ruta: str, formato: str = None) -> None:
        """
        Guarda DataFrame en cualquier formato soportado.

        Args:
            df: DataFrame a guardar
            ruta: Ruta del archivo de salida
            formato: Formato explícito (opcional, se detecta por extensión)
        """
        if formato is None:
            formato = ConversorUniversal.detectar_formato(ruta)

        print(f"💾 Guardando como {formato.upper()}: {ruta}")

        if formato == 'csv':
            df.to_csv(ruta, index=False)
        elif formato == 'json':
            df.to_json(ruta, orient='records', indent=2, force_ascii=False)
        elif formato == 'jsonl':
            df.to_json(ruta, orient='records', lines=True, force_ascii=False)
        elif formato == 'parquet':
            df.to_parquet(ruta, compression='snappy', index=False)
        else:
            raise ValueError(f"Formato no soportado: {formato}")

        print(f"   ✅ Guardado exitosamente")

    @staticmethod
    def convertir(ruta_origen: str, ruta_destino: str) -> dict:
        """
        Convierte archivo de un formato a otro automáticamente.

        Args:
            ruta_origen: Ruta del archivo de origen
            ruta_destino: Ruta del archivo de destino

        Returns:
            Diccionario con metadata de conversión
        """
        import os
        import time

        formato_origen = ConversorUniversal.detectar_formato(ruta_origen)
        formato_destino = ConversorUniversal.detectar_formato(ruta_destino)

        print(f"\n🔄 Conversión: {formato_origen.upper()} → {formato_destino.upper()}")

        # Leer
        inicio = time.time()
        df = ConversorUniversal.leer_archivo(ruta_origen, formato_origen)
        tiempo_lectura = time.time() - inicio

        # Guardar
        inicio = time.time()
        ConversorUniversal.guardar_archivo(df, ruta_destino, formato_destino)
        tiempo_escritura = time.time() - inicio

        # Metadata
        tamanio_origen = os.path.getsize(ruta_origen) / 1024  # KB
        tamanio_destino = os.path.getsize(ruta_destino) / 1024  # KB

        metadata = {
            'formato_origen': formato_origen,
            'formato_destino': formato_destino,
            'registros': len(df),
            'tiempo_lectura_s': round(tiempo_lectura, 4),
            'tiempo_escritura_s': round(tiempo_escritura, 4),
            'tamanio_origen_kb': round(tamanio_origen, 2),
            'tamanio_destino_kb': round(tamanio_destino, 2),
            'cambio_tamanio_pct': round((tamanio_destino - tamanio_origen) / tamanio_origen * 100, 1)
        }

        print(f"\n📊 RESULTADO:")
        print(f"   Registros: {metadata['registros']:,}")
        print(f"   Tiempo total: {(tiempo_lectura + tiempo_escritura):.4f}s")
        print(f"   Tamaño origen: {metadata['tamanio_origen_kb']} KB")
        print(f"   Tamaño destino: {metadata['tamanio_destino_kb']} KB")
        print(f"   Cambio tamaño: {metadata['cambio_tamanio_pct']:+.1f}%")

        return metadata


# Ejemplo de uso
if __name__ == '__main__':
    import numpy as np

    print("=" * 70)
    print("CONVERSOR UNIVERSAL DE FORMATOS")
    print("=" * 70)

    # 1. Crear datos de ejemplo en CSV
    df_ejemplo = pd.DataFrame({
        'id': range(1, 1001),
        'nombre': [f'Item_{i}' for i in range(1000)],
        'valor': np.random.randint(0, 1000, 1000)
    })
    df_ejemplo.to_csv('datos.csv', index=False)

    # 2. Conversiones
    conversiones = [
        ('datos.csv', 'datos.json'),
        ('datos.json', 'datos.jsonl'),
        ('datos.jsonl', 'datos.parquet'),
        ('datos.parquet', 'datos_final.csv')
    ]

    resultados = []

    for origen, destino in conversiones:
        metadata = ConversorUniversal.convertir(origen, destino)
        resultados.append(metadata)
        print()

    # 3. Resumen
    print("=" * 70)
    print("📊 RESUMEN DE CONVERSIONES")
    print("=" * 70)
    df_resumen = pd.DataFrame(resultados)
    print(df_resumen[['formato_origen', 'formato_destino', 'tamanio_origen_kb',
                       'tamanio_destino_kb', 'cambio_tamanio_pct']].to_string(index=False))
```

---

## 📚 Resumen

Has completado 12 ejercicios progresivos sobre formatos de datos modernos:

### Básicos ⭐
- Conversiones simples entre formatos
- Compresión básica
- Lectura streaming de JSON Lines

### Intermedios ⭐⭐
- Normalización de JSON nested
- Particionamiento de Parquet
- Consolidación de múltiples fuentes
- Lectura selectiva optimizada

### Avanzados ⭐⭐⭐
- Pipeline ETL completo
- Benchmarks exhaustivos
- Conversor universal con autodetección

### Próximos Pasos

- Practica con datasets reales de tu trabajo
- Implementa estos patrones en proyectos productivos
- Experimenta con diferentes algoritmos de compresión
- Optimiza particionamiento según tus consultas

---

*Última actualización: 2025-10-30*
