"""
Módulo de validaciones para consultas SQL.

Este módulo contiene funciones puras de validación de inputs
que se utilizan en las funciones de consultas.
"""

from pathlib import Path


def validar_precio_positivo(precio: float) -> None:
    """
    Valida que el precio sea un número positivo mayor a cero.

    Args:
        precio: Precio a validar

    Raises:
        TypeError: Si precio no es un número (int o float)
        ValueError: Si precio es menor o igual a cero

    Examples:
        >>> validar_precio_positivo(100.0)
        >>> validar_precio_positivo(0.01)
        >>> validar_precio_positivo(0.0)
        Traceback (most recent call last):
        ...
        ValueError: El precio debe ser mayor a cero
    """
    if not isinstance(precio, (int, float)):
        raise TypeError("El precio debe ser un número (int o float)")

    if precio <= 0:
        raise ValueError("El precio debe ser mayor a cero")


def validar_categoria_no_vacia(categoria: str) -> None:
    """
    Valida que la categoría sea un string no vacío.

    Args:
        categoria: Nombre de la categoría

    Raises:
        TypeError: Si categoría no es un string
        ValueError: Si categoría está vacía o es solo espacios

    Examples:
        >>> validar_categoria_no_vacia("Accesorios")
        >>> validar_categoria_no_vacia("")
        Traceback (most recent call last):
        ...
        ValueError: La categoría no puede estar vacía
    """
    if not isinstance(categoria, str):
        raise TypeError("La categoría debe ser un string")

    if not categoria.strip():
        raise ValueError("La categoría no puede estar vacía")


def validar_numero_positivo(numero: int, nombre_parametro: str) -> None:
    """
    Valida que un número sea un entero positivo mayor a cero.

    Args:
        numero: Número a validar
        nombre_parametro: Nombre del parámetro (para mensaje de error)

    Raises:
        TypeError: Si numero no es un entero
        ValueError: Si numero es menor o igual a cero

    Examples:
        >>> validar_numero_positivo(5, "n")
        >>> validar_numero_positivo(0, "n")
        Traceback (most recent call last):
        ...
        ValueError: El parámetro 'n' debe ser mayor a cero
    """
    if not isinstance(numero, int):
        raise TypeError(f"El parámetro '{nombre_parametro}' debe ser un entero")

    if numero <= 0:
        raise ValueError(f"El parámetro '{nombre_parametro}' debe ser mayor a cero")


def validar_ruta_db_existe(ruta: str) -> None:
    """
    Valida que la ruta de la base de datos exista.

    Args:
        ruta: Ruta al archivo de base de datos

    Raises:
        TypeError: Si ruta no es un string
        ValueError: Si ruta está vacía
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> validar_ruta_db_existe("base.db")
        Traceback (most recent call last):
        ...
        FileNotFoundError: El archivo de base de datos 'base.db' no existe
    """
    if not isinstance(ruta, str):
        raise TypeError("La ruta debe ser un string")

    if not ruta.strip():
        raise ValueError("La ruta no puede estar vacía")

    # Permitir :memory: para bases de datos en memoria
    if ruta == ":memory:":
        return

    ruta_path = Path(ruta)
    if not ruta_path.exists():
        raise FileNotFoundError(f"El archivo de base de datos '{ruta}' no existe")
