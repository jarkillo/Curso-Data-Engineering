# Tema 1: Conceptos de ETL/ELT - Fundamentos de Pipelines de Datos

**Tiempo de lectura**: 30-45 minutos
**Nivel**: Intermedio
**Prerrequisitos**: Módulo 1 (Python básico) y Módulo 2 (SQL básico)

---

## Introducción: ¿Por qué importan los Pipelines de Datos?

Imagina que trabajas en una empresa de e-commerce como Amazon. Cada segundo:
- Miles de usuarios navegan por productos
- Cientos realizan compras
- Los vendedores actualizan precios e inventarios
- Los sistemas de recomendación generan sugerencias

¿Cómo conviertes todo ese caos de datos en **información útil** para tomar decisiones? La respuesta: **pipelines de datos**.

Un **pipeline de datos** es como una **línea de producción en una fábrica**:
- **Entrada (materias primas)**: Datos crudos de diferentes fuentes
- **Proceso (transformación)**: Limpieza, validación, combinación
- **Salida (producto final)**: Datos listos para análisis o aplicaciones

En este tema aprenderás los conceptos fundamentales que todo Data Engineer debe dominar para construir pipelines robustos y escalables.

---

## 🎯 Objetivos de Aprendizaje

Al completar este tema, serás capaz de:

1. Explicar qué es un pipeline de datos y por qué es fundamental
2. Diferenciar entre ETL y ELT y cuándo usar cada uno
3. Comprender arquitecturas de pipelines (batch vs streaming)
4. Diseñar pipelines idempotentes que se puedan reprocesar
5. Identificar componentes clave de un pipeline de producción

---

## 1. ¿Qué es un Pipeline de Datos?

### Definición Simple

Un **pipeline de datos** es una serie de pasos automatizados que mueven y transforman datos desde una o más fuentes hasta un destino final.

### Analogía: El Ciclo del Agua

Piensa en el ciclo del agua:
1. **Evaporación (Extract)**: El agua se extrae de océanos, ríos, lagos
2. **Formación de nubes (Transform)**: El vapor se condensa y se purifica
3. **Precipitación (Load)**: El agua cae limpia y lista para consumir

Un pipeline de datos funciona igual:
1. **Extract**: Extraer datos de múltiples fuentes
2. **Transform**: Limpiar, validar, combinar, enriquecer
3. **Load**: Cargar en el destino (base de datos, data warehouse, data lake)

### En el Mundo Real

**Ejemplo**: Pipeline de análisis de ventas
```
1. Extract: Leer datos de ventas del sistema de punto de venta (POS)
2. Transform:
   - Convertir monedas a una sola (USD)
   - Calcular totales por producto
   - Identificar productos más vendidos
3. Load: Guardar resultados en PostgreSQL para dashboards
```

### Por Qué es Importante en Data Engineering

Como Data Engineer, tu trabajo NO es solo escribir código que funcione una vez. Tu trabajo es:
- ✅ Automatizar procesos que se ejecutan **miles de veces**
- ✅ Manejar **millones de registros** sin fallar
- ✅ Garantizar que los datos lleguen **a tiempo y correctos**
- ✅ Recuperarse de **errores sin intervención manual**

Un pipeline bien diseñado es la diferencia entre:
- ❌ Trabajar 12 horas corrigiendo errores manualmente
- ✅ Tomar café mientras el sistema se repara solo

---

## 2. ETL vs ELT: La Gran Diferencia

### ETL (Extract, Transform, Load)

**Definición**: Transformar los datos **antes** de cargarlos en el destino.

**Analogía**: Restaurante con cocina visible

Imagina un restaurante donde:
1. **Extract**: El chef compra ingredientes crudos del mercado
2. **Transform**: Cocina, mezcla, sazona en la cocina (antes de servir)
3. **Load**: Sirve el plato **ya preparado** al cliente

**Flujo**:
```
Fuente → Extract → Transform → Load → Destino
         (datos)   (proceso)   (ya listo)
```

**Ejemplo Real**:
```
1. Extract: Leer CSV de ventas (5GB)
2. Transform:
   - Filtrar solo ventas del último mes
   - Calcular total_con_impuesto
   - Agrupar por producto
3. Load: Insertar 100,000 filas resumidas en PostgreSQL
```

**Ventajas de ETL**:
- ✅ Cargamos **menos datos** (solo lo necesario)
- ✅ El destino recibe datos **ya procesados**
- ✅ Útil cuando el destino tiene **capacidad limitada**

**Desventajas de ETL**:
- ❌ Necesitas **servidor potente para transformar**
- ❌ Si quieres cambiar la transformación, debes **reprocesar desde cero**
- ❌ Más lento si tienes muchas transformaciones complejas

---

### ELT (Extract, Load, Transform)

**Definición**: Cargar los datos **primero** y transformar **después** en el destino.

**Analogía**: Buffet de comida

Imagina un buffet donde:
1. **Extract**: Traer ingredientes del mercado
2. **Load**: Poner TODO en la mesa (sin cocinar)
3. **Transform**: El cliente elige y mezcla lo que quiere

**Flujo**:
```
Fuente → Extract → Load → Transform → Resultado
         (datos)   (todo)   (en destino)
```

**Ejemplo Real**:
```
1. Extract: Leer CSV de ventas (5GB)
2. Load: Insertar **todas** las 10 millones de filas en Snowflake
3. Transform: Ejecutar SQL dentro de Snowflake para calcular reportes
```

**Ventajas de ELT**:
- ✅ Aprovechas la **potencia del data warehouse** (Snowflake, BigQuery)
- ✅ Puedes **re-transformar sin extraer de nuevo**
- ✅ Más **flexible**: cambias la transformación sin tocar la extracción
- ✅ **Más rápido** con grandes volúmenes (el DWH tiene GPUs, clusters)

**Desventajas de ELT**:
- ❌ Cargas **todos los datos** (incluso los que no usarás)
- ❌ Necesitas un destino **potente** (Snowflake, BigQuery, Redshift)
- ❌ Costos de almacenamiento pueden ser **altos**

---

### ¿Cuándo Usar ETL vs ELT?

| Situación                                      | Recomendación | Por Qué                                |
| ---------------------------------------------- | ------------- | -------------------------------------- |
| Tienes **Snowflake/BigQuery/Redshift**         | **ELT**       | Aprovecha su poder de cómputo          |
| Destino es **PostgreSQL/MySQL pequeño**        | **ETL**       | No lo sobrecargues con datos crudos    |
| Volumen < 1GB diario                           | **ETL**       | No necesitas infraestructura compleja  |
| Volumen > 100GB diario                         | **ELT**       | ETL sería muy lento                    |
| Necesitas **flexibilidad** para re-transformar | **ELT**       | No dependes de re-extraer              |
| Tienes **servidor potente** para transformar   | **ETL**       | Usa lo que tienes                      |
| Datos altamente **sensibles** (GDPR)           | **ETL**       | Filtra datos sensibles antes de cargar |

---

### Ejemplo Comparativo

**Escenario**: Analizar ventas de una tienda online

**Con ETL**:
```python
# 1. Extract
ventas = leer_csv("ventas_2025.csv")  # 5GB, 10M filas

# 2. Transform (antes de cargar)
ventas_filtradas = ventas[ventas['fecha'] >= '2025-10-01']  # Solo octubre
ventas_con_impuesto = calcular_impuesto(ventas_filtradas)
resumen = agrupar_por_producto(ventas_con_impuesto)

# 3. Load (solo 100K filas resumidas)
guardar_en_postgres(resumen)  # 100K filas, 50MB
```

**Con ELT**:
```python
# 1. Extract
ventas = leer_csv("ventas_2025.csv")  # 5GB, 10M filas

# 2. Load (TODO)
guardar_en_snowflake(ventas)  # 10M filas, 5GB

# 3. Transform (dentro de Snowflake con SQL)
ejecutar_sql("""
    SELECT
        producto,
        SUM(precio * 1.21) AS total_con_impuesto
    FROM ventas
    WHERE fecha >= '2025-10-01'
    GROUP BY producto
""")
```

**Resultado**: Mismo dato final, pero el proceso es diferente.

---

## 3. Arquitecturas de Pipelines: Batch vs Streaming

### Batch Processing (Por Lotes)

**Definición**: Procesar datos en **bloques** o **lotes** a intervalos regulares.

**Analogía**: Autobús público

Un autobús:
- Espera a que **varios pasajeros** suban
- Parte cada **30 minutos** (intervalo fijo)
- Lleva a **todos juntos** al destino

**Ejemplo**:
```python
# Pipeline que se ejecuta cada 24 horas
cada_dia_a_las_3am():
    ventas_del_dia = extraer_ventas()
    ventas_limpias = transformar(ventas_del_dia)
    cargar_en_warehouse(ventas_limpias)
```

**Casos de Uso**:
- 📊 Reportes diarios de ventas
- 📧 Envío de newsletters semanales
- 💰 Cálculo de nómina mensual
- 📈 Análisis de datos históricos

**Ventajas**:
- ✅ Más **simple** de implementar
- ✅ Usa recursos de forma **eficiente** (procesa mucho de golpe)
- ✅ Más **económico** (no necesitas infraestructura 24/7)

**Desventajas**:
- ❌ **Latencia alta**: Los datos llegan con retraso
- ❌ No sirve para **decisiones en tiempo real**

---

### Streaming Processing (En Tiempo Real)

**Definición**: Procesar datos **uno por uno** o en **micro-lotes** a medida que llegan.

**Analogía**: Taxi

Un taxi:
- Sale **inmediatamente** cuando llega un pasajero
- No espera a nadie más
- Entrega **al instante**

**Ejemplo**:
```python
# Pipeline que procesa cada evento al instante
while True:
    evento = esperar_evento()  # Click en la web, compra, etc.
    evento_procesado = transformar(evento)
    guardar_en_tiempo_real(evento_procesado)
```

**Casos de Uso**:
- 🚨 Detección de fraude en transacciones bancarias
- 📍 Tracking de ubicación en tiempo real (Uber, Glovo)
- 💬 Chat en vivo y notificaciones
- 📺 Streaming de video (Netflix, YouTube)
- 🎮 Videojuegos online

**Ventajas**:
- ✅ **Latencia baja**: Datos disponibles en segundos
- ✅ Permite **decisiones inmediatas**
- ✅ Mejor experiencia de usuario

**Desventajas**:
- ❌ Más **complejo** de implementar (Kafka, Spark Streaming)
- ❌ Más **costoso** (infraestructura debe estar siempre activa)
- ❌ Más difícil de **debuggear**

---

### ¿Cuándo Usar Batch vs Streaming?

| Pregunta                                              | Batch | Streaming |
| ----------------------------------------------------- | ----- | --------- |
| ¿Los datos deben estar disponibles en **< 1 minuto**? | ❌     | ✅         |
| ¿Puedes esperar **horas o días**?                     | ✅     | ❌         |
| ¿Tienes presupuesto **limitado**?                     | ✅     | ❌         |
| ¿Necesitas procesar **grandes volúmenes** (TB)?       | ✅     | ⚠️         |
| ¿Es crítico para el negocio (fraude, seguridad)?      | ❌     | ✅         |

**Regla general**:
- **Batch**: Reportes, análisis históricos, dashboards que se actualizan cada X horas
- **Streaming**: Detección de fraude, notificaciones, tracking en vivo

---

### Arquitectura Híbrida (Lambda Architecture)

En la práctica, muchas empresas usan **ambos**:

```
                        ┌──────────────┐
                        │   Fuente     │
                        │  de Datos    │
                        └───────┬──────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
            ┌───────▼────────┐    ┌────────▼────────┐
            │  Batch Layer   │    │ Streaming Layer │
            │  (histórico)   │    │  (tiempo real)  │
            └───────┬────────┘    └────────┬────────┘
                    │                       │
                    └───────────┬───────────┘
                                │
                        ┌───────▼──────┐
                        │   Serving    │
                        │    Layer     │
                        └──────────────┘
```

**Ejemplo**:
- **Batch**: Procesa ventas históricas cada noche (últimos 5 años)
- **Streaming**: Procesa ventas de hoy en tiempo real (últimas 24 horas)
- **Serving**: Combina ambos para dar vista completa

---

## 4. Idempotencia: La Clave de Pipelines Robustos

### ¿Qué es la Idempotencia?

**Definición**: Una operación es **idempotente** si ejecutarla **múltiples veces** produce el **mismo resultado** que ejecutarla **una vez**.

**Analogía**: Interruptor de luz

Cuando enciendes la luz:
- Primera vez: ✅ Luz encendida
- Segunda vez: ✅ Luz sigue encendida (no se rompe)
- Tercera vez: ✅ Luz sigue encendida

No importa cuántas veces presiones el interruptor estando encendido, el resultado es el mismo: **luz encendida**.

### En Pipelines de Datos

**Pipeline NO Idempotente** (❌ MAL):
```python
def procesar_ventas(fecha):
    ventas = extraer_ventas(fecha)
    for venta in ventas:
        # ❌ Inserta SIEMPRE (duplica si vuelves a ejecutar)
        insertar_en_db(venta)
```

**Problema**: Si ejecutas este pipeline 2 veces, tendrás **datos duplicados**.

```sql
-- Primera ejecución: 100 filas
-- Segunda ejecución: 200 filas (100 duplicadas!)
SELECT COUNT(*) FROM ventas;  -- 200 ❌
```

**Pipeline Idempotente** (✅ BIEN):
```python
def procesar_ventas(fecha):
    ventas = extraer_ventas(fecha)

    # ✅ Borra datos de esa fecha primero
    eliminar_ventas_de_fecha(fecha)

    # ✅ Inserta datos frescos
    for venta in ventas:
        insertar_en_db(venta)
```

**Resultado**: Si ejecutas este pipeline 2 veces, tendrás **100 filas** (sin duplicados).

```sql
-- Primera ejecución: 100 filas
-- Segunda ejecución: 100 filas (mismo resultado!)
SELECT COUNT(*) FROM ventas;  -- 100 ✅
```

---

### Estrategias para Lograr Idempotencia

#### 1. **DELETE + INSERT** (Recomendado para batch pequeño)

```python
# 1. Borra datos del período
DELETE FROM ventas WHERE fecha = '2025-10-23'

# 2. Inserta datos frescos
INSERT INTO ventas VALUES (...)
```

**Ventajas**: Simple y efectivo
**Desventajas**: No eficiente con grandes volúmenes

#### 2. **TRUNCATE + INSERT** (Para tablas temporales)

```python
# 1. Vacía la tabla completamente
TRUNCATE TABLE ventas_temp

# 2. Inserta datos
INSERT INTO ventas_temp VALUES (...)
```

**Ventajas**: Muy rápido
**Desventajas**: Pierdes TODO (solo para tablas staging)

#### 3. **MERGE / UPSERT** (Recomendado para producción)

```python
# Si existe: actualiza. Si no existe: inserta
MERGE INTO ventas AS target
USING ventas_nuevas AS source
ON target.id = source.id
WHEN MATCHED THEN
    UPDATE SET precio = source.precio
WHEN NOT MATCHED THEN
    INSERT VALUES (source.id, source.precio)
```

**Ventajas**: Maneja inserciones y actualizaciones
**Desventajas**: Más complejo de implementar

#### 4. **Archivos con Timestamp** (Para data lakes)

```python
# Nombra archivos con timestamp único
archivo = f"ventas_{fecha}_{timestamp}.parquet"

# Si reprocesas, creas un archivo nuevo
# Luego puedes deduplicar leyendo todos
```

**Ventajas**: Historial completo de ejecuciones
**Desventajas**: Necesitas lógica de deduplicación al leer

---

### Por Qué es Crítica la Idempotencia

Imagina este escenario:

```
3:00 AM: Pipeline de ventas se ejecuta
3:30 AM: Falla por error de red (50% procesado)
3:35 AM: Sistema de alertas notifica al ingeniero
3:40 AM: Ingeniero re-ejecuta el pipeline

¿Qué pasa?
```

**Sin idempotencia** (❌):
- Primera ejecución: 50% de datos insertados
- Re-ejecución: 50% duplicados + 50% nuevos
- Resultado: **Datos inconsistentes, reportes incorrectos**
- Consecuencia: El CEO toma decisiones con datos **ERRÓNEOS**

**Con idempotencia** (✅):
- Primera ejecución: 50% de datos insertados (falla)
- Re-ejecución: Borra TODO y procesa 100% de nuevo
- Resultado: **Datos correctos y consistentes**
- Consecuencia: El CEO puede confiar en los reportes

**Regla de Oro**: Siempre diseña tus pipelines para que puedan **reprocesarse** sin causar problemas.

---

## 5. Componentes de un Pipeline de Producción

Un pipeline profesional NO es solo "extract, transform, load". Incluye:

### 1. **Extracción (Extract)**
- Leer datos de múltiples fuentes
- Manejar diferentes formatos (CSV, JSON, API, DB)
- **Retry logic**: Reintentar si falla la conexión
- **Validación inicial**: ¿Los datos tienen el formato esperado?

### 2. **Transformación (Transform)**
- Limpiar datos (nulos, duplicados, outliers)
- Calcular nuevas columnas
- Combinar datos de diferentes fuentes
- **Validación**: ¿Los datos transformados son correctos?

### 3. **Carga (Load)**
- Guardar en destino (DB, data warehouse, data lake)
- **Bulk inserts**: Cargar miles de filas de golpe (no una por una)
- **Idempotencia**: Asegurar que se puede reprocesar

### 4. **Logging (Registro)**
```python
logger.info("Iniciando pipeline de ventas")
logger.info(f"Extraídas {len(ventas)} ventas")
logger.warning(f"Encontrados {nulos} valores nulos")
logger.error("Error al conectar a la DB")
```

**Por qué es crucial**: Sin logs, cuando algo falla, no sabes **qué, dónde ni por qué**.

### 5. **Monitoreo (Monitoring)**
- **Métricas**: ¿Cuántas filas procesadas? ¿Cuánto tiempo tomó?
- **Alertas**: Notificar si el pipeline falla o tarda mucho
- **Dashboards**: Visualizar el estado del pipeline en tiempo real

### 6. **Manejo de Errores (Error Handling)**
```python
try:
    extraer_datos()
except ConnectionError:
    # Reintentar 3 veces con exponential backoff
    reintentar()
except ValueError:
    # Guardar datos problemáticos en "dead letter queue"
    guardar_error()
```

### 7. **Tests (Testing)**
- **Unit tests**: ¿La función de transformación funciona bien?
- **Integration tests**: ¿El pipeline completo funciona?
- **Data quality tests**: ¿Los datos cargados son correctos?

---

## 6. Reprocessing: Cuando Algo Sale Mal

**Reprocessing** es **volver a ejecutar** un pipeline para un período de tiempo pasado.

### ¿Cuándo necesitas Reprocessing?

1. **Bug en la transformación** descubierto 2 semanas después
2. **Fuente de datos incorrecta**: Te dieron datos erróneos y ahora tienen los correctos
3. **Cambio de negocio**: Ahora quieres calcular un nuevo campo en datos históricos
4. **Fallo parcial**: El pipeline procesó 50% y falló

### Ejemplo

```python
# 1. Pipeline original (1 octubre)
procesar_ventas('2025-10-01')  # Procesó mal (bug en transformación)

# 2. Descubres el bug (15 octubre)
# Los datos de octubre están INCORRECTOS

# 3. Corriges el bug

# 4. Reprocessing: Vuelves a procesar todo octubre
for dia in range(1, 16):
    procesar_ventas(f'2025-10-{dia:02d}')
```

### Cómo Diseñar para Reprocessing

1. **Idempotencia**: Asegura que reprocesar no cause duplicados
2. **Particionamiento**: Procesa por fecha para poder reprocesar períodos específicos
3. **Versionado**: Guarda diferentes versiones de los datos

```python
# Mal diseño (❌): Todo en una tabla sin fecha
guardar_en_db(ventas)

# Buen diseño (✅): Particionado por fecha
guardar_en_db(ventas, particion='2025-10-23')
```

---

## 7. Errores Comunes al Diseñar Pipelines

### Error 1: No Hacer el Pipeline Idempotente

**Problema**: Ejecutar 2 veces = datos duplicados

**Solución**: Usa DELETE + INSERT o MERGE/UPSERT

---

### Error 2: No Loggear Suficiente

**Problema**: Cuando falla, no sabes qué pasó

**Solución**:
```python
logger.info("Iniciando pipeline")
logger.info(f"Extraídas {n} filas")
logger.warning(f"{nulos} valores nulos encontrados")
logger.error("Error al conectar a la DB: {error}")
```

---

### Error 3: Procesar Todo en una Transacción Grande

**Problema**: Si algo falla al 90%, pierdes todo el trabajo

**Solución**: Usa **micro-batches** (procesa de 1000 en 1000)

```python
# Mal (❌): Todo o nada
with transaccion():
    for venta in todas_las_ventas:  # 10 millones
        insertar(venta)

# Bien (✅): En bloques
for lote in dividir_en_lotes(ventas, 1000):
    with transaccion():
        for venta in lote:
            insertar(venta)
```

---

### Error 4: No Manejar Casos Borde

**Casos borde comunes**:
- ¿Qué pasa si el archivo está vacío?
- ¿Qué pasa si no hay datos para hoy?
- ¿Qué pasa si la columna esperada no existe?

**Solución**: Valida **siempre** antes de procesar

```python
if archivo_vacio():
    logger.warning("Archivo vacío, saltando procesamiento")
    return

if not columna_existe('precio'):
    raise ValueError("Columna 'precio' no encontrada")
```

---

### Error 5: No Testear el Pipeline

**Problema**: Lo pruebas con 10 filas, falla con 10 millones

**Solución**:
- Test con datos reales (no inventados)
- Test con volúmenes grandes
- Test con datos sucios (nulos, duplicados, outliers)

---

## Checklist de Aprendizaje

Antes de continuar al siguiente tema, verifica que puedes:

- [ ] Explicar qué es un pipeline de datos con tus propias palabras
- [ ] Diferenciar entre ETL y ELT
- [ ] Decidir cuándo usar ETL vs ELT según el contexto
- [ ] Explicar la diferencia entre Batch y Streaming
- [ ] Definir qué es idempotencia y por qué es importante
- [ ] Diseñar un pipeline idempotente (DELETE + INSERT o MERGE)
- [ ] Listar los componentes de un pipeline de producción
- [ ] Explicar qué es reprocessing y cuándo se necesita
- [ ] Identificar errores comunes al diseñar pipelines

---

## Resumen del Tema

1. **Pipeline de datos**: Serie de pasos automatizados que mueven y transforman datos
2. **ETL**: Transform **antes** de cargar (útil con destinos pequeños)
3. **ELT**: Transform **después** de cargar (útil con data warehouses potentes)
4. **Batch**: Procesar por lotes cada X tiempo (simple, económico, latencia alta)
5. **Streaming**: Procesar en tiempo real (complejo, costoso, latencia baja)
6. **Idempotencia**: Ejecutar N veces = mismo resultado que 1 vez (crítico para robustez)
7. **Reprocessing**: Volver a ejecutar un pipeline para corregir datos históricos
8. **Componentes clave**: Extract, Transform, Load, Logging, Monitoring, Error Handling, Tests

---

## Próximos Pasos

Ahora que entiendes los conceptos fundamentales, en los siguientes temas aprenderás a **implementarlos**:

- **Tema 2**: Extracción de datos (archivos, APIs, web scraping)
- **Tema 3**: Transformación con Pandas
- **Tema 4**: Validación de calidad de datos
- **Tema 5**: Formatos modernos (Parquet, Avro)
- **Tema 6**: Estrategias de carga y pipelines completos

---

## Recursos Adicionales

### Libros
- "Data Pipelines Pocket Reference" - James Densmore
- "Designing Data-Intensive Applications" - Martin Kleppmann

### Artículos
- [ETL vs ELT: The Difference Is In The How](https://www.integrate.io/blog/etl-vs-elt/)
- [Idempotent Data Pipelines](https://medium.com/airbnb-engineering/idempotent-data-pipelines-ef9c4e7f5c6d)

### Herramientas
- Apache Airflow (orquestación de pipelines)
- dbt (transformaciones con SQL)
- Great Expectations (calidad de datos)

---

**¡Felicidades!** Has completado la teoría del Tema 1. Ahora continúa con **02-EJEMPLOS.md** para ver pipelines en acción, y luego practica con **03-EJERCICIOS.md**.

**Última actualización**: 2025-10-23
