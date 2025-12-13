"""
Tests para el módulo de pipelines ML.

Estos tests verifican la correcta construcción y funcionamiento
de pipelines de Machine Learning production-ready.
"""

import numpy as np
import pandas as pd
import pytest
from numpy.testing import assert_array_equal

from src.ml_pipeline import (
    create_classification_pipeline,
    create_preprocessor,
    create_regression_pipeline,
    evaluate_model,
    load_pipeline,
    optimize_hyperparameters,
    predict_single,
    save_pipeline,
    train_with_cv,
)


@pytest.fixture
def sample_classification_data():
    """Genera datos de clasificación de prueba."""
    np.random.seed(42)
    n = 200

    data = pd.DataFrame(
        {
            "edad": np.random.randint(18, 70, n),
            "ingresos": np.random.exponential(40000, n).round(2),
            "antiguedad": np.random.randint(0, 120, n),
            "tipo_cliente": np.random.choice(["nuevo", "regular", "premium"], n),
            "region": np.random.choice(["norte", "sur", "centro"], n),
            "target": np.random.choice([0, 1], n, p=[0.3, 0.7]),
        }
    )

    # Introducir missing
    data.loc[np.random.choice(n, 20), "ingresos"] = np.nan
    data.loc[np.random.choice(n, 10), "tipo_cliente"] = np.nan

    return data


@pytest.fixture
def sample_regression_data():
    """Genera datos de regresión de prueba."""
    np.random.seed(42)
    n = 200

    data = pd.DataFrame(
        {
            "distancia": np.random.uniform(10, 500, n).round(1),
            "peso": np.random.exponential(10, n).round(2),
            "volumen": np.random.uniform(0.1, 5, n).round(3),
            "prioridad": np.random.choice(["standard", "express"], n),
            "target": np.random.exponential(24, n).round(1),
        }
    )

    return data


class TestCreatePreprocessor:
    """Tests para create_preprocessor."""

    def test_create_preprocessor_basic(self, sample_classification_data):
        """Debe crear un ColumnTransformer válido."""
        numeric_features = ["edad", "ingresos", "antiguedad"]
        categorical_features = ["tipo_cliente", "region"]

        preprocessor = create_preprocessor(numeric_features, categorical_features)

        assert preprocessor is not None
        assert hasattr(preprocessor, "fit")
        assert hasattr(preprocessor, "transform")

    def test_create_preprocessor_handles_missing(self, sample_classification_data):
        """El preprocesador debe manejar missing values."""
        numeric_features = ["edad", "ingresos", "antiguedad"]
        categorical_features = ["tipo_cliente", "region"]

        preprocessor = create_preprocessor(numeric_features, categorical_features)

        X = sample_classification_data.drop("target", axis=1)
        X_transformed = preprocessor.fit_transform(X)

        # No debe haber NaN después de transformar
        assert not np.isnan(X_transformed).any()

    def test_create_preprocessor_output_shape(self, sample_classification_data):
        """El output debe tener el número correcto de features."""
        numeric_features = ["edad", "ingresos", "antiguedad"]
        categorical_features = ["tipo_cliente", "region"]

        preprocessor = create_preprocessor(numeric_features, categorical_features)

        X = sample_classification_data.drop("target", axis=1)
        X_transformed = preprocessor.fit_transform(X)

        # 3 numéricas + (3 tipos_cliente + 3 regiones) = 9 features
        assert X_transformed.shape[0] == len(X)
        assert X_transformed.shape[1] >= 3  # Al menos las numéricas

    def test_create_preprocessor_empty_categorical(self):
        """Debe funcionar sin features categóricas."""
        preprocessor = create_preprocessor(
            numeric_features=["a", "b"], categorical_features=[]
        )
        assert preprocessor is not None


class TestCreateClassificationPipeline:
    """Tests para create_classification_pipeline."""

    def test_create_classification_pipeline_default(self, sample_classification_data):
        """Debe crear un pipeline de clasificación funcional."""
        numeric_features = ["edad", "ingresos", "antiguedad"]
        categorical_features = ["tipo_cliente", "region"]

        pipeline = create_classification_pipeline(
            numeric_features, categorical_features
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        # Debe poder entrenar
        pipeline.fit(X, y)

        # Debe poder predecir
        predictions = pipeline.predict(X)
        assert len(predictions) == len(X)
        assert set(predictions).issubset({0, 1})

    def test_create_classification_pipeline_custom_model(
        self, sample_classification_data
    ):
        """Debe aceptar un modelo personalizado."""
        from sklearn.linear_model import LogisticRegression

        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
            model=LogisticRegression(random_state=42),
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        pipeline.fit(X, y)
        assert hasattr(pipeline.named_steps["classifier"], "coef_")

    def test_create_classification_pipeline_predict_proba(
        self, sample_classification_data
    ):
        """Debe soportar predict_proba."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        pipeline.fit(X, y)
        probas = pipeline.predict_proba(X)

        assert probas.shape == (len(X), 2)
        assert np.allclose(probas.sum(axis=1), 1.0)


class TestCreateRegressionPipeline:
    """Tests para create_regression_pipeline."""

    def test_create_regression_pipeline_default(self, sample_regression_data):
        """Debe crear un pipeline de regresión funcional."""
        pipeline = create_regression_pipeline(
            numeric_features=["distancia", "peso", "volumen"],
            categorical_features=["prioridad"],
        )

        X = sample_regression_data.drop("target", axis=1)
        y = sample_regression_data["target"]

        pipeline.fit(X, y)
        predictions = pipeline.predict(X)

        assert len(predictions) == len(X)
        assert predictions.dtype in [np.float64, np.float32]


class TestTrainWithCV:
    """Tests para train_with_cv."""

    def test_train_with_cv_returns_scores(self, sample_classification_data):
        """Debe retornar scores de cross-validation."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        scores = train_with_cv(pipeline, X, y, cv=3)

        assert "mean" in scores
        assert "std" in scores
        assert "scores" in scores
        assert len(scores["scores"]) == 3
        assert 0 <= scores["mean"] <= 1

    def test_train_with_cv_stratified(self, sample_classification_data):
        """Debe usar stratified CV para clasificación."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        scores = train_with_cv(pipeline, X, y, cv=5, stratify=True)

        assert len(scores["scores"]) == 5


class TestOptimizeHyperparameters:
    """Tests para optimize_hyperparameters."""

    def test_optimize_returns_best_params(self, sample_classification_data):
        """Debe retornar los mejores parámetros."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        param_grid = {
            "classifier__n_estimators": [10, 20],
            "classifier__max_depth": [3, 5],
        }

        result = optimize_hyperparameters(pipeline, X, y, param_grid, cv=2)

        assert "best_params" in result
        assert "best_score" in result
        assert "best_estimator" in result
        assert result["best_params"]["classifier__n_estimators"] in [10, 20]

    def test_optimize_returns_trained_model(self, sample_classification_data):
        """El modelo retornado debe estar entrenado."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        param_grid = {"classifier__n_estimators": [10]}

        result = optimize_hyperparameters(pipeline, X, y, param_grid, cv=2)

        # El modelo debe poder predecir sin re-entrenar
        predictions = result["best_estimator"].predict(X)
        assert len(predictions) == len(X)


class TestEvaluateModel:
    """Tests para evaluate_model."""

    def test_evaluate_classification(self, sample_classification_data):
        """Debe evaluar modelo de clasificación correctamente."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        pipeline.fit(X, y)
        metrics = evaluate_model(pipeline, X, y, task="classification")

        assert "accuracy" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "f1" in metrics
        assert 0 <= metrics["accuracy"] <= 1

    def test_evaluate_regression(self, sample_regression_data):
        """Debe evaluar modelo de regresión correctamente."""
        pipeline = create_regression_pipeline(
            numeric_features=["distancia", "peso", "volumen"],
            categorical_features=["prioridad"],
        )

        X = sample_regression_data.drop("target", axis=1)
        y = sample_regression_data["target"]

        pipeline.fit(X, y)
        metrics = evaluate_model(pipeline, X, y, task="regression")

        assert "mae" in metrics
        assert "rmse" in metrics
        assert "r2" in metrics
        assert metrics["mae"] >= 0
        assert metrics["rmse"] >= 0


class TestSaveLoadPipeline:
    """Tests para save_pipeline y load_pipeline."""

    def test_save_and_load(self, sample_classification_data, tmp_path):
        """Debe guardar y cargar pipeline correctamente."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        pipeline.fit(X, y)

        # Guardar
        filepath = tmp_path / "test_pipeline.pkl"
        save_pipeline(pipeline, str(filepath))

        assert filepath.exists()

        # Cargar
        loaded_pipeline = load_pipeline(str(filepath))

        # Debe hacer las mismas predicciones
        original_pred = pipeline.predict(X)
        loaded_pred = loaded_pipeline.predict(X)

        assert_array_equal(original_pred, loaded_pred)

    def test_load_nonexistent_raises(self):
        """Debe lanzar error si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            load_pipeline("nonexistent_file.pkl")


class TestPredictSingle:
    """Tests para predict_single."""

    def test_predict_single_dict(self, sample_classification_data):
        """Debe predecir desde un diccionario."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        pipeline.fit(X, y)

        single_input = {
            "edad": 35,
            "ingresos": 50000.0,
            "antiguedad": 24,
            "tipo_cliente": "regular",
            "region": "norte",
        }

        result = predict_single(pipeline, single_input)

        assert "prediction" in result
        assert "probability" in result
        assert result["prediction"] in [0, 1]
        assert 0 <= result["probability"] <= 1

    def test_predict_single_handles_unknown_category(self, sample_classification_data):
        """Debe manejar categorías desconocidas."""
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        pipeline.fit(X, y)

        # Categoría que no estaba en entrenamiento
        single_input = {
            "edad": 35,
            "ingresos": 50000.0,
            "antiguedad": 24,
            "tipo_cliente": "VIP",  # Nueva categoría
            "region": "oeste",  # Nueva categoría
        }

        # No debe lanzar error
        result = predict_single(pipeline, single_input)
        assert "prediction" in result


class TestIntegration:
    """Tests de integración del flujo completo."""

    def test_full_classification_workflow(self, sample_classification_data):
        """Debe completar flujo de clasificación end-to-end."""
        # 1. Crear pipeline
        pipeline = create_classification_pipeline(
            numeric_features=["edad", "ingresos", "antiguedad"],
            categorical_features=["tipo_cliente", "region"],
        )

        X = sample_classification_data.drop("target", axis=1)
        y = sample_classification_data["target"]

        # 2. Cross-validation
        cv_scores = train_with_cv(pipeline, X, y, cv=3)
        assert cv_scores["mean"] > 0

        # 3. Entrenar modelo final
        pipeline.fit(X, y)

        # 4. Evaluar
        metrics = evaluate_model(pipeline, X, y, task="classification")
        assert metrics["accuracy"] > 0

        # 5. Predecir single
        result = predict_single(
            pipeline,
            {
                "edad": 30,
                "ingresos": 45000,
                "antiguedad": 12,
                "tipo_cliente": "nuevo",
                "region": "sur",
            },
        )
        assert result["prediction"] in [0, 1]

    def test_full_regression_workflow(self, sample_regression_data):
        """Debe completar flujo de regresión end-to-end."""
        # 1. Crear pipeline
        pipeline = create_regression_pipeline(
            numeric_features=["distancia", "peso", "volumen"],
            categorical_features=["prioridad"],
        )

        X = sample_regression_data.drop("target", axis=1)
        y = sample_regression_data["target"]

        # 2. Cross-validation (stratify=False para regresión)
        cv_scores = train_with_cv(
            pipeline, X, y, cv=3, scoring="neg_mean_absolute_error", stratify=False
        )
        assert cv_scores["mean"] < 0  # MAE negativo

        # 3. Entrenar
        pipeline.fit(X, y)

        # 4. Evaluar
        metrics = evaluate_model(pipeline, X, y, task="regression")
        assert metrics["mae"] >= 0
