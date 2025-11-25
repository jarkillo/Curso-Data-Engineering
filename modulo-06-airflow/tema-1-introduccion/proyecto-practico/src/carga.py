"""
Módulo de carga/guardado de reportes

Funciones para guardar reportes de ventas en diferentes formatos.

Formatos soportados:
- CSV: Para análisis posterior en Excel/Python
- TXT: Para lectura humana directa
"""

from datetime import datetime
from pathlib import Path

import pandas as pd


def guardar_reporte_csv(metricas: dict, fecha: str, directorio_base: str = None) -> str:
    """
    Guarda un reporte de métricas en formato CSV.

    Args:
        metricas: Dict con métricas calculadas
        fecha: Fecha del reporte en formato YYYY-MM-DD
        directorio_base: Directorio base donde guardar (opcional)

    Returns:
        str: Ruta del archivo guardado

    Examples:
        >>> metricas = {"total_ventas": 1250.50, "ticket_promedio": 208.42}
        >>> ruta = guardar_reporte_csv(metricas, "2025-10-25")
        >>> print(ruta)
        'data/output/reporte_2025_10_25.csv'
    """
    # Determinar directorio
    if directorio_base is None:
        directorio_base = Path(__file__).parent.parent / "data" / "output"
    else:
        directorio_base = Path(directorio_base)

    # Crear directorio si no existe
    directorio_base.mkdir(parents=True, exist_ok=True)

    # Construir nombre de archivo
    fecha_formato = fecha.replace("-", "_")
    nombre_archivo = f"reporte_{fecha_formato}.csv"
    ruta_completa = directorio_base / nombre_archivo

    # Convertir métricas a DataFrame
    # Aplanar top_productos si existe
    metricas_flat = metricas.copy()
    if "top_productos" in metricas_flat and isinstance(
        metricas_flat["top_productos"], list
    ):
        # Extraer top 3 productos como columnas separadas
        top_productos = metricas_flat.pop("top_productos")
        for i, producto in enumerate(top_productos[:3], 1):
            metricas_flat[f"top{i}_producto"] = producto.get("producto", "")
            metricas_flat[f"top{i}_cantidad"] = producto.get("cantidad", 0)

    # Crear DataFrame
    df = pd.DataFrame([metricas_flat])

    # Guardar CSV
    df.to_csv(ruta_completa, index=False)

    print(f"💾 Reporte CSV guardado en: {ruta_completa}")

    return str(ruta_completa)


def guardar_reporte_txt(metricas: dict, fecha: str, directorio_base: str = None) -> str:
    """
    Guarda un reporte de métricas en formato TXT legible.

    Args:
        metricas: Dict con métricas calculadas
        fecha: Fecha del reporte en formato YYYY-MM-DD
        directorio_base: Directorio base donde guardar (opcional)

    Returns:
        str: Ruta del archivo guardado

    Examples:
        >>> metricas = {"total_ventas": 1250.50}
        >>> ruta = guardar_reporte_txt(metricas, "2025-10-25")
        >>> print(ruta)
        'data/output/reporte_2025_10_25.txt'
    """
    # Determinar directorio
    if directorio_base is None:
        directorio_base = Path(__file__).parent.parent / "data" / "output"
    else:
        directorio_base = Path(directorio_base)

    # Crear directorio si no existe
    directorio_base.mkdir(parents=True, exist_ok=True)

    # Construir nombre de archivo
    fecha_formato = fecha.replace("-", "_")
    nombre_archivo = f"reporte_{fecha_formato}.txt"
    ruta_completa = directorio_base / nombre_archivo

    # Construir contenido del reporte
    contenido = []
    contenido.append("=" * 60)
    contenido.append("    REPORTE DE VENTAS - CLOUDMART")
    contenido.append("=" * 60)
    contenido.append(f"Fecha: {fecha}")
    contenido.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    contenido.append("=" * 60)
    contenido.append("")

    # Métricas principales
    contenido.append("MÉTRICAS PRINCIPALES")
    contenido.append("-" * 60)

    if "total_ventas" in metricas:
        contenido.append(f"Total de Ventas:      ${metricas['total_ventas']:>15,.2f}")

    if "ticket_promedio" in metricas:
        contenido.append(
            f"Ticket Promedio:      ${metricas['ticket_promedio']:>15,.2f}"
        )

    if "cantidad_ventas" in metricas:
        contenido.append(f"Cantidad de Ventas:   {metricas['cantidad_ventas']:>18}")

    # Top productos
    if "top_productos" in metricas and metricas["top_productos"]:
        contenido.append("")
        contenido.append("TOP 5 PRODUCTOS MÁS VENDIDOS")
        contenido.append("-" * 60)

        for i, producto in enumerate(metricas["top_productos"], 1):
            nombre = producto.get("producto", "N/A")
            cantidad = producto.get("cantidad", 0)
            contenido.append(f"{i}. {nombre:<40} {cantidad:>5} unidades")

    contenido.append("")
    contenido.append("=" * 60)
    contenido.append("Fin del Reporte")
    contenido.append("=" * 60)

    # Guardar archivo
    with open(ruta_completa, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))

    print(f"📄 Reporte TXT guardado en: {ruta_completa}")

    return str(ruta_completa)
