# Proyectos Prácticos del Master

Este documento detalla todos los proyectos prácticos del Master en Ingeniería de Datos, organizados por módulo con complejidad progresiva.

---

## Tabla de Contenidos

- [Módulo 1: Fundamentos de Programación](#módulo-1-fundamentos-de-programación)
- [Módulo 2: Bases de Datos y SQL](#módulo-2-bases-de-datos-y-sql)
- [Módulo 3: Ingeniería de Datos Core](#módulo-3-ingeniería-de-datos-core)
- [Módulo 4: Almacenamiento y Modelado](#módulo-4-almacenamiento-y-modelado)
- [Módulo 5: Big Data](#módulo-5-big-data-y-procesamiento-distribuido)
- [Módulo 6: Cloud Data Engineering](#módulo-6-cloud-data-engineering)
- [Módulo 7: Orquestación](#módulo-7-orquestación-y-automatización)
- [Módulo 8: IA y ML](#módulo-8-ia-y-machine-learning)
- [Módulo 9: DataOps](#módulo-9-dataops-calidad-y-gobernanza)
- [Módulo 10: Proyecto Final](#módulo-10-proyecto-final)

---

## Módulo 1: Fundamentos de Programación

### Proyecto 1.1: Calculadora de Estadísticas Básicas

**Objetivo**: Crear funciones reutilizables para calcular estadísticas, aplicando TDD y buenas prácticas.

**Duración estimada**: 1 semana

**Requerimientos**:

1. Implementar funciones para:
   - Media (promedio)
   - Mediana
   - Moda
   - Desviación estándar
   - Varianza
   - Percentiles (25, 50, 75)

2. Requisitos técnicos:
   - Tipado explícito en todas las funciones
   - Validación de inputs (listas no vacías, números válidos)
   - Manejo de errores con excepciones específicas
   - Tests con pytest (coverage >80%)
   - Documentación con docstrings

**Estructura esperada**:
```
proyecto-1-estadisticas/
├── src/
│   └── estadisticas.py
├── tests/
│   └── test_estadisticas.py
├── README.md
└── requirements.txt
```

**Criterios de éxito**:
- [ ] Todas las funciones pasan tests
- [ ] Código formateado con black
- [ ] Sin errores de flake8
- [ ] README con ejemplos de uso
- [ ] Manejo correcto de casos edge (lista vacía, valores None)

**Ejemplo de uso esperado**:
```python
from estadisticas import calcular_media, calcular_desviacion_estandar

datos = [10, 20, 30, 40, 50]
media = calcular_media(datos)  # 30.0
desv = calcular_desviacion_estandar(datos)  # 14.14
```

---

### Proyecto 1.2: Procesador de Archivos CSV

**Objetivo**: Leer, validar y transformar archivos CSV con manejo robusto de errores.

**Duración estimada**: 1-2 semanas

**Requerimientos**:

1. Funcionalidades:
   - Leer archivos CSV con diferentes delimitadores
   - Validar estructura (columnas esperadas, tipos de datos)
   - Limpiar datos (eliminar duplicados, valores nulos)
   - Transformar datos (cambiar formatos de fecha, normalizar strings)
   - Escribir resultados en nuevo CSV

2. Manejo de errores:
   - Archivo no encontrado
   - Columnas faltantes
   - Tipos de datos incorrectos
   - Registros con formato inválido

3. Requisitos técnicos:
   - Usar módulo `csv` de Python (no pandas todavía)
   - Funciones puras sin efectos secundarios
   - Logging con diferentes niveles (INFO, WARNING, ERROR)
   - Tests con archivos de prueba
   - Uso de `pathlib.Path` para rutas

**Estructura esperada**:
```
proyecto-2-csv-processor/
├── src/
│   ├── lector.py
│   ├── validador.py
│   ├── transformador.py
│   └── escritor.py
├── tests/
│   ├── test_lector.py
│   ├── test_validador.py
│   └── fixtures/
│       ├── datos_validos.csv
│       └── datos_invalidos.csv
├── logs/
├── README.md
└── requirements.txt
```

**Criterios de éxito**:
- [ ] Procesa archivos CSV de >10,000 filas
- [ ] Log detallado de todas las operaciones
- [ ] Validación robusta con mensajes claros
- [ ] Tests incluyen casos de error
- [ ] Documentación de funciones principales

---

### Proyecto 1.3: Sistema de Logs Configurable

**Objetivo**: Implementar un sistema de logging profesional para aplicaciones.

**Duración estimada**: 1 semana

**Requerimientos**:

1. Configuración flexible:
   - Niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - Múltiples outputs (consola, archivo, ambos)
   - Rotación de archivos por tamaño o fecha
   - Formato personalizable

2. Funcionalidades:
   - Logger singleton (instancia única)
   - Logs estructurados (JSON para parsing)
   - Context managers para logging de bloques
   - Decoradores para logging de funciones

3. Requisitos técnicos:
   - Usar módulo `logging` de Python
   - Configuración desde archivo (JSON o YAML)
   - Tests para cada nivel de log
   - Documentación de configuración

**Criterios de éxito**:
- [ ] Sistema configurable sin cambiar código
- [ ] Logs estructurados en JSON
- [ ] Rotación de archivos funciona
- [ ] Decoradores fáciles de usar
- [ ] Ejemplos de uso documentados

---

## Módulo 2: Bases de Datos y SQL

### Proyecto 2.1: Sistema de Biblioteca

**Objetivo**: Diseñar y implementar un sistema de gestión de biblioteca con modelo relacional completo.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. Modelo de datos:
   - Tablas: libros, autores, usuarios, prestamos, categorias
   - Relaciones: muchos-a-muchos (libros-autores), uno-a-muchos (prestamos)
   - Constraints: PK, FK, unique, check
   - Normalización hasta 3NF

2. Funcionalidades SQL:
   - Consultas complejas con múltiples JOINs
   - Window functions (ranking de libros más prestados)
   - CTEs para análisis complejos
   - Views para consultas frecuentes
   - Índices para optimización

3. Integración con Python:
   - Funciones para CRUD operations
   - Manejo de transacciones
   - Prevención de SQL injection
   - Connection pooling

**Estructura esperada**:
```
proyecto-biblioteca/
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_create_tables.sql
│   ├── 03_create_indexes.sql
│   ├── 04_create_views.sql
│   └── 05_insert_sample_data.sql
├── src/
│   ├── database.py
│   ├── libros.py
│   ├── prestamos.py
│   └── usuarios.py
├── tests/
│   └── test_database.py
├── docs/
│   └── modelo_er.png
├── README.md
└── requirements.txt
```

**Consultas destacadas a implementar**:
- Top 10 libros más prestados del último año
- Usuarios con préstamos vencidos
- Análisis de tendencias por categoría
- Disponibilidad de libros en tiempo real

**Criterios de éxito**:
- [ ] Modelo ER documentado con diagrama
- [ ] Todas las tablas normalizadas
- [ ] Índices justificados y documentados
- [ ] Prevención de SQL injection validada
- [ ] Performance de queries optimizada
- [ ] Tests de integridad referencial

---

### Proyecto 2.2: ETL Básico con Python

**Objetivo**: Extraer datos de CSV, transformar y cargar en PostgreSQL.

**Duración estimada**: 2 semanas

**Requerimientos**:

1. Extracción:
   - Leer múltiples archivos CSV de una carpeta
   - Validar estructura de cada archivo
   - Logging de proceso de extracción

2. Transformación:
   - Limpieza de datos (nulos, duplicados)
   - Conversión de tipos de datos
   - Cálculo de campos derivados
   - Enriquecimiento con datos de lookup

3. Carga:
   - Bulk insert en PostgreSQL
   - Manejo de errores (rollback en caso de fallo)
   - Update de registros existentes (upsert)
   - Logging de registros cargados

4. Control:
   - Tabla de auditoría (metadata de ejecuciones)
   - Manejo idempotente (puede re-ejecutarse)
   - Validación post-carga

**Estructura esperada**:
```
proyecto-etl-basico/
├── src/
│   ├── extractor.py
│   ├── transformador.py
│   ├── cargador.py
│   └── main.py
├── data/
│   ├── input/
│   └── processed/
├── sql/
│   └── create_tables.sql
├── tests/
├── config/
│   └── database.yaml
└── README.md
```

**Criterios de éxito**:
- [ ] ETL idempotente (re-ejecutable)
- [ ] Transacciones garantizan consistencia
- [ ] Logging completo del proceso
- [ ] Performance: >10,000 registros/segundo
- [ ] Tests de integración completos

---

### Proyecto 2.3: API de Consultas Seguras

**Objetivo**: Crear funciones Python que ejecuten consultas SQL de forma segura y eficiente.

**Duración estimada**: 1-2 semanas

**Requerimientos**:

1. API de funciones:
   - `buscar_usuarios(filtros: dict) -> List[Usuario]`
   - `obtener_estadisticas_ventas(fecha_inicio, fecha_fin) -> dict`
   - `generar_reporte(tipo: str, parametros: dict) -> DataFrame`

2. Seguridad:
   - Consultas parametrizadas (no f-strings)
   - Validación de inputs
   - Rate limiting (prevenir abuso)
   - Logging de accesos

3. Performance:
   - Connection pooling con SQLAlchemy
   - Caching de consultas frecuentes
   - Paginación de resultados grandes
   - Timeouts configurables

**Criterios de éxito**:
- [ ] Sin vulnerabilidades de SQL injection
- [ ] Connection pool configurado correctamente
- [ ] Cache funciona para queries repetidas
- [ ] Tests de seguridad implementados
- [ ] Documentación de API completa

---

## Módulo 3: Ingeniería de Datos Core

### Proyecto 3.1: Pipeline de Noticias

**Objetivo**: Extraer noticias de API pública, limpiar y almacenar en base de datos.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. Extracción:
   - Consumir API REST (ej: NewsAPI, Guardian API)
   - Manejar paginación y rate limits
   - Reintentos con backoff exponencial
   - Logging de requests

2. Transformación con Pandas:
   - Limpieza de HTML en contenido
   - Normalización de fechas
   - Extracción de entidades (keywords, categorías)
   - Deduplicación inteligente
   - Análisis de sentimiento básico (opcional)

3. Carga:
   - Almacenar en PostgreSQL
   - Diseño de tablas optimizado
   - Manejo de duplicados (upsert)

4. Validación:
   - Schema validation con Pydantic
   - Data quality checks
   - Reportes de calidad

**Estructura esperada**:
```
proyecto-pipeline-noticias/
├── src/
│   ├── extractor/
│   │   ├── api_client.py
│   │   └── retry_handler.py
│   ├── transformador/
│   │   ├── limpieza.py
│   │   └── validacion.py
│   ├── cargador/
│   │   └── database.py
│   └── pipeline.py
├── tests/
│   ├── test_extractor.py
│   ├── test_transformador.py
│   └── test_integration.py
├── config/
│   └── config.yaml
├── logs/
└── README.md
```

**Criterios de éxito**:
- [ ] Pipeline procesa >1000 noticias
- [ ] Manejo robusto de errores de API
- [ ] Validación de datos completa
- [ ] Deduplicación efectiva
- [ ] Logs detallados de proceso
- [ ] Tests de integración pasan

---

### Proyecto 3.2: ETL Incremental

**Objetivo**: Pipeline que procesa solo datos nuevos usando watermarks.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. Control de watermarks:
   - Tabla de control con última ejecución
   - Tracking de estado por partición
   - Manejo de re-procesamiento

2. Extracción incremental:
   - Query con filtro temporal
   - Detección de updates (change data capture básico)
   - Manejo de deletes (soft deletes)

3. Transformación:
   - Solo procesar registros nuevos/modificados
   - Mantener historial de cambios
   - Calcular deltas

4. Validación:
   - Reconciliación entre source y target
   - Alertas de discrepancias
   - Reportes de cambios procesados

**Funcionalidades clave**:
- Reanudar desde último punto exitoso
- Backfill de fechas históricas
- Dry-run mode (sin commitear cambios)

**Criterios de éxito**:
- [ ] Solo procesa datos nuevos (eficiente)
- [ ] Puede recuperarse de errores
- [ ] Watermarks actualizados correctamente
- [ ] Reconciliación 100% exacta
- [ ] Documentación de estrategia implementada

---

### Proyecto 3.3: Framework de Data Quality

**Objetivo**: Sistema reutilizable para validar calidad de datos.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. Validaciones implementadas:
   - Schema validation (columnas, tipos)
   - Nullability checks
   - Uniqueness constraints
   - Referential integrity
   - Value ranges (min, max)
   - Format validation (emails, phones, dates)
   - Custom business rules

2. Framework:
   - Configuración declarativa (YAML/JSON)
   - Extensible para nuevas validaciones
   - Reportes detallados de fallos
   - Métricas de calidad (% completeness, etc.)

3. Integración:
   - Usable en pipelines existentes
   - Great Expectations integration
   - Alertas automáticas
   - Dashboard de calidad (opcional)

**Estructura esperada**:
```
proyecto-data-quality/
├── src/
│   ├── validadores/
│   │   ├── base.py
│   │   ├── schema.py
│   │   ├── completeness.py
│   │   ├── uniqueness.py
│   │   └── custom.py
│   ├── framework.py
│   └── reportes.py
├── config/
│   └── validaciones.yaml
├── tests/
├── ejemplos/
│   └── uso_basico.py
└── README.md
```

**Criterios de éxito**:
- [ ] Framework extensible y reutilizable
- [ ] Configuración declarativa clara
- [ ] Reportes detallados y accionables
- [ ] Tests para cada validador
- [ ] Documentación con ejemplos
- [ ] Integrable con Great Expectations

---

## Módulo 4: Almacenamiento y Modelado

### Proyecto 4.1: Data Warehouse de Ventas

**Objetivo**: Diseñar e implementar DWH dimensional con SCD Type 2.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Modelo dimensional:
   - Fact table: ventas (grain: transacción)
   - Dimensions: producto, cliente, tienda, tiempo, vendedor
   - Métricas: cantidad, monto, descuento, ganancia
   - Star schema

2. SCD Type 2 implementado en:
   - Dim_Cliente (cambios de dirección, categoría)
   - Dim_Producto (cambios de precio, categoría)

3. Campos SCD Type 2:
   - Surrogate key (auto-increment)
   - Natural key (business key)
   - fecha_inicio, fecha_fin
   - is_current (flag booleano)
   - version_number

4. ETL al DWH:
   - Carga inicial (full load)
   - Carga incremental con detección de cambios
   - Manejo de late-arriving facts

5. Consultas analíticas:
   - Ventas por período (año, trimestre, mes)
   - Top productos/clientes/tiendas
   - Análisis de tendencias
   - Comparaciones YoY (year-over-year)

**Estructura esperada**:
```
proyecto-dwh-ventas/
├── sql/
│   ├── 01_create_staging.sql
│   ├── 02_create_dimensions.sql
│   ├── 03_create_facts.sql
│   ├── 04_create_views.sql
│   └── 05_sample_queries.sql
├── src/
│   ├── etl/
│   │   ├── load_dimensions.py
│   │   ├── load_facts.py
│   │   └── scd_handler.py
│   └── utils/
│       └── database.py
├── docs/
│   ├── modelo_dimensional.png
│   └── diccionario_datos.md
├── tests/
└── README.md
```

**Criterios de éxito**:
- [ ] Modelo dimensional correctamente implementado
- [ ] SCD Type 2 funciona correctamente
- [ ] ETL incremental eficiente
- [ ] Queries analíticas optimizadas
- [ ] Documentación completa del modelo
- [ ] Diagramas ER y dimensional

---

### Proyecto 4.2: Data Lake con Capas

**Objetivo**: Organizar Data Lake en capas bronze/silver/gold.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. Arquitectura del Data Lake:
   ```
   data-lake/
   ├── bronze/  (raw data, sin transformar)
   │   ├── ventas/
   │   ├── clientes/
   │   └── productos/
   ├── silver/  (cleaned, validated)
   │   ├── ventas/
   │   ├── clientes/
   │   └── productos/
   └── gold/    (aggregated, business-ready)
       ├── ventas_diarias/
       ├── kpis/
       └── reportes/
   ```

2. Bronze layer:
   - Ingesta de datos raw (CSV, JSON, API)
   - Particionado por fecha de ingesta
   - Sin transformaciones
   - Metadata tracking

3. Silver layer:
   - Limpieza y validación
   - Schema enforcement
   - Deduplicación
   - Formato Parquet optimizado

4. Gold layer:
   - Agregaciones de negocio
   - Tablas listas para analytics/BI
   - Métricas pre-calculadas
   - Optimizado para lectura

5. Pipeline entre capas:
   - Bronze → Silver: limpieza
   - Silver → Gold: agregación
   - Orquestación con scripts Python

**Estructura esperada**:
```
proyecto-data-lake/
├── src/
│   ├── ingesta/
│   │   └── to_bronze.py
│   ├── procesamiento/
│   │   ├── bronze_to_silver.py
│   │   └── silver_to_gold.py
│   └── utils/
│       └── storage.py
├── data-lake/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── config/
│   └── partitioning.yaml
└── README.md
```

**Criterios de éxito**:
- [ ] Capas claramente separadas
- [ ] Particionamiento eficiente
- [ ] Formato Parquet en silver/gold
- [ ] Metadata tracking implementado
- [ ] Pipeline automatizado entre capas
- [ ] Documentación de convenciones

---

### Proyecto 4.3: Delta Lake con Time Travel

**Objetivo**: Implementar capacidades ACID en Data Lake con Delta Lake.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. Conversión a Delta:
   - Migrar datos Parquet a Delta format
   - Mantener estructura de particionamiento
   - Configuración de retention policies

2. Operaciones ACID:
   - Insert/Update/Delete en Data Lake
   - Merge (upsert) operations
   - Transacciones garantizadas

3. Time travel:
   - Queries a versiones históricas
   - Restore de datos anteriores
   - Audit trail completo

4. Optimizaciones Delta:
   - OPTIMIZE (compaction)
   - VACUUM (cleanup)
   - Z-ORDER clustering

5. Schema evolution:
   - Add columns
   - Change column types
   - Merge schema changes

**Funcionalidades a demostrar**:
```python
# Time travel
df = spark.read.format("delta").option("versionAsOf", 5).load("/path")

# Merge
deltaTable.merge(updates, "target.id = source.id") \
  .whenMatchedUpdate(set = {...}) \
  .whenNotMatchedInsert(values = {...}) \
  .execute()

# Optimize
spark.sql("OPTIMIZE delta_table ZORDER BY (customer_id)")
```

**Criterios de éxito**:
- [ ] Delta Lake funcional con ACID
- [ ] Time travel implementado
- [ ] Merge operations funcionan
- [ ] Optimizaciones aplicadas
- [ ] Schema evolution documentada
- [ ] Performance mejorado vs Parquet

---

## Módulo 5: Big Data y Procesamiento Distribuido

### Proyecto 5.1: Procesamiento de Logs con Spark

**Objetivo**: Analizar millones de registros de logs usando Apache Spark.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Dataset:
   - Generar o usar logs de servidor web (Apache/Nginx format)
   - Tamaño: >10 millones de registros
   - Formato: JSON Lines o CSV

2. Procesamiento con PySpark:
   - Parsing de logs con regex
   - Agregaciones (requests por hora, por endpoint)
   - Detección de errores (status codes 4xx, 5xx)
   - Identificación de IPs sospechosas (rate anomalies)
   - Window functions (rolling averages)

3. Análisis:
   - Top endpoints más llamados
   - Distribución de response times
   - User agents analysis
   - Geographic distribution (si hay IP geolocation)
   - Anomaly detection básica

4. Optimizaciones:
   - Particionamiento eficiente
   - Caching de DataFrames intermedios
   - Broadcast de lookup tables
   - Evitar shuffles innecesarios

5. Output:
   - Resultados en Parquet particionado
   - Reportes agregados en PostgreSQL
   - Dashboards con métricas (opcional)

**Estructura esperada**:
```
proyecto-spark-logs/
├── src/
│   ├── ingesta.py
│   ├── procesamiento.py
│   ├── analisis.py
│   └── utils/
│       └── spark_session.py
├── jobs/
│   └── process_logs.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── exploratory_analysis.ipynb
└── README.md
```

**Métricas de performance esperadas**:
- Procesar >10M registros en <5 minutos (local)
- Uso eficiente de memoria (sin OOM errors)
- Paralelismo bien distribuido

**Criterios de éxito**:
- [ ] Job procesa millones de registros eficientemente
- [ ] Optimizaciones de Spark aplicadas
- [ ] Análisis genera insights útiles
- [ ] Código modular y reutilizable
- [ ] Spark UI muestra buena distribución
- [ ] Documentación de optimizaciones

---

### Proyecto 5.2: Pipeline de Streaming con Kafka + Spark

**Objetivo**: Procesar eventos en tiempo real con Kafka y Spark Streaming.

**Duración estimada**: 4-5 semanas

**Requerimientos**:

1. Arquitectura:
   ```
   Producer → Kafka → Spark Streaming → Output (DB/File/Dashboard)
   ```

2. Kafka Setup:
   - Topics: raw_events, processed_events, alerts
   - Multiple partitions para paralelismo
   - Replication factor configurado
   - Schema registry (con Avro - opcional)

3. Producer (simulado):
   - Generar eventos sintéticos (clicks, transacciones, IoT)
   - Rate configurable (eventos/segundo)
   - Diferentes tipos de eventos

4. Spark Structured Streaming:
   - Consumir de Kafka
   - Transformaciones en micro-batches
   - Windowing (tumbling, sliding, session windows)
   - Watermarks para late data
   - Stateful operations (running totals)

5. Procesamiento:
   - Agregaciones en ventanas de tiempo
   - Detección de patrones (ej: más de X eventos en Y minutos)
   - Enriquecimiento con datos estáticos (broadcast)
   - Alertas para anomalías

6. Output:
   - Escribir resultados a Kafka (processed topic)
   - Almacenar en PostgreSQL para analytics
   - Triggers para alertas críticas

7. Monitoreo:
   - Lag de consumer
   - Throughput de procesamiento
   - Errores y reinicios

**Estructura esperada**:
```
proyecto-streaming/
├── producer/
│   └── event_generator.py
├── consumer/
│   ├── spark_streaming_job.py
│   └── processors/
│       ├── aggregator.py
│       └── alerter.py
├── kafka/
│   └── docker-compose.yml
├── config/
│   └── kafka_config.yaml
└── README.md
```

**Criterios de éxito**:
- [ ] Pipeline procesa eventos en tiempo real
- [ ] Latencia end-to-end <5 segundos
- [ ] Windowing funciona correctamente
- [ ] Manejo de late-arriving data
- [ ] Alertas se generan automáticamente
- [ ] Sistema resiliente a fallos
- [ ] Monitoreo implementado

---

### Proyecto 5.3: Sistema de Recomendaciones Distribuido

**Objetivo**: Generar recomendaciones usando procesamiento distribuido con Spark.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Dataset:
   - Transacciones user-item (ej: compras, clicks, ratings)
   - >1M usuarios, >100K items
   - Generado sintéticamente o dataset público (MovieLens, etc.)

2. Algoritmo:
   - Collaborative filtering con ALS (Alternating Least Squares)
   - Matrix factorization distribuido
   - Spark MLlib

3. Pipeline:
   - Preparación de datos (user-item matrix)
   - Training de modelo ALS
   - Generación de recomendaciones para todos los usuarios
   - Evaluación de modelo (RMSE, precision@k)

4. Optimizaciones:
   - Hyperparameter tuning (rank, iterations, regularization)
   - Caching de matrices intermedias
   - Particionamiento estratégico

5. Serving:
   - Pre-compute recomendaciones batch
   - Almacenar en Redis/PostgreSQL
   - API para consultar recomendaciones

**Criterios de éxito**:
- [ ] Modelo entrena en tiempo razonable
- [ ] Recomendaciones generadas para >1M usuarios
- [ ] Métricas de evaluación calculadas
- [ ] Pipeline optimizado para big data
- [ ] Resultados almacenados eficientemente
- [ ] Documentación de approach

---

## Módulo 6: Cloud Data Engineering

### Proyecto 6.1: Pipeline Serverless en AWS

**Objetivo**: Implementar pipeline completamente serverless usando servicios AWS.

**Duración estimada**: 3-4 semanas

**Arquitectura**:
```
S3 (landing) → Lambda (trigger) → Glue (ETL) → S3 (processed) → Athena (queries)
```

**Requerimientos**:

1. Componentes AWS:
   - **S3**: Buckets para raw, processed, curated
   - **Lambda**: Trigger para procesar nuevos archivos
   - **Glue**: ETL jobs y Data Catalog
   - **Athena**: Queries SQL sobre S3
   - **CloudWatch**: Logging y monitoring
   - **IAM**: Roles y policies

2. Flujo:
   - Archivo CSV/JSON llega a S3 (landing zone)
   - Lambda se dispara automáticamente
   - Lambda valida y lanza Glue job
   - Glue transforma datos (limpieza, validación)
   - Glue escribe Parquet a S3 (processed zone)
   - Glue actualiza Data Catalog
   - Athena puede querier los datos procesados

3. Glue ETL:
   - PySpark script
   - Schema validation
   - Particionamiento por fecha
   - Format conversion (CSV → Parquet)

4. Infraestructura como Código:
   - Terraform para toda la infraestructura
   - Versionado en Git
   - Environments (dev, prod)

5. Seguridad:
   - Encryption at rest (S3)
   - Encryption in transit (SSL/TLS)
   - IAM least privilege
   - Secrets en Secrets Manager

**Estructura esperada**:
```
proyecto-aws-serverless/
├── terraform/
│   ├── main.tf
│   ├── s3.tf
│   ├── lambda.tf
│   ├── glue.tf
│   └── iam.tf
├── lambda/
│   └── trigger_function.py
├── glue/
│   └── etl_job.py
├── tests/
└── README.md
```

**Criterios de éxito**:
- [ ] Pipeline totalmente serverless
- [ ] IaC despliega toda la infraestructura
- [ ] Procesamiento automático al subir archivo
- [ ] Queries en Athena funcionan
- [ ] Seguridad implementada correctamente
- [ ] Costos optimizados y documentados
- [ ] Monitoring con CloudWatch

---

### Proyecto 6.2: Data Warehouse en Snowflake

**Objetivo**: Implementar DWH cloud-native con capacidades modernas.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Arquitectura Snowflake:
   - Databases: RAW, ANALYTICS, REPORTING
   - Schemas por dominio de negocio
   - Roles y permisos (RBAC)
   - Warehouses (compute) separados por uso

2. Ingesta de datos:
   - Snowpipe para ingesta continua desde S3
   - COPY commands para bulk loads
   - Stages externos (S3, Azure Blob)

3. Modelo dimensional:
   - Star schema en ANALYTICS database
   - SCD Type 2 usando MERGE
   - Time dimension con date spine
   - Views en REPORTING para BI tools

4. Features de Snowflake:
   - Time travel para auditoría
   - Zero-copy cloning para dev/test
   - Data sharing (opcional)
   - Streams y Tasks para CDC

5. Optimizaciones:
   - Clustering keys en tablas grandes
   - Materializedviews para queries frecuentes
   - Query optimization (pruning, caching)

6. Integración:
   - dbt para transformaciones
   - Conexión desde Python (snowflake-connector)
   - Tableau/PowerBI para visualización (opcional)

**Estructura esperada**:
```
proyecto-snowflake-dwh/
├── sql/
│   ├── 01_setup_databases.sql
│   ├── 02_setup_schemas.sql
│   ├── 03_create_stages.sql
│   ├── 04_create_tables.sql
│   └── 05_setup_snowpipe.sql
├── dbt/
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
├── python/
│   └── ingestion/
└── docs/
    └── arquitectura.md
```

**Criterios de éxito**:
- [ ] DWH implementado en Snowflake
- [ ] Ingesta automática funciona (Snowpipe)
- [ ] dbt transforma datos correctamente
- [ ] Time travel funcional
- [ ] Cloning usado para ambientes
- [ ] Performance optimizado (clustering)
- [ ] RBAC implementado
- [ ] Documentación completa

---

### Proyecto 6.3: IaC Multi-Cloud con Terraform

**Objetivo**: Desplegar infraestructura de datos en múltiples clouds con Terraform.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Recursos a desplegar:
   
   **AWS**:
   - S3 buckets
   - Redshift cluster
   - Lambda functions
   - VPC y networking
   
   **GCP**:
   - Cloud Storage buckets
   - BigQuery datasets
   - Cloud Functions
   
   **Azure** (opcional):
   - Blob Storage
   - Synapse workspace

2. Terraform:
   - Módulos reutilizables
   - Remote state (S3 backend)
   - Workspaces para environments
   - Variables y outputs bien definidos
   - Secrets management

3. Networking:
   - VPC/VNet setup
   - Private subnets
   - Security groups
   - VPC peering (si integración multi-cloud)

4. CI/CD para IaC:
   - GitHub Actions workflow
   - Terraform plan en PRs
   - Terraform apply en merge a main
   - Drift detection

5. Documentación:
   - Diagramas de arquitectura
   - Decision records (ADRs)
   - Runbooks de despliegue
   - Disaster recovery plan

**Estructura esperada**:
```
proyecto-iac-multicloud/
├── terraform/
│   ├── modules/
│   │   ├── aws-data-lake/
│   │   ├── gcp-bigquery/
│   │   └── azure-storage/
│   ├── environments/
│   │   ├── dev/
│   │   └── prod/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── .github/
│   └── workflows/
│       └── terraform.yml
├── docs/
│   ├── architecture.md
│   └── adr/
└── README.md
```

**Criterios de éxito**:
- [ ] IaC despliega en múltiples clouds
- [ ] Módulos reutilizables y bien estructurados
- [ ] CI/CD automatiza despliegues
- [ ] State remoto configurado
- [ ] Secrets manejados correctamente
- [ ] Documentación exhaustiva
- [ ] Destroy funciona sin errores

---

### Proyecto 6.4: Pipeline Multi-Cloud (AWS → GCP)

**Objetivo**: Integrar datos entre diferentes cloud providers.

**Duración estimada**: 2-3 semanas

**Arquitectura**:
```
AWS S3 → AWS Lambda → GCP Cloud Function → BigQuery
```

**Requerimientos**:

1. Source (AWS):
   - Datos en S3
   - Lambda para exportar/notificar

2. Target (GCP):
   - Cloud Function recibe datos
   - Procesa y carga a BigQuery

3. Transferencia:
   - Pub/Sub para messaging entre clouds
   - Cloud Storage Transfer Service (alternativa)
   - Autenticación cross-cloud (service accounts)

4. Monitoring:
   - CloudWatch (AWS)
   - Cloud Monitoring (GCP)
   - Alertas de fallos

**Criterios de éxito**:
- [ ] Datos fluyen automáticamente entre clouds
- [ ] Autenticación cross-cloud segura
- [ ] Pipeline resiliente a fallos
- [ ] Monitoring end-to-end
- [ ] Costos de transferencia optimizados

---

## Módulo 7: Orquestación y Automatización

### Proyecto 7.1: Pipeline Completo con Airflow + dbt

**Objetivo**: Orquestar pipeline end-to-end usando Airflow y dbt.

**Duración estimada**: 4-5 semanas

**Arquitectura**:
```
Airflow DAG:
  Extract (API) → Load to Raw DB → dbt transform → Data Quality → Export to DWH
```

**Requerimientos**:

1. Airflow Setup:
   - Docker Compose con servicios Airflow
   - Postgres como metadata DB
   - LocalExecutor o CeleryExecutor
   - Variables y Connections configuradas

2. DAG Structure:
   - Task para extracción de API
   - Task para carga a staging
   - TaskGroup de transformaciones dbt
   - Task de validación de calidad
   - Task de carga a DWH
   - Notificaciones en fallo/éxito

3. dbt Project:
   - Models organizados por capa (staging, intermediate, marts)
   - Tests de datos (not_null, unique, relationships)
   - Documentation con descriptions
   - Macros reutilizables
   - Snapshots para SCD

4. Integración Airflow + dbt:
   - BashOperator o DbtOperator
   - Dependency entre dbt models respetada
   - Logs de dbt visibles en Airflow

5. Data Quality:
   - Great Expectations expectations
   - Validación post-transformación
   - Reportes de calidad

6. Scheduling:
   - DAG ejecuta diariamente
   - Backfill capability
   - SLAs configurados
   - Alertas de retrasos

**Estructura esperada**:
```
proyecto-airflow-dbt/
├── airflow/
│   ├── dags/
│   │   └── main_pipeline.py
│   ├── plugins/
│   └── docker-compose.yml
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── tests/
│   ├── macros/
│   └── dbt_project.yml
├── great_expectations/
│   └── expectations/
├── tests/
└── README.md
```

**Criterios de éxito**:
- [ ] DAG ejecuta completamente sin errores
- [ ] dbt models bien estructurados y testeados
- [ ] Data quality checks implementados
- [ ] Idempotencia garantizada
- [ ] Backfills funcionan correctamente
- [ ] Alertas configuradas
- [ ] Documentación generada automáticamente
- [ ] Logs útiles y trackeables

---

### Proyecto 7.2: CI/CD para Data Pipelines

**Objetivo**: Implementar continuous integration y deployment para pipelines de datos.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. GitHub Actions Workflows:
   
   **PR Workflow** (on pull_request):
   - Linting (flake8, black, sqlfluff)
   - Unit tests (pytest)
   - dbt tests
   - Great Expectations validation
   - Terraform plan (infraestructura)
   
   **Deploy Workflow** (on push to main):
   - Deploy to dev environment
   - Run integration tests
   - Deploy to production (con aprobación manual)
   - Notificaciones

2. Testing Strategy:
   - Unit tests para funciones Python
   - Integration tests para pipelines completos
   - dbt tests para SQL
   - Schema tests
   - Data quality tests

3. Environments:
   - dev: despliegue automático
   - staging: para testing pre-prod
   - prod: con aprobación manual

4. Pre-commit Hooks:
   - Formateo automático (black)
   - Linting
   - Tests rápidos
   - Validación de secretos (no commits de API keys)

5. Rollback Strategy:
   - Versionado de dbt models
   - Blue-green deployment (si aplica)
   - Automated rollback en caso de fallo

**Estructura esperada**:
```
proyecto-cicd-pipelines/
├── .github/
│   └── workflows/
│       ├── pr_checks.yml
│       ├── deploy_dev.yml
│       └── deploy_prod.yml
├── .pre-commit-config.yaml
├── src/
├── tests/
│   ├── unit/
│   └── integration/
├── dbt/
├── terraform/
└── README.md
```

**Criterios de éxito**:
- [ ] CI ejecuta en cada PR automáticamente
- [ ] Tests previenen merges con errores
- [ ] Deploy a dev automático
- [ ] Deploy a prod requiere aprobación
- [ ] Pre-commit hooks funcionan
- [ ] Rollback strategy documentada
- [ ] Notificaciones de deploy

---

### Proyecto 7.3: Sistema de Monitoreo de Pipelines

**Objetivo**: Dashboard y alertas para monitorear salud de pipelines.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. Métricas a trackear:
   - Latencia de pipelines (tiempo de ejecución)
   - Throughput (registros procesados)
   - Tasa de error
   - Data freshness (última actualización)
   - SLA compliance

2. Stack:
   - Prometheus para métricas
   - Grafana para dashboards
   - Alertmanager para alertas
   - Exporters custom para pipelines

3. Instrumentación:
   - Airflow metrics
   - dbt run statistics
   - Custom metrics desde Python
   - Database metrics (rows processed)

4. Dashboards:
   - Overview de todos los pipelines
   - Detalle por pipeline
   - Alertas activas
   - Historical trends

5. Alertas:
   - Pipeline falló
   - Pipeline excede SLA
   - Data freshness alert
   - Disk space warnings
   - Integración con Slack/Email

**Criterios de éxito**:
- [ ] Métricas se recolectan automáticamente
- [ ] Dashboards visualizan estado de pipelines
- [ ] Alertas se disparan correctamente
- [ ] Integración con Slack funciona
- [ ] Historical data para análisis
- [ ] Documentación de setup

---

## Módulo 8: IA y Machine Learning

### Proyecto 8.1: Pipeline ML End-to-End con MLflow

**Objetivo**: Implementar pipeline ML completo desde training hasta producción.

**Duración estimada**: 4-5 semanas

**Requerimientos**:

1. Problema de negocio:
   - Predicción de churn de clientes
   - Clasificación binaria
   - Dataset: transacciones, comportamiento, demografía

2. Feature Engineering:
   - Crear features desde datos raw
   - Feature store con Feast
   - Transformaciones reproducibles
   - Train/test split temporal

3. Training Pipeline:
   - Multiple modelos (LogisticRegression, RandomForest, XGBoost)
   - Hyperparameter tuning
   - Cross-validation
   - MLflow tracking de experimentos

4. Model Registry:
   - Registrar modelos en MLflow
   - Versionado de modelos
   - Staging → Production promotion
   - Model metadata

5. Serving:
   - API REST con FastAPI
   - Endpoint de predicción
   - Batch predictions (Airflow job)
   - Dockerizar API

6. Monitoring:
   - Log de predictions
   - Model performance tracking
   - Data drift detection
   - Feature drift detection

**Estructura esperada**:
```
proyecto-ml-pipeline/
├── feature_engineering/
│   ├── create_features.py
│   └── feature_store/
├── training/
│   ├── train.py
│   ├── evaluate.py
│   └── hyperparameter_tuning.py
├── serving/
│   ├── api/
│   │   ├── main.py
│   │   └── Dockerfile
│   └── batch/
│       └── batch_predictions.py
├── monitoring/
│   └── drift_detection.py
├── mlflow/
│   └── docker-compose.yml
├── airflow/
│   └── dags/
│       ├── training_pipeline.py
│       └── inference_pipeline.py
└── README.md
```

**Criterios de éxito**:
- [ ] Pipeline entrenable end-to-end
- [ ] Experimentos trackeados en MLflow
- [ ] Modelo desplegado como API
- [ ] Batch predictions funcionan
- [ ] Monitoring de drift implementado
- [ ] Reproducibilidad garantizada
- [ ] Documentación completa

---

### Proyecto 8.2: Feature Store Empresarial

**Objetivo**: Implementar feature store para reutilización de features entre modelos.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Feast Setup:
   - Feature repository
   - Online store (Redis)
   - Offline store (PostgreSQL/Parquet)
   - Feature registry

2. Features a implementar:
   - User features (agregaciones de comportamiento)
   - Product features
   - Time-based features (rolling averages)
   - Real-time features (streaming)

3. Feature definitions:
   - Entities (user, product)
   - Feature views
   - Feature services
   - TTL y refresh policies

4. Pipelines:
   - Materialization jobs (offline → online)
   - Real-time feature computation
   - Orquestación con Airflow

5. Serving:
   - Online serving para predicciones real-time
   - Point-in-time correct joins para training
   - API de features

6. Monitoreo:
   - Freshness de features
   - Data quality de features
   - Usage analytics

**Criterios de éxito**:
- [ ] Features reutilizables entre proyectos
- [ ] Online/offline stores sincronizados
- [ ] Point-in-time joins correctos
- [ ] Features actualizadas automáticamente
- [ ] Documentación de cada feature
- [ ] Tests de features

---

### Proyecto 8.3: API de ML con FastAPI

**Objetivo**: Desplegar modelos ML como API REST profesional.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. FastAPI Application:
   - Endpoint `/predict` (single prediction)
   - Endpoint `/predict/batch` (multiple predictions)
   - Endpoint `/health` (healthcheck)
   - Endpoint `/metrics` (Prometheus metrics)

2. Features:
   - Input validation con Pydantic
   - Async support
   - Rate limiting
   - Authentication (API keys)
   - CORS configurado

3. Model Loading:
   - Lazy loading de modelo
   - Model caching en memoria
   - Soporte para múltiples modelos
   - Model versioning en API

4. Deployment:
   - Dockerizar aplicación
   - docker-compose con nginx
   - Kubernetes manifests (opcional)
   - CI/CD para deploy automático

5. Monitoring:
   - Logging de requests
   - Metrics (latency, throughput)
   - Error tracking
   - A/B testing capability (opcional)

**Estructura esperada**:
```
proyecto-ml-api/
├── app/
│   ├── main.py
│   ├── routers/
│   │   └── prediction.py
│   ├── models/
│   │   └── model_loader.py
│   ├── schemas/
│   │   └── request_response.py
│   └── middleware/
│       ├── auth.py
│       └── rate_limit.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── k8s/
│   └── deployment.yaml
└── README.md
```

**Criterios de éxito**:
- [ ] API responde en <100ms (p95)
- [ ] Validación de inputs robusta
- [ ] Rate limiting funciona
- [ ] Autenticación implementada
- [ ] Dockerizado y deployable
- [ ] Tests de integración pasan
- [ ] Documentación OpenAPI automática

---

### Proyecto 8.4: Sistema RAG (Retrieval Augmented Generation)

**Objetivo**: Chatbot que responde preguntas sobre documentación usando RAG.

**Duración estimada**: 4-5 semanas

**Requerimientos**:

1. Corpus de documentos:
   - Documentación técnica (Markdown, PDF)
   - >100 documentos
   - Múltiples temas/módulos

2. Ingesta y Procesamiento:
   - Document loaders (LangChain)
   - Text splitting (chunks de 500-1000 tokens)
   - Metadata extraction

3. Vector Database:
   - Embeddings con OpenAI/HuggingFace
   - Almacenar en Chroma/Pinecone
   - Indexing optimizado

4. Retrieval:
   - Similarity search
   - Semantic search
   - Hybrid search (keyword + semantic)
   - Re-ranking de resultados

5. Generation:
   - LLM: GPT-4, Claude, o Llama
   - Prompt engineering
   - Context injection
   - Source citation

6. Application:
   - Interfaz web con Streamlit
   - Chat history
   - Source highlighting
   - Feedback loop

7. Evaluation:
   - Retrieval metrics (precision, recall)
   - Answer quality (RAGAS framework)
   - Latency benchmarks

**Estructura esperada**:
```
proyecto-rag/
├── ingestion/
│   ├── document_loader.py
│   ├── chunker.py
│   └── embedder.py
├── retrieval/
│   ├── vector_store.py
│   ├── retriever.py
│   └── reranker.py
├── generation/
│   ├── llm_client.py
│   └── prompt_templates.py
├── app/
│   └── streamlit_app.py
├── evaluation/
│   └── eval_pipeline.py
├── data/
│   ├── raw_docs/
│   └── processed/
└── README.md
```

**Criterios de éxito**:
- [ ] Retrieval relevante (>80% precision@5)
- [ ] Respuestas coherentes y con fuentes
- [ ] Latencia <3 segundos end-to-end
- [ ] Interfaz funcional y usable
- [ ] Cita fuentes correctamente
- [ ] Cost-effective (optimizado API calls)
- [ ] Evaluation metrics documentados

---

### Proyecto 8.5: Data Quality con ML

**Objetivo**: Detección automática de anomalías en pipelines usando ML.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Anomaly Detection:
   - Isolation Forest para outliers
   - Statistical tests (Z-score)
   - Time series anomalies (Prophet)
   - Distribution shifts

2. Features para monitoreo:
   - Volume (row count changes)
   - Schema changes
   - Null rate changes
   - Value distribution shifts
   - Freshness anomalies

3. Training:
   - Historical data de pipelines
   - Labeled anomalies (si existen)
   - Unsupervised learning
   - Thresholds automáticos

4. Deployment:
   - Integración con pipelines de Airflow
   - Alertas automáticas de anomalías
   - Dashboard de anomalías detectadas
   - False positive feedback loop

5. Evaluation:
   - Precision/Recall de detección
   - False positive rate
   - Time to detection

**Criterios de éxito**:
- [ ] Detecta anomalías automáticamente
- [ ] Integrado con pipelines existentes
- [ ] False positive rate <10%
- [ ] Alertas accionables
- [ ] Dashboard de monitoreo
- [ ] Documentación de approach

---

## Módulo 9: DataOps, Calidad y Gobernanza

### Proyecto 9.1: Framework de Calidad Empresarial

**Objetivo**: Sistema completo de data quality con Great Expectations.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Great Expectations Setup:
   - Data Context configurado
   - Multiple Datasources (PostgreSQL, S3, Snowflake)
   - Expectation Suites organizadas
   - Validation Operators

2. Expectations a implementar:
   - Schema expectations (columns, types)
   - Table expectations (row count ranges)
   - Column expectations (nullity, uniqueness)
   - Multi-column expectations (relationships)
   - Custom expectations (business rules)

3. Validation Pipeline:
   - Pre-load validation
   - Post-load validation
   - Scheduled validations
   - Integración con Airflow

4. Data Docs:
   - Generación automática de documentación
   - Validation results history
   - Hosted en S3/static server

5. Alertas:
   - Notificaciones de validación fallida
   - Slack integration
   - Email alerts
   - Metrics para Prometheus

6. Profiling:
   - Auto-profiling de datasets nuevos
   - Generación automática de expectations
   - Statistical summaries

**Estructura esperada**:
```
proyecto-data-quality/
├── great_expectations/
│   ├── expectations/
│   │   ├── ventas_suite.json
│   │   ├── clientes_suite.json
│   │   └── productos_suite.json
│   ├── checkpoints/
│   ├── plugins/
│   │   └── custom_expectations.py
│   └── great_expectations.yml
├── airflow/
│   └── dags/
│       └── validation_pipeline.py
├── docs/
│   └── data_quality_standards.md
└── README.md
```

**Criterios de éxito**:
- [ ] Expectations completas y mantenibles
- [ ] Validaciones automáticas en pipelines
- [ ] Data Docs generadas y accesibles
- [ ] Alertas funcionando
- [ ] Custom expectations documentadas
- [ ] Tests para custom expectations

---

### Proyecto 9.2: Data Catalog con DataHub

**Objetivo**: Implementar catálogo de datos centralizado para discoverability.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. DataHub Setup:
   - Docker deployment
   - Backend (GMS, MAE, MCE)
   - Frontend UI
   - Metadata storage

2. Metadata Ingestion:
   - PostgreSQL databases
   - Snowflake/Redshift
   - dbt models
   - Airflow DAGs
   - S3 datasets

3. Metadata Enrichment:
   - Business glossary terms
   - Tags y clasificación
   - Ownership assignment
   - Documentation
   - Data quality scores

4. Data Lineage:
   - Table-level lineage
   - Column-level lineage (si posible)
   - Lineage desde dbt
   - Lineage desde Airflow

5. Search y Discovery:
   - Full-text search
   - Faceted search (por tags, owners)
   - Browse by domain
   - Related entities

6. Governance:
   - PII tagging
   - Sensitive data identification
   - Access policies documentation
   - Compliance tracking

**Estructura esperada**:
```
proyecto-data-catalog/
├── datahub/
│   ├── docker-compose.yml
│   └── ingestion/
│       ├── postgres_recipe.yml
│       ├── snowflake_recipe.yml
│       └── dbt_recipe.yml
├── scripts/
│   ├── enrich_metadata.py
│   └── bulk_tag.py
├── docs/
│   ├── glossary.md
│   └── tagging_standards.md
└── README.md
```

**Criterios de éxito**:
- [ ] Todos los data assets catalogados
- [ ] Lineage visible end-to-end
- [ ] Search funciona efectivamente
- [ ] Owners asignados a todos los assets
- [ ] Documentation completa
- [ ] PII data tagged
- [ ] Integración con dbt y Airflow

---

### Proyecto 9.3: Lineage Tracking con OpenLineage

**Objetivo**: Tracking automático de lineage en todos los pipelines.

**Duración estimada**: 2-3 semanas

**Requerimientos**:

1. OpenLineage Integration:
   - Airflow OpenLineage provider
   - dbt OpenLineage integration
   - Spark OpenLineage listener
   - Custom extractors para scripts Python

2. Lineage Backend:
   - Marquez backend
   - GraphQL API
   - Visualización de lineage

3. Captura de metadata:
   - Job runs
   - Datasets (inputs/outputs)
   - Transformations
   - Schema changes

4. Visualización:
   - Graph view de lineage
   - Impact analysis
   - Root cause analysis
   - Time-based lineage

**Criterios de éxito**:
- [ ] Lineage capturado automáticamente
- [ ] Visualización clara y navegable
- [ ] Impact analysis funciona
- [ ] Integration con Airflow completa
- [ ] Documentation de setup

---

### Proyecto 9.4: Seguridad y Compliance

**Objetivo**: Implementar controles de seguridad y compliance en plataforma de datos.

**Duración estimada**: 3-4 semanas

**Requerimientos**:

1. Data Classification:
   - PII identification (automated)
   - Sensitivity levels (public, internal, confidential)
   - Tagging system
   - Policy enforcement

2. Access Control:
   - RBAC implementation
   - Row-level security (RLS)
   - Column-level security
   - Dynamic data masking

3. Encryption:
   - At rest (database encryption)
   - In transit (TLS/SSL)
   - Key management (KMS)

4. Audit Logging:
   - Access logs
   - Change logs
   - Query logs
   - Export for SIEM

5. Compliance:
   - GDPR compliance checks
   - Data retention policies
   - Right to be forgotten (implementation)
   - Consent management

6. Security Testing:
   - Penetration testing scripts
   - SQL injection tests
   - Access control tests
   - Encryption validation

**Estructura esperada**:
```
proyecto-seguridad/
├── classification/
│   ├── pii_detector.py
│   └── tagger.py
├── access_control/
│   ├── rbac.sql
│   ├── rls_policies.sql
│   └── masking.sql
├── audit/
│   ├── logging_setup.py
│   └── audit_queries.sql
├── compliance/
│   ├── gdpr_compliance.py
│   └── retention_policies.sql
├── tests/
│   └── security_tests.py
├── docs/
│   ├── security_policies.md
│   └── compliance_checklist.md
└── README.md
```

**Criterios de éxito**:
- [ ] PII automatically detected y tagged
- [ ] RBAC implementado correctamente
- [ ] Encryption at rest y in transit
- [ ] Audit logs completos
- [ ] Compliance con GDPR validado
- [ ] Security tests pasan
- [ ] Documentation de políticas

---

## Módulo 10: Proyecto Final

### Opción 1: Plataforma de E-commerce Analytics

**Duración estimada**: 12-16 semanas

**Descripción completa**:

Sistema completo de analytics para e-commerce que procesa datos de múltiples fuentes, genera insights en tiempo real, y proporciona recomendaciones personalizadas.

**Componentes**:

1. **Ingesta de Datos**:
   - Web clickstream (eventos de navegación)
   - Transacciones de ventas (PostgreSQL)
   - Datos de productos (API REST)
   - Reviews de clientes (scraping o API)
   - Marketing campaigns data (CSV/API)

2. **Arquitectura**:
   - Data Lake en S3 (bronze/silver/gold)
   - Streaming con Kafka (eventos real-time)
   - Spark Streaming para procesamiento real-time
   - Data Warehouse en Snowflake (analytics)
   - Feature Store con Feast

3. **Procesamiento**:
   - Batch pipelines (Airflow + dbt)
   - Streaming pipelines (Kafka + Spark)
   - Real-time aggregations
   - Session analysis

4. **Analytics**:
   - RFM segmentation
   - Customer lifetime value
   - Churn prediction
   - Product recommendations (ML)
   - Market basket analysis

5. **ML/AI**:
   - Recommender system (collaborative filtering)
   - Price optimization model
   - Demand forecasting
   - Sentiment analysis de reviews
   - RAG chatbot para customer support

6. **Serving**:
   - FastAPI para recomendaciones
   - REST API para analytics
   - Real-time dashboard (Streamlit/Grafana)
   - BI layer (Tableau/PowerBI conectado a Snowflake)

7. **DataOps**:
   - CI/CD completo
   - Data quality monitoring
   - Data catalog (DataHub)
   - Lineage tracking
   - Alerting system

**Entregables**:

1. Código fuente completo en GitHub
2. IaC con Terraform
3. Documentación técnica exhaustiva
4. Diagramas de arquitectura
5. Presentación de resultados
6. Demo funcional
7. Runbooks operacionales

**KPIs del Proyecto**:
- Procesar >1M eventos/día en real-time
- Latencia de recomendaciones <200ms
- Precision@10 de recomendaciones >70%
- Data freshness <5 minutos
- Pipeline SLA >99%

---

### Opción 2: Plataforma de IoT y Smart Cities

**Duración estimada**: 12-16 semanas

**Descripción**:

Plataforma para ingestar, procesar y analizar datos de sensores IoT en tiempo real para aplicaciones de smart cities (tráfico, calidad del aire, gestión de residuos, etc.).

**Componentes**:

1. **Simulación de Sensores**:
   - Script para generar datos sintéticos de sensores
   - Múltiples tipos: temperatura, tráfico, contaminación
   - Frecuencia alta (segundos)

2. **Streaming Architecture**:
   - Kafka para ingesta
   - Spark Structured Streaming
   - Time-series database (InfluxDB/TimescaleDB)

3. **Processing**:
   - Aggregations en tiempo real
   - Anomaly detection (ML)
   - Alertas automáticas
   - Historical analysis

4. **ML/AI**:
   - Predictive maintenance de sensores
   - Traffic prediction
   - Air quality forecasting
   - Optimization algorithms (rutas, recursos)

5. **Visualization**:
   - Mapas geoespaciales (Folium, Mapbox)
   - Real-time dashboards
   - Alert system
   - Public API

6. **Scale**:
   - Kubernetes deployment
   - Auto-scaling
   - Multi-region (opcional)

---

### Opción 3: Plataforma de Social Media Analytics

**Duración estimada**: 12-16 semanas

**Descripción**:

Sistema para extraer, analizar y generar insights de datos de redes sociales usando NLP y LLMs.

**Componentes**:

1. **Data Collection**:
   - Twitter API (posts, trends)
   - Reddit API (subreddits)
   - Instagram/Facebook (si acceso disponible)
   - Web scraping (ético y legal)

2. **Processing**:
   - Text cleaning y preprocessing
   - NLP: sentiment analysis, entity extraction
   - Topic modeling
   - Trend detection

3. **Analytics**:
   - Trending topics
   - Influencer identification
   - Sentiment over time
   - Network analysis (social graphs)

4. **ML/AI**:
   - LLM-based content classification
   - Fake news detection
   - Viral prediction model
   - RAG Q&A sobre contenido

5. **Real-time**:
   - Streaming de posts nuevos
   - Real-time sentiment dashboard
   - Alert system para crisis

---

### Opción 4: Plataforma de Healthcare Analytics

**Duración estimada**: 12-16 semanas

**Descripción**:

Plataforma para análisis de datos de salud con énfasis en seguridad, compliance y privacidad.

**Componentes**:

1. **Data Sources**:
   - Electronic Health Records (simulados)
   - Wearables data
   - Lab results
   - Claims data

2. **Security & Compliance**:
   - HIPAA compliance
   - PHI de-identification
   - Encryption at rest/transit
   - Audit logging
   - Access controls estrictos

3. **Analytics**:
   - Patient risk scoring
   - Readmission prediction
   - Disease progression modeling
   - Population health analytics

4. **ML/AI**:
   - Predictive models para condiciones crónicas
   - Drug interaction checking
   - Clinical decision support
   - Medical image analysis (opcional)

5. **Governance**:
   - Data catalog con clasificación
   - Lineage completo
   - Retention policies
   - Consent management

---

## Conclusión

Este documento detalla todos los proyectos prácticos del Master. Cada proyecto ha sido diseñado para:

1. **Reforzar conocimientos** del módulo correspondiente
2. **Integrar conceptos** de módulos anteriores
3. **Simular situaciones reales** de la industria
4. **Construir un portafolio** profesional
5. **Preparar para el Proyecto Final**

### Recomendaciones Generales

- **No saltarse proyectos**: Cada uno construye sobre el anterior
- **Documentar todo**: El código sin documentación no sirve en producción
- **Tests primero**: Practicar TDD cuando sea aplicable
- **Code reviews**: Buscar feedback de peers o mentores
- **Refactorizar**: Mejorar proyectos anteriores con nuevos conocimientos

### Portafolio en GitHub

Todos los proyectos deben estar en GitHub con:
- README exhaustivo
- Código limpio y comentado
- Tests que pasen
- CI/CD configurado (desde módulo 7)
- Documentación de decisiones

**¡Los proyectos son la clave del aprendizaje! Dedícales tiempo y esfuerzo.**

