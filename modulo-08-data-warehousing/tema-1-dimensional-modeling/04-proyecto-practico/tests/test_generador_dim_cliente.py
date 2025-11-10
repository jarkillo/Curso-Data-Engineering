"""
Tests para generador_dim_cliente.py.

Tests escritos PRIMERO siguiendo TDD para DimCliente con SCD Type 2.
"""

from datetime import date

import pandas as pd
import pytest


class TestGenerarDimCliente:
    """Tests para la función generar_dim_cliente."""

    def test_generar_100_clientes(self):
        """Should generate exactly 100 cliente records."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(100)

        assert isinstance(clientes, pd.DataFrame)
        assert len(clientes) == 100

    def test_tiene_columnas_requeridas(self):
        """Should have all required columns including SCD Type 2 fields."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(10)

        columnas_esperadas = [
            "cliente_id",
            "nombre",
            "email",
            "telefono",
            "direccion",
            "ciudad",
            "estado",
            "codigo_postal",
            "fecha_registro",
            "segmento",
            # Campos SCD Type 2
            "fecha_inicio",
            "fecha_fin",
            "version",
            "es_actual",
        ]

        for col in columnas_esperadas:
            assert col in clientes.columns, f"Falta columna: {col}"

    def test_cliente_id_es_unico_por_version(self):
        """Should have unique combination of cliente_id + version."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(50)

        # La combinación cliente_id + version debe ser única
        combinacion = (
            clientes["cliente_id"].astype(str) + "_" + clientes["version"].astype(str)
        )
        assert combinacion.is_unique

    def test_email_formato_valido(self):
        """Should have valid email format."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(20)

        # Todos los emails deben contener @
        assert all("@" in email for email in clientes["email"])

    def test_telefono_no_vacio(self):
        """Should have non-empty phone numbers."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(20)

        assert clientes["telefono"].notna().all()
        assert (clientes["telefono"].str.len() > 0).all()

    def test_segmento_valido(self):
        """Should have valid customer segments."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(100)

        segmentos_validos = ["Premium", "Regular", "Nuevo"]
        segmentos_unicos = clientes["segmento"].unique()

        for seg in segmentos_unicos:
            assert seg in segmentos_validos

    def test_scd_type2_version_inicial_es_1(self):
        """Should start with version 1 for new customers."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(50)

        # Todos los registros iniciales deben tener version = 1
        assert (clientes["version"] == 1).all()

    def test_scd_type2_es_actual_es_true(self):
        """Should mark all initial records as current (es_actual = True)."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(50)

        # Todos los registros iniciales deben ser actuales
        assert (clientes["es_actual"]).all()

    def test_scd_type2_fecha_inicio_valida(self):
        """Should have valid fecha_inicio (date type)."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(20)

        # fecha_inicio debe ser tipo date
        assert clientes["fecha_inicio"].dtype == "object"
        assert all(isinstance(f, date) for f in clientes["fecha_inicio"])

    def test_scd_type2_fecha_fin_es_none_inicial(self):
        """Should have fecha_fin = None for initial (current) records."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(30)

        # Para registros actuales, fecha_fin debe ser None
        assert clientes["fecha_fin"].isna().all()

    def test_fecha_registro_valida(self):
        """Should have valid registration dates."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(20)

        # fecha_registro debe ser tipo date
        assert clientes["fecha_registro"].dtype == "object"
        assert all(isinstance(f, date) for f in clientes["fecha_registro"])

    def test_num_clientes_cero_raise_error(self):
        """Should raise ValueError if num_clientes is 0."""
        from src.generador_dim_cliente import generar_dim_cliente

        with pytest.raises(ValueError, match="debe ser mayor que 0"):
            generar_dim_cliente(0)

    def test_num_clientes_negativo_raise_error(self):
        """Should raise ValueError if num_clientes is negative."""
        from src.generador_dim_cliente import generar_dim_cliente

        with pytest.raises(ValueError, match="debe ser mayor que 0"):
            generar_dim_cliente(-10)

    def test_codigo_postal_formato_valido(self):
        """Should have valid postal codes (5 digits)."""
        from src.generador_dim_cliente import generar_dim_cliente

        clientes = generar_dim_cliente(30)

        # Códigos postales deben tener 5 dígitos
        assert all(len(cp) == 5 for cp in clientes["codigo_postal"])
        assert all(cp.isdigit() for cp in clientes["codigo_postal"])
