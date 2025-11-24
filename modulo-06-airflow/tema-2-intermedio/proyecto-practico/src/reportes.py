"""
Módulo de generación de reportes.

Este módulo proporciona funciones para generar reportes detallados y simples,
y exportarlos a formatos CSV y JSON.
"""

import json
from pathlib import Path

import pandas as pd


def generar_reporte_detallado(df: pd.DataFrame, total: float) -> dict:
    """
    Genera un reporte detallado con métricas completas.

    Incluye:
    - Tipo de reporte
    - Total de ventas
    - Número de clientes
    - Detalles de cada cliente

    Args:
        df: DataFrame con métricas por cliente
        total: Total de ventas global

    Returns:
        Diccionario con el reporte detallado

    Examples:
        >>> df = pd.DataFrame({
        ...     'cliente_id': ['C001', 'C002'],
        ...     'nombre': ['Alice', 'Bob'],
        ...     'total_ventas': [3600.0, 255.0]
        ... })
        >>> reporte = generar_reporte_detallado(df, 3855.0)
        >>> reporte['tipo']
        'detallado'
    """
    clientes = df.to_dict("records")

    reporte = {
        "tipo": "detallado",
        "total_ventas": total,
        "num_clientes": len(df),
        "clientes": clientes,
    }

    print(f"[REPORTE_DETALLADO] Generado con {len(df)} clientes")
    return reporte


def generar_reporte_simple(df: pd.DataFrame, total: float) -> dict:
    """
    Genera un reporte simple con métricas básicas.

    Incluye:
    - Tipo de reporte
    - Total de ventas
    - Número de clientes

    Args:
        df: DataFrame con métricas por cliente
        total: Total de ventas global

    Returns:
        Diccionario con el reporte simple

    Examples:
        >>> df = pd.DataFrame({
        ...     'cliente_id': ['C001', 'C002'],
        ...     'total_ventas': [3600.0, 255.0]
        ... })
        >>> reporte = generar_reporte_simple(df, 3855.0)
        >>> reporte['tipo']
        'simple'
    """
    reporte = {
        "tipo": "simple",
        "total_ventas": total,
        "num_clientes": len(df),
    }

    print(f"[REPORTE_SIMPLE] Generado con {len(df)} clientes")
    return reporte


def exportar_reporte_csv(df: pd.DataFrame, ruta: str) -> None:
    """
    Exporta un DataFrame a formato CSV.

    Crea el directorio padre si no existe.

    Args:
        df: DataFrame a exportar
        ruta: Ruta donde guardar el archivo CSV

    Examples:
        >>> df = pd.DataFrame({'col': [1, 2, 3]})
        >>> exportar_reporte_csv(df, "/tmp/reporte.csv")
    """
    ruta_path = Path(ruta)

    # Crear directorio padre si no existe
    ruta_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(ruta_path, index=False)
    print(f"[EXPORTAR_CSV] Guardado en: {ruta}")


def exportar_reporte_json(reporte: dict, ruta: str) -> None:
    """
    Exporta un diccionario a formato JSON.

    Crea el directorio padre si no existe.

    Args:
        reporte: Diccionario a exportar
        ruta: Ruta donde guardar el archivo JSON

    Examples:
        >>> reporte = {'total': 3855.0, 'clientes': 2}
        >>> exportar_reporte_json(reporte, "/tmp/reporte.json")
    """
    ruta_path = Path(ruta)

    # Crear directorio padre si no existe
    ruta_path.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_path, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    print(f"[EXPORTAR_JSON] Guardado en: {ruta}")
