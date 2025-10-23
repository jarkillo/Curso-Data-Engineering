"""
Tests para el módulo de consultas básicas.

Estos tests validan las funciones de consultas SELECT, WHERE, ORDER BY, LIMIT.
"""

import pytest


class TestObtenerTodosLosProductos:
    """Tests para obtener_todos_los_productos."""

    def test_retorna_todos_los_productos(self, db_en_memoria):
        """Debe retornar todos los 10 productos."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_todos_los_productos

        conn = ConexionSQLite(":memory:")
        # Copiar datos de fixture
        conn.conexion = db_en_memoria

        resultados = obtener_todos_los_productos(conn)

        assert len(resultados) == 10
        assert all(isinstance(p, dict) for p in resultados)
        assert all("id" in p and "nombre" in p for p in resultados)

    def test_productos_tienen_todos_los_campos(self, db_en_memoria):
        """Los productos deben tener todos los campos esperados."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_todos_los_productos

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_todos_los_productos(conn)
        producto = resultados[0]

        assert "id" in producto
        assert "nombre" in producto
        assert "precio" in producto
        assert "categoria" in producto
        assert "stock_actual" in producto
        assert "proveedor" in producto


class TestFiltrarProductosPorCategoria:
    """Tests para filtrar_productos_por_categoria."""

    def test_filtrar_por_accesorios(self, db_en_memoria):
        """Debe retornar solo productos de categoría Accesorios."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import filtrar_productos_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = filtrar_productos_por_categoria(conn, "Accesorios")

        assert len(resultados) == 4
        assert all(p["categoria"] == "Accesorios" for p in resultados)

    def test_filtrar_por_computadoras(self, db_en_memoria):
        """Debe retornar solo productos de categoría Computadoras."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import filtrar_productos_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = filtrar_productos_por_categoria(conn, "Computadoras")

        assert len(resultados) == 3
        assert all(p["categoria"] == "Computadoras" for p in resultados)

    def test_filtrar_categoria_inexistente_retorna_vacio(self, db_en_memoria):
        """Debe retornar lista vacía si la categoría no existe."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import filtrar_productos_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = filtrar_productos_por_categoria(conn, "CategoriaInexistente")

        assert resultados == []

    def test_con_categoria_vacia_lanza_value_error(self, db_en_memoria):
        """Debe lanzar ValueError si la categoría está vacía."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import filtrar_productos_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        with pytest.raises(ValueError):
            filtrar_productos_por_categoria(conn, "")


class TestObtenerProductosCaros:
    """Tests para obtener_productos_caros."""

    def test_filtrar_productos_mayores_a_500(self, db_en_memoria):
        """Debe retornar productos con precio > 500."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_productos_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_productos_caros(conn, 500.0)

        assert len(resultados) == 5
        assert all(p["precio"] > 500.0 for p in resultados)

    def test_productos_ordenados_por_precio_descendente(self, db_en_memoria):
        """Los productos deben estar ordenados de más caro a más barato."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_productos_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_productos_caros(conn, 100.0)

        precios = [p["precio"] for p in resultados]
        assert precios == sorted(precios, reverse=True)

    def test_con_precio_negativo_lanza_value_error(self, db_en_memoria):
        """Debe lanzar ValueError si el precio es negativo."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_productos_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        with pytest.raises(ValueError):
            obtener_productos_caros(conn, -10.0)

    def test_con_precio_cero_lanza_value_error(self, db_en_memoria):
        """Debe lanzar ValueError si el precio es cero."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_productos_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        with pytest.raises(ValueError):
            obtener_productos_caros(conn, 0.0)


class TestObtenerTopNProductosMasCaros:
    """Tests para obtener_top_n_productos_mas_caros."""

    def test_obtener_top_5_productos(self, db_en_memoria):
        """Debe retornar los 5 productos más caros."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_top_n_productos_mas_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_top_n_productos_mas_caros(conn, 5)

        assert len(resultados) == 5
        # El más caro debe ser MacBook Pro (1999.99)
        assert resultados[0]["nombre"] == 'MacBook Pro 14"'
        assert resultados[0]["precio"] == 1999.99

    def test_obtener_top_3_productos(self, db_en_memoria):
        """Debe retornar los 3 productos más caros."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_top_n_productos_mas_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_top_n_productos_mas_caros(conn, 3)

        assert len(resultados) == 3

    def test_productos_ordenados_descendente(self, db_en_memoria):
        """Los productos deben estar ordenados de más caro a más barato."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_top_n_productos_mas_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_top_n_productos_mas_caros(conn, 5)

        precios = [p["precio"] for p in resultados]
        assert precios == sorted(precios, reverse=True)

    def test_con_n_mayor_que_total_retorna_todos(self, db_en_memoria):
        """Si N > total de productos, debe retornar todos."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_top_n_productos_mas_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_top_n_productos_mas_caros(conn, 100)

        assert len(resultados) == 10

    def test_con_n_cero_lanza_value_error(self, db_en_memoria):
        """Debe lanzar ValueError si N es cero."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_top_n_productos_mas_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        with pytest.raises(ValueError):
            obtener_top_n_productos_mas_caros(conn, 0)

    def test_con_n_negativo_lanza_value_error(self, db_en_memoria):
        """Debe lanzar ValueError si N es negativo."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_basicas import obtener_top_n_productos_mas_caros

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        with pytest.raises(ValueError):
            obtener_top_n_productos_mas_caros(conn, -5)
