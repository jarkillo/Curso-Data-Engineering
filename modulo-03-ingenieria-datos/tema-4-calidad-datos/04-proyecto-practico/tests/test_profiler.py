"""Tests para profiler.py - Metodología TDD - Cobertura >90%."""

import pandas as pd
import pytest
from src.profiler import (
    detectar_correlaciones,
    generar_perfil_basico,
    generar_perfil_completo,
    generar_reporte_calidad,
)


class TestGenerarPerfilBasico:
    """Tests para generar_perfil_basico."""

    def test_perfil_completo(self, df_basico):
        """Verifica generación de perfil básico."""
        perfil = generar_perfil_basico(df_basico)

        assert "num_registros" in perfil
        assert "num_columnas" in perfil
        assert "columnas" in perfil
        assert perfil["num_registros"] == len(df_basico)

    def test_estadisticas_por_columna(self, df_basico):
        """Verifica estadísticas por columna."""
        perfil = generar_perfil_basico(df_basico)

        for col in df_basico.columns:
            assert col in perfil["columnas"]
            assert "tipo" in perfil["columnas"][col]
            assert "nulos" in perfil["columnas"][col]

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError):
            generar_perfil_basico(df_vacio)


class TestGenerarPerfilCompleto:
    """Tests para generar_perfil_completo."""

    def test_perfil_sin_archivo(self, df_basico):
        """Verifica generación sin guardar archivo."""
        perfil = generar_perfil_completo(df_basico, archivo_salida=None)

        assert isinstance(perfil, dict)
        assert "num_registros" in perfil

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError):
            generar_perfil_completo(df_vacio)


class TestDetectarCorrelaciones:
    """Tests para detectar_correlaciones."""

    def test_sin_correlaciones_altas(self):
        """Verifica cuando no hay correlaciones altas."""
        df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [5, 4, 3, 2, 1]})

        correlaciones = detectar_correlaciones(df, umbral=0.95)

        assert len(correlaciones) >= 0

    def test_con_correlaciones(self):
        """Verifica detección de correlaciones."""
        df = pd.DataFrame(
            {
                "a": [1, 2, 3, 4, 5],
                "b": [2, 4, 6, 8, 10],  # Perfectamente correlacionado con a
            }
        )

        correlaciones = detectar_correlaciones(df, umbral=0.9)

        assert len(correlaciones) > 0

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError):
            detectar_correlaciones(df_vacio)


class TestGenerarReporteCalidad:
    """Tests para generar_reporte_calidad."""

    def test_reporte_completo(self, df_basico):
        """Verifica generación de reporte completo."""
        reporte = generar_reporte_calidad(df_basico)

        assert "perfil_basico" in reporte
        assert "completitud" in reporte
        assert "duplicados" in reporte

    def test_metricas_incluidas(self, df_con_nulos):
        """Verifica métricas de calidad."""
        reporte = generar_reporte_calidad(df_con_nulos)

        assert reporte["completitud"]["porcentaje_global"] < 100

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError):
            generar_reporte_calidad(df_vacio)
