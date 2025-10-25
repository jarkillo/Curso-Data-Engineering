"""
Módulo de detección de anomalías

Detecta caídas significativas en las ventas comparadas con el promedio histórico.

Regla de negocio:
- Si las ventas actuales son X% menores que el promedio histórico,
  se considera una anomalía que requiere investigación.
"""

from typing import Dict, List


def detectar_caida_ventas(
    total_actual: float, total_historico: float, umbral: float = 0.3
) -> Dict:
    """
    Detecta si hay una caída significativa en las ventas.

    Args:
        total_actual: Total de ventas del día actual
        total_historico: Promedio histórico de ventas
        umbral: Porcentaje de caída para considerar anomalía (default: 0.3 = 30%)

    Returns:
        dict: Resultado de la detección con estructura:
            {
                "anomalia": bool,
                "porcentaje_caida": float,
                "mensaje": str,
                "total_actual": float,
                "total_historico": float
            }

    Raises:
        ValueError: Si total_historico es cero

    Examples:
        >>> detectar_caida_ventas(700.0, 1000.0, umbral=0.3)
        {"anomalia": False, "porcentaje_caida": 0.3, ...}

        >>> detectar_caida_ventas(600.0, 1000.0, umbral=0.3)
        {"anomalia": True, "porcentaje_caida": 0.4, ...}
    """
    if total_historico <= 0:
        raise ValueError(
            "El total histórico no puede ser cero o negativo. "
            "Necesitas datos históricos válidos para detectar anomalías."
        )

    # Calcular porcentaje de caída
    diferencia = total_historico - total_actual
    porcentaje_caida = diferencia / total_historico

    # Detectar si es anomalía (caída > umbral)
    es_anomalia = porcentaje_caida > umbral

    # Construir mensaje
    if es_anomalia:
        mensaje = (
            f"⚠️  ANOMALÍA DETECTADA: Caída del {porcentaje_caida*100:.1f}% en ventas. "
            f"Actual: ${total_actual:,.2f} vs Histórico: ${total_historico:,.2f}"
        )
    else:
        mensaje = (
            f"✅ Ventas normales. "
            f"Actual: ${total_actual:,.2f} vs Histórico: ${total_historico:,.2f}"
        )

    resultado = {
        "anomalia": es_anomalia,
        "porcentaje_caida": porcentaje_caida,
        "mensaje": mensaje,
        "total_actual": total_actual,
        "total_historico": total_historico,
        "umbral": umbral,
    }

    print(mensaje)

    return resultado


def calcular_promedio_historico(fechas: List[str]) -> float:
    """
    Calcula el promedio histórico de ventas basado en una lista de fechas.

    Lee los archivos CSV de las fechas especificadas y calcula el promedio
    de ventas totales.

    Args:
        fechas: Lista de fechas en formato YYYY-MM-DD

    Returns:
        float: Promedio de ventas totales

    Raises:
        ValueError: Si la lista está vacía o no se pueden leer los archivos

    Examples:
        >>> fechas = ["2025-10-20", "2025-10-21", "2025-10-22"]
        >>> promedio = calcular_promedio_historico(fechas)
        >>> promedio
        1250.50
    """
    if not fechas:
        raise ValueError(
            "La lista de fechas no puede estar vacía para calcular promedio histórico"
        )

    totales = []

    # Importar aquí para evitar dependencia circular
    from src.extraccion import extraer_ventas_csv, obtener_ruta_archivo

    for fecha in fechas:
        try:
            ruta = obtener_ruta_archivo(fecha)
            df = extraer_ventas_csv(ruta)
            total = df["total"].sum()
            totales.append(total)
        except FileNotFoundError:
            print(f"⚠️  Archivo para fecha {fecha} no encontrado, omitiendo...")
            continue
        except Exception as e:
            print(f"⚠️  Error al procesar fecha {fecha}: {str(e)}")
            continue

    if not totales:
        raise ValueError(
            "No se pudieron leer datos históricos. "
            "Verifica que los archivos de las fechas especificadas existan."
        )

    promedio = sum(totales) / len(totales)

    print(
        f"📈 Promedio histórico calculado: ${promedio:,.2f} "
        f"(basado en {len(totales)} días)"
    )

    return float(promedio)
