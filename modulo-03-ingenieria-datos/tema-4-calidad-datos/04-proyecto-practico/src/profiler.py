"""Módulo de Data Profiling y Análisis de Calidad."""

import numpy as np
import pandas as pd


def generar_perfil_basico(df: pd.DataFrame) -> dict:
    """Estadísticas descriptivas básicas por columna."""
    if df.empty:
        raise ValueError("DataFrame está vacío")

    perfil = {
        "num_registros": len(df),
        "num_columnas": len(df.columns),
        "memoria_mb": round(df.memory_usage(deep=True).sum() / (1024**2), 2),
        "columnas": {},
    }

    for col in df.columns:
        perfil["columnas"][col] = {
            "tipo": str(df[col].dtype),
            "nulos": int(df[col].isnull().sum()),
            "porcentaje_nulos": round(df[col].isnull().mean() * 100, 2),
            "unicos": int(df[col].nunique()),
            "duplicados": int(df[col].duplicated().sum()),
        }

        if pd.api.types.is_numeric_dtype(df[col]):
            perfil["columnas"][col].update(
                {
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "media": float(df[col].mean()),
                    "mediana": float(df[col].median()),
                    "std": float(df[col].std()),
                }
            )

    return perfil


def generar_perfil_completo(
    df: pd.DataFrame, archivo_salida: str | None = None
) -> dict:
    """
    Análisis completo de calidad.

    Args:
        archivo_salida: Ruta para guardar reporte HTML (opcional)
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    perfil = generar_perfil_basico(df)

    # Si se especifica archivo, generar reporte HTML con ydata-profiling
    if archivo_salida:
        try:
            from ydata_profiling import ProfileReport

            profile = ProfileReport(df, title="Reporte de Calidad", minimal=True)
            profile.to_file(archivo_salida)
        except ImportError:
            pass  # ydata-profiling es opcional

    return perfil


def detectar_correlaciones(df: pd.DataFrame, umbral: float = 0.7) -> pd.DataFrame:
    """Identifica variables altamente correlacionadas."""
    if df.empty:
        raise ValueError("DataFrame está vacío")

    df_numerico = df.select_dtypes(include=[np.number])

    if df_numerico.empty:
        return pd.DataFrame(columns=["variable1", "variable2", "correlacion"])

    correlaciones = df_numerico.corr()

    pares_alta_corr = []

    for i in range(len(correlaciones.columns)):
        for j in range(i + 1, len(correlaciones.columns)):
            col1 = correlaciones.columns[i]
            col2 = correlaciones.columns[j]
            valor = correlaciones.iloc[i, j]

            if abs(valor) >= umbral:
                pares_alta_corr.append(
                    {
                        "variable1": col1,
                        "variable2": col2,
                        "correlacion": round(valor, 3),
                    }
                )

    return pd.DataFrame(pares_alta_corr)


def generar_reporte_calidad(df: pd.DataFrame) -> dict:
    """Dashboard completo con todas las métricas de calidad."""
    if df.empty:
        raise ValueError("DataFrame está vacío")

    perfil = generar_perfil_basico(df)

    # Completitud
    total_celdas = len(df) * len(df.columns)
    celdas_vacias = df.isnull().sum().sum()

    completitud = {
        "total_celdas": total_celdas,
        "celdas_vacias": int(celdas_vacias),
        "porcentaje_global": round((1 - celdas_vacias / total_celdas) * 100, 2),
    }

    # Duplicados
    duplicados = {
        "registros_duplicados": int(df.duplicated().sum()),
        "porcentaje": round((df.duplicated().sum() / len(df)) * 100, 2),
    }

    # Correlaciones
    correlaciones_altas = detectar_correlaciones(df, umbral=0.7)

    reporte = {
        "perfil_basico": perfil,
        "completitud": completitud,
        "duplicados": duplicados,
        "correlaciones_altas": len(correlaciones_altas),
    }

    return reporte
