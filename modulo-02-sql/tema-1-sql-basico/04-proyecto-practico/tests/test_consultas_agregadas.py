"""
Tests para el módulo de consultas agregadas.

Estos tests validan las funciones con COUNT, SUM, AVG, MAX, MIN.
"""


class TestContarProductos:
    """Tests para contar_productos."""

    def test_cuenta_todos_los_productos(self, db_en_memoria):
        """Debe retornar el número total de productos (10)."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agregadas import contar_productos

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        total = contar_productos(conn)

        assert total == 10
        assert isinstance(total, int)


class TestCalcularPrecioPromedio:
    """Tests para calcular_precio_promedio."""

    def test_calcula_precio_promedio_correcto(self, db_en_memoria):
        """Debe calcular el precio promedio correctamente."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agregadas import calcular_precio_promedio

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        promedio = calcular_precio_promedio(conn)

        # Precio promedio esperado: suma de todos / 10
        # Aproximadamente 697.99
        assert isinstance(promedio, float)
        assert 690.0 < promedio < 710.0

    def test_promedio_redondeado_a_dos_decimales(self, db_en_memoria):
        """El promedio debe estar redondeado a 2 decimales."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agregadas import calcular_precio_promedio

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        promedio = calcular_precio_promedio(conn)

        # Verificar que tiene máximo 2 decimales
        assert round(promedio, 2) == promedio


class TestObtenerEstadisticasPrecios:
    """Tests para obtener_estadisticas_precios."""

    def test_retorna_diccionario_con_todas_las_claves(self, db_en_memoria):
        """Debe retornar diccionario con minimo, maximo, promedio, total."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agregadas import obtener_estadisticas_precios

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        stats = obtener_estadisticas_precios(conn)

        assert isinstance(stats, dict)
        assert "minimo" in stats
        assert "maximo" in stats
        assert "promedio" in stats
        assert "total" in stats

    def test_valores_estadisticos_correctos(self, db_en_memoria):
        """Los valores estadísticos deben ser correctos."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agregadas import obtener_estadisticas_precios

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        stats = obtener_estadisticas_precios(conn)

        # Producto más barato: Webcam (79.99)
        assert stats["minimo"] == 79.99
        # Producto más caro: MacBook Pro (1999.99)
        assert stats["maximo"] == 1999.99
        # Total de productos
        assert stats["total"] == 10
        # Promedio
        assert 690.0 < stats["promedio"] < 710.0


class TestCalcularIngresosTotales:
    """Tests para calcular_ingresos_totales."""

    def test_calcula_ingresos_totales_correctos(self, db_en_memoria):
        """Debe calcular los ingresos totales correctamente."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agregadas import calcular_ingresos_totales

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        ingresos = calcular_ingresos_totales(conn)

        # Ingresos esperados: suma de (cantidad * precio_unitario)
        # Aproximadamente 10299.67
        assert isinstance(ingresos, float)
        assert 10200.0 < ingresos < 10400.0

    def test_ingresos_redondeados_a_dos_decimales(self, db_en_memoria):
        """Los ingresos deben estar redondeados a 2 decimales."""
        from src.conexion_db import ConexionSQLite
        from src.consultas_agregadas import calcular_ingresos_totales

        conn = ConexionSQLite(":memory:")
        conn.conexion = db_en_memoria

        ingresos = calcular_ingresos_totales(conn)

        assert round(ingresos, 2) == ingresos
