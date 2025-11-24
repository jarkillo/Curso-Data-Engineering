"""
Tests para el módulo ddl_generator.

Proyecto: Sistema de Diseño y Validación de Data Warehouse
"""

import pytest

from src.ddl_generator import (
    generar_create_dim_table,
    generar_create_fact_table,
    generar_ddl_completo,
    generar_indices,
)


class TestGenerarCreateDimTable:
    """Tests para generar_create_dim_table."""

    def test_generar_dim_table_simple(self):
        """Debe generar CREATE TABLE para dimensión simple."""
        dim_def = {
            "columnas": {
                "fecha_id": "INTEGER PRIMARY KEY",
                "fecha": "DATE NOT NULL",
                "anio": "INTEGER",
            }
        }

        ddl = generar_create_dim_table("dim_fecha", dim_def)

        assert "CREATE TABLE dim_fecha" in ddl
        assert "fecha_id INTEGER PRIMARY KEY" in ddl
        assert "fecha DATE NOT NULL" in ddl
        assert "anio INTEGER" in ddl

    def test_generar_dim_table_con_constraints(self):
        """Debe incluir constraints en la definición."""
        dim_def = {
            "columnas": {
                "producto_id": "INTEGER PRIMARY KEY",
                "nombre": "VARCHAR(200) NOT NULL",
                "precio": "NUMERIC(10,2) CHECK (precio > 0)",
            }
        }

        ddl = generar_create_dim_table("dim_producto", dim_def)

        assert "CHECK (precio > 0)" in ddl

    def test_generar_dim_table_columnas_vacias(self):
        """Debe lanzar error si no hay columnas."""
        dim_def = {"columnas": {}}

        with pytest.raises(ValueError, match="debe tener al menos una columna"):
            generar_create_dim_table("dim_test", dim_def)


class TestGenerarCreateFactTable:
    """Tests para generar_create_fact_table."""

    def test_generar_fact_table_con_fks(self):
        """Debe generar CREATE TABLE con FKs."""
        fact_def = {
            "columnas": {
                "venta_id": "BIGSERIAL PRIMARY KEY",
                "fecha_id": "INTEGER REFERENCES dim_fecha",
                "cliente_id": "INTEGER REFERENCES dim_cliente",
                "monto_venta": "NUMERIC(10,2)",
            }
        }

        ddl = generar_create_fact_table("fact_ventas", fact_def)

        assert "CREATE TABLE fact_ventas" in ddl
        assert "venta_id BIGSERIAL PRIMARY KEY" in ddl
        assert "fecha_id INTEGER REFERENCES dim_fecha" in ddl
        assert "cliente_id INTEGER REFERENCES dim_cliente" in ddl

    def test_generar_fact_table_sin_fks_lanza_error(self):
        """Debe lanzar error si fact table no tiene FKs."""
        fact_def = {
            "columnas": {
                "venta_id": "INTEGER PRIMARY KEY",
                "monto": "NUMERIC",
            }
        }

        with pytest.raises(ValueError, match="debe tener al menos una FK"):
            generar_create_fact_table("fact_ventas", fact_def)


class TestGenerarIndices:
    """Tests para generar_indices."""

    def test_generar_indices_para_fact_table(self):
        """Debe generar índices en columnas FK de fact table."""
        fact_def = {
            "columnas": {
                "venta_id": "BIGSERIAL PRIMARY KEY",
                "fecha_id": "INTEGER REFERENCES dim_fecha",
                "cliente_id": "INTEGER REFERENCES dim_cliente",
                "producto_id": "INTEGER REFERENCES dim_producto",
            }
        }

        indices = generar_indices("fact_ventas", fact_def, es_fact_table=True)

        assert len(indices) >= 3  # Un índice por cada FK
        assert any("idx_fact_ventas_fecha" in idx for idx in indices)
        assert any("idx_fact_ventas_cliente" in idx for idx in indices)
        assert any("idx_fact_ventas_producto" in idx for idx in indices)

    def test_generar_indices_contenido_correcto(self):
        """Debe generar statement CREATE INDEX válido."""
        fact_def = {
            "columnas": {
                "venta_id": "BIGSERIAL PRIMARY KEY",
                "fecha_id": "INTEGER REFERENCES dim_fecha",
            }
        }

        indices = generar_indices("fact_ventas", fact_def, es_fact_table=True)

        assert len(indices) == 1
        idx = indices[0]
        assert "CREATE INDEX" in idx
        assert "ON fact_ventas" in idx
        assert "fecha_id" in idx

    def test_generar_indices_dimension_vacia(self):
        """Debe retornar lista vacía si dimensión no requiere índices."""
        dim_def = {"columnas": {"dim_id": "INTEGER PRIMARY KEY"}}

        indices = generar_indices("dim_test", dim_def, es_fact_table=False)

        assert indices == []


class TestGenerarDDLCompleto:
    """Tests para generar_ddl_completo."""

    def test_generar_ddl_completo_star_schema(self):
        """Debe generar DDL completo para un Star Schema."""
        schema = {
            "fact_ventas": {
                "tipo": "fact",
                "columnas": {
                    "venta_id": "BIGSERIAL PRIMARY KEY",
                    "fecha_id": "INTEGER REFERENCES dim_fecha",
                    "cliente_id": "INTEGER REFERENCES dim_cliente",
                    "monto": "NUMERIC(10,2)",
                },
            },
            "dim_fecha": {
                "tipo": "dimension",
                "columnas": {"fecha_id": "INTEGER PRIMARY KEY", "fecha": "DATE"},
            },
            "dim_cliente": {
                "tipo": "dimension",
                "columnas": {"cliente_id": "INTEGER PRIMARY KEY", "nombre": "VARCHAR"},
            },
        }

        ddl = generar_ddl_completo(schema)

        # Debe tener secciones para dimensiones y fact table
        assert "-- Dimensiones" in ddl or "CREATE TABLE dim_" in ddl
        assert "CREATE TABLE fact_ventas" in ddl
        assert "CREATE TABLE dim_fecha" in ddl
        assert "CREATE TABLE dim_cliente" in ddl

    def test_generar_ddl_completo_con_indices(self):
        """Debe incluir índices en el DDL completo."""
        schema = {
            "fact_ventas": {
                "tipo": "fact",
                "columnas": {
                    "venta_id": "BIGSERIAL PRIMARY KEY",
                    "fecha_id": "INTEGER REFERENCES dim_fecha",
                },
            },
            "dim_fecha": {
                "tipo": "dimension",
                "columnas": {"fecha_id": "INTEGER PRIMARY KEY"},
            },
        }

        ddl = generar_ddl_completo(schema)

        assert "CREATE INDEX" in ddl

    def test_generar_ddl_completo_orden_correcto(self):
        """Debe generar dimensiones antes de fact table (orden de FKs)."""
        schema = {
            "fact_ventas": {
                "tipo": "fact",
                "columnas": {
                    "venta_id": "BIGSERIAL PRIMARY KEY",
                    "fecha_id": "INTEGER REFERENCES dim_fecha",
                },
            },
            "dim_fecha": {
                "tipo": "dimension",
                "columnas": {"fecha_id": "INTEGER PRIMARY KEY"},
            },
        }

        ddl = generar_ddl_completo(schema)

        # Posición de dim_fecha debe ser antes de fact_ventas
        pos_dim = ddl.index("CREATE TABLE dim_fecha")
        pos_fact = ddl.index("CREATE TABLE fact_ventas")

        assert pos_dim < pos_fact
