"""
Funciones de validación para prevenir SQL injection y errores comunes.

IMPORTANTE: Este módulo implementa validaciones de seguridad críticas.
No saltarse estas validaciones bajo ninguna circunstancia.
"""

import re
from typing import Any

import pandas as pd

from src.error_ids import ErrorIds
from src.logging_utils import log_error


def validar_identificador_sql(nombre: str) -> None:
    """
    Valida que un identificador SQL (tabla/columna) sea seguro.

    Previene SQL injection al asegurar que el identificador solo contiene
    caracteres alfanuméricos y guiones bajos.

    Args:
        nombre: Nombre de tabla o columna a validar

    Raises:
        TypeError: Si nombre no es string
        ValueError: Si el identificador contiene caracteres inválidos

    Examples:
        >>> validar_identificador_sql("usuarios")  # OK
        >>> validar_identificador_sql("tabla_ventas_2024")  # OK
        >>> validar_identificador_sql("users; DROP TABLE users; --")  # ValueError!

    Security Notes:
        - Solo permite: letras (a-z, A-Z), números (0-9), guión bajo (_)
        - Debe empezar con letra o guión bajo (no número)
        - Longitud máxima: 64 caracteres (límite de MySQL/PostgreSQL)
    """
    if not isinstance(nombre, str):
        raise TypeError(
            f"Identificador SQL debe ser string, recibido: {type(nombre).__name__}"
        )

    if not nombre:
        raise ValueError("Identificador SQL no puede estar vacío")

    # Validar formato: solo letras, números y guión bajo, empezando con letra/guión
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", nombre):
        log_error(
            "SQL injection attempt detected",
            {
                "error_id": ErrorIds.SQL_INVALID_IDENTIFIER,
                "identifier": nombre,
                "pattern_matched": False,
            },
        )
        raise ValueError(
            f"Identificador SQL inválido: '{nombre}'. "
            f"Solo se permiten letras, números y guión bajo. "
            f"Debe empezar con letra o guión bajo."
        )

    # Validar longitud (límite de MySQL y PostgreSQL)
    if len(nombre) > 64:
        raise ValueError(
            f"Identificador SQL muy largo (máx 64 caracteres): '{nombre}' ({len(nombre)} chars)"
        )


def validar_dataframe_no_vacio(df: Any) -> None:
    """
    Valida que el argumento sea un DataFrame no vacío.

    Args:
        df: Objeto a validar

    Raises:
        TypeError: Si no es pandas.DataFrame
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2, 3]})
        >>> validar_dataframe_no_vacio(df)  # OK
        >>>
        >>> validar_dataframe_no_vacio(pd.DataFrame())  # ValueError!
        >>> validar_dataframe_no_vacio([1, 2, 3])  # TypeError!
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Se esperaba pandas.DataFrame, recibido: {type(df).__name__}")

    if df.empty:
        log_error(
            "Empty DataFrame provided",
            {"error_id": ErrorIds.VALIDATION_EMPTY_DATAFRAME, "shape": df.shape},
        )
        raise ValueError("DataFrame no puede estar vacío")


def validar_columna_existe(df: pd.DataFrame, columna: str) -> None:
    """
    Valida que una columna exista en el DataFrame.

    Args:
        df: DataFrame a verificar
        columna: Nombre de la columna

    Raises:
        ValueError: Si la columna no existe

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2], "nombre": ["A", "B"]})
        >>> validar_columna_existe(df, "id")  # OK
        >>> validar_columna_existe(df, "edad")  # ValueError!
    """
    if columna not in df.columns:
        raise ValueError(
            f"Columna '{columna}' no existe en el DataFrame. "
            f"Columnas disponibles: {list(df.columns)}"
        )
