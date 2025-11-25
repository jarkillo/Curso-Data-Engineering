"""
Módulo de carga de datos (capa Gold).

Carga datos en Parquet y bases de datos relacionales.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import Engine


def cargar_a_parquet(df: pd.DataFrame, ruta: Path) -> None:
    """
    Carga DataFrame en formato Parquet.

    Args:
        df: DataFrame a guardar
        ruta: Ruta del archivo Parquet

    Raises:
        ValueError: Si DataFrame está vacío

    Examples:
        >>> from pathlib import Path
        >>> df = pd.DataFrame({"col": [1, 2, 3]})
        >>> cargar_a_parquet(df, Path("datos.parquet"))  # doctest: +SKIP
    """
    if df.empty:
        raise ValueError("No se puede cargar DataFrame vacío")

    # Crear directorio si no existe
    ruta.parent.mkdir(parents=True, exist_ok=True)

    # Guardar con compresión
    df.to_parquet(ruta, index=False, compression="snappy")


def cargar_a_base_datos(
    df: pd.DataFrame, engine: Engine, tabla: str, if_exists: str = "replace"
) -> int:
    """
    Carga DataFrame en base de datos.

    Args:
        df: DataFrame a cargar
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla
        if_exists: Acción si tabla existe ("fail", "replace", "append")

    Returns:
        Número de registros cargados

    Raises:
        ValueError: Si DataFrame está vacío

    Examples:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine("sqlite:///:memory:")
        >>> df = pd.DataFrame({"id": [1, 2], "valor": [10, 20]})
        >>> num_cargados = cargar_a_base_datos(df, engine, "tabla")
        >>> num_cargados
        2
    """
    if df.empty:
        raise ValueError("No se puede cargar DataFrame vacío")

    # Cargar en base de datos
    df.to_sql(tabla, engine, if_exists=if_exists, index=False, method="multi")

    return len(df)


def verificar_carga_parquet(df: pd.DataFrame, ruta: Path) -> dict:
    """
    Verifica que carga en Parquet fue exitosa.

    Args:
        df: DataFrame original
        ruta: Ruta del archivo Parquet

    Returns:
        Dict con resultado de verificación

    Examples:
        >>> from pathlib import Path
        >>> df = pd.DataFrame({"col": [1, 2, 3]})
        >>> resultado = verificar_carga_parquet(df, Path("inexistente.parquet"))
        >>> resultado["valido"]
        False
    """
    try:
        if not ruta.exists():
            return {
                "valido": False,
                "registros_esperados": len(df),
                "registros_cargados": 0,
                "mensaje": "Archivo no existe",
            }

        df_leido = pd.read_parquet(ruta)
        conteo_cargado = len(df_leido)
        conteo_esperado = len(df)

        return {
            "valido": conteo_cargado == conteo_esperado,
            "registros_esperados": conteo_esperado,
            "registros_cargados": conteo_cargado,
        }

    except Exception as e:
        return {
            "valido": False,
            "registros_esperados": len(df),
            "registros_cargados": 0,
            "mensaje": f"Error al verificar: {str(e)}",
        }


def verificar_carga_base_datos(df: pd.DataFrame, engine: Engine, tabla: str) -> dict:
    """
    Verifica que carga en base de datos fue exitosa.

    Args:
        df: DataFrame original
        engine: SQLAlchemy engine
        tabla: Nombre de la tabla

    Returns:
        Dict con resultado de verificación

    Examples:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine("sqlite:///:memory:")
        >>> df = pd.DataFrame({"col": [1, 2, 3]})
        >>> resultado = verificar_carga_base_datos(df, engine, "inexistente")
        >>> resultado["valido"]
        False
    """
    try:
        df_leido = pd.read_sql(f"SELECT COUNT(*) as total FROM {tabla}", engine)
        conteo_cargado = int(df_leido.iloc[0]["total"])
        conteo_esperado = len(df)

        return {
            "valido": conteo_cargado == conteo_esperado,
            "registros_esperados": conteo_esperado,
            "registros_cargados": conteo_cargado,
        }

    except Exception as e:
        return {
            "valido": False,
            "registros_esperados": len(df),
            "registros_cargados": 0,
            "mensaje": f"Error al verificar: {str(e)}",
        }
