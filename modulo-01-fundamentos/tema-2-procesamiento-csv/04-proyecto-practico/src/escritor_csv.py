"""
Módulo de escritura de archivos CSV.

Funciones para escribir datos en archivos CSV de forma robusta,
con soporte para diferentes delimitadores y encodings.
"""

import csv
from typing import Dict, List, Optional


def escribir_csv(
    datos: List[Dict[str, str]],
    ruta_archivo: str,
    headers: Optional[List[str]] = None,
    delimitador: str = ",",
    encoding: str = "utf-8"
) -> None:
    """
    Escribe una lista de diccionarios en un archivo CSV.

    Args:
        datos: Lista de diccionarios con los datos a escribir
        ruta_archivo: Ruta donde guardar el archivo CSV
        headers: Lista de headers (opcional, se infiere de los datos si no
                 se proporciona)
        delimitador: Delimitador a usar (por defecto: ',')
        encoding: Codificación del archivo (por defecto: 'utf-8')

    Raises:
        ValueError: Si datos está vacío y no se proporcionan headers

    Examples:
        >>> datos = [{"nombre": "Ana", "edad": "25"}]
        >>> escribir_csv(datos, "salida.csv")
    """
    # Validar que si datos está vacío, se proporcionan headers
    if not datos and not headers:
        raise ValueError(
            "Si la lista de datos está vacía, debe proporcionar los "
            "headers explícitamente"
        )

    # Inferir headers de los datos si no se proporcionan
    if not headers:
        headers = list(datos[0].keys())

    # Escribir CSV
    with open(ruta_archivo, "w", encoding=encoding, newline="") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=headers,
            delimiter=delimitador
        )

        escritor.writeheader()
        escritor.writerows(datos)
