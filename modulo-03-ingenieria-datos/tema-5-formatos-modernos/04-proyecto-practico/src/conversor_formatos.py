"""
Módulo de conversión entre formatos de datos.

Proporciona funciones para convertir entre CSV, JSON, JSON Lines y Parquet.
"""

import os
from pathlib import Path
from typing import List, Optional

import pandas as pd


def convertir_csv_a_parquet(
    ruta_csv: str, ruta_parquet: str, compresion: str = "snappy"
) -> None:
    """
    Convierte archivo CSV a Parquet con compresión.

    Args:
        ruta_csv: Ruta del archivo CSV de entrada
        ruta_parquet: Ruta del archivo Parquet de salida
        compresion: Algoritmo de compresión ('snappy', 'gzip', 'brotli', 'zstd', None)

    Raises:
        FileNotFoundError: Si el archivo CSV no existe
        ValueError: Si la compresión es inválida
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_csv}")

    algoritmos_validos = ["snappy", "gzip", "brotli", "zstd", None]
    if compresion not in algoritmos_validos:
        raise ValueError(
            f"Algoritmo de compresión inválida: {compresion}. "
            f"Debe ser uno de: {algoritmos_validos}"
        )

    # Leer CSV
    df = pd.read_csv(ruta_csv)

    # Guardar como Parquet
    df.to_parquet(ruta_parquet, engine="pyarrow", compression=compresion, index=False)


def convertir_json_a_parquet(
    ruta_json: str, ruta_parquet: str, orient: str = "records"
) -> None:
    """
    Convierte archivo JSON a Parquet.

    Args:
        ruta_json: Ruta del archivo JSON de entrada
        ruta_parquet: Ruta del archivo Parquet de salida
        orient: Orientación del JSON ('records', 'split', 'index', 'columns', 'values', 'lines')

    Raises:
        FileNotFoundError: Si el archivo JSON no existe
    """
    if not os.path.exists(ruta_json):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_json}")

    # Leer JSON
    if orient == "lines":
        df = pd.read_json(ruta_json, lines=True)
    else:
        df = pd.read_json(ruta_json, orient=orient)

    # Guardar como Parquet
    df.to_parquet(ruta_parquet, engine="pyarrow", compression="snappy", index=False)


def convertir_parquet_a_csv(ruta_parquet: str, ruta_csv: str) -> None:
    """
    Convierte archivo Parquet a CSV.

    Args:
        ruta_parquet: Ruta del archivo Parquet de entrada
        ruta_csv: Ruta del archivo CSV de salida

    Raises:
        FileNotFoundError: Si el archivo Parquet no existe
    """
    if not os.path.exists(ruta_parquet):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_parquet}")

    # Leer Parquet
    df = pd.read_parquet(ruta_parquet)

    # Guardar como CSV
    df.to_csv(ruta_csv, index=False)


def convertir_json_a_csv(ruta_json: str, ruta_csv: str) -> None:
    """
    Convierte archivo JSON a CSV.

    Args:
        ruta_json: Ruta del archivo JSON de entrada
        ruta_csv: Ruta del archivo CSV de salida

    Raises:
        FileNotFoundError: Si el archivo JSON no existe
    """
    if not os.path.exists(ruta_json):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_json}")

    # Leer JSON (detectar si es JSON Lines)
    try:
        df = pd.read_json(ruta_json)
    except ValueError:
        # Intentar como JSON Lines
        df = pd.read_json(ruta_json, lines=True)

    # Guardar como CSV
    df.to_csv(ruta_csv, index=False)


def convertir_csv_a_json_lines(ruta_csv: str, ruta_jsonl: str) -> None:
    """
    Convierte archivo CSV a JSON Lines.

    Args:
        ruta_csv: Ruta del archivo CSV de entrada
        ruta_jsonl: Ruta del archivo JSON Lines de salida

    Raises:
        FileNotFoundError: Si el archivo CSV no existe
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_csv}")

    # Leer CSV
    df = pd.read_csv(ruta_csv)

    # Guardar como JSON Lines
    df.to_json(ruta_jsonl, orient="records", lines=True, force_ascii=False)


def leer_multiple_formatos(ruta: str) -> pd.DataFrame:
    """
    Lee archivo detectando automáticamente el formato.

    Soporta: CSV, JSON, JSON Lines, Parquet

    Args:
        ruta: Ruta del archivo a leer

    Returns:
        DataFrame con los datos

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato no es soportado
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    path = Path(ruta)
    extension = path.suffix.lower()

    # Manejar archivos comprimidos
    if extension == ".gz":
        # Obtener extensión real (ej: .csv.gz → .csv)
        extension = Path(path.stem).suffix.lower()

    # Leer según formato
    if extension == ".csv":
        return pd.read_csv(ruta)
    elif extension == ".json":
        # Detectar si es JSON Lines por contenido
        with open(ruta, "r", encoding="utf-8") as f:
            primera_linea = f.readline().strip()

        if primera_linea.startswith("[") or primera_linea.startswith("{"):
            # JSON estándar
            return pd.read_json(ruta)
        else:
            # Probablemente JSON Lines
            return pd.read_json(ruta, lines=True)
    elif extension == ".jsonl":
        return pd.read_json(ruta, lines=True)
    elif extension == ".parquet":
        return pd.read_parquet(ruta)
    else:
        raise ValueError(
            f"Formato no soportado: {extension}. "
            f"Soportados: .csv, .json, .jsonl, .parquet"
        )


def guardar_formato_automatico(
    df: pd.DataFrame, ruta: str, formato: Optional[str] = None
) -> None:
    """
    Guarda DataFrame detectando automáticamente el formato por extensión.

    Args:
        df: DataFrame a guardar
        ruta: Ruta del archivo de salida
        formato: Formato explícito (opcional, se detecta por extensión)

    Raises:
        ValueError: Si el DataFrame está vacío o formato no soportado
    """
    if df.empty:
        raise ValueError("No se puede guardar un DataFrame vacío")

    # Detectar formato
    if formato is None:
        path = Path(ruta)
        extension = path.suffix.lower()

        if extension == ".csv":
            formato = "csv"
        elif extension in [".json", ".jsonl"]:
            formato = "jsonl" if extension == ".jsonl" else "json"
        elif extension == ".parquet":
            formato = "parquet"
        else:
            raise ValueError(
                f"Formato no soportado: {extension}. "
                f"Soportados: .csv, .json, .jsonl, .parquet"
            )

    # Guardar según formato
    if formato == "csv":
        df.to_csv(ruta, index=False)
    elif formato == "json":
        df.to_json(ruta, orient="records", indent=2, force_ascii=False)
    elif formato == "jsonl":
        df.to_json(ruta, orient="records", lines=True, force_ascii=False)
    elif formato == "parquet":
        df.to_parquet(ruta, engine="pyarrow", compression="snappy", index=False)
    else:
        raise ValueError(f"Formato no soportado: {formato}")


def convertir_con_particiones(
    df: pd.DataFrame,
    ruta_base: str,
    columnas_particion: List[str],
    formato: str = "parquet",
) -> None:
    """
    Guarda DataFrame particionado por columnas especificadas.

    Args:
        df: DataFrame a guardar
        ruta_base: Directorio base para particiones
        columnas_particion: Lista de columnas para particionar
        formato: Formato de salida (solo 'parquet' soportado actualmente)

    Raises:
        ValueError: Si columna no existe o formato no es Parquet
    """
    # Validar formato
    if formato != "parquet":
        raise ValueError(
            "Particionamiento solo soporta Parquet actualmente. "
            f"Formato recibido: {formato}"
        )

    # Validar columnas
    for col in columnas_particion:
        if col not in df.columns:
            raise ValueError(f"Columna '{col}' no existe en DataFrame")

    # Guardar particionado
    df.to_parquet(
        ruta_base,
        engine="pyarrow",
        compression="snappy",
        partition_cols=columnas_particion,
        index=False,
    )
