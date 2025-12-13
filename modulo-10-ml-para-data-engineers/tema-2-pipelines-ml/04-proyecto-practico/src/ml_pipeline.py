"""
Módulo de pipelines ML production-ready.

Este módulo proporciona funciones para crear, entrenar, evaluar
y desplegar pipelines de Machine Learning. Sigue las mejores
prácticas de sklearn y está diseñado para uso en producción.

Funciones disponibles:
- create_preprocessor: Crea ColumnTransformer para preprocesamiento
- create_classification_pipeline: Pipeline de clasificación
- create_regression_pipeline: Pipeline de regresión
- train_with_cv: Entrena con cross-validation
- optimize_hyperparameters: Búsqueda de hiperparámetros
- evaluate_model: Evalúa métricas del modelo
- save_pipeline: Guarda pipeline a disco
- load_pipeline: Carga pipeline desde disco
- predict_single: Predicción para un solo registro
"""

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def create_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
    numeric_strategy: str = "median",
    categorical_fill: str = "missing",
) -> ColumnTransformer:
    """
    Crea un preprocesador ColumnTransformer para datos mixtos.

    Aplica transformaciones diferenciadas a columnas numéricas y categóricas:
    - Numéricas: Imputación + StandardScaler
    - Categóricas: Imputación + OneHotEncoder

    Args:
        numeric_features: Lista de nombres de columnas numéricas
        categorical_features: Lista de nombres de columnas categóricas
        numeric_strategy: Estrategia de imputación para numéricas
        categorical_fill: Valor de relleno para categóricas

    Returns:
        ColumnTransformer configurado

    Examples:
        >>> preprocessor = create_preprocessor(
        ...     numeric_features=['edad', 'ingresos'],
        ...     categorical_features=['ciudad', 'tipo']
        ... )
    """
    transformers = []

    # Pipeline para numéricas
    if numeric_features:
        numeric_transformer = Pipeline(
            [
                ("imputer", SimpleImputer(strategy=numeric_strategy)),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("num", numeric_transformer, numeric_features))

    # Pipeline para categóricas
    if categorical_features:
        categorical_transformer = Pipeline(
            [
                (
                    "imputer",
                    SimpleImputer(strategy="constant", fill_value=categorical_fill),
                ),
                (
                    "encoder",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                ),
            ]
        )
        transformers.append(("cat", categorical_transformer, categorical_features))

    return ColumnTransformer(transformers=transformers, remainder="drop")


def create_classification_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
    model: Any | None = None,
) -> Pipeline:
    """
    Crea un pipeline de clasificación completo.

    Combina preprocesamiento y modelo en un único objeto serializable.

    Args:
        numeric_features: Lista de columnas numéricas
        categorical_features: Lista de columnas categóricas
        model: Modelo de clasificación (default: RandomForestClassifier)

    Returns:
        Pipeline de sklearn listo para entrenar

    Examples:
        >>> pipeline = create_classification_pipeline(
        ...     numeric_features=['edad', 'ingresos'],
        ...     categorical_features=['tipo_cliente']
        ... )
        >>> pipeline.fit(X_train, y_train)
    """
    if model is None:
        model = RandomForestClassifier(n_estimators=100, random_state=42)

    preprocessor = create_preprocessor(numeric_features, categorical_features)

    return Pipeline([("preprocessor", preprocessor), ("classifier", model)])


def create_regression_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
    model: Any | None = None,
) -> Pipeline:
    """
    Crea un pipeline de regresión completo.

    Args:
        numeric_features: Lista de columnas numéricas
        categorical_features: Lista de columnas categóricas
        model: Modelo de regresión (default: GradientBoostingRegressor)

    Returns:
        Pipeline de sklearn listo para entrenar

    Examples:
        >>> pipeline = create_regression_pipeline(
        ...     numeric_features=['distancia', 'peso'],
        ...     categorical_features=['prioridad']
        ... )
    """
    if model is None:
        model = GradientBoostingRegressor(n_estimators=100, random_state=42)

    preprocessor = create_preprocessor(numeric_features, categorical_features)

    return Pipeline([("preprocessor", preprocessor), ("regressor", model)])


def train_with_cv(
    pipeline: Pipeline,
    X: pd.DataFrame,  # noqa: N803
    y: pd.Series | np.ndarray,
    cv: int = 5,
    scoring: str = "accuracy",
    stratify: bool = True,
) -> dict:
    """
    Entrena y evalúa un pipeline usando cross-validation.

    Args:
        pipeline: Pipeline de sklearn
        X: Features
        y: Target
        cv: Número de folds
        scoring: Métrica de evaluación
        stratify: Usar stratified CV (para clasificación)

    Returns:
        Diccionario con 'mean', 'std' y 'scores' de cada fold

    Examples:
        >>> scores = train_with_cv(pipeline, X, y, cv=5)
        >>> print(f"Accuracy: {scores['mean']:.3f} (+/- {scores['std']*2:.3f})")
    """
    if stratify:
        cv_splitter = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    else:
        cv_splitter = cv

    scores = cross_val_score(pipeline, X, y, cv=cv_splitter, scoring=scoring)

    return {"mean": float(scores.mean()), "std": float(scores.std()), "scores": scores}


def optimize_hyperparameters(
    pipeline: Pipeline,
    X: pd.DataFrame,  # noqa: N803
    y: pd.Series | np.ndarray,
    param_grid: dict,
    cv: int = 5,
    scoring: str = "accuracy",
    n_jobs: int = -1,
) -> dict:
    """
    Optimiza hiperparámetros usando GridSearchCV.

    Args:
        pipeline: Pipeline de sklearn
        X: Features
        y: Target
        param_grid: Diccionario con parámetros a buscar
        cv: Número de folds
        scoring: Métrica de evaluación
        n_jobs: Número de jobs paralelos (-1 = todos los cores)

    Returns:
        Diccionario con 'best_params', 'best_score' y 'best_estimator'

    Examples:
        >>> param_grid = {
        ...     'classifier__n_estimators': [50, 100],
        ...     'classifier__max_depth': [3, 5, 10]
        ... }
        >>> result = optimize_hyperparameters(pipeline, X, y, param_grid)
        >>> print(f"Mejores parámetros: {result['best_params']}")
    """
    grid_search = GridSearchCV(
        pipeline, param_grid, cv=cv, scoring=scoring, n_jobs=n_jobs
    )

    grid_search.fit(X, y)

    return {
        "best_params": grid_search.best_params_,
        "best_score": float(grid_search.best_score_),
        "best_estimator": grid_search.best_estimator_,
    }


def evaluate_model(
    pipeline: Pipeline,
    X: pd.DataFrame,  # noqa: N803
    y: pd.Series | np.ndarray,
    task: str = "classification",
) -> dict:
    """
    Evalúa un modelo entrenado con múltiples métricas.

    Args:
        pipeline: Pipeline entrenado
        X: Features
        y: Target real
        task: Tipo de tarea ('classification' o 'regression')

    Returns:
        Diccionario con métricas de evaluación

    Raises:
        ValueError: Si task no es válido

    Examples:
        >>> metrics = evaluate_model(pipeline, X_test, y_test, task='classification')
        >>> print(f"Accuracy: {metrics['accuracy']:.3f}")
    """
    y_pred = pipeline.predict(X)

    if task == "classification":
        return {
            "accuracy": float(accuracy_score(y, y_pred)),
            "precision": float(precision_score(y, y_pred, average="weighted")),
            "recall": float(recall_score(y, y_pred, average="weighted")),
            "f1": float(f1_score(y, y_pred, average="weighted")),
        }
    elif task == "regression":
        return {
            "mae": float(mean_absolute_error(y, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y, y_pred))),
            "r2": float(r2_score(y, y_pred)),
        }
    else:
        raise ValueError(f"Task debe ser 'classification' o 'regression', no '{task}'")


def save_pipeline(pipeline: Pipeline, filepath: str) -> None:
    """
    Guarda un pipeline a disco.

    Args:
        pipeline: Pipeline a guardar
        filepath: Ruta del archivo (debe terminar en .pkl)

    Examples:
        >>> save_pipeline(pipeline, 'model_v1.pkl')
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, filepath)


def load_pipeline(filepath: str) -> Pipeline:
    """
    Carga un pipeline desde disco.

    Args:
        filepath: Ruta del archivo .pkl

    Returns:
        Pipeline cargado

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> pipeline = load_pipeline('model_v1.pkl')
        >>> predictions = pipeline.predict(new_data)
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")

    return joblib.load(filepath)


def predict_single(
    pipeline: Pipeline, data: dict, include_probability: bool = True
) -> dict:
    """
    Realiza predicción para un solo registro.

    Args:
        pipeline: Pipeline entrenado
        data: Diccionario con los datos del registro
        include_probability: Incluir probabilidad (solo clasificación)

    Returns:
        Diccionario con 'prediction' y opcionalmente 'probability'

    Examples:
        >>> result = predict_single(pipeline, {
        ...     'edad': 35,
        ...     'ingresos': 50000,
        ...     'tipo_cliente': 'premium'
        ... })
        >>> print(f"Predicción: {result['prediction']}")
    """
    # Convertir dict a DataFrame
    df = pd.DataFrame([data])

    # Predecir
    prediction = pipeline.predict(df)[0]

    result = {
        "prediction": (
            int(prediction) if isinstance(prediction, np.integer) else prediction
        )
    }

    # Agregar probabilidad si es clasificación y está disponible
    if include_probability and hasattr(pipeline, "predict_proba"):
        try:
            proba = pipeline.predict_proba(df)[0]
            # Probabilidad de la clase positiva (índice 1)
            prob_value = proba[1] if len(proba) > 1 else proba[0]
            result["probability"] = float(prob_value)
        except (AttributeError, IndexError):
            result["probability"] = None

    return result
