# Ejercicios Prácticos: Pipelines de Machine Learning

Estos ejercicios están diseñados para que practiques la creación de pipelines ML production-ready. Cada ejercicio incluye contexto empresarial, datos, y una solución completa al final.

---

## Ejercicios Básicos

### Ejercicio 1: Pipeline Simple de Clasificación

**Dificultad**: ⭐ Fácil

**Contexto**:
**FinTech Analytics** necesita un pipeline básico para predecir aprobación de préstamos.

**Datos**:
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

np.random.seed(42)
n = 500

prestamos = pd.DataFrame({
    'ingresos': np.random.exponential(40000, n).round(2),
    'deuda': np.random.exponential(5000, n).round(2),
    'edad': np.random.randint(18, 65, n),
    'aprobado': np.random.choice([0, 1], n, p=[0.3, 0.7])
})

# Introducir missing
prestamos.loc[np.random.choice(n, 30), 'ingresos'] = np.nan
```

**Pregunta**:
Crea un Pipeline con:
1. SimpleImputer (estrategia: mediana)
2. StandardScaler
3. LogisticRegression

Entrena y evalúa en train/test split (80/20).

**Pista**:
Usa `Pipeline` de sklearn y recuerda hacer el split ANTES de crear el pipeline.

---

### Ejercicio 2: Cross-Validation Básico

**Dificultad**: ⭐ Fácil

**Contexto**:
**CloudAPI Systems** quiere evaluar de forma robusta un modelo de predicción de errores.

**Datos**:
```python
np.random.seed(42)
n = 400

apis = pd.DataFrame({
    'latencia_ms': np.random.exponential(100, n).round(2),
    'requests_hora': np.random.randint(100, 10000, n),
    'tamaño_response': np.random.exponential(500, n).round(0),
    'tiene_error': np.random.choice([0, 1], n, p=[0.85, 0.15])
})
```

**Pregunta**:
1. Crea un pipeline con StandardScaler + RandomForestClassifier
2. Evalúa con cross_val_score usando 5 folds
3. Reporta media y desviación estándar del accuracy

**Pista**:
Usa `StratifiedKFold` para mantener proporción de clases (15% errores).

---

### Ejercicio 3: Train/Test/Validation Split

**Dificultad**: ⭐ Fácil

**Contexto**:
Necesitas dividir datos correctamente para un proyecto de ML.

**Datos**:
```python
np.random.seed(42)
X = np.random.randn(1000, 5)
y = np.random.choice([0, 1], 1000, p=[0.6, 0.4])
```

**Pregunta**:
Divide los datos en:
- 60% training
- 20% validation
- 20% test

Verifica que la proporción de clases se mantiene en los tres conjuntos.

**Pista**:
Necesitas dos llamadas a `train_test_split` con `stratify=y`.

---

## Ejercicios Intermedios

### Ejercicio 4: ColumnTransformer para Datos Mixtos

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**RestaurantData Co.** tiene datos con columnas numéricas y categóricas que necesitan diferentes preprocesos.

**Datos**:
```python
np.random.seed(42)
n = 600

restaurantes = pd.DataFrame({
    'capacidad': np.random.randint(20, 200, n),
    'precio_medio': np.random.uniform(10, 80, n).round(2),
    'antiguedad_años': np.random.randint(1, 30, n),
    'tipo_cocina': np.random.choice(['italiana', 'mexicana', 'japonesa', 'americana'], n),
    'zona': np.random.choice(['centro', 'periferia', 'turistica'], n),
    'exito': np.random.choice([0, 1], n, p=[0.4, 0.6])
})

# Missing values
restaurantes.loc[np.random.choice(n, 40), 'precio_medio'] = np.nan
restaurantes.loc[np.random.choice(n, 25), 'tipo_cocina'] = np.nan
```

**Pregunta**:
Crea un ColumnTransformer que:
1. Para numéricas (`capacidad`, `precio_medio`, `antiguedad_años`):
   - Imputar con mediana
   - Escalar con StandardScaler
2. Para categóricas (`tipo_cocina`, `zona`):
   - Imputar con valor constante 'desconocido'
   - OneHotEncoder con `handle_unknown='ignore'`

Entrena un RandomForestClassifier y evalúa con CV.

**Pista**:
Define dos Pipeline separados y combínalos con ColumnTransformer.

---

### Ejercicio 5: GridSearchCV

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
**LogisticFlow** necesita optimizar los hiperparámetros de un modelo de predicción de tiempos de entrega.

**Datos**:
```python
np.random.seed(42)
n = 800

envios = pd.DataFrame({
    'distancia_km': np.random.uniform(5, 300, n).round(1),
    'peso_kg': np.random.exponential(5, n).round(2),
    'es_urgente': np.random.choice([0, 1], n, p=[0.7, 0.3]),
    'tiempo_entrega_min': np.random.exponential(60, n).round(0)  # Target
})
```

**Pregunta**:
1. Crea un pipeline con StandardScaler + GradientBoostingRegressor
2. Define un param_grid para buscar:
   - `n_estimators`: [50, 100, 150]
   - `max_depth`: [3, 5, 7]
   - `learning_rate`: [0.01, 0.1, 0.2]
3. Ejecuta GridSearchCV con 5-fold CV y scoring='neg_mean_absolute_error'
4. Reporta los mejores parámetros y el mejor MAE

**Pista**:
Los nombres de parámetros en el grid deben incluir el nombre del paso: `'regressor__n_estimators'`.

---

### Ejercicio 6: Comparación de Modelos

**Dificultad**: ⭐⭐ Intermedio

**Contexto**:
Necesitas comparar varios modelos para elegir el mejor para un problema de clasificación.

**Datos**:
```python
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=10,
    n_redundant=5,
    n_classes=2,
    random_state=42
)
```

**Pregunta**:
Compara los siguientes modelos usando 5-fold CV:
1. LogisticRegression
2. RandomForestClassifier (n_estimators=100)
3. GradientBoostingClassifier (n_estimators=100)
4. SVC (kernel='rbf')

Usa StandardScaler como preprocesamiento para todos. Reporta accuracy media y std para cada modelo. ¿Cuál elegirías y por qué?

**Pista**:
Crea un diccionario de modelos y itera sobre ellos.

---

## Ejercicios Avanzados

### Ejercicio 7: Pipeline con Feature Selection

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
**FinTech Analytics** tiene muchas features y quiere seleccionar solo las más importantes.

**Datos**:
```python
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=500,
    n_features=50,  # Muchas features
    n_informative=10,  # Solo 10 son informativas
    n_redundant=20,
    n_classes=2,
    random_state=42
)
X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(50)])
```

**Pregunta**:
Crea un pipeline que:
1. Escale las features (StandardScaler)
2. Seleccione las K mejores features (SelectKBest con f_classif)
3. Entrene un LogisticRegression

Usa GridSearchCV para encontrar el mejor valor de K entre [5, 10, 15, 20, 25].

Reporta:
- El mejor K
- Las features seleccionadas
- El accuracy final

**Pista**:
Usa `SelectKBest` de `sklearn.feature_selection`.

---

### Ejercicio 8: Pipeline para Series Temporales

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
**CloudAPI Systems** tiene datos de métricas de APIs ordenados temporalmente.

**Datos**:
```python
np.random.seed(42)
n = 500

# Datos ordenados temporalmente
fechas = pd.date_range('2024-01-01', periods=n, freq='H')

metricas = pd.DataFrame({
    'fecha': fechas,
    'latencia': np.random.exponential(100, n) + np.sin(np.arange(n) / 24) * 20,
    'requests': np.random.randint(100, 1000, n),
    'cpu_percent': np.random.uniform(10, 90, n),
    'tiene_alerta': np.random.choice([0, 1], n, p=[0.9, 0.1])
})

# Features y target
X = metricas[['latencia', 'requests', 'cpu_percent']]
y = metricas['tiene_alerta']
```

**Pregunta**:
1. Usa TimeSeriesSplit con 5 splits para cross-validation
2. Crea un pipeline con StandardScaler + RandomForestClassifier
3. Compara los resultados con StratifiedKFold normal
4. ¿Por qué es importante usar TimeSeriesSplit para datos temporales?

**Pista**:
TimeSeriesSplit garantiza que siempre entrenas con datos pasados y predices datos futuros.

---

### Ejercicio 9: Pipeline Completo para Producción

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
Debes crear un pipeline production-ready que se pueda guardar, cargar y usar para predicciones.

**Datos**:
```python
np.random.seed(42)
n = 1000

clientes = pd.DataFrame({
    'edad': np.random.randint(18, 70, n),
    'ingresos': np.random.exponential(3000, n).round(2),
    'antiguedad_meses': np.random.randint(0, 120, n),
    'tipo_cuenta': np.random.choice(['basica', 'premium', 'business'], n),
    'canal': np.random.choice(['web', 'app', 'presencial'], n),
    'churn': np.random.choice([0, 1], n, p=[0.85, 0.15])
})

# Missing values
clientes.loc[np.random.choice(n, 80), 'ingresos'] = np.nan
clientes.loc[np.random.choice(n, 40), 'tipo_cuenta'] = np.nan
```

**Pregunta**:
1. Crea un pipeline completo con ColumnTransformer
2. Optimiza hiperparámetros con GridSearchCV
3. Guarda el mejor pipeline con joblib
4. Crea una función `predecir_churn(datos_cliente: dict) -> dict` que:
   - Cargue el pipeline
   - Haga la predicción
   - Retorne `{'churn': bool, 'probabilidad': float}`
5. Prueba la función con un cliente nuevo

**Pista**:
Recuerda usar `handle_unknown='ignore'` en OneHotEncoder para manejar categorías nuevas en producción.

---

### Ejercicio 10: Detectar Data Leakage

**Dificultad**: ⭐⭐⭐ Difícil

**Contexto**:
Revisa el siguiente código y encuentra los problemas de data leakage.

**Código a revisar**:
```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Datos
np.random.seed(42)
X = pd.DataFrame({
    'feature1': np.random.randn(1000),
    'feature2': np.random.randn(1000),
    'feature3': np.random.randn(1000)
})
X.loc[np.random.choice(1000, 100), 'feature1'] = np.nan
y = np.random.choice([0, 1], 1000)

# Preprocesamiento
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Entrenar
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluar
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
```

**Pregunta**:
1. Identifica al menos 2 problemas de data leakage
2. Reescribe el código correctamente usando Pipeline
3. Explica por qué el código original daría métricas engañosamente buenas

**Pista**:
¿En qué momento se hace el fit del imputer y scaler? ¿Qué datos se usan?

---

## Soluciones

### Solución Ejercicio 1

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

np.random.seed(42)
n = 500

prestamos = pd.DataFrame({
    'ingresos': np.random.exponential(40000, n).round(2),
    'deuda': np.random.exponential(5000, n).round(2),
    'edad': np.random.randint(18, 65, n),
    'aprobado': np.random.choice([0, 1], n, p=[0.3, 0.7])
})
prestamos.loc[np.random.choice(n, 30), 'ingresos'] = np.nan

# Separar features y target
X = prestamos.drop('aprobado', axis=1)
y = prestamos['aprobado']

# Split ANTES de cualquier transformación
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Crear pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression(random_state=42))
])

# Entrenar
pipeline.fit(X_train, y_train)

# Evaluar
print(f"Accuracy en training: {pipeline.score(X_train, y_train):.3f}")
print(f"Accuracy en test: {pipeline.score(X_test, y_test):.3f}")
```

---

### Solución Ejercicio 2

```python
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

np.random.seed(42)
n = 400

apis = pd.DataFrame({
    'latencia_ms': np.random.exponential(100, n).round(2),
    'requests_hora': np.random.randint(100, 10000, n),
    'tamaño_response': np.random.exponential(500, n).round(0),
    'tiene_error': np.random.choice([0, 1], n, p=[0.85, 0.15])
})

X = apis.drop('tiene_error', axis=1)
y = apis['tiene_error']

# Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Cross-validation estratificada
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X, y, cv=cv, scoring='accuracy')

print(f"Scores por fold: {scores.round(3)}")
print(f"Accuracy media: {scores.mean():.3f}")
print(f"Desviación estándar: {scores.std():.3f}")
print(f"Intervalo: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")
```

---

### Solución Ejercicio 3

```python
import numpy as np
from sklearn.model_selection import train_test_split

np.random.seed(42)
X = np.random.randn(1000, 5)
y = np.random.choice([0, 1], 1000, p=[0.6, 0.4])

# Paso 1: Separar test (20%)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Paso 2: Separar validation (20% del total = 25% del restante)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42, stratify=y_temp
)

# Verificar tamaños
print("=== Tamaños ===")
print(f"Training: {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
print(f"Validation: {len(X_val)} ({len(X_val)/len(X)*100:.0f}%)")
print(f"Test: {len(X_test)} ({len(X_test)/len(X)*100:.0f}%)")

# Verificar proporción de clases
print("\n=== Proporción clase 1 ===")
print(f"Original: {y.mean():.2%}")
print(f"Training: {y_train.mean():.2%}")
print(f"Validation: {y_val.mean():.2%}")
print(f"Test: {y_test.mean():.2%}")
```

---

### Solución Ejercicio 4

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

np.random.seed(42)
n = 600

restaurantes = pd.DataFrame({
    'capacidad': np.random.randint(20, 200, n),
    'precio_medio': np.random.uniform(10, 80, n).round(2),
    'antiguedad_años': np.random.randint(1, 30, n),
    'tipo_cocina': np.random.choice(['italiana', 'mexicana', 'japonesa', 'americana'], n),
    'zona': np.random.choice(['centro', 'periferia', 'turistica'], n),
    'exito': np.random.choice([0, 1], n, p=[0.4, 0.6])
})
restaurantes.loc[np.random.choice(n, 40), 'precio_medio'] = np.nan
restaurantes.loc[np.random.choice(n, 25), 'tipo_cocina'] = np.nan

# Definir columnas
numeric_features = ['capacidad', 'precio_medio', 'antiguedad_años']
categorical_features = ['tipo_cocina', 'zona']

# Transformadores
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='desconocido')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# ColumnTransformer
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Pipeline completo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Separar datos
X = restaurantes.drop('exito', axis=1)
y = restaurantes['exito']

# Cross-validation
scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')
print(f"Accuracy CV: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")
```

---

### Solución Ejercicio 5

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor

np.random.seed(42)
n = 800

envios = pd.DataFrame({
    'distancia_km': np.random.uniform(5, 300, n).round(1),
    'peso_kg': np.random.exponential(5, n).round(2),
    'es_urgente': np.random.choice([0, 1], n, p=[0.7, 0.3]),
    'tiempo_entrega_min': np.random.exponential(60, n).round(0)
})

X = envios.drop('tiempo_entrega_min', axis=1)
y = envios['tiempo_entrega_min']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', GradientBoostingRegressor(random_state=42))
])

# Grid de parámetros
param_grid = {
    'regressor__n_estimators': [50, 100, 150],
    'regressor__max_depth': [3, 5, 7],
    'regressor__learning_rate': [0.01, 0.1, 0.2]
}

# GridSearchCV
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='neg_mean_absolute_error',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("=== Mejores Parámetros ===")
print(grid_search.best_params_)
print(f"\nMejor MAE (CV): {-grid_search.best_score_:.2f} minutos")

# Evaluación final
from sklearn.metrics import mean_absolute_error
y_pred = grid_search.predict(X_test)
print(f"MAE en Test: {mean_absolute_error(y_test, y_pred):.2f} minutos")
```

---

### Solución Ejercicio 6

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

X, y = make_classification(
    n_samples=1000, n_features=20, n_informative=10,
    n_redundant=5, n_classes=2, random_state=42
)

# Modelos a comparar
models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM (RBF)': SVC(kernel='rbf', random_state=42)
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = {}

print("=== Comparación de Modelos ===")
print("-" * 50)

for name, model in models.items():
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', model)
    ])

    scores = cross_val_score(pipeline, X, y, cv=cv, scoring='accuracy')
    results[name] = {'mean': scores.mean(), 'std': scores.std()}

    print(f"{name:25s} | {scores.mean():.3f} (+/- {scores.std()*2:.3f})")

print("-" * 50)

# Mejor modelo
best = max(results.items(), key=lambda x: x[1]['mean'])
print(f"\n✓ Mejor modelo: {best[0]}")
print(f"  Razón: Mayor accuracy media con variabilidad aceptable")
```

---

### Solución Ejercicio 10

```python
"""
PROBLEMAS DE DATA LEAKAGE EN EL CÓDIGO ORIGINAL:

1. El imputer se entrena con TODOS los datos (incluyendo test)
   - imputer.fit_transform(X) usa X completo
   - La media usada para imputar incluye valores del test set

2. El scaler se entrena con TODOS los datos (incluyendo test)
   - scaler.fit_transform(X_imputed) usa X completo
   - Media y std incluyen información del test set

3. El split se hace DESPUÉS del preprocesamiento
   - Los datos ya están "contaminados"

CONSECUENCIAS:
- El modelo "ve" información del test set durante entrenamiento
- Las métricas serán optimistas (mejor de lo real)
- En producción, el modelo rendirá peor

CÓDIGO CORRECTO:
"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Datos
np.random.seed(42)
X = pd.DataFrame({
    'feature1': np.random.randn(1000),
    'feature2': np.random.randn(1000),
    'feature3': np.random.randn(1000)
})
X.loc[np.random.choice(1000, 100), 'feature1'] = np.nan
y = np.random.choice([0, 1], 1000)

# ✅ CORRECTO: Split ANTES de cualquier preprocesamiento
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ✅ CORRECTO: Usar Pipeline
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# ✅ CORRECTO: fit solo con datos de entrenamiento
pipeline.fit(X_train, y_train)

# Evaluar
y_pred = pipeline.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")

# El Pipeline garantiza que:
# - El imputer calcula la media SOLO con X_train
# - El scaler calcula media/std SOLO con X_train
# - En X_test solo se aplica transform(), no fit()
```

---

## Próximo Paso

Has completado los ejercicios de Pipelines ML. Ahora aplica todo en un proyecto práctico completo.

[Continuar a 04-proyecto-practico →](04-proyecto-practico/)
