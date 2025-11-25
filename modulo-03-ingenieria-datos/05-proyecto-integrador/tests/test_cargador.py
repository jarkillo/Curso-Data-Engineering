"""
Tests para módulo de carga de datos.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

from pathlib import Path

import pandas as pd
import pytest

from src.cargador import (
    cargar_a_base_datos,
    cargar_a_parquet,
    verificar_carga_base_datos,
    verificar_carga_parquet,
)


class TestCargarAParquet:
    """Tests para carga en Parquet."""

    def test_carga_dataframe_correctamente(
        self, df_noticias_silver, directorio_temporal
    ):
        """Debe guardar DataFrame en Parquet."""
        ruta = directorio_temporal / "gold" / "noticias_gold.parquet"

        cargar_a_parquet(df_noticias_silver, ruta)

        assert ruta.exists()

    def test_parquet_es_legible(self, df_noticias_silver, directorio_temporal):
        """Archivo Parquet debe ser legible."""
        ruta = directorio_temporal / "gold" / "noticias_gold.parquet"

        cargar_a_parquet(df_noticias_silver, ruta)

        df_leido = pd.read_parquet(ruta)
        assert len(df_leido) == len(df_noticias_silver)

    def test_crea_directorio_si_no_existe(
        self, df_noticias_silver, directorio_temporal
    ):
        """Debe crear directorio si no existe."""
        ruta = directorio_temporal / "nueva_capa" / "datos.parquet"

        cargar_a_parquet(df_noticias_silver, ruta)

        assert ruta.exists()

    def test_dataframe_vacio_levanta_error(self, directorio_temporal):
        """DataFrame vacío debe levantar ValueError."""
        df_vacio = pd.DataFrame()
        ruta = directorio_temporal / "gold" / "noticias.parquet"

        with pytest.raises(ValueError, match="vacío"):
            cargar_a_parquet(df_vacio, ruta)


class TestCargarABaseDatos:
    """Tests para carga en base de datos."""

    def test_carga_en_tabla_nueva(self, df_noticias_silver, engine_temporal):
        """Debe crear tabla y cargar datos."""
        num_cargados = cargar_a_base_datos(
            df_noticias_silver, engine_temporal, "noticias_silver", if_exists="replace"
        )

        assert num_cargados == len(df_noticias_silver)

        # Verificar que se creó la tabla
        df_leido = pd.read_sql("SELECT * FROM noticias_silver", engine_temporal)
        assert len(df_leido) == len(df_noticias_silver)

    def test_append_agrega_registros(self, df_noticias_silver, engine_temporal):
        """Modo append debe agregar registros."""
        # Cargar datos iniciales
        cargar_a_base_datos(
            df_noticias_silver, engine_temporal, "noticias", if_exists="replace"
        )

        # Agregar más datos
        df_nuevos = df_noticias_silver.head(2).copy()
        num_agregados = cargar_a_base_datos(
            df_nuevos, engine_temporal, "noticias", if_exists="append"
        )

        assert num_agregados == 2

        # Verificar total
        df_leido = pd.read_sql("SELECT * FROM noticias", engine_temporal)
        assert len(df_leido) == len(df_noticias_silver) + 2

    def test_replace_reemplaza_datos(self, df_noticias_silver, engine_temporal):
        """Modo replace debe reemplazar datos."""
        # Cargar datos iniciales
        cargar_a_base_datos(
            df_noticias_silver, engine_temporal, "noticias", if_exists="replace"
        )

        # Reemplazar con datos diferentes
        df_nuevos = df_noticias_silver.head(2).copy()
        cargar_a_base_datos(df_nuevos, engine_temporal, "noticias", if_exists="replace")

        # Verificar que solo están los nuevos
        df_leido = pd.read_sql("SELECT * FROM noticias", engine_temporal)
        assert len(df_leido) == 2

    def test_dataframe_vacio_levanta_error(self, engine_temporal):
        """DataFrame vacío debe levantar ValueError."""
        df_vacio = pd.DataFrame()

        with pytest.raises(ValueError, match="vacío"):
            cargar_a_base_datos(df_vacio, engine_temporal, "tabla")


class TestVerificarCargaParquet:
    """Tests para verificación de carga Parquet."""

    def test_verificacion_exitosa(self, df_noticias_silver, directorio_temporal):
        """Debe verificar carga exitosa."""
        ruta = directorio_temporal / "gold" / "noticias.parquet"
        cargar_a_parquet(df_noticias_silver, ruta)

        resultado = verificar_carga_parquet(df_noticias_silver, ruta)

        assert resultado["valido"]
        assert resultado["registros_esperados"] == len(df_noticias_silver)
        assert resultado["registros_cargados"] == len(df_noticias_silver)

    def test_verificacion_falla_si_conteos_difieren(
        self, df_noticias_silver, directorio_temporal
    ):
        """Debe fallar si conteos no coinciden."""
        ruta = directorio_temporal / "gold" / "noticias.parquet"

        # Cargar solo parte de los datos
        df_parcial = df_noticias_silver.head(2)
        cargar_a_parquet(df_parcial, ruta)

        # Verificar con DataFrame completo
        resultado = verificar_carga_parquet(df_noticias_silver, ruta)

        assert not resultado["valido"]

    def test_archivo_inexistente_retorna_false(self, df_noticias_silver):
        """Archivo inexistente debe retornar falso."""
        ruta_inexistente = Path("inexistente.parquet")

        resultado = verificar_carga_parquet(df_noticias_silver, ruta_inexistente)

        assert not resultado["valido"]


class TestVerificarCargaBaseDatos:
    """Tests para verificación de carga en BD."""

    def test_verificacion_exitosa(self, df_noticias_silver, engine_temporal):
        """Debe verificar carga exitosa."""
        cargar_a_base_datos(df_noticias_silver, engine_temporal, "noticias")

        resultado = verificar_carga_base_datos(
            df_noticias_silver, engine_temporal, "noticias"
        )

        assert resultado["valido"]
        assert resultado["registros_esperados"] == len(df_noticias_silver)
        assert resultado["registros_cargados"] == len(df_noticias_silver)

    def test_verificacion_falla_si_conteos_difieren(
        self, df_noticias_silver, engine_temporal
    ):
        """Debe fallar si conteos no coinciden."""
        # Cargar solo parte
        df_parcial = df_noticias_silver.head(2)
        cargar_a_base_datos(df_parcial, engine_temporal, "noticias")

        # Verificar con DataFrame completo
        resultado = verificar_carga_base_datos(
            df_noticias_silver, engine_temporal, "noticias"
        )

        assert not resultado["valido"]

    def test_tabla_inexistente_retorna_false(self, df_noticias_silver, engine_temporal):
        """Tabla inexistente debe retornar falso."""
        resultado = verificar_carga_base_datos(
            df_noticias_silver, engine_temporal, "tabla_inexistente"
        )

        assert not resultado["valido"]
