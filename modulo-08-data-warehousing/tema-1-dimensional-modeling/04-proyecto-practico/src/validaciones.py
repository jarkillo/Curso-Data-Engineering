"""
Módulo de validaciones para garantizar calidad de datos en Data Warehouse.

Este módulo provee funciones reutilizables para validar datos antes de cargarlos
al Data Warehouse, asegurando integridad y calidad.

Funciones:
    validar_no_nulos: Verifica que campos obligatorios no tengan valores nulos
    validar_rangos: Valida que valores numéricos estén en rangos esperados
    validar_tipos: Verifica que campos tengan los tipos de datos correctos
    validar_integridad_referencial: Valida que claves foráneas existan
    validar_unicidad: Verifica que campos únicos no tengan duplicados
"""

from typing import Optional

import pandas as pd


def validar_no_nulos(
    df: pd.DataFrame, campos_obligatorios: list[str]
) -> dict[str, bool | list[str]]:
    """
    Valida que campos obligatorios no contengan valores nulos.

    Args:
        df: DataFrame a validar
        campos_obligatorios: Lista de nombres de campos que no pueden ser nulos

    Returns:
        Diccionario con:
            - is_valid (bool): True si todos los campos obligatorios están completos
            - errors (list[str]): Lista de mensajes de error (vacía si is_valid=True)

    Examples:
        >>> df = pd.DataFrame([
        ...     {"id": 1, "nombre": "Juan"},
        ...     {"id": 2, "nombre": "María"}
        ... ])
        >>> resultado = validar_no_nulos(df, ["id", "nombre"])
        >>> resultado["is_valid"]
        True

        >>> df = pd.DataFrame([
        ...     {"id": 1, "nombre": None}
        ... ])
        >>> resultado = validar_no_nulos(df, ["id", "nombre"])
        >>> resultado["is_valid"]
        False
    """
    errors = []

    # DataFrame vacío es válido
    if df.empty:
        return {"is_valid": True, "errors": []}

    for campo in campos_obligatorios:
        if campo not in df.columns:
            errors.append(f"Campo '{campo}' no existe en DataFrame")
            continue

        nulos = df[campo].isna()
        num_nulos = nulos.sum()

        if num_nulos > 0:
            errors.append(
                f"Campo '{campo}' tiene {num_nulos} valores nulos "
                f"(filas: {nulos[nulos].index.tolist()})"
            )

    return {"is_valid": len(errors) == 0, "errors": errors}


def validar_rangos(
    df: pd.DataFrame, rangos: dict[str, Optional[tuple[float, float]]]
) -> dict[str, bool | list[str]]:
    """
    Valida que valores numéricos estén dentro de rangos permitidos.

    Args:
        df: DataFrame a validar
        rangos: Diccionario {campo: (min, max)} o {campo: None} para sin límite

    Returns:
        Diccionario con:
            - is_valid (bool): True si todos los valores están en rango
            - errors (list[str]): Lista de mensajes de error

    Examples:
        >>> df = pd.DataFrame([
        ...     {"edad": 25, "precio": 100.0},
        ...     {"edad": 30, "precio": 500.0}
        ... ])
        >>> rangos = {"edad": (18, 100), "precio": (0, 10000)}
        >>> resultado = validar_rangos(df, rangos)
        >>> resultado["is_valid"]
        True

        >>> df = pd.DataFrame([{"edad": 150, "precio": -10.0}])
        >>> resultado = validar_rangos(df, {"edad": (18, 100), "precio": (0, 10000)})
        >>> resultado["is_valid"]
        False
    """
    errors = []

    if df.empty:
        return {"is_valid": True, "errors": []}

    for campo, rango in rangos.items():
        if campo not in df.columns:
            errors.append(f"Campo '{campo}' no existe en DataFrame")
            continue

        # Si rango es None, no validar
        if rango is None:
            continue

        min_val, max_val = rango

        fuera_rango = (df[campo] < min_val) | (df[campo] > max_val)
        num_fuera = fuera_rango.sum()

        if num_fuera > 0:
            valores_incorrectos = df.loc[fuera_rango, campo].tolist()
            errors.append(
                f"Campo '{campo}' tiene {num_fuera} valores fuera de rango "
                f"[{min_val}, {max_val}]. Valores: {valores_incorrectos[:5]}"
            )

    return {"is_valid": len(errors) == 0, "errors": errors}


def validar_tipos(
    df: pd.DataFrame, tipos_esperados: dict[str, type]
) -> dict[str, bool | list[str]]:
    """
    Valida que campos tengan los tipos de datos esperados.

    Args:
        df: DataFrame a validar
        tipos_esperados: Diccionario {campo: tipo} ej: {"id": int, "nombre": str}

    Returns:
        Diccionario con:
            - is_valid (bool): True si todos los tipos son correctos
            - errors (list[str]): Lista de mensajes de error

    Examples:
        >>> df = pd.DataFrame([
        ...     {"id": 1, "nombre": "Juan", "precio": 100.5}
        ... ])
        >>> tipos = {"id": int, "nombre": str, "precio": float}
        >>> resultado = validar_tipos(df, tipos)
        >>> resultado["is_valid"]
        True

        >>> df = pd.DataFrame([
        ...     {"id": "1", "nombre": 123}
        ... ])
        >>> tipos = {"id": int, "nombre": str}
        >>> resultado = validar_tipos(df, tipos)
        >>> resultado["is_valid"]
        False
    """
    errors = []

    if df.empty:
        return {"is_valid": True, "errors": []}

    for campo, tipo_esperado in tipos_esperados.items():
        if campo not in df.columns:
            errors.append(f"Campo '{campo}' no existe en DataFrame")
            continue

        # Verificar tipo de cada valor
        tipos_incorrectos = ~df[campo].apply(
            lambda x, t=tipo_esperado: isinstance(x, t)
        )
        num_incorrectos = tipos_incorrectos.sum()

        if num_incorrectos > 0:
            valores_ejemplos = df.loc[tipos_incorrectos, campo].head(3).tolist()
            tipos_encontrados = [type(v).__name__ for v in valores_ejemplos]
            errors.append(
                f"Campo '{campo}' tiene {num_incorrectos} valores con tipo incorrecto. "
                f"Esperado: {tipo_esperado.__name__}, "
                f"Encontrados: {tipos_encontrados}"
            )

    return {"is_valid": len(errors) == 0, "errors": errors}


def validar_integridad_referencial(
    df: pd.DataFrame, relaciones: dict[str, pd.DataFrame]
) -> dict[str, bool | list[str]]:
    """
    Valida que claves foráneas existan en tablas referenciadas.

    Args:
        df: DataFrame con tabla de hechos o dimensión
        relaciones: Diccionario {campo_fk: df_referencia}
                   ej: {"producto_id": df_productos, "cliente_id": df_clientes}

    Returns:
        Diccionario con:
            - is_valid (bool): True si todas las FK existen
            - errors (list[str]): Lista de mensajes de error

    Examples:
        >>> df_ventas = pd.DataFrame([
        ...     {"venta_id": 1, "producto_id": 10}
        ... ])
        >>> df_productos = pd.DataFrame([{"producto_id": 10}])
        >>> resultado = validar_integridad_referencial(
        ...     df_ventas, {"producto_id": df_productos}
        ... )
        >>> resultado["is_valid"]
        True

        >>> df_ventas = pd.DataFrame([
        ...     {"venta_id": 1, "producto_id": 99}
        ... ])
        >>> resultado = validar_integridad_referencial(
        ...     df_ventas, {"producto_id": df_productos}
        ... )
        >>> resultado["is_valid"]
        False
    """
    errors = []

    if df.empty:
        return {"is_valid": True, "errors": []}

    for campo_fk, df_referencia in relaciones.items():
        if campo_fk not in df.columns:
            errors.append(f"Campo FK '{campo_fk}' no existe en DataFrame")
            continue

        if campo_fk not in df_referencia.columns:
            errors.append(f"Campo FK '{campo_fk}' no existe en tabla de referencia")
            continue

        # Obtener valores únicos de FK en tabla principal
        valores_fk = df[campo_fk].unique()

        # Obtener valores válidos de la tabla referenciada
        valores_validos = df_referencia[campo_fk].unique()

        # Encontrar FK que no existen
        fk_faltantes = set(valores_fk) - set(valores_validos)

        if len(fk_faltantes) > 0:
            fk_faltantes_lista = list(fk_faltantes)[:5]  # Máximo 5 ejemplos
            errors.append(
                f"Campo '{campo_fk}' tiene {len(fk_faltantes)} valores que no existen "
                f"en tabla referenciada. Ejemplos: {fk_faltantes_lista}"
            )

    return {"is_valid": len(errors) == 0, "errors": errors}


def validar_unicidad(
    df: pd.DataFrame, campos_unicos: list[str | list[str]]
) -> dict[str, bool | list[str]]:
    """
    Valida que campos o combinaciones de campos sean únicos.

    Args:
        df: DataFrame a validar
        campos_unicos: Lista de campos únicos (str) o combinaciones (list[str])
                      ej: ["email", ["cliente_id", "fecha"]]

    Returns:
        Diccionario con:
            - is_valid (bool): True si no hay duplicados
            - errors (list[str]): Lista de mensajes de error

    Examples:
        >>> df = pd.DataFrame([
        ...     {"id": 1, "email": "a@test.com"},
        ...     {"id": 2, "email": "b@test.com"}
        ... ])
        >>> resultado = validar_unicidad(df, ["id", "email"])
        >>> resultado["is_valid"]
        True

        >>> df = pd.DataFrame([
        ...     {"id": 1, "email": "a@test.com"},
        ...     {"id": 1, "email": "b@test.com"}
        ... ])
        >>> resultado = validar_unicidad(df, ["id"])
        >>> resultado["is_valid"]
        False
    """
    errors = []

    if df.empty:
        return {"is_valid": True, "errors": []}

    for campo in campos_unicos:
        if isinstance(campo, list):
            # Combinación de campos
            campo_nombre = "+".join(campo)

            # Verificar que todos los campos existen
            campos_faltantes = [c for c in campo if c not in df.columns]
            if campos_faltantes:
                errors.append(f"Campos {campos_faltantes} no existen en DataFrame")
                continue

            # Verificar duplicados en combinación
            duplicados = df.duplicated(subset=campo, keep=False)
            num_duplicados = duplicados.sum()

            if num_duplicados > 0:
                valores_dup = df.loc[duplicados, campo].head(3).values.tolist()
                errors.append(
                    f"Combinación {campo_nombre} tiene {num_duplicados} duplicados. "
                    f"Ejemplos: {valores_dup}"
                )

        else:
            # Campo simple
            if campo not in df.columns:
                errors.append(f"Campo '{campo}' no existe en DataFrame")
                continue

            duplicados = df[campo].duplicated(keep=False)
            num_duplicados = duplicados.sum()

            if num_duplicados > 0:
                valores_dup = df.loc[duplicados, campo].unique().tolist()[:5]
                errors.append(
                    f"Campo '{campo}' tiene {num_duplicados} duplicados. "
                    f"Valores duplicados: {valores_dup}"
                )

    return {"is_valid": len(errors) == 0, "errors": errors}
