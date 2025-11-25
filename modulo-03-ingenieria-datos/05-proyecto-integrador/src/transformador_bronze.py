"""
Módulo de transformación Bronze → Silver.

Limpia, normaliza y valida datos crudos para generar capa Silver.
"""

import pandas as pd


def limpiar_textos(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """
    Limpia textos eliminando espacios extras.

    Args:
        df: DataFrame a limpiar
        columnas: Lista de columnas a limpiar

    Returns:
        DataFrame con textos limpios

    Examples:
        >>> df = pd.DataFrame({"col": ["  texto  "]})
        >>> df_limpio = limpiar_textos(df, ["col"])
        >>> df_limpio["col"].iloc[0]
        'texto'
    """
    df_limpio = df.copy()

    for col in columnas:
        if col in df_limpio.columns:
            df_limpio[col] = df_limpio[col].str.strip()

    return df_limpio


def normalizar_columnas(df: pd.DataFrame, mapeo: dict[str, str]) -> pd.DataFrame:
    """
    Renombra columnas según mapeo.

    Args:
        df: DataFrame a normalizar
        mapeo: Diccionario {nombre_viejo: nombre_nuevo}

    Returns:
        DataFrame con columnas renombradas

    Examples:
        >>> df = pd.DataFrame({"old": [1]})
        >>> mapeo = {"old": "new"}
        >>> df_normalizado = normalizar_columnas(df, mapeo)
        >>> "new" in df_normalizado.columns
        True
    """
    return df.rename(columns=mapeo)


def convertir_fechas(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """
    Convierte columna de fecha a datetime.

    Args:
        df: DataFrame a convertir
        columna: Nombre de columna de fecha

    Returns:
        DataFrame con fecha como datetime

    Examples:
        >>> df = pd.DataFrame({"fecha": ["2024-01-01"]})
        >>> df_convertido = convertir_fechas(df, "fecha")
        >>> pd.api.types.is_datetime64_any_dtype(df_convertido["fecha"])
        True
    """
    df_convertido = df.copy()

    # Convertir con errors='coerce' para manejar fechas inválidas
    df_convertido[columna] = pd.to_datetime(df_convertido[columna], errors="coerce")

    return df_convertido


def eliminar_registros_invalidos(
    df: pd.DataFrame, columnas_criticas: list[str]
) -> pd.DataFrame:
    """
    Elimina registros con valores nulos en columnas críticas.

    Args:
        df: DataFrame a limpiar
        columnas_criticas: Columnas que no deben tener nulos

    Returns:
        DataFrame sin registros inválidos

    Examples:
        >>> df = pd.DataFrame({"id": [1, None, 3]})
        >>> df_limpio = eliminar_registros_invalidos(df, ["id"])
        >>> len(df_limpio)
        2
    """
    df_limpio = df.copy()

    for col in columnas_criticas:
        if col in df_limpio.columns:
            df_limpio = df_limpio[df_limpio[col].notna()]

    return df_limpio


def agregar_metricas_basicas(
    df: pd.DataFrame, columna_contenido: str, columna_titulo: str
) -> pd.DataFrame:
    """
    Agrega métricas básicas de longitud.

    Args:
        df: DataFrame al que agregar métricas
        columna_contenido: Nombre de columna de contenido
        columna_titulo: Nombre de columna de título

    Returns:
        DataFrame con métricas agregadas

    Examples:
        >>> df = pd.DataFrame({"contenido": ["Hola"], "titulo": ["Test"]})
        >>> df_metricas = agregar_metricas_basicas(df, "contenido", "titulo")
        >>> "longitud_contenido" in df_metricas.columns
        True
    """
    df_con_metricas = df.copy()

    # Agregar longitud de contenido
    if columna_contenido in df_con_metricas.columns:
        df_con_metricas["longitud_contenido"] = df_con_metricas[
            columna_contenido
        ].str.len()

    # Agregar longitud de título
    if columna_titulo in df_con_metricas.columns:
        df_con_metricas["longitud_titulo"] = df_con_metricas[columna_titulo].str.len()

    return df_con_metricas


def transformar_bronze_a_silver(df_bronze: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma DataFrame Bronze a Silver.

    Pipeline completo:
    1. Validar que no esté vacío
    2. Limpiar textos
    3. Normalizar nombres de columnas
    4. Convertir fechas
    5. Eliminar registros inválidos
    6. Agregar métricas básicas

    Args:
        df_bronze: DataFrame en formato Bronze

    Returns:
        DataFrame en formato Silver

    Raises:
        ValueError: Si DataFrame está vacío

    Examples:
        >>> df_bronze = pd.DataFrame({
        ...     "title": ["Test"],
        ...     "published_date": ["2024-01-01"]
        ... })
        >>> df_silver = transformar_bronze_a_silver(df_bronze)
        >>> "titulo" in df_silver.columns
        True
    """
    if df_bronze.empty:
        raise ValueError("No se puede transformar DataFrame vacío")

    df = df_bronze.copy()

    # 1. Limpiar textos
    columnas_texto = ["title", "content", "author", "source", "category"]
    df = limpiar_textos(df, columnas_texto)

    # 2. Normalizar columnas (inglés → español)
    mapeo = {
        "title": "titulo",
        "content": "contenido",
        "author": "autor",
        "published_date": "fecha_publicacion",
        "source": "fuente",
        "category": "categoria",
    }
    df = normalizar_columnas(df, mapeo)

    # 3. Convertir fechas
    df = convertir_fechas(df, "fecha_publicacion")

    # 4. Eliminar registros inválidos
    columnas_criticas = ["titulo", "fecha_publicacion"]
    df = eliminar_registros_invalidos(df, columnas_criticas)

    # 5. Agregar métricas básicas
    df = agregar_metricas_basicas(df, "contenido", "titulo")

    return df
