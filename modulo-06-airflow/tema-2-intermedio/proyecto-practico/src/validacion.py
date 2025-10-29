"""
Módulo de validación de datos.

Este módulo proporciona funciones para validar schemas y datos de ventas y clientes,
asegurando la integridad de los datos antes del procesamiento.
"""

import pandas as pd


def validar_schema_ventas(df: pd.DataFrame) -> None:
    """
    Valida que el DataFrame de ventas tenga las columnas requeridas.

    Args:
        df: DataFrame de ventas a validar

    Raises:
        ValueError: Si faltan columnas requeridas

    Examples:
        >>> df = pd.DataFrame({
        ...     'producto': ['Laptop'],
        ...     'cantidad': [3],
        ...     'precio': [1200.0],
        ...     'cliente_id': ['C001']
        ... })
        >>> validar_schema_ventas(df)  # No lanza excepción
    """
    columnas_requeridas = ["producto", "cantidad", "precio", "cliente_id"]
    columnas_presentes = df.columns.tolist()

    columnas_faltantes = [
        col for col in columnas_requeridas if col not in columnas_presentes
    ]

    if columnas_faltantes:
        raise ValueError(f"Faltan columnas requeridas: {columnas_faltantes}")

    print("[VALIDAR_SCHEMA_VENTAS] Schema válido")


def validar_datos_ventas(df: pd.DataFrame) -> None:  # noqa: C901
    """
    Valida los datos del DataFrame de ventas.

    Verifica:
    - No hay valores nulos
    - cantidad es positiva
    - precio es positivo

    Args:
        df: DataFrame de ventas a validar

    Raises:
        ValueError: Si los datos no son válidos

    Examples:
        >>> df = pd.DataFrame({
        ...     'producto': ['Laptop'],
        ...     'cantidad': [3],
        ...     'precio': [1200.0],
        ...     'cliente_id': ['C001']
        ... })
        >>> validar_datos_ventas(df)  # No lanza excepción
    """
    # Validar valores nulos
    if df.isnull().any().any():
        columnas_con_nulos = df.columns[df.isnull().any()].tolist()
        raise ValueError(
            f"El DataFrame contiene valores nulos en: {columnas_con_nulos}"
        )

    # Validar que cantidad sea positiva
    if "cantidad" in df.columns:
        if (df["cantidad"] < 0).any():
            raise ValueError("La columna 'cantidad' debe ser positivo")

    # Validar que precio sea positivo
    if "precio" in df.columns:
        if (df["precio"] < 0).any():
            raise ValueError("La columna 'precio' debe ser positivo")

    print(f"[VALIDAR_DATOS_VENTAS] Validados {len(df)} registros exitosamente")


def validar_schema_clientes(df: pd.DataFrame) -> None:
    """
    Valida que el DataFrame de clientes tenga las columnas requeridas.

    Args:
        df: DataFrame de clientes a validar

    Raises:
        ValueError: Si faltan columnas requeridas

    Examples:
        >>> df = pd.DataFrame({
        ...     'cliente_id': ['C001'],
        ...     'nombre': ['Alice'],
        ...     'nivel': ['premium']
        ... })
        >>> validar_schema_clientes(df)  # No lanza excepción
    """
    columnas_requeridas = ["cliente_id", "nombre", "nivel"]
    columnas_presentes = df.columns.tolist()

    columnas_faltantes = [
        col for col in columnas_requeridas if col not in columnas_presentes
    ]

    if columnas_faltantes:
        raise ValueError(f"Faltan columnas requeridas: {columnas_faltantes}")

    print("[VALIDAR_SCHEMA_CLIENTES] Schema válido")


def validar_datos_clientes(df: pd.DataFrame) -> None:
    """
    Valida los datos del DataFrame de clientes.

    Verifica:
    - nivel está en la lista de valores permitidos

    Args:
        df: DataFrame de clientes a validar

    Raises:
        ValueError: Si los datos no son válidos

    Examples:
        >>> df = pd.DataFrame({
        ...     'cliente_id': ['C001'],
        ...     'nombre': ['Alice'],
        ...     'nivel': ['premium']
        ... })
        >>> validar_datos_clientes(df)  # No lanza excepción
    """
    niveles_validos = ["premium", "normal", "vip"]

    if "nivel" in df.columns:
        niveles_invalidos = df[~df["nivel"].isin(niveles_validos)]["nivel"].unique()
        if len(niveles_invalidos) > 0:
            invalidos_str = niveles_invalidos.tolist()
            raise ValueError(
                f"La columna 'nivel' contiene valores inválidos: {invalidos_str}. "
                f"Los valores válidos son: {niveles_validos}. "
                f"El nivel debe ser uno de: {', '.join(niveles_validos)}"
            )

    print(f"[VALIDAR_DATOS_CLIENTES] Validados {len(df)} registros exitosamente")
