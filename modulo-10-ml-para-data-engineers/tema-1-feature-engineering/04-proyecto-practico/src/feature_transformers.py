"""
Módulo de transformadores de features para Machine Learning.

Este módulo proporciona funciones puras para transformar datos crudos
en features aptas para modelos de ML. Todas las funciones siguen
principios funcionales: sin efectos secundarios, tipado explícito,
y manejo de errores específico.

Funciones disponibles:
- Encoding: encode_ordinal, encode_onehot, encode_cyclic
- Scaling: scale_standard, scale_minmax, scale_robust
- Imputación: impute_numeric, impute_categorical
- Outliers: detect_outliers_iqr, detect_outliers_zscore, cap_outliers
"""

import numpy as np
import pandas as pd

# =============================================================================
# ENCODING FUNCTIONS
# =============================================================================


def encode_ordinal(values: list | pd.Series, order: list[str]) -> list[int]:
    """
    Codifica variables categóricas ordinales a números.

    Convierte categorías con orden natural a valores numéricos
    respetando la jerarquía especificada.

    Args:
        values: Lista o Series con los valores categóricos a codificar
        order: Lista con las categorías en orden ascendente

    Returns:
        Lista de enteros representando las categorías codificadas

    Raises:
        ValueError: Si el orden está vacío o hay categorías desconocidas

    Examples:
        >>> encode_ordinal(['bajo', 'alto', 'medio'], ['bajo', 'medio', 'alto'])
        [0, 2, 1]
        >>> encode_ordinal(['S', 'M', 'L'], ['XS', 'S', 'M', 'L', 'XL'])
        [1, 2, 3]
    """
    if len(order) == 0:
        raise ValueError("El orden no puede estar vacío")

    if len(values) == 0:
        return []

    order_map = {cat: idx for idx, cat in enumerate(order)}

    result = []
    for val in values:
        if val not in order_map:
            raise ValueError(
                f"Categoría desconocida: '{val}'. Categorías válidas: {order}"
            )
        result.append(order_map[val])

    return result


def encode_onehot(values: list | pd.Series, prefix: str | None = None) -> pd.DataFrame:
    """
    Aplica One-Hot Encoding a variables categóricas nominales.

    Crea una columna binaria (0/1) para cada categoría única.

    Args:
        values: Lista o Series con los valores categóricos
        prefix: Prefijo opcional para los nombres de columnas

    Returns:
        DataFrame con columnas binarias para cada categoría

    Examples:
        >>> encode_onehot(['A', 'B', 'A'])
           A  B
        0  1  0
        1  0  1
        2  1  0

        >>> encode_onehot(['rojo', 'azul'], prefix='color')
           color_azul  color_rojo
        0          0           1
        1          1           0
    """
    if len(values) == 0:
        return pd.DataFrame()

    series = pd.Series(values)
    return pd.get_dummies(series, prefix=prefix, dtype=int)


def encode_cyclic(
    values: int | float | list | np.ndarray, max_val: int
) -> tuple[float, float] | np.ndarray:
    """
    Codifica valores cíclicos usando seno y coseno.

    Convierte valores que representan ciclos (horas, días, meses)
    en representaciones seno/coseno que preservan la naturaleza
    cíclica de los datos.

    Args:
        values: Valor(es) a codificar
        max_val: Valor máximo del ciclo (24 para horas, 7 para días, etc.)

    Returns:
        Si es un solo valor: tupla (seno, coseno)
        Si es lista/array: array de shape (n, 2) con columnas [sin, cos]

    Raises:
        ValueError: Si max_val es cero o negativo

    Examples:
        >>> sin, cos = encode_cyclic(0, 24)  # Medianoche
        >>> print(f"sin={sin:.2f}, cos={cos:.2f}")
        sin=0.00, cos=1.00

        >>> encode_cyclic([0, 12], 24)  # Medianoche y mediodía
        array([[ 0., 1.], [ 0., -1.]])
    """
    if max_val <= 0:
        raise ValueError("max_val debe ser mayor que cero")

    is_scalar = np.isscalar(values)
    values_arr = np.atleast_1d(values).astype(float)

    angle = 2 * np.pi * values_arr / max_val
    sin_val = np.sin(angle)
    cos_val = np.cos(angle)

    if is_scalar:
        return float(sin_val[0]), float(cos_val[0])

    return np.column_stack([sin_val, cos_val])


# =============================================================================
# SCALING FUNCTIONS
# =============================================================================


def scale_standard(
    values: list | np.ndarray, params: dict | None = None
) -> tuple[np.ndarray, dict]:
    """
    Aplica StandardScaler (Z-score normalization).

    Transforma los datos para que tengan media=0 y desviación estándar=1.
    Fórmula: z = (x - mean) / std

    Args:
        values: Lista o array de valores numéricos
        params: Diccionario opcional con 'mean' y 'std' pre-calculados
                (usar para aplicar a datos de test/producción)

    Returns:
        Tupla de (valores_escalados, parámetros)
        Los parámetros incluyen 'mean' y 'std' para uso en producción

    Raises:
        ValueError: Si la lista está vacía o la desviación estándar es cero

    Examples:
        >>> scaled, params = scale_standard([10, 20, 30])
        >>> print(f"Media: {scaled.mean():.2f}, Std: {scaled.std():.2f}")
        Media: 0.00, Std: 1.00
    """
    values_arr = np.array(values, dtype=float)

    if len(values_arr) == 0:
        raise ValueError("La lista de valores no puede estar vacía")

    if params is None:
        mean = float(np.mean(values_arr))
        std = float(np.std(values_arr))

        if std == 0:
            raise ValueError(
                "La desviación estándar es cero. Todos los valores son iguales."
            )

        params = {"mean": mean, "std": std}
    else:
        mean = params["mean"]
        std = params["std"]

    scaled = (values_arr - mean) / std
    return scaled, params


def scale_minmax(
    values: list | np.ndarray,
    feature_range: tuple[float, float] = (0, 1),
    params: dict | None = None,
) -> tuple[np.ndarray, dict]:
    """
    Aplica MinMaxScaler para escalar a un rango específico.

    Transforma los datos al rango especificado (por defecto [0, 1]).
    Fórmula: x_scaled = (x - min) / (max - min) * (range_max - range_min) + range_min

    Args:
        values: Lista o array de valores numéricos
        feature_range: Tupla (min, max) del rango objetivo
        params: Diccionario opcional con 'min' y 'max' pre-calculados

    Returns:
        Tupla de (valores_escalados, parámetros)

    Raises:
        ValueError: Si la lista está vacía o min == max

    Examples:
        >>> scaled, params = scale_minmax([0, 50, 100])
        >>> print(scaled)
        [0.0, 0.5, 1.0]

        >>> scaled, _ = scale_minmax([0, 50, 100], feature_range=(-1, 1))
        >>> print(scaled)
        [-1.0, 0.0, 1.0]
    """
    values_arr = np.array(values, dtype=float)

    if len(values_arr) == 0:
        raise ValueError("La lista de valores no puede estar vacía")

    range_min, range_max = feature_range

    if params is None:
        data_min = float(np.min(values_arr))
        data_max = float(np.max(values_arr))
        params = {"min": data_min, "max": data_max}
    else:
        data_min = params["min"]
        data_max = params["max"]

    if data_max == data_min:
        raise ValueError("Min y max son iguales. No se puede escalar.")

    scaled = (values_arr - data_min) / (data_max - data_min)
    scaled = scaled * (range_max - range_min) + range_min

    return scaled, params


def scale_robust(
    values: list | np.ndarray, params: dict | None = None
) -> tuple[np.ndarray, dict]:
    """
    Aplica RobustScaler usando mediana e IQR.

    Escala usando estadísticos robustos (mediana, rango intercuartílico)
    que son menos sensibles a outliers que media y std.
    Fórmula: x_scaled = (x - median) / IQR

    Args:
        values: Lista o array de valores numéricos
        params: Diccionario opcional con 'median' e 'iqr' pre-calculados

    Returns:
        Tupla de (valores_escalados, parámetros)

    Examples:
        >>> values = [1, 2, 3, 4, 5, 100]  # 100 es outlier
        >>> scaled, params = scale_robust(values)
        >>> print(f"Mediana usada: {params['median']}")
    """
    values_arr = np.array(values, dtype=float)

    if len(values_arr) == 0:
        raise ValueError("La lista de valores no puede estar vacía")

    if params is None:
        median = float(np.median(values_arr))
        q1 = float(np.percentile(values_arr, 25))
        q3 = float(np.percentile(values_arr, 75))
        iqr = q3 - q1

        if iqr == 0:
            iqr = 1.0  # Evitar división por cero

        params = {"median": median, "iqr": iqr, "q1": q1, "q3": q3}
    else:
        median = params["median"]
        iqr = params["iqr"]

    scaled = (values_arr - median) / iqr
    return scaled, params


# =============================================================================
# IMPUTATION FUNCTIONS
# =============================================================================


def impute_numeric(
    values: list | np.ndarray,
    strategy: str = "median",
    fill_value: float | None = None,
) -> np.ndarray:
    """
    Imputa valores faltantes en datos numéricos.

    Reemplaza valores NaN usando la estrategia especificada.

    Args:
        values: Lista o array con posibles valores NaN
        strategy: Estrategia de imputación ('mean', 'median', 'constant')
        fill_value: Valor a usar si strategy='constant'

    Returns:
        Array con valores imputados

    Raises:
        ValueError: Si todos son NaN o estrategia inválida

    Examples:
        >>> impute_numeric([1, np.nan, 3], strategy='mean')
        array([1., 2., 3.])

        >>> impute_numeric([1, np.nan, 5], strategy='median')
        array([1., 3., 5.])

        >>> impute_numeric([1, np.nan, 3], strategy='constant', fill_value=0)
        array([1., 0., 3.])
    """
    values_arr = np.array(values, dtype=float)
    mask = np.isnan(values_arr)

    # Verificar que no todos sean NaN
    if mask.all():
        raise ValueError("Todos los valores son NaN. No se puede imputar.")

    valid_strategies = ["mean", "median", "constant"]
    if strategy not in valid_strategies:
        raise ValueError(
            f"Estrategia no válida: '{strategy}'. Opciones: {valid_strategies}"
        )

    if strategy == "mean":
        fill = np.nanmean(values_arr)
    elif strategy == "median":
        fill = np.nanmedian(values_arr)
    elif strategy == "constant":
        if fill_value is None:
            raise ValueError("fill_value requerido para strategy='constant'")
        fill = fill_value

    result = values_arr.copy()
    result[mask] = fill
    return result


def impute_categorical(
    values: list | pd.Series,
    strategy: str = "mode",
    fill_value: str | None = None,
) -> list:
    """
    Imputa valores faltantes en datos categóricos.

    Reemplaza valores None/NaN usando la estrategia especificada.

    Args:
        values: Lista o Series con posibles valores None/NaN
        strategy: Estrategia de imputación ('mode', 'constant')
        fill_value: Valor a usar si strategy='constant'

    Returns:
        Lista con valores imputados

    Examples:
        >>> impute_categorical(['A', None, 'A', 'B'], strategy='mode')
        ['A', 'A', 'A', 'B']

        >>> impute_categorical(['A', None, 'B'], strategy='constant', fill_value='X')
        ['A', 'X', 'B']
    """
    series = pd.Series(values)

    if strategy == "mode":
        mode = series.mode()
        if len(mode) > 0:
            fill = mode.iloc[0]
        else:
            raise ValueError("No se puede calcular la moda. Todos son None.")
    elif strategy == "constant":
        if fill_value is None:
            raise ValueError("fill_value requerido para strategy='constant'")
        fill = fill_value
    else:
        raise ValueError(f"Estrategia no válida: '{strategy}'")

    result = series.fillna(fill)
    return result.tolist()


# =============================================================================
# OUTLIER FUNCTIONS
# =============================================================================


def detect_outliers_iqr(
    values: list | np.ndarray, multiplier: float = 1.5
) -> np.ndarray:
    """
    Detecta outliers usando el método IQR.

    Un valor es outlier si está fuera del rango:
    [Q1 - multiplier*IQR, Q3 + multiplier*IQR]

    Args:
        values: Lista o array de valores numéricos
        multiplier: Factor multiplicador del IQR (default 1.5)

    Returns:
        Array booleano donde True indica outlier

    Examples:
        >>> values = [1, 2, 3, 4, 5, 100]
        >>> outliers = detect_outliers_iqr(values)
        >>> print(values[outliers])
        [100]
    """
    values_arr = np.array(values, dtype=float)

    q1 = np.percentile(values_arr, 25)
    q3 = np.percentile(values_arr, 75)
    iqr = q3 - q1

    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    outliers = (values_arr < lower_bound) | (values_arr > upper_bound)
    return outliers


def detect_outliers_zscore(
    values: list | np.ndarray, threshold: float = 3.0
) -> np.ndarray:
    """
    Detecta outliers usando Z-score.

    Un valor es outlier si |z-score| > threshold.

    Args:
        values: Lista o array de valores numéricos
        threshold: Umbral de Z-score (default 3.0)

    Returns:
        Array booleano donde True indica outlier

    Examples:
        >>> values = [10, 12, 11, 13, 100]
        >>> outliers = detect_outliers_zscore(values, threshold=2)
        >>> print(outliers)
        [False, False, False, False, True]
    """
    values_arr = np.array(values, dtype=float)

    mean = np.mean(values_arr)
    std = np.std(values_arr)

    if std == 0:
        return np.zeros(len(values_arr), dtype=bool)

    z_scores = np.abs((values_arr - mean) / std)
    outliers = z_scores > threshold
    return outliers


def cap_outliers(
    values: list | np.ndarray,
    lower_percentile: float = 1,
    upper_percentile: float = 99,
) -> np.ndarray:
    """
    Limita outliers a percentiles específicos (capping/winsorization).

    Reemplaza valores por debajo del percentil inferior y por encima
    del percentil superior con los valores de esos percentiles.

    Args:
        values: Lista o array de valores numéricos
        lower_percentile: Percentil inferior (default 1)
        upper_percentile: Percentil superior (default 99)

    Returns:
        Array con outliers limitados

    Examples:
        >>> values = [-100, 1, 2, 3, 4, 5, 200]
        >>> capped = cap_outliers(values, lower_percentile=5, upper_percentile=95)
        >>> print(f"Min: {capped.min():.1f}, Max: {capped.max():.1f}")
    """
    values_arr = np.array(values, dtype=float)

    lower_bound = np.percentile(values_arr, lower_percentile)
    upper_bound = np.percentile(values_arr, upper_percentile)

    capped = np.clip(values_arr, lower_bound, upper_bound)
    return capped
