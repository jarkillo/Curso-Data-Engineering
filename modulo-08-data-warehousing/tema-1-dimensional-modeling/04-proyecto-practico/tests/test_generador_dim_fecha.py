"""
Tests para generador_dim_fecha.py.

Tests escritos PRIMERO siguiendo TDD (Test-Driven Development).
"""

import pandas as pd
import pytest


class TestGenerarDimFecha:
    """Tests para la función generar_dim_fecha."""

    def test_generar_anio_completo_2024(self):
        """Should generate 366 rows for 2024 (leap year)."""
        from src.generador_dim_fecha import generar_dim_fecha

        dim_fecha = generar_dim_fecha("2024-01-01", "2024-12-31")

        assert isinstance(dim_fecha, pd.DataFrame)
        assert len(dim_fecha) == 366  # Año bisiesto

    def test_generar_mes_enero_2024(self):
        """Should generate 31 rows for January 2024."""
        from src.generador_dim_fecha import generar_dim_fecha

        dim_fecha = generar_dim_fecha("2024-01-01", "2024-01-31")

        assert len(dim_fecha) == 31

    def test_tiene_todas_las_columnas_requeridas(self):
        """Should have all required columns."""
        from src.generador_dim_fecha import generar_dim_fecha

        dim_fecha = generar_dim_fecha("2024-01-01", "2024-01-05")

        columnas_esperadas = [
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

        for col in columnas_esperadas:
            assert col in dim_fecha.columns, f"Falta columna: {col}"

    def test_fecha_id_tiene_formato_correcto(self):
        """Should have fecha_id in YYYYMMDD format."""
        from src.generador_dim_fecha import generar_dim_fecha

        dim_fecha = generar_dim_fecha("2024-03-15", "2024-03-15")

        assert dim_fecha["fecha_id"].iloc[0] == 20240315

    def test_dia_semana_correcto(self):
        """Should have correct day of week for known date."""
        from src.generador_dim_fecha import generar_dim_fecha

        # 2024-01-01 es lunes
        dim_fecha = generar_dim_fecha("2024-01-01", "2024-01-01")

        assert dim_fecha["dia_semana"].iloc[0] == "Lunes"
        assert dim_fecha["numero_dia_semana"].iloc[0] == 0

    def test_fin_de_semana_correcto(self):
        """Should correctly identify weekends."""
        from src.generador_dim_fecha import generar_dim_fecha

        # 2024-01-06 es sábado, 2024-01-07 es domingo
        dim_fecha = generar_dim_fecha("2024-01-06", "2024-01-08")

        assert dim_fecha.iloc[0]["es_fin_de_semana"]  # Sábado
        assert dim_fecha.iloc[1]["es_fin_de_semana"]  # Domingo
        assert not dim_fecha.iloc[2]["es_fin_de_semana"]  # Lunes

    def test_trimestre_correcto(self):
        """Should assign correct quarter."""
        from src.generador_dim_fecha import generar_dim_fecha

        dim_fecha = generar_dim_fecha("2024-01-01", "2024-12-31")

        # Enero (mes 1) = Trimestre 1
        assert dim_fecha[dim_fecha["mes"] == 1]["trimestre"].iloc[0] == 1
        # Abril (mes 4) = Trimestre 2
        assert dim_fecha[dim_fecha["mes"] == 4]["trimestre"].iloc[0] == 2
        # Julio (mes 7) = Trimestre 3
        assert dim_fecha[dim_fecha["mes"] == 7]["trimestre"].iloc[0] == 3
        # Octubre (mes 10) = Trimestre 4
        assert dim_fecha[dim_fecha["mes"] == 10]["trimestre"].iloc[0] == 4

    def test_con_festivos(self):
        """Should mark holidays correctly."""
        from src.generador_dim_fecha import generar_dim_fecha

        festivos = [
            {"fecha": "2024-01-01", "nombre": "Año Nuevo"},
            {"fecha": "2024-12-25", "nombre": "Navidad"},
        ]

        dim_fecha = generar_dim_fecha("2024-01-01", "2024-12-31", festivos)

        # Verificar Año Nuevo
        anio_nuevo = dim_fecha[dim_fecha["fecha_id"] == 20240101].iloc[0]
        assert anio_nuevo["es_dia_festivo"]
        assert anio_nuevo["nombre_festivo"] == "Año Nuevo"

        # Verificar Navidad
        navidad = dim_fecha[dim_fecha["fecha_id"] == 20241225].iloc[0]
        assert navidad["es_dia_festivo"]
        assert navidad["nombre_festivo"] == "Navidad"

    def test_sin_festivos_todos_son_false(self):
        """Should mark all dates as non-holidays when no holidays provided."""
        from src.generador_dim_fecha import generar_dim_fecha

        dim_fecha = generar_dim_fecha("2024-01-01", "2024-01-31")

        assert dim_fecha["es_dia_festivo"].sum() == 0

    def test_fecha_inicio_mayor_que_fin_raise_error(self):
        """Should raise ValueError if start date > end date."""
        from src.generador_dim_fecha import generar_dim_fecha

        with pytest.raises(ValueError, match="fecha_inicio debe ser menor"):
            generar_dim_fecha("2024-12-31", "2024-01-01")

    def test_formato_fecha_invalido_raise_error(self):
        """Should raise ValueError if date format is invalid."""
        from src.generador_dim_fecha import generar_dim_fecha

        with pytest.raises(ValueError):
            generar_dim_fecha("2024/01/01", "2024-12-31")

    def test_mes_nombre_en_espanol(self):
        """Should have month names in Spanish."""
        from src.generador_dim_fecha import generar_dim_fecha

        dim_fecha = generar_dim_fecha("2024-01-01", "2024-12-31")

        meses_esperados = [
            "Enero",
            "Febrero",
            "Marzo",
            "Abril",
            "Mayo",
            "Junio",
            "Julio",
            "Agosto",
            "Septiembre",
            "Octubre",
            "Noviembre",
            "Diciembre",
        ]

        meses_en_dim = dim_fecha["mes_nombre"].unique().tolist()

        for mes in meses_esperados:
            assert mes in meses_en_dim
