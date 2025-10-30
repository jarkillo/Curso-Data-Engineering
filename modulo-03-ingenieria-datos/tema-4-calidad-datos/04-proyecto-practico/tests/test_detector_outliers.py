"""Tests para detector_outliers.py - Metodología TDD - Cobertura >90%."""

import numpy as np
import pandas as pd
import pytest
from src.detector_outliers import (
    detectar_outliers_iqr,
    detectar_outliers_isolation_forest,
    detectar_outliers_zscore,
    generar_reporte_outliers,
    tratar_outliers,
    visualizar_outliers,
)


class TestDetectarOutliersIQR:
    """Tests para detectar_outliers_iqr."""

    def test_sin_outliers(self):
        """Verifica cuando no hay outliers."""
        np.random.seed(42)
        df = pd.DataFrame({"valores": np.random.normal(100, 10, 100)})

        outliers, stats = detectar_outliers_iqr(df, "valores")

        assert outliers.sum() <= 5  # Máximo 5% esperado por ruido

    def test_con_outliers_conocidos(self, df_con_outliers):
        """Verifica detección de outliers conocidos."""
        outliers, stats = detectar_outliers_iqr(df_con_outliers, "valor")

        assert outliers.sum() > 0
        assert "Q1" in stats
        assert "Q3" in stats
        assert "IQR" in stats

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            detectar_outliers_iqr(df_vacio, "valores")

    def test_columna_no_numerica(self, df_basico):
        """Verifica que falla con columna no numérica."""
        with pytest.raises(TypeError, match="numéric"):
            detectar_outliers_iqr(df_basico, "nombre")


class TestDetectarOutliersZScore:
    """Tests para detectar_outliers_zscore."""

    def test_con_outliers(self, df_con_outliers):
        """Verifica detección con Z-score."""
        outliers, stats = detectar_outliers_zscore(df_con_outliers, "valor", umbral=3.0)

        assert outliers.sum() > 0
        assert "media" in stats
        assert "std" in stats

    def test_umbral_personalizado(self, df_con_outliers):
        """Verifica funcionamiento con umbrales diferentes."""
        outliers_3 = detectar_outliers_zscore(df_con_outliers, "valor", umbral=3.0)[0]
        outliers_2 = detectar_outliers_zscore(df_con_outliers, "valor", umbral=2.0)[0]

        assert outliers_2.sum() >= outliers_3.sum()

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError):
            detectar_outliers_zscore(df_vacio, "valores")


class TestDetectarOutliersIsolationForest:
    """Tests para detectar_outliers_isolation_forest."""

    def test_deteccion_multivariada(self, df_multivariado):
        """Verifica detección multivariada."""
        outliers = detectar_outliers_isolation_forest(
            df_multivariado, ["precio", "cantidad"], contamination=0.05
        )

        assert outliers.sum() > 0
        assert isinstance(outliers, pd.Series)

    def test_columnas_no_numericas(self, df_basico):
        """Verifica que falla con columnas no numéricas."""
        with pytest.raises(TypeError):
            detectar_outliers_isolation_forest(df_basico, ["nombre"])

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError):
            detectar_outliers_isolation_forest(df_vacio, ["valores"])


class TestTratarOutliers:
    """Tests para tratar_outliers."""

    def test_tratamiento_eliminar(self, df_con_outliers):
        """Verifica eliminación de outliers."""
        outliers, _ = detectar_outliers_iqr(df_con_outliers, "valor")
        df_tratado = tratar_outliers(
            df_con_outliers, "valor", outliers, metodo="eliminar"
        )

        assert len(df_tratado) < len(df_con_outliers)
        assert len(df_tratado) == len(df_con_outliers) - outliers.sum()

    def test_tratamiento_imputar(self, df_con_outliers):
        """Verifica imputación de outliers."""
        outliers, _ = detectar_outliers_iqr(df_con_outliers, "valor")
        df_tratado = tratar_outliers(
            df_con_outliers, "valor", outliers, metodo="imputar"
        )

        assert len(df_tratado) == len(df_con_outliers)
        # Valores extremos deben ser reemplazados
        assert df_tratado["valor"].max() < df_con_outliers["valor"].max()

    def test_tratamiento_capping(self):
        """Verifica capping de outliers."""
        df = pd.DataFrame({"valor": [1, 2, 3, 4, 5, 100]})
        outliers = pd.Series([False, False, False, False, False, True])

        df_tratado = tratar_outliers(df, "valor", outliers, metodo="capping")

        assert len(df_tratado) == len(df)
        assert df_tratado["valor"].max() < 100

    def test_metodo_invalido(self, df_con_outliers):
        """Verifica manejo de método inválido."""
        outliers, _ = detectar_outliers_iqr(df_con_outliers, "valor")

        with pytest.raises(ValueError, match="Método"):
            tratar_outliers(df_con_outliers, "valor", outliers, metodo="invalido")


class TestVisualizarOutliers:
    """Tests para visualizar_outliers."""

    def test_genera_archivo(self, df_con_outliers, tmp_path):
        """Verifica que genera archivo de imagen."""
        archivo_salida = tmp_path / "outliers.png"

        visualizar_outliers(df_con_outliers, "valor", str(archivo_salida))

        assert archivo_salida.exists()

    def test_columna_no_numerica(self, df_basico, tmp_path):
        """Verifica que falla con columna no numérica."""
        archivo_salida = tmp_path / "outliers.png"

        with pytest.raises(TypeError):
            visualizar_outliers(df_basico, "nombre", str(archivo_salida))


class TestGenerarReporteOutliers:
    """Tests para generar_reporte_outliers."""

    def test_reporte_completo(self, df_multivariado):
        """Verifica generación de reporte completo."""
        reporte = generar_reporte_outliers(df_multivariado, ["precio", "cantidad"])

        assert "precio" in reporte
        assert "cantidad" in reporte
        assert "outliers_iqr" in reporte["precio"]
        assert "outliers_zscore" in reporte["precio"]

    def test_estadisticas_incluidas(self, df_con_outliers):
        """Verifica que incluye estadísticas necesarias."""
        reporte = generar_reporte_outliers(df_con_outliers, ["valor"])

        assert "outliers_iqr" in reporte["valor"]
        assert "porcentaje_iqr" in reporte["valor"]

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError):
            generar_reporte_outliers(df_vacio, ["valor"])
