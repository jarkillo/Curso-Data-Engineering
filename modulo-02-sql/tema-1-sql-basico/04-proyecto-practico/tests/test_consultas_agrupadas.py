"""
Tests para el módulo de consultas agrupadas.

Estos tests validan las funciones con GROUP BY y HAVING.
"""

import pytest


class TestContarProductosPorCategoria:
    """Tests para contar_productos_por_categoria."""

    def test_retorna_conteo_por_categoria(self, db_en_memoria):
        """Debe retornar conteo de productos por categoría."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import contar_productos_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = contar_productos_por_categoria(conn)

        assert len(resultados) == 5  # 5 categorías diferentes
        assert all("categoria" in r and "cantidad" in r for r in resultados)

    def test_resultados_ordenados_por_cantidad_descendente(self, db_en_memoria):
        """Los resultados deben estar ordenados por cantidad descendente."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import contar_productos_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = contar_productos_por_categoria(conn)

        cantidades = [r["cantidad"] for r in resultados]
        assert cantidades == sorted(cantidades, reverse=True)

    def test_categoria_con_mas_productos_es_accesorios(self, db_en_memoria):
        """La categoría con más productos debe ser Accesorios (4)."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import contar_productos_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = contar_productos_por_categoria(conn)

        assert resultados[0]["categoria"] == "Accesorios"
        assert resultados[0]["cantidad"] == 4


class TestCalcularValorInventarioPorCategoria:
    """Tests para calcular_valor_inventario_por_categoria."""

    def test_retorna_valor_por_categoria(self, db_en_memoria):
        """Debe retornar valor de inventario por categoría."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import calcular_valor_inventario_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = calcular_valor_inventario_por_categoria(conn)

        assert len(resultados) == 5
        assert all("categoria" in r and "valor_inventario" in r for r in resultados)

    def test_resultados_ordenados_por_valor_descendente(self, db_en_memoria):
        """Los resultados deben estar ordenados por valor descendente."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import calcular_valor_inventario_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = calcular_valor_inventario_por_categoria(conn)

        valores = [r["valor_inventario"] for r in resultados]
        assert valores == sorted(valores, reverse=True)

    def test_categoria_con_mayor_valor_es_computadoras(self, db_en_memoria):
        """La categoría con mayor valor debe ser Computadoras."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import calcular_valor_inventario_por_categoria

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = calcular_valor_inventario_por_categoria(conn)

        assert resultados[0]["categoria"] == "Computadoras"
        # Valor aproximado: 47499.65
        assert resultados[0]["valor_inventario"] > 45000.0


class TestObtenerCategoriasConMasDeNProductos:
    """Tests para obtener_categorias_con_mas_de_n_productos."""

    def test_con_n_igual_1_retorna_dos_categorias(self, db_en_memoria):
        """Con N=1 debe retornar categorías con más de 1 producto."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import obtener_categorias_con_mas_de_n_productos

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_categorias_con_mas_de_n_productos(conn, 1)

        # Accesorios (4) y Computadoras (3)
        assert len(resultados) == 2

    def test_con_n_igual_2_retorna_dos_categorias(self, db_en_memoria):
        """Con N=2 debe retornar categorías con más de 2 productos."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import obtener_categorias_con_mas_de_n_productos

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_categorias_con_mas_de_n_productos(conn, 2)

        # Accesorios (4) y Computadoras (3)
        assert len(resultados) == 2

    def test_con_n_igual_3_retorna_una_categoria(self, db_en_memoria):
        """Con N=3 debe retornar solo Accesorios (4 productos)."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import obtener_categorias_con_mas_de_n_productos

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_categorias_con_mas_de_n_productos(conn, 3)

        assert len(resultados) == 1
        assert resultados[0]["categoria"] == "Accesorios"

    def test_con_n_muy_alto_retorna_vacio(self, db_en_memoria):
        """Con N muy alto debe retornar lista vacía."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import obtener_categorias_con_mas_de_n_productos

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = obtener_categorias_con_mas_de_n_productos(conn, 100)

        assert resultados == []

    def test_con_n_negativo_lanza_value_error(self, db_en_memoria):
        """Debe lanzar ValueError si N es negativo."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import obtener_categorias_con_mas_de_n_productos

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        with pytest.raises(ValueError):
            obtener_categorias_con_mas_de_n_productos(conn, -1)


class TestAnalizarVentasPorProducto:
    """Tests para analizar_ventas_por_producto."""

    def test_retorna_analisis_de_ventas(self, db_en_memoria):
        """Debe retornar análisis de ventas por producto."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import analizar_ventas_por_producto

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = analizar_ventas_por_producto(conn)

        assert len(resultados) > 0
        assert all("producto_id" in r for r in resultados)
        assert all("unidades_vendidas" in r for r in resultados)
        assert all("ingresos_totales" in r for r in resultados)

    def test_resultados_ordenados_por_ingresos_descendente(self, db_en_memoria):
        """Los resultados deben estar ordenados por ingresos descendente."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import analizar_ventas_por_producto

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = analizar_ventas_por_producto(conn)

        ingresos = [r["ingresos_totales"] for r in resultados]
        assert ingresos == sorted(ingresos, reverse=True)

    def test_producto_con_mas_ingresos_es_laptop_hp(self, db_en_memoria):
        """El producto con más ingresos debe ser Laptop HP (producto_id=1)."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agrupadas import analizar_ventas_por_producto

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        resultados = analizar_ventas_por_producto(conn)

        # Laptop HP vendió 3 unidades a 899.99 = 2699.97
        assert resultados[0]["producto_id"] == 1
        assert resultados[0]["unidades_vendidas"] == 3
        assert 2690.0 < resultados[0]["ingresos_totales"] < 2710.0
