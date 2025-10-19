"""
Módulo de lectura de archivos CSV.

Funciones para leer archivos CSV de forma robusta, con validación
y detección automática de delimitadores.
"""

import csv
import os
from typing import Dict, List


def validar_archivo_existe(ruta_archivo: str) -> None:
    """
    Valida que un archivo existe y no está vacío.

    Args:
        ruta_archivo: Ruta al archivo CSV

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está vacío

    Examples:
        >>> validar_archivo_existe("datos.csv")
        # No lanza error si el archivo existe y no está vacío
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")

    if os.path.getsize(ruta_archivo) == 0:
        raise ValueError(f"El archivo está vacío: {ruta_archivo}")


def detectar_delimitador(ruta_archivo: str) -> str:
    """
    Detecta automáticamente el delimitador usado en un archivo CSV.

    Args:
        ruta_archivo: Ruta al archivo CSV

    Returns:
        Delimitador detectado (',', ';', '\\t', etc.)

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> detectar_delimitador("datos.csv")
        ','
    """
    # Validar que el archivo existe
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo no existe: {ruta_archivo}")

    # Detectar delimitador
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        muestra = archivo.read(1024)
        sniffer = csv.Sniffer()
        delimitador = sniffer.sniff(muestra).delimiter
        return delimitador


def leer_csv(
    ruta_archivo: str,
    delimitador: str = ",",
    encoding: str = "utf-8"
) -> List[Dict[str, str]]:
    """
    Lee un archivo CSV y retorna una lista de diccionarios.

    Cada diccionario representa una fila, con las claves siendo los headers
    y los valores siendo los datos de esa fila.

    Args:
        ruta_archivo: Ruta al archivo CSV
        delimitador: Delimitador usado en el CSV (por defecto: ',')
        encoding: Codificación del archivo (por defecto: 'utf-8')

    Returns:
        Lista de diccionarios con los datos del CSV

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está vacío

    Examples:
        >>> leer_csv("datos.csv")
        [{'nombre': 'Ana', 'edad': '25'}, {'nombre': 'Luis', 'edad': '30'}]
    """
    # Validar archivo
    validar_archivo_existe(ruta_archivo)

    # Leer CSV
    datos = []
    with open(ruta_archivo, "r", encoding=encoding) as archivo:
        lector = csv.DictReader(archivo, delimiter=delimitador)

        for fila in lector:
            datos.append(fila)

    return datos
