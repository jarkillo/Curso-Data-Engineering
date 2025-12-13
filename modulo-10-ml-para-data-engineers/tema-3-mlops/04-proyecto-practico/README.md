# Proyecto Práctico: Herramientas MLOps

## Descripción

Este proyecto implementa herramientas esenciales para MLOps (Machine Learning Operations), enfocándose en las capacidades fundamentales que un Data Engineer necesita para productivizar modelos de ML.

## Objetivos

- Implementar detección de data drift con tests estadísticos
- Crear un Model Registry para gestionar versiones de modelos
- Implementar logging estructurado para predicciones
- Desarrollar validaciones pre-deployment
- Crear un sistema de alertas para monitoreo

## Conceptos Clave

### Data Drift

El **drift** ocurre cuando la distribución de los datos de producción difiere de los datos de entrenamiento. Implementamos dos métodos de detección:

- **Test de Kolmogorov-Smirnov (KS)**: Compara distribuciones acumuladas
- **Population Stability Index (PSI)**: Mide cambios en proporciones por buckets

### Model Registry

Sistema de gestión de versiones de modelos que permite:
- Registrar modelos con métricas
- Promover a staging/production
- Rollback a versiones anteriores
- Verificar integridad con checksums

### Logging y Alertas

- **Logging estructurado**: Formato JSON para análisis
- **Sanitización de PII**: Protección de datos personales
- **Sistema de alertas**: Con cooldown para evitar spam

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   └── mlops_tools.py      # Funciones y clases principales
├── tests/
│   ├── __init__.py
│   └── test_mlops_tools.py # Tests con pytest
├── README.md
└── requirements.txt
```

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

## Ejecutar Tests

```bash
pytest -v --cov=src --cov-report=html
```

## Funciones Implementadas

### Drift Detection

#### `detect_drift_ks`

```python
def detect_drift_ks(
    reference: np.ndarray,
    current: np.ndarray,
    threshold: float = 0.05
) -> dict:
    """Detectar drift usando test de Kolmogorov-Smirnov."""
```

**Parámetros**:
- `reference`: Datos de referencia (entrenamiento)
- `current`: Datos actuales (producción)
- `threshold`: Umbral de p-value

**Retorna**: Dict con `statistic`, `p_value`, `drift_detected`

#### `detect_drift_psi`

```python
def detect_drift_psi(
    reference: np.ndarray,
    current: np.ndarray,
    buckets: int = 10,
    threshold: float = 0.2
) -> dict:
    """Detectar drift usando Population Stability Index."""
```

#### `analyze_feature_drift`

```python
def analyze_feature_drift(
    reference_data: dict,
    current_data: dict,
    features: list[str],
    tests: list[str] = None
) -> dict:
    """Analizar drift en múltiples features."""
```

### Model Registry

#### `ModelRegistry`

```python
registry = ModelRegistry("./my_registry")

# Registrar modelo
registry.register_model("churn", "1.0.0", "model.pkl", {"accuracy": 0.85})

# Promover
registry.promote_to_staging("churn", "1.0.0")
registry.promote_to_production("churn", "1.0.0")

# Rollback
registry.rollback("churn")

# Obtener ruta
path = registry.get_production_model_path("churn")
```

### Logging

#### `PredictionLogger`

```python
logger = PredictionLogger("my-service")
entry = logger.create_log_entry(
    request_id="req-123",
    input_data={"age": 35},
    prediction={"class": 1},
    latency_ms=45.2
)
```

#### `sanitize_pii`

```python
data = {"age": 35, "email": "test@example.com"}
clean_data = sanitize_pii(data)  # {"age": 35}
```

### Validation

#### `validate_model_for_deployment`

```python
config = {
    "min_accuracy": 0.80,
    "max_latency_ms": 100,
    "required_methods": ["predict", "predict_proba"]
}
result = validate_model_for_deployment(model, X_val, y_val, config)
```

### Alerting

#### `AlertSystem`

```python
thresholds = {
    "latency_p99_ms": {"warning": 100, "critical": 200}
}
alert_system = AlertSystem(thresholds, cooldown_hours=1)

metrics = {"latency_p99_ms": [50, 120, 250]}
result = alert_system.analyze_metrics(metrics)
```

## Ejemplos de Uso

### Detectar Drift en Producción

```python
import numpy as np
from src.mlops_tools import analyze_feature_drift

# Datos de referencia (entrenamiento)
reference = {
    "age": np.array([25, 30, 35, 28, 32, 29, 31, 27]),
    "income": np.array([45000, 52000, 38000, 61000, 48000, 55000])
}

# Datos de producción
production = {
    "age": np.array([26, 31, 34, 29, 33, 28]),
    "income": np.array([75000, 82000, 68000, 91000, 78000, 85000])  # ¡Drift!
}

report = analyze_feature_drift(reference, production, ["age", "income"])
print(f"Alerta: {report['drift_alert']}")
print(f"Features con drift: {report['features_with_drift']}")
```

### Pipeline de Deployment

```python
from src.mlops_tools import (
    ModelRegistry,
    validate_model_for_deployment
)

# 1. Validar modelo
config = {"min_accuracy": 0.80, "max_latency_ms": 100}
validation = validate_model_for_deployment(model, X_val, y_val, config)

if not validation["passed"]:
    print(f"Validación fallida: {validation['errors']}")
    exit(1)

# 2. Registrar en registry
registry = ModelRegistry("./registry")
registry.register_model(
    "churn_predictor",
    "2.0.0",
    "model.pkl",
    validation["metrics"]
)

# 3. Promover a producción
registry.promote_to_production("churn_predictor", "2.0.0")
```

## Troubleshooting

### Error: "Modelo no encontrado"

**Causa**: La ruta al modelo no existe.
**Solución**: Verificar que el archivo existe antes de registrar.

### Drift detectado pero modelo funciona bien

**Causa**: El drift no siempre afecta el rendimiento.
**Solución**: Combinar detección de drift con métricas de performance.

## Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md) - Conceptos de MLOps
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - Ejemplos prácticos
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - Ejercicios con soluciones
