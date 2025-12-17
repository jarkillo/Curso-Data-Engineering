# 🔧 Proyecto Práctico: Analytics de Salud con GCP

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Contexto del Proyecto](#contexto-del-proyecto)
3. [Arquitectura](#arquitectura)
4. [Funciones Implementadas](#funciones-implementadas)
5. [Instalación y Setup](#instalación-y-setup)
6. [Ejecución](#ejecución)
7. [Tests](#tests)
8. [Estructura del Proyecto](#estructura-del-proyecto)

---

## Introducción

Este proyecto implementa un **sistema completo de analytics de salud** usando servicios de Google Cloud Platform (GCP). El objetivo es demostrar cómo construir pipelines de datos en la nube utilizando:

- ✅ **Cloud Storage**: Para almacenar archivos de pacientes
- ✅ **BigQuery**: Para análisis de datos y queries SQL
- ✅ **Dataflow (Apache Beam)**: Para procesamiento ETL
- ✅ **Pub/Sub**: Para ingesta en tiempo real
- ✅ **Cloud Functions**: Para automatización (simulado)

El proyecto sigue **Test-Driven Development (TDD)** con >80% de cobertura de tests.

---

## Contexto del Proyecto

### Empresa Ficticia: HealthTech Analytics Inc.

**HealthTech Analytics Inc.** es una startup que ayuda a hospitales y clínicas a analizar datos de pacientes para mejorar la calidad de atención médica.

### Desafío de Negocio

Los hospitales generan miles de registros diarios:
- **Registros de pacientes**: Admisiones, diagnósticos, tratamientos
- **Consultas médicas**: Historial de visitas, prescripciones
- **Eventos de monitoreo**: Signos vitales, alertas médicas

**Problema**: Los datos están dispersos en archivos CSV, necesitan:
1. **Centralización**: Todos los datos en un data warehouse
2. **Análisis en tiempo real**: Detectar pacientes de alto riesgo
3. **Reportes automatizados**: KPIs diarios para directores médicos

### Solución Técnica

Construir un **pipeline de datos en GCP** que:
1. Almacene archivos CSV en Cloud Storage
2. Procese datos con Dataflow (limpiar, validar, enriquecer)
3. Cargue en BigQuery para análisis
4. Detecte eventos críticos con Pub/Sub
5. Genere alertas automáticas

---

## Arquitectura

### Diagrama General

```
┌─────────────────────────────────────────────────────────────────┐
│                      HEALTHTECH ANALYTICS                        │
│                   Pipeline de Datos en GCP                       │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │  Hospitales      │
                    │  (CSVs diarios)  │
                    └────────┬─────────┘
                             │
                             v
                    ┌──────────────────┐
                    │  Cloud Storage   │ ← CAPA 1: ALMACENAMIENTO
                    │  (Data Lake)     │
                    └────────┬─────────┘
                             │
                             v
                    ┌──────────────────┐
                    │  Dataflow        │ ← CAPA 2: PROCESAMIENTO
                    │  (ETL con Beam)  │
                    └────────┬─────────┘
                             │
                 ┌───────────┴───────────┐
                 v                       v
        ┌────────────────┐      ┌───────────────┐
        │   BigQuery     │      │   Pub/Sub     │ ← CAPA 3: ANALYTICS
        │ (Data Warehouse)│      │  (Eventos)    │
        └────────┬───────┘      └───────┬───────┘
                 │                       │
                 v                       v
        ┌────────────────┐      ┌───────────────┐
        │  Dashboards    │      │   Alertas     │ ← CAPA 4: CONSUMO
        │  (BI Tools)    │      │  (Emails)     │
        └────────────────┘      └───────────────┘
```

### Flujo de Datos Detallado

```
1. INGESTA:
   Hospital → CSV → Cloud Storage (gs://healthtech-data/raw/YYYY-MM-DD/pacientes_*.csv)

2. PROCESAMIENTO (Dataflow):
   - Leer CSV desde Cloud Storage
   - Validar datos (nulls, formatos)
   - Limpiar (normalizar timestamps, categorizar)
   - Enriquecer (calcular edad desde fecha de nacimiento, categoría de riesgo)
   - Filtrar registros inválidos

3. ALMACENAMIENTO:
   - Datos limpios → BigQuery (tabla: healthtech.pacientes)
   - Datos inválidos → Cloud Storage (gs://healthtech-data/invalid/)

4. ANÁLISIS (BigQuery):
   - Queries SQL para KPIs (pacientes por diagnóstico, edad promedio, etc.)
   - Agregaciones por fecha, hospital, diagnóstico

5. EVENTOS CRÍTICOS (Pub/Sub):
   - Detectar pacientes de alto riesgo
   - Publicar evento a topic: healthtech-alerts
   - Consumir evento → Enviar email/SMS

6. AUTOMATIZACIÓN:
   - Schedule diario en Cloud Functions (simulated)
   - Trigger: Nuevos archivos en Cloud Storage → Iniciar Dataflow job
```

---

## Funciones Implementadas

El proyecto está organizado en **6 módulos principales** con funciones pequeñas y testeables.

### Módulo 1: `storage_operations.py` (Cloud Storage)

Funciones para gestionar archivos en Cloud Storage.

**Funciones**:
1. `subir_archivo_a_gcs(bucket_name: str, archivo_local: str, ruta_destino: str) -> str`
   - Sube un archivo local a Cloud Storage
   - Configura metadata (tipo, fecha_subida)
   - Retorna URI del archivo (gs://...)

2. `descargar_archivo_desde_gcs(uri: str, archivo_local: str) -> None`
   - Descarga un archivo desde GCS
   - Parsea URI para extraer bucket y path

3. `listar_archivos_por_prefijo(bucket_name: str, prefijo: str) -> list[str]`
   - Lista archivos que coincidan con un prefijo
   - Ejemplo: `prefijo="raw/pacientes/2025-01-15/"` lista todos los CSVs del 15 de enero

4. `eliminar_archivo_gcs(uri: str) -> None`
   - Elimina un archivo de Cloud Storage

**Cobertura esperada**: >90%

---

### Módulo 2: `validation.py` (Validación de Datos)

Funciones para validar registros de pacientes.

**Funciones**:
1. `validar_paciente_id(paciente_id: str) -> tuple[bool, str]`
   - Valida formato de ID (ej: "P001")
   - Retorna (es_valido, mensaje_error)

2. `validar_edad(edad: Any) -> tuple[bool, str]`
   - Valida que edad sea int >= 0

3. `validar_diagnostico(diagnostico: str) -> tuple[bool, str]`
   - Valida que diagnóstico no esté vacío

4. `validar_fecha_nacimiento(fecha_str: str) -> tuple[bool, str]`
   - Valida formato YYYY-MM-DD
   - Valida que fecha no sea futura

5. `validar_registro_completo(registro: dict) -> tuple[bool, str]`
   - Valida que tenga todos los campos requeridos
   - Llama a validadores específicos
   - Retorna (es_valido, mensaje_error)

**Cobertura esperada**: >95%

---

### Módulo 3: `transformations.py` (Transformaciones ETL)

Funciones para limpiar y transformar datos.

**Funciones**:
1. `limpiar_nulls(datos: list[dict]) -> list[dict]`
   - Elimina registros con nulls en campos críticos

2. `normalizar_fechas(datos: list[dict]) -> list[dict]`
   - Normaliza fechas a formato ISO 8601 (YYYY-MM-DD)

3. `calcular_edad_desde_fecha_nacimiento(fecha_nacimiento: str) -> int`
   - Calcula edad actual desde fecha de nacimiento

4. `categorizar_por_edad(edad: int) -> str`
   - Categoriza paciente: "niño" (<18), "adulto" (18-64), "mayor" (65+)

5. `categorizar_nivel_riesgo(registro: dict) -> str`
   - Categoriza riesgo: "bajo", "medio", "alto"
   - Basado en edad, diagnóstico, signos vitales

6. `enriquecer_registro(registro: dict) -> dict`
   - Agrega campos calculados (edad, categoría, riesgo)
   - Agrega timestamp de procesamiento

**Cobertura esperada**: >90%

---

### Módulo 4: `bigquery_operations.py` (BigQuery)

Funciones para interactuar con BigQuery.

**Funciones**:
1. `crear_dataset(project_id: str, dataset_id: str, location: str = "US") -> bigquery.Dataset`
   - Crea un dataset en BigQuery

2. `crear_tabla_pacientes(project_id: str, dataset_id: str, tabla_id: str) -> bigquery.Table`
   - Crea tabla particionada para pacientes
   - Schema: paciente_id, nombre, edad, diagnostico, fecha_registro, etc.

3. `cargar_datos_desde_lista(project_id: str, dataset_id: str, tabla_id: str, datos: list[dict]) -> int`
   - Carga datos desde lista de diccionarios a BigQuery
   - Retorna número de filas insertadas

4. `ejecutar_query(project_id: str, query: str) -> list[dict]`
   - Ejecuta query SQL y retorna resultados como lista de dicts

5. `obtener_distribucion_diagnosticos(project_id: str, dataset_id: str, tabla_id: str) -> list[dict]`
   - Query pre-construida para distribución de diagnósticos
   - Retorna: [{diagnostico, total, porcentaje}, ...]

6. `obtener_estadisticas_por_edad(project_id: str, dataset_id: str, tabla_id: str) -> list[dict]`
   - Query pre-construida para estadísticas por rango de edad
   - Retorna: [{rango_edad, total_pacientes, diagnostico_mas_comun}, ...]

**Cobertura esperada**: >85% (algunas funciones requieren BigQuery real)

---

### Módulo 5: `pubsub_operations.py` (Pub/Sub)

Funciones para mensajería con Pub/Sub.

**Funciones**:
1. `crear_topic(project_id: str, topic_id: str) -> str`
   - Crea un topic en Pub/Sub
   - Retorna nombre completo del topic

2. `crear_subscription(project_id: str, topic_id: str, subscription_id: str) -> str`
   - Crea una subscription para consumir mensajes

3. `publicar_evento(project_id: str, topic_id: str, evento: dict) -> str`
   - Publica un evento (dict) a Pub/Sub
   - Serializa a JSON
   - Retorna message_id

4. `publicar_alerta_paciente_riesgo(project_id: str, topic_id: str, paciente: dict) -> str`
   - Función específica para alertas de pacientes de alto riesgo
   - Formato estandarizado: {tipo_evento, paciente_id, nivel_riesgo, timestamp}

5. `consumir_mensajes_simulado(mensajes: list[bytes]) -> list[dict]`
   - Simula consumo de mensajes (para testing sin Pub/Sub real)
   - Parsea JSON y retorna lista de eventos

**Cobertura esperada**: >85%

---

### Módulo 6: `beam_pipelines.py` (Dataflow con Apache Beam)

DoFns y funciones para pipelines Dataflow.

**DoFns (Beam Transforms)**:
1. `ParsearCSV(beam.DoFn)`
   - Parsea líneas CSV a diccionarios

2. `ValidarRegistro(beam.DoFn)`
   - Valida registros usando funciones de `validation.py`
   - Descarta inválidos

3. `EnriquecerRegistro(beam.DoFn)`
   - Enriquece registros usando funciones de `transformations.py`

4. `DetectarPacientesAltoRiesgo(beam.DoFn)`
   - Filtra pacientes de alto riesgo
   - Para publicar a Pub/Sub

5. `CalcularMetricasPorDiagnostico(beam.DoFn)`
   - Agrega métricas por diagnóstico (count, edad promedio, etc.)

**Funciones**:
1. `crear_pipeline_batch(input_path: str, output_table: str, project_id: str) -> beam.Pipeline`
   - Crea pipeline batch completo
   - Lee CSV → Valida → Enriquece → Escribe a BigQuery

2. `crear_pipeline_streaming(subscription_id: str, output_table: str, project_id: str) -> beam.Pipeline`
   - Crea pipeline streaming
   - Lee Pub/Sub → Procesa → Escribe a BigQuery

**Cobertura esperada**: >80% (DoFns son altamente testeables)

---

## Instalación y Setup

### Requisitos

- **Python**: 3.9+
- **Cuenta GCP**: Con proyecto creado
- **SDK de Google Cloud**: `gcloud` CLI instalado
- **Librerías Python**:
  ```
  google-cloud-storage==2.10.0
  google-cloud-bigquery==3.11.0
  google-cloud-pubsub==2.18.0
  apache-beam[gcp]==2.50.0
  pytest==7.4.0
  pytest-cov==4.1.0
  ```

### Paso 1: Clonar Repositorio

```bash
cd "E:\Curso Data Engineering\modulo-07-cloud\tema-2-gcp\04-proyecto-practico"
```

### Paso 2: Crear Entorno Virtual

```bash
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Credenciales de GCP

**Opción 1: Usar cuenta personal**
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

**Opción 2: Usar Service Account (producción)**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### Paso 5: Crear Recursos en GCP

```bash
# Crear bucket
gsutil mb -l us-central1 gs://healthtech-data-YOUR_PROJECT_ID

# Crear dataset en BigQuery
bq mk --location=US healthtech_analytics
```

### Paso 6: Configurar Variables de Entorno

Crear archivo `.env`:
```bash
PROJECT_ID=your-project-id
BUCKET_NAME=healthtech-data-your-project-id
DATASET_ID=healthtech_analytics
LOCATION=us-central1
```

---

## Ejecución

### Ejemplo 1: Subir CSV a Cloud Storage

```bash
python -m src.examples.example_01_storage
```

**Código** (`src/examples/example_01_storage.py`):
```python
from src.storage_operations import subir_archivo_a_gcs

uri = subir_archivo_a_gcs(
    bucket_name="healthtech-data-myproject",
    archivo_local="data/pacientes_sample.csv",
    ruta_destino="raw/pacientes/2025-01-15/pacientes.csv"
)

print(f"✅ Archivo subido: {uri}")
```

---

### Ejemplo 2: Procesar CSV con Validación

```bash
python -m src.examples.example_02_validation
```

**Código**:
```python
from src.validation import validar_registro_completo

registro = {
    "paciente_id": "P001",
    "nombre": "Juan Pérez",
    "edad": 45,
    "diagnostico": "Diabetes"
}

es_valido, error = validar_registro_completo(registro)

if es_valido:
    print("✅ Registro válido")
else:
    print(f"❌ Error: {error}")
```

---

### Ejemplo 3: Cargar Datos a BigQuery

```bash
python -m src.examples.example_03_bigquery
```

**Código**:
```python
from src.bigquery_operations import cargar_datos_desde_lista

datos = [
    {"paciente_id": "P001", "nombre": "Juan Pérez", "edad": 45, "diagnostico": "Diabetes", "fecha_registro": "2025-01-15"},
    {"paciente_id": "P002", "nombre": "María García", "edad": 32, "diagnostico": "Hipertensión", "fecha_registro": "2025-01-15"}
]

filas_insertadas = cargar_datos_desde_lista(
    project_id="healthtech-prod",
    dataset_id="healthtech_analytics",
    tabla_id="pacientes",
    datos=datos
)

print(f"✅ {filas_insertadas} filas insertadas en BigQuery")
```

---

### Ejemplo 4: Pipeline Dataflow (Batch Local)

```bash
python -m src.examples.example_04_dataflow_batch
```

**Código**:
```python
from src.beam_pipelines import crear_pipeline_batch

pipeline = crear_pipeline_batch(
    input_path="data/pacientes_*.csv",
    output_table="healthtech-prod:healthtech_analytics.pacientes",
    project_id="healthtech-prod"
)

# Ejecutar localmente (DirectRunner)
pipeline.run().wait_until_finish()
```

---

### Ejemplo 5: Publicar Alertas a Pub/Sub

```bash
python -m src.examples.example_05_pubsub
```

**Código**:
```python
from src.pubsub_operations import publicar_alerta_paciente_riesgo

paciente = {
    "paciente_id": "P001",
    "nombre": "Juan Pérez",
    "edad": 68,
    "diagnostico": "Diabetes",
    "nivel_riesgo": "alto"
}

message_id = publicar_alerta_paciente_riesgo(
    project_id="healthtech-prod",
    topic_id="healthtech-alerts",
    paciente=paciente
)

print(f"✅ Alerta publicada: {message_id}")
```

---

## Tests

### Ejecutar Todos los Tests

```bash
pytest tests/ -v
```

### Ejecutar con Cobertura

```bash
pytest tests/ --cov=src --cov-report=html
```

Luego abre `htmlcov/index.html` en tu navegador para ver el reporte detallado.

### Ejecutar Tests de un Módulo Específico

```bash
pytest tests/test_validation.py -v
pytest tests/test_bigquery_operations.py -v
```

### Estructura de Tests

```
tests/
├── test_storage_operations.py      (25 tests)
├── test_validation.py               (30 tests)
├── test_transformations.py          (20 tests)
├── test_bigquery_operations.py      (15 tests, algunos mocked)
├── test_pubsub_operations.py        (15 tests, algunos mocked)
└── test_beam_pipelines.py           (20 tests, con TestPipeline)
```

**Total**: ~125 tests

---

## Estructura del Proyecto

```
04-proyecto-practico/
│
├── src/
│   ├── __init__.py
│   ├── storage_operations.py       (4 funciones, ~150 líneas)
│   ├── validation.py                (5 funciones, ~200 líneas)
│   ├── transformations.py           (6 funciones, ~250 líneas)
│   ├── bigquery_operations.py       (6 funciones, ~300 líneas)
│   ├── pubsub_operations.py         (5 funciones, ~200 líneas)
│   └── beam_pipelines.py            (5 DoFns + 2 funciones, ~400 líneas)
│
├── tests/
│   ├── __init__.py
│   ├── test_storage_operations.py   (~400 líneas)
│   ├── test_validation.py           (~500 líneas)
│   ├── test_transformations.py      (~350 líneas)
│   ├── test_bigquery_operations.py  (~300 líneas)
│   ├── test_pubsub_operations.py    (~300 líneas)
│   └── test_beam_pipelines.py       (~400 líneas)
│
├── data/
│   ├── pacientes_sample.csv         (datos de prueba)
│   └── pacientes_invalid.csv        (datos inválidos para testing)
│
├── examples/
│   ├── example_01_storage.py
│   ├── example_02_validation.py
│   ├── example_03_bigquery.py
│   ├── example_04_dataflow_batch.py
│   └── example_05_pubsub.py
│
├── .env.example                     (template de configuración)
├── requirements.txt                 (dependencias Python)
├── pytest.ini                       (configuración de pytest)
├── .gitignore
└── README.md                        (este archivo)
```

---

## Conceptos Clave Aplicados

### 1. Test-Driven Development (TDD)

Todos los módulos siguen el ciclo **Red → Green → Refactor**:
1. Escribir test que falla
2. Implementar código mínimo para que pase
3. Refactorizar manteniendo tests verdes

### 2. Programación Funcional

- Funciones puras (sin efectos colaterales)
- No modifican parámetros de entrada
- Retornan nuevos objetos

### 3. Tipado Explícito

Todas las funciones tienen type hints:
```python
def validar_edad(edad: Any) -> tuple[bool, str]:
    ...
```

### 4. Docstrings con Ejemplos

Todas las funciones tienen docstrings con:
- Descripción
- Args
- Returns
- Raises
- Examples (doctests)

### 5. Manejo de Errores Explícito

Funciones de validación retornan tuplas `(bool, str)`:
```python
es_valido, mensaje_error = validar_registro_completo(registro)
```

### 6. Testing con Mocks

Para servicios externos (BigQuery, Pub/Sub), usamos mocks:
```python
@patch('google.cloud.bigquery.Client')
def test_crear_dataset(mock_client):
    ...
```

---

## Próximos Pasos

1. **Implementar funciones faltantes** (stubs actuales)
2. **Alcanzar >90% de cobertura** en todos los módulos
3. **Deploy a GCP**: Ejecutar pipeline en Dataflow real
4. **Añadir Cloud Composer**: Orquestar con Airflow
5. **Monitoreo**: Logs, métricas, alertas

---

## Recursos Adicionales

- [Google Cloud Storage Docs](https://cloud.google.com/storage/docs)
- [BigQuery Docs](https://cloud.google.com/bigquery/docs)
- [Apache Beam Docs](https://beam.apache.org/documentation/)
- [Pub/Sub Docs](https://cloud.google.com/pubsub/docs)
- [Testing with pytest](https://docs.pytest.org/)

---

*Última actualización: 2025-01-15*
*Proyecto construido con 💙 siguiendo TDD y mejores prácticas de Data Engineering*
---

## 🧭 Navegación

⬅️ **Anterior**: [03 Ejercicios](../03-EJERCICIOS.md) | ➡️ **Siguiente**: [Infrastructure as Code - 01 Teoria](../../tema-3-iac/01-TEORIA.md)
