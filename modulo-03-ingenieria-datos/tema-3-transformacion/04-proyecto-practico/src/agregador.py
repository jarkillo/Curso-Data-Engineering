"""
Módulo de agregación de datos.

Proporciona funciones para agrupar y agregar datos de diferentes formas.
"""

from typing import Any, Dict, List

import pandas as pd


def agrupar_con_multiples_metricas(
    df: pd.DataFrame, columnas_agrupacion: List[str], agregaciones: Dict[str, List[str]]
) -> pd.DataFrame:
    """
    Agrupa datos y calcula múltiples métricas.

    Args:
        df: DataFrame a agrupar
        columnas_agrupacion: Columnas por las que agrupar
        agregaciones: Dict {columna: [lista_de_agregaciones]}

    Returns:
        DataFrame agregado con métricas calculadas

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen

    Examples:
        >>> df = pd.DataFrame({
        ...     'categoria': ['A', 'A', 'B'],
        ...     'ventas': [100, 200, 150]
        ... })
        >>> aggs = {'ventas': ['sum', 'mean', 'count']}
        >>> resultado = agrupar_con_multiples_metricas(df, ['categoria'], aggs)
        >>> len(resultado)
        2
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    for col in columnas_agrupacion:
        if col not in df.columns:
            raise ValueError(f"La columna de agrupación '{col}' no existe")

    for col in agregaciones.keys():
        if col not in df.columns:
            raise ValueError(f"La columna a agregar '{col}' no existe")

    # Realizar agregación
    resultado = df.groupby(columnas_agrupacion).agg(agregaciones)

    # Aplanar nombres de columnas multinivel
    resultado.columns = ["_".join(col).strip() for col in resultado.columns.values]

    return resultado.reset_index()


def calcular_top_n_por_grupo(
    df: pd.DataFrame,
    columna_agrupacion: str,
    columna_valor: str,
    n: int = 5,
    ascendente: bool = False,
) -> pd.DataFrame:
    """
    Obtiene los top N registros por cada grupo.

    Args:
        df: DataFrame a procesar
        columna_agrupacion: Columna por la que agrupar
        columna_valor: Columna por la que ordenar
        n: Número de registros top a obtener
        ascendente: Si True, obtiene los menores valores

    Returns:
        DataFrame con top N por grupo

    Raises:
        ValueError: Si el DataFrame está vacío o parámetros inválidos

    Examples:
        >>> df = pd.DataFrame({
        ...     'categoria': ['A', 'A', 'B', 'B'],
        ...     'ventas': [100, 200, 150, 250]
        ... })
        >>> resultado = calcular_top_n_por_grupo(df, 'categoria', 'ventas', n=1)
        >>> len(resultado)
        2
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna_agrupacion not in df.columns:
        raise ValueError(f"La columna '{columna_agrupacion}' no existe")

    if columna_valor not in df.columns:
        raise ValueError(f"La columna '{columna_valor}' no existe")

    if n < 1:
        raise ValueError("n debe ser >= 1")

    # Ordenar y obtener top N por grupo
    if ascendente:
        resultado = (
            df.groupby(columna_agrupacion, group_keys=False)
            .apply(lambda x: x.nsmallest(n, columna_valor))
            .reset_index(drop=True)
        )
    else:
        resultado = (
            df.groupby(columna_agrupacion, group_keys=False)
            .apply(lambda x: x.nlargest(n, columna_valor))
            .reset_index(drop=True)
        )

    return resultado


def crear_tabla_pivot(
    df: pd.DataFrame,
    indice: str,
    columnas: str,
    valores: str,
    funcion_agregacion: str = "sum",
    rellenar_nulos: Any = 0,
) -> pd.DataFrame:
    """
    Crea una tabla dinámica (pivot table).

    Args:
        df: DataFrame base
        indice: Columna para el índice de la tabla
        columnas: Columna para las columnas de la tabla
        valores: Columna con los valores a agregar
        funcion_agregacion: Función de agregación ('sum', 'mean', 'count', etc.)
        rellenar_nulos: Valor para rellenar NaN

    Returns:
        DataFrame pivotado

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen

    Examples:
        >>> df = pd.DataFrame({
        ...     'producto': ['A', 'A', 'B'],
        ...     'mes': ['Ene', 'Feb', 'Ene'],
        ...     'ventas': [100, 200, 150]
        ... })
        >>> resultado = crear_tabla_pivot(df, 'producto', 'mes', 'ventas')
        >>> 'Ene' in resultado.columns
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    for col in [indice, columnas, valores]:
        if col not in df.columns:
            raise ValueError(f"La columna '{col}' no existe")

    pivot = pd.pivot_table(
        df,
        values=valores,
        index=indice,
        columns=columnas,
        aggfunc=funcion_agregacion,
        fill_value=rellenar_nulos,
    )

    return pivot.reset_index()


def calcular_porcentajes_por_grupo(
    df: pd.DataFrame, columna_agrupacion: str, columna_valor: str
) -> pd.DataFrame:
    """
    Calcula el porcentaje de cada valor respecto al total del grupo.

    Args:
        df: DataFrame a procesar
        columna_agrupacion: Columna por la que agrupar
        columna_valor: Columna con valores numéricos

    Returns:
        DataFrame con columna de porcentaje añadida

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen

    Examples:
        >>> df = pd.DataFrame({
        ...     'categoria': ['A', 'A', 'B'],
        ...     'ventas': [100, 200, 150]
        ... })
        >>> resultado = calcular_porcentajes_por_grupo(df, 'categoria', 'ventas')
        >>> 'ventas_pct' in resultado.columns
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna_agrupacion not in df.columns:
        raise ValueError(f"La columna '{columna_agrupacion}' no existe")

    if columna_valor not in df.columns:
        raise ValueError(f"La columna '{columna_valor}' no existe")

    df_resultado = df.copy()

    # Calcular total por grupo
    total_por_grupo = df_resultado.groupby(columna_agrupacion)[columna_valor].transform(
        "sum"
    )

    # Calcular porcentaje
    nombre_nueva_col = f"{columna_valor}_pct"
    df_resultado[nombre_nueva_col] = (
        df_resultado[columna_valor] / total_por_grupo * 100
    ).round(2)

    return df_resultado


def generar_resumen_estadistico(
    df: pd.DataFrame, columna_agrupacion: str, columna_valor: str
) -> pd.DataFrame:
    """
    Genera un resumen estadístico completo por grupo.

    Args:
        df: DataFrame a analizar
        columna_agrupacion: Columna por la que agrupar
        columna_valor: Columna con valores numéricos a analizar

    Returns:
        DataFrame con estadísticas por grupo (count, mean, median, std, min, max, etc.)

    Raises:
        ValueError: Si el DataFrame está vacío o columnas no existen

    Examples:
        >>> df = pd.DataFrame({
        ...     'categoria': ['A', 'A', 'B'],
        ...     'ventas': [100, 200, 150]
        ... })
        >>> resultado = generar_resumen_estadistico(df, 'categoria', 'ventas')
        >>> 'count' in resultado.columns
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if columna_agrupacion not in df.columns:
        raise ValueError(f"La columna '{columna_agrupacion}' no existe")

    if columna_valor not in df.columns:
        raise ValueError(f"La columna '{columna_valor}' no existe")

    # Calcular estadísticas
    resumen = (
        df.groupby(columna_agrupacion)[columna_valor]
        .agg(
            [
                ("count", "count"),
                ("sum", "sum"),
                ("mean", "mean"),
                ("median", "median"),
                ("std", "std"),
                ("min", "min"),
                ("max", "max"),
                ("q25", lambda x: x.quantile(0.25)),
                ("q75", lambda x: x.quantile(0.75)),
            ]
        )
        .round(2)
    )

    # Calcular rango y coeficiente de variación
    resumen["range"] = (resumen["max"] - resumen["min"]).round(2)
    resumen["cv"] = ((resumen["std"] / resumen["mean"]) * 100).round(2)

    return resumen.reset_index()
