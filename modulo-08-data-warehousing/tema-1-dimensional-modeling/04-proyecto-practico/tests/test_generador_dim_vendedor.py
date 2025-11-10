"""
Tests para generador_dim_vendedor.py.

Tests escritos PRIMERO siguiendo TDD para generador de DimVendedor.
Cobertura objetivo: ≥80%.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestGenerarDimVendedor:
    """Tests para generar_dim_vendedor()."""

    def test_genera_numero_correcto_de_vendedores(self):
        """Should generate correct number of salesperson records."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        num_vendedores = 50
        df = generar_dim_vendedor(num_vendedores)

        assert len(df) == num_vendedores

    def test_retorna_dataframe(self):
        """Should return pandas DataFrame."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        resultado = generar_dim_vendedor(10)

        assert isinstance(resultado, pd.DataFrame)

    def test_tiene_columnas_requeridas(self):
        """Should have all required columns."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(10)
        columnas_requeridas = [
            "vendedor_id",
            "nombre",
            "email",
            "telefono",
            "region",
            "comision_porcentaje",
            "supervisor_id",
            "gerente_regional",
        ]

        for columna in columnas_requeridas:
            assert columna in df.columns

    def test_vendedor_id_es_unico(self):
        """Should have unique vendedor_id values."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(100)

        assert df["vendedor_id"].is_unique

    def test_vendedor_id_empieza_en_1(self):
        """Should start vendedor_id from 1."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(10)

        assert df["vendedor_id"].min() == 1

    def test_nombre_no_es_nulo(self):
        """Should have no null values in nombre."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(50)

        assert df["nombre"].notna().all()

    def test_email_formato_valido(self):
        """Should have valid email format."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(20)

        # Todos los emails deben contener @
        assert df["email"].str.contains("@").all()

    def test_region_es_valida(self):
        """Should have valid region values."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(100)
        regiones_validas = ["Norte", "Sur", "Centro", "Este", "Oeste"]

        assert df["region"].isin(regiones_validas).all()

    def test_comision_porcentaje_en_rango(self):
        """Should have commission percentage in valid range (0-20%)."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(100)

        assert (df["comision_porcentaje"] >= 0).all()
        assert (df["comision_porcentaje"] <= 20).all()

    def test_supervisor_id_puede_ser_nulo(self):
        """Should allow null supervisor_id for top-level salespeople."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(50)

        # Debe haber al menos algunos registros con supervisor_id nulo (gerentes)
        assert df["supervisor_id"].isna().any()

    def test_supervisor_id_referencia_vendedor_existente(self):
        """Should have supervisor_id referencing existing vendedor_id."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(50)

        # Filtrar supervisores no nulos
        supervisores_no_nulos = df["supervisor_id"].dropna()

        if len(supervisores_no_nulos) > 0:
            # Todos los supervisor_id deben existir en vendedor_id
            assert supervisores_no_nulos.isin(df["vendedor_id"]).all()

    def test_gerente_regional_no_es_nulo(self):
        """Should have no null values in gerente_regional."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(50)

        assert df["gerente_regional"].notna().all()

    def test_tipos_de_datos_correctos(self):
        """Should have correct data types."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(20)

        assert df["vendedor_id"].dtype in ["int64", "int32"]
        assert df["nombre"].dtype == "object"  # string
        assert df["email"].dtype == "object"
        assert df["telefono"].dtype == "object"
        assert df["region"].dtype == "object"
        assert df["comision_porcentaje"].dtype in ["float64", "float32"]
        # supervisor_id puede ser float por valores NaN
        assert df["gerente_regional"].dtype == "object"

    def test_falla_con_numero_negativo(self):
        """Should raise ValueError if num_vendedores is negative."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        with pytest.raises(ValueError, match="debe ser positivo"):
            generar_dim_vendedor(-10)

    def test_falla_con_cero(self):
        """Should raise ValueError if num_vendedores is zero."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        with pytest.raises(ValueError, match="debe ser positivo"):
            generar_dim_vendedor(0)

    def test_telefono_tiene_formato_correcto(self):
        """Should have valid phone format."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(20)

        # Verificar que telefono no esté vacío
        assert (df["telefono"].str.len() > 0).all()

    def test_estructura_jerarquica_coherente(self):
        """Should have coherent hierarchical structure."""
        from src.generador_dim_vendedor import generar_dim_vendedor

        df = generar_dim_vendedor(100)

        # Los vendedores con supervisor_id nulo deben ser gerentes
        gerentes = df[df["supervisor_id"].isna()]
        assert len(gerentes) > 0

        # Los vendedores con supervisor_id no nulo deben reportar a alguien
        vendedores_con_supervisor = df[df["supervisor_id"].notna()]
        assert len(vendedores_con_supervisor) > 0
