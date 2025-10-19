"""
Módulo de validación de archivos CSV.

Funciones para validar datos CSV según reglas de negocio,
tipos de datos y estructura esperada.
"""

import csv
import os
from typing import Dict, List, Type


def validar_headers(
    ruta_archivo: str,
    headers_esperados: List[str],
    delimitador: str = ","
) -> bool:
    """
    Valida que un archivo CSV tiene los headers esperados.

    Args:
        ruta_archivo: Ruta al archivo CSV
        headers_esperados: Lista de headers que debe tener el archivo
        delimitador: Delimitador usado en el CSV (por defecto: ',')

    Returns:
        True si los headers coinciden, False si no

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> validar_headers("datos.csv", ["nombre", "edad", "ciudad"])
        True
    """
    # Validar que el archivo existe
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")

    # Leer headers
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=delimitador)
        headers = next(lector)

    # Comparar
    return headers == headers_esperados


def validar_tipo_dato(valor: str, tipo_esperado: Type) -> bool:
    """
    Valida que un valor puede ser convertido al tipo esperado.

    Args:
        valor: Valor a validar (como string)
        tipo_esperado: Tipo de dato esperado (int, float, str)

    Returns:
        True si el valor puede ser convertido al tipo, False si no

    Examples:
        >>> validar_tipo_dato("25", int)
        True
        >>> validar_tipo_dato("abc", int)
        False
    """
    # String siempre es válido
    if tipo_esperado == str:
        return True

    # Intentar convertir
    try:
        if tipo_esperado == int:
            int(valor)
            return True
        elif tipo_esperado == float:
            float(valor)
            return True
        else:
            return False
    except (ValueError, TypeError):
        return False


def validar_fila(
    fila: Dict[str, str],
    validaciones: Dict[str, Type]
) -> List[str]:
    """
    Valida una fila del CSV según reglas de validación.

    Args:
        fila: Diccionario con los datos de la fila
        validaciones: Diccionario {columna: tipo_esperado}

    Returns:
        Lista de errores encontrados (vacía si todo está bien)

    Examples:
        >>> fila = {"nombre": "Ana", "edad": "25"}
        >>> validaciones = {"nombre": str, "edad": int}
        >>> validar_fila(fila, validaciones)
        []
    """
    errores = []

    for columna, tipo_esperado in validaciones.items():
        # Verificar que la columna existe
        if columna not in fila:
            errores.append(f"Columna '{columna}' falta en la fila")
            continue

        valor = fila[columna]

        # Verificar que no está vacío
        if not valor.strip():
            errores.append(f"Columna '{columna}' está vacío")
            continue

        # Verificar tipo
        if not validar_tipo_dato(valor, tipo_esperado):
            errores.append(
                f"Columna '{columna}' tiene tipo inválido "
                f"(esperado: {tipo_esperado.__name__}, valor: '{valor}')"
            )

    return errores
