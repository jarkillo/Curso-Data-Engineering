"""
Generador de Fact Table FactVentas para Data Warehouse.

Este módulo genera datos sintéticos para la tabla de hechos de ventas,
conectando todas las dimensiones del Star Schema.
"""

import random

import pandas as pd


def generar_fact_ventas(
    num_ventas: int,
    dim_fecha: pd.DataFrame,
    dim_producto: pd.DataFrame,
    dim_cliente: pd.DataFrame,
    dim_vendedor: pd.DataFrame,
) -> pd.DataFrame:
    """
    Genera datos sintéticos para la tabla de hechos FactVentas.

    Crea transacciones de ventas conectando todas las dimensiones del Star Schema
    con métricas de negocio (cantidad, precio, descuento, impuesto).

    Args:
        num_ventas: Número de transacciones de ventas a generar (debe ser > 0)
        dim_fecha: DataFrame con dimensión de fechas (debe tener 'fecha_id')
        dim_producto: DataFrame con dimensión de productos
            (debe tener 'producto_id', 'precio_catalogo')
        dim_cliente: DataFrame con dimensión de clientes (debe tener 'cliente_id')
        dim_vendedor: DataFrame con dimensión de vendedores (debe tener 'vendedor_id')

    Returns:
        DataFrame con columnas:
        - venta_id (int): ID único de la venta (PK)
        - fecha_id (int): FK a DimFecha
        - producto_id (int): FK a DimProducto
        - cliente_id (int): FK a DimCliente
        - vendedor_id (int): FK a DimVendedor
        - cantidad (int): Unidades vendidas (1-10)
        - precio_unitario (float): Precio por unidad (con variación ±20% sobre catálogo)
        - monto_bruto (float): Subtotal antes de descuentos (cantidad * precio_unitario)
        - descuento (float): Monto de descuento aplicado (0-40% del subtotal)
        - impuesto (float): Impuesto aplicado (16% del subtotal después de descuento)
        - monto_neto (float): Monto final (subtotal - descuento + impuesto)

    Raises:
        ValueError: Si num_ventas <= 0 o si alguna dimensión está vacía

    Examples:
        >>> dim_fecha = generar_dim_fecha("2024-01-01", "2024-12-31")
        >>> dim_producto = generar_dim_producto(100)
        >>> dim_cliente = generar_dim_cliente(200)
        >>> dim_vendedor = generar_dim_vendedor(50)
        >>> fact_ventas = generar_fact_ventas(
        ...     1000, dim_fecha, dim_producto, dim_cliente, dim_vendedor
        ... )
        >>> fact_ventas.shape
        (1000, 11)
        >>> fact_ventas['venta_id'].is_unique
        True
    """
    # Validaciones de entrada
    if num_ventas <= 0:
        raise ValueError("num_ventas debe ser positivo")

    if (
        len(dim_fecha) == 0
        or len(dim_producto) == 0
        or len(dim_cliente) == 0
        or len(dim_vendedor) == 0
    ):
        raise ValueError("Dimensiones no pueden estar vacías")

    # Verificar columnas requeridas
    if "fecha_id" not in dim_fecha.columns:
        raise ValueError("dim_fecha debe tener columna 'fecha_id'")
    if (
        "producto_id" not in dim_producto.columns
        or "precio_catalogo" not in dim_producto.columns
    ):
        raise ValueError(
            "dim_producto debe tener columnas 'producto_id' y 'precio_catalogo'"
        )
    if "cliente_id" not in dim_cliente.columns:
        raise ValueError("dim_cliente debe tener columna 'cliente_id'")
    if "vendedor_id" not in dim_vendedor.columns:
        raise ValueError("dim_vendedor debe tener columna 'vendedor_id'")

    # Configurar seed para reproducibilidad en contexto educativo
    random.seed(42)

    ventas = []

    for i in range(1, num_ventas + 1):
        # Seleccionar dimensiones aleatoriamente
        fecha_id = random.choice(dim_fecha["fecha_id"].tolist())
        producto_row = dim_producto.sample(n=1).iloc[0]
        producto_id = producto_row["producto_id"]
        precio_catalogo = producto_row["precio_catalogo"]
        cliente_id = random.choice(dim_cliente["cliente_id"].tolist())
        vendedor_id = random.choice(dim_vendedor["vendedor_id"].tolist())

        # Generar métricas de negocio
        cantidad = random.randint(1, 10)  # 1-10 unidades

        # Precio unitario con variación ±20% sobre precio catálogo
        variacion = random.uniform(0.8, 1.2)
        precio_unitario = round(precio_catalogo * variacion, 2)

        # Calcular subtotal
        subtotal = cantidad * precio_unitario

        # Descuento: 0-40% del subtotal
        porcentaje_descuento = random.uniform(0, 0.40)
        descuento = round(subtotal * porcentaje_descuento, 2)

        # Impuesto: 16% sobre (subtotal - descuento)
        base_imponible = subtotal - descuento
        impuesto = round(base_imponible * 0.16, 2)

        # Monto neto final
        monto_neto = round(subtotal - descuento + impuesto, 2)

        # Monto bruto (subtotal antes de descuentos)
        monto_bruto = round(subtotal, 2)

        venta = {
            "venta_id": i,
            "fecha_id": fecha_id,
            "producto_id": producto_id,
            "cliente_id": cliente_id,
            "vendedor_id": vendedor_id,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "monto_bruto": monto_bruto,
            "descuento": descuento,
            "impuesto": impuesto,
            "monto_neto": monto_neto,
        }

        ventas.append(venta)

    # Crear DataFrame
    df = pd.DataFrame(ventas)

    # Asegurar tipos de datos correctos
    df["venta_id"] = df["venta_id"].astype(int)
    df["fecha_id"] = df["fecha_id"].astype(int)
    df["producto_id"] = df["producto_id"].astype(int)
    df["cliente_id"] = df["cliente_id"].astype(int)
    df["vendedor_id"] = df["vendedor_id"].astype(int)
    df["cantidad"] = df["cantidad"].astype(int)
    df["precio_unitario"] = df["precio_unitario"].astype(float)
    df["descuento"] = df["descuento"].astype(float)
    df["impuesto"] = df["impuesto"].astype(float)
    df["monto_bruto"] = df["monto_bruto"].astype(float)
    df["monto_neto"] = df["monto_neto"].astype(float)

    return df
