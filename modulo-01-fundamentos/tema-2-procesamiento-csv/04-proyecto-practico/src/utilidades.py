"""
Módulo de utilidades para procesamiento de archivos CSV.

Funciones auxiliares reutilizables para operaciones comunes con CSV.
"""

import csv
import os
from typing import List


def contar_filas(ruta_archivo: str) -> int:
    """
    Cuenta el número de filas de datos en un archivo CSV (sin contar el header).

    Args:
        ruta_archivo: Ruta al archivo CSV

    Returns:
        Número de filas de datos (sin header)

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está vacío

    Examples:
        >>> contar_filas("datos.csv")
        10
    """
    # Validar que el archivo existe
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")

    # Validar que no está vacío
    if os.path.getsize(ruta_archivo) == 0:
        raise ValueError(f"El archivo está vacío: {ruta_archivo}")

    # Contar filas
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar header
        return sum(1 for _ in lector)


def obtener_headers(ruta_archivo: str, delimitador: str = ",") -> List[str]:
    """
    Obtiene la lista de headers (nombres de columnas) de un archivo CSV.

    Args:
        ruta_archivo: Ruta al archivo CSV
        delimitador: Delimitador usado en el CSV (por defecto: ',')

    Returns:
        Lista con los nombres de las columnas

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está vacío

    Examples:
        >>> obtener_headers("datos.csv")
        ['nombre', 'edad', 'ciudad']
    """
    # Validar que el archivo existe
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")

    # Validar que no está vacío
    if os.path.getsize(ruta_archivo) == 0:
        raise ValueError(f"El archivo está vacío: {ruta_archivo}")

    # Leer headers
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=delimitador)
        headers = next(lector)
        return headers
