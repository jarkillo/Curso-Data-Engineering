"""
Módulo de limpieza de datos.

Proporciona funciones para limpiar y normalizar datos crudos.
"""

from typing import Any

import numpy as np
import pandas as pd


def eliminar_duplicados_completos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas completamente duplicadas del DataFrame.

    Args:
        df: DataFrame con posibles duplicados

    Returns:
        DataFrame sin duplicados

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'a': [1, 1, 2], 'b': [1, 1, 2]})
        >>> resultado = eliminar_duplicados_completos(df)
        >>> len(resultado)
        2
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    df_sin_duplicados = df.drop_duplicates()
    return df_sin_duplicados.reset_index(drop=True)


def eliminar_filas_sin_id(df: pd.DataFrame, columna_id: str = "id") -> pd.DataFrame:
    """
    Elimina filas que no tengan ID válido.

    Args:
        df: DataFrame con datos
        columna_id: Nombre de la columna de ID

    Returns:
        DataFrame sin filas con ID nulo

    Raises:
        ValueError: Si la columna no existe o el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'id': [1, None, 3], 'valor': [10, 20, 30]})
        >>> resultado = eliminar_filas_sin_id(df)
        >>> len(resultado)
        2
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna_id not in df.columns:
        raise ValueError(f"La columna '{columna_id}' no existe en el DataFrame")

    df_limpio = df.dropna(subset=[columna_id])
    return df_limpio.reset_index(drop=True)


def rellenar_valores_nulos(
    df: pd.DataFrame, estrategias: dict[str, Any]
) -> pd.DataFrame:
    """
    Rellena valores nulos según estrategias específicas por columna.

    Args:
        df: DataFrame con valores nulos
        estrategias: Diccionario {columna: valor_relleno_o_estrategia}
                    Estrategias: 'mean', 'median', 'mode', o un valor específico

    Returns:
        DataFrame con valores nulos rellenados

    Raises:
        ValueError: Si el DataFrame está vacío
        TypeError: Si la estrategia no es válida

    Examples:
        >>> df = pd.DataFrame({'a': [1, None, 3], 'b': ['x', None, 'z']})
        >>> estrategias = {'a': 'mean', 'b': 'desconocido'}
        >>> resultado = rellenar_valores_nulos(df, estrategias)
        >>> resultado['a'].isnull().sum()
        0
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    df_rellenado = df.copy()

    for columna, estrategia in estrategias.items():
        if columna not in df_rellenado.columns:
            continue

        if estrategia == "mean":
            valor = df_rellenado[columna].mean()
        elif estrategia == "median":
            valor = df_rellenado[columna].median()
        elif estrategia == "mode":
            valor = (
                df_rellenado[columna].mode()[0]
                if not df_rellenado[columna].mode().empty
                else None
            )
        else:
            valor = estrategia

        df_rellenado[columna] = df_rellenado[columna].fillna(valor)

    return df_rellenado


def normalizar_texto(
    df: pd.DataFrame, columnas: list[str], convertir_a: str = "title"
) -> pd.DataFrame:
    """
    Normaliza columnas de texto (mayúsculas, minúsculas, title case, trim).

    Args:
        df: DataFrame con columnas de texto
        columnas: Lista de nombres de columnas a normalizar
        convertir_a: Tipo de normalización ('lower', 'upper', 'title', 'strip')

    Returns:
        DataFrame con texto normalizado

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen
        TypeError: Si convertir_a no es válido

    Examples:
        >>> df = pd.DataFrame({'nombre': ['  JUAN  ', 'maria']})
        >>> resultado = normalizar_texto(df, ['nombre'], 'title')
        >>> resultado['nombre'].tolist()
        ['Juan', 'Maria']
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    tipos_validos = ["lower", "upper", "title", "strip"]
    if convertir_a not in tipos_validos:
        raise TypeError(f"convertir_a debe ser uno de: {tipos_validos}")

    df_normalizado = df.copy()

    for columna in columnas:
        if columna not in df_normalizado.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame")

        # Asegurar que sea string
        df_normalizado[columna] = df_normalizado[columna].astype(str)

        # Siempre hacer strip primero
        df_normalizado[columna] = df_normalizado[columna].str.strip()

        # Aplicar transformación
        if convertir_a == "lower":
            df_normalizado[columna] = df_normalizado[columna].str.lower()
        elif convertir_a == "upper":
            df_normalizado[columna] = df_normalizado[columna].str.upper()
        elif convertir_a == "title":
            df_normalizado[columna] = df_normalizado[columna].str.title()

    return df_normalizado


def validar_rangos_numericos(
    df: pd.DataFrame, rangos: dict[str, tuple]
) -> pd.DataFrame:
    """Valida que valores numéricos estén dentro de rangos válidos.

    Valores fuera de rango se convierten a NaN.

    Args:
        df: DataFrame con columnas numéricas
        rangos: Diccionario {columna: (min, max)}

    Returns:
        DataFrame con valores fuera de rango convertidos a NaN

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen

    Examples:
        >>> df = pd.DataFrame({'edad': [25, 150, 30]})
        >>> rangos = {'edad': (0, 120)}
        >>> resultado = validar_rangos_numericos(df, rangos)
        >>> resultado['edad'].tolist()
        [25.0, nan, 30.0]
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    df_validado = df.copy()

    for columna, (minimo, maximo) in rangos.items():
        if columna not in df_validado.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame")

        # Convertir a numérico si no lo es
        df_validado[columna] = pd.to_numeric(df_validado[columna], errors="coerce")

        # Validar rango
        mascara = (df_validado[columna] < minimo) | (df_validado[columna] > maximo)
        df_validado.loc[mascara, columna] = np.nan

    return df_validado


def eliminar_filas_con_errores_criticos(
    df: pd.DataFrame, columnas_criticas: list[str]
) -> pd.DataFrame:
    """
    Elimina filas que tengan valores nulos en columnas críticas.

    Args:
        df: DataFrame con datos
        columnas_criticas: Lista de columnas que no pueden tener nulos

    Returns:
        DataFrame sin filas con errores críticos

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen

    Examples:
        >>> df = pd.DataFrame({
        ...     'id': [1, 2, 3],
        ...     'nombre': ['Ana', None, 'Carlos'],
        ...     'email': ['a@test.com', 'b@test.com', None]
        ... })
        >>> resultado = eliminar_filas_con_errores_criticos(df, ['nombre', 'email'])
        >>> len(resultado)
        1
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    for columna in columnas_criticas:
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame")

    df_limpio = df.dropna(subset=columnas_criticas)
    return df_limpio.reset_index(drop=True)
