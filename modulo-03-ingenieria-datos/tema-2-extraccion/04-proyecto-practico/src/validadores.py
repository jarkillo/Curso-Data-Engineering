"""
Módulo de validación de datos extraídos.

Funciones para validar la calidad y consistencia de datos.
"""

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def validar_no_vacio(df: pd.DataFrame) -> dict[str, Any]:
    """
    Valida que el DataFrame no esté vacío.

    Args:
        df: DataFrame a validar

    Returns:
        Dict con resultado de validación
    """
    es_valido = len(df) > 0
    return {
        "valido": es_valido,
        "mensaje": "OK" if es_valido else "DataFrame vacío",
        "num_filas": len(df),
    }


def validar_columnas_requeridas(
    df: pd.DataFrame, columnas: list[str]
) -> dict[str, Any]:
    """
    Valida que existan las columnas requeridas.

    Args:
        df: DataFrame a validar
        columnas: Columnas requeridas

    Returns:
        Dict con resultado de validación
    """
    columnas_presentes = set(df.columns)
    columnas_esperadas = set(columnas)
    columnas_faltantes = columnas_esperadas - columnas_presentes

    es_valido = len(columnas_faltantes) == 0

    return {
        "valido": es_valido,
        "mensaje": "OK" if es_valido else f"Faltan columnas: {columnas_faltantes}",
        "columnas_faltantes": list(columnas_faltantes),
    }


def validar_tipos_datos(df: pd.DataFrame, schema: dict[str, type]) -> dict[str, Any]:
    """
    Valida los tipos de datos de las columnas.

    Args:
        df: DataFrame a validar
        schema: Dict con nombre_columna: tipo_esperado

    Returns:
        Dict con resultado de validación
    """
    errores = []

    for columna, tipo_esperado in schema.items():
        if columna not in df.columns:
            errores.append(f"Columna '{columna}' no existe")
            continue

        # Verificación simplificada de tipos
        if tipo_esperado in [int, float]:
            if not pd.api.types.is_numeric_dtype(df[columna]):
                errores.append(f"Columna '{columna}' debe ser numérica")
        elif tipo_esperado == str:
            if (
                not pd.api.types.is_string_dtype(df[columna])
                and df[columna].dtype != object
            ):
                errores.append(f"Columna '{columna}' debe ser string")

    es_valido = len(errores) == 0

    return {
        "valido": es_valido,
        "mensaje": "OK" if es_valido else f"Errores de tipo: {errores}",
        "errores": errores,
    }


def validar_valores_nulos(
    df: pd.DataFrame,
    columnas_no_nulas: list[str] | None = None,
    porcentaje_max_nulos: float = 0.1,
) -> dict[str, Any]:
    """
    Valida porcentaje de valores nulos.

    Args:
        df: DataFrame a validar
        columnas_no_nulas: Columnas que no deben tener nulos
        porcentaje_max_nulos: Porcentaje máximo de nulos permitido

    Returns:
        Dict con resultado de validación
    """
    errores = []

    # Verificar columnas que no deben tener nulos
    if columnas_no_nulas:
        for columna in columnas_no_nulas:
            if columna in df.columns:
                num_nulos = df[columna].isnull().sum()
                if num_nulos > 0:
                    errores.append(f"Columna '{columna}' tiene {num_nulos} nulos")

    # Verificar porcentaje global
    porcentaje_nulos = df.isnull().sum().sum() / (len(df) * len(df.columns))
    if porcentaje_nulos > porcentaje_max_nulos:
        errores.append(
            f"Porcentaje de nulos ({porcentaje_nulos:.1%}) "
            f"excede máximo permitido ({porcentaje_max_nulos:.1%})"
        )

    es_valido = len(errores) == 0

    return {
        "valido": es_valido,
        "mensaje": "OK" if es_valido else f"Errores de nulos: {errores}",
        "errores": errores,
        "porcentaje_nulos": porcentaje_nulos,
    }


def validar_valores_duplicados(
    df: pd.DataFrame, columnas_clave: list[str] | None = None
) -> dict[str, Any]:
    """
    Valida duplicados en el DataFrame.

    Args:
        df: DataFrame a validar
        columnas_clave: Columnas que definen unicidad

    Returns:
        Dict con resultado de validación
    """
    if columnas_clave:
        num_duplicados = df.duplicated(subset=columnas_clave).sum()
    else:
        num_duplicados = df.duplicated().sum()

    es_valido = num_duplicados == 0

    return {
        "valido": es_valido,
        "mensaje": "OK" if es_valido else f"Encontrados {num_duplicados} duplicados",
        "num_duplicados": int(num_duplicados),
    }


def generar_reporte_validacion(
    df: pd.DataFrame, validaciones: dict[str, dict]
) -> dict[str, Any]:
    """
    Genera reporte completo de validación.

    Args:
        df: DataFrame validado
        validaciones: Dict con resultados de cada validación

    Returns:
        Reporte completo
    """
    validaciones_ok = sum(1 for v in validaciones.values() if v["valido"])
    total_validaciones = len(validaciones)

    return {
        "resumen": {
            "validaciones_exitosas": validaciones_ok,
            "validaciones_fallidas": total_validaciones - validaciones_ok,
            "porcentaje_exito": (
                validaciones_ok / total_validaciones if total_validaciones > 0 else 0
            ),
            "num_filas": len(df),
            "num_columnas": len(df.columns),
        },
        "detalle": validaciones,
        "todo_valido": validaciones_ok == total_validaciones,
    }
