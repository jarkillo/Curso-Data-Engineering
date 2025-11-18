"""
Módulo para estrategia de carga completa (Full Load).

Implementa funciones para reemplazar completamente los datos de una tabla.
"""

import pandas as pd
from sqlalchemy import Engine, text


def full_load(df: pd.DataFrame, engine: Engine, tabla: str) -> int:
    """
    Carga completa: elimina todos los datos existentes e inserta los nuevos.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla destino

    Returns:
        Número de registros cargados

    Raises:
        ValueError: Si el DataFrame está vacío

    Examples:
        >>> engine = create_engine("sqlite:///db.db")
        >>> df = pd.DataFrame({"id": [1, 2], "valor": [10, 20]})
        >>> num_cargados = full_load(df, engine, "mi_tabla")
        >>> print(num_cargados)
        2
    """
    if df.empty:
        raise ValueError("No se puede hacer full load con DataFrame vacío")

    with engine.begin() as conn:
        # 1. Eliminar datos existentes si la tabla ya existe
        if _tabla_existe(engine, tabla):
            conn.execute(text(f"DELETE FROM {tabla}"))

        # 2. Insertar todos los datos
        df.to_sql(tabla, conn, if_exists="append", index=False, method="multi")

    return len(df)


def full_load_con_validacion(
    df: pd.DataFrame,
    engine: Engine,
    tabla: str,
    columnas_requeridas: list[str] | None = None,
    columnas_no_nulas: list[str] | None = None,
) -> dict:
    """
    Full load con validación previa de datos.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columnas_requeridas: Columnas que deben exist en el DataFrame
        columnas_no_nulas: Columnas que no deben tener valores nulos

    Returns:
        Dict con resultado: {"valido": bool, "cargados": int, "invalidos": int, "mensaje": str}

    Examples:
        >>> resultado = full_load_con_validacion(
        ...     df,
        ...     engine,
        ...     "tabla",
        ...     columnas_requeridas=["id", "nombre"]
        ... )
        >>> print(resultado["valido"])
        True
    """
    resultado = {"valido": True, "cargados": 0, "invalidos": 0, "mensaje": "OK"}

    # Validar columnas requeridas
    if columnas_requeridas:
        columnas_faltantes = set(columnas_requeridas) - set(df.columns)
        if columnas_faltantes:
            resultado["valido"] = False
            resultado["mensaje"] = f"Faltan columnas: {columnas_faltantes}"
            return resultado

    # Validar valores nulos en columnas críticas
    if columnas_no_nulas:
        for col in columnas_no_nulas:
            if col in df.columns and df[col].isnull().any():
                num_nulos = df[col].isnull().sum()
                resultado["valido"] = False
                resultado["invalidos"] = num_nulos
                resultado["mensaje"] = (
                    f"Columna '{col}' tiene {num_nulos} valores nulos"
                )
                return resultado

    # Si validación pasa, cargar datos
    try:
        num_cargados = full_load(df, engine, tabla)
        resultado["cargados"] = num_cargados
    except Exception as e:
        resultado["valido"] = False
        resultado["mensaje"] = f"Error durante carga: {str(e)}"

    return resultado


def full_load_idempotente(df: pd.DataFrame, engine: Engine, tabla: str) -> dict:
    """
    Full load idempotente: puede ejecutarse múltiples veces con mismo resultado.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla

    Returns:
        Dict con métricas: {"cargados": int, "operacion": str}

    Examples:
        >>> # Primera ejecución
        >>> resultado = full_load_idempotente(df, engine, "tabla")
        >>> print(resultado["operacion"])
        'insert'
        >>> # Segunda ejecución (reemplaza datos)
        >>> resultado = full_load_idempotente(df, engine, "tabla")
        >>> print(resultado["operacion"])
        'replace'
    """
    tabla_existe = _tabla_existe(engine, tabla)

    with engine.begin() as conn:
        if tabla_existe:
            # Eliminar datos existentes
            conn.execute(text(f"DELETE FROM {tabla}"))
            operacion = "replace"
        else:
            operacion = "insert"

        # Insertar datos
        df.to_sql(tabla, conn, if_exists="append", index=False, method="multi")

    return {"cargados": len(df), "operacion": operacion}


def verificar_carga_exitosa(df: pd.DataFrame, engine: Engine, tabla: str) -> bool:
    """
    Verifica que la carga fue exitosa comparando conteos.

    Args:
        df: DataFrame que se intentó cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla

    Returns:
        True si conteos coinciden, False si no

    Examples:
        >>> full_load(df, engine, "tabla")
        >>> exito = verificar_carga_exitosa(df, engine, "tabla")
        >>> print(exito)
        True
    """
    try:
        total_bd = pd.read_sql(f"SELECT COUNT(*) as total FROM {tabla}", engine).iloc[
            0
        ]["total"]
        return bool(total_bd == len(df))
    except Exception:
        return False


def _tabla_existe(engine: Engine, tabla: str) -> bool:
    """
    Verifica si una tabla existe en la base de datos.

    Args:
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla

    Returns:
        True si existe, False si no
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(f"SELECT 1 FROM {tabla} LIMIT 1"))
        return True
    except Exception:
        return False
