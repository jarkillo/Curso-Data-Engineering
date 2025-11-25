"""
Tests para transformador Silver → Gold.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import pandas as pd
import pytest

from src.transformador_silver import (
    agregar_metricas_temporales,
    agregar_noticias_por_categoria,
    agregar_noticias_por_fuente,
    calcular_estadisticas_longitud,
    transformar_silver_a_gold,
)


class TestAgregarNoticiasPorFuente:
    """Tests para agregación por fuente."""

    def test_agrega_correctamente_por_fuente(self, df_noticias_silver):
        """Debe agregar noticias por fuente."""
        df_agg = agregar_noticias_por_fuente(df_noticias_silver)

        assert "fuente" in df_agg.columns
        assert "total_noticias" in df_agg.columns
        assert "longitud_promedio_contenido" in df_agg.columns

    def test_cuenta_total_correcto(self, df_noticias_silver):
        """Debe contar correctamente el total de noticias por fuente."""
        df_agg = agregar_noticias_por_fuente(df_noticias_silver)

        # Verificar que suma de totales es igual a filas originales
        assert df_agg["total_noticias"].sum() == len(df_noticias_silver)

    def test_calcula_promedios_correctos(self):
        """Debe calcular promedios correctamente."""
        df = pd.DataFrame(
            {
                "fuente": ["A", "A", "B"],
                "longitud_contenido": [10, 20, 30],
                "longitud_titulo": [5, 5, 10],
            }
        )

        df_agg = agregar_noticias_por_fuente(df)

        # Fuente A: promedio contenido = (10+20)/2 = 15
        fila_a = df_agg[df_agg["fuente"] == "A"].iloc[0]
        assert fila_a["longitud_promedio_contenido"] == 15.0


class TestAgregarNoticiasPorCategoria:
    """Tests para agregación por categoría."""

    def test_agrega_correctamente_por_categoria(self, df_noticias_silver):
        """Debe agregar noticias por categoría."""
        df_agg = agregar_noticias_por_categoria(df_noticias_silver)

        assert "categoria" in df_agg.columns
        assert "total_noticias" in df_agg.columns

    def test_ordena_por_total_descendente(self, df_noticias_silver):
        """Debe ordenar por total de noticias descendente."""
        df_agg = agregar_noticias_por_categoria(df_noticias_silver)

        # Verificar que está ordenado descendentemente
        assert df_agg["total_noticias"].is_monotonic_decreasing


class TestAgregarMetricasTemporales:
    """Tests para métricas temporales."""

    def test_agrega_fecha_sin_hora(self, df_noticias_silver):
        """Debe agregar columna de fecha sin hora."""
        df_temporal = agregar_metricas_temporales(df_noticias_silver)

        assert "fecha" in df_temporal.columns
        # Verificar que es solo fecha (sin hora)
        assert df_temporal["fecha"].dt.hour.sum() == 0

    def test_agrega_dia_semana(self, df_noticias_silver):
        """Debe agregar columna de día de la semana."""
        df_temporal = agregar_metricas_temporales(df_noticias_silver)

        assert "dia_semana" in df_temporal.columns
        # Día de semana debe ser 0-6
        assert df_temporal["dia_semana"].min() >= 0
        assert df_temporal["dia_semana"].max() <= 6

    def test_agrega_hora(self, df_noticias_silver):
        """Debe agregar columna de hora."""
        df_temporal = agregar_metricas_temporales(df_noticias_silver)

        assert "hora" in df_temporal.columns
        # Hora debe ser 0-23
        assert df_temporal["hora"].min() >= 0
        assert df_temporal["hora"].max() <= 23


class TestCalcularEstadisticasLongitud:
    """Tests para estadísticas de longitud."""

    def test_calcula_estadisticas_contenido(self):
        """Debe calcular estadísticas de longitud de contenido."""
        df = pd.DataFrame({"longitud_contenido": [10, 20, 30, 40, 50]})

        stats = calcular_estadisticas_longitud(df, "longitud_contenido")

        assert "min" in stats
        assert "max" in stats
        assert "mean" in stats
        assert "median" in stats
        assert stats["min"] == 10
        assert stats["max"] == 50
        assert stats["mean"] == 30.0

    def test_maneja_columna_inexistente(self):
        """Debe levantar error si columna no existe."""
        df = pd.DataFrame({"otra": [1, 2, 3]})

        with pytest.raises(KeyError):
            calcular_estadisticas_longitud(df, "longitud_inexistente")


class TestTransformarSilverAGold:
    """Tests para transformación completa Silver → Gold."""

    def test_transforma_correctamente(self, df_noticias_silver):
        """Debe transformar DataFrame Silver a Gold."""
        resultado = transformar_silver_a_gold(df_noticias_silver)

        assert "por_fuente" in resultado
        assert "por_categoria" in resultado
        assert "estadisticas" in resultado

    def test_por_fuente_es_dataframe(self, df_noticias_silver):
        """Resultado por_fuente debe ser DataFrame."""
        resultado = transformar_silver_a_gold(df_noticias_silver)

        assert isinstance(resultado["por_fuente"], pd.DataFrame)
        assert len(resultado["por_fuente"]) > 0

    def test_por_categoria_es_dataframe(self, df_noticias_silver):
        """Resultado por_categoria debe ser DataFrame."""
        resultado = transformar_silver_a_gold(df_noticias_silver)

        assert isinstance(resultado["por_categoria"], pd.DataFrame)
        assert len(resultado["por_categoria"]) > 0

    def test_estadisticas_es_dict(self, df_noticias_silver):
        """Resultado estadísticas debe ser diccionario."""
        resultado = transformar_silver_a_gold(df_noticias_silver)

        assert isinstance(resultado["estadisticas"], dict)
        assert "contenido" in resultado["estadisticas"]
        assert "titulo" in resultado["estadisticas"]

    def test_dataframe_vacio_levanta_error(self):
        """DataFrame vacío debe levantar ValueError."""
        df_vacio = pd.DataFrame()

        with pytest.raises(ValueError, match="vacío"):
            transformar_silver_a_gold(df_vacio)
