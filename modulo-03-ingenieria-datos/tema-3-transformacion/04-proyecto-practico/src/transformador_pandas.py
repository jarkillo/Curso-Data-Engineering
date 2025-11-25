"""
Módulo de transformación de datos con Pandas.

Proporciona funciones para aplicar transformaciones y enriquecimientos a los datos.
"""

from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd


def calcular_columnas_derivadas(
    df: pd.DataFrame, formulas: dict[str, str]
) -> pd.DataFrame:
    """
    Calcula columnas derivadas usando expresiones eval de pandas.

    Args:
        df: DataFrame base
        formulas: Diccionario {nueva_columna: 'expresion'}

    Returns:
        DataFrame con columnas calculadas

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> formulas = {'c': 'a + b', 'd': 'a * b'}
        >>> resultado = calcular_columnas_derivadas(df, formulas)
        >>> 'c' in resultado.columns
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    df_resultado = df.copy()

    for nueva_col, formula in formulas.items():
        try:
            df_resultado[nueva_col] = df_resultado.eval(formula)
        except Exception as e:
            raise ValueError(
                f"Error al evaluar '{formula}' para columna '{nueva_col}': {str(e)}"
            )

    return df_resultado


def aplicar_transformacion_por_fila(
    df: pd.DataFrame, columna: str, funcion: Callable
) -> pd.DataFrame:
    """
    Aplica una función personalizada a cada fila de una columna.

    Args:
        df: DataFrame a transformar
        columna: Nombre de la columna a transformar
        funcion: Función a aplicar

    Returns:
        DataFrame con columna transformada

    Raises:
        ValueError: Si el DataFrame está vacío o columna no existe

    Examples:
        >>> df = pd.DataFrame({'precio': [100, 200, 300]})
        >>> resultado = aplicar_transformacion_por_fila(df, 'precio', lambda x: x * 1.21)
        >>> resultado['precio'].tolist()
        [121.0, 242.0, 363.0]
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame")

    df_resultado = df.copy()
    df_resultado[columna] = df_resultado[columna].apply(funcion)

    return df_resultado


def categorizar_valores(
    df: pd.DataFrame, columna: str, nueva_columna: str, categorias: dict[str, Callable]
) -> pd.DataFrame:
    """
    Categoriza valores de una columna basándose en condiciones.

    Args:
        df: DataFrame a transformar
        columna: Columna a categorizar
        nueva_columna: Nombre de la nueva columna con categorías
        categorias: Dict {nombre_categoria: función_condición}

    Returns:
        DataFrame con nueva columna de categorías

    Raises:
        ValueError: Si el DataFrame está vacío o columna no existe

    Examples:
        >>> df = pd.DataFrame({'edad': [10, 25, 60]})
        >>> categorias = {
        ...     'Joven': lambda x: x < 30,
        ...     'Adulto': lambda x: 30 <= x < 60,
        ...     'Senior': lambda x: x >= 60
        ... }
        >>> resultado = categorizar_valores(df, 'edad', 'categoria', categorias)
        >>> resultado['categoria'].tolist()
        ['Joven', 'Joven', 'Senior']
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame")

    df_resultado = df.copy()

    def aplicar_categoria(valor):
        for categoria, condicion in categorias.items():
            if condicion(valor):
                return categoria
        return "Otros"

    df_resultado[nueva_columna] = df_resultado[columna].apply(aplicar_categoria)

    return df_resultado


def agregar_metricas_por_grupo(
    df: pd.DataFrame,
    columna_agrupacion: str,
    columna_metrica: str,
    agregaciones: list[str],
) -> pd.DataFrame:
    """
    Agrega métricas calculadas por grupo a cada fila (transform).

    Args:
        df: DataFrame a enriquecer
        columna_agrupacion: Columna por la que agrupar
        columna_metrica: Columna sobre la que calcular métricas
        agregaciones: Lista de agregaciones ('mean', 'sum', 'count', etc.)

    Returns:
        DataFrame con columnas de métricas por grupo

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen

    Examples:
        >>> df = pd.DataFrame({
        ...     'categoria': ['A', 'A', 'B'],
        ...     'ventas': [100, 200, 150]
        ... })
        >>> resultado = agregar_metricas_por_grupo(df, 'categoria', 'ventas', ['mean', 'sum'])
        >>> 'ventas_mean' in resultado.columns
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna_agrupacion not in df.columns:
        raise ValueError(f"La columna '{columna_agrupacion}' no existe")

    if columna_metrica not in df.columns:
        raise ValueError(f"La columna '{columna_metrica}' no existe")

    df_resultado = df.copy()

    for agregacion in agregaciones:
        nombre_nueva_col = f"{columna_metrica}_{agregacion}"
        df_resultado[nombre_nueva_col] = df_resultado.groupby(columna_agrupacion)[
            columna_metrica
        ].transform(agregacion)

    return df_resultado


def aplicar_ventana_movil(
    df: pd.DataFrame, columna: str, ventana: int, operacion: str = "mean"
) -> pd.DataFrame:
    """
    Aplica operación de ventana móvil (rolling window).

    Args:
        df: DataFrame con datos ordenados
        columna: Columna sobre la que aplicar rolling
        ventana: Tamaño de la ventana
        operacion: Operación ('mean', 'sum', 'std', 'min', 'max')

    Returns:
        DataFrame con nueva columna rolling

    Raises:
        ValueError: Si el DataFrame está vacío o parámetros inválidos

    Examples:
        >>> df = pd.DataFrame({'ventas': [10, 20, 30, 40]})
        >>> resultado = aplicar_ventana_movil(df, 'ventas', 2, 'mean')
        >>> 'ventas_rolling_mean' in resultado.columns
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe")

    if ventana < 1:
        raise ValueError("La ventana debe ser >= 1")

    operaciones_validas = ["mean", "sum", "std", "min", "max"]
    if operacion not in operaciones_validas:
        raise ValueError(f"Operación debe ser una de: {operaciones_validas}")

    df_resultado = df.copy()
    nombre_nueva_col = f"{columna}_rolling_{operacion}"

    serie_rolling = df_resultado[columna].rolling(window=ventana)

    if operacion == "mean":
        df_resultado[nombre_nueva_col] = serie_rolling.mean()
    elif operacion == "sum":
        df_resultado[nombre_nueva_col] = serie_rolling.sum()
    elif operacion == "std":
        df_resultado[nombre_nueva_col] = serie_rolling.std()
    elif operacion == "min":
        df_resultado[nombre_nueva_col] = serie_rolling.min()
    elif operacion == "max":
        df_resultado[nombre_nueva_col] = serie_rolling.max()

    return df_resultado


def crear_columna_condicional(
    df: pd.DataFrame, nueva_columna: str, condiciones: list[tuple], default: Any = None
) -> pd.DataFrame:
    """
    Crea columna basada en múltiples condiciones (np.select style).

    Args:
        df: DataFrame base
        nueva_columna: Nombre de la nueva columna
        condiciones: Lista de tuplas (condicion_booleana, valor_si_true)
        default: Valor por defecto si ninguna condición se cumple

    Returns:
        DataFrame con nueva columna condicional

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'precio': [10, 50, 150]})
        >>> condiciones = [
        ...     (df['precio'] < 50, 'Bajo'),
        ...     (df['precio'] < 100, 'Medio')
        ... ]
        >>> resultado = crear_columna_condicional(df, 'rango', condiciones, 'Alto')
        >>> resultado['rango'].tolist()
        ['Bajo', 'Medio', 'Alto']
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    df_resultado = df.copy()

    # Extraer condiciones y valores
    lista_condiciones = [cond for cond, _ in condiciones]
    lista_valores = [val for _, val in condiciones]

    df_resultado[nueva_columna] = np.select(
        lista_condiciones, lista_valores, default=default
    )

    return df_resultado


def extraer_informacion_temporal(
    df: pd.DataFrame, columna_fecha: str, componentes: list[str]
) -> pd.DataFrame:
    """
    Extrae componentes temporales de una columna de fecha.

    Args:
        df: DataFrame con columna de fecha
        columna_fecha: Nombre de la columna con fechas
        componentes: Lista de componentes a extraer
                    ('year', 'month', 'day', 'weekday', 'quarter', 'dayofweek')

    Returns:
        DataFrame con columnas temporales extraídas

    Raises:
        ValueError: Si el DataFrame está vacío o columna no existe

    Examples:
        >>> df = pd.DataFrame({'fecha': ['2024-01-15', '2024-02-20']})
        >>> df['fecha'] = pd.to_datetime(df['fecha'])
        >>> resultado = extraer_informacion_temporal(df, 'fecha', ['year', 'month'])
        >>> 'fecha_year' in resultado.columns
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna_fecha not in df.columns:
        raise ValueError(f"La columna '{columna_fecha}' no existe")

    df_resultado = df.copy()

    # Convertir a datetime si no lo es
    if not pd.api.types.is_datetime64_any_dtype(df_resultado[columna_fecha]):
        df_resultado[columna_fecha] = pd.to_datetime(df_resultado[columna_fecha])

    # Mapeo de componentes a atributos datetime
    mapeo_componentes = {
        "year": lambda dt: dt.year,
        "month": lambda dt: dt.month,
        "day": lambda dt: dt.day,
        "weekday": lambda dt: dt.day_name(),
        "quarter": lambda dt: dt.quarter,
        "dayofweek": lambda dt: dt.dayofweek,
    }

    # Extraer componentes
    for componente in componentes:
        if componente not in mapeo_componentes:
            raise ValueError(f"Componente '{componente}' no reconocido")

        nombre_nueva_col = f"{columna_fecha}_{componente}"
        df_resultado[nombre_nueva_col] = mapeo_componentes[componente](
            df_resultado[columna_fecha].dt
        )

    return df_resultado


def aplicar_transformacion_condicional_compleja(
    df: pd.DataFrame, nueva_columna: str, funcion_transformacion: Callable
) -> pd.DataFrame:
    """
    Aplica una función de transformación que recibe la fila completa.

    Args:
        df: DataFrame a transformar
        nueva_columna: Nombre de la columna resultante
        funcion_transformacion: Función que recibe pd.Series (fila) y retorna valor

    Returns:
        DataFrame con nueva columna transformada

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> def calc(row):
        ...     return row['a'] + row['b'] if row['a'] > 0 else 0
        >>> resultado = aplicar_transformacion_condicional_compleja(df, 'c', calc)
        >>> resultado['c'].tolist()
        [4, 6]
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    df_resultado = df.copy()
    df_resultado[nueva_columna] = df_resultado.apply(funcion_transformacion, axis=1)

    return df_resultado
