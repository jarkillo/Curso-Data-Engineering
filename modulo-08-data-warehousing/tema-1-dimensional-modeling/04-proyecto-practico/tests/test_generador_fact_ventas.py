"""
Tests para generador_fact_ventas.py.

Tests escritos PRIMERO siguiendo TDD para generador de FactVentas.
Cobertura objetivo: ≥80%.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestGenerarFactVentas:
    """Tests para generar_fact_ventas()."""

    def test_genera_numero_correcto_de_ventas(self):
        """Should generate correct number of sales records."""
        from src.generador_fact_ventas import generar_fact_ventas

        # Crear dimensiones mínimas para test
        dim_fecha = pd.DataFrame({"fecha_id": [20240101, 20240102, 20240103]})
        dim_producto = pd.DataFrame(
            {
                "producto_id": [1, 2, 3],
                "precio_catalogo": [100.0, 200.0, 150.0],
            }
        )
        dim_cliente = pd.DataFrame({"cliente_id": [1, 2, 3]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1, 2, 3]})

        num_ventas = 50
        df = generar_fact_ventas(
            num_ventas, dim_fecha, dim_producto, dim_cliente, dim_vendedor
        )

        assert len(df) == num_ventas

    def test_retorna_dataframe(self):
        """Should return pandas DataFrame."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        resultado = generar_fact_ventas(
            10, dim_fecha, dim_producto, dim_cliente, dim_vendedor
        )

        assert isinstance(resultado, pd.DataFrame)

    def test_tiene_columnas_requeridas(self):
        """Should have all required columns."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(10, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        columnas_requeridas = [
            "venta_id",
            "fecha_id",
            "producto_id",
            "cliente_id",
            "vendedor_id",
            "cantidad",
            "precio_unitario",
            "descuento",
            "impuesto",
            "monto_neto",
        ]

        for columna in columnas_requeridas:
            assert columna in df.columns

    def test_venta_id_es_unico(self):
        """Should have unique venta_id values."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101, 20240102]})
        dim_producto = pd.DataFrame(
            {
                "producto_id": [1, 2],
                "precio_catalogo": [100.0, 200.0],
            }
        )
        dim_cliente = pd.DataFrame({"cliente_id": [1, 2]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1, 2]})

        df = generar_fact_ventas(
            100, dim_fecha, dim_producto, dim_cliente, dim_vendedor
        )

        assert df["venta_id"].is_unique

    def test_venta_id_empieza_en_1(self):
        """Should start venta_id from 1."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(10, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        assert df["venta_id"].min() == 1

    def test_fecha_id_referencia_dimensiones(self):
        """Should have fecha_id referencing existing dimension."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101, 20240102]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        # Todas las fecha_id deben existir en dim_fecha
        assert df["fecha_id"].isin(dim_fecha["fecha_id"]).all()

    def test_producto_id_referencia_dimensiones(self):
        """Should have producto_id referencing existing dimension."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame(
            {
                "producto_id": [1, 2, 3],
                "precio_catalogo": [100.0, 200.0, 150.0],
            }
        )
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        # Todas las producto_id deben existir en dim_producto
        assert df["producto_id"].isin(dim_producto["producto_id"]).all()

    def test_cliente_id_referencia_dimensiones(self):
        """Should have cliente_id referencing existing dimension."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1, 2, 3]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        # Todas las cliente_id deben existir en dim_cliente
        assert df["cliente_id"].isin(dim_cliente["cliente_id"]).all()

    def test_vendedor_id_referencia_dimensiones(self):
        """Should have vendedor_id referencing existing dimension."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1, 2, 3]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        # Todas las vendedor_id deben existir en dim_vendedor
        assert df["vendedor_id"].isin(dim_vendedor["vendedor_id"]).all()

    def test_cantidad_es_positiva(self):
        """Should have positive quantity values."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        assert (df["cantidad"] > 0).all()

    def test_precio_unitario_es_positivo(self):
        """Should have positive unit price values."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        assert (df["precio_unitario"] > 0).all()

    def test_descuento_en_rango_valido(self):
        """Should have discount as non-negative amounts (≤40% of subtotal)."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(
            100, dim_fecha, dim_producto, dim_cliente, dim_vendedor
        )

        # El descuento debe ser no negativo
        assert (df["descuento"] >= 0).all()

        # El descuento debe ser ≤40% del subtotal (cantidad * precio_unitario)
        subtotal = df["cantidad"] * df["precio_unitario"]
        assert (
            df["descuento"] <= subtotal * 0.40 + 0.01
        ).all()  # +0.01 tolerancia redondeo

    def test_impuesto_es_positivo(self):
        """Should have positive tax values."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        assert (df["impuesto"] >= 0).all()

    def test_monto_neto_coherente(self):
        """Should have coherent net amount calculated from other fields."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(10, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        # Verificar que monto_neto = (cantidad * precio_unitario - descuento) + impuesto
        # Con tolerancia para errores de redondeo
        monto_calculado = (
            df["cantidad"] * df["precio_unitario"] - df["descuento"] + df["impuesto"]
        )

        assert ((df["monto_neto"] - monto_calculado).abs() < 0.01).all()

    def test_tipos_de_datos_correctos(self):
        """Should have correct data types."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(20, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        assert df["venta_id"].dtype in ["int64", "int32"]
        assert df["fecha_id"].dtype in ["int64", "int32"]
        assert df["producto_id"].dtype in ["int64", "int32"]
        assert df["cliente_id"].dtype in ["int64", "int32"]
        assert df["vendedor_id"].dtype in ["int64", "int32"]
        assert df["cantidad"].dtype in ["int64", "int32"]
        assert df["precio_unitario"].dtype in ["float64", "float32"]
        assert df["descuento"].dtype in ["float64", "float32"]
        assert df["impuesto"].dtype in ["float64", "float32"]
        assert df["monto_neto"].dtype in ["float64", "float32"]

    def test_falla_con_dimensiones_vacias(self):
        """Should raise ValueError if any dimension is empty."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": []})  # Vacía
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        with pytest.raises(ValueError, match="Dimensiones no pueden estar vacías"):
            generar_fact_ventas(10, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

    def test_falla_con_num_ventas_cero(self):
        """Should raise ValueError if num_ventas is zero."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        with pytest.raises(ValueError, match="debe ser positivo"):
            generar_fact_ventas(0, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

    def test_falla_con_num_ventas_negativo(self):
        """Should raise ValueError if num_ventas is negative."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame({"producto_id": [1], "precio_catalogo": [100.0]})
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        with pytest.raises(ValueError, match="debe ser positivo"):
            generar_fact_ventas(-10, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

    def test_precio_unitario_cerca_de_precio_catalogo(self):
        """Should have unit price close to catalog price (with variations)."""
        from src.generador_fact_ventas import generar_fact_ventas

        dim_fecha = pd.DataFrame({"fecha_id": [20240101]})
        dim_producto = pd.DataFrame(
            {
                "producto_id": [1],
                "precio_catalogo": [100.0],
            }
        )
        dim_cliente = pd.DataFrame({"cliente_id": [1]})
        dim_vendedor = pd.DataFrame({"vendedor_id": [1]})

        df = generar_fact_ventas(50, dim_fecha, dim_producto, dim_cliente, dim_vendedor)

        # El precio unitario debe estar dentro de ±20% del precio catálogo
        precio_catalogo = 100.0
        assert (df["precio_unitario"] >= precio_catalogo * 0.8).all()
        assert (df["precio_unitario"] <= precio_catalogo * 1.2).all()
