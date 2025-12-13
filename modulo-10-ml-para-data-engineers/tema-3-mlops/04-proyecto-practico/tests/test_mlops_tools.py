"""Tests para las herramientas MLOps."""

import json

import numpy as np
import pytest
from sklearn.ensemble import RandomForestClassifier

from src.mlops_tools import (
    # Alerting
    AlertSystem,
    # Model Registry
    ModelRegistry,
    # Logging
    PredictionLogger,
    analyze_feature_drift,
    # Drift Detection
    detect_drift_ks,
    detect_drift_psi,
    sanitize_pii,
    # Validation
    validate_model_for_deployment,
)

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def reference_data():
    """Datos de referencia para tests de drift."""
    np.random.seed(42)
    return {
        "age": np.random.normal(35, 10, 100),
        "income": np.random.normal(50000, 15000, 100),
    }


@pytest.fixture
def production_data_no_drift():
    """Datos de producción sin drift."""
    np.random.seed(43)
    return {
        "age": np.random.normal(35, 10, 100),
        "income": np.random.normal(50000, 15000, 100),
    }


@pytest.fixture
def production_data_with_drift():
    """Datos de producción con drift significativo."""
    np.random.seed(44)
    return {
        "age": np.random.normal(35, 10, 100),
        "income": np.random.normal(75000, 15000, 100),  # Drift en income
    }


@pytest.fixture
def temp_registry_path(tmp_path):
    """Directorio temporal para el registry."""
    return str(tmp_path / "test_registry")


@pytest.fixture
def trained_model():
    """Modelo entrenado para tests."""
    np.random.seed(42)
    X = np.random.randn(100, 4)
    y = np.random.randint(0, 2, 100)
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    return model


@pytest.fixture
def validation_data():
    """Datos de validación."""
    np.random.seed(42)
    X = np.random.randn(20, 4)
    y = np.random.randint(0, 2, 20)
    return X, y


# ============================================================================
# Tests: Drift Detection - KS Test
# ============================================================================


class TestDetectDriftKS:
    """Tests para detect_drift_ks."""

    def test_no_drift_high_pvalue(self, reference_data, production_data_no_drift):
        """Distribuciones similares deberían tener p-value alto."""
        result = detect_drift_ks(reference_data["age"], production_data_no_drift["age"])

        assert "p_value" in result
        assert "drift_detected" in result
        assert result["p_value"] > 0.05
        assert result["drift_detected"] == False  # noqa: E712

    def test_drift_low_pvalue(self, reference_data, production_data_with_drift):
        """Distribuciones diferentes deberían tener p-value bajo."""
        result = detect_drift_ks(
            reference_data["income"], production_data_with_drift["income"]
        )

        assert result["p_value"] < 0.05
        assert result["drift_detected"] == True  # noqa: E712

    def test_returns_statistic(self, reference_data):
        """Debe retornar el estadístico KS."""
        result = detect_drift_ks(reference_data["age"], reference_data["age"])

        assert "statistic" in result
        assert 0 <= result["statistic"] <= 1

    def test_custom_threshold(self, reference_data, production_data_no_drift):
        """Debe respetar threshold personalizado."""
        result = detect_drift_ks(
            reference_data["age"],
            production_data_no_drift["age"],
            threshold=0.99,
        )

        # Con threshold muy alto, casi siempre detectaría drift
        assert result["threshold"] == 0.99


# ============================================================================
# Tests: Drift Detection - PSI
# ============================================================================


class TestDetectDriftPSI:
    """Tests para detect_drift_psi."""

    def test_no_drift_low_psi(self, reference_data, production_data_no_drift):
        """Distribuciones similares deberían tener PSI bajo."""
        result = detect_drift_psi(
            reference_data["age"], production_data_no_drift["age"]
        )

        assert "psi_value" in result
        assert result["psi_value"] < 0.2
        assert result["drift_detected"] is False

    def test_drift_high_psi(self, reference_data, production_data_with_drift):
        """Distribuciones diferentes deberían tener PSI alto."""
        result = detect_drift_psi(
            reference_data["income"], production_data_with_drift["income"]
        )

        assert result["psi_value"] > 0.2
        assert result["drift_detected"] is True

    def test_interpretation_field(self, reference_data, production_data_no_drift):
        """Debe incluir interpretación del PSI."""
        result = detect_drift_psi(
            reference_data["age"], production_data_no_drift["age"]
        )

        assert "interpretation" in result
        assert result["interpretation"] in [
            "sin cambio",
            "cambio moderado",
            "cambio significativo",
        ]


# ============================================================================
# Tests: Feature Drift Analysis
# ============================================================================


class TestAnalyzeFeatureDrift:
    """Tests para analyze_feature_drift."""

    def test_analyzes_all_features(self, reference_data, production_data_no_drift):
        """Debe analizar todas las features."""
        report = analyze_feature_drift(
            reference_data, production_data_no_drift, ["age", "income"]
        )

        assert report["features_analyzed"] == 2
        assert "age" in report["details"]
        assert "income" in report["details"]

    def test_detects_drifted_features(self, reference_data, production_data_with_drift):
        """Debe identificar features con drift."""
        report = analyze_feature_drift(
            reference_data, production_data_with_drift, ["age", "income"]
        )

        assert report["features_with_drift"] > 0
        assert report["drift_alert"] is True

    def test_report_structure(self, reference_data, production_data_no_drift):
        """Debe retornar estructura correcta."""
        report = analyze_feature_drift(
            reference_data, production_data_no_drift, ["age"]
        )

        assert "timestamp" in report
        assert "features_analyzed" in report
        assert "features_with_drift" in report
        assert "details" in report
        assert "drift_alert" in report


# ============================================================================
# Tests: Model Registry
# ============================================================================


class TestModelRegistry:
    """Tests para ModelRegistry."""

    def test_register_model(self, temp_registry_path, trained_model, tmp_path):
        """Debe registrar modelo correctamente."""
        # Guardar modelo temporal
        model_path = tmp_path / "model.pkl"
        import joblib

        joblib.dump(trained_model, model_path)

        registry = ModelRegistry(temp_registry_path)
        result = registry.register_model(
            model_name="test_model",
            version="1.0.0",
            model_path=str(model_path),
            metrics={"accuracy": 0.85},
        )

        assert result["status"] == "registered"
        assert result["model_name"] == "test_model"
        assert result["version"] == "1.0.0"

    def test_promote_to_staging(self, temp_registry_path, trained_model, tmp_path):
        """Debe promover a staging."""
        model_path = tmp_path / "model.pkl"
        import joblib

        joblib.dump(trained_model, model_path)

        registry = ModelRegistry(temp_registry_path)
        registry.register_model(
            "test_model", "1.0.0", str(model_path), {"accuracy": 0.85}
        )

        result = registry.promote_to_staging("test_model", "1.0.0")
        assert result["status"] == "promoted_to_staging"

    def test_promote_to_production(self, temp_registry_path, trained_model, tmp_path):
        """Debe promover a producción."""
        model_path = tmp_path / "model.pkl"
        import joblib

        joblib.dump(trained_model, model_path)

        registry = ModelRegistry(temp_registry_path)
        registry.register_model(
            "test_model", "1.0.0", str(model_path), {"accuracy": 0.85}
        )

        result = registry.promote_to_production("test_model", "1.0.0")
        assert result["status"] == "promoted_to_production"

    def test_get_production_path(self, temp_registry_path, trained_model, tmp_path):
        """Debe retornar ruta del modelo en producción."""
        model_path = tmp_path / "model.pkl"
        import joblib

        joblib.dump(trained_model, model_path)

        registry = ModelRegistry(temp_registry_path)
        registry.register_model(
            "test_model", "1.0.0", str(model_path), {"accuracy": 0.85}
        )
        registry.promote_to_production("test_model", "1.0.0")

        prod_path = registry.get_production_model_path("test_model")
        assert prod_path.exists()

    def test_rollback(self, temp_registry_path, trained_model, tmp_path):
        """Debe hacer rollback a versión anterior."""
        import joblib

        # Registrar dos versiones
        for version in ["1.0.0", "1.1.0"]:
            model_path = tmp_path / f"model_{version}.pkl"
            joblib.dump(trained_model, model_path)
            registry = ModelRegistry(temp_registry_path)
            registry.register_model(
                "test_model", version, str(model_path), {"accuracy": 0.85}
            )

        registry.promote_to_production("test_model", "1.0.0")
        registry.promote_to_production("test_model", "1.1.0")

        result = registry.rollback("test_model")
        assert result["status"] == "rolled_back"
        assert result["to_version"] == "1.0.0"


# ============================================================================
# Tests: Prediction Logger
# ============================================================================


class TestPredictionLogger:
    """Tests para PredictionLogger."""

    def test_log_prediction_structure(self):
        """Log debe tener estructura correcta."""
        logger = PredictionLogger("test_service")

        log_entry = logger.create_log_entry(
            request_id="req-123",
            input_data={"age": 35, "income": 50000},
            prediction={"class": 1, "probability": 0.87},
            latency_ms=45.2,
        )

        assert "timestamp" in log_entry
        assert "request_id" in log_entry
        assert "input" in log_entry
        assert "output" in log_entry
        assert "latency_ms" in log_entry
        assert log_entry["request_id"] == "req-123"

    def test_log_is_json_serializable(self):
        """Log debe ser serializable a JSON."""
        logger = PredictionLogger("test_service")

        log_entry = logger.create_log_entry(
            request_id="req-123",
            input_data={"age": 35},
            prediction={"class": 1},
            latency_ms=45.2,
        )

        # No debería lanzar excepción
        json_str = json.dumps(log_entry)
        assert isinstance(json_str, str)


class TestSanitizePII:
    """Tests para sanitize_pii."""

    def test_removes_email(self):
        """Debe remover campo email."""
        data = {"age": 35, "email": "test@example.com", "income": 50000}
        sanitized = sanitize_pii(data)

        assert "email" not in sanitized
        assert "age" in sanitized
        assert "income" in sanitized

    def test_removes_multiple_pii_fields(self):
        """Debe remover múltiples campos PII."""
        data = {
            "age": 35,
            "email": "test@example.com",
            "phone": "123-456-7890",
            "ssn": "123-45-6789",
            "income": 50000,
        }
        sanitized = sanitize_pii(data)

        assert "email" not in sanitized
        assert "phone" not in sanitized
        assert "ssn" not in sanitized
        assert "age" in sanitized
        assert "income" in sanitized

    def test_custom_pii_fields(self):
        """Debe permitir campos PII personalizados."""
        data = {"secret_field": "secret", "public_field": "public"}
        sanitized = sanitize_pii(data, pii_fields=["secret_field"])

        assert "secret_field" not in sanitized
        assert "public_field" in sanitized


# ============================================================================
# Tests: Model Validation
# ============================================================================


class TestValidateModelForDeployment:
    """Tests para validate_model_for_deployment."""

    def test_passes_valid_model(self, trained_model, validation_data):
        """Modelo válido debe pasar validación."""
        X_val, y_val = validation_data
        config = {
            "min_accuracy": 0.3,  # Umbral bajo para datos aleatorios
            "max_latency_ms": 1000,
            "required_methods": ["predict"],
        }

        result = validate_model_for_deployment(trained_model, X_val, y_val, config)
        assert result["passed"] == True  # noqa: E712

    def test_fails_missing_method(self, validation_data):
        """Debe fallar si falta método requerido."""
        X_val, y_val = validation_data

        # Modelo sin método predict_proba
        class FakeModel:
            def predict(self, x):  # noqa: N803
                return np.zeros(len(x))

        config = {
            "min_accuracy": 0.5,
            "max_latency_ms": 1000,
            "required_methods": ["predict", "predict_proba"],
        }

        result = validate_model_for_deployment(FakeModel(), X_val, y_val, config)
        assert result["passed"] is False
        assert any("predict_proba" in str(e) for e in result["errors"])

    def test_fails_low_accuracy(self, validation_data):
        """Debe fallar si accuracy es muy baja."""
        X_val, y_val = validation_data

        # Modelo que siempre predice mal
        class BadModel:
            def predict(self, x):  # noqa: N803
                return np.ones(len(x))  # Siempre predice 1

        config = {
            "min_accuracy": 0.99,  # Umbral muy alto
            "max_latency_ms": 1000,
            "required_methods": ["predict"],
        }

        result = validate_model_for_deployment(BadModel(), X_val, y_val, config)
        assert result["passed"] is False

    def test_returns_metrics(self, trained_model, validation_data):
        """Debe retornar métricas calculadas."""
        X_val, y_val = validation_data
        config = {
            "min_accuracy": 0.5,
            "max_latency_ms": 1000,
            "required_methods": ["predict"],
        }

        result = validate_model_for_deployment(trained_model, X_val, y_val, config)
        assert "metrics" in result
        assert "accuracy" in result["metrics"]
        assert "latency_avg_ms" in result["metrics"]


# ============================================================================
# Tests: Alert System
# ============================================================================


class TestAlertSystem:
    """Tests para AlertSystem."""

    def test_generates_warning(self):
        """Debe generar alerta warning."""
        thresholds = {
            "latency_p99_ms": {"warning": 100, "critical": 200},
        }
        alert_system = AlertSystem(thresholds)

        metrics = {"latency_p99_ms": [50, 60, 120]}  # 120 > 100 warning

        result = alert_system.analyze_metrics(metrics)
        assert result["summary"]["alerts_generated"] > 0

    def test_generates_critical(self):
        """Debe generar alerta critical."""
        thresholds = {
            "latency_p99_ms": {"warning": 100, "critical": 200},
        }
        alert_system = AlertSystem(thresholds)

        metrics = {"latency_p99_ms": [50, 60, 250]}  # 250 > 200 critical

        result = alert_system.analyze_metrics(metrics)
        assert any(a["severity"] == "critical" for a in result["alerts"])

    def test_respects_cooldown(self):
        """Debe respetar cooldown entre alertas."""
        thresholds = {
            "latency_p99_ms": {"warning": 100, "critical": 200},
        }
        alert_system = AlertSystem(thresholds, cooldown_hours=2)

        # Métricas con valores altos consecutivos
        metrics = {"latency_p99_ms": [120, 130, 140, 150]}  # Todos > warning

        result = alert_system.analyze_metrics(metrics)

        # Solo debería generar una alerta debido al cooldown
        assert result["summary"]["alerts_generated"] <= 2
        assert result["summary"]["alerts_suppressed"] > 0

    def test_no_alerts_under_threshold(self):
        """No debe generar alertas si todo está normal."""
        thresholds = {
            "latency_p99_ms": {"warning": 100, "critical": 200},
        }
        alert_system = AlertSystem(thresholds)

        metrics = {"latency_p99_ms": [50, 60, 70, 80]}  # Todos bajo umbral

        result = alert_system.analyze_metrics(metrics)
        assert result["summary"]["alerts_generated"] == 0

    def test_summary_structure(self):
        """get_summary debe retornar estructura correcta."""
        thresholds = {"latency_p99_ms": {"warning": 100}}
        alert_system = AlertSystem(thresholds)

        metrics = {"latency_p99_ms": [50, 120]}
        alert_system.analyze_metrics(metrics)

        summary = alert_system.get_summary()
        assert "total_alerts" in summary
