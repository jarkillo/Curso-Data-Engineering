"""
Módulo para estrategia de carga completa (Full Load).

Implementa funciones para reemplazar completamente los datos de una tabla.

SECURITY NOTE: SQL Injection y Nombres de Tablas
------------------------------------------------
Este módulo usa f-strings para insertar nombres de tabla en queries SQL:
    conn.execute(text(f"DELETE FROM {tabla}"))

Esto es SEGURO en este contexto porque:
1. Los nombres de tabla vienen de código controlado, no input de usuarios
2. SQLAlchemy no soporta nombres de tabla/columna parametrizados
3. Se validan con validar_identificador_sql() antes de usar

NUNCA uses este patrón con input de usuario sin validación.
"""

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError, OperationalError

from src.error_ids import ErrorIds
from src.logging_utils import log_error
from src.validations import validar_dataframe_no_vacio, validar_identificador_sql


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
        ValueError: Si el DataFrame está vacío o nombre de tabla inválido
        OperationalError: Si falla la operación de base de datos
        IntegrityError: Si hay violación de constraints

    Examples:
        >>> engine = create_engine("sqlite:///db.db")
        >>> df = pd.DataFrame({"id": [1, 2], "valor": [10, 20]})
        >>> num_cargados = full_load(df, engine, "mi_tabla")
        >>> print(num_cargados)
        2
    """
    # Validaciones de seguridad y entrada
    validar_dataframe_no_vacio(df)
    validar_identificador_sql(tabla)

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
        columnas_requeridas: Columnas que deben existir en el DataFrame
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
    except (OperationalError, IntegrityError) as e:
        # Errores esperados de base de datos
        log_error(
            "Full load failed - database error",
            {
                "error_id": ErrorIds.DATABASE_OPERATION_FAILED,
                "tabla": tabla,
                "num_rows": len(df),
                "error": str(e),
            },
        )
        resultado["valido"] = False
        resultado["mensaje"] = f"Error de base de datos: {str(e)}"
    except Exception as e:
        # Errores inesperados - logear y re-raise
        log_error(
            "Full load failed - unexpected error",
            {"error_id": ErrorIds.UNEXPECTED_ERROR, "tabla": tabla, "error": str(e)},
        )
        raise

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
        True si conteos coinciden

    Raises:
        OperationalError: Si la tabla no existe o query falla
        ValueError: Si no se puede verificar la carga

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
    except OperationalError as e:
        log_error(
            "Verification query failed",
            {
                "error_id": ErrorIds.DATABASE_QUERY_FAILED,
                "tabla": tabla,
                "error": str(e),
            },
        )
        raise ValueError(f"No se pudo verificar tabla '{tabla}': {e}") from e
    except Exception as e:
        log_error(
            "Unexpected error during verification",
            {"error_id": ErrorIds.UNEXPECTED_ERROR, "tabla": tabla, "error": str(e)},
        )
        raise


def _tabla_existe(engine: Engine, tabla: str) -> bool:
    """
    Verifica si una tabla existe en la base de datos.

    Args:
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla

    Returns:
        True si existe, False si no

    Raises:
        OperationalError: Si hay error de BD que NO es "tabla no existe"
        Exception: Para errores inesperados de infraestructura
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(f"SELECT 1 FROM {tabla} LIMIT 1"))
        return True
    except OperationalError as e:
        # Verificar si el error es específicamente "tabla no existe"
        error_msg = str(e).lower()
        if any(
            msg in error_msg for msg in ["no such table", "doesn't exist", "not exist"]
        ):
            return False
        else:
            # Otros errores operacionales deben ser logueados y re-raised
            log_error(
                "Database query failed during table check",
                {
                    "error_id": ErrorIds.DATABASE_QUERY_FAILED,
                    "tabla": tabla,
                    "error": str(e),
                },
            )
            raise
    except Exception as e:
        log_error(
            "Unexpected error checking table existence",
            {"error_id": ErrorIds.UNEXPECTED_ERROR, "tabla": tabla, "error": str(e)},
        )
        raise
