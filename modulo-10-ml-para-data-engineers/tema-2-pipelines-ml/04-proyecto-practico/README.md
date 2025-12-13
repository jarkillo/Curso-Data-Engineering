# Proyecto Práctico: ML Pipeline Builder

Framework para crear pipelines de Machine Learning production-ready con sklearn.

## Objetivos

- Crear pipelines reproducibles y serializables
- Manejar datos mixtos (numéricos + categóricos)
- Implementar cross-validation y optimización de hiperparámetros
- Diseñar código listo para producción

## Conceptos Clave

### Pipeline

Un Pipeline encadena transformaciones y modelo en un único objeto que:
- Se entrena con un solo `fit()`
- Predice con un solo `predict()`
- Se serializa completo para producción

### ColumnTransformer

Aplica diferentes transformaciones a diferentes columnas:
- Numéricas: Imputar + Escalar
- Categóricas: Imputar + OneHot Encoding

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   └── ml_pipeline.py      # Funciones principales
├── tests/
│   ├── __init__.py
│   └── test_ml_pipeline.py # Tests
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
pytest -v --cov=src --cov-report=term-missing
```

## Funciones Implementadas

### `create_preprocessor`

```python
def create_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str]
) -> ColumnTransformer:
    """Crea preprocesador para datos mixtos."""
```

### `create_classification_pipeline`

```python
def create_classification_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
    model: Any = None
) -> Pipeline:
    """Crea pipeline de clasificación completo."""
```

### `create_regression_pipeline`

```python
def create_regression_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
    model: Any = None
) -> Pipeline:
    """Crea pipeline de regresión completo."""
```

### `train_with_cv`

```python
def train_with_cv(
    pipeline: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5
) -> dict:
    """Evalúa con cross-validation."""
```

### `optimize_hyperparameters`

```python
def optimize_hyperparameters(
    pipeline: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    param_grid: dict
) -> dict:
    """Busca mejores hiperparámetros."""
```

### `evaluate_model`

```python
def evaluate_model(
    pipeline: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    task: str
) -> dict:
    """Evalúa modelo con múltiples métricas."""
```

### `save_pipeline` / `load_pipeline`

```python
def save_pipeline(pipeline: Pipeline, filepath: str) -> None:
    """Guarda pipeline a disco."""

def load_pipeline(filepath: str) -> Pipeline:
    """Carga pipeline desde disco."""
```

### `predict_single`

```python
def predict_single(pipeline: Pipeline, data: dict) -> dict:
    """Predice para un solo registro."""
```

## Ejemplo de Uso

```python
from src.ml_pipeline import (
    create_classification_pipeline,
    train_with_cv,
    optimize_hyperparameters,
    evaluate_model,
    save_pipeline,
    predict_single
)
import pandas as pd

# 1. Crear datos
data = pd.DataFrame({
    'edad': [25, 30, 35, 40],
    'ingresos': [30000, 45000, 55000, 70000],
    'tipo': ['A', 'B', 'A', 'B'],
    'target': [0, 0, 1, 1]
})

X = data.drop('target', axis=1)
y = data['target']

# 2. Crear pipeline
pipeline = create_classification_pipeline(
    numeric_features=['edad', 'ingresos'],
    categorical_features=['tipo']
)

# 3. Cross-validation
cv_scores = train_with_cv(pipeline, X, y, cv=3)
print(f"CV Score: {cv_scores['mean']:.3f}")

# 4. Optimizar hiperparámetros
param_grid = {
    'classifier__n_estimators': [50, 100],
    'classifier__max_depth': [3, 5]
}
result = optimize_hyperparameters(pipeline, X, y, param_grid)
best_pipeline = result['best_estimator']

# 5. Evaluar
metrics = evaluate_model(best_pipeline, X, y, task='classification')
print(f"Accuracy: {metrics['accuracy']:.3f}")

# 6. Guardar para producción
save_pipeline(best_pipeline, 'model.pkl')

# 7. Predecir nuevo registro
nuevo_cliente = {'edad': 28, 'ingresos': 40000, 'tipo': 'A'}
resultado = predict_single(best_pipeline, nuevo_cliente)
print(f"Predicción: {resultado['prediction']}")
```

## Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md)
- [02-EJEMPLOS.md](../02-EJEMPLOS.md)
- [03-EJERCICIOS.md](../03-EJERCICIOS.md)
