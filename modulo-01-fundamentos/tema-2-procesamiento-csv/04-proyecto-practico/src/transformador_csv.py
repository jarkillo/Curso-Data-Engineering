"""
Módulo de transformación de archivos CSV.

Funciones para transformar, filtrar y consolidar datos CSV.
"""

import csv
from typing import Callable, Dict, List

from src.lector_csv import leer_csv
from src.escritor_csv import escribir_csv


def filtrar_filas(
    datos: List[Dict[str, str]],
    condicion: Callable[[Dict[str, str]], bool]
) -> List[Dict[str, str]]:
    """
    Filtra filas de datos según una condición.

    Args:
        datos: Lista de diccionarios con los datos
        condicion: Función que retorna True si la fila debe incluirse

    Returns:
        Nueva lista con solo las filas que cumplen la condición

    Examples:
        >>> datos = [{"nombre": "Ana", "edad": "25"}, {"nombre": "Luis", "edad": "30"}]
        >>> filtrar_filas(datos, lambda fila: int(fila["edad"]) > 25)
        [{"nombre": "Luis", "edad": "30"}]
    """
    return [fila for fila in datos if condicion(fila)]


def agregar_columna(
    datos: List[Dict[str, str]],
    nombre_columna: str,
    funcion_calculo: Callable[[Dict[str, str]], str]
) -> List[Dict[str, str]]:
    """
    Agrega una nueva columna calculada a los datos.

    Esta función NO modifica la lista original (función pura).

    Args:
        datos: Lista de diccionarios con los datos
        nombre_columna: Nombre de la nueva columna
        funcion_calculo: Función que calcula el valor de la nueva
                         columna

    Returns:
        Nueva lista con la columna adicional

    Examples:
        >>> datos = [{"precio": "10", "cantidad": "2"}]
        >>> agregar_columna(
        ...     datos, "total",
        ...     lambda f: str(float(f["precio"]) * int(f["cantidad"]))
        ... )
        [{"precio": "10", "cantidad": "2", "total": "20.0"}]
    """
    # Crear nueva lista (no modificar la original)
    resultado = []

    for fila in datos:
        # Crear copia de la fila
        nueva_fila = fila.copy()

        # Calcular y agregar nueva columna
        nueva_fila[nombre_columna] = funcion_calculo(fila)

        resultado.append(nueva_fila)

    return resultado


def consolidar_csvs(
    archivos: List[str],
    archivo_salida: str,
    delimitador: str = ",",
    encoding: str = "utf-8"
) -> None:
    """
    Consolida múltiples archivos CSV en uno solo.

    Todos los archivos deben tener los mismos headers.

    Args:
        archivos: Lista de rutas a los archivos CSV a consolidar
        archivo_salida: Ruta donde guardar el archivo consolidado
        delimitador: Delimitador usado en los CSV (por defecto: ',')
        encoding: Codificación de los archivos (por defecto: 'utf-8')

    Raises:
        ValueError: Si la lista de archivos está vacía o si los headers no coinciden
        FileNotFoundError: Si algún archivo no existe

    Examples:
        >>> consolidar_csvs(["ventas_a.csv", "ventas_b.csv"], "consolidado.csv")
    """
    # Validar que hay al menos un archivo
    if not archivos:
        raise ValueError("Debe proporcionar al menos un archivo para consolidar")

    # Leer primer archivo para obtener headers
    primer_archivo = archivos[0]
    datos_consolidados = leer_csv(
        primer_archivo, delimitador=delimitador, encoding=encoding
    )

    # Leer headers del primer archivo
    with open(primer_archivo, "r", encoding=encoding) as f:
        lector = csv.reader(f, delimiter=delimitador)
        headers_esperados = next(lector)

    # Leer resto de archivos
    for archivo in archivos[1:]:
        # Validar headers
        with open(archivo, "r", encoding=encoding) as f:
            lector = csv.reader(f, delimiter=delimitador)
            headers = next(lector)

            if headers != headers_esperados:
                raise ValueError(
                    f"El archivo {archivo} tiene headers diferentes. "
                    f"Esperado: {headers_esperados}, Encontrado: {headers}"
                )

        # Leer datos
        datos = leer_csv(archivo, delimitador=delimitador, encoding=encoding)
        datos_consolidados.extend(datos)

    # Escribir archivo consolidado
    escribir_csv(
        datos_consolidados,
        archivo_salida,
        headers=headers_esperados,
        delimitador=delimitador,
        encoding=encoding
    )
