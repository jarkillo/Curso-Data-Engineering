# Pipelines de Machine Learning: De Experimento a Producción

## Introducción

### ¿Por qué necesitamos Pipelines de ML?

Imagina que eres un chef en un restaurante de alta cocina. Cada plato requiere múltiples pasos: preparar ingredientes, cocinar en cierto orden, emplatar con precisión. Si cada vez que preparas el mismo plato lo haces de forma diferente, los resultados serán inconsistentes. Los clientes esperan que el risotto del martes sepa igual que el del sábado.

**Un Pipeline de ML es exactamente eso: una receta estandarizada y reproducible para transformar datos crudos en predicciones.**

En el mundo real del Data Engineering, esto es crítico porque:

1. **Reproducibilidad**: El mismo código debe producir los mismos resultados
2. **Consistencia train-production**: Las transformaciones en entrenamiento deben ser idénticas en producción
3. **Mantenibilidad**: Es más fácil debuggear y mejorar un pipeline modular
4. **Automatización**: Los pipelines permiten reentrenamiento automático
5. **Colaboración**: Otros pueden entender y modificar tu trabajo

### El Problema Sin Pipelines

```python
# ❌ CÓDIGO SPAGHETTI (sin pipeline)
# Cada paso está suelto, fácil de equivocarse

# Paso 1: Imputar
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)  # ¿Usé el mismo imputer? ¿O creé uno nuevo?

# Paso 2: Escalar
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)  # ¿Seguro que es transform y no fit_transform?

# Paso 3: Encoding
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
# Ups, olvidé que algunas columnas son categóricas...
# ¿En qué orden aplico las transformaciones?

# Paso 4: Entrenar
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train_scaled, y_train)

# EN PRODUCCIÓN:
# ¿Cómo aplico exactamente los mismos pasos?
# ¿Guardé todos los transformers?
# ¿Los aplico en el mismo orden?
```

### La Solución: Pipelines

```python
# ✅ CON PIPELINE
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier())
])

# Entrenamiento: un solo comando
pipeline.fit(X_train, y_train)

# Predicción: aplica TODOS los pasos automáticamente
predictions = pipeline.predict(X_test)

# Producción: mismo pipeline, mismos pasos, mismo orden
# joblib.dump(pipeline, 'model.pkl')
```

---

## Conceptos Fundamentales

### Concepto 1: ¿Qué es un Pipeline?

Un **Pipeline** es una secuencia ordenada de transformaciones que se aplican a los datos, terminando opcionalmente en un estimador (modelo).

**Analogía**: Es como una línea de ensamblaje en una fábrica. Cada estación hace una tarea específica, y el producto pasa de una estación a la siguiente en orden. Si cambias el orden de las estaciones, el producto final será diferente (o defectuoso).

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Pipeline de ML                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Datos     Paso 1        Paso 2        Paso 3        Paso N        │
│  Crudos → [Imputar] → [Escalar] → [Encoding] → ... → [Modelo]      │
│                                                                     │
│  Cada paso:                                                         │
│  - Recibe datos del paso anterior                                   │
│  - Aplica su transformación                                         │
│  - Pasa el resultado al siguiente                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**En scikit-learn**, un Pipeline tiene estas características:

1. **Secuencial**: Los pasos se ejecutan en orden
2. **Nombrado**: Cada paso tiene un nombre único
3. **Encadenable**: La salida de un paso es la entrada del siguiente
4. **Serializable**: Se puede guardar y cargar completo

### Concepto 2: Transformers vs Estimators

En scikit-learn, hay dos tipos de componentes:

#### Transformers

Modifican los datos sin hacer predicciones.

```python
# Ejemplos de Transformers
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA

# Todos tienen estos métodos:
# - fit(X): Aprende parámetros de los datos
# - transform(X): Aplica la transformación
# - fit_transform(X): Hace ambos (solo en entrenamiento)
```

**Analogía**: Un transformer es como un filtro de agua. Aprende (fit) las impurezas que debe eliminar mirando una muestra, y luego transforma (transform) toda el agua que pasa.

#### Estimators

Hacen predicciones.

```python
# Ejemplos de Estimators
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# Todos tienen estos métodos:
# - fit(X, y): Entrena el modelo
# - predict(X): Hace predicciones
# - score(X, y): Evalúa el rendimiento
```

**Regla importante**: En un Pipeline, todos los pasos excepto el último deben ser Transformers. El último puede ser Transformer o Estimator.

```python
# ✅ CORRECTO: Transformers + Estimator final
Pipeline([
    ('imputer', SimpleImputer()),      # Transformer
    ('scaler', StandardScaler()),       # Transformer
    ('model', RandomForestClassifier()) # Estimator (último)
])

# ✅ CORRECTO: Solo Transformers (para preprocesamiento)
Pipeline([
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler()),
    ('encoder', OneHotEncoder())
])

# ❌ INCORRECTO: Estimator no al final
Pipeline([
    ('model', RandomForestClassifier()),  # ¡Error! No puede estar aquí
    ('scaler', StandardScaler())
])
```

### Concepto 3: ColumnTransformer

**El problema**: Diferentes columnas necesitan diferentes transformaciones.

```python
# Datos típicos
# edad (numérica) → Escalar
# salario (numérica) → Escalar
# ciudad (categórica) → One-Hot Encoding
# educacion (ordinal) → Label Encoding
```

**Analogía**: Es como un restaurante con diferentes estaciones de cocina. La carne va a la parrilla, el pescado al horno, las verduras al wok. Cada ingrediente va a la estación correcta.

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Definir qué columnas van a cada transformación
numeric_features = ['edad', 'salario', 'antiguedad']
categorical_features = ['ciudad', 'departamento']

# Pipeline para numéricas
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline para categóricas
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combinar con ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)
```

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ColumnTransformer                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Datos de Entrada                                                   │
│  ┌──────┬────────┬────────┬───────────┬─────────────┐              │
│  │ edad │ salario│ciudad  │departamento│ antiguedad │              │
│  └──┬───┴────┬───┴────┬───┴─────┬─────┴──────┬──────┘              │
│     │        │        │         │            │                      │
│     ▼        ▼        ▼         ▼            ▼                      │
│  ┌──────────────┐  ┌────────────────────────┐                      │
│  │  Numéricas   │  │     Categóricas        │                      │
│  │  ┌────────┐  │  │  ┌─────────────────┐   │                      │
│  │  │Imputer │  │  │  │Imputer          │   │                      │
│  │  └───┬────┘  │  │  └────────┬────────┘   │                      │
│  │      ▼       │  │           ▼            │                      │
│  │  ┌────────┐  │  │  ┌─────────────────┐   │                      │
│  │  │Scaler  │  │  │  │OneHotEncoder    │   │                      │
│  │  └───┬────┘  │  │  └────────┬────────┘   │                      │
│  └──────┼───────┘  └───────────┼────────────┘                      │
│         │                      │                                    │
│         └──────────┬───────────┘                                    │
│                    ▼                                                │
│           [Datos Transformados]                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Concepto 4: Train/Test/Validation Split

**El problema**: ¿Cómo sabemos si nuestro modelo funciona bien?

**Analogía**: Es como estudiar para un examen. Si estudias con las mismas preguntas que vendrán en el examen, sacarás buena nota, pero no sabrás si realmente aprendiste. Necesitas practicar con preguntas diferentes a las del examen real.

#### Split Simple: Train/Test

```python
from sklearn.model_selection import train_test_split

# Dividir datos: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,  # Reproducibilidad
    stratify=y        # Mantener proporción de clases
)
```

**Problema**: ¿Qué pasa si necesitas ajustar hiperparámetros? Si usas el test set para esto, estás "contaminando" tu evaluación.

#### Split Completo: Train/Validation/Test

```python
# Paso 1: Separar test set (intocable hasta el final)
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Paso 2: Separar validation de training
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42  # 0.25 * 0.8 = 0.2
)

# Resultado: 60% train, 20% validation, 20% test
```

```
┌─────────────────────────────────────────────────────────────────────┐
│                    División de Datos                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Datos Totales (100%)                                               │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                                                                │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                              │                                      │
│              ┌───────────────┴───────────────┐                     │
│              ▼                               ▼                      │
│  ┌──────────────────────────┐    ┌─────────────────────┐           │
│  │    Train + Val (80%)     │    │    Test (20%)       │           │
│  │                          │    │                     │           │
│  │  ┌────────┐ ┌─────────┐  │    │  NUNCA tocar hasta  │           │
│  │  │Train   │ │ Val     │  │    │  evaluación final   │           │
│  │  │ (60%)  │ │ (20%)   │  │    │                     │           │
│  │  └────────┘ └─────────┘  │    └─────────────────────┘           │
│  └──────────────────────────┘                                      │
│                                                                     │
│  Uso de cada conjunto:                                              │
│  - Train: Entrenar el modelo                                        │
│  - Validation: Ajustar hiperparámetros, early stopping             │
│  - Test: Evaluación final única                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Concepto 5: Cross-Validation

**El problema**: Con un solo split train/val, la evaluación depende mucho de qué datos cayeron en cada conjunto. Si por casualidad los datos "fáciles" cayeron en validación, tu modelo parecerá mejor de lo que es.

**Analogía**: Imagina que quieres saber si eres bueno jugando al fútbol. Si solo juegas un partido contra un equipo muy malo, pensarás que eres excelente. Pero si juegas 5 partidos contra equipos diferentes, tendrás una idea más realista de tu nivel.

**Cross-Validation** divide los datos en K partes (folds) y entrena K modelos, cada uno usando una parte diferente como validación.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    5-Fold Cross-Validation                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Fold 1: [VAL][Train][Train][Train][Train] → Score 1                │
│  Fold 2: [Train][VAL][Train][Train][Train] → Score 2                │
│  Fold 3: [Train][Train][VAL][Train][Train] → Score 3                │
│  Fold 4: [Train][Train][Train][VAL][Train] → Score 4                │
│  Fold 5: [Train][Train][Train][Train][VAL] → Score 5                │
│                                                                     │
│  Score Final = promedio(Score 1, 2, 3, 4, 5)                        │
│  Varianza = qué tan estable es el modelo                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

```python
from sklearn.model_selection import cross_val_score

# Cross-validation con 5 folds
scores = cross_val_score(
    pipeline,
    X_train,
    y_train,
    cv=5,
    scoring='accuracy'
)

print(f"Scores por fold: {scores}")
print(f"Media: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

#### Tipos de Cross-Validation

| Tipo | Uso | Descripción |
|------|-----|-------------|
| **KFold** | Datos balanceados | Divide en K partes iguales |
| **StratifiedKFold** | Clasificación desbalanceada | Mantiene proporción de clases |
| **TimeSeriesSplit** | Series temporales | Respeta el orden temporal |
| **LeaveOneOut** | Datasets pequeños | Cada muestra es un fold |
| **GroupKFold** | Datos con grupos | Mantiene grupos juntos |

```python
from sklearn.model_selection import (
    KFold, StratifiedKFold, TimeSeriesSplit, cross_val_score
)

# Para clasificación con clases desbalanceadas
cv_stratified = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X, y, cv=cv_stratified)

# Para series temporales (NO mezclar datos)
cv_time = TimeSeriesSplit(n_splits=5)
scores = cross_val_score(pipeline, X, y, cv=cv_time)
```

### Concepto 6: Búsqueda de Hiperparámetros

**El problema**: Los modelos tienen parámetros que no se aprenden de los datos (hiperparámetros). ¿Cómo encontramos los mejores?

**Analogía**: Es como cocinar un plato nuevo. Podrías probar todas las combinaciones de sal, pimienta y especias (exhaustivo pero lento), o probar combinaciones aleatorias hasta encontrar algo bueno (más rápido pero impreciso).

#### Grid Search (Búsqueda Exhaustiva)

Prueba TODAS las combinaciones posibles.

```python
from sklearn.model_selection import GridSearchCV

# Definir parámetros a probar
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [3, 5, 10, None],
    'classifier__min_samples_split': [2, 5, 10]
}

# Total de combinaciones: 3 * 4 * 3 = 36 modelos a entrenar

grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1  # Usar todos los cores
)

grid_search.fit(X_train, y_train)

print(f"Mejores parámetros: {grid_search.best_params_}")
print(f"Mejor score: {grid_search.best_score_:.3f}")
```

#### Random Search (Búsqueda Aleatoria)

Prueba combinaciones aleatorias. Sorprendentemente efectivo.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# Definir distribuciones de parámetros
param_distributions = {
    'classifier__n_estimators': randint(50, 300),
    'classifier__max_depth': randint(3, 20),
    'classifier__min_samples_split': randint(2, 20),
    'classifier__min_samples_leaf': randint(1, 10)
}

random_search = RandomizedSearchCV(
    pipeline,
    param_distributions,
    n_iter=50,  # Probar 50 combinaciones aleatorias
    cv=5,
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)

random_search.fit(X_train, y_train)
```

**¿Cuál usar?**

| Método | Ventaja | Desventaja | Usar cuando... |
|--------|---------|------------|----------------|
| Grid Search | Exhaustivo | Lento con muchos params | Pocos hiperparámetros |
| Random Search | Rápido | Puede perder óptimo | Muchos hiperparámetros |

### Concepto 7: Evitar Data Leakage

**Data Leakage** es cuando información del test set "filtra" al entrenamiento, dando métricas artificialmente buenas.

**Analogía**: Es como si el estudiante viera las respuestas del examen antes de hacerlo. Sacará 10, pero no ha aprendido nada.

#### Errores Comunes de Leakage

```python
# ❌ ERROR 1: Escalar ANTES de split
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # ¡Usa info de TODO X, incluido test!
X_train, X_test = train_test_split(X_scaled)

# ✅ CORRECTO: Escalar DESPUÉS de split
X_train, X_test = train_test_split(X)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # Solo fit en train
X_test_scaled = scaler.transform(X_test)        # Solo transform en test


# ❌ ERROR 2: Imputar con media global
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)  # Media incluye test set
X_train, X_test = train_test_split(X_imputed)

# ✅ CORRECTO: Usar Pipeline (hace fit/transform correctamente)
pipeline = Pipeline([
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipeline.fit(X_train, y_train)  # Fit de todos los pasos solo con train


# ❌ ERROR 3: Feature engineering con datos futuros
df['precio_promedio_futuro'] = df['precio'].rolling(window=7).mean().shift(-7)
# ¡Estás usando datos del futuro para predecir el presente!

# ✅ CORRECTO: Solo usar datos pasados
df['precio_promedio_pasado'] = df['precio'].rolling(window=7).mean().shift(1)
```

#### La Regla de Oro

> **Todo lo que calcules (media, std, categorías, etc.) debe venir SOLO del training set.**
>
> El test set es el futuro. No puedes saber nada sobre el futuro cuando entrenas.

---

## Aplicaciones Prácticas en Data Engineering

### Caso de Uso 1: Pipeline de Clasificación de Clientes

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score

# Definir tipos de columnas
numeric_features = ['edad', 'ingresos', 'antiguedad_meses']
categorical_features = ['segmento', 'canal_adquisicion', 'region']

# Preprocesador
preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), numeric_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='desconocido')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ]), categorical_features)
])

# Pipeline completo
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Entrenar y evaluar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
pipeline.fit(X_train, y_train)

# Cross-validation
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
print(f"CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std()*2:.3f})")
```

### Caso de Uso 2: Pipeline con Selección de Features

```python
from sklearn.feature_selection import SelectKBest, f_classif

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('feature_selection', SelectKBest(f_classif, k=10)),  # Top 10 features
    ('classifier', RandomForestClassifier())
])
```

### Caso de Uso 3: Pipeline para Producción

```python
import joblib

# Entrenar pipeline
pipeline.fit(X_train, y_train)

# Guardar para producción
joblib.dump(pipeline, 'modelo_clasificacion_v1.pkl')

# En producción: cargar y usar
def predict_cliente(datos_nuevos: dict) -> str:
    """Predice la categoría de un cliente nuevo."""
    pipeline = joblib.load('modelo_clasificacion_v1.pkl')

    # Convertir dict a DataFrame
    df = pd.DataFrame([datos_nuevos])

    # Predecir (el pipeline aplica TODOS los pasos)
    prediccion = pipeline.predict(df)

    return prediccion[0]
```

---

## Errores Comunes

### Error 1: Olvidar Stratify en Clasificación Desbalanceada

```python
# ❌ INCORRECTO: Sin stratify
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Si tienes 5% de clase positiva, podrías tener 0% en test por azar

# ✅ CORRECTO: Con stratify
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y
)
# Mantiene la proporción 95%/5% en ambos conjuntos
```

### Error 2: Usar el Test Set para Ajustar Hiperparámetros

```python
# ❌ INCORRECTO
for params in param_combinations:
    model = Model(**params)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)  # ¡Estás optimizando para test!
    if score > best_score:
        best_params = params

# ✅ CORRECTO: Usar cross-validation
grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)  # Solo usa train
final_score = grid_search.score(X_test, y_test)  # Test solo al final
```

### Error 3: No Guardar el Pipeline Completo

```python
# ❌ INCORRECTO: Solo guardar el modelo
joblib.dump(model, 'model.pkl')
# En producción: ¿cómo escalo? ¿cómo imputo? ¿qué encoder uso?

# ✅ CORRECTO: Guardar pipeline completo
joblib.dump(pipeline, 'pipeline.pkl')
# En producción: todo incluido
```

### Error 4: Mezclar Datos Temporales

```python
# ❌ INCORRECTO: Shuffle en series temporales
X_train, X_test = train_test_split(X, test_size=0.2, shuffle=True)
# Puedes entrenar con datos del futuro

# ✅ CORRECTO: Mantener orden temporal
X_train, X_test = train_test_split(X, test_size=0.2, shuffle=False)
# O usar TimeSeriesSplit
```

---

## Checklist de Aprendizaje

Al terminar este tema, deberías poder:

- [ ] Explicar qué es un Pipeline y por qué es importante
- [ ] Diferenciar entre Transformers y Estimators
- [ ] Usar ColumnTransformer para diferentes tipos de columnas
- [ ] Implementar train/test/validation split correctamente
- [ ] Aplicar cross-validation para evaluación robusta
- [ ] Usar GridSearchCV y RandomizedSearchCV
- [ ] Identificar y evitar data leakage
- [ ] Guardar y cargar pipelines para producción

---

## Resumen

| Concepto | Qué Hace | Cuándo Usarlo |
|----------|----------|---------------|
| **Pipeline** | Encadena transformaciones | Siempre en producción |
| **ColumnTransformer** | Aplica diferentes transformaciones por columna | Datos mixtos (num + cat) |
| **train_test_split** | Divide datos | Evaluación básica |
| **cross_val_score** | Evalúa con múltiples folds | Evaluación robusta |
| **GridSearchCV** | Busca hiperparámetros exhaustivamente | Pocos hiperparámetros |
| **RandomizedSearchCV** | Busca hiperparámetros aleatoriamente | Muchos hiperparámetros |
| **StratifiedKFold** | CV manteniendo proporción de clases | Clasificación desbalanceada |
| **TimeSeriesSplit** | CV respetando orden temporal | Series temporales |

---

## Próximo Paso

En la siguiente sección veremos ejemplos prácticos de pipelines completos con código ejecutable.

[Continuar a 02-EJEMPLOS.md →](02-EJEMPLOS.md)
