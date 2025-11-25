"""
Módulo de validación de esquemas y calidad de datos.

Proporciona funciones para validar la estructura y calidad de los datos.
"""

from typing import Any

import numpy as np
import pandas as pd


def validar_columnas_requeridas(
    df: pd.DataFrame, columnas_requeridas: list[str]
) -> tuple[bool, list[str]]:
    """
    Valida que el DataFrame contenga las columnas requeridas.

    Args:
        df: DataFrame a validar
        columnas_requeridas: Lista de nombres de columnas requeridas

    Returns:
        Tupla (es_valido, lista_de_columnas_faltantes)

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'a': [1], 'b': [2]})
        >>> es_valido, faltantes = validar_columnas_requeridas(df, ['a', 'b', 'c'])
        >>> es_valido
        False
        >>> faltantes
        ['c']
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    columnas_actuales = set(df.columns)
    columnas_req = set(columnas_requeridas)

    columnas_faltantes = list(columnas_req - columnas_actuales)

    es_valido = len(columnas_faltantes) == 0

    return es_valido, columnas_faltantes


def validar_tipos_de_datos(
    df: pd.DataFrame, tipos_esperados: dict[str, str]
) -> tuple[bool, dict[str, dict]]:
    """
    Valida que las columnas tengan los tipos de datos esperados.

    Args:
        df: DataFrame a validar
        tipos_esperados: Dict {columna: tipo_esperado}
                        Tipos: 'int', 'float', 'string', 'datetime', 'bool'

    Returns:
        Tupla (es_valido, diccionario_de_errores)
        diccionario_de_errores: {columna: {'esperado': tipo, 'actual': tipo}}

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'edad': [25, 30], 'nombre': ['Ana', 'Juan']})
        >>> tipos = {'edad': 'int', 'nombre': 'string'}
        >>> es_valido, errores = validar_tipos_de_datos(df, tipos)
        >>> es_valido
        True
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    errores = {}

    mapeo_tipos = {
        "int": [np.int8, np.int16, np.int32, np.int64, int],
        "float": [np.float16, np.float32, np.float64, float],
        "string": [object, str],
        "datetime": ["datetime64[ns]"],
        "bool": [bool, np.bool_],
    }

    for columna, tipo_esperado in tipos_esperados.items():
        if columna not in df.columns:
            errores[columna] = {
                "esperado": tipo_esperado,
                "actual": "COLUMNA_NO_EXISTE",
            }
            continue

        tipo_actual = df[columna].dtype

        # Verificar si el tipo coincide
        if tipo_esperado in mapeo_tipos:
            tipos_validos = mapeo_tipos[tipo_esperado]

            # Para datetime, comparar como string
            if tipo_esperado == "datetime":
                if str(tipo_actual) not in tipos_validos:
                    errores[columna] = {
                        "esperado": tipo_esperado,
                        "actual": str(tipo_actual),
                    }
            else:
                if not any(np.issubdtype(tipo_actual, t) for t in tipos_validos):
                    errores[columna] = {
                        "esperado": tipo_esperado,
                        "actual": str(tipo_actual),
                    }

    es_valido = len(errores) == 0

    return es_valido, errores


def validar_completitud_datos(
    df: pd.DataFrame, umbral_minimo: float = 0.8
) -> tuple[bool, pd.Series]:
    """
    Valida que los datos tengan completitud mínima (% de valores no nulos).

    Args:
        df: DataFrame a validar
        umbral_minimo: Porcentaje mínimo de completitud (0 a 1)

    Returns:
        Tupla (es_valido, serie_con_porcentajes_por_columna)

    Raises:
        ValueError: Si el DataFrame está vacío o umbral inválido

    Examples:
        >>> df = pd.DataFrame({
        ...     'a': [1, 2, None, 4],
        ...     'b': [10, 20, 30, 40]
        ... })
        >>> es_valido, completitud = validar_completitud_datos(df, 0.8)
        >>> es_valido
        False
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    if not 0 <= umbral_minimo <= 1:
        raise ValueError("El umbral debe estar entre 0 y 1")

    # Calcular porcentaje de completitud por columna
    total_filas = len(df)
    valores_no_nulos = df.count()
    completitud = (valores_no_nulos / total_filas).round(4)

    # Verificar si todas las columnas cumplen el umbral
    es_valido = (completitud >= umbral_minimo).all()

    return es_valido, completitud


def generar_reporte_calidad(
    df: pd.DataFrame,
    columnas_requeridas: list[str] | None = None,
    tipos_esperados: dict[str, str] | None = None,
    umbral_completitud: float = 0.8,
) -> dict:
    """
    Genera un reporte completo de calidad de datos.

    Args:
        df: DataFrame a analizar
        columnas_requeridas: Lista de columnas que deben existir
        tipos_esperados: Tipos de datos esperados por columna
        umbral_completitud: Umbral mínimo de completitud

    Returns:
        Diccionario con métricas de calidad:
        - total_filas
        - total_columnas
        - columnas_con_nulos
        - porcentaje_nulos_total
        - duplicados_completos
        - validacion_columnas (si se proporcionó columnas_requeridas)
        - validacion_tipos (si se proporcionó tipos_esperados)
        - validacion_completitud
        - es_valido (bool general)

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> reporte = generar_reporte_calidad(df)
        >>> reporte['total_filas']
        2
    """
    if df.empty:
        raise ValueError("El DataFrame no puede estar vacío")

    reporte: dict[str, Any] = {}

    # Métricas básicas
    reporte["total_filas"] = len(df)
    reporte["total_columnas"] = len(df.columns)

    # Análisis de nulos
    nulos_por_columna = df.isnull().sum()
    reporte["columnas_con_nulos"] = (nulos_por_columna > 0).sum()
    reporte["porcentaje_nulos_total"] = round(
        (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2
    )

    # Análisis de duplicados
    reporte["duplicados_completos"] = df.duplicated().sum()
    reporte["porcentaje_duplicados"] = round((df.duplicated().sum() / len(df)) * 100, 2)

    # Validaciones opcionales
    problemas = []

    # Validar columnas requeridas
    if columnas_requeridas is not None:
        valido, faltantes = validar_columnas_requeridas(df, columnas_requeridas)
        reporte["validacion_columnas"] = {
            "es_valido": valido,
            "columnas_faltantes": faltantes,
        }
        if not valido:
            problemas.append("columnas_faltantes")

    # Validar tipos de datos
    if tipos_esperados is not None:
        valido, errores = validar_tipos_de_datos(df, tipos_esperados)
        reporte["validacion_tipos"] = {"es_valido": valido, "errores": errores}
        if not valido:
            problemas.append("tipos_incorrectos")

    # Validar completitud
    valido, completitud = validar_completitud_datos(df, umbral_completitud)
    reporte["validacion_completitud"] = {
        "es_valido": valido,
        "umbral": umbral_completitud,
        "completitud_por_columna": completitud.to_dict(),
    }
    if not valido:
        problemas.append("completitud_insuficiente")

    # Determinar validez general
    reporte["es_valido"] = len(problemas) == 0
    reporte["problemas_encontrados"] = problemas

    return reporte
