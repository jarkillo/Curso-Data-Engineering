# Ejemplos Prácticos: Conceptos de ETL/ELT

**Tiempo de lectura**: 45-60 minutos
**Nivel**: Intermedio
**Prerrequisitos**: Haber leído `01-TEORIA.md`

---

## Introducción

En este archivo encontrarás 5 ejemplos trabajados paso a paso que ilustran los conceptos de pipelines de datos. Cada ejemplo incluye:
- Contexto empresarial realista
- Datos de ejemplo
- Código Python completo
- Explicación detallada de cada paso
- Interpretación de resultados

**Recomendación**: Ejecuta el código en tu entorno para experimentar.

---

## Datos de Ejemplo

Para todos los ejemplos, usaremos una empresa ficticia:

**TechStore**: E-commerce de productos electrónicos con 5 sucursales.

Archivos de datos (debes crear estos archivos para ejecutar los ejemplos):

### `ventas_2025.csv`
```csv
fecha,sucursal,producto,cantidad,precio_unitario
2025-10-01,Madrid,Laptop Dell,2,899.99
2025-10-01,Barcelona,Mouse Logitech,5,29.99
2025-10-02,Madrid,Teclado Mecánico,3,149.99
2025-10-02,Valencia,Monitor Samsung,1,399.99
2025-10-03,Barcelona,Laptop HP,1,799.99
2025-10-03,Sevilla,Auriculares Sony,4,79.99
2025-10-04,Madrid,SSD 1TB,2,119.99
2025-10-04,Barcelona,Webcam Logitech,3,89.99
2025-10-05,Valencia,Laptop Dell,1,899.99
2025-10-05,Sevilla,Mouse Wireless,6,19.99
```

---

## Ejemplo 1: Pipeline ETL Básico (CSV → Transform → SQLite)

### Nivel: Básico ⭐

### Contexto

TechStore necesita un pipeline que:
1. Lea ventas diarias desde CSV
2. Calcule el total de cada venta (cantidad × precio)
3. Guarde en una base de datos SQLite

Este es un pipeline **ETL**: transforma antes de cargar.

---

### Paso 1: Extract (Leer CSV)

```python
import pandas as pd
from pathlib import Path

def extraer_ventas(archivo: str) -> pd.DataFrame:
    """
    Extrae datos de ventas desde un archivo CSV.

    Args:
        archivo: Ruta al archivo CSV

    Returns:
        DataFrame con las ventas
    """
    print(f"📂 Leyendo archivo: {archivo}")

    # Validar que el archivo existe
    if not Path(archivo).exists():
        raise FileNotFoundError(f"Archivo {archivo} no encontrado")

    # Leer CSV
    ventas = pd.read_csv(archivo)

    print(f"✅ Extraídas {len(ventas)} ventas")
    return ventas


# Ejecutar extracción
ventas = extraer_ventas("ventas_2025.csv")
print(ventas.head())
```

**Output**:
```
📂 Leyendo archivo: ventas_2025.csv
✅ Extraídas 10 ventas
        fecha   sucursal            producto  cantidad  precio_unitario
0  2025-10-01     Madrid        Laptop Dell         2           899.99
1  2025-10-01  Barcelona    Mouse Logitech         5            29.99
2  2025-10-02     Madrid  Teclado Mecánico         3           149.99
```

---

### Paso 2: Transform (Calcular Total)

```python
def transformar_ventas(ventas: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma los datos calculando el total de cada venta.

    Args:
        ventas: DataFrame con ventas crudas

    Returns:
        DataFrame con columna 'total' añadida
    """
    print("🔄 Transformando datos...")

    # Calcular total = cantidad × precio_unitario
    ventas['total'] = ventas['cantidad'] * ventas['precio_unitario']

    # Redondear a 2 decimales
    ventas['total'] = ventas['total'].round(2)

    print(f"✅ Transformación completada: {len(ventas)} filas")
    return ventas


# Ejecutar transformación
ventas_transformadas = transformar_ventas(ventas)
print(ventas_transformadas.head())
```

**Output**:
```
🔄 Transformando datos...
✅ Transformación completada: 10 filas
        fecha   sucursal            producto  cantidad  precio_unitario    total
0  2025-10-01     Madrid        Laptop Dell         2           899.99  1799.98
1  2025-10-01  Barcelona    Mouse Logitech         5            29.99   149.95
2  2025-10-02     Madrid  Teclado Mecánico         3           149.99   449.97
```

---

### Paso 3: Load (Guardar en SQLite)

```python
import sqlite3
from typing import Optional

def cargar_en_db(ventas: pd.DataFrame, db_path: str = "ventas.db") -> None:
    """
    Carga las ventas en una base de datos SQLite.

    Args:
        ventas: DataFrame con ventas transformadas
        db_path: Ruta a la base de datos SQLite
    """
    print(f"💾 Cargando datos en {db_path}...")

    # Conectar a SQLite (crea la DB si no existe)
    conn = sqlite3.connect(db_path)

    try:
        # Cargar DataFrame en tabla 'ventas'
        # if_exists='replace' → Reemplaza la tabla (idempotente)
        ventas.to_sql('ventas', conn, if_exists='replace', index=False)

        print(f"✅ Cargadas {len(ventas)} filas en la tabla 'ventas'")
    finally:
        conn.close()


# Ejecutar carga
cargar_en_db(ventas_transformadas)

# Verificar que se cargó correctamente
conn = sqlite3.connect("ventas.db")
resultado = pd.read_sql("SELECT * FROM ventas LIMIT 3", conn)
conn.close()

print("\n📊 Primeras 3 filas en la base de datos:")
print(resultado)
```

**Output**:
```
💾 Cargando datos en ventas.db...
✅ Cargadas 10 filas en la tabla 'ventas'

📊 Primeras 3 filas en la base de datos:
        fecha   sucursal            producto  cantidad  precio_unitario    total
0  2025-10-01     Madrid        Laptop Dell         2           899.99  1799.98
1  2025-10-01  Barcelona    Mouse Logitech         5            29.99   149.95
2  2025-10-02     Madrid  Teclado Mecánico         3           149.99   449.97
```

---

### Pipeline Completo (ETL)

```python
def pipeline_etl_basico(archivo_csv: str, db_path: str = "ventas.db") -> None:
    """
    Pipeline ETL completo: Extract → Transform → Load.

    Args:
        archivo_csv: Archivo CSV con ventas
        db_path: Base de datos de destino
    """
    print("🚀 Iniciando Pipeline ETL...")

    # 1. Extract
    ventas = extraer_ventas(archivo_csv)

    # 2. Transform
    ventas_transformadas = transformar_ventas(ventas)

    # 3. Load
    cargar_en_db(ventas_transformadas, db_path)

    print("✅ Pipeline ETL completado exitosamente!")


# Ejecutar pipeline completo
pipeline_etl_basico("ventas_2025.csv")
```

---

### Interpretación de Resultados

**¿Qué logramos?**
- ✅ Automatizamos el proceso de cargar ventas diarias
- ✅ Calculamos el total de cada venta (ahorramos tiempo vs hacerlo manual)
- ✅ Centralizamos los datos en una base de datos (fácil de consultar)

**¿Es idempotente?**
- ✅ Sí, porque usamos `if_exists='replace'`
- Si ejecutamos el pipeline 2 veces, obtenemos el mismo resultado
- No hay duplicados

**Decisiones de negocio basadas en esto**:
```python
# Análisis rápido con SQL
conn = sqlite3.connect("ventas.db")
analisis = pd.read_sql("""
    SELECT sucursal, SUM(total) AS total_ventas
    FROM ventas
    GROUP BY sucursal
    ORDER BY total_ventas DESC
""", conn)
conn.close()

print(analisis)
```

**Output**:
```
    sucursal  total_ventas
0     Madrid       2369.94
1  Barcelona       1039.93
2   Valencia        1299.98
3    Sevilla        439.95
```

**Decisión**: Madrid es la sucursal más rentable. Podemos:
- Replicar estrategias de Madrid en otras sucursales
- Asignar más inventario a Madrid

---

## Ejemplo 2: Pipeline ELT (Load → Transform en SQL)

### Nivel: Básico ⭐

### Contexto

Ahora TechStore quiere usar **ELT**: cargar los datos **primero** (sin transformar) y hacer el cálculo de totales **en la base de datos** con SQL.

---

### Paso 1: Extract (Igual que antes)

```python
ventas = extraer_ventas("ventas_2025.csv")
```

---

### Paso 2: Load (Cargar SIN transformar)

```python
def cargar_datos_crudos(ventas: pd.DataFrame, db_path: str = "ventas.db") -> None:
    """
    Carga datos CRUDOS sin transformar (ELT).

    Args:
        ventas: DataFrame con ventas sin transformar
        db_path: Ruta a la base de datos
    """
    print(f"💾 Cargando datos CRUDOS en {db_path}...")

    conn = sqlite3.connect(db_path)
    try:
        # Cargar datos SIN la columna 'total'
        ventas.to_sql('ventas_crudas', conn, if_exists='replace', index=False)
        print(f"✅ Cargadas {len(ventas)} filas en 'ventas_crudas'")
    finally:
        conn.close()


# Cargar datos crudos
cargar_datos_crudos(ventas)
```

---

### Paso 3: Transform (Dentro de la base de datos)

```python
def transformar_en_db(db_path: str = "ventas.db") -> pd.DataFrame:
    """
    Transforma datos DENTRO de la base de datos usando SQL.

    Args:
        db_path: Ruta a la base de datos

    Returns:
        DataFrame con datos transformados
    """
    print("🔄 Transformando datos dentro de la base de datos...")

    conn = sqlite3.connect(db_path)
    try:
        # Crear vista con el total calculado
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ventas_procesadas AS
            SELECT
                fecha,
                sucursal,
                producto,
                cantidad,
                precio_unitario,
                ROUND(cantidad * precio_unitario, 2) AS total
            FROM ventas_crudas
        """)

        # Leer resultado
        resultado = pd.read_sql("SELECT * FROM ventas_procesadas", conn)

        print(f"✅ Transformación completada: {len(resultado)} filas")
        return resultado
    finally:
        conn.close()


# Transformar en la base de datos
ventas_procesadas = transformar_en_db()
print(ventas_procesadas.head())
```

---

### Pipeline Completo (ELT)

```python
def pipeline_elt(archivo_csv: str, db_path: str = "ventas.db") -> None:
    """
    Pipeline ELT completo: Extract → Load → Transform.

    Args:
        archivo_csv: Archivo CSV con ventas
        db_path: Base de datos de destino
    """
    print("🚀 Iniciando Pipeline ELT...")

    # 1. Extract
    ventas = extraer_ventas(archivo_csv)

    # 2. Load (datos crudos)
    cargar_datos_crudos(ventas, db_path)

    # 3. Transform (dentro de la DB)
    ventas_procesadas = transformar_en_db(db_path)

    print("✅ Pipeline ELT completado exitosamente!")
    return ventas_procesadas


# Ejecutar pipeline ELT
pipeline_elt("ventas_2025.csv")
```

---

### Interpretación de Resultados

**¿Qué diferencia hay con ETL?**

| Aspecto            | ETL (Ejemplo 1)                                     | ELT (Ejemplo 2)                      |
| ------------------ | --------------------------------------------------- | ------------------------------------ |
| **Transformación** | En Python (Pandas)                                  | En SQL (dentro de la DB)             |
| **Datos cargados** | Ya transformados                                    | Crudos                               |
| **Flexibilidad**   | Si quieres cambiar transformación, debes reprocesar | Puedes re-transformar sin re-extraer |
| **Velocidad**      | Más lenta con grandes volúmenes                     | Más rápida (DB optimizada para SQL)  |

**¿Cuándo usar ELT?**
- ✅ Cuando tienes una base de datos potente (PostgreSQL, Snowflake)
- ✅ Cuando quieres flexibilidad para re-transformar
- ✅ Cuando trabajas con grandes volúmenes

---

## Ejemplo 3: Pipeline Batch Diario (Programado)

### Nivel: Intermedio ⭐⭐

### Contexto

TechStore necesita un pipeline que se ejecute **automáticamente cada día** a las 3:00 AM para procesar las ventas del día anterior.

---

### Paso 1: Pipeline con Fecha Parametrizada

```python
from datetime import datetime, timedelta

def pipeline_batch_diario(fecha: str, db_path: str = "ventas.db") -> None:
    """
    Pipeline batch que procesa ventas de una fecha específica.

    Args:
        fecha: Fecha a procesar (formato: YYYY-MM-DD)
        db_path: Base de datos de destino
    """
    print(f"🚀 Iniciando Pipeline Batch para fecha: {fecha}")

    # 1. Extract: Leer TODAS las ventas
    ventas = extraer_ventas("ventas_2025.csv")

    # 2. Filter: Quedarnos solo con las ventas de la fecha
    ventas_fecha = ventas[ventas['fecha'] == fecha].copy()

    if len(ventas_fecha) == 0:
        print(f"⚠️ No hay ventas para la fecha {fecha}")
        return

    print(f"📊 Encontradas {len(ventas_fecha)} ventas para {fecha}")

    # 3. Transform: Calcular total
    ventas_fecha['total'] = (ventas_fecha['cantidad'] *
                              ventas_fecha['precio_unitario']).round(2)

    # 4. Load: Cargar en la DB (idempotente)
    conn = sqlite3.connect(db_path)
    try:
        # Borrar ventas de esa fecha primero (idempotencia)
        conn.execute("DELETE FROM ventas WHERE fecha = ?", (fecha,))

        # Insertar ventas nuevas
        ventas_fecha.to_sql('ventas', conn, if_exists='append', index=False)

        print(f"✅ Cargadas {len(ventas_fecha)} ventas para {fecha}")
    finally:
        conn.close()

    print(f"✅ Pipeline Batch completado para {fecha}")


# Ejecutar para diferentes fechas
pipeline_batch_diario("2025-10-01")
pipeline_batch_diario("2025-10-02")
pipeline_batch_diario("2025-10-03")
```

**Output**:
```
🚀 Iniciando Pipeline Batch para fecha: 2025-10-01
📊 Encontradas 2 ventas para 2025-10-01
✅ Cargadas 2 ventas para 2025-10-01
✅ Pipeline Batch completado para 2025-10-01

🚀 Iniciando Pipeline Batch para fecha: 2025-10-02
📊 Encontradas 2 ventas para 2025-10-02
✅ Cargadas 2 ventas para 2025-10-02
✅ Pipeline Batch completado para 2025-10-02
...
```

---

### Paso 2: Programar Ejecución Automática (Simulación)

```python
def pipeline_automatico():
    """
    Simula un pipeline que se ejecuta cada día.
    En producción, esto se haría con cron o Apache Airflow.
    """
    # Obtener la fecha de ayer
    ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"⏰ Ejecutando pipeline programado para {ayer}")

    try:
        pipeline_batch_diario(ayer)
    except Exception as e:
        print(f"❌ Error en el pipeline: {e}")
        # En producción, aquí enviarías una alerta (email, Slack, etc.)


# Ejecutar pipeline automático
pipeline_automatico()
```

---

### Interpretación de Resultados

**¿Qué logramos?**
- ✅ Pipeline parametrizado por fecha (flexible)
- ✅ Idempotente (DELETE antes de INSERT)
- ✅ Manejo de casos borde (¿qué pasa si no hay ventas?)
- ✅ Listo para programarse con cron o Airflow

**Ventajas del Batch Processing**:
- Simple de implementar
- Usa recursos eficientemente (procesa todo de golpe)
- Perfecto para reportes diarios

**Limitaciones**:
- Latencia alta (datos disponibles solo una vez al día)
- No sirve para decisiones en tiempo real

---

## Ejemplo 4: Pipeline con Reprocessing (Corregir Datos Históricos)

### Nivel: Intermedio ⭐⭐

### Contexto

TechStore descubre que el pipeline del 1 al 5 de octubre tenía un **bug**: no calculaba correctamente el IVA (21%). Necesitan **reprocesar** esos días.

---

### Paso 1: Pipeline con Bug (Incorrecto)

```python
def pipeline_con_bug(fecha: str) -> None:
    """
    Pipeline INCORRECTO que no calcula el IVA.
    """
    ventas = extraer_ventas("ventas_2025.csv")
    ventas_fecha = ventas[ventas['fecha'] == fecha].copy()

    # ❌ Bug: No suma el IVA
    ventas_fecha['total'] = (ventas_fecha['cantidad'] *
                              ventas_fecha['precio_unitario']).round(2)

    conn = sqlite3.connect("ventas.db")
    try:
        conn.execute("DELETE FROM ventas WHERE fecha = ?", (fecha,))
        ventas_fecha.to_sql('ventas', conn, if_exists='append', index=False)
    finally:
        conn.close()


# Simular que procesamos con bug
for dia in range(1, 6):
    fecha = f"2025-10-{dia:02d}"
    pipeline_con_bug(fecha)
    print(f"❌ Procesado (con bug) {fecha}")
```

---

### Paso 2: Corregir el Bug

```python
def pipeline_corregido(fecha: str) -> None:
    """
    Pipeline CORREGIDO que calcula el IVA correctamente.
    """
    ventas = extraer_ventas("ventas_2025.csv")
    ventas_fecha = ventas[ventas['fecha'] == fecha].copy()

    # ✅ Corrección: Sumar 21% de IVA
    ventas_fecha['total_sin_iva'] = (ventas_fecha['cantidad'] *
                                      ventas_fecha['precio_unitario']).round(2)
    ventas_fecha['total'] = (ventas_fecha['total_sin_iva'] * 1.21).round(2)

    conn = sqlite3.connect("ventas.db")
    try:
        # Idempotencia: Borra y re-inserta
        conn.execute("DELETE FROM ventas WHERE fecha = ?", (fecha,))
        ventas_fecha.to_sql('ventas', conn, if_exists='append', index=False)
    finally:
        conn.close()

    print(f"✅ Reprocesado (corregido) {fecha}")
```

---

### Paso 3: Reprocessing Masivo

```python
def reprocessing_fechas(fecha_inicio: str, fecha_fin: str) -> None:
    """
    Reprocesa un rango de fechas con el pipeline corregido.

    Args:
        fecha_inicio: Fecha inicial (YYYY-MM-DD)
        fecha_fin: Fecha final (YYYY-MM-DD)
    """
    print(f"🔄 Iniciando reprocessing de {fecha_inicio} a {fecha_fin}...")

    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    fecha_actual = inicio
    while fecha_actual <= fin:
        fecha_str = fecha_actual.strftime("%Y-%m-%d")
        pipeline_corregido(fecha_str)
        fecha_actual += timedelta(days=1)

    print("✅ Reprocessing completado!")


# Reprocesar del 1 al 5 de octubre
reprocessing_fechas("2025-10-01", "2025-10-05")
```

**Output**:
```
🔄 Iniciando reprocessing de 2025-10-01 a 2025-10-05...
✅ Reprocesado (corregido) 2025-10-01
✅ Reprocesado (corregido) 2025-10-02
✅ Reprocesado (corregido) 2025-10-03
✅ Reprocesado (corregido) 2025-10-04
✅ Reprocesado (corregido) 2025-10-05
✅ Reprocessing completado!
```

---

### Verificar Corrección

```python
# Comparar datos antes y después del reprocessing
conn = sqlite3.connect("ventas.db")

# Consulta antes (con bug): total promedio ~200€
# Consulta después (corregido): total promedio ~242€ (20% más por el IVA)
resultado = pd.read_sql("""
    SELECT
        fecha,
        COUNT(*) AS num_ventas,
        ROUND(AVG(total), 2) AS total_promedio
    FROM ventas
    WHERE fecha BETWEEN '2025-10-01' AND '2025-10-05'
    GROUP BY fecha
    ORDER BY fecha
""", conn)
conn.close()

print(resultado)
```

**Output**:
```
        fecha  num_ventas  total_promedio
0  2025-10-01           2          1180.93
1  2025-10-02           2           539.95
2  2025-10-03           2           532.48
3  2025-10-04           2           254.28
4  2025-10-05           2           559.48
```

---

### Interpretación de Resultados

**¿Por qué fue posible el reprocessing?**
- ✅ **Idempotencia**: El pipeline borra y re-inserta (DELETE + INSERT)
- ✅ **Particionamiento por fecha**: Podemos reprocesar solo días específicos
- ✅ **Fuente de datos conservada**: El CSV original sigue disponible

**Lecciones aprendidas**:
1. **Siempre diseña pipelines idempotentes** → Podrás reprocesar sin problemas
2. **Particiona por fecha** → Reprocessing más eficiente
3. **Guarda logs detallados** → Podrás identificar cuándo comenzó el bug
4. **Testea con datos reales** → Descubre bugs antes de producción

---

## Ejemplo 5: Pipeline con Logging y Manejo de Errores

### Nivel: Avanzado ⭐⭐⭐

### Contexto

TechStore necesita un pipeline **productivo** con:
- Logging detallado
- Manejo de errores
- Reintentos automáticos
- Métricas de ejecución

---

### Paso 1: Configurar Logging

```python
import logging
import time
from typing import Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

---

### Paso 2: Pipeline con Logging y Métricas

```python
def pipeline_produccion(fecha: str, db_path: str = "ventas.db") -> Dict[str, Any]:
    """
    Pipeline de producción con logging, métricas y manejo de errores.

    Args:
        fecha: Fecha a procesar
        db_path: Base de datos de destino

    Returns:
        Dict con métricas de ejecución
    """
    inicio = time.time()
    metricas = {
        'fecha': fecha,
        'filas_extraidas': 0,
        'filas_procesadas': 0,
        'filas_cargadas': 0,
        'tiempo_segundos': 0,
        'estado': 'INICIADO'
    }

    try:
        logger.info(f"🚀 Iniciando pipeline para fecha: {fecha}")

        # 1. Extract
        logger.info("📂 Extrayendo datos...")
        ventas = extraer_ventas("ventas_2025.csv")
        metricas['filas_extraidas'] = len(ventas)
        logger.info(f"✅ Extraídas {len(ventas)} filas")

        # 2. Filter
        logger.info(f"🔍 Filtrando ventas de {fecha}...")
        ventas_fecha = ventas[ventas['fecha'] == fecha].copy()

        if len(ventas_fecha) == 0:
            logger.warning(f"⚠️ No hay ventas para {fecha}")
            metricas['estado'] = 'SIN_DATOS'
            return metricas

        logger.info(f"✅ Encontradas {len(ventas_fecha)} ventas")

        # 3. Transform
        logger.info("🔄 Transformando datos...")
        ventas_fecha['total'] = (ventas_fecha['cantidad'] *
                                  ventas_fecha['precio_unitario'] * 1.21).round(2)
        metricas['filas_procesadas'] = len(ventas_fecha)
        logger.info(f"✅ Transformadas {len(ventas_fecha)} filas")

        # 4. Load
        logger.info(f"💾 Cargando datos en {db_path}...")
        conn = sqlite3.connect(db_path)
        try:
            # Idempotencia
            filas_borradas = conn.execute(
                "DELETE FROM ventas WHERE fecha = ?", (fecha,)
            ).rowcount

            if filas_borradas > 0:
                logger.info(f"🗑️ Borradas {filas_borradas} filas existentes")

            # Cargar nuevas filas
            ventas_fecha.to_sql('ventas', conn, if_exists='append', index=False)
            metricas['filas_cargadas'] = len(ventas_fecha)
            logger.info(f"✅ Cargadas {len(ventas_fecha)} filas")
        finally:
            conn.close()

        # Métricas finales
        metricas['tiempo_segundos'] = round(time.time() - inicio, 2)
        metricas['estado'] = 'EXITOSO'
        logger.info(f"✅ Pipeline completado en {metricas['tiempo_segundos']}s")

        return metricas

    except FileNotFoundError as e:
        logger.error(f"❌ Archivo no encontrado: {e}")
        metricas['estado'] = 'ERROR_ARCHIVO'
        raise

    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}", exc_info=True)
        metricas['estado'] = 'ERROR'
        raise
    finally:
        # Siempre registrar métricas finales
        logger.info(f"📊 Métricas: {metricas}")


# Ejecutar pipeline de producción
metricas = pipeline_produccion("2025-10-01")
print(metricas)
```

**Output (en consola y en pipeline.log)**:
```
2025-10-23 10:30:15 - __main__ - INFO - 🚀 Iniciando pipeline para fecha: 2025-10-01
2025-10-23 10:30:15 - __main__ - INFO - 📂 Extrayendo datos...
2025-10-23 10:30:15 - __main__ - INFO - ✅ Extraídas 10 filas
2025-10-23 10:30:15 - __main__ - INFO - 🔍 Filtrando ventas de 2025-10-01...
2025-10-23 10:30:15 - __main__ - INFO - ✅ Encontradas 2 ventas
2025-10-23 10:30:15 - __main__ - INFO - 🔄 Transformando datos...
2025-10-23 10:30:15 - __main__ - INFO - ✅ Transformadas 2 filas
2025-10-23 10:30:15 - __main__ - INFO - 💾 Cargando datos en ventas.db...
2025-10-23 10:30:15 - __main__ - INFO - ✅ Cargadas 2 filas
2025-10-23 10:30:15 - __main__ - INFO - ✅ Pipeline completado en 0.12s
2025-10-23 10:30:15 - __main__ - INFO - 📊 Métricas: {...}

{'fecha': '2025-10-01', 'filas_extraidas': 10, 'filas_procesadas': 2,
 'filas_cargadas': 2, 'tiempo_segundos': 0.12, 'estado': 'EXITOSO'}
```

---

### Paso 3: Manejo de Errores con Reintentos

```python
import time
from typing import Callable

def retry_con_exponential_backoff(
    func: Callable,
    max_intentos: int = 3,
    *args,
    **kwargs
) -> Any:
    """
    Ejecuta una función con reintentos y exponential backoff.

    Args:
        func: Función a ejecutar
        max_intentos: Número máximo de reintentos
        *args: Argumentos para la función
        **kwargs: Argumentos con nombre para la función

    Returns:
        Resultado de la función si tiene éxito

    Raises:
        La última excepción si todos los intentos fallan
    """
    for intento in range(1, max_intentos + 1):
        try:
            logger.info(f"🔄 Intento {intento}/{max_intentos}")
            resultado = func(*args, **kwargs)
            logger.info(f"✅ Éxito en intento {intento}")
            return resultado

        except Exception as e:
            logger.warning(f"⚠️ Intento {intento} falló: {e}")

            if intento == max_intentos:
                logger.error(f"❌ Todos los intentos fallaron")
                raise

            # Exponential backoff: 2^intento segundos
            espera = 2 ** intento
            logger.info(f"⏳ Esperando {espera}s antes de reintentar...")
            time.sleep(espera)


# Ejemplo de uso
try:
    metricas = retry_con_exponential_backoff(
        pipeline_produccion,
        max_intentos=3,
        fecha="2025-10-01"
    )
    print(f"✅ Pipeline exitoso: {metricas}")
except Exception as e:
    print(f"❌ Pipeline falló después de todos los reintentos: {e}")
```

---

### Interpretación de Resultados

**¿Qué logramos con este pipeline de producción?**

1. **Logging detallado**:
   - Cada paso está registrado
   - Fácil de debuggear cuando algo falla
   - Auditoría completa de ejecuciones

2. **Métricas**:
   - Cuántas filas se procesaron
   - Cuánto tiempo tomó
   - Estado final (EXITOSO, ERROR, SIN_DATOS)
   - Útil para monitoreo y alertas

3. **Manejo de errores**:
   - Diferentes tipos de errores (archivo no encontrado, error de DB, etc.)
   - Logs de errores con stack trace completo
   - Reintentos automáticos con exponential backoff

4. **Idempotencia garantizada**:
   - DELETE + INSERT
   - Logs indican si se borraron filas existentes

**Este es un pipeline listo para producción** ✅

---

## Resumen de los Ejemplos

| Ejemplo | Concepto     | Nivel | Aprendizaje Clave                                     |
| ------- | ------------ | ----- | ----------------------------------------------------- |
| 1       | ETL Básico   | ⭐     | Extract → Transform → Load (transformación en Python) |
| 2       | ELT          | ⭐     | Extract → Load → Transform (transformación en SQL)    |
| 3       | Batch Diario | ⭐⭐    | Pipelines parametrizados por fecha, idempotencia      |
| 4       | Reprocessing | ⭐⭐    | Corregir bugs reprocesando datos históricos           |
| 5       | Producción   | ⭐⭐⭐   | Logging, métricas, reintentos, manejo de errores      |

---

## Próximos Pasos

Ahora que has visto pipelines en acción, es tu turno de practicar:

1. **Ejecuta todos los ejemplos** en tu entorno local
2. **Modifica el código**: Prueba diferentes transformaciones
3. **Continúa con `03-EJERCICIOS.md`**: 15 ejercicios para dominar los conceptos
4. **Proyecto práctico**: Implementa tu propio pipeline con TDD

---

**¡Felicidades!** Has completado los ejemplos del Tema 1. Ahora tienes las bases para diseñar pipelines robustos y escalables.

**Última actualización**: 2025-10-23
---

## 🧭 Navegación

⬅️ **Anterior**: [01 Teoria](01-TEORIA.md) | ➡️ **Siguiente**: [03 Ejercicios](03-EJERCICIOS.md)
