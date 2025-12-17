# Ejercicios Prácticos: Conceptos de ETL/ELT

**Tiempo estimado**: 2-4 horas
**Nivel**: Intermedio
**Prerrequisitos**: Haber leído `01-TEORIA.md` y `02-EJEMPLOS.md`

---

## Instrucciones Generales

1. **Intenta resolver cada ejercicio por tu cuenta** antes de ver la solución
2. **Ejecuta el código** para verificar que funciona
3. **Experimenta**: Modifica el código y observa qué pasa
4. **Usa la tabla de autoevaluación** al final para tracking tu progreso

---

## Datos de Ejemplo

Para algunos ejercicios, necesitarás estos archivos:

### `productos.csv`
```csv
id,nombre,precio,categoria
1,Laptop Dell,899.99,Computadoras
2,Mouse Logitech,29.99,Accesorios
3,Teclado Mecánico,149.99,Accesorios
4,Monitor Samsung,399.99,Pantallas
5,SSD 1TB,119.99,Almacenamiento
```

### `ventas_octubre.csv`
```csv
fecha,producto_id,cantidad,tienda
2025-10-01,1,2,Madrid
2025-10-01,2,5,Barcelona
2025-10-02,3,3,Madrid
2025-10-02,4,1,Valencia
2025-10-03,5,2,Sevilla
```

---

## Ejercicios Básicos (⭐)

### Ejercicio 1: Identificar ETL vs ELT
**Dificultad**: ⭐ Fácil

**Contexto**:
Trabajas en **DataFlow Analytics** y te presentan dos propuestas de pipeline para procesar logs de servidores.

**Propuesta A**:
```
1. Leer logs del servidor (1GB)
2. Filtrar solo errores (reduce a 10MB)
3. Calcular estadísticas (agregaciones)
4. Guardar resultados en PostgreSQL (10MB)
```

**Propuesta B**:
```
1. Leer logs del servidor (1GB)
2. Guardar TODO en Snowflake (1GB)
3. Ejecutar SQL en Snowflake para filtrar y agregar
```

**Pregunta**:
1. ¿Cuál es ETL y cuál es ELT?
2. ¿Cuál recomendarías si tienes un servidor pequeño?
3. ¿Cuál recomendarías si ya tienes Snowflake?

**Ayuda**:
- ETL transforma ANTES de cargar
- ELT transforma DESPUÉS de cargar

---

### Ejercicio 2: Hacer un Pipeline Idempotente
**Dificultad**: ⭐ Fácil

**Contexto**:
Este pipeline de **StreamingCo** NO es idempotente:

```python
import sqlite3

def pipeline_no_idempotente(fecha: str):
    conn = sqlite3.connect("videos.db")

    # ❌ Siempre inserta (duplica si ejecutas 2 veces)
    conn.execute("""
        INSERT INTO videos_vistos (fecha, video_id, vistas)
        VALUES (?, 101, 1500)
    """, (fecha,))

    conn.commit()
    conn.close()
```

**Tu tarea**:
1. Modifica el código para que sea idempotente
2. Ejecuta el pipeline 3 veces y verifica que NO hay duplicados

**Ayuda**:
- Usa `DELETE FROM ... WHERE fecha = ?` antes de INSERT

---

### Ejercicio 3: Calcular Tiempo de Ejecución
**Dificultad**: ⭐ Fácil

**Contexto**:
**TechMetrics** necesita saber cuánto tarda su pipeline.

**Tu tarea**:
Completa el siguiente código para medir el tiempo de ejecución:

```python
import time
import pandas as pd

def pipeline_con_metricas(archivo: str):
    inicio = # ❓ ¿Qué va aquí?

    # Procesar datos
    datos = pd.read_csv(archivo)
    datos['total'] = datos['cantidad'] * datos['precio']

    fin = # ❓ ¿Qué va aquí?
    tiempo = # ❓ ¿Cómo calcular tiempo transcurrido?

    print(f"⏱️ Pipeline completado en {tiempo} segundos")
    return datos
```

**Ayuda**:
- `time.time()` devuelve el timestamp actual
- Resta `fin - inicio` para obtener tiempo transcurrido

---

### Ejercicio 4: Logging Básico
**Dificultad**: ⭐ Fácil

**Contexto**:
**LogMaster Inc** quiere añadir logging a su pipeline.

**Tu tarea**:
Añade logs INFO en cada paso:

```python
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pipeline_con_logs(archivo: str):
    # ❓ Log: "Iniciando pipeline"

    datos = pd.read_csv(archivo)
    # ❓ Log: "Extraídas {n} filas"

    datos['total'] = datos['cantidad'] * datos['precio']
    # ❓ Log: "Transformadas {n} filas"

    # ❓ Log: "Pipeline completado"

    return datos
```

**Ayuda**:
- `logger.info("Mensaje")`
- `logger.info(f"Extraídas {len(datos)} filas")`

---

### Ejercicio 5: Batch vs Streaming
**Dificultad**: ⭐ Fácil

**Contexto**:
**DecisionMaker Corp** debe elegir entre batch y streaming para estos casos:

**Casos**:
1. Reportes de ventas mensuales para el CEO
2. Detección de transacciones fraudulentas en un banco
3. Dashboard de métricas que se actualiza cada 6 horas
4. Notificaciones en tiempo real de nuevos mensajes (como WhatsApp)
5. Cálculo de nómina de empleados

**Tu tarea**:
Para cada caso, decide:
- ¿Batch o Streaming?
- ¿Por qué?

**Ayuda**:
- Batch: Cuando puedes esperar horas/días
- Streaming: Cuando necesitas respuesta inmediata (<1 minuto)

---

## Ejercicios Intermedios (⭐⭐)

### Ejercicio 6: Implementar ETL Completo
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**RetailChain** necesita un pipeline ETL que:
1. Lea `ventas_octubre.csv` y `productos.csv`
2. Combine ambas tablas (JOIN) para obtener precio de cada venta
3. Calcule el total de cada venta (cantidad × precio)
4. Guarde en SQLite

**Tu tarea**:
Implementa el pipeline completo:

```python
import pandas as pd
import sqlite3

def pipeline_etl_retail():
    # 1. Extract
    # ❓ Leer ventas_octubre.csv
    # ❓ Leer productos.csv

    # 2. Transform
    # ❓ Hacer merge entre ventas y productos (por producto_id = id)
    # ❓ Calcular total = cantidad * precio

    # 3. Load
    # ❓ Guardar en SQLite (tabla: ventas_procesadas)

    pass

# Ejecutar
pipeline_etl_retail()
```

**Ayuda**:
- `pd.merge(ventas, productos, left_on='producto_id', right_on='id')`
- `df.to_sql('tabla', conn, if_exists='replace', index=False)`

---

### Ejercicio 7: Pipeline Parametrizado por Fecha
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**DailyData Inc** necesita un pipeline que procese ventas de UNA fecha específica.

**Tu tarea**:
Completa el pipeline para que sea parametrizado:

```python
def pipeline_por_fecha(fecha: str):
    """
    Procesa ventas de una fecha específica.

    Args:
        fecha: Fecha a procesar (formato: YYYY-MM-DD)
    """
    # 1. Leer TODAS las ventas
    ventas = pd.read_csv("ventas_octubre.csv")

    # 2. Filtrar solo la fecha especificada
    # ❓ ventas_fecha = ...

    # 3. Si no hay datos, imprimir advertencia y salir
    # ❓ if len(ventas_fecha) == 0: ...

    # 4. Calcular total
    # ❓ ventas_fecha['total'] = ...

    # 5. Guardar en DB (idempotente)
    conn = sqlite3.connect("ventas.db")
    # ❓ DELETE FROM ventas WHERE fecha = ?
    # ❓ INSERT nuevas filas
    conn.close()

    print(f"✅ Procesadas {len(ventas_fecha)} ventas para {fecha}")

# Ejecutar para diferentes fechas
pipeline_por_fecha("2025-10-01")
pipeline_por_fecha("2025-10-02")
```

**Ayuda**:
- `df[df['columna'] == valor]` para filtrar
- `if len(df) == 0: print("⚠️ Sin datos"); return`

---

### Ejercicio 8: Reprocessing con Rango de Fechas
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**BugFix Analytics** descubrió un bug y debe reprocesar del 1 al 5 de octubre.

**Tu tarea**:
Implementa una función que reprocese un rango de fechas:

```python
from datetime import datetime, timedelta

def reprocessing_rango(fecha_inicio: str, fecha_fin: str):
    """
    Reprocesa un rango de fechas.

    Args:
        fecha_inicio: Fecha inicial (YYYY-MM-DD)
        fecha_fin: Fecha final (YYYY-MM-DD)
    """
    # ❓ Convertir strings a datetime
    # ❓ Iterar desde fecha_inicio hasta fecha_fin
    # ❓ Para cada fecha, ejecutar pipeline_por_fecha()

    pass

# Ejecutar
reprocessing_rango("2025-10-01", "2025-10-05")
```

**Ayuda**:
- `datetime.strptime(fecha, "%Y-%m-%d")` convierte string a datetime
- `fecha += timedelta(days=1)` avanza un día
- `while fecha_actual <= fecha_fin:`

---

### Ejercicio 9: Implementar ELT con SQL
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**SQLMasters** quiere usar ELT: cargar datos crudos y transformar en la base de datos.

**Tu tarea**:
1. Carga `productos.csv` y `ventas_octubre.csv` en SQLite SIN transformar
2. Escribe una query SQL que calcule el total de ventas por tienda

```python
def pipeline_elt():
    # 1. Extract y Load (sin transformar)
    conn = sqlite3.connect("ventas.db")

    # ❓ Cargar productos.csv en tabla 'productos'
    # ❓ Cargar ventas_octubre.csv en tabla 'ventas'

    # 2. Transform (con SQL)
    query = """
        -- ❓ Escribe query SQL que calcule:
        -- tienda, SUM(cantidad * precio) AS total
        -- JOIN entre ventas y productos
        -- GROUP BY tienda
    """

    resultado = pd.read_sql(query, conn)
    conn.close()

    return resultado

# Ejecutar
resultado = pipeline_elt()
print(resultado)
```

**Ayuda**:
```sql
SELECT tienda, SUM(v.cantidad * p.precio) AS total
FROM ventas v
JOIN productos p ON v.producto_id = p.id
GROUP BY tienda
```

---

### Ejercicio 10: Manejo de Archivos Vacíos
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**SafePipeline Corp** quiere que su pipeline maneje archivos vacíos sin fallar.

**Tu tarea**:
Añade validación para archivos vacíos:

```python
def pipeline_seguro(archivo: str):
    # 1. Verificar que el archivo existe
    # ❓ if not Path(archivo).exists(): raise FileNotFoundError(...)

    # 2. Leer archivo
    datos = pd.read_csv(archivo)

    # 3. Verificar que NO esté vacío
    # ❓ if len(datos) == 0: logger.warning(...); return

    # 4. Procesar normalmente
    datos['total'] = datos['cantidad'] * datos['precio']
    return datos
```

**Ayuda**:
- `from pathlib import Path`
- `if not Path(archivo).exists():`
- `if len(datos) == 0:`

---

## Ejercicios Avanzados (⭐⭐⭐)

### Ejercicio 11: Pipeline con Reintentos
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**ReliableSystems** necesita un pipeline que reintente automáticamente si falla.

**Tu tarea**:
Implementa un decorador que añada reintentos a cualquier función:

```python
import time
from functools import wraps

def retry(max_intentos=3, espera_segundos=2):
    """
    Decorador que añade reintentos a una función.

    Args:
        max_intentos: Número máximo de intentos
        espera_segundos: Segundos entre intentos
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ❓ Implementar lógica de reintentos
            # ❓ for intento in range(1, max_intentos + 1):
            # ❓     try: ejecutar func
            # ❓     except: esperar y reintentar
            # ❓ Si todos fallan: raise última excepción
            pass
        return wrapper
    return decorador


# Uso
@retry(max_intentos=3, espera_segundos=1)
def funcion_que_puede_fallar():
    import random
    if random.random() < 0.7:  # 70% de fallos
        raise ConnectionError("Error de conexión")
    return "¡Éxito!"

# Probar
resultado = funcion_que_puede_fallar()
print(resultado)
```

**Ayuda**:
```python
for intento in range(1, max_intentos + 1):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if intento == max_intentos:
            raise
        time.sleep(espera_segundos)
```

---

### Ejercicio 12: Métricas Completas de Pipeline
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**MetricsHub** necesita un pipeline que registre métricas detalladas.

**Tu tarea**:
Implementa un pipeline que retorne un diccionario con:
- `filas_extraidas`: Número de filas leídas
- `filas_filtradas`: Número de filas después de filtrar
- `filas_cargadas`: Número de filas guardadas
- `tiempo_extraccion`: Segundos
- `tiempo_transformacion`: Segundos
- `tiempo_carga`: Segundos
- `tiempo_total`: Segundos
- `estado`: "EXITOSO" o "ERROR"

```python
import time
from typing import Dict, Any

def pipeline_con_metricas(fecha: str) -> Dict[str, Any]:
    """
    Pipeline que registra métricas detalladas.
    """
    metricas = {
        'filas_extraidas': 0,
        'filas_filtradas': 0,
        'filas_cargadas': 0,
        'tiempo_extraccion': 0,
        'tiempo_transformacion': 0,
        'tiempo_carga': 0,
        'tiempo_total': 0,
        'estado': 'INICIADO'
    }

    inicio_total = time.time()

    try:
        # 1. Extract
        # ❓ Medir tiempo de extracción
        # ❓ metricas['filas_extraidas'] = len(datos)

        # 2. Transform
        # ❓ Medir tiempo de transformación
        # ❓ metricas['filas_filtradas'] = len(datos_filtrados)

        # 3. Load
        # ❓ Medir tiempo de carga
        # ❓ metricas['filas_cargadas'] = len(datos_cargados)

        metricas['estado'] = 'EXITOSO'
    except Exception as e:
        metricas['estado'] = 'ERROR'
        raise
    finally:
        metricas['tiempo_total'] = time.time() - inicio_total

    return metricas

# Ejecutar
metricas = pipeline_con_metricas("2025-10-01")
print(metricas)
```

---

### Ejercicio 13: Pipeline con Validación de Calidad
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**QualityFirst Analytics** necesita validar datos ANTES de cargarlos.

**Tu tarea**:
Implementa validaciones de calidad:
- NO debe haber valores nulos en columnas críticas
- NO debe haber duplicados (por fecha + producto_id)
- Los totales deben ser > 0

```python
def validar_datos(datos: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Valida calidad de datos.

    Returns:
        (es_valido, lista_de_errores)
    """
    errores = []

    # ❓ Validar nulos en columnas críticas
    columnas_criticas = ['fecha', 'producto_id', 'cantidad']
    # ❓ if datos[col].isnull().any(): errores.append(...)

    # ❓ Validar duplicados
    # ❓ duplicados = datos.duplicated(subset=['fecha', 'producto_id'])
    # ❓ if duplicados.sum() > 0: errores.append(...)

    # ❓ Validar totales > 0
    # ❓ if (datos['total'] <= 0).any(): errores.append(...)

    es_valido = len(errores) == 0
    return es_valido, errores


def pipeline_con_validacion(fecha: str):
    # 1. Extract y Transform
    datos = extraer_y_transformar(fecha)

    # 2. Validar
    es_valido, errores = validar_datos(datos)

    if not es_valido:
        logger.error(f"❌ Validación falló: {errores}")
        raise ValueError(f"Datos inválidos: {errores}")

    # 3. Load (solo si pasa validación)
    cargar_en_db(datos)

    logger.info("✅ Pipeline completado con datos válidos")
```

**Ayuda**:
- `df[col].isnull().any()` detecta nulos
- `df.duplicated(subset=['col1', 'col2'])` detecta duplicados
- `(df['col'] <= 0).any()` detecta valores no positivos

---

### Ejercicio 14: Lambda Architecture (Batch + Streaming)
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**HybridData Corp** necesita combinar batch (histórico) y streaming (tiempo real).

**Tu tarea**:
Diseña (pseudocódigo) una arquitectura Lambda que:
1. **Batch Layer**: Procesa ventas históricas cada noche (últimos 5 años)
2. **Streaming Layer**: Procesa ventas de hoy en tiempo real
3. **Serving Layer**: Combina ambos para dar vista completa

```python
def batch_layer():
    """
    Procesa datos históricos (últimos 5 años).
    Se ejecuta cada noche a las 3 AM.
    """
    # ❓ Pseudocódigo:
    # - Leer ventas de los últimos 5 años
    # - Calcular totales por producto (agregación)
    # - Guardar en tabla 'ventas_historicas'
    pass


def streaming_layer():
    """
    Procesa datos en tiempo real (hoy).
    Se ejecuta cada minuto.
    """
    # ❓ Pseudocódigo:
    # - Leer ventas de las últimas 24 horas
    # - Calcular totales por producto
    # - Guardar en tabla 'ventas_tiempo_real'
    pass


def serving_layer(producto_id: int) -> dict:
    """
    Combina batch y streaming para dar vista completa.

    Returns:
        {'historico': X, 'hoy': Y, 'total': X+Y}
    """
    # ❓ Pseudocódigo:
    # - Consultar ventas_historicas para producto_id
    # - Consultar ventas_tiempo_real para producto_id
    # - Sumar ambos
    # - Retornar resultado combinado
    pass
```

**Pregunta adicional**:
¿Por qué separar batch y streaming? ¿Por qué no procesar todo en streaming?

---

### Ejercicio 15: Pipeline End-to-End Completo
**Dificultad**: ⭐⭐⭐ Avanzado

**Contexto**:
**MasterPipeline Inc** necesita un pipeline de producción con TODO:
- Logging
- Métricas
- Reintentos
- Validación
- Idempotencia
- Manejo de errores

**Tu tarea**:
Integra TODO lo aprendido en un pipeline completo:

```python
import logging
import time
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def pipeline_master(fecha: str, db_path: str = "ventas.db") -> Dict[str, Any]:
    """
    Pipeline de producción con todas las mejores prácticas.

    Args:
        fecha: Fecha a procesar (YYYY-MM-DD)
        db_path: Base de datos de destino

    Returns:
        Diccionario con métricas completas
    """
    # ❓ Implementa TODO:
    # 1. Inicializar métricas
    # 2. Extract con validación de archivo
    # 3. Filter por fecha
    # 4. Validar datos (nulos, duplicados)
    # 5. Transform (calcular total)
    # 6. Load con idempotencia (DELETE + INSERT)
    # 7. Logging en cada paso
    # 8. Manejo de errores (try/except)
    # 9. Métricas finales (tiempo, filas, estado)
    # 10. Reintentos si falla (decorador @retry)

    pass


# Ejecutar
try:
    metricas = pipeline_master("2025-10-01")
    print(f"✅ Pipeline exitoso: {metricas}")
except Exception as e:
    print(f"❌ Pipeline falló: {e}")
```

**Checklist de implementación**:
- [ ] Logging en cada paso
- [ ] Métricas de tiempo y filas
- [ ] Validación de datos
- [ ] Idempotencia (DELETE + INSERT)
- [ ] Manejo de errores
- [ ] Reintentos con exponential backoff
- [ ] Estado final (EXITOSO/ERROR)

---

## Soluciones

### Solución Ejercicio 1

**Respuestas**:
1. **Propuesta A es ETL** (transforma antes de cargar: filtrado y agregaciones en Python)
   **Propuesta B es ELT** (transforma después de cargar: SQL en Snowflake)

2. **Con servidor pequeño**: Propuesta A (ETL)
   - Reduces de 1GB a 10MB antes de cargar
   - No sobrecargas PostgreSQL

3. **Con Snowflake**: Propuesta B (ELT)
   - Aprovechas el poder de cómputo de Snowflake
   - Más flexible para re-transformar

---

### Solución Ejercicio 2

```python
import sqlite3

def pipeline_idempotente(fecha: str):
    conn = sqlite3.connect("videos.db")

    # ✅ PRIMERO: Borra datos de esa fecha
    conn.execute("""
        DELETE FROM videos_vistos WHERE fecha = ?
    """, (fecha,))

    # ✅ SEGUNDO: Inserta datos nuevos
    conn.execute("""
        INSERT INTO videos_vistos (fecha, video_id, vistas)
        VALUES (?, 101, 1500)
    """, (fecha,))

    conn.commit()
    conn.close()
    print(f"✅ Pipeline idempotente ejecutado para {fecha}")

# Ejecutar 3 veces
pipeline_idempotente("2025-10-23")
pipeline_idempotente("2025-10-23")  # No duplica
pipeline_idempotente("2025-10-23")  # Sigue sin duplicar

# Verificar: Solo 1 fila
conn = sqlite3.connect("videos.db")
resultado = conn.execute(
    "SELECT COUNT(*) FROM videos_vistos WHERE fecha = '2025-10-23'"
).fetchone()
conn.close()

print(f"Número de filas: {resultado[0]}")  # Debe ser 1
```

---

### Solución Ejercicio 3

```python
import time
import pandas as pd

def pipeline_con_metricas(archivo: str):
    inicio = time.time()  # ✅ Timestamp al inicio

    # Procesar datos
    datos = pd.read_csv(archivo)
    datos['total'] = datos['cantidad'] * datos['precio']

    fin = time.time()  # ✅ Timestamp al final
    tiempo = round(fin - inicio, 2)  # ✅ Calcular diferencia

    print(f"⏱️ Pipeline completado en {tiempo} segundos")
    return datos
```

---

### Solución Ejercicio 4

```python
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pipeline_con_logs(archivo: str):
    logger.info("🚀 Iniciando pipeline")  # ✅ Log de inicio

    datos = pd.read_csv(archivo)
    logger.info(f"📂 Extraídas {len(datos)} filas")  # ✅ Log de extracción

    datos['total'] = datos['cantidad'] * datos['precio']
    logger.info(f"🔄 Transformadas {len(datos)} filas")  # ✅ Log de transformación

    logger.info("✅ Pipeline completado")  # ✅ Log de finalización

    return datos
```

---

### Solución Ejercicio 5

1. **Reportes de ventas mensuales**: **Batch** (puedes esperar 1 mes)
2. **Detección de fraude**: **Streaming** (debe ser inmediato)
3. **Dashboard cada 6 horas**: **Batch** (no necesitas tiempo real)
4. **Notificaciones WhatsApp**: **Streaming** (instantáneo)
5. **Cálculo de nómina**: **Batch** (se hace mensualmente)

---

### Solución Ejercicio 6

```python
import pandas as pd
import sqlite3

def pipeline_etl_retail():
    # 1. Extract
    ventas = pd.read_csv("ventas_octubre.csv")
    productos = pd.read_csv("productos.csv")
    print(f"📂 Extraídas {len(ventas)} ventas y {len(productos)} productos")

    # 2. Transform
    # Merge (JOIN) por producto_id = id
    datos = pd.merge(ventas, productos, left_on='producto_id', right_on='id')

    # Calcular total
    datos['total'] = (datos['cantidad'] * datos['precio']).round(2)

    print(f"🔄 Transformadas {len(datos)} filas")

    # 3. Load
    conn = sqlite3.connect("retail.db")
    datos.to_sql('ventas_procesadas', conn, if_exists='replace', index=False)
    conn.close()

    print(f"💾 Cargadas {len(datos)} filas")
    print("✅ Pipeline ETL completado")

# Ejecutar
pipeline_etl_retail()
```

---

### Solución Ejercicio 7

```python
import pandas as pd
import sqlite3

def pipeline_por_fecha(fecha: str):
    # 1. Leer TODAS las ventas
    ventas = pd.read_csv("ventas_octubre.csv")

    # 2. Filtrar solo la fecha especificada
    ventas_fecha = ventas[ventas['fecha'] == fecha].copy()

    # 3. Si no hay datos, salir
    if len(ventas_fecha) == 0:
        print(f"⚠️ No hay ventas para {fecha}")
        return

    # 4. Calcular total (asumiendo que tenemos precio en el CSV)
    ventas_fecha['total'] = ventas_fecha['cantidad'] * 100  # Ejemplo

    # 5. Guardar en DB (idempotente)
    conn = sqlite3.connect("ventas.db")
    try:
        # DELETE para idempotencia
        conn.execute("DELETE FROM ventas WHERE fecha = ?", (fecha,))

        # INSERT nuevas filas
        ventas_fecha.to_sql('ventas', conn, if_exists='append', index=False)
    finally:
        conn.close()

    print(f"✅ Procesadas {len(ventas_fecha)} ventas para {fecha}")

# Ejecutar
pipeline_por_fecha("2025-10-01")
pipeline_por_fecha("2025-10-02")
```

---

### Solución Ejercicio 8

```python
from datetime import datetime, timedelta

def reprocessing_rango(fecha_inicio: str, fecha_fin: str):
    # Convertir strings a datetime
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

    print(f"🔄 Reprocessing de {fecha_inicio} a {fecha_fin}...")

    fecha_actual = inicio
    while fecha_actual <= fin:
        fecha_str = fecha_actual.strftime("%Y-%m-%d")
        pipeline_por_fecha(fecha_str)
        fecha_actual += timedelta(days=1)

    print("✅ Reprocessing completado!")

# Ejecutar
reprocessing_rango("2025-10-01", "2025-10-05")
```

---

### Solución Ejercicio 9

```python
import pandas as pd
import sqlite3

def pipeline_elt():
    conn = sqlite3.connect("ventas.db")

    # 1. Extract y Load (sin transformar)
    productos = pd.read_csv("productos.csv")
    ventas = pd.read_csv("ventas_octubre.csv")

    productos.to_sql('productos', conn, if_exists='replace', index=False)
    ventas.to_sql('ventas', conn, if_exists='replace', index=False)

    print("💾 Datos crudos cargados")

    # 2. Transform (con SQL en la DB)
    query = """
        SELECT
            v.tienda,
            SUM(v.cantidad * p.precio) AS total
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        GROUP BY v.tienda
        ORDER BY total DESC
    """

    resultado = pd.read_sql(query, conn)
    conn.close()

    print("🔄 Transformación SQL completada")
    return resultado

# Ejecutar
resultado = pipeline_elt()
print(resultado)
```

**Output**:
```
    tienda    total
0   Madrid  2149.95
1  Valencia  399.99
2   Sevilla  239.98
```

---

### Solución Ejercicio 10

```python
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pipeline_seguro(archivo: str):
    # 1. Verificar que el archivo existe
    if not Path(archivo).exists():
        raise FileNotFoundError(f"❌ Archivo {archivo} no encontrado")

    # 2. Leer archivo
    datos = pd.read_csv(archivo)

    # 3. Verificar que NO esté vacío
    if len(datos) == 0:
        logger.warning(f"⚠️ Archivo {archivo} está vacío, saltando procesamiento")
        return None

    # 4. Procesar normalmente
    datos['total'] = datos['cantidad'] * datos['precio']
    logger.info(f"✅ Procesadas {len(datos)} filas")

    return datos

# Probar con archivo vacío
# Crear archivo vacío para testing
with open("vacio.csv", "w") as f:
    f.write("fecha,producto,cantidad,precio\n")  # Solo header

resultado = pipeline_seguro("vacio.csv")
print(f"Resultado: {resultado}")  # None
```

---

### Solución Ejercicio 11

```python
import time
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry(max_intentos=3, espera_segundos=2):
    """
    Decorador que añade reintentos a una función.
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for intento in range(1, max_intentos + 1):
                try:
                    logger.info(f"🔄 Intento {intento}/{max_intentos}")
                    resultado = func(*args, **kwargs)
                    logger.info(f"✅ Éxito en intento {intento}")
                    return resultado

                except Exception as e:
                    logger.warning(f"⚠️ Intento {intento} falló: {e}")

                    if intento == max_intentos:
                        logger.error("❌ Todos los intentos fallaron")
                        raise

                    logger.info(f"⏳ Esperando {espera_segundos}s...")
                    time.sleep(espera_segundos)

        return wrapper
    return decorador


# Uso
@retry(max_intentos=3, espera_segundos=1)
def funcion_que_puede_fallar():
    import random
    if random.random() < 0.7:  # 70% de fallos
        raise ConnectionError("Error de conexión")
    return "¡Éxito!"

# Probar
resultado = funcion_que_puede_fallar()
print(resultado)
```

---

### Solución Ejercicio 12

```python
import time
import pandas as pd
import sqlite3
from typing import Dict, Any

def pipeline_con_metricas(fecha: str) -> Dict[str, Any]:
    metricas = {
        'filas_extraidas': 0,
        'filas_filtradas': 0,
        'filas_cargadas': 0,
        'tiempo_extraccion': 0,
        'tiempo_transformacion': 0,
        'tiempo_carga': 0,
        'tiempo_total': 0,
        'estado': 'INICIADO'
    }

    inicio_total = time.time()

    try:
        # 1. Extract
        inicio_extract = time.time()
        datos = pd.read_csv("ventas_octubre.csv")
        metricas['filas_extraidas'] = len(datos)
        metricas['tiempo_extraccion'] = round(time.time() - inicio_extract, 3)

        # 2. Transform
        inicio_transform = time.time()
        datos_filtrados = datos[datos['fecha'] == fecha].copy()
        datos_filtrados['total'] = datos_filtrados['cantidad'] * 100
        metricas['filas_filtradas'] = len(datos_filtrados)
        metricas['tiempo_transformacion'] = round(time.time() - inicio_transform, 3)

        # 3. Load
        inicio_load = time.time()
        conn = sqlite3.connect("ventas.db")
        conn.execute("DELETE FROM ventas WHERE fecha = ?", (fecha,))
        datos_filtrados.to_sql('ventas', conn, if_exists='append', index=False)
        conn.close()
        metricas['filas_cargadas'] = len(datos_filtrados)
        metricas['tiempo_carga'] = round(time.time() - inicio_load, 3)

        metricas['estado'] = 'EXITOSO'

    except Exception as e:
        metricas['estado'] = 'ERROR'
        raise
    finally:
        metricas['tiempo_total'] = round(time.time() - inicio_total, 3)

    return metricas

# Ejecutar
metricas = pipeline_con_metricas("2025-10-01")
print(metricas)
```

---

### Solución Ejercicio 13

```python
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validar_datos(datos: pd.DataFrame) -> tuple[bool, list[str]]:
    errores = []

    # Validar nulos en columnas críticas
    columnas_criticas = ['fecha', 'producto_id', 'cantidad']
    for col in columnas_criticas:
        if datos[col].isnull().any():
            nulos = datos[col].isnull().sum()
            errores.append(f"Columna '{col}' tiene {nulos} valores nulos")

    # Validar duplicados
    duplicados = datos.duplicated(subset=['fecha', 'producto_id'])
    if duplicados.sum() > 0:
        errores.append(f"Hay {duplicados.sum()} filas duplicadas")

    # Validar totales > 0
    if 'total' in datos.columns:
        if (datos['total'] <= 0).any():
            negativos = (datos['total'] <= 0).sum()
            errores.append(f"Hay {negativos} totales <= 0")

    es_valido = len(errores) == 0
    return es_valido, errores


def pipeline_con_validacion(fecha: str):
    # 1. Extract y Transform
    datos = pd.read_csv("ventas_octubre.csv")
    datos = datos[datos['fecha'] == fecha].copy()
    datos['total'] = datos['cantidad'] * 100

    # 2. Validar
    es_valido, errores = validar_datos(datos)

    if not es_valido:
        logger.error(f"❌ Validación falló: {errores}")
        raise ValueError(f"Datos inválidos: {errores}")

    # 3. Load (solo si pasa validación)
    logger.info("✅ Validación exitosa, cargando datos...")
    # ... cargar en DB ...

    logger.info("✅ Pipeline completado con datos válidos")

# Ejecutar
try:
    pipeline_con_validacion("2025-10-01")
except ValueError as e:
    print(f"Pipeline abortado: {e}")
```

---

### Solución Ejercicio 14

```python
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

def batch_layer():
    """
    Procesa datos históricos (últimos 5 años).
    """
    print("🌙 Batch Layer: Procesando datos históricos...")

    # Pseudocódigo:
    # 1. Leer ventas de los últimos 5 años
    fecha_inicio = (datetime.now() - timedelta(days=5*365)).strftime("%Y-%m-%d")
    fecha_fin = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # 2. Agregar por producto
    conn = sqlite3.connect("ventas.db")
    historico = pd.read_sql(f"""
        SELECT producto_id, SUM(total) AS total_historico
        FROM ventas
        WHERE fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
        GROUP BY producto_id
    """, conn)

    # 3. Guardar en tabla 'ventas_historicas'
    historico.to_sql('ventas_historicas', conn, if_exists='replace', index=False)
    conn.close()

    print(f"✅ Procesados datos históricos de {fecha_inicio} a {fecha_fin}")


def streaming_layer():
    """
    Procesa datos en tiempo real (hoy).
    """
    print("⚡ Streaming Layer: Procesando datos de hoy...")

    # Pseudocódigo:
    # 1. Leer ventas de hoy
    hoy = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("ventas.db")
    tiempo_real = pd.read_sql(f"""
        SELECT producto_id, SUM(total) AS total_hoy
        FROM ventas
        WHERE fecha = '{hoy}'
        GROUP BY producto_id
    """, conn)

    # 2. Guardar en tabla 'ventas_tiempo_real'
    tiempo_real.to_sql('ventas_tiempo_real', conn, if_exists='replace', index=False)
    conn.close()

    print(f"✅ Procesados datos de {hoy}")


def serving_layer(producto_id: int) -> dict:
    """
    Combina batch y streaming.
    """
    conn = sqlite3.connect("ventas.db")

    # Consultar histórico
    historico = pd.read_sql(f"""
        SELECT total_historico
        FROM ventas_historicas
        WHERE producto_id = {producto_id}
    """, conn)

    # Consultar tiempo real
    tiempo_real = pd.read_sql(f"""
        SELECT total_hoy
        FROM ventas_tiempo_real
        WHERE producto_id = {producto_id}
    """, conn)

    conn.close()

    # Combinar
    total_historico = historico['total_historico'].iloc[0] if not historico.empty else 0
    total_hoy = tiempo_real['total_hoy'].iloc[0] if not tiempo_real.empty else 0

    return {
        'historico': total_historico,
        'hoy': total_hoy,
        'total': total_historico + total_hoy
    }

# Ejecutar
batch_layer()       # Se ejecuta cada noche
streaming_layer()   # Se ejecuta cada minuto
resultado = serving_layer(producto_id=1)
print(resultado)
```

**Respuesta a la pregunta**:
¿Por qué separar batch y streaming?
- **Eficiencia**: Procesar 5 años de datos en streaming sería muy lento y costoso
- **Latencia**: Streaming para lo urgente, batch para lo histórico
- **Costo**: Batch usa recursos solo de noche, streaming 24/7

---

### Solución Ejercicio 15

**(Ver combinación de soluciones anteriores para un pipeline completo)**

```python
import logging
import time
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, Any
from functools import wraps

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Decorador de reintentos
def retry(max_intentos=3):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for intento in range(1, max_intentos + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Intento {intento} falló: {e}")
                    if intento == max_intentos:
                        raise
                    time.sleep(2 ** intento)
        return wrapper
    return decorador


# Validación
def validar_datos(datos: pd.DataFrame) -> tuple[bool, list[str]]:
    errores = []

    if datos['fecha'].isnull().any():
        errores.append("Hay fechas nulas")

    if datos.duplicated(subset=['fecha', 'producto_id']).sum() > 0:
        errores.append("Hay duplicados")

    if (datos['total'] <= 0).any():
        errores.append("Hay totales <= 0")

    return len(errores) == 0, errores


# Pipeline master
@retry(max_intentos=3)
def pipeline_master(fecha: str, db_path: str = "ventas.db") -> Dict[str, Any]:
    logger.info(f"🚀 Iniciando pipeline para {fecha}")

    metricas = {
        'fecha': fecha,
        'filas_extraidas': 0,
        'filas_procesadas': 0,
        'filas_cargadas': 0,
        'tiempo_total': 0,
        'estado': 'INICIADO'
    }

    inicio = time.time()

    try:
        # 1. Extract
        archivo = "ventas_octubre.csv"
        if not Path(archivo).exists():
            raise FileNotFoundError(f"Archivo {archivo} no encontrado")

        datos = pd.read_csv(archivo)
        metricas['filas_extraidas'] = len(datos)
        logger.info(f"📂 Extraídas {len(datos)} filas")

        # 2. Filter
        datos_fecha = datos[datos['fecha'] == fecha].copy()
        if len(datos_fecha) == 0:
            logger.warning(f"⚠️ No hay datos para {fecha}")
            metricas['estado'] = 'SIN_DATOS'
            return metricas

        # 3. Transform
        datos_fecha['total'] = (datos_fecha['cantidad'] * 100).round(2)
        metricas['filas_procesadas'] = len(datos_fecha)
        logger.info(f"🔄 Transformadas {len(datos_fecha)} filas")

        # 4. Validate
        es_valido, errores = validar_datos(datos_fecha)
        if not es_valido:
            raise ValueError(f"Validación falló: {errores}")
        logger.info("✅ Validación exitosa")

        # 5. Load (idempotente)
        conn = sqlite3.connect(db_path)
        try:
            conn.execute("DELETE FROM ventas WHERE fecha = ?", (fecha,))
            datos_fecha.to_sql('ventas', conn, if_exists='append', index=False)
            metricas['filas_cargadas'] = len(datos_fecha)
        finally:
            conn.close()

        logger.info(f"💾 Cargadas {metricas['filas_cargadas']} filas")

        metricas['estado'] = 'EXITOSO'

    except Exception as e:
        logger.error(f"❌ Error: {e}")
        metricas['estado'] = 'ERROR'
        raise
    finally:
        metricas['tiempo_total'] = round(time.time() - inicio, 2)
        logger.info(f"📊 Métricas: {metricas}")

    return metricas


# Ejecutar
try:
    metricas = pipeline_master("2025-10-01")
    print(f"✅ Pipeline exitoso: {metricas}")
except Exception as e:
    print(f"❌ Pipeline falló: {e}")
```

---

## Tabla de Autoevaluación

| Ejercicio                 | Completado | Correcto | Notas |
| ------------------------- | ---------- | -------- | ----- |
| 1. ETL vs ELT             | [ ]        | [ ]      |       |
| 2. Idempotencia           | [ ]        | [ ]      |       |
| 3. Tiempo de ejecución    | [ ]        | [ ]      |       |
| 4. Logging básico         | [ ]        | [ ]      |       |
| 5. Batch vs Streaming     | [ ]        | [ ]      |       |
| 6. ETL completo           | [ ]        | [ ]      |       |
| 7. Pipeline por fecha     | [ ]        | [ ]      |       |
| 8. Reprocessing           | [ ]        | [ ]      |       |
| 9. ELT con SQL            | [ ]        | [ ]      |       |
| 10. Archivos vacíos       | [ ]        | [ ]      |       |
| 11. Reintentos            | [ ]        | [ ]      |       |
| 12. Métricas completas    | [ ]        | [ ]      |       |
| 13. Validación de calidad | [ ]        | [ ]      |       |
| 14. Lambda Architecture   | [ ]        | [ ]      |       |
| 15. Pipeline end-to-end   | [ ]        | [ ]      |       |

---

## Consejos para Mejorar

### Si completaste 0-5 ejercicios (⭐):
- ✅ Revisa `01-TEORIA.md` de nuevo
- ✅ Estudia los ejemplos en `02-EJEMPLOS.md`
- ✅ Practica los ejercicios básicos primero

### Si completaste 6-10 ejercicios (⭐⭐):
- ✅ Buen progreso! Sigue practicando
- ✅ Intenta los ejercicios intermedios
- ✅ Experimenta modificando el código

### Si completaste 11-15 ejercicios (⭐⭐⭐):
- ✅ ¡Excelente trabajo!
- ✅ Estás listo para el proyecto práctico
- ✅ Continúa con `04-proyecto-practico/`

---

## Próximos Pasos

1. **Revisa las soluciones** y compáralas con tu código
2. **Experimenta**: Modifica el código, prueba cosas nuevas
3. **Continúa con el Proyecto Práctico**: `04-proyecto-practico/`
4. **Practica TDD**: Escribe tests antes del código

---

**¡Felicidades por completar los ejercicios!** Ahora tienes las habilidades para diseñar pipelines robustos y escalables.

**Última actualización**: 2025-10-23
---

## 🧭 Navegación

⬅️ **Anterior**: [02 Ejemplos](02-EJEMPLOS.md) | ➡️ **Siguiente**: [Proyecto Práctico](04-proyecto-practico/README.md)
