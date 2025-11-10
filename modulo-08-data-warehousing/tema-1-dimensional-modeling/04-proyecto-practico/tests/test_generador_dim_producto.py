"""
Tests para generador_dim_producto.py.

Tests escritos PRIMERO siguiendo TDD.
"""

import pandas as pd
import pytest


class TestGenerarDimProducto:
    """Tests para la función generar_dim_producto."""

    def test_generar_100_productos(self):
        """Should generate exactly 100 products."""
        from src.generador_dim_producto import generar_dim_producto

        productos = generar_dim_producto(100)

        assert isinstance(productos, pd.DataFrame)
        assert len(productos) == 100

    def test_tiene_columnas_requeridas(self):
        """Should have all required columns."""
        from src.generador_dim_producto import generar_dim_producto

        productos = generar_dim_producto(10)

        columnas_esperadas = [
            "producto_id",
            "sku",
            "nombre_producto",
            "marca",
            "categoria",
            "subcategoria",
            "precio_catalogo",
            "peso_kg",
            "requiere_refrigeracion",
        ]

        for col in columnas_esperadas:
            assert col in productos.columns, f"Falta columna: {col}"

    def test_producto_id_es_unico(self):
        """Should have unique producto_id."""
        from src.generador_dim_producto import generar_dim_producto

        productos = generar_dim_producto(50)

        assert productos["producto_id"].is_unique

    def test_sku_es_unico(self):
        """Should have unique SKU."""
        from src.generador_dim_producto import generar_dim_producto

        productos = generar_dim_producto(50)

        assert productos["sku"].is_unique

    def test_precio_catalogo_positivo(self):
        """Should have positive catalog prices."""
        from src.generador_dim_producto import generar_dim_producto

        productos = generar_dim_producto(50)

        assert (productos["precio_catalogo"] > 0).all()

    def test_peso_positivo(self):
        """Should have positive weight."""
        from src.generador_dim_producto import generar_dim_producto

        productos = generar_dim_producto(50)

        assert (productos["peso_kg"] > 0).all()

    def test_categorias_validas(self):
        """Should have valid categories."""
        from src.generador_dim_producto import generar_dim_producto

        productos = generar_dim_producto(100)

        categorias_validas = [
            "Electrónica",
            "Ropa",
            "Hogar",
            "Deportes",
            "Libros",
        ]

        # Todas las categorías deben estar en la lista válida
        categorias_unicas = productos["categoria"].unique()
        for cat in categorias_unicas:
            assert cat in categorias_validas

    def test_num_productos_cero_raise_error(self):
        """Should raise ValueError if num_productos is 0."""
        from src.generador_dim_producto import generar_dim_producto

        with pytest.raises(ValueError, match="debe ser mayor que 0"):
            generar_dim_producto(0)

    def test_num_productos_negativo_raise_error(self):
        """Should raise ValueError if num_productos is negative."""
        from src.generador_dim_producto import generar_dim_producto

        with pytest.raises(ValueError, match="debe ser mayor que 0"):
            generar_dim_producto(-10)


class TestAsignarCategoria:
    """Tests para la función asignar_categoria."""

    def test_laptop_es_electronica(self):
        """Should categorize laptop as Electrónica."""
        from src.generador_dim_producto import asignar_categoria

        categoria, subcategoria = asignar_categoria("Laptop Dell Inspiron 15")

        assert categoria == "Electrónica"
        assert subcategoria == "Computadoras"

    def test_celular_es_electronica(self):
        """Should categorize phone as Electrónica."""
        from src.generador_dim_producto import asignar_categoria

        categoria, subcategoria = asignar_categoria("iPhone 15 Pro")

        assert categoria == "Electrónica"
        assert subcategoria == "Celulares"

    def test_camisa_es_ropa(self):
        """Should categorize shirt as Ropa."""
        from src.generador_dim_producto import asignar_categoria

        categoria, subcategoria = asignar_categoria("Camisa Polo Azul")

        assert categoria == "Ropa"

    def test_libro_es_libros(self):
        """Should categorize book as Libros."""
        from src.generador_dim_producto import asignar_categoria

        categoria, subcategoria = asignar_categoria("Cien Años de Soledad")

        assert categoria == "Libros"

    def test_producto_sin_match_categoria_general(self):
        """Should assign 'General' category to unmatched products."""
        from src.generador_dim_producto import asignar_categoria

        categoria, subcategoria = asignar_categoria("Producto Desconocido XYZ")

        assert categoria == "General"
        assert subcategoria == "Otros"
