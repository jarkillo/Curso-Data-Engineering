"""
Herramientas MLOps para productivización de modelos.

Este módulo proporciona funciones y clases para:
- Detección de data drift
- Gestión de versiones de modelos (Model Registry)
- Logging estructurado de predicciones
- Validación de modelos antes del despliegue
- Sistema de alertas para monitoreo

Ejemplo de uso:
    >>> from src.mlops_tools import detect_drift_ks, ModelRegistry
    >>> result = detect_drift_ks(reference_data, production_data)
    >>> print(f"Drift detectado: {result['drift_detected']}")
"""

import hashlib
import json
import shutil
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib  # noqa: F401 - used in ModelRegistry
import numpy as np
from scipy import stats
from sklearn.metrics import accuracy_score

# ============================================================================
# Drift Detection Functions
# ============================================================================


def detect_drift_ks(
    reference: np.ndarray,
    current: np.ndarray,
    threshold: float = 0.05,
) -> dict[str, Any]:
    """
    Detectar drift usando el test de Kolmogorov-Smirnov.

    El test KS compara las distribuciones acumuladas de dos muestras.
    Un p-value bajo indica que las distribuciones son diferentes.

    Args:
        reference: Datos de referencia (entrenamiento)
        current: Datos actuales (producción)
        threshold: Umbral de p-value para detectar drift

    Returns:
        Diccionario con estadístico, p-value y si hay drift

    Raises:
        ValueError: Si los arrays están vacíos

    Examples:
        >>> ref = np.array([1, 2, 3, 4, 5])
        >>> cur = np.array([1, 2, 3, 4, 5])
        >>> result = detect_drift_ks(ref, cur)
        >>> result['drift_detected']
        False
    """
    if len(reference) == 0 or len(current) == 0:
        raise ValueError("Los arrays no pueden estar vacíos")

    statistic, p_value = stats.ks_2samp(reference, current)

    return {
        "test": "kolmogorov_smirnov",
        "statistic": float(statistic),
        "p_value": float(p_value),
        "threshold": threshold,
        "drift_detected": p_value < threshold,
    }


def detect_drift_psi(
    reference: np.ndarray,
    current: np.ndarray,
    buckets: int = 10,
    threshold: float = 0.2,
) -> dict[str, Any]:
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
        Diccionario con PSI, interpretación y si hay drift

    Raises:
        ValueError: Si los arrays están vacíos

    Examples:
        >>> ref = np.array([1, 2, 3, 4, 5])
        >>> cur = np.array([1, 2, 3, 4, 5])
        >>> result = detect_drift_psi(ref, cur)
        >>> result['interpretation']
        'sin cambio'
    """
    if len(reference) == 0 or len(current) == 0:
        raise ValueError("Los arrays no pueden estar vacíos")

    # Crear buckets basados en referencia
    breakpoints = np.percentile(reference, np.linspace(0, 100, buckets + 1))
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    # Calcular proporciones en cada bucket
    ref_counts = np.histogram(reference, bins=breakpoints)[0]
    cur_counts = np.histogram(current, bins=breakpoints)[0]

    # Evitar división por cero
    ref_pct = (ref_counts + 1) / (len(reference) + buckets)
    cur_pct = (cur_counts + 1) / (len(current) + buckets)

    # Calcular PSI
    psi = float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))

    # Determinar interpretación
    if psi < 0.1:
        interpretation = "sin cambio"
    elif psi < 0.2:
        interpretation = "cambio moderado"
    else:
        interpretation = "cambio significativo"

    return {
        "test": "psi",
        "psi_value": psi,
        "threshold": threshold,
        "drift_detected": psi > threshold,
        "interpretation": interpretation,
    }


def analyze_feature_drift(
    reference_data: dict[str, np.ndarray],
    current_data: dict[str, np.ndarray],
    features: list[str],
    tests: list[str] = None,
) -> dict[str, Any]:
    """
    Analizar drift en múltiples features.

    Args:
        reference_data: Dict con features de referencia
        current_data: Dict con features actuales
        features: Lista de features a analizar
        tests: Tests a aplicar ('ks', 'psi'). Default: ['ks']

    Returns:
        Reporte completo de drift

    Raises:
        ValueError: Si una feature no existe en los datos

    Examples:
        >>> ref = {"age": np.array([25, 30, 35])}
        >>> cur = {"age": np.array([25, 30, 35])}
        >>> report = analyze_feature_drift(ref, cur, ["age"])
        >>> report['drift_alert']
        False
    """
    if tests is None:
        tests = ["ks"]

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "features_analyzed": 0,
        "features_with_drift": 0,
        "details": {},
        "drift_alert": False,
    }

    for feature in features:
        if feature not in reference_data or feature not in current_data:
            continue

        ref = np.array(reference_data[feature])
        cur = np.array(current_data[feature])

        report["features_analyzed"] += 1

        feature_results = {
            "reference_mean": float(np.mean(ref)),
            "reference_std": float(np.std(ref)),
            "current_mean": float(np.mean(cur)),
            "current_std": float(np.std(cur)),
            "tests": {},
            "drift_detected": False,
        }

        if "ks" in tests:
            ks_result = detect_drift_ks(ref, cur)
            feature_results["tests"]["ks"] = ks_result
            if ks_result["drift_detected"]:
                feature_results["drift_detected"] = True

        if "psi" in tests:
            psi_result = detect_drift_psi(ref, cur)
            feature_results["tests"]["psi"] = psi_result
            if psi_result["drift_detected"]:
                feature_results["drift_detected"] = True

        report["details"][feature] = feature_results

        if feature_results["drift_detected"]:
            report["features_with_drift"] += 1

    report["drift_alert"] = report["features_with_drift"] > 0

    return report


# ============================================================================
# Model Registry
# ============================================================================


class ModelRegistry:
    """
    Registry para gestionar versiones de modelos.

    Estructura del registry:
        registry_path/
        ├── index.json
        └── model_name/
            └── version/
                ├── model.pkl
                ├── metadata.json
                └── metrics.json

    Attributes:
        registry_path: Ruta al directorio del registry
        index: Índice de modelos registrados

    Examples:
        >>> registry = ModelRegistry("./my_registry")
        >>> registry.register_model("churn", "1.0.0", "model.pkl", {"acc": 0.9})
        >>> registry.promote_to_production("churn", "1.0.0")
    """

    def __init__(self, registry_path: str):
        """
        Inicializar registry.

        Args:
            registry_path: Ruta al directorio del registry
        """
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.registry_path / "index.json"
        self._load_index()

    def _load_index(self) -> None:
        """Cargar índice del registry."""
        if self.index_path.exists():
            with open(self.index_path) as f:
                self.index = json.load(f)
        else:
            self.index = {
                "models": {},
                "created_at": datetime.utcnow().isoformat(),
            }
            self._save_index()

    def _save_index(self) -> None:
        """Guardar índice."""
        self.index["updated_at"] = datetime.utcnow().isoformat()
        with open(self.index_path, "w") as f:
            json.dump(self.index, f, indent=2)

    def _compute_checksum(self, file_path: Path) -> str:
        """Calcular checksum MD5 de un archivo."""
        hash_md5 = hashlib.md5(usedforsecurity=False)  # noqa: S324
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def register_model(
        self,
        model_name: str,
        version: str,
        model_path: str,
        metrics: dict[str, float],
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Registrar una nueva versión de modelo.

        Args:
            model_name: Nombre del modelo
            version: Versión semántica (e.g., "1.0.0")
            model_path: Ruta al archivo del modelo
            metrics: Métricas de evaluación
            metadata: Metadata adicional opcional

        Returns:
            Información del registro

        Raises:
            FileNotFoundError: Si el modelo no existe
        """
        model_path = Path(model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"Modelo no encontrado: {model_path}")

        # Crear directorio para el modelo
        version_dir = self.registry_path / model_name / version
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
            **(metadata or {}),
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
                "staging_version": None,
            }

        if version not in self.index["models"][model_name]["versions"]:
            self.index["models"][model_name]["versions"].append(version)
        self.index["models"][model_name]["latest_version"] = version
        self._save_index()

        return {
            "status": "registered",
            "model_name": model_name,
            "version": version,
            "path": str(version_dir),
        }

    def promote_to_staging(self, model_name: str, version: str) -> dict[str, Any]:
        """
        Promover versión a staging.

        Args:
            model_name: Nombre del modelo
            version: Versión a promover

        Returns:
            Resultado de la promoción

        Raises:
            ValueError: Si modelo o versión no existen
        """
        if model_name not in self.index["models"]:
            raise ValueError(f"Modelo no encontrado: {model_name}")

        if version not in self.index["models"][model_name]["versions"]:
            raise ValueError(f"Versión no encontrada: {version}")

        self.index["models"][model_name]["staging_version"] = version
        self._save_index()

        return {
            "status": "promoted_to_staging",
            "model_name": model_name,
            "version": version,
        }

    def promote_to_production(self, model_name: str, version: str) -> dict[str, Any]:
        """
        Promover versión a producción.

        Args:
            model_name: Nombre del modelo
            version: Versión a promover

        Returns:
            Resultado de la promoción

        Raises:
            ValueError: Si modelo o versión no existen
        """
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
            "previous_version": previous,
        }

    def rollback(self, model_name: str) -> dict[str, Any]:
        """
        Revertir a versión anterior de producción.

        Args:
            model_name: Nombre del modelo

        Returns:
            Resultado del rollback

        Raises:
            ValueError: Si no hay versión anterior
        """
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
            "to_version": previous,
        }

    def get_production_model_path(self, model_name: str) -> Path:
        """
        Obtener ruta al modelo en producción.

        Args:
            model_name: Nombre del modelo

        Returns:
            Path al archivo del modelo

        Raises:
            ValueError: Si no hay modelo en producción
        """
        if model_name not in self.index["models"]:
            raise ValueError(f"Modelo no encontrado: {model_name}")

        version = self.index["models"][model_name].get("production_version")
        if not version:
            raise ValueError(f"No hay versión en producción: {model_name}")

        return self.registry_path / model_name / version / "model.pkl"


# ============================================================================
# Prediction Logging
# ============================================================================


class PredictionLogger:
    """
    Logger estructurado para predicciones ML.

    Attributes:
        service_name: Nombre del servicio

    Examples:
        >>> logger = PredictionLogger("churn-api")
        >>> entry = logger.create_log_entry(
        ...     request_id="req-123",
        ...     input_data={"age": 35},
        ...     prediction={"class": 1},
        ...     latency_ms=45.2
        ... )
    """

    def __init__(self, service_name: str):
        """
        Inicializar logger.

        Args:
            service_name: Nombre del servicio
        """
        self.service_name = service_name

    def create_log_entry(
        self,
        request_id: str,
        input_data: dict[str, Any],
        prediction: dict[str, Any],
        latency_ms: float,
        model_version: str = "unknown",
    ) -> dict[str, Any]:
        """
        Crear entrada de log estructurada.

        Args:
            request_id: ID único de la solicitud
            input_data: Datos de entrada (ya sanitizados)
            prediction: Resultado de la predicción
            latency_ms: Latencia en milisegundos
            model_version: Versión del modelo

        Returns:
            Diccionario con el log estructurado
        """
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": self.service_name,
            "request_id": request_id,
            "event": "prediction",
            "input": input_data,
            "output": prediction,
            "latency_ms": latency_ms,
            "model_version": model_version,
        }


def sanitize_pii(
    data: dict[str, Any],
    pii_fields: list[str] | None = None,
) -> dict[str, Any]:
    """
    Sanitizar datos removiendo campos PII.

    Args:
        data: Datos originales
        pii_fields: Campos a remover. Default: campos comunes de PII

    Returns:
        Datos sin campos PII

    Examples:
        >>> data = {"age": 35, "email": "test@example.com"}
        >>> sanitize_pii(data)
        {'age': 35}
    """
    if pii_fields is None:
        pii_fields = [
            "email",
            "phone",
            "ssn",
            "address",
            "name",
            "credit_card",
            "customer_id",
        ]

    pii_fields_lower = [f.lower() for f in pii_fields]

    return {k: v for k, v in data.items() if k.lower() not in pii_fields_lower}


# ============================================================================
# Model Validation
# ============================================================================


def validate_model_for_deployment(
    model: Any,
    X_val: np.ndarray,  # noqa: N803
    y_val: np.ndarray,
    config: dict[str, Any],
) -> dict[str, Any]:
    """
    Validar modelo antes del despliegue.

    Args:
        model: Modelo a validar
        X_val: Datos de validación
        y_val: Labels de validación
        config: Configuración con umbrales y requisitos

    Returns:
        Reporte de validación con pass/fail y detalles

    Examples:
        >>> config = {"min_accuracy": 0.8, "required_methods": ["predict"]}
        >>> result = validate_model_for_deployment(model, X, y, config)
        >>> result['passed']
        True
    """
    report = {
        "passed": True,
        "checks": [],
        "metrics": {},
        "errors": [],
    }

    # 1. Verificar métodos requeridos
    for method in config.get("required_methods", []):
        has_method = hasattr(model, method) and callable(getattr(model, method))
        check = {
            "name": f"method_{method}",
            "passed": has_method,
            "message": f"Método {method}: {'OK' if has_method else 'Ausente'}",
        }
        report["checks"].append(check)
        if not has_method:
            report["passed"] = False
            report["errors"].append(f"Método requerido ausente: {method}")

    # 2. Medir latencia
    max_latency = config.get("max_latency_ms", 100)
    latencies = []

    try:
        for _ in range(10):
            start = time.time()
            _ = model.predict(X_val[:1])
            latencies.append((time.time() - start) * 1000)

        avg_latency = float(np.mean(latencies))
        p95_latency = float(np.percentile(latencies, 95))

        report["metrics"]["latency_avg_ms"] = avg_latency
        report["metrics"]["latency_p95_ms"] = p95_latency

        check = {
            "name": "latency",
            "passed": p95_latency <= max_latency,
            "message": f"Latencia P95: {p95_latency:.2f}ms (máx: {max_latency}ms)",
        }
        report["checks"].append(check)

        if p95_latency > max_latency:
            report["passed"] = False
            report["errors"].append(f"Latencia excede límite: {p95_latency:.2f}ms")

    except Exception as e:
        report["passed"] = False
        report["errors"].append(f"Error en medición de latencia: {e}")

    # 3. Calcular métricas
    try:
        predictions = model.predict(X_val)
        accuracy = float(accuracy_score(y_val, predictions))
        report["metrics"]["accuracy"] = accuracy

        min_accuracy = config.get("min_accuracy", 0.8)
        check = {
            "name": "accuracy",
            "passed": accuracy >= min_accuracy,
            "message": f"Accuracy: {accuracy:.4f} (mín: {min_accuracy})",
        }
        report["checks"].append(check)

        if accuracy < min_accuracy:
            report["passed"] = False
            report["errors"].append(f"Accuracy bajo: {accuracy:.4f}")

    except Exception as e:
        report["passed"] = False
        report["errors"].append(f"Error calculando métricas: {e}")

    return report


# ============================================================================
# Alert System
# ============================================================================


class AlertSystem:
    """
    Sistema de alertas para monitoreo de modelos.

    Attributes:
        thresholds: Umbrales por métrica
        cooldown_hours: Horas de cooldown entre alertas

    Examples:
        >>> thresholds = {"latency_p99_ms": {"warning": 100, "critical": 200}}
        >>> alert_system = AlertSystem(thresholds)
        >>> result = alert_system.analyze_metrics({"latency_p99_ms": [50, 150]})
    """

    def __init__(
        self,
        thresholds: dict[str, dict[str, float]],
        cooldown_hours: int = 1,
    ):
        """
        Inicializar sistema de alertas.

        Args:
            thresholds: Umbrales por métrica {metric: {warning: x, critical: y}}
            cooldown_hours: Horas de cooldown entre alertas del mismo tipo
        """
        self.thresholds = thresholds
        self.cooldown_hours = cooldown_hours
        self.alert_history: list[dict[str, Any]] = []
        self.last_alert_time: dict[str, int] = defaultdict(lambda: -999)

    def _check_cooldown(self, alert_key: str, current_hour: int) -> bool:
        """Verificar si pasó el cooldown."""
        last_hour = self.last_alert_time.get(alert_key, -self.cooldown_hours - 1)
        return current_hour - last_hour >= self.cooldown_hours

    def _determine_severity(self, metric: str, value: float) -> tuple[str, bool]:
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
        hourly_metrics: dict[str, list[float]],
        start_hour: int = 0,
    ) -> dict[str, Any]:
        """
        Analizar métricas y generar alertas.

        Args:
            hourly_metrics: Métricas por hora
            start_hour: Hora de inicio para tracking

        Returns:
            Reporte con alertas generadas
        """
        alerts = []
        summary = {
            "total_hours": 0,
            "alerts_generated": 0,
            "alerts_suppressed": 0,
            "by_severity": {"warning": 0, "critical": 0},
        }

        # Obtener número de horas
        num_hours = len(list(hourly_metrics.values())[0])

        for hour_idx in range(num_hours):
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
                            "threshold": self.thresholds[metric][severity],
                        }
                        alerts.append(alert)
                        self.alert_history.append(alert)
                        self.last_alert_time[alert_key] = current_hour
                        summary["alerts_generated"] += 1
                        summary["by_severity"][severity] += 1
                    else:
                        summary["alerts_suppressed"] += 1

        return {"alerts": alerts, "summary": summary}

    def get_summary(self) -> dict[str, Any]:
        """
        Obtener resumen de las últimas alertas.

        Returns:
            Resumen con total de alertas y desglose
        """
        if not self.alert_history:
            return {"message": "No hay alertas en el historial", "total_alerts": 0}

        by_metric = defaultdict(list)
        for alert in self.alert_history:
            by_metric[alert["metric"]].append(alert)

        return {
            "total_alerts": len(self.alert_history),
            "by_metric": {
                metric: {
                    "count": len(alerts_list),
                    "severities": [a["severity"] for a in alerts_list],
                }
                for metric, alerts_list in by_metric.items()
            },
            "most_recent": self.alert_history[-5:],
        }
