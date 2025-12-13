# MLOps y Productivización de Modelos

## Introducción

Has construido un modelo de Machine Learning que predice con precisión. ¡Felicidades! Pero ahora viene la pregunta del millón: **¿cómo lo ponemos a funcionar en el mundo real?**

Imagina que eres un chef que ha creado una receta perfecta en su cocina de pruebas. MLOps es todo lo que necesitas para convertir esa receta en un restaurante funcionando: la cocina industrial, los procesos de compra de ingredientes, el control de calidad, los turnos del personal, y la capacidad de servir miles de platos manteniendo la misma calidad.

### ¿Por qué es esto importante para un Data Engineer?

Como Data Engineer, serás el puente entre los científicos de datos que crean modelos y los sistemas de producción que los ejecutan. Necesitas entender:

- **Cómo empaquetar modelos** para que funcionen fuera de un notebook
- **Cómo servir predicciones** a aplicaciones y usuarios
- **Cómo monitorear** que el modelo sigue funcionando correctamente
- **Cómo actualizar modelos** sin interrumpir el servicio

---

## Conceptos Fundamentales

### ¿Qué es MLOps?

**MLOps** (Machine Learning Operations) es la práctica de aplicar principios de DevOps al ciclo de vida de Machine Learning. Es la disciplina que permite llevar modelos desde el experimento hasta producción de forma confiable y reproducible.

**Analogía del restaurante:**
- **ML tradicional** = Chef cocinando solo en su casa
- **MLOps** = Restaurante con cocina industrial, procesos estandarizados, control de calidad

### El Ciclo de Vida MLOps

```
┌─────────────────────────────────────────────────────────────────┐
│                     CICLO DE VIDA MLOPS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Datos   │───▶│ Entrena- │───▶│ Despliegue│───▶│ Monitoreo│  │
│  │          │    │  miento  │    │           │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │                                               │         │
│       │                                               │         │
│       └───────────── Retroalimentación ◀─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Las 4 fases:**

1. **Datos**: Recolección, validación, versionado de datos
2. **Entrenamiento**: Experimentos, selección de modelo, validación
3. **Despliegue**: Empaquetado, servicio, integración
4. **Monitoreo**: Rendimiento, drift, alertas

---

## Niveles de Madurez MLOps

No todas las organizaciones necesitan el mismo nivel de automatización. Hay tres niveles de madurez:

### Nivel 0: Manual

```
Científico de Datos → Notebook → Modelo.pkl → "Aquí tienes el archivo"
```

**Características:**
- Todo se hace manualmente
- Los modelos se pasan por email o carpetas compartidas
- No hay reproducibilidad
- No hay monitoreo

**Cuándo es apropiado:**
- Pruebas de concepto
- Proyectos pequeños con pocas predicciones
- Modelos que rara vez cambian

### Nivel 1: Pipeline Automatizado

```
Datos → Pipeline Automático → Modelo → Despliegue Manual
```

**Características:**
- Entrenamiento automatizado
- Versionado de modelos
- Tests automáticos
- Despliegue todavía requiere intervención

**Cuándo es apropiado:**
- Equipos pequeños-medianos
- Modelos que se reentrenan mensualmente
- Cuando necesitas reproducibilidad

### Nivel 2: CI/CD Completo

```
Cambio en Datos/Código → Pipeline → Tests → Despliegue Automático → Monitoreo
```

**Características:**
- Todo automatizado
- Despliegue continuo
- Rollback automático si hay problemas
- Reentrenamiento automático

**Cuándo es apropiado:**
- Equipos grandes
- Modelos críticos para el negocio
- Modelos que necesitan actualizarse frecuentemente

---

## Versionado de Modelos

### ¿Por qué versionar modelos?

Imagina que despliegas un modelo nuevo y las predicciones empiezan a fallar. ¿Cómo vuelves a la versión anterior? Sin versionado, estás perdido.

### Elementos a Versionar

```
┌─────────────────────────────────────────────────────────────────┐
│                 ¿QUÉ VERSIONAR EN ML?                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CÓDIGO              2. DATOS                3. MODELO       │
│  ├── train.py           ├── train_v1.csv       ├── model_v1.pkl│
│  ├── preprocess.py      ├── train_v2.csv       ├── model_v2.pkl│
│  └── evaluate.py        └── features.parquet   └── metrics.json│
│                                                                 │
│  4. CONFIGURACIÓN       5. AMBIENTE                             │
│  ├── hyperparams.yaml   ├── requirements.txt                   │
│  └── features.yaml      └── Dockerfile                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Herramientas de Versionado

| Herramienta | Qué versiona | Analogía |
|-------------|--------------|----------|
| **Git** | Código | Historial de recetas escritas |
| **DVC** | Datos grandes | Historial de ingredientes |
| **MLflow** | Experimentos y modelos | Libro de cocina con resultados |
| **Docker** | Ambiente | La cocina completa empaquetada |

---

## Empaquetado de Modelos

### El Problema del "Funciona en mi Máquina"

```python
# En el notebook del científico de datos:
import pandas as pd  # versión 1.5.3
model = load("modelo.pkl")  # sklearn 1.2.0
prediction = model.predict(data)  # ¡Funciona!

# En producción:
import pandas as pd  # versión 2.0.0 - ¡INCOMPATIBLE!
model = load("modelo.pkl")  # ¡ERROR!
```

### Solución: Contenedores Docker

**Analogía:** Un contenedor es como una caja de mudanza que contiene todo lo necesario para que tu modelo funcione: el código, las librerías, las configuraciones.

```dockerfile
# Dockerfile para un modelo de ML
FROM python:3.11-slim

# Copiar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar código y modelo
COPY src/ /app/src/
COPY models/model.pkl /app/models/

# Exponer puerto para la API
EXPOSE 8000

# Comando para iniciar
CMD ["python", "-m", "uvicorn", "src.api:app", "--host", "0.0.0.0"]
```

### requirements.txt Fijado

```txt
# ❌ MAL: Versiones no especificadas
pandas
scikit-learn
numpy

# ✅ BIEN: Versiones exactas
pandas==2.0.3
scikit-learn==1.3.0
numpy==1.24.3
```

---

## Servir Modelos: APIs de Predicción

### ¿Por qué una API?

Tu modelo necesita recibir datos y devolver predicciones. Una API REST es la forma estándar de hacerlo.

**Analogía:** La API es como la ventanilla de un restaurante de comida rápida. El cliente (aplicación) hace un pedido (datos), la cocina (modelo) lo procesa, y devuelve el resultado (predicción).

### Patrones de Servicio

#### 1. Predicción Síncrona (Tiempo Real)

```
Cliente → API → Modelo → Respuesta inmediata
         ↓
    ~50-200ms
```

**Uso:** Recomendaciones en tiempo real, detección de fraude

```python
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("model.pkl")

@app.post("/predict")
def predict(data: dict):
    """Predicción en tiempo real."""
    prediction = model.predict([data["features"]])[0]
    return {"prediction": prediction}
```

#### 2. Predicción Asíncrona (Batch)

```
Cliente → Cola de Mensajes → Worker → Base de Datos
    ↓                                      ↓
"Tu trabajo está en cola"        "Resultados listos"
```

**Uso:** Procesamiento masivo, predicciones no urgentes

#### 3. Predicción en Streaming

```
Flujo de Datos → Modelo en Streaming → Flujo de Predicciones
```

**Uso:** Detección de anomalías en tiempo real, IoT

### Estructura de una API de ML

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="API de Predicción ML")

# Cargar modelo al iniciar
model = None

@app.on_event("startup")
def load_model():
    """Cargar modelo al iniciar la aplicación."""
    global model
    model = joblib.load("models/model.pkl")

# Esquema de entrada
class PredictionRequest(BaseModel):
    feature_1: float
    feature_2: float
    category: str

# Esquema de salida
class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """Realizar predicción."""
    try:
        # Preparar datos
        features = np.array([[
            request.feature_1,
            request.feature_2
        ]])

        # Predecir
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].max()

        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            model_version="1.0.0"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    """Verificar que el servicio está funcionando."""
    return {"status": "healthy", "model_loaded": model is not None}
```

---

## Monitoreo de Modelos en Producción

### ¿Por qué Monitorear?

Un modelo que funcionaba perfectamente puede degradarse con el tiempo. Las razones:

1. **Data Drift**: Los datos de entrada cambian
2. **Concept Drift**: La relación entrada-salida cambia
3. **Errores técnicos**: Fallos de infraestructura

**Analogía del GPS:** Tu GPS funcionaba perfecto hace 5 años, pero ahora algunas calles han cambiado. Sin actualizaciones, te lleva por rutas incorrectas.

### Tipos de Monitoreo

```
┌─────────────────────────────────────────────────────────────────┐
│                   MONITOREO EN MLOPS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. INFRAESTRUCTURA        2. MODELO                           │
│  ├── Latencia              ├── Accuracy en producción          │
│  ├── Errores               ├── Distribución de predicciones    │
│  ├── CPU/Memoria           └── Confianza promedio              │
│  └── Disponibilidad                                            │
│                                                                 │
│  3. DATOS                  4. NEGOCIO                          │
│  ├── Data drift            ├── Conversiones                    │
│  ├── Schema changes        ├── Revenue impact                  │
│  └── Missing values        └── User satisfaction               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Drift: Cuando los Datos Cambian

**Data Drift** ocurre cuando la distribución de los datos de entrada cambia respecto a los datos de entrenamiento.

```python
import numpy as np
from scipy import stats

def detect_drift_ks(reference: np.ndarray, current: np.ndarray,
                    threshold: float = 0.05) -> dict:
    """
    Detectar drift usando el test de Kolmogorov-Smirnov.

    Args:
        reference: Datos de referencia (entrenamiento)
        current: Datos actuales (producción)
        threshold: Umbral de p-value para detectar drift

    Returns:
        Diccionario con estadístico, p-value y si hay drift
    """
    statistic, p_value = stats.ks_2samp(reference, current)

    return {
        "statistic": statistic,
        "p_value": p_value,
        "drift_detected": p_value < threshold
    }

# Ejemplo
reference_ages = np.array([25, 30, 35, 28, 32, 29, 31, 27])
production_ages = np.array([45, 50, 48, 52, 47, 55, 49, 51])  # ¡Población más vieja!

result = detect_drift_ks(reference_ages, production_ages)
print(f"Drift detectado: {result['drift_detected']}")  # True
```

### Métricas de Monitoreo Esenciales

| Métrica | Qué mide | Alerta cuando |
|---------|----------|---------------|
| **Latencia P99** | Tiempo de respuesta | > 500ms |
| **Tasa de errores** | Predicciones fallidas | > 1% |
| **Prediction drift** | Cambio en distribución de predicciones | Desviación significativa |
| **Feature drift** | Cambio en distribución de features | p-value < 0.05 |
| **Confianza promedio** | Certeza del modelo | Caída > 10% |

---

## Reentrenamiento de Modelos

### ¿Cuándo Reentrenar?

```
┌─────────────────────────────────────────────────────────────────┐
│              TRIGGERS DE REENTRENAMIENTO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PROGRAMADO              2. POR RENDIMIENTO                  │
│  ├── Cada semana            ├── Accuracy < umbral               │
│  ├── Cada mes               ├── Drift detectado                 │
│  └── Cada X nuevos datos    └── Métricas de negocio caen        │
│                                                                 │
│  3. MANUAL                  4. POR EVENTO                       │
│  ├── Nuevo feature          ├── Cambio en el negocio            │
│  ├── Bug corregido          ├── Nueva fuente de datos           │
│  └── Experimento            └── Regulación nueva                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline de Reentrenamiento

```python
def retraining_pipeline(
    new_data_path: str,
    model_registry: str,
    performance_threshold: float = 0.85
) -> dict:
    """
    Pipeline de reentrenamiento automático.

    Args:
        new_data_path: Ruta a los nuevos datos
        model_registry: Ruta al registro de modelos
        performance_threshold: Umbral mínimo de rendimiento

    Returns:
        Resultado del reentrenamiento
    """
    # 1. Cargar datos nuevos
    new_data = load_data(new_data_path)

    # 2. Cargar modelo actual
    current_model = load_model(f"{model_registry}/production/model.pkl")

    # 3. Evaluar modelo actual con datos nuevos
    current_score = evaluate(current_model, new_data)

    # 4. Si rendimiento es aceptable, no reentrenar
    if current_score >= performance_threshold:
        return {
            "action": "no_retrain",
            "current_score": current_score,
            "reason": "Rendimiento aceptable"
        }

    # 5. Reentrenar con datos combinados
    combined_data = combine_with_historical(new_data)
    new_model = train_model(combined_data)
    new_score = evaluate(new_model, new_data)

    # 6. Solo desplegar si mejora
    if new_score > current_score:
        save_model(new_model, f"{model_registry}/staging/model.pkl")
        return {
            "action": "retrain_success",
            "old_score": current_score,
            "new_score": new_score,
            "improvement": new_score - current_score
        }

    return {
        "action": "retrain_no_improvement",
        "reason": "Nuevo modelo no mejora"
    }
```

---

## Registro de Modelos (Model Registry)

### ¿Qué es un Model Registry?

Un **Model Registry** es un repositorio centralizado para gestionar modelos de ML. Es como un almacén organizado donde cada modelo tiene su etiqueta, versión y documentación.

### Estructura Típica

```
model_registry/
├── churn_predictor/
│   ├── v1.0.0/
│   │   ├── model.pkl
│   │   ├── metadata.json
│   │   └── metrics.json
│   ├── v1.1.0/
│   │   ├── model.pkl
│   │   ├── metadata.json
│   │   └── metrics.json
│   └── production -> v1.1.0  (enlace simbólico)
├── fraud_detector/
│   └── ...
└── registry_index.json
```

### Metadatos del Modelo

```json
{
    "model_name": "churn_predictor",
    "version": "1.1.0",
    "created_at": "2025-01-15T10:30:00Z",
    "created_by": "data_team",
    "framework": "scikit-learn",
    "framework_version": "1.3.0",
    "python_version": "3.11",
    "features": ["age", "tenure", "monthly_charges", "contract_type"],
    "target": "churn",
    "training_data": {
        "source": "warehouse.customers",
        "rows": 50000,
        "date_range": "2024-01-01 to 2024-12-31"
    },
    "metrics": {
        "accuracy": 0.87,
        "precision": 0.82,
        "recall": 0.79,
        "f1": 0.80,
        "auc_roc": 0.91
    },
    "status": "production"
}
```

---

## A/B Testing de Modelos

### ¿Por qué A/B Testing?

Antes de reemplazar un modelo en producción, quieres estar seguro de que el nuevo es mejor. A/B testing te permite comparar modelos con tráfico real.

### Patrones de Despliegue

#### 1. Canary Deployment

```
100% tráfico → Modelo A (actual)

Después:
95% tráfico → Modelo A
5% tráfico → Modelo B (nuevo)  ← "Canario"

Si B funciona bien:
50% → A, 50% → B

Finalmente:
100% → Modelo B
```

**Analogía:** El nombre viene de los mineros que llevaban canarios a las minas. Si el canario moría, había gas tóxico. Aquí, el 5% del tráfico es tu "canario".

#### 2. Shadow Mode

```
100% tráfico → Modelo A (responde al usuario)
                 ↓
              Modelo B (predice pero no responde)
                 ↓
              Comparar predicciones
```

**Uso:** Cuando el nuevo modelo es arriesgado y quieres evaluar sin impacto.

#### 3. Blue-Green Deployment

```
Ambiente BLUE (actual) ← Todo el tráfico
Ambiente GREEN (nuevo) ← Sin tráfico

Después del switch:
Ambiente BLUE ← Sin tráfico
Ambiente GREEN ← Todo el tráfico
```

**Uso:** Cambios grandes donde quieres rollback instantáneo.

---

## Logging y Trazabilidad

### ¿Por Qué Loggear Todo?

Cuando algo sale mal en producción, necesitas poder responder:
- ¿Qué datos recibió el modelo?
- ¿Qué predicción hizo?
- ¿Cuánto tardó?
- ¿Hubo errores?

### Estructura de Logs

```python
import logging
import json
from datetime import datetime
import uuid

# Configurar logger estructurado
logging.basicConfig(
    format='%(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def log_prediction(request_id: str, input_data: dict,
                   prediction: dict, latency_ms: float):
    """Loggear una predicción de forma estructurada."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "event": "prediction",
        "input": input_data,
        "output": prediction,
        "latency_ms": latency_ms,
        "model_version": "1.1.0"
    }
    logger.info(json.dumps(log_entry))

# Uso
request_id = str(uuid.uuid4())
log_prediction(
    request_id=request_id,
    input_data={"age": 35, "income": 50000},
    prediction={"class": 1, "probability": 0.87},
    latency_ms=45.2
)
```

### Información a Loggear

| Categoría | Campos | Por qué |
|-----------|--------|---------|
| **Identificación** | request_id, timestamp | Trazabilidad |
| **Entrada** | features, valores | Debugging, reentrenamiento |
| **Salida** | predicción, probabilidad | Análisis de resultados |
| **Rendimiento** | latencia, memoria | Optimización |
| **Contexto** | model_version, usuario | Auditoría |

---

## Seguridad en MLOps

### Riesgos de Seguridad

1. **Model Theft**: Alguien roba tu modelo
2. **Data Poisoning**: Datos maliciosos en entrenamiento
3. **Adversarial Attacks**: Inputs diseñados para engañar al modelo
4. **PII Exposure**: Datos personales en logs

### Mejores Prácticas

```python
# 1. Validar inputs
from pydantic import BaseModel, validator

class SecureRequest(BaseModel):
    age: int
    income: float

    @validator('age')
    def age_must_be_reasonable(cls, v):
        if not 0 < v < 150:
            raise ValueError('Edad fuera de rango válido')
        return v

    @validator('income')
    def income_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Ingreso no puede ser negativo')
        return v

# 2. Rate limiting
from fastapi import Request
from slowapi import Limiter

limiter = Limiter(key_func=lambda request: request.client.host)

@app.post("/predict")
@limiter.limit("100/minute")
async def predict(request: Request, data: SecureRequest):
    pass

# 3. No loggear PII
def sanitize_for_logging(data: dict) -> dict:
    """Remover campos sensibles antes de loggear."""
    sensitive_fields = ['ssn', 'email', 'phone', 'address']
    return {k: v for k, v in data.items() if k not in sensitive_fields}
```

---

## Herramientas del Ecosistema MLOps

### Panorama de Herramientas

```
┌─────────────────────────────────────────────────────────────────┐
│                   ECOSISTEMA MLOPS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  EXPERIMENTOS          FEATURE STORE       ORQUESTACIÓN         │
│  ├── MLflow            ├── Feast           ├── Airflow          │
│  ├── Weights & Biases  ├── Tecton          ├── Prefect          │
│  └── Neptune           └── Hopsworks       └── Dagster          │
│                                                                 │
│  SERVING               MONITOREO           INFRAESTRUCTURA      │
│  ├── BentoML           ├── Evidently       ├── Kubernetes       │
│  ├── Seldon            ├── Whylabs         ├── Docker           │
│  ├── MLflow Serving    ├── Arize           └── Terraform        │
│  └── TensorFlow Serving└── Fiddler                              │
│                                                                 │
│  PLATAFORMAS END-TO-END                                         │
│  ├── AWS SageMaker                                              │
│  ├── Google Vertex AI                                           │
│  ├── Azure ML                                                   │
│  └── Databricks                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Cuándo Usar Qué

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Startup, equipo pequeño | MLflow + FastAPI + Docker | Simple, open source |
| Empresa mediana | MLflow + Kubernetes + Airflow | Escalable, control |
| Empresa grande en AWS | SageMaker | Integración completa |
| Empresa grande en GCP | Vertex AI | Integración completa |

---

## Errores Comunes en MLOps

### Error 1: No Versionar el Ambiente

```python
# ❌ MAL
pip install pandas scikit-learn

# ✅ BIEN
pip install pandas==2.0.3 scikit-learn==1.3.0
```

### Error 2: Entrenar y Servir con Código Diferente

```python
# ❌ MAL: Preprocessing diferente
# En entrenamiento:
df['age_normalized'] = (df['age'] - 30) / 10

# En producción:
df['age_normalized'] = df['age'] / 100  # ¡Diferente!

# ✅ BIEN: Usar el mismo pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
# El pipeline tiene el preprocesamiento incluido
```

### Error 3: No Monitorear Data Drift

```python
# ❌ MAL: Desplegar y olvidar
model = train(data)
deploy(model)
# ... 6 meses después, el modelo falla silenciosamente

# ✅ BIEN: Monitoreo continuo
scheduler.add_job(check_drift, trigger='interval', hours=24)
```

### Error 4: No Tener Plan de Rollback

```python
# ❌ MAL: Solo una versión
models/model.pkl  # Si falla, ¿a qué vuelves?

# ✅ BIEN: Mantener versiones
models/
├── production/model.pkl -> v1.2.0
├── v1.1.0/model.pkl
├── v1.2.0/model.pkl
└── v1.3.0/model.pkl  # staging
```

### Error 5: Loggear PII

```python
# ❌ MAL
logger.info(f"Predicción para usuario {user_email}: {prediction}")

# ✅ BIEN
logger.info(f"Predicción para request {request_id}: {prediction}")
```

---

## Checklist de Productivización

Antes de desplegar un modelo en producción, verifica:

### Código y Reproducibilidad
- [ ] El código está versionado en Git
- [ ] Las dependencias están fijadas (requirements.txt con versiones)
- [ ] El modelo puede reconstruirse desde el código
- [ ] Hay tests automatizados

### Empaquetado
- [ ] El modelo está serializado correctamente (joblib/pickle)
- [ ] Existe Dockerfile funcional
- [ ] El contenedor se puede construir y ejecutar localmente

### API
- [ ] Endpoint `/predict` funciona
- [ ] Endpoint `/health` existe
- [ ] Validación de inputs implementada
- [ ] Manejo de errores robusto
- [ ] Documentación de API (OpenAPI/Swagger)

### Monitoreo
- [ ] Logs estructurados implementados
- [ ] Métricas de latencia configuradas
- [ ] Detección de drift implementada
- [ ] Alertas configuradas

### Operaciones
- [ ] Plan de rollback documentado
- [ ] Procedimiento de reentrenamiento definido
- [ ] Responsables identificados
- [ ] Runbook de incidentes creado

---

## Checklist de Aprendizaje

- [ ] Entiendo qué es MLOps y por qué es necesario
- [ ] Puedo explicar los 3 niveles de madurez MLOps
- [ ] Sé qué elementos versionar en un proyecto ML
- [ ] Puedo crear una API de predicción con FastAPI
- [ ] Entiendo qué es data drift y cómo detectarlo
- [ ] Conozco los patrones de despliegue (canary, blue-green)
- [ ] Sé qué información loggear y cuál NO loggear
- [ ] Puedo diseñar un pipeline de reentrenamiento
- [ ] Conozco las herramientas principales del ecosistema MLOps

---

## Resumen

MLOps es la disciplina que permite llevar modelos de ML del notebook a producción de forma confiable. Los elementos clave son:

1. **Versionado**: Código, datos, modelos, ambiente
2. **Empaquetado**: Docker para reproducibilidad
3. **Servicio**: APIs REST con FastAPI
4. **Monitoreo**: Drift, rendimiento, errores
5. **Reentrenamiento**: Pipelines automáticos
6. **Seguridad**: Validación, rate limiting, sin PII

Como Data Engineer, serás responsable de construir la infraestructura que hace todo esto posible. No necesitas dominar cada herramienta, pero sí entender los conceptos y poder implementar soluciones básicas.

**Recuerda:** Un modelo que no está en producción no genera valor. MLOps es lo que convierte experimentos en impacto real.
