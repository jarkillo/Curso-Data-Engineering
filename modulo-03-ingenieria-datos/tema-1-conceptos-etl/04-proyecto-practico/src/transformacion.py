"""
Módulo de transformación de datos.

Este módulo contiene funciones para transformar y enriquecer los datos
extraídos antes de cargarlos en el destino.
"""

from typing import Any


def calcular_total_venta(venta: dict[str, Any]) -> dict[str, Any]:
    """
    Calcula el total de una venta (cantidad * precio_unitario).

    Args:
        venta: Diccionario con datos de la venta

    Returns:
        Nuevo diccionario con el campo 'total' añadido

    Examples:
        >>> venta = {"cantidad": 2, "precio_unitario": 100.0}
        >>> resultado = calcular_total_venta(venta)
        >>> resultado["total"]
        200.0
    """
    venta_con_total = venta.copy()
    total = venta["cantidad"] * venta["precio_unitario"]
    venta_con_total["total"] = round(total, 2)
    return venta_con_total


def enriquecer_venta_con_producto(
    venta: dict[str, Any], productos: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Enriquece una venta con información del producto.

    Añade los campos 'nombre_producto' y 'categoria' a la venta.

    Args:
        venta: Diccionario con datos de la venta
        productos: Lista de diccionarios con información de productos

    Returns:
        Nuevo diccionario con información del producto añadida

    Raises:
        ValueError: Si el producto no se encuentra en la lista

    Examples:
        >>> venta = {"producto_id": 101}
        >>> productos = [{"producto_id": 101, "nombre": "Laptop", "categoria": "Compu"}]
        >>> resultado = enriquecer_venta_con_producto(venta, productos)
        >>> resultado["nombre_producto"]
        'Laptop'
    """
    venta_enriquecida = venta.copy()
    producto_id = venta["producto_id"]

    # Buscar el producto
    producto = next((p for p in productos if p["producto_id"] == producto_id), None)

    if producto is None:
        raise ValueError(f"Producto {producto_id} no encontrado")

    venta_enriquecida["nombre_producto"] = producto["nombre"]
    venta_enriquecida["categoria"] = producto["categoria"]

    return venta_enriquecida


def enriquecer_venta_con_cliente(
    venta: dict[str, Any], clientes: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Enriquece una venta con información del cliente.

    Añade los campos 'nombre_cliente' y 'ciudad' a la venta.

    Args:
        venta: Diccionario con datos de la venta
        clientes: Lista de diccionarios con información de clientes

    Returns:
        Nuevo diccionario con información del cliente añadida

    Raises:
        ValueError: Si el cliente no se encuentra en la lista

    Examples:
        >>> venta = {"cliente_id": 1001}
        >>> clientes = [{"cliente_id": 1001, "nombre": "Juan", "ciudad": "Madrid"}]
        >>> resultado = enriquecer_venta_con_cliente(venta, clientes)
        >>> resultado["nombre_cliente"]
        'Juan'
    """
    venta_enriquecida = venta.copy()
    cliente_id = venta["cliente_id"]

    # Buscar el cliente
    cliente = next((c for c in clientes if c["cliente_id"] == cliente_id), None)

    if cliente is None:
        raise ValueError(f"Cliente {cliente_id} no encontrado")

    venta_enriquecida["nombre_cliente"] = cliente["nombre"]
    venta_enriquecida["ciudad"] = cliente["ciudad"]

    return venta_enriquecida


def transformar_ventas(
    ventas: list[dict[str, Any]],
    productos: list[dict[str, Any]],
    clientes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Transforma una lista de ventas aplicando todas las transformaciones.

    Aplica:
    1. Calcular total
    2. Enriquecer con información de producto
    3. Enriquecer con información de cliente

    Args:
        ventas: Lista de diccionarios con ventas
        productos: Lista de diccionarios con productos
        clientes: Lista de diccionarios con clientes

    Returns:
        Lista de ventas transformadas

    Examples:
        >>> ventas = [{"venta_id": 1, "producto_id": 101, "cliente_id": 1001,
        ...            "cantidad": 2, "precio_unitario": 100.0}]
        >>> productos = [{"producto_id": 101, "nombre": "Laptop", "categoria": "Compu"}]
        >>> clientes = [{"cliente_id": 1001, "nombre": "Juan", "ciudad": "Madrid"}]
        >>> resultado = transformar_ventas(ventas, productos, clientes)
        >>> resultado[0]["total"]
        200.0
    """
    if not ventas:
        return []

    ventas_transformadas = []

    for venta in ventas:
        # Paso 1: Calcular total
        venta_con_total = calcular_total_venta(venta)

        # Paso 2: Enriquecer con producto
        venta_con_producto = enriquecer_venta_con_producto(venta_con_total, productos)

        # Paso 3: Enriquecer con cliente
        venta_completa = enriquecer_venta_con_cliente(venta_con_producto, clientes)

        ventas_transformadas.append(venta_completa)

    return ventas_transformadas
