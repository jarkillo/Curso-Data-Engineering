"""
Módulo de extracción de datos desde múltiples fuentes.

Este módulo proporciona funciones para extraer datos de archivos CSV y JSON,
transformándolos en DataFrames de pandas para su posterior procesamiento.
"""

from pathlib import Path

import pandas as pd


def extraer_ventas_csv(ruta_csv: str) -> pd.DataFrame:
    """
    Extrae datos de ventas desde un archivo CSV.

    Args:
        ruta_csv: Ruta al archivo CSV de ventas

    Returns:
        DataFrame con columnas: producto, cantidad, precio, cliente_id

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> df = extraer_ventas_csv("data/input/ventas.csv")
        >>> print(df.columns.tolist())
        ['producto', 'cantidad', 'precio', 'cliente_id']
    """
    ruta = Path(ruta_csv)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    df = pd.read_csv(ruta)
    print(f"[EXTRAER_VENTAS] Extraídos {len(df)} registros de ventas")
    return df


def extraer_clientes_json(ruta_json: str) -> pd.DataFrame:
    """
    Extrae datos de clientes desde un archivo JSON.

    Args:
        ruta_json: Ruta al archivo JSON de clientes

    Returns:
        DataFrame con columnas: cliente_id, nombre, nivel

    Raises:
        FileNotFoundError: Si el archivo no existe

    Examples:
        >>> df = extraer_clientes_json("data/input/clientes.json")
        >>> print(df.columns.tolist())
        ['cliente_id', 'nombre', 'nivel']
    """
    ruta = Path(ruta_json)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_json}")

    df = pd.read_json(ruta)
    print(f"[EXTRAER_CLIENTES] Extraídos {len(df)} registros de clientes")
    return df


def contar_registros_extraidos(df: pd.DataFrame) -> int:
    """
    Cuenta la cantidad de registros en un DataFrame.

    Esta función es útil para guardar en XCom el número de registros extraídos.

    Args:
        df: DataFrame con los datos extraídos

    Returns:
        Número de filas en el DataFrame

    Examples:
        >>> df = pd.DataFrame({'col': [1, 2, 3]})
        >>> contar_registros_extraidos(df)
        3
    """
    count = len(df)
    print(f"[CONTAR] Total de registros: {count}")
    return count
