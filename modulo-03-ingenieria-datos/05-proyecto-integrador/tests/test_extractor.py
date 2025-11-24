"""
Tests para módulo de extracción de noticias.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import pandas as pd
import pytest

from src.extractor import (
    extraer_noticias_api_simulada,
    extraer_noticias_desde_parquet,
    guardar_en_bronze,
    normalizar_respuesta_api,
)


class TestExtraerNoticiasAPISimulada:
    """Tests para extracción de API simulada."""

    def test_extrae_noticias_simuladas_correctamente(self):
        """Debe generar DataFrame con noticias simuladas."""
        df = extraer_noticias_api_simulada(num_noticias=10)

        assert len(df) == 10
        assert "id" in df.columns
        assert "title" in df.columns
        assert "content" in df.columns
        assert "author" in df.columns
        assert "published_date" in df.columns
        assert "source" in df.columns
        assert "category" in df.columns
        assert "url" in df.columns

    def test_genera_ids_unicos(self):
        """Los IDs generados deben ser únicos."""
        df = extraer_noticias_api_simulada(num_noticias=20)

        assert df["id"].nunique() == 20

    def test_num_noticias_invalido_levanta_error(self):
        """Número inválido de noticias debe levantar ValueError."""
        with pytest.raises(ValueError, match="debe ser mayor que 0"):
            extraer_noticias_api_simulada(num_noticias=0)

        with pytest.raises(ValueError, match="debe ser mayor que 0"):
            extraer_noticias_api_simulada(num_noticias=-5)


class TestNormalizarRespuestaAPI:
    """Tests para normalización de respuesta de API."""

    def test_normaliza_respuesta_correctamente(self, api_response_mock):
        """Debe convertir respuesta de API a DataFrame normalizado."""
        df = normalizar_respuesta_api(api_response_mock)

        assert len(df) == 3
        assert "id" in df.columns
        assert "title" in df.columns
        assert "source" in df.columns

    def test_maneja_articulos_vacios(self):
        """Respuesta sin artículos debe retornar DataFrame vacío."""
        respuesta = {"status": "ok", "totalResults": 0, "articles": []}
        df = normalizar_respuesta_api(respuesta)

        assert len(df) == 0
        assert isinstance(df, pd.DataFrame)

    def test_maneja_campos_nulos(self):
        """Debe manejar campos nulos en artículos."""
        respuesta = {
            "status": "ok",
            "articles": [
                {
                    "source": {"name": "Test"},
                    "author": None,
                    "title": "Test Title",
                    "url": "https://test.com",
                    "publishedAt": "2024-01-01T00:00:00Z",
                    "content": None,
                }
            ],
        }
        df = normalizar_respuesta_api(respuesta)

        assert len(df) == 1
        assert pd.isna(df.iloc[0]["author"])


class TestGuardarEnBronze:
    """Tests para guardado en capa Bronze."""

    def test_guarda_parquet_correctamente(
        self, df_noticias_bronze, directorio_temporal
    ):
        """Debe guardar DataFrame en formato Parquet."""
        ruta = directorio_temporal / "bronze" / "noticias.parquet"

        guardar_en_bronze(df_noticias_bronze, ruta)

        assert ruta.exists()

        # Verificar que se puede leer
        df_leido = pd.read_parquet(ruta)
        assert len(df_leido) == len(df_noticias_bronze)

    def test_crea_directorio_si_no_existe(
        self, df_noticias_bronze, directorio_temporal
    ):
        """Debe crear directorio Bronze si no existe."""
        ruta = directorio_temporal / "nueva_capa" / "noticias.parquet"

        guardar_en_bronze(df_noticias_bronze, ruta)

        assert ruta.exists()

    def test_dataframe_vacio_levanta_error(self, directorio_temporal):
        """DataFrame vacío debe levantar ValueError."""
        df_vacio = pd.DataFrame()
        ruta = directorio_temporal / "bronze" / "noticias.parquet"

        with pytest.raises(ValueError, match="vacío"):
            guardar_en_bronze(df_vacio, ruta)


class TestExtraerNoticiasDesdeParquet:
    """Tests para lectura de datos Bronze."""

    def test_lee_parquet_correctamente(self, archivo_parquet_temporal):
        """Debe leer archivo Parquet correctamente."""
        df = extraer_noticias_desde_parquet(archivo_parquet_temporal)

        assert len(df) > 0
        assert "id" in df.columns
        assert "title" in df.columns

    def test_archivo_inexistente_levanta_error(self):
        """Archivo inexistente debe levantar FileNotFoundError."""
        from pathlib import Path

        ruta_inexistente = Path("inexistente.parquet")

        with pytest.raises(FileNotFoundError):
            extraer_noticias_desde_parquet(ruta_inexistente)
