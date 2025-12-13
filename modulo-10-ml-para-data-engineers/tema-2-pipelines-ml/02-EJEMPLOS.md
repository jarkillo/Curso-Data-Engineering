# Ejemplos Prácticos: Pipelines de Machine Learning

En esta sección trabajaremos ejemplos paso a paso de pipelines ML production-ready. Todos los ejemplos son ejecutables y usan empresas ficticias para contexto profesional.

---

## Ejemplo 1: Pipeline Básico de Clasificación - Nivel: Básico

### Contexto

**FinTech Analytics** necesita predecir si un cliente aprobará su solicitud de crédito. Tienen datos históricos de clientes con variables numéricas y categóricas.

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

# Datos de clientes de FinTech Analytics
np.random.seed(42)
n = 1000

clientes = pd.DataFrame({
    'edad': np.random.randint(18, 70, n),
    'ingresos': np.random.exponential(40000, n).round(2),
    'deuda_actual': np.random.exponential(5000, n).round(2),
    'meses_empleo': np.random.randint(0, 240, n),
    'aprobado': np.random.choice([0, 1], n, p=[0.3, 0.7])
})

# Introducir algunos valores faltantes
clientes.loc[np.random.choice(n, 50), 'ingresos'] = np.nan
clientes.loc[np.random.choice(n, 30), 'meses_empleo'] = np.nan

print("=== Datos de Clientes ===")
print(clientes.head(10))
print(f"\nMissing values:\n{clientes.isnull().sum()}")
```

### Paso 1: Dividir datos ANTES de cualquier transformación

```python
# Separar features y target
X = clientes.drop('aprobado', axis=1)
y = clientes['aprobado']

# Split estratificado (mantiene proporción de clases)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # Importante para clasificación
)

print(f"=== División de Datos ===")
print(f"Training: {len(X_train)} muestras")
print(f"Test: {len(X_test)} muestras")
print(f"\nProporción clase 1 en train: {y_train.mean():.2%}")
print(f"Proporción clase 1 en test: {y_test.mean():.2%}")
```

### Paso 2: Crear Pipeline simple

```python
# Pipeline con todos los pasos
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),  # Paso 1: Imputar NaN
    ('scaler', StandardScaler()),                    # Paso 2: Escalar
    ('classifier', LogisticRegression(random_state=42))  # Paso 3: Modelo
])

print("\n=== Pipeline Creado ===")
print(pipeline)
```

### Paso 3: Entrenar y evaluar

```python
# Entrenar pipeline (fit aplica todos los pasos en orden)
pipeline.fit(X_train, y_train)

# Evaluar en test set
train_score = pipeline.score(X_train, y_train)
test_score = pipeline.score(X_test, y_test)

print(f"\n=== Resultados ===")
print(f"Accuracy en training: {train_score:.3f}")
print(f"Accuracy en test: {test_score:.3f}")

# Hacer predicciones
predicciones = pipeline.predict(X_test)
probabilidades = pipeline.predict_proba(X_test)

print(f"\nPrimeras 5 predicciones: {predicciones[:5]}")
print(f"Probabilidades clase 1: {probabilidades[:5, 1].round(3)}")
```

### Paso 4: Inspeccionar el pipeline entrenado

```python
# Acceder a componentes individuales
imputer_fitted = pipeline.named_steps['imputer']
scaler_fitted = pipeline.named_steps['scaler']
model_fitted = pipeline.named_steps['classifier']

print("\n=== Parámetros Aprendidos ===")
print(f"Valores imputados (mediana): {imputer_fitted.statistics_}")
print(f"Medias del scaler: {scaler_fitted.mean_.round(2)}")
print(f"Coeficientes del modelo: {model_fitted.coef_.round(3)}")
```

### Resultado

```
=== Resultados ===
Accuracy en training: 0.723
Accuracy en test: 0.705
```

### Interpretación

- El pipeline encadena imputación → escalado → modelo en un solo objeto
- `fit()` entrena todos los pasos secuencialmente
- `predict()` aplica todas las transformaciones y luego predice
- Los parámetros de cada paso se aprenden SOLO del training set

---

## Ejemplo 2: ColumnTransformer para Datos Mixtos - Nivel: Intermedio

### Contexto

**RestaurantData Co.** quiere predecir si un restaurante tendrá alta demanda basándose en características mixtas (numéricas y categóricas).

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Datos de restaurantes
np.random.seed(42)
n = 500

restaurantes = pd.DataFrame({
    'capacidad': np.random.randint(20, 200, n),
    'precio_promedio': np.random.uniform(10, 80, n).round(2),
    'calificacion': np.random.uniform(3.0, 5.0, n).round(1),
    'tipo_cocina': np.random.choice(['italiana', 'mexicana', 'japonesa', 'americana', 'mediterranea'], n),
    'ubicacion': np.random.choice(['centro', 'residencial', 'comercial', 'turistica'], n),
    'tiene_terraza': np.random.choice(['si', 'no'], n),
    'alta_demanda': np.random.choice([0, 1], n, p=[0.4, 0.6])
})

# Introducir missing values
restaurantes.loc[np.random.choice(n, 40), 'precio_promedio'] = np.nan
restaurantes.loc[np.random.choice(n, 25), 'tipo_cocina'] = np.nan

print("=== Datos de Restaurantes ===")
print(restaurantes.head())
print(f"\nTipos de datos:\n{restaurantes.dtypes}")
print(f"\nMissing values:\n{restaurantes.isnull().sum()}")
```

### Paso 1: Definir columnas por tipo

```python
# Identificar columnas por tipo
numeric_features = ['capacidad', 'precio_promedio', 'calificacion']
categorical_features = ['tipo_cocina', 'ubicacion', 'tiene_terraza']

print("=== Tipos de Features ===")
print(f"Numéricas: {numeric_features}")
print(f"Categóricas: {categorical_features}")
```

### Paso 2: Crear transformadores específicos

```python
# Pipeline para variables numéricas
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline para variables categóricas
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='desconocido')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

print("=== Transformadores Definidos ===")
print("Numérico: Imputar (mediana) → Escalar (StandardScaler)")
print("Categórico: Imputar ('desconocido') → OneHot Encoding")
```

### Paso 3: Combinar con ColumnTransformer

```python
# Combinar transformadores
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='drop'  # Ignorar columnas no especificadas
)

# Pipeline completo con preprocesador + modelo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

print("\n=== Pipeline Completo ===")
print(pipeline)
```

### Paso 4: Entrenar y evaluar

```python
# Separar features y target
X = restaurantes.drop('alta_demanda', axis=1)
y = restaurantes['alta_demanda']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Entrenar
pipeline.fit(X_train, y_train)

# Evaluar
print("\n=== Resultados ===")
print(f"Accuracy en training: {pipeline.score(X_train, y_train):.3f}")
print(f"Accuracy en test: {pipeline.score(X_test, y_test):.3f}")
```

### Paso 5: Inspeccionar features transformadas

```python
# Ver nombres de features después del preprocesamiento
feature_names = (
    numeric_features +
    list(pipeline.named_steps['preprocessor']
         .named_transformers_['cat']
         .named_steps['encoder']
         .get_feature_names_out(categorical_features))
)

print(f"\n=== Features Transformadas ({len(feature_names)}) ===")
for i, name in enumerate(feature_names):
    print(f"  {i}: {name}")

# Ver importancia de features
importances = pipeline.named_steps['classifier'].feature_importances_
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)

print("\n=== Top 5 Features por Importancia ===")
print(importance_df.head())
```

### Interpretación

- `ColumnTransformer` permite aplicar diferentes transformaciones a diferentes columnas
- Las numéricas se imputan con mediana y escalan
- Las categóricas se imputan con valor constante y codifican con one-hot
- El pipeline completo maneja todo automáticamente

---

## Ejemplo 3: Cross-Validation y Selección de Modelo - Nivel: Intermedio

### Contexto

**CloudAPI Systems** necesita predecir qué APIs tendrán alta latencia. Quieren comparar varios modelos usando cross-validation.

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

# Datos de APIs
np.random.seed(42)
n = 800

apis = pd.DataFrame({
    'requests_por_segundo': np.random.exponential(500, n).round(0),
    'tamaño_payload_kb': np.random.exponential(50, n).round(2),
    'num_dependencias': np.random.randint(1, 20, n),
    'complejidad_query': np.random.uniform(1, 10, n).round(2),
    'cache_hit_rate': np.random.uniform(0, 1, n).round(3),
    'alta_latencia': np.random.choice([0, 1], n, p=[0.7, 0.3])
})

X = apis.drop('alta_latencia', axis=1)
y = apis['alta_latencia']

print("=== Datos de APIs ===")
print(X.head())
print(f"\nDistribución del target: {y.value_counts().to_dict()}")
```

### Paso 1: Definir pipeline base

```python
# Preprocesamiento común para todos los modelos
preprocessor = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

print("=== Preprocesador Base ===")
print(preprocessor)
```

### Paso 2: Definir modelos a comparar

```python
# Diccionario de modelos a evaluar
models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(random_state=42)
}

print("=== Modelos a Comparar ===")
for name in models:
    print(f"  - {name}")
```

### Paso 3: Evaluar cada modelo con cross-validation

```python
# Configurar cross-validation estratificado
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {}

print("\n=== Evaluación con 5-Fold CV ===")
print("-" * 60)

for name, model in models.items():
    # Crear pipeline para este modelo
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    # Cross-validation
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring='accuracy')

    results[name] = {
        'mean': scores.mean(),
        'std': scores.std(),
        'scores': scores
    }

    print(f"{name:25s} | Accuracy: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")

print("-" * 60)
```

### Paso 4: Visualizar resultados

```python
# Crear DataFrame de resultados
results_df = pd.DataFrame({
    'Modelo': list(results.keys()),
    'Accuracy Media': [r['mean'] for r in results.values()],
    'Desv. Estándar': [r['std'] for r in results.values()]
}).sort_values('Accuracy Media', ascending=False)

print("\n=== Ranking de Modelos ===")
print(results_df.to_string(index=False))

# Mejor modelo
best_model = results_df.iloc[0]['Modelo']
print(f"\n✓ Mejor modelo: {best_model}")
print(f"  Accuracy: {results[best_model]['mean']:.3f}")
print(f"  Variabilidad baja indica modelo estable")
```

### Paso 5: Entrenar modelo final

```python
from sklearn.model_selection import train_test_split

# Split final para evaluación
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Pipeline con mejor modelo
final_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', models[best_model])
])

# Entrenar
final_pipeline.fit(X_train, y_train)

# Evaluación final
print("\n=== Evaluación Final ===")
print(f"Training accuracy: {final_pipeline.score(X_train, y_train):.3f}")
print(f"Test accuracy: {final_pipeline.score(X_test, y_test):.3f}")
```

### Interpretación

- Cross-validation da una estimación más robusta que un solo split
- La desviación estándar indica qué tan estable es el modelo
- Se usa StratifiedKFold para mantener proporción de clases en cada fold

---

## Ejemplo 4: GridSearchCV para Optimización - Nivel: Avanzado

### Contexto

**LogisticFlow** quiere optimizar un modelo de predicción de tiempos de entrega. Necesitan encontrar los mejores hiperparámetros.

### Datos

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

# Datos de envíos
np.random.seed(42)
n = 1000

envios = pd.DataFrame({
    'distancia_km': np.random.uniform(10, 500, n).round(1),
    'peso_kg': np.random.exponential(10, n).round(2),
    'volumen_m3': np.random.uniform(0.1, 5, n).round(3),
    'prioridad': np.random.choice(['standard', 'express', 'urgente'], n),
    'tipo_vehiculo': np.random.choice(['moto', 'furgoneta', 'camion'], n),
    'zona_destino': np.random.choice(['urbana', 'suburbana', 'rural'], n),
    'hora_envio': np.random.randint(0, 24, n),
    'tiempo_entrega_horas': np.random.exponential(24, n).round(1)  # Target
})

print("=== Datos de Envíos ===")
print(envios.head())
print(f"\nTarget (tiempo_entrega_horas) - Media: {envios['tiempo_entrega_horas'].mean():.1f}h")
```

### Paso 1: Preparar pipeline base

```python
numeric_features = ['distancia_km', 'peso_kg', 'volumen_m3', 'hora_envio']
categorical_features = ['prioridad', 'tipo_vehiculo', 'zona_destino']

preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), numeric_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='desconocido')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ]), categorical_features)
])

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42))
])

print("=== Pipeline Base ===")
print(pipeline)
```

### Paso 2: Definir grid de hiperparámetros

```python
# Parámetros a buscar
# Nota: usar 'nombre_paso__parametro' para parámetros del pipeline
param_grid = {
    'regressor__n_estimators': [50, 100, 200],
    'regressor__max_depth': [5, 10, 20, None],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4]
}

total_combinations = 3 * 4 * 3 * 3
print(f"\n=== Grid de Hiperparámetros ===")
print(f"Parámetros a optimizar:")
for param, values in param_grid.items():
    print(f"  {param}: {values}")
print(f"\nTotal de combinaciones: {total_combinations}")
print(f"Con 5-fold CV: {total_combinations * 5} modelos a entrenar")
```

### Paso 3: Ejecutar GridSearchCV

```python
# Separar datos
X = envios.drop('tiempo_entrega_horas', axis=1)
y = envios['tiempo_entrega_horas']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Configurar GridSearchCV
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='neg_mean_absolute_error',  # MAE negativo (sklearn maximiza)
    n_jobs=-1,  # Usar todos los cores
    verbose=1
)

print("\n=== Ejecutando GridSearchCV ===")
grid_search.fit(X_train, y_train)

print(f"\n✓ Búsqueda completada!")
```

### Paso 4: Analizar resultados

```python
print("\n=== Mejores Hiperparámetros ===")
for param, value in grid_search.best_params_.items():
    print(f"  {param}: {value}")

print(f"\nMejor MAE (CV): {-grid_search.best_score_:.2f} horas")

# Top 5 combinaciones
results_df = pd.DataFrame(grid_search.cv_results_)
top_5 = results_df.nsmallest(5, 'rank_test_score')[
    ['params', 'mean_test_score', 'std_test_score', 'rank_test_score']
]

print("\n=== Top 5 Combinaciones ===")
for i, row in top_5.iterrows():
    print(f"Rank {row['rank_test_score']}: MAE={-row['mean_test_score']:.2f} (+/- {row['std_test_score']*2:.2f})")
```

### Paso 5: Evaluar modelo final

```python
# El mejor modelo ya está entrenado
best_pipeline = grid_search.best_estimator_

# Evaluar en test set
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

y_pred = best_pipeline.predict(X_test)

print("\n=== Evaluación Final en Test Set ===")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f} horas")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f} horas")
print(f"R²: {r2_score(y_test, y_pred):.3f}")
```

### Interpretación

- GridSearchCV prueba todas las combinaciones de hiperparámetros
- Usa cross-validation para cada combinación (evita overfitting al validation set)
- El mejor modelo se guarda automáticamente en `best_estimator_`

---

## Ejemplo 5: Pipeline Completo para Producción - Nivel: Avanzado

### Contexto

**FinTech Analytics** necesita un pipeline de scoring crediticio listo para producción, incluyendo: preprocesamiento, modelo, guardado y predicción en nuevos datos.

### Paso 1: Crear y entrenar pipeline

```python
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Datos de entrenamiento
np.random.seed(42)
n = 2000

datos_train = pd.DataFrame({
    'edad': np.random.randint(18, 70, n),
    'ingresos_mensuales': np.random.exponential(3000, n).round(2),
    'deuda_total': np.random.exponential(5000, n).round(2),
    'meses_empleo_actual': np.random.randint(0, 240, n),
    'num_creditos_activos': np.random.randint(0, 10, n),
    'tipo_empleo': np.random.choice(['fijo', 'temporal', 'autonomo', 'desempleado'], n),
    'nivel_educacion': np.random.choice(['secundaria', 'universidad', 'master', 'doctorado'], n),
    'estado_civil': np.random.choice(['soltero', 'casado', 'divorciado'], n),
    'aprobado': np.random.choice([0, 1], n, p=[0.35, 0.65])
})

# Introducir missing values realistas
datos_train.loc[np.random.choice(n, 100), 'ingresos_mensuales'] = np.nan
datos_train.loc[np.random.choice(n, 50), 'meses_empleo_actual'] = np.nan
datos_train.loc[np.random.choice(n, 30), 'tipo_empleo'] = np.nan

print("=== Datos de Entrenamiento ===")
print(datos_train.info())
```

### Paso 2: Definir pipeline completo

```python
# Definir columnas
numeric_features = ['edad', 'ingresos_mensuales', 'deuda_total',
                   'meses_empleo_actual', 'num_creditos_activos']
categorical_features = ['tipo_empleo', 'nivel_educacion', 'estado_civil']

# Preprocesador
preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), numeric_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='desconocido')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ]), categorical_features)
])

# Pipeline completo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    ))
])

print("\n=== Pipeline de Producción ===")
print(pipeline)
```

### Paso 3: Entrenar y validar

```python
# Separar features y target
X = datos_train.drop('aprobado', axis=1)
y = datos_train['aprobado']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Cross-validation antes de entrenar
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='roc_auc')
print(f"\n=== Cross-Validation (5-fold) ===")
print(f"ROC-AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")

# Entrenar modelo final
pipeline.fit(X_train, y_train)

# Evaluar en test
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

print(f"\n=== Evaluación en Test Set ===")
print(classification_report(y_test, y_pred, target_names=['Rechazado', 'Aprobado']))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")
```

### Paso 4: Guardar pipeline para producción

```python
# Guardar pipeline completo
model_path = 'credit_scoring_pipeline_v1.pkl'
joblib.dump(pipeline, model_path)

print(f"\n=== Pipeline Guardado ===")
print(f"Archivo: {model_path}")
print(f"Tamaño: {os.path.getsize(model_path) / 1024:.1f} KB")

# Metadata del modelo
metadata = {
    'version': '1.0.0',
    'fecha_entrenamiento': pd.Timestamp.now().isoformat(),
    'metricas': {
        'roc_auc_cv': cv_scores.mean(),
        'roc_auc_test': roc_auc_score(y_test, y_proba)
    },
    'features': {
        'numericas': numeric_features,
        'categoricas': categorical_features
    }
}

joblib.dump(metadata, 'credit_scoring_metadata_v1.pkl')
print(f"Metadata guardada")
```

### Paso 5: Función de predicción para producción

```python
def predecir_credito(datos_cliente: dict) -> dict:
    """
    Predice si un cliente será aprobado para crédito.

    Args:
        datos_cliente: Diccionario con datos del cliente

    Returns:
        Diccionario con predicción y probabilidad
    """
    # Cargar pipeline
    pipeline = joblib.load('credit_scoring_pipeline_v1.pkl')

    # Convertir a DataFrame
    df = pd.DataFrame([datos_cliente])

    # Predecir
    prediccion = pipeline.predict(df)[0]
    probabilidad = pipeline.predict_proba(df)[0, 1]

    return {
        'aprobado': bool(prediccion),
        'probabilidad_aprobacion': round(probabilidad, 3),
        'decision': 'APROBADO' if prediccion == 1 else 'RECHAZADO'
    }


# Probar con nuevo cliente
nuevo_cliente = {
    'edad': 35,
    'ingresos_mensuales': 4500.00,
    'deuda_total': 2000.00,
    'meses_empleo_actual': 36,
    'num_creditos_activos': 2,
    'tipo_empleo': 'fijo',
    'nivel_educacion': 'universidad',
    'estado_civil': 'casado'
}

resultado = predecir_credito(nuevo_cliente)

print("\n=== Predicción para Nuevo Cliente ===")
print(f"Datos: {nuevo_cliente}")
print(f"\nResultado: {resultado}")
```

### Interpretación

El pipeline de producción:
1. Está completamente autocontenido (preprocesamiento + modelo)
2. Maneja missing values automáticamente
3. Maneja categorías nuevas con `handle_unknown='ignore'`
4. Se puede serializar y cargar fácilmente
5. Produce predicciones consistentes

---

## Código Resumen

```python
"""
Pipeline ML - Patrón Recomendado para Producción
"""
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import joblib

# 1. Definir columnas
numeric_features = ['col1', 'col2']
categorical_features = ['col3', 'col4']

# 2. Crear preprocesador
preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_features),
    ('cat', categorical_pipeline, categorical_features)
])

# 3. Crear pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', modelo)
])

# 4. Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)

# 5. Validar con CV
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)

# 6. (Opcional) Optimizar hiperparámetros
grid_search = GridSearchCV(pipeline, param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_pipeline = grid_search.best_estimator_

# 7. Entrenar modelo final
pipeline.fit(X_train, y_train)

# 8. Evaluar en test
score = pipeline.score(X_test, y_test)

# 9. Guardar para producción
joblib.dump(pipeline, 'model.pkl')

# 10. Usar en producción
pipeline = joblib.load('model.pkl')
predictions = pipeline.predict(new_data)
```

---

## Próximo Paso

Ahora que has visto los ejemplos, es hora de practicar por tu cuenta.

[Continuar a 03-EJERCICIOS.md →](03-EJERCICIOS.md)
