"""
Módulo para estrategia de carga upsert (insert + update).

Implementa funciones para insertar registros nuevos y actualizar existentes.

SECURITY NOTE: SQL Injection y Nombres de Tablas
------------------------------------------------
Este módulo usa f-strings para insertar nombres de tabla en queries SQL.
Esto es SEGURO porque se validan con validar_identificador_sql() antes de usar.
Ver cargador_full.py para más detalles sobre esta práctica.
"""

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.exc import OperationalError

from src.error_ids import ErrorIds
from src.logging_utils import log_error, log_for_debugging
from src.validations import (
    validar_columna_existe,
    validar_dataframe_no_vacio,
    validar_identificador_sql,
)


def upsert(df: pd.DataFrame, engine: Engine, tabla: str, columna_clave: str) -> None:
    """
    Upsert: inserta registros nuevos y actualiza existentes.

    Estrategia: DELETE registros con claves existentes + INSERT todos.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_clave: Columna que identifica registros únicos

    Raises:
        ValueError: Si la columna clave no existe

    Examples:
        >>> df = pd.DataFrame({"id": [1, 2, 3], "valor": [10, 20, 30]})
        >>> upsert(df, engine, "tabla", "id")
    """
    # Validaciones de seguridad
    validar_identificador_sql(tabla)
    validar_identificador_sql(columna_clave)
    validar_dataframe_no_vacio(df)
    validar_columna_existe(df, columna_clave)

    with engine.begin() as conn:
        # Verificar si tabla existe
        try:
            conn.execute(text(f"SELECT 1 FROM {tabla} LIMIT 1"))
            tabla_existe = True
        except OperationalError:
            # Tabla no existe (expected)
            log_for_debugging(
                "Table does not exist yet, will create on first insert",
                {"tabla": tabla},
            )
            tabla_existe = False
        except Exception as e:
            # Error inesperado al verificar tabla
            log_error(
                "Unexpected error checking if table exists",
                {
                    "error_id": ErrorIds.DATABASE_QUERY_FAILED,
                    "tabla": tabla,
                    "error": str(e),
                },
            )
            raise

        if tabla_existe:
            # Eliminar registros con claves que vamos a insertar
            # Usar bound parameters para evitar SQL injection
            claves = df[columna_clave].tolist()

            if claves:  # Solo ejecutar si hay claves
                # Crear placeholders para bound parameters
                placeholders = ",".join([f":key_{i}" for i in range(len(claves))])
                # Crear dict de parámetros
                params = {f"key_{i}": clave for i, clave in enumerate(claves)}

                conn.execute(
                    text(
                        f"DELETE FROM {tabla} WHERE {columna_clave} IN ({placeholders})"
                    ),
                    params,
                )

        # Insertar todos los registros
        df.to_sql(tabla, conn, if_exists="append", index=False, method="multi")


def upsert_con_metricas(
    df: pd.DataFrame, engine: Engine, tabla: str, columna_clave: str
) -> dict:
    """
    Upsert con métricas de inserts vs updates.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_clave: Columna clave

    Returns:
        Dict con métricas: {"inserts": int, "updates": int, "total": int}

    Examples:
        >>> resultado = upsert_con_metricas(df, engine, "tabla", "id")
        >>> print(f"Inserts: {resultado['inserts']}, Updates: {resultado['updates']}")
    """
    # Contar registros antes
    try:
        total_antes = pd.read_sql(
            f"SELECT COUNT(*) as total FROM {tabla}", engine
        ).iloc[0]["total"]
    except OperationalError:
        # Tabla no existe (expected)
        log_for_debugging("Table does not exist, count=0", {"tabla": tabla})
        total_antes = 0
    except Exception as e:
        # Error inesperado al contar
        log_error(
            "Unexpected error counting rows before upsert",
            {
                "error_id": ErrorIds.DATABASE_QUERY_FAILED,
                "tabla": tabla,
                "error": str(e),
            },
        )
        raise

    # Ejecutar upsert
    upsert(df, engine, tabla, columna_clave)

    # Contar después
    total_despues = pd.read_sql(f"SELECT COUNT(*) as total FROM {tabla}", engine).iloc[
        0
    ]["total"]

    # Calcular métricas
    inserts = total_despues - total_antes
    updates = len(df) - inserts

    return {"inserts": inserts, "updates": updates, "total": len(df)}


def detectar_cambios(
    df: pd.DataFrame, engine: Engine, tabla: str, columna_clave: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detecta qué registros son nuevos vs existentes.

    Args:
        df: DataFrame a analizar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        columna_clave: Columna clave

    Returns:
        Tupla (df_nuevos, df_existentes)

    Examples:
        >>> df_nuevos, df_existentes = detectar_cambios(df, engine, "tabla", "id")
        >>> print(f"Nuevos: {len(df_nuevos)}, Existentes: {len(df_existentes)}")
    """
    # Validaciones de seguridad
    validar_identificador_sql(tabla)
    validar_identificador_sql(columna_clave)

    # Intentar leer claves existentes
    try:
        claves_bd = pd.read_sql(f"SELECT {columna_clave} FROM {tabla}", engine)[
            columna_clave
        ].tolist()
    except OperationalError:
        # Tabla no existe (expected) - todos son nuevos
        log_for_debugging(
            "Table does not exist, all records are new",
            {"tabla": tabla, "total_records": len(df)},
        )
        return df, pd.DataFrame()
    except Exception as e:
        # Error inesperado al leer claves
        log_error(
            "Unexpected error reading existing keys",
            {
                "error_id": ErrorIds.DATABASE_QUERY_FAILED,
                "tabla": tabla,
                "columna_clave": columna_clave,
                "error": str(e),
            },
        )
        raise

    # Separar nuevos de existentes
    mask_nuevos = ~df[columna_clave].isin(claves_bd)
    df_nuevos = df[mask_nuevos].copy()
    df_existentes = df[~mask_nuevos].copy()

    return df_nuevos, df_existentes
