# Ejemplos Prácticos: MLOps y Productivización

## Ejemplo 1: API de Predicción con FastAPI - Nivel: Básico

### Contexto

**DataFlow Analytics** necesita exponer un modelo de clasificación de clientes como API REST para que otras aplicaciones puedan consumirlo. El modelo predice si un cliente va a abandonar el servicio (churn).

### Objetivo

Crear una API de predicción completa con:
- Endpoint de predicción
- Endpoint de salud
- Validación de inputs
- Manejo de errores

### Paso 1: Estructura del Proyecto

```
churn_api/
├── src/
│   ├── __init__.py
│   ├── api.py          # API FastAPI
│   ├── model.py        # Carga de modelo
│   └── schemas.py      # Esquemas Pydantic
├── models/
│   └── churn_model.pkl
├── tests/
│   └── test_api.py
├── requirements.txt
└── Dockerfile
```

### Paso 2: Definir Esquemas de Entrada/Salida

```python
# src/schemas.py
"""Esquemas de validación para la API."""

from pydantic import BaseModel, Field, validator


class CustomerData(BaseModel):
    """Datos de entrada para predicción de churn."""

    age: int = Field(..., ge=18, le=120, description="Edad del cliente")
    tenure_months: int = Field(..., ge=0, description="Meses como cliente")
    monthly_charges: float = Field(..., gt=0, description="Cargo mensual")
    total_charges: float = Field(..., ge=0, description="Cargos totales")
    contract_type: str = Field(..., description="Tipo de contrato")

    @validator("contract_type")
    def validate_contract(cls, v):
        """Validar tipo de contrato."""
        valid_types = ["month-to-month", "one_year", "two_year"]
        if v not in valid_types:
            raise ValueError(f"Contrato debe ser uno de: {valid_types}")
        return v

    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "tenure_months": 24,
                "monthly_charges": 75.50,
                "total_charges": 1812.00,
                "contract_type": "one_year"
            }
        }


class PredictionResponse(BaseModel):
    """Respuesta de predicción."""

    prediction: int = Field(..., description="0=No churn, 1=Churn")
    probability: float = Field(..., description="Probabilidad de churn")
    risk_level: str = Field(..., description="Nivel de riesgo")
    model_version: str = Field(..., description="Versión del modelo")


class HealthResponse(BaseModel):
    """Respuesta del health check."""

    status: str
    model_loaded: bool
    version: str
```

### Paso 3: Cargar el Modelo

```python
# src/model.py
"""Gestión del modelo de ML."""

import joblib
from pathlib import Path
from typing import Optional
import numpy as np

MODEL_PATH = Path("models/churn_model.pkl")
MODEL_VERSION = "1.0.0"

# Variable global para el modelo
_model = None


def load_model() -> None:
    """Cargar modelo desde disco."""
    global _model
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
    else:
        raise FileNotFoundError(f"Modelo no encontrado en {MODEL_PATH}")


def get_model():
    """Obtener instancia del modelo."""
    if _model is None:
        raise RuntimeError("Modelo no cargado. Llamar load_model() primero.")
    return _model


def predict(features: np.ndarray) -> tuple[int, float]:
    """
    Realizar predicción.

    Args:
        features: Array con features del cliente

    Returns:
        Tupla (predicción, probabilidad)
    """
    model = get_model()
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]  # Prob de clase 1
    return int(prediction), float(probability)


def get_risk_level(probability: float) -> str:
    """Determinar nivel de riesgo basado en probabilidad."""
    if probability < 0.3:
        return "bajo"
    elif probability < 0.7:
        return "medio"
    else:
        return "alto"
```

### Paso 4: Crear la API

```python
# src/api.py
"""API de predicción de churn."""

from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import numpy as np
import logging

from src.schemas import CustomerData, PredictionResponse, HealthResponse
from src.model import load_model, predict, get_risk_level, MODEL_VERSION

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cargar modelo al iniciar la aplicación."""
    logger.info("Cargando modelo...")
    try:
        load_model()
        logger.info("Modelo cargado exitosamente")
    except FileNotFoundError as e:
        logger.warning(f"Modelo no encontrado: {e}")
    yield
    logger.info("Cerrando aplicación...")


app = FastAPI(
    title="API de Predicción de Churn",
    description="API para predecir abandono de clientes",
    version=MODEL_VERSION,
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Verificar estado del servicio."""
    try:
        from src.model import _model
        model_loaded = _model is not None
    except Exception:
        model_loaded = False

    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        version=MODEL_VERSION
    )


@app.post("/predict", response_model=PredictionResponse)
def predict_churn(customer: CustomerData):
    """
    Predecir probabilidad de churn para un cliente.

    - **age**: Edad del cliente (18-120)
    - **tenure_months**: Meses como cliente
    - **monthly_charges**: Cargo mensual ($)
    - **total_charges**: Cargos totales acumulados ($)
    - **contract_type**: Tipo de contrato (month-to-month, one_year, two_year)
    """
    try:
        # Preparar features
        contract_mapping = {
            "month-to-month": 0,
            "one_year": 1,
            "two_year": 2
        }

        features = np.array([[
            customer.age,
            customer.tenure_months,
            customer.monthly_charges,
            customer.total_charges,
            contract_mapping[customer.contract_type]
        ]])

        # Predecir
        prediction, probability = predict(features)
        risk_level = get_risk_level(probability)

        logger.info(
            f"Predicción realizada: prob={probability:.3f}, risk={risk_level}"
        )

        return PredictionResponse(
            prediction=prediction,
            probability=round(probability, 4),
            risk_level=risk_level,
            model_version=MODEL_VERSION
        )

    except RuntimeError as e:
        logger.error(f"Error de modelo: {e}")
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    """Endpoint raíz con información del servicio."""
    return {
        "service": "Churn Prediction API",
        "version": MODEL_VERSION,
        "docs": "/docs"
    }
```

### Paso 5: Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements primero (para cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código y modelo
COPY src/ /app/src/
COPY models/ /app/models/

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Paso 6: Probar la API

```python
# tests/test_api.py
"""Tests para la API de churn."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np

from src.api import app


@pytest.fixture
def client():
    """Cliente de test."""
    return TestClient(app)


@pytest.fixture
def mock_model():
    """Mock del modelo."""
    model = MagicMock()
    model.predict.return_value = np.array([1])
    model.predict_proba.return_value = np.array([[0.3, 0.7]])
    return model


def test_health_endpoint(client):
    """Test del endpoint de salud."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data


def test_predict_valid_input(client, mock_model):
    """Test de predicción con input válido."""
    with patch("src.model._model", mock_model):
        response = client.post("/predict", json={
            "age": 35,
            "tenure_months": 24,
            "monthly_charges": 75.50,
            "total_charges": 1812.00,
            "contract_type": "one_year"
        })

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert "risk_level" in data


def test_predict_invalid_age(client):
    """Test de validación de edad."""
    response = client.post("/predict", json={
        "age": 10,  # Menor que 18
        "tenure_months": 24,
        "monthly_charges": 75.50,
        "total_charges": 1812.00,
        "contract_type": "one_year"
    })
    assert response.status_code == 422  # Validation error


def test_predict_invalid_contract(client):
    """Test de validación de contrato."""
    response = client.post("/predict", json={
        "age": 35,
        "tenure_months": 24,
        "monthly_charges": 75.50,
        "total_charges": 1812.00,
        "contract_type": "invalid"  # Tipo inválido
    })
    assert response.status_code == 422
```

### Resultado

```bash
# Construir imagen Docker
docker build -t churn-api .

# Ejecutar contenedor
docker run -p 8000:8000 churn-api

# Probar
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 35, "tenure_months": 24, "monthly_charges": 75.5,
       "total_charges": 1812.0, "contract_type": "one_year"}'

# Respuesta:
{
  "prediction": 0,
  "probability": 0.2341,
  "risk_level": "bajo",
  "model_version": "1.0.0"
}
```

### Interpretación

Esta API implementa los principios básicos de MLOps:
- **Validación robusta**: Pydantic valida todos los inputs
- **Health check**: Permite a orquestadores verificar el estado
- **Versionado**: El modelo y la API tienen versiones
- **Containerización**: Docker garantiza reproducibilidad

---

## Ejemplo 2: Detección de Data Drift - Nivel: Intermedio

### Contexto

**FinTech Solutions** tiene un modelo de scoring crediticio en producción. Necesitan detectar automáticamente cuando los datos de entrada empiezan a diferir de los datos de entrenamiento.

### Objetivo

Implementar un sistema de detección de drift que:
- Compare distribuciones estadísticamente
- Genere alertas cuando hay drift significativo
- Produzca reportes visuales

### Paso 1: Funciones de Detección de Drift

```python
# drift_detector.py
"""Detector de data drift para modelos en producción."""

import numpy as np
from scipy import stats
from typing import Optional
import json
from datetime import datetime


def detect_drift_ks(
    reference: np.ndarray,
    current: np.ndarray,
    threshold: float = 0.05
) -> dict:
    """
    Detectar drift usando test de Kolmogorov-Smirnov.

    El test KS compara las distribuciones acumuladas de dos muestras.
    Un p-value bajo indica que las distribuciones son diferentes.

    Args:
        reference: Datos de referencia (entrenamiento)
        current: Datos actuales (producción)
        threshold: Umbral de p-value para detectar drift

    Returns:
        Diccionario con resultados del test
    """
    statistic, p_value = stats.ks_2samp(reference, current)

    return {
        "test": "kolmogorov_smirnov",
        "statistic": float(statistic),
        "p_value": float(p_value),
        "threshold": threshold,
        "drift_detected": p_value < threshold
    }


def detect_drift_psi(
    reference: np.ndarray,
    current: np.ndarray,
    buckets: int = 10,
    threshold: float = 0.2
) -> dict:
    """
    Detectar drift usando Population Stability Index (PSI).

    PSI mide cuánto ha cambiado una distribución comparando
    proporciones en buckets.

    Interpretación de PSI:
    - < 0.1: Sin cambio significativo
    - 0.1 - 0.2: Cambio moderado
    - > 0.2: Cambio significativo

    Args:
        reference: Datos de referencia
        current: Datos actuales
        buckets: Número de buckets para discretizar
        threshold: Umbral de PSI para detectar drift

    Returns:
        Diccionario con resultados
    """
    # Crear buckets basados en referencia
    breakpoints = np.percentile(
        reference,
        np.linspace(0, 100, buckets + 1)
    )
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    # Calcular proporciones en cada bucket
    ref_counts = np.histogram(reference, bins=breakpoints)[0]
    cur_counts = np.histogram(current, bins=breakpoints)[0]

    # Evitar división por cero
    ref_pct = (ref_counts + 1) / (len(reference) + buckets)
    cur_pct = (cur_counts + 1) / (len(current) + buckets)

    # Calcular PSI
    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))

    return {
        "test": "psi",
        "psi_value": float(psi),
        "threshold": threshold,
        "drift_detected": psi > threshold,
        "interpretation": (
            "sin cambio" if psi < 0.1
            else "cambio moderado" if psi < 0.2
            else "cambio significativo"
        )
    }


def detect_drift_wasserstein(
    reference: np.ndarray,
    current: np.ndarray,
    threshold: Optional[float] = None
) -> dict:
    """
    Detectar drift usando distancia de Wasserstein (Earth Mover's Distance).

    Mide la "cantidad de trabajo" necesaria para transformar
    una distribución en otra.

    Args:
        reference: Datos de referencia
        current: Datos actuales
        threshold: Umbral opcional (si None, se calcula automáticamente)

    Returns:
        Diccionario con resultados
    """
    distance = stats.wasserstein_distance(reference, current)

    # Threshold basado en desviación estándar de referencia
    if threshold is None:
        threshold = 0.1 * np.std(reference)

    return {
        "test": "wasserstein",
        "distance": float(distance),
        "threshold": float(threshold),
        "drift_detected": distance > threshold,
        "normalized_distance": float(distance / np.std(reference))
    }


def analyze_feature_drift(
    reference_data: dict,
    current_data: dict,
    numeric_features: list[str],
    tests: list[str] = ["ks", "psi"]
) -> dict:
    """
    Analizar drift en múltiples features.

    Args:
        reference_data: Dict con features de referencia
        current_data: Dict con features actuales
        numeric_features: Lista de features numéricas
        tests: Tests a aplicar ('ks', 'psi', 'wasserstein')

    Returns:
        Reporte completo de drift
    """
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "features_analyzed": len(numeric_features),
        "features_with_drift": 0,
        "details": {}
    }

    for feature in numeric_features:
        ref = np.array(reference_data[feature])
        cur = np.array(current_data[feature])

        feature_results = {
            "reference_mean": float(np.mean(ref)),
            "reference_std": float(np.std(ref)),
            "current_mean": float(np.mean(cur)),
            "current_std": float(np.std(cur)),
            "tests": {}
        }

        drift_detected = False

        if "ks" in tests:
            ks_result = detect_drift_ks(ref, cur)
            feature_results["tests"]["ks"] = ks_result
            if ks_result["drift_detected"]:
                drift_detected = True

        if "psi" in tests:
            psi_result = detect_drift_psi(ref, cur)
            feature_results["tests"]["psi"] = psi_result
            if psi_result["drift_detected"]:
                drift_detected = True

        if "wasserstein" in tests:
            ws_result = detect_drift_wasserstein(ref, cur)
            feature_results["tests"]["wasserstein"] = ws_result
            if ws_result["drift_detected"]:
                drift_detected = True

        feature_results["drift_detected"] = drift_detected
        report["details"][feature] = feature_results

        if drift_detected:
            report["features_with_drift"] += 1

    report["drift_alert"] = report["features_with_drift"] > 0

    return report
```

### Paso 2: Uso Práctico

```python
# Datos de entrenamiento (referencia)
reference = {
    "age": np.random.normal(35, 10, 1000),
    "income": np.random.normal(50000, 15000, 1000),
    "debt_ratio": np.random.beta(2, 5, 1000)
}

# Datos de producción (con drift en income)
current = {
    "age": np.random.normal(35, 10, 500),  # Sin cambio
    "income": np.random.normal(65000, 15000, 500),  # ¡Drift!
    "debt_ratio": np.random.beta(2, 5, 500)  # Sin cambio
}

# Analizar
report = analyze_feature_drift(
    reference,
    current,
    ["age", "income", "debt_ratio"],
    tests=["ks", "psi"]
)

print(json.dumps(report, indent=2))
```

### Resultado

```json
{
  "timestamp": "2025-01-15T10:30:00.000000",
  "features_analyzed": 3,
  "features_with_drift": 1,
  "details": {
    "age": {
      "reference_mean": 35.12,
      "current_mean": 34.89,
      "drift_detected": false,
      "tests": {
        "ks": {"drift_detected": false, "p_value": 0.45}
      }
    },
    "income": {
      "reference_mean": 50234.5,
      "current_mean": 65123.8,
      "drift_detected": true,
      "tests": {
        "ks": {"drift_detected": true, "p_value": 0.0001},
        "psi": {"drift_detected": true, "psi_value": 0.35}
      }
    },
    "debt_ratio": {
      "reference_mean": 0.28,
      "current_mean": 0.29,
      "drift_detected": false
    }
  },
  "drift_alert": true
}
```

### Interpretación

El sistema detecta correctamente que:
- **age** y **debt_ratio**: Sin drift significativo
- **income**: Drift detectado (la media pasó de ~50K a ~65K)

Esto indicaría que el modelo podría necesitar reentrenamiento, ya que está recibiendo un perfil de clientes diferente al que vio durante el entrenamiento.

---

## Ejemplo 3: Model Registry Simple - Nivel: Intermedio

### Contexto

**Analytics Corp** necesita un sistema para gestionar versiones de modelos, trackear métricas y manejar el ciclo staging → production.

### Paso 1: Implementar Model Registry

```python
# model_registry.py
"""Registry simple para gestión de modelos ML."""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional
import hashlib


class ModelRegistry:
    """
    Registry para gestionar versiones de modelos.

    Estructura:
        registry_path/
        ├── index.json
        ├── model_name/
        │   ├── v1.0.0/
        │   │   ├── model.pkl
        │   │   ├── metadata.json
        │   │   └── metrics.json
        │   ├── v1.1.0/
        │   │   └── ...
        │   └── production.json  (enlace a versión en producción)
    """

    def __init__(self, registry_path: str = "model_registry"):
        """Inicializar registry."""
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.registry_path / "index.json"
        self._load_index()

    def _load_index(self):
        """Cargar índice del registry."""
        if self.index_path.exists():
            with open(self.index_path, "r") as f:
                self.index = json.load(f)
        else:
            self.index = {"models": {}, "created_at": datetime.utcnow().isoformat()}
            self._save_index()

    def _save_index(self):
        """Guardar índice."""
        self.index["updated_at"] = datetime.utcnow().isoformat()
        with open(self.index_path, "w") as f:
            json.dump(self.index, f, indent=2)

    def _compute_checksum(self, file_path: Path) -> str:
        """Calcular checksum MD5 de un archivo."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def register_model(
        self,
        model_name: str,
        version: str,
        model_path: str,
        metrics: dict,
        metadata: Optional[dict] = None
    ) -> dict:
        """
        Registrar una nueva versión de modelo.

        Args:
            model_name: Nombre del modelo
            version: Versión semántica (e.g., "1.0.0")
            model_path: Ruta al archivo del modelo
            metrics: Métricas de evaluación
            metadata: Metadata adicional

        Returns:
            Información del registro
        """
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {model_path}")

        # Crear directorio para el modelo
        model_dir = self.registry_path / model_name
        version_dir = model_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)

        # Copiar modelo
        dest_path = version_dir / "model.pkl"
        shutil.copy(model_path, dest_path)
        checksum = self._compute_checksum(dest_path)

        # Crear metadata
        full_metadata = {
            "model_name": model_name,
            "version": version,
            "registered_at": datetime.utcnow().isoformat(),
            "checksum": checksum,
            "file_size_bytes": dest_path.stat().st_size,
            **(metadata or {})
        }

        # Guardar metadata y métricas
        with open(version_dir / "metadata.json", "w") as f:
            json.dump(full_metadata, f, indent=2)

        with open(version_dir / "metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        # Actualizar índice
        if model_name not in self.index["models"]:
            self.index["models"][model_name] = {
                "versions": [],
                "production_version": None,
                "staging_version": None
            }

        self.index["models"][model_name]["versions"].append(version)
        self.index["models"][model_name]["latest_version"] = version
        self._save_index()

        return {
            "status": "registered",
            "model_name": model_name,
            "version": version,
            "path": str(version_dir)
        }

    def promote_to_staging(self, model_name: str, version: str) -> dict:
        """Promover versión a staging."""
        if model_name not in self.index["models"]:
            raise ValueError(f"Modelo no encontrado: {model_name}")

        if version not in self.index["models"][model_name]["versions"]:
            raise ValueError(f"Versión no encontrada: {version}")

        self.index["models"][model_name]["staging_version"] = version
        self._save_index()

        return {
            "status": "promoted_to_staging",
            "model_name": model_name,
            "version": version
        }

    def promote_to_production(self, model_name: str, version: str) -> dict:
        """Promover versión a producción."""
        if model_name not in self.index["models"]:
            raise ValueError(f"Modelo no encontrado: {model_name}")

        if version not in self.index["models"][model_name]["versions"]:
            raise ValueError(f"Versión no encontrada: {version}")

        # Guardar versión anterior para rollback
        previous = self.index["models"][model_name].get("production_version")
        if previous:
            self.index["models"][model_name]["previous_production"] = previous

        self.index["models"][model_name]["production_version"] = version
        self.index["models"][model_name]["staging_version"] = None
        self._save_index()

        return {
            "status": "promoted_to_production",
            "model_name": model_name,
            "version": version,
            "previous_version": previous
        }

    def rollback(self, model_name: str) -> dict:
        """Revertir a versión anterior de producción."""
        if model_name not in self.index["models"]:
            raise ValueError(f"Modelo no encontrado: {model_name}")

        previous = self.index["models"][model_name].get("previous_production")
        if not previous:
            raise ValueError("No hay versión anterior para rollback")

        current = self.index["models"][model_name]["production_version"]
        self.index["models"][model_name]["production_version"] = previous
        self.index["models"][model_name]["previous_production"] = current
        self._save_index()

        return {
            "status": "rolled_back",
            "model_name": model_name,
            "from_version": current,
            "to_version": previous
        }

    def get_production_model_path(self, model_name: str) -> Path:
        """Obtener ruta al modelo en producción."""
        if model_name not in self.index["models"]:
            raise ValueError(f"Modelo no encontrado: {model_name}")

        version = self.index["models"][model_name].get("production_version")
        if not version:
            raise ValueError(f"No hay versión en producción para {model_name}")

        return self.registry_path / model_name / version / "model.pkl"

    def get_model_info(self, model_name: str, version: str) -> dict:
        """Obtener información completa de una versión."""
        version_dir = self.registry_path / model_name / version

        if not version_dir.exists():
            raise ValueError(f"Versión no encontrada: {model_name}/{version}")

        with open(version_dir / "metadata.json", "r") as f:
            metadata = json.load(f)

        with open(version_dir / "metrics.json", "r") as f:
            metrics = json.load(f)

        return {
            "metadata": metadata,
            "metrics": metrics,
            "is_production": (
                self.index["models"][model_name].get("production_version") == version
            ),
            "is_staging": (
                self.index["models"][model_name].get("staging_version") == version
            )
        }

    def list_models(self) -> dict:
        """Listar todos los modelos registrados."""
        return self.index["models"]
```

### Paso 2: Uso del Registry

```python
import joblib
from sklearn.ensemble import RandomForestClassifier

# Crear un modelo de ejemplo
model = RandomForestClassifier(n_estimators=100)
# ... entrenar el modelo ...
joblib.dump(model, "temp_model.pkl")

# Inicializar registry
registry = ModelRegistry("./my_registry")

# Registrar modelo v1.0.0
result = registry.register_model(
    model_name="churn_classifier",
    version="1.0.0",
    model_path="temp_model.pkl",
    metrics={
        "accuracy": 0.85,
        "f1_score": 0.82,
        "auc_roc": 0.89
    },
    metadata={
        "framework": "scikit-learn",
        "framework_version": "1.3.0",
        "training_data": "customers_2024.csv",
        "features": ["age", "tenure", "monthly_charges"]
    }
)
print(f"Registrado: {result}")

# Promover a staging
registry.promote_to_staging("churn_classifier", "1.0.0")
print("Promovido a staging")

# Después de validar, promover a producción
registry.promote_to_production("churn_classifier", "1.0.0")
print("Promovido a producción")

# Obtener modelo de producción
model_path = registry.get_production_model_path("churn_classifier")
print(f"Modelo en producción: {model_path}")

# Ver información
info = registry.get_model_info("churn_classifier", "1.0.0")
print(json.dumps(info, indent=2))
```

### Resultado

```
Registrado: {'status': 'registered', 'model_name': 'churn_classifier', 'version': '1.0.0'}
Promovido a staging
Promovido a producción
Modelo en producción: my_registry/churn_classifier/1.0.0/model.pkl

{
  "metadata": {
    "model_name": "churn_classifier",
    "version": "1.0.0",
    "registered_at": "2025-01-15T10:30:00",
    "framework": "scikit-learn",
    "features": ["age", "tenure", "monthly_charges"]
  },
  "metrics": {
    "accuracy": 0.85,
    "f1_score": 0.82,
    "auc_roc": 0.89
  },
  "is_production": true,
  "is_staging": false
}
```

---

## Ejemplo 4: Logging Estructurado para Predicciones - Nivel: Básico

### Contexto

**LogiTech Analytics** necesita implementar logging estructurado para poder analizar el comportamiento del modelo en producción.

### Paso 1: Implementar Logger Estructurado

```python
# prediction_logger.py
"""Logger estructurado para predicciones ML."""

import json
import logging
from datetime import datetime
from typing import Any, Optional
import uuid


class PredictionLogger:
    """Logger para predicciones con formato estructurado."""

    def __init__(self, service_name: str, log_level: int = logging.INFO):
        """
        Inicializar logger.

        Args:
            service_name: Nombre del servicio
            log_level: Nivel de logging
        """
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(log_level)

        # Formato JSON
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)

    def _create_log_entry(
        self,
        event_type: str,
        data: dict,
        request_id: Optional[str] = None
    ) -> dict:
        """Crear entrada de log estructurada."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": self.service_name,
            "request_id": request_id or str(uuid.uuid4()),
            "event": event_type,
            **data
        }

    def log_prediction(
        self,
        request_id: str,
        input_features: dict,
        prediction: Any,
        probability: Optional[float] = None,
        latency_ms: Optional[float] = None,
        model_version: str = "unknown"
    ):
        """
        Loggear una predicción.

        Args:
            request_id: ID único de la solicitud
            input_features: Features de entrada (sanitizadas)
            prediction: Resultado de la predicción
            probability: Probabilidad (si aplica)
            latency_ms: Latencia en milisegundos
            model_version: Versión del modelo
        """
        entry = self._create_log_entry(
            "prediction",
            {
                "input": input_features,
                "output": {
                    "prediction": prediction,
                    "probability": probability
                },
                "latency_ms": latency_ms,
                "model_version": model_version
            },
            request_id
        )
        self.logger.info(json.dumps(entry))

    def log_error(
        self,
        request_id: str,
        error_type: str,
        error_message: str,
        input_features: Optional[dict] = None
    ):
        """Loggear un error."""
        entry = self._create_log_entry(
            "error",
            {
                "error_type": error_type,
                "error_message": error_message,
                "input": input_features
            },
            request_id
        )
        self.logger.error(json.dumps(entry))

    def log_model_loaded(self, model_version: str, load_time_ms: float):
        """Loggear carga de modelo."""
        entry = self._create_log_entry(
            "model_loaded",
            {
                "model_version": model_version,
                "load_time_ms": load_time_ms
            }
        )
        self.logger.info(json.dumps(entry))

    def log_drift_alert(
        self,
        feature: str,
        drift_score: float,
        threshold: float
    ):
        """Loggear alerta de drift."""
        entry = self._create_log_entry(
            "drift_alert",
            {
                "feature": feature,
                "drift_score": drift_score,
                "threshold": threshold,
                "severity": "high" if drift_score > threshold * 2 else "medium"
            }
        )
        self.logger.warning(json.dumps(entry))


def sanitize_input(data: dict, pii_fields: list[str] = None) -> dict:
    """
    Sanitizar datos removiendo campos PII.

    Args:
        data: Datos originales
        pii_fields: Campos a remover

    Returns:
        Datos sanitizados
    """
    if pii_fields is None:
        pii_fields = ["email", "phone", "ssn", "address", "name", "credit_card"]

    return {k: v for k, v in data.items() if k.lower() not in pii_fields}
```

### Paso 2: Integrar con API

```python
# Uso en la API
import time

logger = PredictionLogger("churn-prediction-api")

@app.post("/predict")
def predict(customer: CustomerData):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    try:
        # Sanitizar input para logging
        safe_input = sanitize_input(customer.dict())

        # Hacer predicción
        prediction, probability = model.predict(...)

        # Calcular latencia
        latency_ms = (time.time() - start_time) * 1000

        # Loggear predicción
        logger.log_prediction(
            request_id=request_id,
            input_features=safe_input,
            prediction=prediction,
            probability=probability,
            latency_ms=latency_ms,
            model_version="1.0.0"
        )

        return {"prediction": prediction, "probability": probability}

    except Exception as e:
        logger.log_error(
            request_id=request_id,
            error_type=type(e).__name__,
            error_message=str(e),
            input_features=sanitize_input(customer.dict())
        )
        raise
```

### Resultado

```json
{"timestamp": "2025-01-15T10:30:00.123Z", "service": "churn-prediction-api", "request_id": "abc-123", "event": "prediction", "input": {"age": 35, "tenure_months": 24}, "output": {"prediction": 0, "probability": 0.23}, "latency_ms": 45.2, "model_version": "1.0.0"}
```

---

## Ejemplo 5: Pipeline de Reentrenamiento Automático - Nivel: Avanzado

### Contexto

**DataMart Corp** necesita un pipeline que automáticamente reentrene el modelo cuando detecte degradación en el rendimiento o drift significativo.

### Implementación

```python
# retraining_pipeline.py
"""Pipeline de reentrenamiento automático."""

import json
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional
import numpy as np
from sklearn.model_selection import cross_val_score
import joblib


class RetrainingPipeline:
    """Pipeline para reentrenamiento automático de modelos."""

    def __init__(
        self,
        model_registry_path: str,
        model_name: str,
        train_function: Callable,
        performance_threshold: float = 0.80
    ):
        """
        Inicializar pipeline.

        Args:
            model_registry_path: Ruta al registry
            model_name: Nombre del modelo
            train_function: Función de entrenamiento
            performance_threshold: Umbral mínimo de rendimiento
        """
        self.registry_path = Path(model_registry_path)
        self.model_name = model_name
        self.train_function = train_function
        self.performance_threshold = performance_threshold
        self.logs = []

    def _log(self, message: str, level: str = "info"):
        """Agregar entrada al log."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message
        }
        self.logs.append(entry)
        print(f"[{level.upper()}] {message}")

    def check_model_performance(
        self,
        model,
        X_test: np.ndarray,
        y_test: np.ndarray,
        metric: str = "accuracy"
    ) -> float:
        """Evaluar rendimiento actual del modelo."""
        if metric == "accuracy":
            from sklearn.metrics import accuracy_score
            predictions = model.predict(X_test)
            return accuracy_score(y_test, predictions)
        else:
            raise ValueError(f"Métrica no soportada: {metric}")

    def should_retrain(
        self,
        current_score: float,
        drift_detected: bool = False
    ) -> tuple[bool, str]:
        """
        Determinar si se debe reentrenar.

        Args:
            current_score: Score actual del modelo
            drift_detected: Si se detectó drift

        Returns:
            Tupla (debe_reentrenar, razón)
        """
        if drift_detected:
            return True, "Data drift detectado"

        if current_score < self.performance_threshold:
            return True, f"Rendimiento ({current_score:.3f}) bajo umbral ({self.performance_threshold})"

        return False, "Rendimiento aceptable"

    def run(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_test: np.ndarray,
        y_test: np.ndarray,
        drift_detected: bool = False,
        force_retrain: bool = False
    ) -> dict:
        """
        Ejecutar pipeline de reentrenamiento.

        Args:
            X_train: Datos de entrenamiento
            y_train: Labels de entrenamiento
            X_test: Datos de test
            y_test: Labels de test
            drift_detected: Si se detectó drift
            force_retrain: Forzar reentrenamiento

        Returns:
            Resultado del pipeline
        """
        self._log("Iniciando pipeline de reentrenamiento")
        result = {
            "started_at": datetime.utcnow().isoformat(),
            "action": None,
            "details": {}
        }

        # 1. Cargar modelo actual
        try:
            current_model_path = (
                self.registry_path / self.model_name / "production" / "model.pkl"
            )
            if current_model_path.exists():
                current_model = joblib.load(current_model_path)
                self._log("Modelo actual cargado")
            else:
                self._log("No hay modelo en producción, se entrenará nuevo", "warning")
                force_retrain = True
                current_model = None
        except Exception as e:
            self._log(f"Error cargando modelo: {e}", "error")
            force_retrain = True
            current_model = None

        # 2. Evaluar modelo actual
        if current_model is not None:
            current_score = self.check_model_performance(
                current_model, X_test, y_test
            )
            self._log(f"Rendimiento actual: {current_score:.4f}")
            result["details"]["current_score"] = current_score
        else:
            current_score = 0.0

        # 3. Decidir si reentrenar
        if not force_retrain:
            should_retrain, reason = self.should_retrain(current_score, drift_detected)
            self._log(f"¿Reentrenar? {should_retrain}. Razón: {reason}")
        else:
            should_retrain = True
            reason = "Forzado"

        if not should_retrain:
            result["action"] = "no_retrain"
            result["reason"] = reason
            result["completed_at"] = datetime.utcnow().isoformat()
            return result

        # 4. Reentrenar
        self._log("Iniciando reentrenamiento...")
        try:
            new_model = self.train_function(X_train, y_train)
            self._log("Reentrenamiento completado")
        except Exception as e:
            self._log(f"Error en reentrenamiento: {e}", "error")
            result["action"] = "retrain_failed"
            result["error"] = str(e)
            return result

        # 5. Evaluar nuevo modelo
        new_score = self.check_model_performance(new_model, X_test, y_test)
        self._log(f"Rendimiento nuevo modelo: {new_score:.4f}")
        result["details"]["new_score"] = new_score

        # 6. Comparar y decidir
        improvement = new_score - current_score

        if new_score < self.performance_threshold:
            self._log(
                f"Nuevo modelo no alcanza umbral ({new_score:.3f} < {self.performance_threshold})",
                "warning"
            )
            result["action"] = "retrain_rejected"
            result["reason"] = "No alcanza umbral mínimo"

        elif improvement < 0:
            self._log(
                f"Nuevo modelo es peor ({improvement:.4f})",
                "warning"
            )
            result["action"] = "retrain_rejected"
            result["reason"] = "No mejora sobre modelo actual"

        else:
            # 7. Guardar nuevo modelo
            self._log(f"Nuevo modelo mejora en {improvement:.4f}")
            version = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            save_path = self.registry_path / self.model_name / version
            save_path.mkdir(parents=True, exist_ok=True)

            model_file = save_path / "model.pkl"
            joblib.dump(new_model, model_file)

            # Guardar métricas
            metrics = {
                "accuracy": new_score,
                "improvement": improvement,
                "trained_at": datetime.utcnow().isoformat()
            }
            with open(save_path / "metrics.json", "w") as f:
                json.dump(metrics, f, indent=2)

            self._log(f"Modelo guardado en {save_path}")
            result["action"] = "retrain_success"
            result["new_version"] = version
            result["details"]["improvement"] = improvement

        result["completed_at"] = datetime.utcnow().isoformat()
        result["logs"] = self.logs

        return result


# Ejemplo de uso
def train_model(X, y):
    """Función de entrenamiento."""
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model


# Crear pipeline
pipeline = RetrainingPipeline(
    model_registry_path="./registry",
    model_name="churn_classifier",
    train_function=train_model,
    performance_threshold=0.80
)

# Ejecutar cuando se detecte drift
# result = pipeline.run(X_train, y_train, X_test, y_test, drift_detected=True)
```

### Resultado

```json
{
  "started_at": "2025-01-15T10:30:00",
  "action": "retrain_success",
  "new_version": "20250115_103045",
  "details": {
    "current_score": 0.82,
    "new_score": 0.87,
    "improvement": 0.05
  },
  "completed_at": "2025-01-15T10:30:45",
  "logs": [
    {"level": "info", "message": "Iniciando pipeline de reentrenamiento"},
    {"level": "info", "message": "Modelo actual cargado"},
    {"level": "info", "message": "Rendimiento actual: 0.8200"},
    {"level": "info", "message": "Reentrenamiento completado"},
    {"level": "info", "message": "Nuevo modelo mejora en 0.0500"}
  ]
}
```

---

## Resumen de Ejemplos

| Ejemplo | Nivel | Concepto Clave | Herramientas |
|---------|-------|----------------|--------------|
| API de Predicción | Básico | Servir modelos como API | FastAPI, Docker, Pydantic |
| Detección de Drift | Intermedio | Monitoreo de datos | scipy.stats, PSI, KS test |
| Model Registry | Intermedio | Versionado de modelos | JSON, checksums |
| Logging Estructurado | Básico | Observabilidad | logging, JSON |
| Reentrenamiento | Avanzado | Automatización del ciclo ML | Pipelines, umbral de rendimiento |

Estos ejemplos cubren los componentes fundamentales de un sistema MLOps: desde servir predicciones hasta detectar problemas y automatizar el mantenimiento del modelo.
