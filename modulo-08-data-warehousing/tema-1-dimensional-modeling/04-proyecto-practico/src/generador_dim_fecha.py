"""
Generador de Dimensión de Fecha (DimFecha).

Este módulo genera una tabla de dimensión de fecha pre-calculada con todos
los atributos necesarios para análisis temporal en un data warehouse.

Funciones:
    generar_dim_fecha: Genera DimFecha para un rango de fechas
"""

from datetime import datetime
from typing import Optional

import pandas as pd


def generar_dim_fecha(
    fecha_inicio: str, fecha_fin: str, festivos: Optional[list[dict[str, str]]] = None
) -> pd.DataFrame:
    """
    Genera tabla de dimensión de fecha pre-calculada.

    Args:
        fecha_inicio: Fecha inicial en formato 'YYYY-MM-DD'
        fecha_fin: Fecha final en formato 'YYYY-MM-DD'
        festivos: Lista opcional de festivos
                  [{'fecha': '2024-01-01', 'nombre': 'Año Nuevo'}, ...]

    Returns:
        DataFrame con DimFecha completa con columnas:
            - fecha_id (int): Formato YYYYMMDD
            - fecha_completa (date): Fecha completa
            - dia (int): Día del mes (1-31)
            - mes (int): Mes (1-12)
            - mes_nombre (str): Nombre del mes en español
            - trimestre (int): Trimestre (1-4)
            - anio (int): Año
            - dia_semana (str): Nombre del día en español
            - numero_dia_semana (int): Número de día (0=Lunes, 6=Domingo)
            - numero_semana (int): Número de semana del año
            - es_fin_de_semana (bool): True si es sábado o domingo
            - es_dia_festivo (bool): True si es día festivo
            - nombre_festivo (str|None): Nombre del festivo o None

    Raises:
        ValueError: Si fecha_inicio > fecha_fin o formato inválido

    Examples:
        >>> dim_fecha = generar_dim_fecha('2024-01-01', '2024-12-31')
        >>> print(dim_fecha.shape)
        (366, 13)  # 366 días (año bisiesto), 13 columnas

        >>> festivos = [{'fecha': '2024-01-01', 'nombre': 'Año Nuevo'}]
        >>> dim_fecha = generar_dim_fecha('2024-01-01', '2024-01-31', festivos)
        >>> print(dim_fecha[dim_fecha['es_dia_festivo']].shape)
        (1, 13)  # Solo un festivo
    """
    # Validar formato de fechas
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(
            f"Formato de fecha inválido. Use 'YYYY-MM-DD'. Error: {e}"
        ) from e

    # Validar que fecha_inicio < fecha_fin
    if fecha_inicio_dt > fecha_fin_dt:
        raise ValueError(
            "fecha_inicio debe ser menor o igual que fecha_fin. "
            f"Recibido: {fecha_inicio} > {fecha_fin}"
        )

    # Generar rango de fechas
    fechas = pd.date_range(start=fecha_inicio_dt, end=fecha_fin_dt, freq="D")

    # Crear DataFrame base
    dim_fecha = pd.DataFrame({"fecha_completa": fechas})

    # Generar fecha_id (formato: YYYYMMDD)
    dim_fecha["fecha_id"] = (
        dim_fecha["fecha_completa"].dt.strftime("%Y%m%d").astype(int)
    )

    # Extraer componentes de fecha
    dim_fecha["dia"] = dim_fecha["fecha_completa"].dt.day
    dim_fecha["mes"] = dim_fecha["fecha_completa"].dt.month
    dim_fecha["anio"] = dim_fecha["fecha_completa"].dt.year

    # Nombres de mes en español
    meses_es = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }
    dim_fecha["mes_nombre"] = dim_fecha["mes"].map(meses_es)

    # Trimestre
    dim_fecha["trimestre"] = dim_fecha["fecha_completa"].dt.quarter

    # Día de semana
    dias_semana_es = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo",
    }
    dim_fecha["numero_dia_semana"] = dim_fecha["fecha_completa"].dt.dayofweek
    dim_fecha["dia_semana"] = dim_fecha["numero_dia_semana"].map(dias_semana_es)

    # Número de semana del año
    dim_fecha["numero_semana"] = dim_fecha["fecha_completa"].dt.isocalendar().week

    # Es fin de semana (Sábado=5, Domingo=6)
    dim_fecha["es_fin_de_semana"] = dim_fecha["numero_dia_semana"].isin([5, 6])

    # Días festivos
    dim_fecha["es_dia_festivo"] = False
    dim_fecha["nombre_festivo"] = None

    if festivos:
        for festivo in festivos:
            try:
                fecha_festivo = datetime.strptime(festivo["fecha"], "%Y-%m-%d")
            except (KeyError, ValueError):
                # Si el festivo tiene formato incorrecto, lo saltamos
                continue

            mask = dim_fecha["fecha_completa"] == fecha_festivo
            dim_fecha.loc[mask, "es_dia_festivo"] = True
            dim_fecha.loc[mask, "nombre_festivo"] = festivo["nombre"]

    # Ordenar columnas
    dim_fecha = dim_fecha[
        [
            "fecha_id",
            "fecha_completa",
            "dia",
            "mes",
            "mes_nombre",
            "trimestre",
            "anio",
            "dia_semana",
            "numero_dia_semana",
            "numero_semana",
            "es_fin_de_semana",
            "es_dia_festivo",
            "nombre_festivo",
        ]
    ]

    return dim_fecha
