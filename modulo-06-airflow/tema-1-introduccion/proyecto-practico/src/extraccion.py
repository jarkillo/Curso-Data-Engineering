"""
Módulo de extracción de datos

Funciones para leer datos de ventas desde archivos CSV.

Principios:
- Funciones puras sin efectos secundarios
- Validación exhaustiva de inputs
- Manejo explícito de errores
- Tipado completo
"""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd


def obtener_ruta_archivo(fecha: str) -> str:
    """
    Construye la ruta al archivo CSV de ventas para una fecha específica.

    Args:
        fecha: Fecha en formato YYYY-MM-DD

    Returns:
        str: Ruta al archivo CSV (data/input/ventas_YYYY_MM_DD.csv)

    Raises:
        ValueError: Si el formato de fecha es inválido

    Examples:
        >>> obtener_ruta_archivo("2025-10-25")
        'data/input/ventas_2025_10_25.csv'
    """
    # Validar formato de fecha
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Formato de fecha inválido: '{fecha}'. Se esperaba formato YYYY-MM-DD"
        )

    # Construir nombre de archivo (reemplazar guiones por guiones bajos)
    fecha_formato = fecha.replace("-", "_")
    nombre_archivo = f"ventas_{fecha_formato}.csv"

    # Construir ruta completa de forma segura
    directorio_base = Path(__file__).parent.parent
    ruta_archivo = directorio_base / "data" / "input" / nombre_archivo

    return str(ruta_archivo)


def extraer_ventas_csv(ruta_archivo: str) -> pd.DataFrame:
    """
    Lee un archivo CSV de ventas y retorna un DataFrame.

    Args:
        ruta_archivo: Ruta al archivo CSV de ventas

    Returns:
        pd.DataFrame: DataFrame con los datos de ventas

    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el archivo está vacío o corrupto

    Examples:
        >>> df = extraer_ventas_csv("data/input/ventas_2025_10_25.csv")
        >>> print(len(df))
        150
    """
    # Verificar que el archivo existe
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(
            f"El archivo '{ruta_archivo}' no existe. "
            f"Verifica la ruta y que los datos estén disponibles."
        )

    # Leer CSV
    try:
        df = pd.read_csv(ruta_archivo)
    except Exception as e:
        raise ValueError(f"Error al leer el archivo CSV '{ruta_archivo}': {str(e)}")

    # Verificar que no está vacío
    if df.empty:
        raise ValueError(
            f"El archivo '{ruta_archivo}' está vacío o solo contiene headers. "
            f"No hay datos para procesar."
        )

    print(f"✅ Extracción exitosa: {len(df)} ventas leídas desde {ruta_archivo}")

    return df
