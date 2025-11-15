"""
Módulo de gestión de compresión de archivos.

Proporciona funciones para comprimir, descomprimir y comparar algoritmos.
"""

import bz2
import gzip
import io
import lzma
import os
import time
from pathlib import Path
from typing import Dict, List

import pandas as pd


def comprimir_archivo(ruta_entrada: str, algoritmo: str = "gzip") -> str:
    """
    Comprime un archivo usando el algoritmo especificado.

    Args:
        ruta_entrada: Ruta del archivo a comprimir
        algoritmo: Algoritmo de compresión ('gzip', 'bz2', 'xz')

    Returns:
        Ruta del archivo comprimido

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el algoritmo no es soportado
    """
    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_entrada}")

    algoritmos_soportados = {
        "gzip": (gzip.open, ".gz"),
        "bz2": (bz2.open, ".bz2"),
        "xz": (lzma.open, ".xz"),
    }

    if algoritmo not in algoritmos_soportados:
        raise ValueError(
            f"Algoritmo de compresión no soportado: {algoritmo}. "
            f"Soportados: {list(algoritmos_soportados.keys())}"
        )

    # Obtener función de compresión y extensión
    funcion_comprimir, extension = algoritmos_soportados[algoritmo]
    ruta_salida = ruta_entrada + extension

    # Comprimir
    with open(ruta_entrada, "rb") as f_in:
        with funcion_comprimir(ruta_salida, "wb") as f_out:
            f_out.write(f_in.read())

    return ruta_salida


def descomprimir_archivo(ruta_comprimida: str) -> str:
    """
    Descomprime un archivo detectando el formato automáticamente.

    Args:
        ruta_comprimida: Ruta del archivo comprimido

    Returns:
        Ruta del archivo descomprimido

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato de compresión no es reconocido
    """
    if not os.path.exists(ruta_comprimida):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_comprimida}")

    path = Path(ruta_comprimida)
    extension = path.suffix.lower()

    # Mapeo de extensiones a funciones de descompresión
    descompresores = {".gz": gzip.open, ".bz2": bz2.open, ".xz": lzma.open}

    if extension not in descompresores:
        raise ValueError(
            f"Formato de compresión no reconocido: {extension}. "
            f"Soportados: {list(descompresores.keys())}"
        )

    # Obtener función de descompresión
    funcion_descomprimir = descompresores[extension]

    # Generar nombre de archivo descomprimido (remover extensión de compresión)
    ruta_salida = str(path.with_suffix(""))

    # Descomprimir
    with funcion_descomprimir(ruta_comprimida, "rb") as f_in:
        with open(ruta_salida, "wb") as f_out:
            f_out.write(f_in.read())

    return ruta_salida


def comparar_compresiones(ruta_archivo: str, algoritmos: List[str]) -> Dict[str, Dict]:
    """
    Compara múltiples algoritmos de compresión para un archivo.

    Args:
        ruta_archivo: Ruta del archivo a comprimir
        algoritmos: Lista de algoritmos a comparar ('gzip', 'bz2', 'xz')

    Returns:
        Diccionario con métricas por algoritmo:
        {
            'gzip': {
                'tamanio_original_kb': float,
                'tamanio_comprimido_kb': float,
                'ratio_compresion': float,
                'reduccion_pct': float,
                'tiempo_compresion_s': float
            },
            ...
        }

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si no se proporcionan algoritmos
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")

    if not algoritmos:
        raise ValueError("Se debe proporcionar al menos un algoritmo")

    tamanio_original = os.path.getsize(ruta_archivo) / 1024  # KB

    resultados = {}
    archivos_temporales = []

    try:
        for algoritmo in algoritmos:
            # Comprimir y medir tiempo
            inicio = time.time()
            ruta_comprimida = comprimir_archivo(ruta_archivo, algoritmo)
            tiempo_compresion = time.time() - inicio

            archivos_temporales.append(ruta_comprimida)

            # Obtener tamaño comprimido
            tamanio_comprimido = os.path.getsize(ruta_comprimida) / 1024  # KB

            # Calcular métricas
            ratio = tamanio_original / tamanio_comprimido
            reduccion = (
                (tamanio_original - tamanio_comprimido) / tamanio_original
            ) * 100

            resultados[algoritmo] = {
                "tamanio_original_kb": round(tamanio_original, 2),
                "tamanio_comprimido_kb": round(tamanio_comprimido, 2),
                "ratio_compresion": round(ratio, 2),
                "reduccion_pct": round(reduccion, 1),
                "tiempo_compresion_s": round(tiempo_compresion, 4),
            }

    finally:
        # Limpiar archivos temporales
        for archivo_temp in archivos_temporales:
            try:
                os.remove(archivo_temp)
            except OSError:
                pass  # Ignorar errores de limpieza

    return resultados


def comprimir_dataframe_memoria(df: pd.DataFrame, algoritmo: str = "gzip") -> bytes:
    """
    Comprime un DataFrame en memoria sin escribir a disco.

    Args:
        df: DataFrame a comprimir
        algoritmo: Algoritmo de compresión ('gzip', 'bz2')

    Returns:
        Bytes comprimidos

    Raises:
        ValueError: Si DataFrame está vacío o algoritmo no soportado
    """
    if df.empty:
        raise ValueError("No se puede comprimir un DataFrame vacío")

    # Mapeo de algoritmos a funciones de compresión
    compresores = {"gzip": gzip.compress, "bz2": bz2.compress}

    if algoritmo not in compresores:
        raise ValueError(
            f"Algoritmo no soportado: {algoritmo}. "
            f"Soportados: {list(compresores.keys())}"
        )

    # Serializar DataFrame a CSV en memoria
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    datos_csv = buffer.getvalue()

    # Comprimir
    funcion_comprimir = compresores[algoritmo]
    datos_comprimidos = funcion_comprimir(datos_csv)

    return datos_comprimidos
