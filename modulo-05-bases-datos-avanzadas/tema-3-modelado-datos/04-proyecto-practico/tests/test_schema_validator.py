"""
Tests para el módulo schema_validator.

Proyecto: Sistema de Diseño y Validación de Data Warehouse
"""

import pytest

from src.schema_validator import (
    identificar_dimension_tables,
    identificar_fact_table,
    validar_foreign_keys,
    validar_star_schema,
)


class TestIdentificarFactTable:
    """Tests para identificar_fact_table."""

    def test_identificar_fact_table_valida(self):
        """Debe identificar correctamente una tabla de hechos."""
        schema = {
            "fact_ventas": {
                "tipo": "fact",
                "columnas": {
                    "venta_id": "INTEGER PRIMARY KEY",
                    "fecha_id": "INTEGER REFERENCES dim_fecha",
                    "cliente_id": "INTEGER REFERENCES dim_cliente",
                    "producto_id": "INTEGER REFERENCES dim_producto",
                    "cantidad": "INTEGER",
                    "monto_venta": "NUMERIC(10,2)",
                },
            }
        }

        fact_table = identificar_fact_table(schema)

        assert fact_table == "fact_ventas"

    def test_identificar_fact_table_por_nombre(self):
        """Debe identificar fact table por prefijo 'fact_'."""
        schema = {
            "fact_pedidos": {
                "columnas": {
                    "pedido_id": "INTEGER PRIMARY KEY",
                    "total": "NUMERIC",
                }
            }
        }

        fact_table = identificar_fact_table(schema)

        assert fact_table == "fact_pedidos"

    def test_identificar_fact_table_sin_fact_lanza_error(self):
        """Debe lanzar ValueError si no hay tabla de hechos."""
        schema = {
            "dim_cliente": {"columnas": {"id": "INTEGER"}},
            "dim_producto": {"columnas": {"id": "INTEGER"}},
        }

        with pytest.raises(ValueError, match="No se encontró tabla de hechos"):
            identificar_fact_table(schema)

    def test_identificar_fact_table_multiples_fact_lanza_error(self):
        """Debe lanzar ValueError si hay múltiples tablas de hechos."""
        schema = {
            "fact_ventas": {"tipo": "fact", "columnas": {}},
            "fact_pedidos": {"tipo": "fact", "columnas": {}},
        }

        with pytest.raises(
            ValueError, match="Se encontraron múltiples tablas de hechos"
        ):
            identificar_fact_table(schema)


class TestIdentificarDimensionTables:
    """Tests para identificar_dimension_tables."""

    def test_identificar_dimension_tables_basico(self):
        """Debe identificar correctamente tablas de dimensión."""
        schema = {
            "dim_fecha": {"tipo": "dimension", "columnas": {}},
            "dim_cliente": {"tipo": "dimension", "columnas": {}},
            "dim_producto": {"tipo": "dimension", "columnas": {}},
            "fact_ventas": {"tipo": "fact", "columnas": {}},
        }

        dimensions = identificar_dimension_tables(schema)

        assert len(dimensions) == 3
        assert "dim_fecha" in dimensions
        assert "dim_cliente" in dimensions
        assert "dim_producto" in dimensions
        assert "fact_ventas" not in dimensions

    def test_identificar_dimension_tables_por_prefijo(self):
        """Debe identificar dimensiones por prefijo 'dim_'."""
        schema = {
            "dim_tiempo": {"columnas": {}},
            "dim_ubicacion": {"columnas": {}},
            "fact_ventas": {"columnas": {}},
        }

        dimensions = identificar_dimension_tables(schema)

        assert len(dimensions) == 2
        assert "dim_tiempo" in dimensions
        assert "dim_ubicacion" in dimensions

    def test_identificar_dimension_tables_vacio_sin_dim(self):
        """Debe retornar lista vacía si no hay dimensiones."""
        schema = {"fact_ventas": {"tipo": "fact", "columnas": {}}}

        dimensions = identificar_dimension_tables(schema)

        assert dimensions == []


class TestValidarForeignKeys:
    """Tests para validar_foreign_keys."""

    def test_validar_foreign_keys_correcto(self):
        """Debe validar correctamente FKs existentes."""
        fact_table = {
            "columnas": {
                "venta_id": "INTEGER PRIMARY KEY",
                "fecha_id": "INTEGER REFERENCES dim_fecha",
                "cliente_id": "INTEGER REFERENCES dim_cliente",
            }
        }

        dimension_tables = ["dim_fecha", "dim_cliente"]

        # No debe lanzar error
        validar_foreign_keys(fact_table, dimension_tables)

    def test_validar_foreign_keys_faltante(self):
        """Debe lanzar error si FK referencia dimensión inexistente."""
        fact_table = {
            "columnas": {
                "venta_id": "INTEGER PRIMARY KEY",
                "fecha_id": "INTEGER REFERENCES dim_fecha",
                "producto_id": "INTEGER REFERENCES dim_producto",  # No existe
            }
        }

        dimension_tables = ["dim_fecha"]

        with pytest.raises(ValueError, match="Clave foránea 'producto_id' referencia"):
            validar_foreign_keys(fact_table, dimension_tables)

    def test_validar_foreign_keys_sin_fks(self):
        """Debe lanzar error si fact table no tiene FKs."""
        fact_table = {
            "columnas": {
                "venta_id": "INTEGER PRIMARY KEY",
                "monto": "NUMERIC",
            }
        }

        dimension_tables = ["dim_fecha", "dim_cliente"]

        with pytest.raises(ValueError, match="Tabla de hechos debe tener al menos"):
            validar_foreign_keys(fact_table, dimension_tables)


class TestValidarStarSchema:
    """Tests para validar_star_schema."""

    def test_validar_star_schema_completo(self):
        """Debe validar correctamente un Star Schema completo."""
        schema = {
            "fact_ventas": {
                "tipo": "fact",
                "columnas": {
                    "venta_id": "INTEGER PRIMARY KEY",
                    "fecha_id": "INTEGER REFERENCES dim_fecha",
                    "cliente_id": "INTEGER REFERENCES dim_cliente",
                    "producto_id": "INTEGER REFERENCES dim_producto",
                    "cantidad": "INTEGER",
                    "monto_venta": "NUMERIC(10,2)",
                },
            },
            "dim_fecha": {
                "tipo": "dimension",
                "columnas": {
                    "fecha_id": "INTEGER PRIMARY KEY",
                    "fecha": "DATE",
                    "anio": "INTEGER",
                },
            },
            "dim_cliente": {
                "tipo": "dimension",
                "columnas": {
                    "cliente_id": "INTEGER PRIMARY KEY",
                    "nombre": "VARCHAR(200)",
                },
            },
            "dim_producto": {
                "tipo": "dimension",
                "columnas": {
                    "producto_id": "INTEGER PRIMARY KEY",
                    "nombre": "VARCHAR(200)",
                },
            },
        }

        resultado = validar_star_schema(schema)

        assert resultado["valido"]
        assert resultado["fact_table"] == "fact_ventas"
        assert len(resultado["dimension_tables"]) == 3

    def test_validar_star_schema_sin_fact_invalido(self):
        """Debe marcar como inválido si falta tabla de hechos."""
        schema = {
            "dim_cliente": {"tipo": "dimension", "columnas": {}},
            "dim_producto": {"tipo": "dimension", "columnas": {}},
        }

        resultado = validar_star_schema(schema)

        assert not resultado["valido"]
        assert any(
            "No se encontró tabla de hechos" in error for error in resultado["errores"]
        )

    def test_validar_star_schema_pocas_dimensiones(self):
        """Debe advertir si hay muy pocas dimensiones (<2)."""
        schema = {
            "fact_ventas": {
                "tipo": "fact",
                "columnas": {
                    "venta_id": "INTEGER PRIMARY KEY",
                    "fecha_id": "INTEGER REFERENCES dim_fecha",
                    "monto": "NUMERIC",
                },
            },
            "dim_fecha": {"tipo": "dimension", "columnas": {}},
        }

        resultado = validar_star_schema(schema)

        assert not resultado["valido"]
        assert any("al menos 2 dimensiones" in error for error in resultado["errores"])

    def test_validar_star_schema_fk_invalida(self):
        """Debe detectar FKs que referencian dimensiones inexistentes."""
        schema = {
            "fact_ventas": {
                "tipo": "fact",
                "columnas": {
                    "venta_id": "INTEGER PRIMARY KEY",
                    "fecha_id": "INTEGER REFERENCES dim_fecha",
                    "cliente_id": "INTEGER REFERENCES dim_cliente",
                    "tienda_id": "INTEGER REFERENCES dim_tienda",  # No existe
                },
            },
            "dim_fecha": {"tipo": "dimension", "columnas": {}},
            "dim_cliente": {"tipo": "dimension", "columnas": {}},
        }

        resultado = validar_star_schema(schema)

        assert not resultado["valido"]
        assert any("tienda_id" in error for error in resultado["errores"])
