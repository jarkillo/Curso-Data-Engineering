"""
Módulo de transformación Silver → Gold.

Agrega y calcula métricas analíticas sobre datos Silver.
"""

import pandas as pd


def agregar_noticias_por_fuente(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega noticias por fuente.

    Args:
        df: DataFrame Silver con noticias

    Returns:
        DataFrame agregado con métricas por fuente

    Examples:
        >>> df = pd.DataFrame({"fuente": ["A", "A"], "longitud_contenido": [10, 20]})
        >>> df_agg = agregar_noticias_por_fuente(df)
        >>> "total_noticias" in df_agg.columns
        True
    """
    df_agg = (
        df.groupby("fuente")
        .agg(
            total_noticias=("fuente", "size"),
            longitud_promedio_contenido=("longitud_contenido", "mean"),
            longitud_promedio_titulo=("longitud_titulo", "mean"),
        )
        .reset_index()
    )

    # Redondear promedios
    df_agg["longitud_promedio_contenido"] = df_agg["longitud_promedio_contenido"].round(
        1
    )
    df_agg["longitud_promedio_titulo"] = df_agg["longitud_promedio_titulo"].round(1)

    return df_agg


def agregar_noticias_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega noticias por categoría.

    Args:
        df: DataFrame Silver con noticias

    Returns:
        DataFrame agregado con métricas por categoría (ordenado descendente)

    Examples:
        >>> df = pd.DataFrame({"categoria": ["A", "A", "B"]})
        >>> df_agg = agregar_noticias_por_categoria(df)
        >>> df_agg["total_noticias"].is_monotonic_decreasing
        True
    """
    df_agg = (
        df.groupby("categoria").agg(total_noticias=("categoria", "size")).reset_index()
    )

    # Ordenar por total descendente
    df_agg = df_agg.sort_values("total_noticias", ascending=False).reset_index(
        drop=True
    )

    return df_agg


def agregar_metricas_temporales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega métricas temporales (fecha, día de semana, hora).

    Args:
        df: DataFrame Silver con columna fecha_publicacion

    Returns:
        DataFrame con métricas temporales agregadas

    Examples:
        >>> df = pd.DataFrame({"fecha_publicacion": pd.to_datetime(["2024-01-15 10:30"])})
        >>> df_temporal = agregar_metricas_temporales(df)
        >>> "fecha" in df_temporal.columns
        True
    """
    df_temporal = df.copy()

    # Extraer fecha sin hora
    df_temporal["fecha"] = df_temporal["fecha_publicacion"].dt.date
    df_temporal["fecha"] = pd.to_datetime(df_temporal["fecha"])

    # Extraer día de la semana (0=Lunes, 6=Domingo)
    df_temporal["dia_semana"] = df_temporal["fecha_publicacion"].dt.dayofweek

    # Extraer hora
    df_temporal["hora"] = df_temporal["fecha_publicacion"].dt.hour

    return df_temporal


def calcular_estadisticas_longitud(df: pd.DataFrame, columna: str) -> dict:
    """
    Calcula estadísticas descriptivas de una columna de longitud.

    Args:
        df: DataFrame con datos
        columna: Nombre de columna a analizar

    Returns:
        Diccionario con estadísticas (min, max, mean, median)

    Raises:
        KeyError: Si columna no existe

    Examples:
        >>> df = pd.DataFrame({"longitud": [10, 20, 30]})
        >>> stats = calcular_estadisticas_longitud(df, "longitud")
        >>> stats["mean"]
        20.0
    """
    if columna not in df.columns:
        raise KeyError(f"Columna '{columna}' no existe en el DataFrame")

    return {
        "min": int(df[columna].min()),
        "max": int(df[columna].max()),
        "mean": round(float(df[columna].mean()), 1),
        "median": float(df[columna].median()),
    }


def transformar_silver_a_gold(df_silver: pd.DataFrame) -> dict:
    """
    Transforma DataFrame Silver a Gold (capa analítica).

    Genera múltiples agregaciones y estadísticas:
    - Agregación por fuente
    - Agregación por categoría
    - Estadísticas de longitud de contenido y título

    Args:
        df_silver: DataFrame en formato Silver

    Returns:
        Diccionario con:
        - "por_fuente": DataFrame agregado por fuente
        - "por_categoria": DataFrame agregado por categoría
        - "estadisticas": Dict con estadísticas descriptivas

    Raises:
        ValueError: Si DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({
        ...     "fuente": ["A"],
        ...     "categoria": ["tech"],
        ...     "longitud_contenido": [100],
        ...     "longitud_titulo": [20]
        ... })
        >>> resultado = transformar_silver_a_gold(df)
        >>> "por_fuente" in resultado
        True
    """
    if df_silver.empty:
        raise ValueError("No se puede transformar DataFrame vacío")

    # Agregar por fuente
    df_por_fuente = agregar_noticias_por_fuente(df_silver)

    # Agregar por categoría
    df_por_categoria = agregar_noticias_por_categoria(df_silver)

    # Calcular estadísticas de longitud
    estadisticas = {
        "contenido": calcular_estadisticas_longitud(df_silver, "longitud_contenido"),
        "titulo": calcular_estadisticas_longitud(df_silver, "longitud_titulo"),
    }

    return {
        "por_fuente": df_por_fuente,
        "por_categoria": df_por_categoria,
        "estadisticas": estadisticas,
    }
