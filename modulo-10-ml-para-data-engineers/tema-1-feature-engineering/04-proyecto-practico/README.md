# Proyecto Práctico: Feature Engineering Pipeline

Pipeline de transformación de features para Machine Learning, implementado con enfoque funcional y TDD.

## Objetivos

- Implementar transformadores de features reutilizables
- Aplicar técnicas de encoding para variables categóricas
- Implementar scalers para normalización de datos
- Manejar valores faltantes y outliers
- Crear código production-ready con >80% de cobertura de tests

## Conceptos Clave

### Encoding

El encoding transforma variables categóricas en números que los modelos de ML pueden procesar.

**Analogía**: Es como traducir de español a código binario. Los modelos solo "hablan" números.

**Tipos**:
- **Ordinal**: Para categorías con orden natural (bajo < medio < alto)
- **One-Hot**: Para categorías sin orden (rojo, azul, verde)
- **Cíclico**: Para valores que se repiten (horas, días, meses)

### Scaling

El scaling normaliza las magnitudes de las variables numéricas.

**Analogía**: Imagina comparar metros con kilómetros. Sin normalizar, el modelo daría más importancia a la columna con números más grandes.

**Tipos**:
- **Standard**: Media=0, Std=1. Para datos normales.
- **MinMax**: Rango [0,1]. Para redes neuronales.
- **Robust**: Usa mediana/IQR. Resistente a outliers.

## Estructura del Proyecto

```
04-proyecto-practico/
├── src/
│   ├── __init__.py
│   └── feature_transformers.py   # Funciones principales
├── tests/
│   ├── __init__.py
│   └── test_feature_transformers.py  # Tests
├── examples/
│   └── example_usage.py          # Ejemplos de uso
├── README.md
└── requirements.txt
```

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar Tests

```bash
# Tests básicos
pytest -v

# Con cobertura
pytest --cov=src --cov-report=term-missing --cov-report=html

# Verificar cobertura >80%
pytest --cov=src --cov-fail-under=80
```

## Funciones Implementadas

### `encode_ordinal`

```python
def encode_ordinal(values: list, order: list[str]) -> list[int]:
    """Codifica variables categóricas ordinales a números."""
```

**Descripción**: Convierte categorías con orden natural a valores numéricos.

**Parámetros**:
- `values` (list): Valores categóricos a codificar
- `order` (list[str]): Categorías en orden ascendente

**Returns**: Lista de enteros

**Raises**:
- `ValueError`: Si hay categorías desconocidas o el orden está vacío

**Ejemplo**:
```python
>>> from src.feature_transformers import encode_ordinal
>>> encode_ordinal(['bajo', 'alto', 'medio'], ['bajo', 'medio', 'alto'])
[0, 2, 1]
```

---

### `encode_onehot`

```python
def encode_onehot(values: list, prefix: str | None = None) -> pd.DataFrame:
    """Aplica One-Hot Encoding a variables categóricas nominales."""
```

**Descripción**: Crea columnas binarias para cada categoría única.

**Parámetros**:
- `values` (list): Valores categóricos
- `prefix` (str, optional): Prefijo para nombres de columnas

**Returns**: DataFrame con columnas binarias

**Ejemplo**:
```python
>>> from src.feature_transformers import encode_onehot
>>> df = encode_onehot(['A', 'B', 'A'], prefix='cat')
>>> print(df)
   cat_A  cat_B
0      1      0
1      0      1
2      1      0
```

---

### `encode_cyclic`

```python
def encode_cyclic(values: int | list, max_val: int) -> tuple | np.ndarray:
    """Codifica valores cíclicos usando seno y coseno."""
```

**Descripción**: Convierte valores cíclicos (horas, días) en representación seno/coseno.

**Parámetros**:
- `values`: Valor(es) a codificar
- `max_val` (int): Valor máximo del ciclo

**Returns**: Tupla (sin, cos) o array (n, 2)

**Ejemplo**:
```python
>>> from src.feature_transformers import encode_cyclic
>>> sin, cos = encode_cyclic(12, 24)  # Mediodía
>>> print(f"sin={sin:.2f}, cos={cos:.2f}")
sin=0.00, cos=-1.00
```

---

### `scale_standard`

```python
def scale_standard(values: list, params: dict | None = None) -> tuple[np.ndarray, dict]:
    """Aplica StandardScaler (Z-score normalization)."""
```

**Descripción**: Transforma datos a media=0, std=1.

**Parámetros**:
- `values` (list): Valores numéricos
- `params` (dict, optional): Parámetros pre-calculados para producción

**Returns**: Tupla (valores_escalados, parámetros)

**Ejemplo**:
```python
>>> from src.feature_transformers import scale_standard
>>> scaled, params = scale_standard([10, 20, 30])
>>> print(f"Media: {scaled.mean():.2f}")
Media: 0.00
```

---

### `scale_minmax`

```python
def scale_minmax(values: list, feature_range: tuple = (0, 1)) -> tuple[np.ndarray, dict]:
    """Aplica MinMaxScaler para escalar a un rango específico."""
```

**Descripción**: Escala valores a un rango definido.

**Ejemplo**:
```python
>>> from src.feature_transformers import scale_minmax
>>> scaled, _ = scale_minmax([0, 50, 100])
>>> print(scaled)
[0.  0.5 1. ]
```

---

### `scale_robust`

```python
def scale_robust(values: list, params: dict | None = None) -> tuple[np.ndarray, dict]:
    """Aplica RobustScaler usando mediana e IQR."""
```

**Descripción**: Escalado robusto a outliers.

---

### `impute_numeric`

```python
def impute_numeric(values: list, strategy: str = "median", fill_value: float | None = None) -> np.ndarray:
    """Imputa valores faltantes en datos numéricos."""
```

**Descripción**: Reemplaza NaN usando la estrategia especificada.

**Estrategias**: `'mean'`, `'median'`, `'constant'`

**Ejemplo**:
```python
>>> import numpy as np
>>> from src.feature_transformers import impute_numeric
>>> impute_numeric([1, np.nan, 3], strategy='median')
array([1., 2., 3.])
```

---

### `impute_categorical`

```python
def impute_categorical(values: list, strategy: str = "mode", fill_value: str | None = None) -> list:
    """Imputa valores faltantes en datos categóricos."""
```

**Estrategias**: `'mode'`, `'constant'`

---

### `detect_outliers_iqr`

```python
def detect_outliers_iqr(values: list, multiplier: float = 1.5) -> np.ndarray:
    """Detecta outliers usando el método IQR."""
```

**Descripción**: Retorna máscara booleana donde True indica outlier.

---

### `detect_outliers_zscore`

```python
def detect_outliers_zscore(values: list, threshold: float = 3.0) -> np.ndarray:
    """Detecta outliers usando Z-score."""
```

---

### `cap_outliers`

```python
def cap_outliers(values: list, lower_percentile: float = 1, upper_percentile: float = 99) -> np.ndarray:
    """Limita outliers a percentiles específicos."""
```

---

## Ejemplos de Uso

### Pipeline básico de encoding

```python
from src.feature_transformers import encode_ordinal, encode_onehot, scale_standard
import pandas as pd

# Datos de ejemplo
data = pd.DataFrame({
    'educacion': ['secundaria', 'universidad', 'master'],
    'ciudad': ['Madrid', 'Barcelona', 'Valencia'],
    'salario': [30000, 50000, 70000]
})

# 1. Encoding ordinal para educación
educacion_encoded = encode_ordinal(
    data['educacion'].tolist(),
    ['secundaria', 'universidad', 'master', 'doctorado']
)

# 2. One-hot encoding para ciudad
ciudad_onehot = encode_onehot(data['ciudad'].tolist(), prefix='ciudad')

# 3. Scaling para salario
salario_scaled, params = scale_standard(data['salario'].tolist())

# 4. Combinar
df_final = pd.DataFrame({
    'educacion': educacion_encoded,
    'salario': salario_scaled
})
df_final = pd.concat([df_final, ciudad_onehot], axis=1)

print(df_final)
```

### Uso en producción (reutilizando parámetros)

```python
from src.feature_transformers import scale_standard

# Entrenamiento: calcular parámetros
train_data = [10, 20, 30, 40, 50]
scaled_train, params = scale_standard(train_data)

# Guardar params para producción
# joblib.dump(params, 'scaler_params.pkl')

# Producción: aplicar mismos parámetros
new_data = [25, 35]
scaled_new, _ = scale_standard(new_data, params=params)
```

### Manejo de missing values

```python
import numpy as np
from src.feature_transformers import impute_numeric, impute_categorical

# Numéricos
valores_num = [10, np.nan, 30, np.nan, 50]
imputados = impute_numeric(valores_num, strategy='median')
print(imputados)  # [10. 30. 30. 30. 50.]

# Categóricos
valores_cat = ['A', None, 'A', 'B', None]
imputados = impute_categorical(valores_cat, strategy='mode')
print(imputados)  # ['A', 'A', 'A', 'B', 'A']
```

## Troubleshooting

### Error: "Categoría desconocida"

**Mensaje**: `ValueError: Categoría desconocida: 'X'. Categorías válidas: [...]`

**Causa**: La categoría no está en la lista de orden para encode_ordinal.

**Solución**:
```python
# Asegúrate de incluir todas las categorías posibles
order = ['bajo', 'medio', 'alto', 'muy_alto']  # Incluir 'muy_alto'
encode_ordinal(['muy_alto'], order)
```

### Error: "La desviación estándar es cero"

**Mensaje**: `ValueError: La desviación estándar es cero. Todos los valores son iguales.`

**Causa**: Todos los valores son idénticos, no se puede escalar.

**Solución**: Verificar los datos o usar MinMaxScaler que no requiere varianza.

### Error: "Todos los valores son NaN"

**Causa**: Intentando imputar cuando no hay valores válidos.

**Solución**: Verificar que al menos hay un valor no-NaN en los datos.

## Recursos Adicionales

- [01-TEORIA.md](../01-TEORIA.md) - Conceptos fundamentales
- [02-EJEMPLOS.md](../02-EJEMPLOS.md) - Ejemplos trabajados
- [03-EJERCICIOS.md](../03-EJERCICIOS.md) - Ejercicios prácticos
- [scikit-learn preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)
