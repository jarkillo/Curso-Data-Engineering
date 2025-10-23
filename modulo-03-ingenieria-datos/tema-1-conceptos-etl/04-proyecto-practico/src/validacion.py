"""
Módulo de validación de datos.

Este módulo contiene funciones para validar la calidad y consistencia
de los datos antes de procesarlos en el pipeline ETL.
"""

from typing import Any


def validar_no_vacia(datos: list[dict], nombre: str) -> None:
    """
    Valida que una lista de datos no esté vacía.

    Args:
        datos: Lista de diccionarios a validar
        nombre: Nombre descriptivo de los datos (para el mensaje de error)

    Raises:
        ValueError: Si la lista está vacía

    Examples:
        >>> validar_no_vacia([{"id": 1}], "ventas")  # OK
        >>> validar_no_vacia([], "ventas")  # ValueError
    """
    if not datos:
        raise ValueError(f"La lista de {nombre} está vacía")


def validar_columnas_requeridas(datos: list[dict], columnas: list[str]) -> None:
    """
    Valida que todas las filas tengan las columnas requeridas.

    Args:
        datos: Lista de diccionarios a validar
        columnas: Lista de nombres de columnas requeridas

    Raises:
        ValueError: Si alguna fila no tiene todas las columnas requeridas

    Examples:
        >>> datos = [{"id": 1, "nombre": "A"}]
        >>> validar_columnas_requeridas(datos, ["id", "nombre"])  # OK
    """
    if not datos:
        return  # Lista vacía, ya se validó antes

    for i, fila in enumerate(datos):
        columnas_presentes = set(fila.keys())
        columnas_faltantes = set(columnas) - columnas_presentes

        if columnas_faltantes:
            raise ValueError(
                f"Fila {i}: Faltan columnas requeridas: {', '.join(columnas_faltantes)}"
            )


def validar_tipos_ventas(ventas: list[dict[str, Any]]) -> None:
    """
    Valida que los tipos de datos en ventas sean correctos.

    Args:
        ventas: Lista de diccionarios con ventas

    Raises:
        TypeError: Si algún campo no tiene el tipo correcto

    Examples:
        >>> venta = {"venta_id": 1, "cantidad": 2, "precio_unitario": 100.0}
        >>> validar_tipos_ventas([venta])  # OK
    """
    for i, venta in enumerate(ventas):
        # Validar venta_id es int
        if not isinstance(venta.get("venta_id"), int):
            raise TypeError(f"Fila {i}: venta_id debe ser int")

        # Validar cantidad es int
        if not isinstance(venta.get("cantidad"), int):
            raise TypeError(f"Fila {i}: cantidad debe ser int")

        # Validar precio_unitario es float o int
        if not isinstance(venta.get("precio_unitario"), (int, float)):
            raise TypeError(f"Fila {i}: precio_unitario debe ser float o int")


def validar_valores_positivos(ventas: list[dict[str, Any]]) -> None:
    """
    Valida que cantidad y precio_unitario sean valores positivos (> 0).

    Args:
        ventas: Lista de diccionarios con ventas

    Raises:
        ValueError: Si algún valor es <= 0

    Examples:
        >>> venta = {"cantidad": 2, "precio_unitario": 100.0}
        >>> validar_valores_positivos([venta])  # OK
    """
    for i, venta in enumerate(ventas):
        # Validar cantidad > 0
        if venta.get("cantidad", 0) <= 0:
            raise ValueError(f"Fila {i}: cantidad debe ser mayor que 0")

        # Validar precio_unitario > 0
        if venta.get("precio_unitario", 0) <= 0:
            raise ValueError(f"Fila {i}: precio_unitario debe ser mayor que 0")


def validar_datos(ventas: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    """
    Ejecuta todas las validaciones sobre ventas y retorna el resultado.

    Args:
        ventas: Lista de diccionarios con ventas

    Returns:
        Tupla (es_valido, lista_de_errores)
        - es_valido: True si todas las validaciones pasan, False si hay errores
        - lista_de_errores: Lista de mensajes de error (vacía si no hay errores)

    Examples:
        >>> venta = {
        ...     "venta_id": 1, "fecha": "2025-10-01",
        ...     "producto_id": 101, "cliente_id": 1001,
        ...     "cantidad": 2, "precio_unitario": 100.0
        ... }
        >>> es_valido, errores = validar_datos([venta])
        >>> es_valido
        True
    """
    errores = []

    # Validación 1: No vacía
    try:
        validar_no_vacia(ventas, "ventas")
    except ValueError as e:
        errores.append(str(e))
        return False, errores  # Si está vacía, no tiene sentido seguir validando

    # Validación 2: Columnas requeridas
    columnas_requeridas = [
        "venta_id",
        "fecha",
        "producto_id",
        "cliente_id",
        "cantidad",
        "precio_unitario",
    ]
    try:
        validar_columnas_requeridas(ventas, columnas_requeridas)
    except ValueError as e:
        errores.append(str(e))

    # Validación 3: Tipos correctos
    try:
        validar_tipos_ventas(ventas)
    except TypeError as e:
        errores.append(str(e))

    # Validación 4: Valores positivos
    try:
        validar_valores_positivos(ventas)
    except ValueError as e:
        errores.append(str(e))

    es_valido = len(errores) == 0
    return es_valido, errores
