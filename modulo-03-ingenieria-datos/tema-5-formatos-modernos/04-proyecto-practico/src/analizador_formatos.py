"""
Módulo de análisis y comparación de formatos de datos.

Proporciona funciones para detectar formatos, obtener metadata y realizar benchmarks.
"""

import json
import os
import tempfile
import time
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


def detectar_formato_archivo(ruta: str) -> str:  # noqa: C901
    """
    Detecta automáticamente el formato de un archivo.

    Args:
        ruta: Ruta del archivo

    Returns:
        Formato detectado: 'csv', 'json', 'jsonl', 'parquet'

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

    # Detectar por extensión
    if extension == ".csv":
        return "csv"
    elif extension == ".parquet":
        return "parquet"
    elif extension == ".jsonl":
        return "jsonl"
    elif extension == ".json":
        # Leer primera línea para distinguir JSON de JSON Lines
        try:
            with open(ruta, encoding="utf-8") as f:
                primera_linea = f.readline().strip()

            # JSON estándar empieza con [ o {
            if primera_linea.startswith("[") or primera_linea.startswith("{"):
                # Verificar si es realmente JSON completo
                try:
                    with open(ruta, encoding="utf-8") as f:
                        segunda_linea = f.readlines()[1:2]
                        if segunda_linea and not segunda_linea[0].strip().startswith(
                            "{"
                        ):
                            # Probablemente JSON estándar
                            return "json"
                except (OSError, IndexError):
                    return "json"

                # Si todas las líneas empiezan con {, es JSON Lines
                return "jsonl"
            else:
                # Formato desconocido
                return "jsonl"  # Asumir JSON Lines por defecto
        except (OSError, json.JSONDecodeError):
            return "json"
    else:
        raise ValueError(
            f"Formato no soportado: {extension}. "
            f"Soportados: .csv, .json, .jsonl, .parquet"
        )


def obtener_metadata_parquet(ruta: str) -> dict:
    """
    Obtiene metadata detallada de un archivo Parquet.

    Args:
        ruta: Ruta del archivo Parquet

    Returns:
        Diccionario con metadata:
        {
            'num_filas': int,
            'num_columnas': int,
            'columnas': List[str],
            'tipos_datos': Dict[str, str],
            'tamanio_archivo_mb': float,
            'compresion': str,
            'num_row_groups': int
        }

    Raises:
        FileNotFoundError: Si el archivo no existe
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    # Leer metadata con PyArrow
    parquet_file = pq.ParquetFile(ruta)
    metadata = parquet_file.metadata

    # Leer DataFrame para obtener tipos de pandas
    df = pd.read_parquet(ruta)

    # Obtener información
    num_filas = metadata.num_rows
    num_columnas = metadata.num_columns
    columnas = df.columns.tolist()

    # Tipos de datos
    tipos_datos = {col: str(dtype) for col, dtype in df.dtypes.items()}

    # Tamaño del archivo
    tamanio_mb = os.path.getsize(ruta) / (1024 * 1024)

    # Compresión (del primer row group)
    compresion = "sin compresión"
    if metadata.num_row_groups > 0:
        row_group = metadata.row_group(0)
        if row_group.num_columns > 0:
            columna_meta = row_group.column(0)
            compresion = columna_meta.compression

    return {
        "num_filas": num_filas,
        "num_columnas": num_columnas,
        "columnas": columnas,
        "tipos_datos": tipos_datos,
        "tamanio_archivo_mb": round(tamanio_mb, 2),
        "compresion": compresion,
        "num_row_groups": metadata.num_row_groups,
    }


def comparar_tamanios_formatos(df: pd.DataFrame) -> dict[str, float]:
    """
    Compara tamaños de un DataFrame guardado en diferentes formatos.

    Args:
        df: DataFrame a comparar

    Returns:
        Diccionario con tamaños en KB por formato:
        {
            'csv': float,
            'json': float,
            'jsonl': float,
            'parquet_snappy': float,
            'parquet_gzip': float
        }

    Raises:
        ValueError: Si DataFrame está vacío
    """
    if df.empty:
        raise ValueError("No se puede comparar con un DataFrame vacío")

    resultados = {}

    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # CSV
        ruta_csv = temp_path / "datos.csv"
        df.to_csv(ruta_csv, index=False)
        resultados["csv"] = os.path.getsize(ruta_csv) / 1024

        # JSON
        ruta_json = temp_path / "datos.json"
        df.to_json(ruta_json, orient="records", indent=2, force_ascii=False)
        resultados["json"] = os.path.getsize(ruta_json) / 1024

        # JSON Lines
        ruta_jsonl = temp_path / "datos.jsonl"
        df.to_json(ruta_jsonl, orient="records", lines=True, force_ascii=False)
        resultados["jsonl"] = os.path.getsize(ruta_jsonl) / 1024

        # Parquet Snappy
        ruta_parquet_snappy = temp_path / "datos_snappy.parquet"
        df.to_parquet(ruta_parquet_snappy, compression="snappy", index=False)
        resultados["parquet_snappy"] = os.path.getsize(ruta_parquet_snappy) / 1024

        # Parquet Gzip
        ruta_parquet_gzip = temp_path / "datos_gzip.parquet"
        df.to_parquet(ruta_parquet_gzip, compression="gzip", index=False)
        resultados["parquet_gzip"] = os.path.getsize(ruta_parquet_gzip) / 1024

    # Redondear resultados
    return {k: round(v, 2) for k, v in resultados.items()}


def benchmark_lectura_escritura(  # noqa: C901
    df: pd.DataFrame, formatos: list[str]
) -> pd.DataFrame:
    """
    Realiza benchmark de lectura/escritura para diferentes formatos.

    Args:
        df: DataFrame a usar en el benchmark
        formatos: Lista de formatos a probar ('csv', 'json', 'jsonl', 'parquet')

    Returns:
        DataFrame con resultados del benchmark:
        columnas: formato, tiempo_escritura_s, tiempo_lectura_s, tamanio_kb

    Raises:
        ValueError: Si DataFrame está vacío o formato no soportado
    """
    if df.empty:
        raise ValueError("No se puede hacer benchmark con un DataFrame vacío")

    formatos_soportados = ["csv", "json", "jsonl", "parquet"]
    for formato in formatos:
        if formato not in formatos_soportados:
            raise ValueError(
                f"Formato no soportado: {formato}. "
                f"Soportados: {formatos_soportados}"
            )

    resultados = []

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for formato in formatos:
            # Preparar ruta
            if formato == "csv":
                ruta = temp_path / "datos.csv"
            elif formato == "json":
                ruta = temp_path / "datos.json"
            elif formato == "jsonl":
                ruta = temp_path / "datos.jsonl"
            else:  # parquet
                ruta = temp_path / "datos.parquet"

            # Medir escritura
            inicio = time.time()
            if formato == "csv":
                df.to_csv(ruta, index=False)
            elif formato == "json":
                df.to_json(ruta, orient="records", indent=2, force_ascii=False)
            elif formato == "jsonl":
                df.to_json(ruta, orient="records", lines=True, force_ascii=False)
            else:  # parquet
                df.to_parquet(ruta, compression="snappy", index=False)
            tiempo_escritura = time.time() - inicio

            # Tamaño
            tamanio_kb = os.path.getsize(ruta) / 1024

            # Medir lectura
            inicio = time.time()
            if formato == "csv":
                _ = pd.read_csv(ruta)
            elif formato == "json":
                _ = pd.read_json(ruta)
            elif formato == "jsonl":
                _ = pd.read_json(ruta, lines=True)
            else:  # parquet
                _ = pd.read_parquet(ruta)
            tiempo_lectura = time.time() - inicio

            resultados.append(
                {
                    "formato": formato,
                    "tiempo_escritura_s": round(tiempo_escritura, 4),
                    "tiempo_lectura_s": round(tiempo_lectura, 4),
                    "tamanio_kb": round(tamanio_kb, 2),
                }
            )

    return pd.DataFrame(resultados)


def generar_reporte_formato(ruta: str) -> dict:
    """
    Genera reporte completo de un archivo de datos.

    Args:
        ruta: Ruta del archivo

    Returns:
        Diccionario con reporte completo:
        {
            'formato': str,
            'tamanio_mb': float,
            'num_registros': int,
            'num_columnas': int,
            'columnas': List[str],
            'tipos_datos': Dict[str, str],
            'metadata_parquet': Dict (solo si es Parquet)
        }

    Raises:
        FileNotFoundError: Si el archivo no existe
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")

    # Detectar formato
    formato = detectar_formato_archivo(ruta)

    # Leer archivo
    if formato == "csv":
        df = pd.read_csv(ruta)
    elif formato == "json":
        df = pd.read_json(ruta)
    elif formato == "jsonl":
        df = pd.read_json(ruta, lines=True)
    else:  # parquet
        df = pd.read_parquet(ruta)

    # Información básica
    tamanio_mb = os.path.getsize(ruta) / (1024 * 1024)

    reporte = {
        "formato": formato,
        "tamanio_mb": round(tamanio_mb, 2),
        "num_registros": len(df),
        "num_columnas": len(df.columns),
        "columnas": df.columns.tolist(),
        "tipos_datos": {col: str(dtype) for col, dtype in df.dtypes.items()},
    }

    # Metadata adicional para Parquet
    if formato == "parquet":
        try:
            metadata_parquet = obtener_metadata_parquet(ruta)
            reporte["metadata_parquet"] = metadata_parquet
            reporte["compresion"] = metadata_parquet["compresion"]
        except Exception:  # nosec B110
            pass  # Si falla, continuar sin metadata adicional

    return reporte
