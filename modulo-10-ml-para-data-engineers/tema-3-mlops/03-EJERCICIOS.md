# Ejercicios Prácticos: MLOps y Productivización

## Ejercicios Básicos

### Ejercicio 1: Validación de Inputs con Pydantic
**Dificultad**: ⭐ Fácil

**Contexto**:
**TechRetail Solutions** necesita validar los datos de entrada para su modelo de recomendación de productos.

**Datos**:
```python
# Datos de entrada esperados
input_data = {
    "user_id": "USR123",
    "age": 28,
    "purchase_history": [45.99, 120.50, 89.00],
    "category_preference": "electronics",
    "session_duration_minutes": 15.5
}
```

**Pregunta**:
Crea un esquema Pydantic que valide:
- `user_id`: String, debe empezar con "USR"
- `age`: Entero entre 13 y 120
- `purchase_history`: Lista de floats, no vacía
- `category_preference`: Uno de ["electronics", "clothing", "home", "sports"]
- `session_duration_minutes`: Float positivo

**Pista**:
Usa `@validator` para validaciones personalizadas y `Field` para restricciones básicas.

---

### Ejercicio 2: Health Check Endpoint
**Dificultad**: ⭐ Fácil

**Contexto**:
**CloudBank Digital** necesita un endpoint de health check que verifique que todos los componentes del servicio de predicción están funcionando.

**Datos**:
```python
# Componentes a verificar
components = {
    "model": {"loaded": True, "version": "2.1.0"},
    "database": {"connected": True, "latency_ms": 5.2},
    "cache": {"available": False, "error": "Connection timeout"}
}
```

**Pregunta**:
Implementa un endpoint `/health` que:
1. Verifique cada componente
2. Devuelva status "healthy" solo si todos los componentes críticos (model, database) funcionan
3. Devuelva status "degraded" si componentes no críticos (cache) fallan
4. Devuelva status "unhealthy" si algún componente crítico falla

**Pista**:
Define qué componentes son críticos y usa un bucle para verificar cada uno.

---

### Ejercicio 3: Logging de Predicciones
**Dificultad**: ⭐ Fácil

**Contexto**:
**InsureTech Analytics** necesita implementar logging estructurado para sus predicciones de riesgo.

**Datos**:
```python
# Datos de una predicción
request_id = "req-abc-123"
input_data = {
    "customer_id": "CUST001",
    "email": "john@example.com",  # PII - no loggear
    "age": 35,
    "vehicle_year": 2020,
    "claims_last_5_years": 1
}
prediction = {"risk_score": 0.23, "category": "low"}
latency_ms = 45.2
```

**Pregunta**:
Implementa una función `log_prediction` que:
1. Remueva campos PII (email, customer_id)
2. Agregue timestamp y request_id
3. Incluya la predicción y latencia
4. Devuelva un diccionario JSON-serializable

**Pista**:
Crea una lista de campos PII y filtra el diccionario antes de loggear.

---

### Ejercicio 4: Serialización de Modelo
**Dificultad**: ⭐ Fácil

**Contexto**:
**DataScience Hub** necesita serializar modelos con metadata para producción.

**Datos**:
```python
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Modelo entrenado
X = np.random.randn(100, 4)
y = np.random.randint(0, 2, 100)
model = RandomForestClassifier(n_estimators=50)
model.fit(X, y)

# Metadata
metadata = {
    "model_name": "fraud_detector",
    "version": "1.0.0",
    "features": ["amount", "time", "location_score", "device_score"],
    "trained_at": "2025-01-15"
}
```

**Pregunta**:
Implementa funciones `save_model_bundle` y `load_model_bundle` que:
1. Guarden el modelo y metadata juntos
2. Calculen un checksum del modelo
3. Permitan cargar y verificar la integridad

**Pista**:
Usa `joblib` para el modelo y `json` para la metadata. Guárdalos en un directorio.

---

## Ejercicios Intermedios

### Ejercicio 5: Detección de Drift Simple
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**FinanceAI Corp** quiere detectar cuando los datos de entrada a su modelo de scoring cambian significativamente.

**Datos**:
```python
import numpy as np

# Datos de referencia (entrenamiento)
reference_income = np.array([45000, 52000, 38000, 61000, 48000, 55000, 42000, 59000])
reference_age = np.array([28, 35, 42, 31, 45, 38, 29, 52])

# Datos de producción (última semana)
production_income = np.array([72000, 85000, 68000, 91000, 78000, 82000, 75000, 88000])
production_age = np.array([30, 33, 40, 35, 42, 37, 31, 48])
```

**Pregunta**:
Implementa una función `simple_drift_check` que:
1. Compare medias y desviaciones estándar
2. Use un umbral de 2 desviaciones estándar para detectar drift
3. Devuelva un reporte indicando qué features tienen drift

**Pista**:
Calcula `abs(mean_prod - mean_ref) / std_ref` y compara con el umbral.

---

### Ejercicio 6: Rate Limiting Manual
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**APIGuard Services** necesita implementar rate limiting simple para proteger su API de predicción.

**Datos**:
```python
# Configuración
max_requests_per_minute = 60
window_size_seconds = 60

# Historial de requests (timestamps)
request_history = {
    "client_A": [1705320000, 1705320005, 1705320010, 1705320015],  # 4 requests
    "client_B": [1705320000] * 100  # 100 requests (debería ser bloqueado)
}
current_timestamp = 1705320030
```

**Pregunta**:
Implementa una clase `RateLimiter` que:
1. Registre requests por cliente
2. Verifique si un cliente puede hacer más requests
3. Limpie requests antiguos (fuera de la ventana)
4. Devuelva tiempo restante si está bloqueado

**Pista**:
Mantén un diccionario con listas de timestamps y filtra los que están fuera de la ventana.

---

### Ejercicio 7: Comparación de Modelos A/B
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**RecommendAI** está probando un nuevo modelo de recomendaciones (modelo B) contra el actual (modelo A).

**Datos**:
```python
import numpy as np

# Resultados del A/B test (1 = conversión, 0 = no conversión)
model_a_results = np.array([1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1])  # 7/15 = 46.7%
model_b_results = np.array([1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1])  # 11/15 = 73.3%

# Latencias en ms
model_a_latency = np.array([45, 52, 48, 51, 47, 53, 49, 46, 50, 48])
model_b_latency = np.array([62, 71, 68, 75, 64, 69, 73, 66, 70, 67])
```

**Pregunta**:
Implementa una función `compare_models` que:
1. Calcule tasa de conversión de cada modelo
2. Calcule latencia promedio y P95
3. Determine si la diferencia es estadísticamente significativa (test chi-cuadrado)
4. Recomiende qué modelo usar considerando conversión y latencia

**Pista**:
Usa `scipy.stats.chi2_contingency` para el test estadístico.

---

### Ejercicio 8: Model Registry Básico
**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**MLOps Team** necesita un registry simple para gestionar versiones de modelos.

**Datos**:
```python
# Modelos a registrar
models_to_register = [
    {
        "name": "churn_predictor",
        "version": "1.0.0",
        "metrics": {"accuracy": 0.85, "f1": 0.82},
        "path": "models/churn_v1.pkl"
    },
    {
        "name": "churn_predictor",
        "version": "1.1.0",
        "metrics": {"accuracy": 0.88, "f1": 0.85},
        "path": "models/churn_v1.1.pkl"
    },
    {
        "name": "fraud_detector",
        "version": "2.0.0",
        "metrics": {"precision": 0.92, "recall": 0.78},
        "path": "models/fraud_v2.pkl"
    }
]
```

**Pregunta**:
Implementa una clase `SimpleRegistry` que:
1. Registre modelos con sus versiones y métricas
2. Liste todas las versiones de un modelo
3. Obtenga la mejor versión según una métrica específica
4. Marque una versión como "production"

**Pista**:
Usa un diccionario anidado: `{model_name: {version: info}}`.

---

## Ejercicios Avanzados

### Ejercicio 9: Pipeline de Validación Pre-Deploy
**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
**SafeML Platform** requiere que todos los modelos pasen validaciones antes de desplegarse.

**Datos**:
```python
import numpy as np

# Modelo nuevo a validar
class MockModel:
    def predict(self, X):
        return np.array([0, 1, 1, 0, 1])

    def predict_proba(self, X):
        return np.array([
            [0.8, 0.2],
            [0.3, 0.7],
            [0.4, 0.6],
            [0.9, 0.1],
            [0.25, 0.75]
        ])

new_model = MockModel()

# Datos de validación
X_val = np.random.randn(5, 4)
y_val = np.array([0, 1, 1, 0, 1])

# Configuración de validación
validation_config = {
    "min_accuracy": 0.80,
    "min_precision": 0.75,
    "max_latency_ms": 100,
    "required_methods": ["predict", "predict_proba"],
    "input_shape": (None, 4)
}
```

**Pregunta**:
Implementa una función `validate_model_for_deployment` que:
1. Verifique que el modelo tiene los métodos requeridos
2. Valide que acepta el shape de input correcto
3. Mida latencia de predicción
4. Calcule métricas y compare con umbrales
5. Devuelva un reporte detallado pass/fail

**Pista**:
Usa `hasattr()` para verificar métodos y `time.time()` para medir latencia.

---

### Ejercicio 10: Sistema de Alertas
**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
**MonitorML** necesita un sistema de alertas que notifique cuando hay problemas con el modelo en producción.

**Datos**:
```python
# Métricas de las últimas 24 horas (por hora)
hourly_metrics = {
    "latency_p99_ms": [45, 48, 52, 55, 120, 150, 180, 95, 88, 75, 65, 58,
                       52, 50, 48, 47, 200, 220, 250, 85, 72, 65, 58, 52],
    "error_rate": [0.01, 0.01, 0.02, 0.01, 0.05, 0.08, 0.12, 0.03, 0.02, 0.01,
                   0.01, 0.01, 0.01, 0.02, 0.01, 0.01, 0.15, 0.18, 0.22, 0.04,
                   0.02, 0.01, 0.01, 0.01],
    "prediction_volume": [100, 95, 80, 60, 45, 40, 35, 50, 120, 180, 220, 250,
                          280, 300, 290, 270, 240, 200, 150, 100, 80, 60, 45, 40]
}

# Umbrales de alerta
alert_thresholds = {
    "latency_p99_ms": {"warning": 100, "critical": 200},
    "error_rate": {"warning": 0.05, "critical": 0.10},
    "prediction_volume_drop": {"warning": 0.3, "critical": 0.5}  # % drop vs promedio
}
```

**Pregunta**:
Implementa una clase `AlertSystem` que:
1. Analice métricas y detecte anomalías
2. Genere alertas con severidad (warning/critical)
3. Evite alertas duplicadas (cooldown de 1 hora)
4. Produzca un resumen de las últimas 24 horas

**Pista**:
Compara cada métrica con su umbral y mantén un historial de alertas enviadas.

---

## Soluciones

### Solución Ejercicio 1

```python
from pydantic import BaseModel, Field, validator
from typing import List


class RecommendationInput(BaseModel):
    """Esquema de validación para input de recomendación."""

    user_id: str = Field(..., min_length=4, description="ID del usuario")
    age: int = Field(..., ge=13, le=120, description="Edad del usuario")
    purchase_history: List[float] = Field(
        ..., min_items=1, description="Historial de compras"
    )
    category_preference: str = Field(..., description="Categoría preferida")
    session_duration_minutes: float = Field(..., gt=0, description="Duración sesión")

    @validator("user_id")
    def user_id_must_start_with_usr(cls, v):
        """Validar que user_id empieza con USR."""
        if not v.startswith("USR"):
            raise ValueError("user_id debe empezar con 'USR'")
        return v

    @validator("category_preference")
    def validate_category(cls, v):
        """Validar categoría permitida."""
        valid_categories = ["electronics", "clothing", "home", "sports"]
        if v not in valid_categories:
            raise ValueError(f"category_preference debe ser uno de: {valid_categories}")
        return v

    @validator("purchase_history")
    def validate_purchases(cls, v):
        """Validar que todas las compras son positivas."""
        if not all(amount > 0 for amount in v):
            raise ValueError("Todos los montos deben ser positivos")
        return v


# Test
valid_input = {
    "user_id": "USR123",
    "age": 28,
    "purchase_history": [45.99, 120.50, 89.00],
    "category_preference": "electronics",
    "session_duration_minutes": 15.5
}

try:
    validated = RecommendationInput(**valid_input)
    print(f"Validación exitosa: {validated.user_id}")
except Exception as e:
    print(f"Error de validación: {e}")

# Test con input inválido
invalid_input = {**valid_input, "user_id": "ABC123"}  # No empieza con USR
try:
    RecommendationInput(**invalid_input)
except Exception as e:
    print(f"Error esperado: {e}")
```

**Resultado esperado**:
```
Validación exitosa: USR123
Error esperado: user_id debe empezar con 'USR'
```

---

### Solución Ejercicio 2

```python
from typing import Dict, Any


def check_health(components: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Verificar salud de componentes del servicio.

    Args:
        components: Estado de cada componente

    Returns:
        Reporte de salud del servicio
    """
    critical_components = ["model", "database"]
    non_critical_components = ["cache"]

    component_status = {}
    critical_failures = []
    non_critical_failures = []

    for name, info in components.items():
        # Determinar si el componente está funcionando
        is_healthy = info.get("loaded", info.get("connected", info.get("available", False)))

        component_status[name] = {
            "healthy": is_healthy,
            "details": info
        }

        if not is_healthy:
            if name in critical_components:
                critical_failures.append(name)
            elif name in non_critical_components:
                non_critical_failures.append(name)

    # Determinar status general
    if critical_failures:
        status = "unhealthy"
    elif non_critical_failures:
        status = "degraded"
    else:
        status = "healthy"

    return {
        "status": status,
        "components": component_status,
        "critical_failures": critical_failures,
        "non_critical_failures": non_critical_failures
    }


# Test
components = {
    "model": {"loaded": True, "version": "2.1.0"},
    "database": {"connected": True, "latency_ms": 5.2},
    "cache": {"available": False, "error": "Connection timeout"}
}

result = check_health(components)
print(f"Status: {result['status']}")  # degraded
print(f"Fallos no críticos: {result['non_critical_failures']}")  # ['cache']

# Test con fallo crítico
components["database"]["connected"] = False
result = check_health(components)
print(f"Status con fallo crítico: {result['status']}")  # unhealthy
```

---

### Solución Ejercicio 3

```python
from datetime import datetime
from typing import Dict, Any, List, Optional
import json


def log_prediction(
    request_id: str,
    input_data: Dict[str, Any],
    prediction: Dict[str, Any],
    latency_ms: float,
    pii_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Crear log estructurado de predicción.

    Args:
        request_id: ID de la solicitud
        input_data: Datos de entrada
        prediction: Resultado de predicción
        latency_ms: Latencia en ms
        pii_fields: Campos PII a remover

    Returns:
        Log estructurado (JSON-serializable)
    """
    if pii_fields is None:
        pii_fields = ["email", "customer_id", "phone", "ssn", "address", "name"]

    # Sanitizar input
    sanitized_input = {
        k: v for k, v in input_data.items()
        if k.lower() not in [f.lower() for f in pii_fields]
    }

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request_id": request_id,
        "event": "prediction",
        "input": sanitized_input,
        "output": prediction,
        "latency_ms": latency_ms
    }

    return log_entry


# Test
request_id = "req-abc-123"
input_data = {
    "customer_id": "CUST001",
    "email": "john@example.com",
    "age": 35,
    "vehicle_year": 2020,
    "claims_last_5_years": 1
}
prediction = {"risk_score": 0.23, "category": "low"}
latency_ms = 45.2

log = log_prediction(request_id, input_data, prediction, latency_ms)
print(json.dumps(log, indent=2))

# Verificar que PII fue removido
assert "email" not in log["input"]
assert "customer_id" not in log["input"]
assert "age" in log["input"]
print("\nPII correctamente removido")
```

---

### Solución Ejercicio 4

```python
import joblib
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple


def compute_checksum(file_path: Path) -> str:
    """Calcular MD5 de un archivo."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def save_model_bundle(
    model: Any,
    metadata: Dict[str, Any],
    output_dir: str
) -> Dict[str, str]:
    """
    Guardar modelo con metadata.

    Args:
        model: Modelo entrenado
        metadata: Información del modelo
        output_dir: Directorio de salida

    Returns:
        Rutas de los archivos guardados
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Guardar modelo
    model_path = output_path / "model.pkl"
    joblib.dump(model, model_path)

    # Calcular checksum
    checksum = compute_checksum(model_path)

    # Agregar checksum a metadata
    full_metadata = {
        **metadata,
        "checksum": checksum,
        "model_file": "model.pkl"
    }

    # Guardar metadata
    metadata_path = output_path / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(full_metadata, f, indent=2)

    return {
        "model_path": str(model_path),
        "metadata_path": str(metadata_path),
        "checksum": checksum
    }


def load_model_bundle(
    bundle_dir: str,
    verify_checksum: bool = True
) -> Tuple[Any, Dict[str, Any]]:
    """
    Cargar modelo y verificar integridad.

    Args:
        bundle_dir: Directorio del bundle
        verify_checksum: Si verificar checksum

    Returns:
        Tupla (modelo, metadata)

    Raises:
        ValueError: Si checksum no coincide
    """
    bundle_path = Path(bundle_dir)

    # Cargar metadata
    with open(bundle_path / "metadata.json", "r") as f:
        metadata = json.load(f)

    # Cargar modelo
    model_path = bundle_path / metadata["model_file"]
    model = joblib.load(model_path)

    # Verificar checksum
    if verify_checksum:
        current_checksum = compute_checksum(model_path)
        if current_checksum != metadata["checksum"]:
            raise ValueError(
                f"Checksum no coincide. Esperado: {metadata['checksum']}, "
                f"Actual: {current_checksum}"
            )

    return model, metadata


# Test
from sklearn.ensemble import RandomForestClassifier
import numpy as np

X = np.random.randn(100, 4)
y = np.random.randint(0, 2, 100)
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

metadata = {
    "model_name": "fraud_detector",
    "version": "1.0.0",
    "features": ["amount", "time", "location_score", "device_score"],
    "trained_at": "2025-01-15"
}

# Guardar
result = save_model_bundle(model, metadata, "test_bundle")
print(f"Bundle guardado: {result}")

# Cargar
loaded_model, loaded_metadata = load_model_bundle("test_bundle")
print(f"\nMetadata cargado: {loaded_metadata['model_name']} v{loaded_metadata['version']}")
print(f"Checksum verificado: {loaded_metadata['checksum']}")

# Cleanup
import shutil
shutil.rmtree("test_bundle")
```

---

### Solución Ejercicio 5

```python
import numpy as np
from typing import Dict, List


def simple_drift_check(
    reference_data: Dict[str, np.ndarray],
    production_data: Dict[str, np.ndarray],
    threshold_std: float = 2.0
) -> Dict[str, Any]:
    """
    Detectar drift comparando medias y desviaciones.

    Args:
        reference_data: Datos de referencia por feature
        production_data: Datos de producción por feature
        threshold_std: Umbral en número de desviaciones estándar

    Returns:
        Reporte de drift
    """
    report = {
        "features_analyzed": 0,
        "features_with_drift": [],
        "details": {}
    }

    for feature_name in reference_data.keys():
        ref = reference_data[feature_name]
        prod = production_data.get(feature_name)

        if prod is None:
            continue

        report["features_analyzed"] += 1

        # Calcular estadísticas
        ref_mean = np.mean(ref)
        ref_std = np.std(ref)
        prod_mean = np.mean(prod)
        prod_std = np.std(prod)

        # Calcular z-score de la diferencia
        if ref_std > 0:
            z_score = abs(prod_mean - ref_mean) / ref_std
        else:
            z_score = 0 if prod_mean == ref_mean else float('inf')

        drift_detected = z_score > threshold_std

        report["details"][feature_name] = {
            "reference_mean": float(ref_mean),
            "reference_std": float(ref_std),
            "production_mean": float(prod_mean),
            "production_std": float(prod_std),
            "z_score": float(z_score),
            "drift_detected": drift_detected
        }

        if drift_detected:
            report["features_with_drift"].append(feature_name)

    report["drift_alert"] = len(report["features_with_drift"]) > 0

    return report


# Test
reference_income = np.array([45000, 52000, 38000, 61000, 48000, 55000, 42000, 59000])
reference_age = np.array([28, 35, 42, 31, 45, 38, 29, 52])

production_income = np.array([72000, 85000, 68000, 91000, 78000, 82000, 75000, 88000])
production_age = np.array([30, 33, 40, 35, 42, 37, 31, 48])

result = simple_drift_check(
    {"income": reference_income, "age": reference_age},
    {"income": production_income, "age": production_age}
)

print(f"Alerta de drift: {result['drift_alert']}")
print(f"Features con drift: {result['features_with_drift']}")
for feature, details in result["details"].items():
    print(f"\n{feature}:")
    print(f"  Ref mean: {details['reference_mean']:.2f}")
    print(f"  Prod mean: {details['production_mean']:.2f}")
    print(f"  Z-score: {details['z_score']:.2f}")
    print(f"  Drift: {details['drift_detected']}")
```

---

### Solución Ejercicio 6

```python
from typing import Dict, List, Tuple
import time


class RateLimiter:
    """Rate limiter basado en ventana deslizante."""

    def __init__(self, max_requests: int, window_seconds: int):
        """
        Inicializar rate limiter.

        Args:
            max_requests: Máximo de requests por ventana
            window_seconds: Tamaño de ventana en segundos
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_history: Dict[str, List[float]] = {}

    def _cleanup_old_requests(self, client_id: str, current_time: float) -> None:
        """Remover requests fuera de la ventana."""
        if client_id not in self.request_history:
            return

        cutoff = current_time - self.window_seconds
        self.request_history[client_id] = [
            ts for ts in self.request_history[client_id]
            if ts > cutoff
        ]

    def is_allowed(self, client_id: str, current_time: float = None) -> Tuple[bool, dict]:
        """
        Verificar si el cliente puede hacer un request.

        Args:
            client_id: ID del cliente
            current_time: Timestamp actual (para testing)

        Returns:
            Tupla (permitido, info)
        """
        if current_time is None:
            current_time = time.time()

        # Limpiar requests antiguos
        self._cleanup_old_requests(client_id, current_time)

        # Obtener historial actual
        history = self.request_history.get(client_id, [])
        current_count = len(history)

        if current_count >= self.max_requests:
            # Calcular tiempo hasta que expire el request más antiguo
            oldest = min(history)
            wait_seconds = oldest + self.window_seconds - current_time

            return False, {
                "allowed": False,
                "current_count": current_count,
                "limit": self.max_requests,
                "retry_after_seconds": max(0, wait_seconds)
            }

        return True, {
            "allowed": True,
            "current_count": current_count,
            "limit": self.max_requests,
            "remaining": self.max_requests - current_count - 1
        }

    def record_request(self, client_id: str, current_time: float = None) -> None:
        """Registrar un request."""
        if current_time is None:
            current_time = time.time()

        if client_id not in self.request_history:
            self.request_history[client_id] = []

        self.request_history[client_id].append(current_time)


# Test
limiter = RateLimiter(max_requests=5, window_seconds=60)

# Simular requests de client_A
base_time = 1705320000
for i in range(5):
    allowed, info = limiter.is_allowed("client_A", base_time + i)
    if allowed:
        limiter.record_request("client_A", base_time + i)
        print(f"Request {i+1}: Permitido, restantes: {info['remaining']}")

# 6to request debería ser bloqueado
allowed, info = limiter.is_allowed("client_A", base_time + 5)
print(f"\nRequest 6: {'Permitido' if allowed else 'Bloqueado'}")
print(f"Reintentar en: {info.get('retry_after_seconds', 0):.1f} segundos")

# Después de 60 segundos, debería permitir de nuevo
allowed, info = limiter.is_allowed("client_A", base_time + 65)
print(f"\nDespués de 65s: {'Permitido' if allowed else 'Bloqueado'}")
```

---

### Solución Ejercicio 7

```python
import numpy as np
from scipy import stats
from typing import Dict, Any


def compare_models(
    model_a_conversions: np.ndarray,
    model_b_conversions: np.ndarray,
    model_a_latency: np.ndarray,
    model_b_latency: np.ndarray,
    significance_level: float = 0.05,
    max_acceptable_latency_increase: float = 0.5  # 50%
) -> Dict[str, Any]:
    """
    Comparar dos modelos en A/B test.

    Args:
        model_a_conversions: Resultados modelo A (0/1)
        model_b_conversions: Resultados modelo B (0/1)
        model_a_latency: Latencias modelo A
        model_b_latency: Latencias modelo B
        significance_level: Nivel de significancia para test
        max_acceptable_latency_increase: Máximo incremento aceptable de latencia

    Returns:
        Reporte de comparación
    """
    # Calcular tasas de conversión
    conv_a = np.mean(model_a_conversions)
    conv_b = np.mean(model_b_conversions)

    # Calcular estadísticas de latencia
    lat_a_mean = np.mean(model_a_latency)
    lat_a_p95 = np.percentile(model_a_latency, 95)
    lat_b_mean = np.mean(model_b_latency)
    lat_b_p95 = np.percentile(model_b_latency, 95)

    # Test chi-cuadrado para conversiones
    # Tabla de contingencia: [[conv_a, no_conv_a], [conv_b, no_conv_b]]
    n_a = len(model_a_conversions)
    n_b = len(model_b_conversions)
    conv_a_count = np.sum(model_a_conversions)
    conv_b_count = np.sum(model_b_conversions)

    contingency_table = [
        [conv_a_count, n_a - conv_a_count],
        [conv_b_count, n_b - conv_b_count]
    ]

    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    significant_difference = p_value < significance_level

    # Calcular incremento de latencia
    latency_increase = (lat_b_mean - lat_a_mean) / lat_a_mean

    # Determinar recomendación
    if conv_b > conv_a and significant_difference:
        if latency_increase <= max_acceptable_latency_increase:
            recommendation = "Usar Modelo B"
            reason = f"B tiene mejor conversión ({conv_b:.1%} vs {conv_a:.1%}) con diferencia significativa"
        else:
            recommendation = "Revisar Modelo B"
            reason = f"B convierte mejor pero latencia aumenta {latency_increase:.1%}"
    elif conv_a >= conv_b:
        recommendation = "Mantener Modelo A"
        reason = "A tiene igual o mejor conversión"
    else:
        recommendation = "Continuar test"
        reason = f"Diferencia no significativa (p-value: {p_value:.4f})"

    return {
        "model_a": {
            "conversion_rate": float(conv_a),
            "sample_size": n_a,
            "latency_mean_ms": float(lat_a_mean),
            "latency_p95_ms": float(lat_a_p95)
        },
        "model_b": {
            "conversion_rate": float(conv_b),
            "sample_size": n_b,
            "latency_mean_ms": float(lat_b_mean),
            "latency_p95_ms": float(lat_b_p95)
        },
        "comparison": {
            "conversion_difference": float(conv_b - conv_a),
            "latency_increase_pct": float(latency_increase * 100),
            "chi2_statistic": float(chi2),
            "p_value": float(p_value),
            "statistically_significant": significant_difference
        },
        "recommendation": recommendation,
        "reason": reason
    }


# Test
model_a_results = np.array([1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1])
model_b_results = np.array([1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1])
model_a_latency = np.array([45, 52, 48, 51, 47, 53, 49, 46, 50, 48])
model_b_latency = np.array([62, 71, 68, 75, 64, 69, 73, 66, 70, 67])

result = compare_models(
    model_a_results, model_b_results,
    model_a_latency, model_b_latency
)

print(f"Modelo A: {result['model_a']['conversion_rate']:.1%} conversión, "
      f"{result['model_a']['latency_mean_ms']:.1f}ms latencia")
print(f"Modelo B: {result['model_b']['conversion_rate']:.1%} conversión, "
      f"{result['model_b']['latency_mean_ms']:.1f}ms latencia")
print(f"\nDiferencia significativa: {result['comparison']['statistically_significant']}")
print(f"P-value: {result['comparison']['p_value']:.4f}")
print(f"\nRecomendación: {result['recommendation']}")
print(f"Razón: {result['reason']}")
```

---

### Solución Ejercicio 8

```python
from typing import Dict, List, Any, Optional


class SimpleRegistry:
    """Registry simple para modelos ML."""

    def __init__(self):
        """Inicializar registry."""
        self.models: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self.production: Dict[str, str] = {}  # model_name -> version

    def register(
        self,
        name: str,
        version: str,
        metrics: Dict[str, float],
        path: str
    ) -> Dict[str, Any]:
        """Registrar un modelo."""
        if name not in self.models:
            self.models[name] = {}

        self.models[name][version] = {
            "metrics": metrics,
            "path": path,
            "registered_at": "2025-01-15T10:00:00"
        }

        return {"status": "registered", "name": name, "version": version}

    def list_versions(self, name: str) -> List[str]:
        """Listar versiones de un modelo."""
        if name not in self.models:
            return []
        return list(self.models[name].keys())

    def get_best_version(
        self,
        name: str,
        metric: str,
        higher_is_better: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Obtener mejor versión según métrica."""
        if name not in self.models:
            return None

        best_version = None
        best_value = None

        for version, info in self.models[name].items():
            value = info["metrics"].get(metric)
            if value is None:
                continue

            if best_value is None:
                best_version = version
                best_value = value
            elif higher_is_better and value > best_value:
                best_version = version
                best_value = value
            elif not higher_is_better and value < best_value:
                best_version = version
                best_value = value

        if best_version is None:
            return None

        return {
            "version": best_version,
            "metric": metric,
            "value": best_value,
            **self.models[name][best_version]
        }

    def set_production(self, name: str, version: str) -> Dict[str, Any]:
        """Marcar versión como producción."""
        if name not in self.models or version not in self.models[name]:
            raise ValueError(f"Modelo {name}:{version} no encontrado")

        previous = self.production.get(name)
        self.production[name] = version

        return {
            "status": "production_set",
            "name": name,
            "version": version,
            "previous_version": previous
        }

    def get_production(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtener versión en producción."""
        if name not in self.production:
            return None

        version = self.production[name]
        return {
            "version": version,
            **self.models[name][version]
        }


# Test
registry = SimpleRegistry()

# Registrar modelos
models_to_register = [
    {"name": "churn_predictor", "version": "1.0.0",
     "metrics": {"accuracy": 0.85, "f1": 0.82}, "path": "models/churn_v1.pkl"},
    {"name": "churn_predictor", "version": "1.1.0",
     "metrics": {"accuracy": 0.88, "f1": 0.85}, "path": "models/churn_v1.1.pkl"},
    {"name": "fraud_detector", "version": "2.0.0",
     "metrics": {"precision": 0.92, "recall": 0.78}, "path": "models/fraud_v2.pkl"}
]

for m in models_to_register:
    registry.register(**m)
    print(f"Registrado: {m['name']} v{m['version']}")

# Listar versiones
print(f"\nVersiones de churn_predictor: {registry.list_versions('churn_predictor')}")

# Obtener mejor versión
best = registry.get_best_version("churn_predictor", "accuracy")
print(f"\nMejor versión por accuracy: {best['version']} ({best['value']})")

# Marcar producción
registry.set_production("churn_predictor", "1.1.0")
prod = registry.get_production("churn_predictor")
print(f"\nEn producción: v{prod['version']}")
```

---

### Solución Ejercicio 9

```python
import time
import numpy as np
from typing import Dict, Any, List
from sklearn.metrics import accuracy_score, precision_score


def validate_model_for_deployment(
    model: Any,
    X_val: np.ndarray,
    y_val: np.ndarray,
    config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validar modelo antes del despliegue.

    Args:
        model: Modelo a validar
        X_val: Datos de validación
        y_val: Labels de validación
        config: Configuración de validación

    Returns:
        Reporte de validación
    """
    report = {
        "passed": True,
        "checks": [],
        "metrics": {},
        "errors": []
    }

    # 1. Verificar métodos requeridos
    for method in config.get("required_methods", []):
        has_method = hasattr(model, method) and callable(getattr(model, method))
        check = {
            "name": f"method_{method}",
            "passed": has_method,
            "message": f"Método {method}: {'Presente' if has_method else 'Ausente'}"
        }
        report["checks"].append(check)
        if not has_method:
            report["passed"] = False
            report["errors"].append(f"Método requerido ausente: {method}")

    # 2. Verificar shape de input
    expected_shape = config.get("input_shape")
    if expected_shape:
        try:
            # Intentar predicción para verificar shape
            _ = model.predict(X_val[:1])
            check = {
                "name": "input_shape",
                "passed": True,
                "message": f"Shape de input válido: {X_val.shape}"
            }
        except Exception as e:
            check = {
                "name": "input_shape",
                "passed": False,
                "message": f"Error con shape de input: {e}"
            }
            report["passed"] = False
            report["errors"].append(str(e))
        report["checks"].append(check)

    # 3. Medir latencia
    max_latency = config.get("max_latency_ms", 100)
    latencies = []
    for _ in range(10):
        start = time.time()
        _ = model.predict(X_val[:1])
        latencies.append((time.time() - start) * 1000)

    avg_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)

    check = {
        "name": "latency",
        "passed": p95_latency <= max_latency,
        "message": f"Latencia P95: {p95_latency:.2f}ms (máx: {max_latency}ms)"
    }
    report["checks"].append(check)
    report["metrics"]["latency_avg_ms"] = float(avg_latency)
    report["metrics"]["latency_p95_ms"] = float(p95_latency)

    if p95_latency > max_latency:
        report["passed"] = False
        report["errors"].append(f"Latencia excede límite: {p95_latency:.2f}ms > {max_latency}ms")

    # 4. Calcular métricas
    predictions = model.predict(X_val)

    accuracy = accuracy_score(y_val, predictions)
    report["metrics"]["accuracy"] = float(accuracy)

    min_accuracy = config.get("min_accuracy", 0.8)
    check = {
        "name": "accuracy",
        "passed": accuracy >= min_accuracy,
        "message": f"Accuracy: {accuracy:.4f} (mín: {min_accuracy})"
    }
    report["checks"].append(check)

    if accuracy < min_accuracy:
        report["passed"] = False
        report["errors"].append(f"Accuracy bajo: {accuracy:.4f} < {min_accuracy}")

    # Precision si aplica
    try:
        precision = precision_score(y_val, predictions, zero_division=0)
        report["metrics"]["precision"] = float(precision)

        min_precision = config.get("min_precision", 0.75)
        check = {
            "name": "precision",
            "passed": precision >= min_precision,
            "message": f"Precision: {precision:.4f} (mín: {min_precision})"
        }
        report["checks"].append(check)

        if precision < min_precision:
            report["passed"] = False
            report["errors"].append(f"Precision bajo: {precision:.4f} < {min_precision}")
    except Exception:
        pass

    return report


# Test
class MockModel:
    def predict(self, X):
        return np.array([0, 1, 1, 0, 1])

    def predict_proba(self, X):
        return np.array([[0.8, 0.2], [0.3, 0.7], [0.4, 0.6], [0.9, 0.1], [0.25, 0.75]])


model = MockModel()
X_val = np.random.randn(5, 4)
y_val = np.array([0, 1, 1, 0, 1])

config = {
    "min_accuracy": 0.80,
    "min_precision": 0.75,
    "max_latency_ms": 100,
    "required_methods": ["predict", "predict_proba"],
    "input_shape": (None, 4)
}

result = validate_model_for_deployment(model, X_val, y_val, config)

print(f"Validación: {'PASÓ' if result['passed'] else 'FALLÓ'}")
print(f"\nChecks:")
for check in result["checks"]:
    status = "✓" if check["passed"] else "✗"
    print(f"  {status} {check['message']}")

print(f"\nMétricas: {result['metrics']}")

if result["errors"]:
    print(f"\nErrores: {result['errors']}")
```

---

### Solución Ejercicio 10

```python
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict


class AlertSystem:
    """Sistema de alertas para monitoreo de modelos."""

    def __init__(self, thresholds: Dict[str, Dict[str, float]], cooldown_hours: int = 1):
        """
        Inicializar sistema de alertas.

        Args:
            thresholds: Umbrales por métrica {metric: {warning: x, critical: y}}
            cooldown_hours: Horas de cooldown entre alertas del mismo tipo
        """
        self.thresholds = thresholds
        self.cooldown_hours = cooldown_hours
        self.alert_history: List[Dict[str, Any]] = []
        self.last_alert_time: Dict[str, int] = defaultdict(int)

    def _check_cooldown(self, alert_key: str, current_hour: int) -> bool:
        """Verificar si pasó el cooldown."""
        last_hour = self.last_alert_time.get(alert_key, -self.cooldown_hours - 1)
        return current_hour - last_hour >= self.cooldown_hours

    def _determine_severity(
        self,
        metric: str,
        value: float
    ) -> tuple[str, bool]:
        """Determinar severidad de alerta."""
        if metric not in self.thresholds:
            return "none", False

        thresholds = self.thresholds[metric]
        critical = thresholds.get("critical")
        warning = thresholds.get("warning")

        if critical is not None and value >= critical:
            return "critical", True
        elif warning is not None and value >= warning:
            return "warning", True

        return "none", False

    def analyze_metrics(
        self,
        hourly_metrics: Dict[str, List[float]],
        start_hour: int = 0
    ) -> Dict[str, Any]:
        """
        Analizar métricas y generar alertas.

        Args:
            hourly_metrics: Métricas por hora
            start_hour: Hora de inicio para tracking

        Returns:
            Reporte con alertas
        """
        alerts = []
        summary = {
            "total_hours": 0,
            "alerts_generated": 0,
            "alerts_suppressed": 0,
            "by_severity": {"warning": 0, "critical": 0}
        }

        # Procesar cada hora
        for hour_idx in range(len(list(hourly_metrics.values())[0])):
            current_hour = start_hour + hour_idx
            summary["total_hours"] += 1

            for metric, values in hourly_metrics.items():
                value = values[hour_idx]
                severity, should_alert = self._determine_severity(metric, value)

                if should_alert:
                    alert_key = f"{metric}_{severity}"

                    if self._check_cooldown(alert_key, current_hour):
                        alert = {
                            "hour": current_hour,
                            "metric": metric,
                            "value": value,
                            "severity": severity,
                            "threshold": self.thresholds[metric][severity]
                        }
                        alerts.append(alert)
                        self.alert_history.append(alert)
                        self.last_alert_time[alert_key] = current_hour
                        summary["alerts_generated"] += 1
                        summary["by_severity"][severity] += 1
                    else:
                        summary["alerts_suppressed"] += 1

            # Verificar caída de volumen
            if "prediction_volume" in hourly_metrics:
                volumes = hourly_metrics["prediction_volume"]
                if hour_idx > 0:
                    avg_volume = sum(volumes[:hour_idx]) / hour_idx
                    current_volume = volumes[hour_idx]

                    if avg_volume > 0:
                        drop_pct = (avg_volume - current_volume) / avg_volume

                        if drop_pct > 0:
                            severity, should_alert = self._check_volume_drop(drop_pct)
                            if should_alert:
                                alert_key = f"volume_drop_{severity}"
                                if self._check_cooldown(alert_key, current_hour):
                                    alert = {
                                        "hour": current_hour,
                                        "metric": "prediction_volume_drop",
                                        "value": drop_pct,
                                        "severity": severity,
                                        "current_volume": current_volume,
                                        "avg_volume": avg_volume
                                    }
                                    alerts.append(alert)
                                    self.last_alert_time[alert_key] = current_hour
                                    summary["alerts_generated"] += 1
                                    summary["by_severity"][severity] += 1

        return {
            "alerts": alerts,
            "summary": summary,
            "total_alerts_in_history": len(self.alert_history)
        }

    def _check_volume_drop(self, drop_pct: float) -> tuple[str, bool]:
        """Verificar caída de volumen."""
        thresholds = self.thresholds.get("prediction_volume_drop", {})
        critical = thresholds.get("critical", 0.5)
        warning = thresholds.get("warning", 0.3)

        if drop_pct >= critical:
            return "critical", True
        elif drop_pct >= warning:
            return "warning", True
        return "none", False

    def get_summary(self) -> Dict[str, Any]:
        """Obtener resumen de las últimas alertas."""
        if not self.alert_history:
            return {"message": "No hay alertas en el historial"}

        by_metric = defaultdict(list)
        for alert in self.alert_history:
            by_metric[alert["metric"]].append(alert)

        return {
            "total_alerts": len(self.alert_history),
            "by_metric": {
                metric: {
                    "count": len(alerts),
                    "severities": [a["severity"] for a in alerts]
                }
                for metric, alerts in by_metric.items()
            },
            "most_recent": self.alert_history[-5:]
        }


# Test
thresholds = {
    "latency_p99_ms": {"warning": 100, "critical": 200},
    "error_rate": {"warning": 0.05, "critical": 0.10},
    "prediction_volume_drop": {"warning": 0.3, "critical": 0.5}
}

alert_system = AlertSystem(thresholds, cooldown_hours=1)

hourly_metrics = {
    "latency_p99_ms": [45, 48, 52, 55, 120, 150, 180, 95, 88, 75, 65, 58,
                       52, 50, 48, 47, 200, 220, 250, 85, 72, 65, 58, 52],
    "error_rate": [0.01, 0.01, 0.02, 0.01, 0.05, 0.08, 0.12, 0.03, 0.02, 0.01,
                   0.01, 0.01, 0.01, 0.02, 0.01, 0.01, 0.15, 0.18, 0.22, 0.04,
                   0.02, 0.01, 0.01, 0.01],
    "prediction_volume": [100, 95, 80, 60, 45, 40, 35, 50, 120, 180, 220, 250,
                          280, 300, 290, 270, 240, 200, 150, 100, 80, 60, 45, 40]
}

result = alert_system.analyze_metrics(hourly_metrics)

print(f"Alertas generadas: {result['summary']['alerts_generated']}")
print(f"Alertas suprimidas (cooldown): {result['summary']['alerts_suppressed']}")
print(f"Por severidad: {result['summary']['by_severity']}")

print("\nAlertas:")
for alert in result["alerts"][:10]:  # Primeras 10
    print(f"  Hora {alert['hour']}: {alert['metric']} = {alert['value']:.4f} "
          f"[{alert['severity'].upper()}]")

summary = alert_system.get_summary()
print(f"\nResumen por métrica: {dict(summary['by_metric'])}")
```

---

## Resumen de Ejercicios

| Ejercicio | Nivel | Tema | Habilidades |
|-----------|-------|------|-------------|
| 1 | Básico | Validación Pydantic | Esquemas, validators |
| 2 | Básico | Health Check | Estados de servicio |
| 3 | Básico | Logging | Sanitización, estructura |
| 4 | Básico | Serialización | joblib, checksums |
| 5 | Intermedio | Drift Detection | Estadística básica |
| 6 | Intermedio | Rate Limiting | Ventanas deslizantes |
| 7 | Intermedio | A/B Testing | Tests estadísticos |
| 8 | Intermedio | Model Registry | Versionado |
| 9 | Avanzado | Validación Deploy | Checks completos |
| 10 | Avanzado | Sistema de Alertas | Monitoreo |
