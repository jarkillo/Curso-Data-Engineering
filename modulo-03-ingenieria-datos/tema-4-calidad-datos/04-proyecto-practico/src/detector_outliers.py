"""Módulo de Detección y Tratamiento de Outliers."""

from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def detectar_outliers_iqr(df: pd.DataFrame, columna: str) -> Tuple[pd.Series, Dict]:
    """
    Detecta outliers usando método IQR.

    Returns:
        Tupla (serie booleana de outliers, diccionario con estadísticas)
    """
    if df.empty:
        raise ValueError("DataFrame está vacío")

    if columna not in df.columns:
        raise KeyError(f"Columna '{columna}' no existe")

    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise TypeError(f"Columna '{columna}' debe ser numérica")

    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    outliers = (df[columna] < limite_inferior) | (df[columna] > limite_superior)

    stats = {
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "outliers_count": outliers.sum(),
        "outliers_percentage": (outliers.sum() / len(df)) * 100,
    }

    return outliers, stats


def detectar_outliers_zscore(
    df: pd.DataFrame, columna: str, umbral: float = 3.0
) -> Tuple[pd.Series, Dict]:
    """Detecta outliers usando Z-score."""
    if df.empty:
        raise ValueError("DataFrame está vacío")

    if columna not in df.columns:
        raise KeyError(f"Columna '{columna}' no existe")

    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise TypeError(f"Columna '{columna}' debe ser numérica")

    media = df[columna].mean()
    std = df[columna].std()

    z_scores = np.abs((df[columna] - media) / std)
    outliers = z_scores > umbral

    stats = {
        "media": media,
        "std": std,
        "umbral_zscore": umbral,
        "outliers_count": outliers.sum(),
        "outliers_percentage": (outliers.sum() / len(df)) * 100,
        "max_zscore": z_scores.max(),
    }

    return outliers, stats


def detectar_outliers_isolation_forest(
    df: pd.DataFrame, columnas: List[str], contamination: float = 0.1
) -> pd.Series:
    """Detecta outliers multivariados con Isolation Forest."""
    if df.empty:
        raise ValueError("DataFrame está vacío")

    for col in columnas:
        if col not in df.columns:
            raise KeyError(f"Columna '{col}' no existe")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise TypeError(f"Columna '{col}' debe ser numérica")

    X = df[columnas].fillna(df[columnas].median())

    clf = IsolationForest(contamination=contamination, random_state=42)
    predicciones = clf.fit_predict(X)

    outliers = pd.Series(predicciones == -1, index=df.index)

    return outliers


def tratar_outliers(
    df: pd.DataFrame, columna: str, outliers: pd.Series, metodo: str = "eliminar"
) -> pd.DataFrame:
    """
    Aplica tratamiento a outliers.

    Args:
        metodo: 'eliminar', 'imputar', 'capping'
    """
    metodos_validos = ["eliminar", "imputar", "capping"]
    if metodo not in metodos_validos:
        raise ValueError(f"Método '{metodo}' no válido. Usar: {metodos_validos}")

    df_tratado = df.copy()

    if metodo == "eliminar":
        return df_tratado[~outliers].reset_index(drop=True)

    elif metodo == "imputar":
        mediana = df_tratado.loc[~outliers, columna].median()
        df_tratado.loc[outliers, columna] = mediana
        return df_tratado

    elif metodo == "capping":
        p05 = df_tratado[columna].quantile(0.05)
        p95 = df_tratado[columna].quantile(0.95)
        df_tratado[columna] = df_tratado[columna].clip(lower=p05, upper=p95)
        return df_tratado


def visualizar_outliers(df: pd.DataFrame, columna: str, archivo_salida: str) -> None:
    """Genera gráfico de análisis de outliers."""
    if columna not in df.columns:
        raise KeyError(f"Columna '{columna}' no existe")

    if not pd.api.types.is_numeric_dtype(df[columna]):
        raise TypeError(f"Columna '{columna}' debe ser numérica")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Boxplot
    axes[0].boxplot(df[columna].dropna())
    axes[0].set_title(f"Boxplot - {columna}")
    axes[0].set_ylabel("Valor")

    # Histograma
    axes[1].hist(df[columna].dropna(), bins=30, edgecolor="black")
    axes[1].set_title(f"Distribución - {columna}")
    axes[1].set_xlabel("Valor")
    axes[1].set_ylabel("Frecuencia")

    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=150, bbox_inches="tight")
    plt.close()


def generar_reporte_outliers(df: pd.DataFrame, columnas_numericas: List[str]) -> Dict:
    """Estadísticas de outliers por columna."""
    if df.empty:
        raise ValueError("DataFrame está vacío")

    reporte = {}

    for col in columnas_numericas:
        outliers_iqr, stats_iqr = detectar_outliers_iqr(df, col)
        outliers_zscore, stats_zscore = detectar_outliers_zscore(df, col)

        reporte[col] = {
            "outliers_iqr": int(outliers_iqr.sum()),
            "porcentaje_iqr": round((outliers_iqr.sum() / len(df)) * 100, 2),
            "outliers_zscore": int(outliers_zscore.sum()),
            "porcentaje_zscore": round((outliers_zscore.sum() / len(df)) * 100, 2),
            "limites_iqr": {
                "inferior": stats_iqr["limite_inferior"],
                "superior": stats_iqr["limite_superior"],
            },
        }

    return reporte
