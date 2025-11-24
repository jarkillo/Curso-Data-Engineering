"""
Módulo de extracción de datos desde archivos CSV.

Este módulo contiene funciones para leer y extraer datos de archivos CSV,
validando que los archivos existan y contengan datos válidos.
"""

import csv
from pathlib import Path
from typing import Any


def leer_csv(ruta: str) -> list[dict[str, str]]:
    """
    Lee un archivo CSV y retorna una lista de diccionarios.

    Args:
        ruta: Ruta al archivo CSV

    Returns:
        Lista de diccionarios donde cada diccionario representa una fila

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está vacío (solo header)
        TypeError: Si ruta es None

    Examples:
        >>> datos = leer_csv("datos/ventas.csv")
        >>> len(datos) > 0
        True
    """
    if ruta is None:
        raise TypeError("La ruta no puede ser None")

    ruta_path = Path(ruta)
    if not ruta_path.exists():
        raise FileNotFoundError(f"El archivo {ruta} no existe")

    with open(ruta, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        datos = list(lector)

    if len(datos) == 0:
        raise ValueError(f"El archivo {ruta} está vacío")

    return datos


def extraer_ventas(ruta: str) -> list[dict[str, Any]]:
    """
    Extrae ventas desde un archivo CSV y convierte los tipos de datos.

    Args:
        ruta: Ruta al archivo CSV de ventas

    Returns:
        Lista de diccionarios con ventas, con tipos de datos correctos

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si faltan columnas requeridas

    Examples:
        >>> ventas = extraer_ventas("datos/ventas.csv")
        >>> ventas[0]["venta_id"]  # Es int, no str
        1
    """
    datos = leer_csv(ruta)

    columnas_requeridas = [
        "venta_id",
        "fecha",
        "producto_id",
        "cliente_id",
        "cantidad",
        "precio_unitario",
    ]

    # Validar columnas requeridas
    if datos:
        columnas_presentes = set(datos[0].keys())
        columnas_faltantes = set(columnas_requeridas) - columnas_presentes
        if columnas_faltantes:
            raise ValueError(
                f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}"
            )

    # Convertir tipos de datos
    ventas_convertidas = []
    for venta in datos:
        venta_convertida = {
            "venta_id": int(venta["venta_id"]),
            "fecha": venta["fecha"],
            "producto_id": int(venta["producto_id"]),
            "cliente_id": int(venta["cliente_id"]),
            "cantidad": int(venta["cantidad"]),
            "precio_unitario": float(venta["precio_unitario"]),
        }
        ventas_convertidas.append(venta_convertida)

    return ventas_convertidas


def extraer_productos(ruta: str) -> list[dict[str, Any]]:
    """
    Extrae productos desde un archivo CSV y convierte los tipos de datos.

    Args:
        ruta: Ruta al archivo CSV de productos

    Returns:
        Lista de diccionarios con productos, con tipos de datos correctos

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> productos = extraer_productos("datos/productos.csv")
        >>> productos[0]["producto_id"]
        101
    """
    datos = leer_csv(ruta)

    productos_convertidos = []
    for producto in datos:
        producto_convertido = {
            "producto_id": int(producto["producto_id"]),
            "nombre": producto["nombre"],
            "categoria": producto["categoria"],
            "stock": int(producto["stock"]),
        }
        productos_convertidos.append(producto_convertido)

    return productos_convertidos


def extraer_clientes(ruta: str) -> list[dict[str, Any]]:
    """
    Extrae clientes desde un archivo CSV y convierte los tipos de datos.

    Args:
        ruta: Ruta al archivo CSV de clientes

    Returns:
        Lista de diccionarios con clientes, con tipos de datos correctos

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> clientes = extraer_clientes("datos/clientes.csv")
        >>> clientes[0]["cliente_id"]
        1001
    """
    datos = leer_csv(ruta)

    clientes_convertidos = []
    for cliente in datos:
        cliente_convertido = {
            "cliente_id": int(cliente["cliente_id"]),
            "nombre": cliente["nombre"],
            "email": cliente["email"],
            "ciudad": cliente["ciudad"],
        }
        clientes_convertidos.append(cliente_convertido)

    return clientes_convertidos
