"""
Módulo de validación de datos

Funciones para validar la integridad de los datos de ventas.

Reglas de negocio:
- Todas las columnas requeridas deben estar presentes
- Cantidades deben ser positivas
- Precios deben ser positivos
- No debe haber valores nulos en columnas críticas
"""

from typing import Dict

import pandas as pd

COLUMNAS_REQUERIDAS = [
    "venta_id",
    "fecha",
    "cliente_id",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "total",
]


def verificar_columnas_requeridas(df: pd.DataFrame) -> bool:
    """
    Verifica que todas las columnas requeridas estén presentes.

    Args:
        df: DataFrame de ventas

    Returns:
        bool: True si todas las columnas están presentes

    Raises:
        ValueError: Si falta alguna columna requerida

    Examples:
        >>> df = pd.DataFrame({"venta_id": [1], "fecha": ["2025-10-25"], ...})
        >>> verificar_columnas_requeridas(df)
        True
    """
    columnas_faltantes = []

    for columna in COLUMNAS_REQUERIDAS:
        if columna not in df.columns:
            columnas_faltantes.append(columna)

    if columnas_faltantes:
        raise ValueError(
            f"Faltan las siguientes columnas requeridas: {columnas_faltantes}. "
            f"Columnas presentes: {list(df.columns)}"
        )

    return True


def verificar_tipos_datos(df: pd.DataFrame) -> bool:
    """
    Verifica que los tipos de datos sean correctos y valores válidos.

    Args:
        df: DataFrame de ventas

    Returns:
        bool: True si todos los tipos y valores son válidos

    Raises:
        ValueError: Si hay valores inválidos

    Examples:
        >>> df = pd.DataFrame({
        ...     "cantidad": [1, 2, 3],
        ...     "precio_unitario": [10.0, 20.0, 30.0]
        ... })
        >>> verificar_tipos_datos(df)
        True
    """
    # Verificar que cantidad sea positiva
    if "cantidad" in df.columns:
        cantidades_invalidas = df[df["cantidad"] <= 0]
        if not cantidades_invalidas.empty:
            raise ValueError(
                f"Se encontraron {len(cantidades_invalidas)} registros con "
                f"cantidad negativa o cero. Todas las cantidades deben ser "
                f"mayores a 0."
            )

    # Verificar que precio_unitario sea positivo
    if "precio_unitario" in df.columns:
        precios_invalidos = df[df["precio_unitario"] <= 0]
        if not precios_invalidos.empty:
            raise ValueError(
                f"Se encontraron {len(precios_invalidos)} registros con "
                f"precio_unitario negativo o cero. Todos los precios deben "
                f"ser mayores a 0."
            )

    # Verificar que total sea positivo
    if "total" in df.columns:
        totales_invalidos = df[df["total"] <= 0]
        if not totales_invalidos.empty:
            raise ValueError(
                f"Se encontraron {len(totales_invalidos)} registros con "
                f"total negativo o cero."
            )

    return True


def validar_datos_ventas(df: pd.DataFrame) -> Dict:  # noqa: C901
    """
    Ejecuta todas las validaciones sobre el DataFrame de ventas.

    Args:
        df: DataFrame de ventas

    Returns:
        dict: Resultado de la validación con estructura:
            {
                "valido": bool,
                "errores": list,
                "advertencias": list
            }

    Examples:
        >>> df = pd.DataFrame({...})  # DataFrame válido
        >>> resultado = validar_datos_ventas(df)
        >>> resultado["valido"]
        True
    """
    errores = []
    advertencias = []

    # Validación 1: Verificar columnas requeridas
    try:
        verificar_columnas_requeridas(df)
    except ValueError as e:
        errores.append(str(e))

    # Validación 2: Verificar tipos de datos
    try:
        verificar_tipos_datos(df)
    except ValueError as e:
        errores.append(str(e))

    # Validación 3: Verificar valores nulos en columnas críticas
    columnas_criticas = ["venta_id", "fecha", "producto", "total"]
    for columna in columnas_criticas:
        if columna in df.columns:
            nulos = df[columna].isnull().sum()
            if nulos > 0:
                errores.append(
                    f"La columna '{columna}' tiene {nulos} valores nulos. "
                    f"Esta columna no puede tener valores nulos."
                )

    # Validación 4: Advertencias (no bloquean el pipeline)
    if len(df) < 5:
        advertencias.append(
            f"El dataset tiene solo {len(df)} registros. " f"¿Es esto esperado?"
        )

    # Construir resultado
    resultado = {
        "valido": len(errores) == 0,
        "errores": errores,
        "advertencias": advertencias,
        "total_registros": len(df),
    }

    if resultado["valido"]:
        print(f"✅ Validación exitosa: {len(df)} registros válidos")
    else:
        print(f"❌ Validación fallida: {len(errores)} errores encontrados")
        for error in errores:
            print(f"  - {error}")

    if advertencias:
        print(f"⚠️  {len(advertencias)} advertencias:")
        for advertencia in advertencias:
            print(f"  - {advertencia}")

    return resultado
