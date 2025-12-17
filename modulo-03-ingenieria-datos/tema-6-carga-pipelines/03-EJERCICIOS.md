# Ejercicios Prácticos: Carga de Datos y Pipelines Completos

Este documento contiene 15 ejercicios progresivos (40% fáciles, 40% intermedios, 20% avanzados) para practicar las estrategias de carga de datos. Cada ejercicio incluye contexto empresarial, datos, solución completa y explicación.

---

## Ejercicios Básicos (⭐ Nivel Fácil)

### Ejercicio 1: Full Load Simple

**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas en **LibrosOnline**, una librería digital. Cada mañana, el equipo de catálogo actualiza la lista de libros disponibles (título, autor, precio, stock). Tu tarea es implementar una función que cargue completamente el catálogo en la base de datos.

**Datos**:
```python
import pandas as pd

catalogo_libros = pd.DataFrame({
    "isbn": ["978-1234", "978-5678", "978-9012"],
    "titulo": ["Python para Todos", "Data Science 101", "SQL Avanzado"],
    "autor": ["Ana García", "Luis Pérez", "María López"],
    "precio": [29.99, 39.99, 34.99],
    "stock": [50, 30, 20]
})
```

**Pregunta**:
Implementa una función `full_load_catalogo(df: pd.DataFrame, connection_string: str) -> int` que:
1. Elimine todos los registros existentes de la tabla `libros`
2. Inserte todos los registros del DataFrame
3. Retorne el número de registros cargados

**Hint**:
Usa una transacción para garantizar que DELETE + INSERT sea atómico.

---

### Ejercicio 2: Detectar Estrategia de Carga Adecuada

**Dificultad**: ⭐ Fácil

**Contexto**:
Eres consultor en **DataPro** y te piden recomendar la estrategia de carga para diferentes casos.

**Pregunta**:
Para cada escenario, elige la estrategia más adecuada (full load, incremental, upsert) y justifica:

**Escenario A**: Tabla de tipos de cambio de monedas (200 pares de monedas), actualizada cada hora
**Escenario B**: Logs de servidor web (10M registros/día), nunca se modifican
**Escenario C**: Base de datos de empleados (5K empleados), pueden cambiar email, teléfono, dirección

**Hint**:
Considera: tamaño del dataset, frecuencia de cambios, si los datos se modifican o solo se agregan.

---

### Ejercicio 3: Implementar Checkpoint Básico

**Dificultad**: ⭐ Fácil

**Contexto**:
En **StreamData**, procesas eventos de usuarios. Necesitas implementar un sistema de checkpoint para rastrear hasta qué ID has procesado.

**Datos**:
```python
eventos = pd.DataFrame({
    "id_evento": [101, 102, 103, 104, 105],
    "usuario_id": [1, 2, 3, 4, 5],
    "accion": ["click", "view", "purchase", "click", "view"],
    "timestamp": pd.date_range("2024-01-15", periods=5, freq="h")
})
```

**Pregunta**:
Implementa dos funciones:
- `guardar_checkpoint(ultimo_id: int, archivo: str = "checkpoint.txt") -> None`
- `leer_checkpoint(archivo: str = "checkpoint.txt") -> int`

**Hint**:
Usa `Path.write_text()` y `Path.read_text()`. Si el archivo no existe, retorna 0.

---

### Ejercicio 4: Validar Datos Antes de Cargar

**Dificultad**: ⭐ Fácil

**Contexto**:
En **VentasExpress**, has detectado que a veces llegan datos inválidos (nulos, negativos). Necesitas validar antes de cargar.

**Datos**:
```python
ventas = pd.DataFrame({
    "id_venta": [1, 2, 3, 4, 5],
    "producto": ["Laptop", None, "Mouse", "Teclado", "Monitor"],  # 1 nulo
    "cantidad": [1, 2, -1, 1, 1],  # 1 negativo
    "monto": [1000.00, 25.00, 15.00, 80.00, None]  # 1 nulo
})
```

**Pregunta**:
Implementa `validar_ventas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]` que:
- Retorne dos DataFrames: `(df_valido, df_invalido)`
- Considerarinválido si: `producto` es nulo, `cantidad <= 0`, o `monto` es nulo

**Hint**:
Usa máscaras booleanas: `mask_valido = df["producto"].notna() & ...`

---

### Ejercicio 5: Contar Registros Después de Cargar

**Dificultad**: ⭐ Fácil

**Contexto**:
En **BancoDigital**, necesitas verificar que la carga fue exitosa comparando el conteo de registros.

**Pregunta**:
Implementa `verificar_carga(df_origen: pd.DataFrame, connection_string: str, tabla: str) -> bool` que:
- Cargue `df_origen` en la tabla
- Cuente registros en la tabla después de cargar
- Retorne `True` si coinciden, `False` si no

**Hint**:
Usa `pd.read_sql("SELECT COUNT(*) as total FROM tabla", engine)`.

---

### Ejercicio 6: Implementar Logging Básico

**Dificultad**: ⭐ Fácil

**Contexto**:
En **TechCorp**, todos los pipelines deben tener logging para auditoría.

**Pregunta**:
Implementa `load_with_logging(df: pd.DataFrame, connection_string: str, tabla: str) -> None` que:
- Configure logging a archivo y consola
- Registre: inicio de carga, número de registros, duración, finalización
- Maneje errores con logging de excepciones

**Hint**:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()]
)
```

---

## Ejercicios Intermedios (⭐⭐ Nivel Medio)

### Ejercicio 7: Incremental Load con Fecha

**Dificultad**: ⭐⭐ Medio

**Contexto**:
En **AppMetrics**, procesas métricas de aplicación cada hora. Solo quieres cargar métricas nuevas desde la última ejecución.

**Datos**:
```python
metricas = pd.DataFrame({
    "id_metrica": range(1, 11),
    "timestamp": pd.date_range("2024-01-15 10:00", periods=10, freq="6min"),
    "cpu_percent": [45.2, 50.1, 48.3, 52.7, 49.8, 51.2, 47.5, 53.1, 50.9, 48.7],
    "memory_mb": [2048, 2156, 2089, 2234, 2178, 2201, 2134, 2267, 2189, 2156]
})
```

**Pregunta**:
Implementa `incremental_load_metricas(df: pd.DataFrame, connection_string: str, checkpoint_file: str) -> dict` que:
- Lea el último timestamp procesado desde checkpoint
- Filtre solo métricas con timestamp mayor
- Cargue solo las métricas nuevas
- Actualice el checkpoint con el timestamp máximo
- Retorne un dict con métricas: `{"procesados": X, "nuevos": Y, "omitidos": Z}`

**Hint**:
Usa `df[df["timestamp"] > last_timestamp]` para filtrar.

---

### Ejercicio 8: Upsert Simple

**Dificultad**: ⭐⭐ Medio

**Contexto**:
En **InventarioTech**, la tabla de productos se actualiza constantemente: nuevos productos se agregan, precios cambian, stock se actualiza.

**Datos**:
```python
# Datos actuales en BD
productos_bd = pd.DataFrame({
    "sku": ["PROD001", "PROD002", "PROD003"],
    "nombre": ["Laptop", "Mouse", "Teclado"],
    "precio": [1200.00, 25.00, 80.00],
    "stock": [10, 50, 30]
})

# Datos nuevos del sistema fuente
productos_fuente = pd.DataFrame({
    "sku": ["PROD002", "PROD003", "PROD004"],  # PROD002 y PROD003 existen, PROD004 es nuevo
    "nombre": ["Mouse", "Teclado", "Monitor"],
    "precio": [22.00, 80.00, 350.00],  # PROD002 cambió precio
    "stock": [45, 25, 15]  # PROD002 y PROD003 cambiaron stock
})
```

**Pregunta**:
Implementa `upsert_productos(df: pd.DataFrame, connection_string: str) -> dict` que:
- Inserte productos nuevos (que no existen en BD)
- Actualice productos existentes
- Retorne métricas: `{"inserts": X, "updates": Y}`

**Hint**:
Usa la estrategia DELETE + INSERT: elimina SKUs que existen y luego inserta todos.

---

### Ejercicio 9: Batch Processing

**Dificultad**: ⭐⭐ Medio

**Contexto**:
En **BigData Corp**, necesitas cargar 500K registros diarios pero tu proceso solo puede manejar 50K en memoria a la vez.

**Datos**:
```python
# Simular dataset grande
import numpy as np

np.random.seed(42)
dataset_grande = pd.DataFrame({
    "id": range(1, 100001),  # 100K registros
    "valor_a": np.random.randint(1, 100, 100000),
    "valor_b": np.random.rand(100000),
    "categoria": np.random.choice(["A", "B", "C"], 100000)
})
```

**Pregunta**:
Implementa `load_in_batches(df: pd.DataFrame, connection_string: str, batch_size: int = 10000) -> dict` que:
- Divida el DataFrame en lotes de `batch_size`
- Cargue cada lote secuencialmente
- Registre progreso con logging
- Retorne métricas: `{"total_rows": X, "num_batches": Y, "duration_seconds": Z}`

**Hint**:
```python
for start in range(0, len(df), batch_size):
    end = min(start + batch_size, len(df))
    batch = df.iloc[start:end]
    # cargar batch
```

---

### Ejercicio 10: Particionamiento por Fecha

**Dificultad**: ⭐⭐ Medio

**Contexto**:
En **AnalyticsPro**, almacenas eventos en Parquet particionado por fecha para consultas eficientes.

**Datos**:
```python
eventos = pd.DataFrame({
    "id_evento": range(1, 21),
    "fecha": pd.to_datetime(["2024-01-15"] * 7 + ["2024-01-16"] * 7 + ["2024-01-17"] * 6),
    "usuario_id": np.random.randint(1000, 9999, 20),
    "accion": np.random.choice(["click", "view", "purchase"], 20)
})
```

**Pregunta**:
Implementa `save_partitioned(df: pd.DataFrame, base_path: str) -> dict` que:
- Guarde el DataFrame particionado por la columna `fecha` en formato Parquet
- Verifique que se crearon las particiones correctas
- Retorne dict con: `{"num_particiones": X, "particiones": ["fecha=2024-01-15", ...]}`

**Hint**:
```python
df.to_parquet(base_path, partition_cols=["fecha"], engine="pyarrow")
# Listar particiones: Path(base_path).glob("fecha=*")
```

---

### Ejercicio 11: Manejo de Errores con Rollback

**Dificultad**: ⭐⭐ Medio

**Contexto**:
En **FinanceCorp**, si la carga de transacciones falla a mitad de proceso, debes hacer rollback para no dejar datos parciales.

**Datos**:
```python
transacciones = pd.DataFrame({
    "id_transaccion": [1, 2, 3, 4, 5],
    "monto": [100.00, 200.00, -50.00, 150.00, 300.00],  # Uno negativo causará error
    "tipo": ["deposito", "retiro", "deposito", "retiro", "deposito"]
})
```

**Pregunta**:
Implementa `load_with_transaction(df: pd.DataFrame, connection_string: str) -> bool` que:
- Valide que `monto > 0` antes de insertar
- Use una transacción que haga rollback si hay error
- Retorne `True` si todo se cargó, `False` si hubo error y rollback

**Hint**:
```python
with engine.begin() as conn:
    # Si algo falla aquí, se hace rollback automático
    df.to_sql("tabla", conn, if_exists="append", index=False)
```

---

### Ejercicio 12: Métricas de Rendimiento

**Dificultad**: ⭐⭐ Medio

**Contexto**:
En **PerformanceMonitor**, necesitas medir y reportar el rendimiento de tus cargas.

**Pregunta**:
Implementa `load_with_metrics(df: pd.DataFrame, connection_string: str) -> dict` que:
- Mida tiempo de inicio y fin
- Calcule duración total
- Calcule throughput (filas/segundo)
- Retorne dict con: `{"rows": X, "duration_s": Y, "throughput_rows_per_sec": Z}`

**Hint**:
```python
from datetime import datetime
start = datetime.now()
# ... cargar datos ...
duration = (datetime.now() - start).total_seconds()
throughput = len(df) / duration
```

---

## Ejercicios Avanzados (⭐⭐⭐ Nivel Difícil)

### Ejercicio 13: Pipeline ETL Completo

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
En **DataMaster**, necesitas construir un pipeline ETL completo que integre: extracción desde CSV, validación, transformación, carga incremental, logging, métricas y manejo de errores.

**Datos**:
```python
# CSV con pedidos
pedidos_csv = """id_pedido,fecha,cliente_id,producto,cantidad,precio_unitario
1001,2024-01-15,5001,Laptop,1,1200.00
1002,2024-01-15,5002,Mouse,2,25.00
1003,2024-01-15,,Teclado,1,80.00
1004,2024-01-15,5004,Monitor,-1,350.00
1005,2024-01-15,5005,WebCam,1,45.00"""
```

**Pregunta**:
Implementa `pipeline_pedidos(csv_file: str, connection_string: str) -> dict` que:

**Fase 1 - Extract**:
- Lea el CSV

**Fase 2 - Validate**:
- Valide: `cliente_id` no nulo, `cantidad > 0`, `precio_unitario > 0`
- Guarde registros inválidos en `pedidos_invalidos.csv`

**Fase 3 - Transform**:
- Agregue columna `total = cantidad * precio_unitario`

**Fase 4 - Load**:
- Cargue solo registros válidos con estrategia incremental (basado en `id_pedido`)
- Use transacciones

**Fase 5 - Log & Metrics**:
- Registre cada fase con logging
- Retorne métricas completas

**Hint**:
Estructura el pipeline en funciones separadas para cada fase. Usa `try-except` global.

---

### Ejercicio 14: Optimizar Carga con Múltiples Estrategias

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
En **OptimizeData**, tienes un data warehouse con 3 tipos de tablas:
- **Dimensiones pequeñas** (<1K filas): países, categorías
- **Dimensiones grandes** (>100K filas): clientes, productos
- **Hechos** (millones de filas): transacciones

**Pregunta**:
Implementa `optimizar_carga_datawarehouse(datos: dict, connection_string: str) -> dict` que:
- Reciba un dict con: `{"dim_paises": df1, "dim_clientes": df2, "fact_ventas": df3}`
- Use **full load** para dimensiones pequeñas
- Use **upsert** para dimensiones grandes
- Use **incremental + batch processing** para hechos
- Retorne métricas por tabla

Decide automáticamente la estrategia basándote en el tamaño del DataFrame.

**Hint**:
```python
if len(df) < 1000:
    # Full load
elif "id_" in df.columns:
    # Upsert (tiene clave primaria)
else:
    # Incremental batch
```

---

### Ejercicio 15: Retry Logic con Backoff Exponencial

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
En **ReliableETL**, tus cargas a veces fallan por problemas temporales de red. Necesitas reintentar automáticamente con backoff exponencial.

**Pregunta**:
Implementa `load_with_retry(df: pd.DataFrame, connection_string: str, max_retries: int = 3) -> dict` que:
- Intente cargar los datos
- Si falla, espere y reintente con backoff exponencial: 2^n segundos (2s, 4s, 8s)
- Registre cada intento con logging
- Después de `max_retries`, lance la excepción
- Retorne métricas: `{"success": bool, "attempts": int, "total_wait_time": float}`

**Hint**:
```python
import time

wait_time = 2 ** attempt  # 2, 4, 8, 16...
logger.warning(f"Intento {attempt} falló. Esperando {wait_time}s...")
time.sleep(wait_time)
```

---

## Soluciones

### Solución Ejercicio 1

```python
from sqlalchemy import create_engine
import pandas as pd

def full_load_catalogo(df: pd.DataFrame, connection_string: str) -> int:
    """
    Carga completa del catálogo de libros.

    Args:
        df: DataFrame con libros
        connection_string: Conexión a BD

    Returns:
        Número de registros cargados
    """
    engine = create_engine(connection_string)

    with engine.begin() as conn:
        # 1. Eliminar registros existentes
        conn.execute("DELETE FROM libros")

        # 2. Insertar todos los registros
        df.to_sql("libros", conn, if_exists="append", index=False, method="multi")

    return len(df)


# Ejemplo de uso
catalogo_libros = pd.DataFrame({
    "isbn": ["978-1234", "978-5678", "978-9012"],
    "titulo": ["Python para Todos", "Data Science 101", "SQL Avanzado"],
    "autor": ["Ana García", "Luis Pérez", "María López"],
    "precio": [29.99, 39.99, 34.99],
    "stock": [50, 30, 20]
})

num_cargados = full_load_catalogo(catalogo_libros, "sqlite:///libreria.db")
print(f"Registros cargados: {num_cargados}")
```

**Explicación**:
- Usa `with engine.begin()` para transacción automática
- `DELETE FROM libros` elimina todos los registros
- `to_sql(..., if_exists="append")` inserta los nuevos
- Si algo falla, se hace rollback automático

**Resultado esperado**:
```
Registros cargados: 3
```

---

### Solución Ejercicio 2

**Escenario A**: **Full Load**
- **Justificación**: Solo 200 registros, dataset muy pequeño. Full load es simple y rápido (<1 segundo).
- Actualizar cada hora no es problema con tan pocos datos.

**Escenario B**: **Incremental Load**
- **Justificación**: 10M registros/día, datos append-only (nunca se modifican).
- Incremental es perfecto: solo procesas logs nuevos desde el último timestamp.
- Full load tardaría horas cada día.

**Escenario C**: **Upsert**
- **Justificación**: Los empleados pueden cambiar info (email, teléfono, dirección).
- Necesitas insertar nuevos empleados Y actualizar existentes.
- Incremental no detecta cambios, full load pierde historial.

---

### Solución Ejercicio 3

```python
from pathlib import Path

def guardar_checkpoint(ultimo_id: int, archivo: str = "checkpoint.txt") -> None:
    """
    Guarda el último ID procesado.

    Args:
        ultimo_id: ID del último registro procesado
        archivo: Ruta al archivo de checkpoint
    """
    Path(archivo).write_text(str(ultimo_id))


def leer_checkpoint(archivo: str = "checkpoint.txt") -> int:
    """
    Lee el último ID procesado.

    Args:
        archivo: Ruta al archivo de checkpoint

    Returns:
        Último ID procesado, o 0 si no existe el archivo
    """
    checkpoint_path = Path(archivo)

    if checkpoint_path.exists():
        return int(checkpoint_path.read_text().strip())
    else:
        return 0


# Ejemplo de uso
guardar_checkpoint(105)
ultimo_id = leer_checkpoint()
print(f"Último ID procesado: {ultimo_id}")  # 105

# Filtrar eventos nuevos
eventos_nuevos = eventos[eventos["id_evento"] > ultimo_id]
print(f"Eventos nuevos: {len(eventos_nuevos)}")
```

**Explicación**:
- `Path.write_text()` escribe el ID como string
- `Path.exists()` verifica si el archivo existe
- Si no existe, retorna 0 (procesar desde el inicio)
- Puedes filtrar: `df[df["id"] > ultimo_id]`

---

### Solución Ejercicio 4

```python
def validar_ventas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Valida ventas separando válidas de inválidas.

    Args:
        df: DataFrame con ventas

    Returns:
        Tupla (df_valido, df_invalido)
    """
    # Crear máscara de validez
    mask_valido = (
        df["producto"].notna() &
        (df["cantidad"] > 0) &
        df["monto"].notna()
    )

    df_valido = df[mask_valido].copy()
    df_invalido = df[~mask_valido].copy()

    return df_valido, df_invalido


# Ejemplo de uso
ventas = pd.DataFrame({
    "id_venta": [1, 2, 3, 4, 5],
    "producto": ["Laptop", None, "Mouse", "Teclado", "Monitor"],
    "cantidad": [1, 2, -1, 1, 1],
    "monto": [1000.00, 25.00, 15.00, 80.00, None]
})

df_valido, df_invalido = validar_ventas(ventas)

print(f"Ventas válidas: {len(df_valido)}")    # 2 (filas 1 y 4)
print(f"Ventas inválidas: {len(df_invalido)}")  # 3 (filas 2, 3, 5)

print("\nVentas inválidas:")
print(df_invalido)
```

**Explicación**:
- Máscara valida 3 condiciones simultáneamente con `&`
- `~mask_valido` invierte la máscara (filas inválidas)
- `.copy()` evita `SettingWithCopyWarning`

**Resultado**:
```
Ventas válidas: 2
Ventas inválidas: 3

Ventas inválidas:
   id_venta producto  cantidad  monto
1         2     None         2  25.00   # producto nulo
2         3    Mouse        -1  15.00   # cantidad negativa
4         5  Monitor         1    NaN   # monto nulo
```

---

### Solución Ejercicio 5

```python
def verificar_carga(
    df_origen: pd.DataFrame,
    connection_string: str,
    tabla: str
) -> bool:
    """
    Carga datos y verifica que el conteo coincida.

    Args:
        df_origen: DataFrame a cargar
        connection_string: Conexión a BD
        tabla: Nombre de la tabla

    Returns:
        True si conteos coinciden, False si no
    """
    engine = create_engine(connection_string)

    # Cargar datos
    with engine.begin() as conn:
        df_origen.to_sql(tabla, conn, if_exists="append", index=False, method="multi")

    # Contar en BD
    total_bd = pd.read_sql(f"SELECT COUNT(*) as total FROM {tabla}", engine).iloc[0]["total"]

    # Comparar
    return total_bd >= len(df_origen)


# Ejemplo de uso
datos = pd.DataFrame({"id": [1, 2, 3], "valor": [10, 20, 30]})
exito = verificar_carga(datos, "sqlite:///test.db", "datos")
print(f"Verificación: {'✅ Éxito' if exito else '❌ Fallo'}")
```

**Explicación**:
- `pd.read_sql()` ejecuta el COUNT(*)
- `.iloc[0]["total"]` extrae el valor del conteo
- Compara con `len(df_origen)`

---

### Solución Ejercicio 6

```python
import logging
from datetime import datetime

def load_with_logging(
    df: pd.DataFrame,
    connection_string: str,
    tabla: str
) -> None:
    """
    Carga datos con logging completo.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD
        tabla: Nombre de la tabla
    """
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("pipeline.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    start_time = datetime.now()
    logger.info(f"Iniciando carga de {len(df)} registros en tabla '{tabla}'")

    try:
        engine = create_engine(connection_string)

        with engine.begin() as conn:
            df.to_sql(tabla, conn, if_exists="append", index=False, method="multi")

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Carga completada exitosamente en {duration:.2f} segundos")

    except Exception as e:
        logger.error(f"Error durante la carga: {str(e)}", exc_info=True)
        raise


# Ejemplo de uso
datos = pd.DataFrame({"id": [1, 2, 3], "valor": [10, 20, 30]})
load_with_logging(datos, "sqlite:///test.db", "datos")
```

**Salida**:
```
2024-01-15 10:00:00 - INFO - Iniciando carga de 3 registros en tabla 'datos'
2024-01-15 10:00:01 - INFO - Carga completada exitosamente en 0.85 segundos
```

---

### Solución Ejercicio 7

```python
from pathlib import Path

def incremental_load_metricas(
    df: pd.DataFrame,
    connection_string: str,
    checkpoint_file: str
) -> dict:
    """
    Carga incremental de métricas con checkpoint.

    Args:
        df: DataFrame con métricas
        connection_string: Conexión a BD
        checkpoint_file: Archivo de checkpoint

    Returns:
        Dict con métricas de la carga
    """
    # Leer checkpoint
    checkpoint_path = Path(checkpoint_file)
    if checkpoint_path.exists():
        last_timestamp = pd.to_datetime(checkpoint_path.read_text().strip())
    else:
        last_timestamp = pd.Timestamp("2000-01-01")

    # Filtrar nuevos
    df_nuevos = df[df["timestamp"] > last_timestamp].copy()

    procesados = len(df)
    nuevos = len(df_nuevos)
    omitidos = procesados - nuevos

    if nuevos > 0:
        # Cargar
        engine = create_engine(connection_string)
        with engine.begin() as conn:
            df_nuevos.to_sql("metricas", conn, if_exists="append", index=False, method="multi")

        # Actualizar checkpoint
        new_checkpoint = df_nuevos["timestamp"].max()
        checkpoint_path.write_text(str(new_checkpoint))

    return {
        "procesados": procesados,
        "nuevos": nuevos,
        "omitidos": omitidos
    }


# Ejemplo de uso
metricas = pd.DataFrame({
    "id_metrica": range(1, 11),
    "timestamp": pd.date_range("2024-01-15 10:00", periods=10, freq="6min"),
    "cpu_percent": [45.2, 50.1, 48.3, 52.7, 49.8, 51.2, 47.5, 53.1, 50.9, 48.7],
    "memory_mb": [2048, 2156, 2089, 2234, 2178, 2201, 2134, 2267, 2189, 2156]
})

resultado = incremental_load_metricas(metricas, "sqlite:///metricas.db", "checkpoint_metricas.txt")
print(f"Procesados: {resultado['procesados']}")
print(f"Nuevos: {resultado['nuevos']}")
print(f"Omitidos: {resultado['omitidos']}")
```

---

### Solución Ejercicio 8

```python
def upsert_productos(df: pd.DataFrame, connection_string: str) -> dict:
    """
    Upsert de productos (insert nuevos + update existentes).

    Args:
        df: DataFrame con productos
        connection_string: Conexión a BD

    Returns:
        Métricas: {"inserts": X, "updates": Y}
    """
    engine = create_engine(connection_string)

    # Contar productos existentes
    total_antes = pd.read_sql("SELECT COUNT(*) as total FROM productos", engine).iloc[0]["total"]

    # Estrategia: DELETE + INSERT
    with engine.begin() as conn:
        # Eliminar SKUs que vamos a upsertear
        skus = df["sku"].tolist()
        placeholders = ",".join([f"'{sku}'" for sku in skus])
        conn.execute(f"DELETE FROM productos WHERE sku IN ({placeholders})")

        # Insertar todos
        df.to_sql("productos", conn, if_exists="append", index=False, method="multi")

    # Contar después
    total_despues = pd.read_sql("SELECT COUNT(*) as total FROM productos", engine).iloc[0]["total"]

    inserts = total_despues - total_antes
    updates = len(df) - inserts

    return {"inserts": inserts, "updates": updates}


# Ejemplo de uso
productos_fuente = pd.DataFrame({
    "sku": ["PROD002", "PROD003", "PROD004"],
    "nombre": ["Mouse", "Teclado", "Monitor"],
    "precio": [22.00, 80.00, 350.00],
    "stock": [45, 25, 15]
})

resultado = upsert_productos(productos_fuente, "sqlite:///inventario.db")
print(f"Inserts: {resultado['inserts']}")  # 1 (PROD004)
print(f"Updates: {resultado['updates']}")  # 2 (PROD002, PROD003)
```

---

### Solución Ejercicio 9

```python
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

def load_in_batches(
    df: pd.DataFrame,
    connection_string: str,
    batch_size: int = 10000
) -> dict:
    """
    Carga datos en lotes para controlar memoria.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD
        batch_size: Tamaño de cada lote

    Returns:
        Métricas de la carga
    """
    start_time = datetime.now()
    total_rows = len(df)
    engine = create_engine(connection_string)

    logger.info(f"Iniciando carga de {total_rows:,} filas en lotes de {batch_size:,}")

    num_batches = 0
    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        batch = df.iloc[start:end]

        with engine.begin() as conn:
            batch.to_sql("datos", conn, if_exists="append", index=False, method="multi")

        num_batches += 1
        progress = (end / total_rows) * 100
        logger.info(f"Lote {num_batches}: {len(batch):,} filas | Progreso: {progress:.1f}%")

    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Carga completada en {duration:.2f} segundos")

    return {
        "total_rows": total_rows,
        "num_batches": num_batches,
        "duration_seconds": duration
    }


# Ejemplo de uso
import numpy as np
np.random.seed(42)

dataset_grande = pd.DataFrame({
    "id": range(1, 100001),
    "valor_a": np.random.randint(1, 100, 100000),
    "valor_b": np.random.rand(100000),
    "categoria": np.random.choice(["A", "B", "C"], 100000)
})

resultado = load_in_batches(dataset_grande, "sqlite:///bigdata.db", batch_size=10000)
print(f"Total filas: {resultado['total_rows']:,}")
print(f"Num lotes: {resultado['num_batches']}")
print(f"Duración: {resultado['duration_seconds']:.2f}s")
```

---

### Solución Ejercicio 10

```python
from pathlib import Path

def save_partitioned(df: pd.DataFrame, base_path: str) -> dict:
    """
    Guarda DataFrame particionado por fecha en Parquet.

    Args:
        df: DataFrame con columna 'fecha'
        base_path: Directorio base

    Returns:
        Dict con info de particiones
    """
    # Guardar particionado
    df.to_parquet(
        base_path,
        partition_cols=["fecha"],
        engine="pyarrow",
        compression="snappy"
    )

    # Listar particiones creadas
    particiones = sorted([p.name for p in Path(base_path).glob("fecha=*")])

    return {
        "num_particiones": len(particiones),
        "particiones": particiones
    }


# Ejemplo de uso
eventos = pd.DataFrame({
    "id_evento": range(1, 21),
    "fecha": pd.to_datetime(["2024-01-15"] * 7 + ["2024-01-16"] * 7 + ["2024-01-17"] * 6),
    "usuario_id": np.random.randint(1000, 9999, 20),
    "accion": np.random.choice(["click", "view", "purchase"], 20)
})

resultado = save_partitioned(eventos, "data/eventos")
print(f"Particiones creadas: {resultado['num_particiones']}")
for part in resultado["particiones"]:
    print(f"  - {part}")

# Leer solo una partición
df_dia = pd.read_parquet("data/eventos", filters=[("fecha", "==", "2024-01-15")])
print(f"\nEventos del 2024-01-15: {len(df_dia)}")
```

---

### Solución Ejercicio 11

```python
def load_with_transaction(df: pd.DataFrame, connection_string: str) -> bool:
    """
    Carga con validación y transacción (rollback si falla).

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD

    Returns:
        True si éxito, False si error
    """
    # Validar antes de cargar
    if (df["monto"] <= 0).any():
        print("❌ Error: Hay montos negativos o cero")
        return False

    try:
        engine = create_engine(connection_string)

        with engine.begin() as conn:
            # Si esto falla, se hace rollback automático
            df.to_sql("transacciones", conn, if_exists="append", index=False, method="multi")

        print("✅ Transacciones cargadas exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error durante carga: {e}")
        return False


# Ejemplo de uso
transacciones = pd.DataFrame({
    "id_transaccion": [1, 2, 3, 4, 5],
    "monto": [100.00, 200.00, -50.00, 150.00, 300.00],
    "tipo": ["deposito", "retiro", "deposito", "retiro", "deposito"]
})

exito = load_with_transaction(transacciones, "sqlite:///finanzas.db")
print(f"Resultado: {'Éxito' if exito else 'Fallo con rollback'}")
```

---

### Solución Ejercicio 12

```python
from datetime import datetime

def load_with_metrics(df: pd.DataFrame, connection_string: str) -> dict:
    """
    Carga datos y mide rendimiento.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD

    Returns:
        Métricas de rendimiento
    """
    start_time = datetime.now()

    engine = create_engine(connection_string)

    with engine.begin() as conn:
        df.to_sql("datos", conn, if_exists="append", index=False, method="multi")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    throughput = len(df) / duration

    return {
        "rows": len(df),
        "duration_s": round(duration, 2),
        "throughput_rows_per_sec": round(throughput, 0)
    }


# Ejemplo de uso
datos = pd.DataFrame({"id": range(1, 10001), "valor": range(10000)})

metricas = load_with_metrics(datos, "sqlite:///performance.db")
print(f"Filas: {metricas['rows']:,}")
print(f"Duración: {metricas['duration_s']}s")
print(f"Throughput: {metricas['throughput_rows_per_sec']:,} filas/seg")
```

---

### Solución Ejercicio 13

```python
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def pipeline_pedidos(csv_file: str, connection_string: str) -> dict:
    """
    Pipeline ETL completo para pedidos.

    Args:
        csv_file: Ruta al CSV
        connection_string: Conexión a BD

    Returns:
        Métricas completas
    """
    start_time = datetime.now()

    try:
        # FASE 1: EXTRACT
        logger.info("=== FASE 1: EXTRACCIÓN ===")
        df = pd.read_csv(csv_file)
        logger.info(f"Extraídos {len(df)} pedidos")

        # FASE 2: VALIDATE
        logger.info("=== FASE 2: VALIDACIÓN ===")
        mask_valido = (
            df["cliente_id"].notna() &
            (df["cantidad"] > 0) &
            (df["precio_unitario"] > 0)
        )

        df_valido = df[mask_valido].copy()
        df_invalido = df[~mask_valido].copy()

        logger.info(f"Válidos: {len(df_valido)}, Inválidos: {len(df_invalido)}")

        if len(df_invalido) > 0:
            df_invalido.to_csv("pedidos_invalidos.csv", index=False)
            logger.warning(f"Pedidos inválidos guardados en pedidos_invalidos.csv")

        # FASE 3: TRANSFORM
        logger.info("=== FASE 3: TRANSFORMACIÓN ===")
        df_valido["total"] = df_valido["cantidad"] * df_valido["precio_unitario"]
        logger.info("Columna 'total' agregada")

        # FASE 4: LOAD (incremental)
        logger.info("=== FASE 4: CARGA ===")
        engine = create_engine(connection_string)

        # Checkpoint
        checkpoint_file = "checkpoint_pedidos.txt"
        if Path(checkpoint_file).exists():
            last_id = int(Path(checkpoint_file).read_text())
        else:
            last_id = 0

        df_nuevos = df_valido[df_valido["id_pedido"] > last_id]

        if len(df_nuevos) > 0:
            with engine.begin() as conn:
                df_nuevos.to_sql("pedidos", conn, if_exists="append", index=False, method="multi")

            new_checkpoint = df_nuevos["id_pedido"].max()
            Path(checkpoint_file).write_text(str(new_checkpoint))
            logger.info(f"Cargados {len(df_nuevos)} pedidos nuevos")
        else:
            logger.info("No hay pedidos nuevos")

        # FASE 5: METRICS
        duration = (datetime.now() - start_time).total_seconds()

        return {
            "success": True,
            "extraidos": len(df),
            "validos": len(df_valido),
            "invalidos": len(df_invalido),
            "cargados": len(df_nuevos),
            "duration_seconds": round(duration, 2)
        }

    except Exception as e:
        logger.error(f"Error en pipeline: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# Ejemplo de uso
resultado = pipeline_pedidos("pedidos.csv", "sqlite:///pedidos.db")
print(f"\nResultado: {'✅ Éxito' if resultado['success'] else '❌ Fallo'}")
print(f"Extraídos: {resultado['extraidos']}")
print(f"Válidos: {resultado['validos']}")
print(f"Inválidos: {resultado['invalidos']}")
print(f"Cargados: {resultado['cargados']}")
```

---

### Solución Ejercicio 14

```python
def optimizar_carga_datawarehouse(datos: dict, connection_string: str) -> dict:
    """
    Carga optimizada con estrategia automática según tamaño.

    Args:
        datos: Dict {"tabla": DataFrame}
        connection_string: Conexión a BD

    Returns:
        Métricas por tabla
    """
    engine = create_engine(connection_string)
    metricas = {}

    for tabla, df in datos.items():
        start_time = datetime.now()

        # Decidir estrategia según tamaño
        if len(df) < 1000:
            # FULL LOAD para dimensiones pequeñas
            with engine.begin() as conn:
                conn.execute(f"DELETE FROM {tabla}")
                df.to_sql(tabla, conn, if_exists="append", index=False, method="multi")
            estrategia = "full_load"

        elif "id_" in df.columns[0]:
            # UPSERT para dimensiones grandes con ID
            id_col = df.columns[0]
            ids = df[id_col].tolist()
            placeholders = ",".join([str(id) for id in ids])

            with engine.begin() as conn:
                conn.execute(f"DELETE FROM {tabla} WHERE {id_col} IN ({placeholders})")
                df.to_sql(tabla, conn, if_exists="append", index=False, method="multi")
            estrategia = "upsert"

        else:
            # INCREMENTAL BATCH para hechos
            batch_size = 10000
            for start in range(0, len(df), batch_size):
                end = min(start + batch_size, len(df))
                batch = df.iloc[start:end]

                with engine.begin() as conn:
                    batch.to_sql(tabla, conn, if_exists="append", index=False, method="multi")
            estrategia = "incremental_batch"

        duration = (datetime.now() - start_time).total_seconds()

        metricas[tabla] = {
            "estrategia": estrategia,
            "rows": len(df),
            "duration_s": round(duration, 2)
        }

    return metricas


# Ejemplo de uso
datos = {
    "dim_paises": pd.DataFrame({"id_pais": [1, 2, 3], "nombre": ["Mexico", "USA", "Canada"]}),  # 3 filas -> full
    "dim_clientes": pd.DataFrame({"id_cliente": range(1, 1001), "nombre": [f"Cliente {i}" for i in range(1, 1001)]}),  # 1000 filas -> upsert
    "fact_ventas": pd.DataFrame({"id_venta": range(1, 50001), "monto": range(50000)})  # 50K filas -> incremental batch
}

metricas = optimizar_carga_datawarehouse(datos, "sqlite:///dw.db")

for tabla, metrica in metricas.items():
    print(f"{tabla}: {metrica['estrategia']} - {metrica['rows']} filas en {metrica['duration_s']}s")
```

---

### Solución Ejercicio 15

```python
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_with_retry(
    df: pd.DataFrame,
    connection_string: str,
    max_retries: int = 3
) -> dict:
    """
    Carga con retry automático y backoff exponencial.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD
        max_retries: Número máximo de reintentos

    Returns:
        Métricas: {"success": bool, "attempts": int, "total_wait_time": float}
    """
    total_wait_time = 0

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Intento {attempt}/{max_retries}")

            engine = create_engine(connection_string)
            with engine.begin() as conn:
                df.to_sql("datos", conn, if_exists="append", index=False, method="multi")

            logger.info(f"✅ Carga exitosa en intento {attempt}")
            return {
                "success": True,
                "attempts": attempt,
                "total_wait_time": total_wait_time
            }

        except Exception as e:
            logger.warning(f"Intento {attempt} falló: {e}")

            if attempt < max_retries:
                # Backoff exponencial: 2^attempt segundos
                wait_time = 2 ** attempt
                logger.warning(f"Esperando {wait_time}s antes del siguiente intento...")
                time.sleep(wait_time)
                total_wait_time += wait_time
            else:
                logger.error(f"❌ Fallo después de {max_retries} intentos")
                raise

    return {
        "success": False,
        "attempts": max_retries,
        "total_wait_time": total_wait_time
    }


# Ejemplo de uso (simulando error temporal)
datos = pd.DataFrame({"id": [1, 2, 3], "valor": [10, 20, 30]})

try:
    resultado = load_with_retry(datos, "sqlite:///retry_test.db", max_retries=3)
    print(f"\nResultado: {'✅ Éxito' if resultado['success'] else '❌ Fallo'}")
    print(f"Intentos: {resultado['attempts']}")
    print(f"Tiempo de espera total: {resultado['total_wait_time']}s")
except Exception as e:
    print(f"Error final: {e}")
```

---

## Resumen de Ejercicios

| # | Tema | Dificultad | Concepto Clave |
|---|------|-----------|----------------|
| 1 | Full Load | ⭐ | Transacciones DELETE + INSERT |
| 2 | Estrategias | ⭐ | Elegir según caso de uso |
| 3 | Checkpoint | ⭐ | Persistir último ID procesado |
| 4 | Validación | ⭐ | Separar válidos/inválidos |
| 5 | Verificación | ⭐ | COUNT(*) post-carga |
| 6 | Logging | ⭐ | Registro a archivo + consola |
| 7 | Incremental | ⭐⭐ | Filtrar por timestamp |
| 8 | Upsert | ⭐⭐ | DELETE + INSERT por clave |
| 9 | Batch Processing | ⭐⭐ | Dividir en lotes |
| 10 | Particionamiento | ⭐⭐ | Parquet con partition_cols |
| 11 | Transacciones | ⭐⭐ | Rollback automático |
| 12 | Métricas | ⭐⭐ | Throughput y duración |
| 13 | Pipeline ETL | ⭐⭐⭐ | Integración completa |
| 14 | Optimización | ⭐⭐⭐ | Estrategia automática |
| 15 | Retry Logic | ⭐⭐⭐ | Backoff exponencial |

**Próximo paso**: En el proyecto práctico (`04-proyecto-practico/`), construirás un pipeline ETL completo con TDD, implementando todas estas técnicas en un caso real.

**¡Éxito con los ejercicios!** 🚀
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
