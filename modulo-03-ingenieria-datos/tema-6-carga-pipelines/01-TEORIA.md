# Tema 6: Carga de Datos y Pipelines Completos

## Introducción

Imagina que eres el gerente de un almacén que recibe camiones con productos todos los días. Tienes tres opciones:

1. **Vaciar todo el almacén** cada día y reorganizar desde cero (tedioso, pero simple)
2. **Solo agregar los productos nuevos** del día (rápido, pero necesitas llevar registro)
3. **Actualizar lo que cambió** y agregar lo nuevo (eficiente, pero requiere comparación)

Estas tres opciones son exactamente lo que enfrentamos en **Data Engineering** cuando cargamos datos en un destino (base de datos, data warehouse, lago de datos). Esta es la **fase de carga** del proceso ETL/ELT, y puede ser la diferencia entre un pipeline que procesa datos en minutos vs. uno que tarda horas.

### ¿Por qué es importante la fase de carga?

La carga de datos es el paso final del pipeline ETL/ELT, pero es uno de los **más críticos**:

- **Afecta el rendimiento**: Una mala estrategia de carga puede hacer que tu pipeline tarde 10x más
- **Impacta la disponibilidad**: Si la carga falla a medianoche, los reportes de la mañana estarán vacíos
- **Determina los costos**: Cargar datos innecesarios consume CPU, memoria, almacenamiento y dinero
- **Define la frescura de los datos**: ¿Datos actualizados cada hora? ¿Cada día? ¿En tiempo real?

En este tema aprenderás:
- Las tres estrategias fundamentales de carga de datos
- Cómo optimizar la carga con bulk inserts y batch processing
- Técnicas de particionamiento para mejorar el rendimiento
- Cómo implementar logging y monitoreo profesional
- Patrones de diseño para pipelines robustos e idempotentes

---

## 1. Estrategias de Carga de Datos

### 1.1 Full Load (Carga Completa)

**¿Qué es?**

Una carga completa significa **reemplazar todos los datos del destino** con los datos de la fuente cada vez que ejecutas el pipeline.

**Analogía**: Cada día, vacías completamente tu armario y vuelves a colocar toda tu ropa desde las cajas.

**¿Cómo funciona?**

```python
# Pseudocódigo
def full_load(df_origen, tabla_destino):
    # 1. Eliminar todos los datos existentes
    tabla_destino.truncate()

    # 2. Insertar todos los datos de origen
    tabla_destino.insert(df_origen)
```

**Ventajas**:
- ✅ **Simplicidad**: La lógica es trivial de implementar
- ✅ **Sin estado**: No necesitas rastrear qué cambió
- ✅ **Recuperación fácil**: Si algo falla, simplemente recargas
- ✅ **Consistencia garantizada**: El destino siempre refleja la fuente exactamente

**Desventajas**:
- ❌ **Lento**: Procesas todos los datos cada vez, incluso los que no cambiaron
- ❌ **Costoso**: Consume mucho CPU, memoria y almacenamiento
- ❌ **Bloqueos**: Durante la carga, la tabla puede estar inaccesible
- ❌ **No escalable**: Con millones de filas, puede tardar horas

**¿Cuándo usar Full Load?**

1. **Datasets pequeños** (<100k filas): El overhead es mínimo
2. **Datos que cambian completamente**: Si >80% de los datos cambian cada día
3. **Datos sin clave única**: No tienes forma de identificar qué cambió
4. **Sistemas simples**: Cuando el tiempo de carga no es crítico
5. **Dimensiones pequeñas**: En data warehouses, las tablas de dimensión pequeñas

**Ejemplo real**:

```python
import pandas as pd
from sqlalchemy import create_engine

def full_load_ventas_diarias(df_ventas: pd.DataFrame, connection_string: str) -> None:
    """
    Carga completa de ventas diarias.

    Args:
        df_ventas: DataFrame con ventas del día
        connection_string: Conexión a la base de datos
    """
    engine = create_engine(connection_string)

    # TRUNCATE + INSERT en una transacción
    with engine.begin() as conn:
        # 1. Eliminar datos existentes
        conn.execute("TRUNCATE TABLE ventas_diarias")

        # 2. Insertar todos los datos
        df_ventas.to_sql(
            "ventas_diarias",
            conn,
            if_exists="append",
            index=False,
            method="multi",  # Bulk insert
        )
```

---

### 1.2 Incremental Load (Carga Incremental)

**¿Qué es?**

Una carga incremental solo procesa y carga **los registros nuevos** desde la última ejecución.

**Analogía**: Solo compras y guardas en tu armario la ropa nueva que te faltaba, sin tocar la que ya tenías.

**¿Cómo funciona?**

```python
# Pseudocódigo
def incremental_load(df_origen, tabla_destino, ultima_fecha):
    # 1. Filtrar solo registros nuevos
    df_nuevos = df_origen[df_origen['fecha'] > ultima_fecha]

    # 2. Insertar solo los registros nuevos
    tabla_destino.insert(df_nuevos)

    # 3. Actualizar el marcador de tiempo
    guardar_ultima_fecha(df_nuevos['fecha'].max())
```

**Ventajas**:
- ✅ **Rápido**: Solo procesas datos nuevos
- ✅ **Eficiente**: Consume menos CPU, memoria y almacenamiento
- ✅ **Escalable**: Funciona con millones de filas
- ✅ **Menos bloqueos**: Operaciones más cortas

**Desventajas**:
- ❌ **Más complejo**: Necesitas rastrear qué ya cargaste
- ❌ **Requiere clave temporal**: Necesitas una columna de fecha/timestamp
- ❌ **No maneja updates**: Si un registro cambia, no lo detecta
- ❌ **Requiere estado**: Debes guardar "última fecha procesada"

**¿Cuándo usar Incremental Load?**

1. **Datos append-only**: Logs, transacciones, eventos que nunca se modifican
2. **Datasets grandes**: Millones de filas donde full load es impráctico
3. **Ejecución frecuente**: Pipelines que corren cada hora o en tiempo real
4. **Clave temporal confiable**: Tienes una columna `created_at` o `timestamp`
5. **Sin updates**: Los datos históricos no cambian

**Ejemplo real**:

```python
import pandas as pd
from datetime import datetime
from pathlib import Path

def incremental_load_logs(
    df_logs: pd.DataFrame,
    connection_string: str,
    checkpoint_file: str = "checkpoint.txt"
) -> None:
    """
    Carga incremental de logs basada en timestamp.

    Args:
        df_logs: DataFrame con logs a cargar
        connection_string: Conexión a la base de datos
        checkpoint_file: Archivo con último timestamp procesado
    """
    # 1. Leer último checkpoint (última fecha procesada)
    checkpoint_path = Path(checkpoint_file)
    if checkpoint_path.exists():
        last_timestamp = pd.to_datetime(checkpoint_path.read_text().strip())
    else:
        last_timestamp = pd.Timestamp("1900-01-01")  # Epoch antiguo

    # 2. Filtrar solo registros nuevos
    df_nuevos = df_logs[df_logs["timestamp"] > last_timestamp]

    if df_nuevos.empty:
        print("No hay datos nuevos para cargar")
        return

    # 3. Cargar solo registros nuevos
    engine = create_engine(connection_string)
    df_nuevos.to_sql(
        "logs",
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    # 4. Actualizar checkpoint
    new_checkpoint = df_nuevos["timestamp"].max()
    checkpoint_path.write_text(str(new_checkpoint))

    print(f"Cargados {len(df_nuevos)} registros nuevos")
```

---

### 1.3 Upsert (Insert + Update)

**¿Qué es?**

Un upsert (contracción de "update" + "insert") significa:
- **Insertar** registros que no existen
- **Actualizar** registros que ya existen y han cambiado

**Analogía**: Cada día revisas tu armario: la ropa nueva la guardas, y la que ya tenías pero está sucia, la lavas y reemplazas.

**¿Cómo funciona?**

```python
# Pseudocódigo
def upsert(df_origen, tabla_destino, clave_primaria):
    for registro in df_origen:
        if existe_en_destino(registro[clave_primaria]):
            # Actualizar registro existente
            tabla_destino.update(registro)
        else:
            # Insertar registro nuevo
            tabla_destino.insert(registro)
```

**Ventajas**:
- ✅ **Completo**: Maneja inserts Y updates
- ✅ **Eficiente**: Solo procesas cambios
- ✅ **Flexible**: Funciona con cualquier tipo de dato
- ✅ **Mantiene historial**: Puedes implementar SCD (Slowly Changing Dimensions)

**Desventajas**:
- ❌ **Complejidad alta**: La lógica es más difícil
- ❌ **Requiere clave primaria**: Necesitas identificar registros únicos
- ❌ **Más lento que incremental**: Cada registro requiere una comparación
- ❌ **Bloqueos**: Los updates pueden causar locks en la base de datos

**¿Cuándo usar Upsert?**

1. **Datos que cambian**: Clientes, productos, inventarios que se actualizan
2. **Tienes clave primaria**: ID único para identificar cada registro
3. **Necesitas actualizar**: No solo agregar, sino modificar datos existentes
4. **Data warehousing**: Dimensiones que cambian lentamente (SCD Type 1 o Type 2)
5. **Sincronización**: Replicar cambios desde un sistema fuente

**Ejemplo real (PostgreSQL)**:

```python
import pandas as pd
from sqlalchemy import create_engine

def upsert_clientes(
    df_clientes: pd.DataFrame,
    connection_string: str
) -> None:
    """
    Upsert de clientes: inserta nuevos, actualiza existentes.

    Args:
        df_clientes: DataFrame con clientes (debe tener 'id_cliente')
        connection_string: Conexión a PostgreSQL
    """
    engine = create_engine(connection_string)

    # Crear tabla temporal
    df_clientes.to_sql(
        "clientes_temp",
        engine,
        if_exists="replace",
        index=False,
    )

    # Upsert usando PostgreSQL ON CONFLICT
    upsert_query = """
    INSERT INTO clientes (id_cliente, nombre, email, ciudad, fecha_actualizacion)
    SELECT id_cliente, nombre, email, ciudad, fecha_actualizacion
    FROM clientes_temp
    ON CONFLICT (id_cliente) DO UPDATE SET
        nombre = EXCLUDED.nombre,
        email = EXCLUDED.email,
        ciudad = EXCLUDED.ciudad,
        fecha_actualizacion = EXCLUDED.fecha_actualizacion;
    """

    with engine.begin() as conn:
        conn.execute(upsert_query)
        conn.execute("DROP TABLE clientes_temp")

    print(f"Upsert completado: {len(df_clientes)} registros procesados")
```

**Comparación de estrategias**:

| Característica | Full Load | Incremental | Upsert |
|----------------|-----------|-------------|--------|
| **Velocidad** | 🐌 Lenta | 🚀 Rápida | 🏃 Media |
| **Complejidad** | 🟢 Simple | 🟡 Media | 🔴 Alta |
| **Maneja updates** | ✅ Sí | ❌ No | ✅ Sí |
| **Requiere clave** | ❌ No | ⚠️ Timestamp | ✅ ID único |
| **Escalabilidad** | ❌ Baja | ✅ Alta | 🟡 Media |
| **Costo** | 💰💰💰 Alto | 💰 Bajo | 💰💰 Medio |

---

## 2. Optimización de Carga: Bulk Inserts y Batch Processing

### 2.1 Row-by-Row vs Bulk Inserts

**Row-by-Row (Fila por Fila)**:

```python
# ❌ LENTO: 1 transacción por fila
for fila in df.iterrows():
    conn.execute(f"INSERT INTO tabla VALUES ({fila})")
```

**Problema**: Cada `INSERT` es una transacción separada con overhead de:
- Conexión de red
- Parsing de SQL
- Bloqueo de tabla
- Escritura a disco

**Para 10,000 filas**: ~30 segundos

**Bulk Insert**:

```python
# ✅ RÁPIDO: 1 transacción para todas las filas
df.to_sql("tabla", conn, if_exists="append", method="multi")
```

**Ventaja**: Una sola transacción, escritura optimizada, mínimo overhead.

**Para 10,000 filas**: ~0.5 segundos (¡60x más rápido!)

### 2.2 Batch Processing

Cuando el dataset es demasiado grande para cargar en memoria:

```python
def load_in_batches(
    df: pd.DataFrame,
    connection_string: str,
    batch_size: int = 10000
) -> None:
    """
    Carga datos en lotes para evitar problemas de memoria.

    Args:
        df: DataFrame grande a cargar
        connection_string: Conexión a BD
        batch_size: Tamaño de cada lote
    """
    engine = create_engine(connection_string)
    total_rows = len(df)

    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        batch = df.iloc[start:end]

        batch.to_sql(
            "tabla",
            engine,
            if_exists="append",
            index=False,
            method="multi",
        )

        print(f"Cargadas {end}/{total_rows} filas")
```

**Ventajas del batch processing**:
- Controla el uso de memoria
- Permite progreso incremental
- Facilita recuperación ante fallos
- Reduce bloqueos en la base de datos

---

## 3. Particionamiento de Datos

### 3.1 ¿Qué es el particionamiento?

**Analogía**: En lugar de tener una caja gigante con todos tus documentos, los organizas en carpetas por año: 2020, 2021, 2022, 2023. Cuando buscas algo de 2023, solo revisas esa carpeta.

**En bases de datos**: Dividir una tabla grande en partes más pequeñas (particiones) basadas en una columna clave (usualmente fecha).

### 3.2 Ventajas del particionamiento

1. **Consultas más rápidas**: Si filtras por fecha, solo se escanea la partición relevante
2. **Mantenimiento eficiente**: Puedes eliminar particiones antiguas sin tocar las nuevas
3. **Carga paralela**: Cargar múltiples particiones simultáneamente
4. **Mejor rendimiento**: Índices más pequeños, cache más efectivo

### 3.3 Ejemplo: Particionamiento por fecha

```python
def load_with_partitioning(
    df: pd.DataFrame,
    base_path: str,
    partition_col: str = "fecha"
) -> None:
    """
    Guarda datos particionados por fecha usando Parquet.

    Args:
        df: DataFrame a guardar
        base_path: Ruta base para particiones
        partition_col: Columna para particionar
    """
    # Pandas automáticamente crea particiones
    df.to_parquet(
        base_path,
        partition_cols=[partition_col],
        engine="pyarrow",
        compression="snappy",
    )

    # Resultado en disco:
    # base_path/
    #   fecha=2024-01-01/
    #     data.parquet
    #   fecha=2024-01-02/
    #     data.parquet
    #   fecha=2024-01-03/
    #     data.parquet
```

**Lectura de particiones específicas**:

```python
import pandas as pd

# Leer solo una partición
df_dia = pd.read_parquet(
    "base_path",
    filters=[("fecha", "==", "2024-01-01")]
)

# Leer rango de particiones
df_semana = pd.read_parquet(
    "base_path",
    filters=[("fecha", ">=", "2024-01-01"), ("fecha", "<=", "2024-01-07")]
)
```

---

## 4. Logging y Monitoreo de Pipelines

### 4.1 ¿Por qué es crítico el logging?

Imagina que tu pipeline falla a las 3am. Sin logging:
- ❌ No sabes qué falló
- ❌ No sabes cuándo falló
- ❌ No sabes cuántos datos se cargaron
- ❌ No puedes reproducir el error

Con logging profesional:
- ✅ Sabes exactamente dónde falló
- ✅ Tienes el stack trace completo
- ✅ Sabes cuántos datos se procesaron
- ✅ Puedes reanudar desde el punto de fallo

### 4.2 Implementación de logging profesional

```python
import logging
from datetime import datetime
from pathlib import Path

def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """
    Configura logging con archivo y consola.

    Args:
        log_dir: Directorio para archivos de log

    Returns:
        Logger configurado
    """
    # Crear directorio si no existe
    Path(log_dir).mkdir(exist_ok=True)

    # Nombre de archivo con timestamp
    log_file = Path(log_dir) / f"pipeline_{datetime.now():%Y%m%d_%H%M%S}.log"

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Archivo
            logging.StreamHandler(),  # Consola
        ],
    )

    return logging.getLogger(__name__)


def load_with_logging(df: pd.DataFrame, connection_string: str) -> None:
    """
    Carga datos con logging completo.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD
    """
    logger = setup_logging()

    logger.info(f"Iniciando carga de {len(df)} registros")
    start_time = datetime.now()

    try:
        engine = create_engine(connection_string)

        logger.info("Conexión a base de datos establecida")

        df.to_sql(
            "tabla",
            engine,
            if_exists="append",
            index=False,
            method="multi",
        )

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Carga completada exitosamente en {duration:.2f} segundos")
        logger.info(f"Filas cargadas: {len(df)}")

    except Exception as e:
        logger.error(f"Error durante la carga: {str(e)}", exc_info=True)
        raise
```

### 4.3 Métricas de monitoreo

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LoadMetrics:
    """Métricas de ejecución del pipeline."""

    start_time: datetime
    end_time: datetime
    rows_processed: int
    rows_inserted: int
    rows_updated: int
    rows_failed: int
    duration_seconds: float
    success: bool
    error_message: str = ""

    def to_dict(self) -> dict:
        """Convierte métricas a diccionario."""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "rows_processed": self.rows_processed,
            "rows_inserted": self.rows_inserted,
            "rows_updated": self.rows_updated,
            "rows_failed": self.rows_failed,
            "duration_seconds": self.duration_seconds,
            "success": self.success,
            "error_message": self.error_message,
        }


def load_with_metrics(df: pd.DataFrame, connection_string: str) -> LoadMetrics:
    """
    Carga datos y retorna métricas.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD

    Returns:
        Métricas de la ejecución
    """
    start_time = datetime.now()
    rows_processed = len(df)

    try:
        engine = create_engine(connection_string)
        df.to_sql("tabla", engine, if_exists="append", index=False, method="multi")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        return LoadMetrics(
            start_time=start_time,
            end_time=end_time,
            rows_processed=rows_processed,
            rows_inserted=rows_processed,
            rows_updated=0,
            rows_failed=0,
            duration_seconds=duration,
            success=True,
        )

    except Exception as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        return LoadMetrics(
            start_time=start_time,
            end_time=end_time,
            rows_processed=rows_processed,
            rows_inserted=0,
            rows_updated=0,
            rows_failed=rows_processed,
            duration_seconds=duration,
            success=False,
            error_message=str(e),
        )
```

---

## 5. Patrones de Diseño para Pipelines Robustos

### 5.1 Idempotencia

**Definición**: Un pipeline es idempotente si ejecutarlo múltiples veces con los mismos datos produce el mismo resultado.

**Analogía**: Si presionas el botón de "Guardar" en tu documento 10 veces, no crea 10 copias. Solo guarda una vez.

**¿Por qué es importante?**

- Puedes re-ejecutar el pipeline sin miedo a duplicar datos
- Facilita la recuperación ante fallos
- Permite retry automático

**Ejemplo sin idempotencia (❌ MALO)**:

```python
def load_ventas(df_ventas):
    # ❌ Cada ejecución agrega duplicados
    df_ventas.to_sql("ventas", engine, if_exists="append")
```

**Ejemplo con idempotencia (✅ BUENO)**:

```python
def load_ventas_idempotente(df_ventas, fecha):
    """
    Carga idempotente: elimina datos de la fecha y recarga.

    Args:
        df_ventas: Ventas a cargar
        fecha: Fecha de las ventas
    """
    with engine.begin() as conn:
        # 1. Eliminar datos existentes de esta fecha
        conn.execute(f"DELETE FROM ventas WHERE fecha = '{fecha}'")

        # 2. Insertar datos
        df_ventas.to_sql("ventas", conn, if_exists="append", index=False)

    # Ahora puedes ejecutar esto 10 veces y el resultado es el mismo
```

### 5.2 Checkpointing

**Definición**: Guardar el estado del pipeline para poder reanudar desde el último punto exitoso.

**Ejemplo**:

```python
def load_with_checkpointing(
    df: pd.DataFrame,
    connection_string: str,
    batch_size: int = 10000
) -> None:
    """
    Carga con checkpointing para reanudar ante fallos.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD
        batch_size: Tamaño de lote
    """
    checkpoint_file = Path("checkpoint.txt")

    # Leer último batch exitoso
    if checkpoint_file.exists():
        last_batch = int(checkpoint_file.read_text())
    else:
        last_batch = 0

    engine = create_engine(connection_string)
    total_batches = len(df) // batch_size + 1

    for batch_num in range(last_batch, total_batches):
        start = batch_num * batch_size
        end = min(start + batch_size, len(df))
        batch = df.iloc[start:end]

        try:
            batch.to_sql("tabla", engine, if_exists="append", index=False, method="multi")

            # Guardar checkpoint
            checkpoint_file.write_text(str(batch_num + 1))
            print(f"Batch {batch_num + 1}/{total_batches} completado")

        except Exception as e:
            print(f"Error en batch {batch_num}: {e}")
            raise

    # Limpiar checkpoint al finalizar
    checkpoint_file.unlink()
```

### 5.3 Transacciones y Rollback

**Principio**: Una transacción es "todo o nada". Si algo falla, deshaces todo el cambio.

```python
def load_with_transaction(df: pd.DataFrame, connection_string: str) -> None:
    """
    Carga con transacción: si falla, hace rollback.

    Args:
        df: DataFrame a cargar
        connection_string: Conexión a BD
    """
    engine = create_engine(connection_string)

    try:
        with engine.begin() as conn:  # Inicia transacción
            # Operación 1
            conn.execute("DELETE FROM ventas WHERE fecha = '2024-01-01'")

            # Operación 2
            df.to_sql("ventas", conn, if_exists="append", index=False)

            # Si todo funciona, hace COMMIT automáticamente

    except Exception as e:
        # Si algo falla, hace ROLLBACK automáticamente
        print(f"Error: {e}. Todos los cambios fueron revertidos")
        raise
```

---

## 6. Aplicaciones Prácticas en Data Engineering

### 6.1 Caso 1: E-commerce

**Escenario**: Tienda online con 1M de productos y 100K transacciones diarias.

**Estrategia**:
- **Productos**: Upsert (los precios cambian)
- **Transacciones**: Incremental (solo se agregan, no cambian)
- **Clientes**: Upsert (direcciones y emails cambian)

### 6.2 Caso 2: Data Warehouse

**Escenario**: Data warehouse con arquitectura Kimball (star schema).

**Estrategia**:
- **Dimensiones pequeñas** (20-30 países): Full load
- **Dimensiones grandes** (1M clientes): Upsert con SCD Type 2
- **Hechos** (transacciones): Incremental particionado por fecha

### 6.3 Caso 3: Logs de Aplicación

**Escenario**: Aplicación web con 10M de logs por día.

**Estrategia**:
- **Carga**: Incremental con batch processing
- **Particionamiento**: Por fecha (una partición por día)
- **Retención**: Eliminar particiones >90 días

---

## 7. Errores Comunes y Cómo Evitarlos

### Error 1: No validar datos antes de cargar

**Problema**: Cargas datos con valores nulos, duplicados o tipos incorrectos.

**Solución**:
```python
def validate_before_load(df: pd.DataFrame) -> None:
    """Valida datos antes de cargar."""
    # 1. Verificar columnas requeridas
    required_cols = ["id", "nombre", "fecha"]
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")

    # 2. Verificar nulos en columnas críticas
    null_counts = df[required_cols].isnull().sum()
    if null_counts.any():
        raise ValueError(f"Valores nulos encontrados: {null_counts}")

    # 3. Verificar duplicados
    if df.duplicated(subset=["id"]).any():
        raise ValueError("IDs duplicados encontrados")
```

### Error 2: No usar transacciones

**Problema**: Si el pipeline falla a mitad de la carga, quedas con datos parciales.

**Solución**: Siempre usa `with engine.begin()` para transacciones automáticas.

### Error 3: Ignorar el tamaño de los lotes

**Problema**: Intentas cargar 10M de filas en una sola transacción y te quedas sin memoria.

**Solución**: Usa batch processing con lotes de 10K-100K filas.

### Error 4: No implementar logging

**Problema**: Cuando el pipeline falla, no sabes por qué.

**Solución**: Implementa logging desde el día 1.

### Error 5: No hacer backups antes de cargas grandes

**Problema**: Sobrescribes datos importantes por accidente.

**Solución**: Siempre haz backup antes de operaciones destructivas.

---

## 8. Lista de Verificación de Aprendizaje

Al finalizar este tema, deberías poder:

- [ ] **Explicar las tres estrategias de carga** (full, incremental, upsert) y cuándo usar cada una
- [ ] **Entender la diferencia** entre row-by-row y bulk inserts
- [ ] **Implementar batch processing** para datasets grandes
- [ ] **Explicar qué es el particionamiento** y sus ventajas
- [ ] **Implementar logging profesional** en un pipeline
- [ ] **Definir qué es idempotencia** y por qué es importante
- [ ] **Implementar checkpointing** para reanudar pipelines
- [ ] **Usar transacciones** para garantizar consistencia
- [ ] **Diseñar una estrategia de carga** para un caso de negocio real
- [ ] **Monitorear métricas** de un pipeline (filas procesadas, duración, errores)

---

## 9. Recursos Adicionales

### Libros Recomendados
- "Data Pipelines Pocket Reference" - James Densmore (Capítulo 5: Loading Data)
- "Designing Data-Intensive Applications" - Martin Kleppmann (Capítulo 3: Storage)

### Documentación Oficial
- PostgreSQL: `ON CONFLICT` para upserts
- SQLAlchemy: Bulk operations
- Pandas: `to_sql()` con `method='multi'`

### Artículos
- "Batch vs Streaming ETL" - Databricks
- "Best Practices for Data Loading" - Snowflake

---

## Conclusión

La fase de carga es donde tu pipeline ETL se encuentra con la realidad:
- ¿Será lo suficientemente rápido para cumplir los SLAs?
- ¿Será robusto ante fallos?
- ¿Escalará cuando los datos crezcan 10x?

Las tres estrategias fundamentales (full load, incremental, upsert) son tus herramientas principales. Cada una tiene su lugar:
- **Full load**: Simplicidad cuando el dataset es pequeño
- **Incremental**: Velocidad cuando los datos solo crecen
- **Upsert**: Flexibilidad cuando los datos cambian

Combínalas con:
- **Bulk inserts** para velocidad
- **Particionamiento** para escalabilidad
- **Logging** para observabilidad
- **Idempotencia** para confiabilidad

Y construirás pipelines de nivel profesional que funcionan en producción 24/7.

En el siguiente documento (`02-EJEMPLOS.md`), veremos estas estrategias en acción con casos reales y código ejecutable.

**¡Éxito en tu aprendizaje!** 🚀
