"""
Tests para transformador Bronze → Silver.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import pandas as pd
import pytest

from src.transformador_bronze import (
    agregar_metricas_basicas,
    convertir_fechas,
    eliminar_registros_invalidos,
    limpiar_textos,
    normalizar_columnas,
    transformar_bronze_a_silver,
)


class TestLimpiarTextos:
    """Tests para limpieza de textos."""

    def test_elimina_espacios_extras(self):
        """Debe eliminar espacios al inicio y final."""
        df = pd.DataFrame({"texto": ["  Hola  ", "  Mundo  "]})

        df_limpio = limpiar_textos(df, ["texto"])

        assert df_limpio["texto"].tolist() == ["Hola", "Mundo"]

    def test_maneja_valores_nulos(self):
        """Debe manejar valores nulos sin error."""
        df = pd.DataFrame({"texto": [" Hola ", None, "  Mundo  "]})

        df_limpio = limpiar_textos(df, ["texto"])

        assert pd.isna(df_limpio.iloc[1]["texto"])
        assert df_limpio.iloc[0]["texto"] == "Hola"

    def test_multiples_columnas(self):
        """Debe limpiar múltiples columnas."""
        df = pd.DataFrame({"col1": [" A ", " B "], "col2": [" C ", " D "]})

        df_limpio = limpiar_textos(df, ["col1", "col2"])

        assert df_limpio["col1"].tolist() == ["A", "B"]
        assert df_limpio["col2"].tolist() == ["C", "D"]


class TestNormalizarColumnas:
    """Tests para normalización de columnas."""

    def test_renombra_columnas_correctamente(self):
        """Debe renombrar columnas según mapeo."""
        df = pd.DataFrame({"title": ["A"], "content": ["B"], "author": ["C"]})

        mapeo = {"title": "titulo", "content": "contenido", "author": "autor"}

        df_normalizado = normalizar_columnas(df, mapeo)

        assert "titulo" in df_normalizado.columns
        assert "contenido" in df_normalizado.columns
        assert "autor" in df_normalizado.columns
        assert "title" not in df_normalizado.columns

    def test_mantiene_columnas_no_mapeadas(self):
        """Debe mantener columnas que no están en el mapeo."""
        df = pd.DataFrame({"title": ["A"], "extra": ["X"]})

        mapeo = {"title": "titulo"}

        df_normalizado = normalizar_columnas(df, mapeo)

        assert "titulo" in df_normalizado.columns
        assert "extra" in df_normalizado.columns


class TestConvertirFechas:
    """Tests para conversión de fechas."""

    def test_convierte_strings_a_datetime(self):
        """Debe convertir strings de fecha a datetime."""
        df = pd.DataFrame({"fecha": ["2024-01-15 10:30:00", "2024-01-16 14:00:00"]})

        df_convertido = convertir_fechas(df, "fecha")

        assert pd.api.types.is_datetime64_any_dtype(df_convertido["fecha"])

    def test_maneja_fechas_invalidas_como_nat(self):
        """Fechas inválidas deben convertirse a NaT."""
        df = pd.DataFrame(
            {"fecha": ["2024-01-15 10:30:00", "invalid_date", "2024-01-16"]}
        )

        df_convertido = convertir_fechas(df, "fecha")

        assert pd.api.types.is_datetime64_any_dtype(df_convertido["fecha"])
        assert pd.isna(df_convertido.iloc[1]["fecha"])

    def test_mantiene_nulos_como_nat(self):
        """Valores None deben mantenerse como NaT."""
        df = pd.DataFrame({"fecha": ["2024-01-15 10:30:00", None]})

        df_convertido = convertir_fechas(df, "fecha")

        assert pd.isna(df_convertido.iloc[1]["fecha"])


class TestEliminarRegistrosInvalidos:
    """Tests para eliminación de registros inválidos."""

    def test_elimina_registros_con_nulos_en_columnas_criticas(self):
        """Debe eliminar registros con nulos en columnas críticas."""
        df = pd.DataFrame(
            {
                "id": [1, 2, None, 4],
                "titulo": ["A", "B", "C", "D"],
                "fecha": pd.to_datetime(
                    ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
                ),
            }
        )

        df_limpio = eliminar_registros_invalidos(df, ["id"])

        assert len(df_limpio) == 3
        assert 3 not in df_limpio["id"].values

    def test_elimina_registros_con_fechas_invalidas(self):
        """Debe eliminar registros con fechas NaT."""
        df = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "fecha": pd.to_datetime(["2024-01-01", None, "2024-01-03"]),
            }
        )

        df_limpio = eliminar_registros_invalidos(df, ["fecha"])

        assert len(df_limpio) == 2

    def test_multiples_columnas_criticas(self):
        """Debe validar múltiples columnas críticas."""
        df = pd.DataFrame({"id": [1, None, 3], "titulo": ["A", "B", None]})

        df_limpio = eliminar_registros_invalidos(df, ["id", "titulo"])

        assert len(df_limpio) == 1
        assert df_limpio.iloc[0]["id"] == 1


class TestAgregarMetricasBasicas:
    """Tests para agregar métricas básicas."""

    def test_agrega_longitud_contenido(self):
        """Debe agregar columna con longitud del contenido."""
        df = pd.DataFrame({"contenido": ["Hola", "Hola mundo", "Test"]})

        df_con_metricas = agregar_metricas_basicas(df, "contenido", "titulo")

        assert "longitud_contenido" in df_con_metricas.columns
        assert df_con_metricas["longitud_contenido"].tolist() == [4, 10, 4]

    def test_agrega_longitud_titulo(self):
        """Debe agregar columna con longitud del título."""
        df = pd.DataFrame({"titulo": ["Hola", "Test", "Ejemplo largo"]})

        df_con_metricas = agregar_metricas_basicas(df, "contenido", "titulo")

        assert "longitud_titulo" in df_con_metricas.columns
        assert df_con_metricas.iloc[2]["longitud_titulo"] == 13

    def test_maneja_valores_nulos(self):
        """Debe manejar valores nulos sin error."""
        df = pd.DataFrame({"contenido": ["Hola", None], "titulo": [None, "Test"]})

        df_con_metricas = agregar_metricas_basicas(df, "contenido", "titulo")

        assert "longitud_contenido" in df_con_metricas.columns
        assert "longitud_titulo" in df_con_metricas.columns


class TestTransformarBronzeASilver:
    """Tests para transformación completa Bronze → Silver."""

    def test_transforma_correctamente(self, df_noticias_bronze):
        """Debe transformar DataFrame Bronze a Silver."""
        df_silver = transformar_bronze_a_silver(df_noticias_bronze)

        # Verificar que tiene columnas en español
        assert "titulo" in df_silver.columns
        assert "contenido" in df_silver.columns
        assert "autor" in df_silver.columns

        # Verificar que fechas son datetime
        assert pd.api.types.is_datetime64_any_dtype(df_silver["fecha_publicacion"])

        # Verificar que registros inválidos fueron eliminados
        assert len(df_silver) < len(df_noticias_bronze)

    def test_agrega_metricas(self, df_noticias_bronze):
        """Debe agregar métricas de longitud."""
        df_silver = transformar_bronze_a_silver(df_noticias_bronze)

        assert "longitud_contenido" in df_silver.columns
        assert "longitud_titulo" in df_silver.columns

    def test_dataframe_vacio_levanta_error(self):
        """DataFrame vacío debe levantar ValueError."""
        df_vacio = pd.DataFrame()

        with pytest.raises(ValueError, match="vacío"):
            transformar_bronze_a_silver(df_vacio)
