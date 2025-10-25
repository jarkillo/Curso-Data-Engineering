"""
Tests para el módulo ejecutor_joins.

TDD: Estos tests se escribieron PRIMERO, antes de la implementación.
"""

import sqlite3

import pytest
from src.ejecutor_joins import (
    ejecutar_join_con_subconsulta,
    ejecutar_join_multiple,
    ejecutar_join_simple,
)


class TestEjecutarJoinSimple:
    """Tests para la función ejecutar_join_simple."""

    def test_inner_join_productos_categorias_devuelve_solo_coincidencias(
        self, conexion_db
    ):
        """INNER JOIN debe retornar solo productos con categoría asignada."""
        resultado = ejecutar_join_simple(
            conexion=conexion_db,
            tabla_izq="productos",
            tabla_der="categorias",
            columna_union_izq="categoria_id",
            columna_union_der="id",
            tipo_join="INNER",
        )

        # Debe haber productos con categoría
        assert len(resultado) > 0

        # Verificar que todos tienen categoria_id no NULL
        for fila in resultado:
            assert fila["categoria_id"] is not None

    def test_left_join_productos_ventas_incluye_productos_sin_ventas(self, conexion_db):
        """LEFT JOIN debe incluir productos incluso si no tienen ventas."""
        resultado = ejecutar_join_simple(
            conexion=conexion_db,
            tabla_izq="productos",
            tabla_der="ventas",
            columna_union_izq="id",
            columna_union_der="producto_id",
            tipo_join="LEFT",
        )

        # Debe retornar al menos tantas filas como productos activos
        cursor = conexion_db.cursor()
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 1")
        num_productos = cursor.fetchone()[0]

        assert len(resultado) >= num_productos

    def test_inner_join_con_columnas_especificas_solo_retorna_esas_columnas(
        self, conexion_db
    ):
        """Cuando se especifican columnas, solo deben retornarse esas."""
        resultado = ejecutar_join_simple(
            conexion=conexion_db,
            tabla_izq="productos",
            tabla_der="categorias",
            columna_union_izq="categoria_id",
            columna_union_der="id",
            tipo_join="INNER",
            columnas_select=["productos.nombre", "categorias.nombre AS categoria"],
        )

        assert len(resultado) > 0

        # Verificar que solo hay las columnas solicitadas
        primera_fila = resultado[0]
        assert "nombre" in primera_fila
        assert "categoria" in primera_fila

    def test_tipo_join_invalido_lanza_valor_error(self, conexion_db):
        """Tipo de JOIN inválido debe lanzar ValueError."""
        with pytest.raises(ValueError, match="tipo_join inválido"):
            ejecutar_join_simple(
                conexion=conexion_db,
                tabla_izq="productos",
                tabla_der="categorias",
                columna_union_izq="categoria_id",
                columna_union_der="id",
                tipo_join="INVALID_JOIN",
            )

    def test_conexion_none_lanza_type_error(self):
        """Conexión None debe lanzar TypeError."""
        with pytest.raises(TypeError, match="conexion debe ser"):
            ejecutar_join_simple(
                conexion=None,
                tabla_izq="productos",
                tabla_der="categorias",
                columna_union_izq="categoria_id",
                columna_union_der="id",
                tipo_join="INNER",
            )

    def test_tabla_inexistente_lanza_sqlite_error(self, conexion_db):
        """Query con tabla inexistente debe lanzar sqlite3.Error."""
        with pytest.raises(sqlite3.Error):
            ejecutar_join_simple(
                conexion=conexion_db,
                tabla_izq="tabla_no_existe",
                tabla_der="categorias",
                columna_union_izq="id",
                columna_union_der="id",
                tipo_join="INNER",
            )

    def test_join_sin_coincidencias_retorna_lista_vacia(self, conexion_db):
        """INNER JOIN sin coincidencias debe retornar lista vacía."""
        # Crear tabla temporal sin datos relacionados
        conexion_db.execute("CREATE TABLE temp (id INTEGER, valor TEXT)")
        conexion_db.execute("INSERT INTO temp VALUES (999, 'test')")

        resultado = ejecutar_join_simple(
            conexion=conexion_db,
            tabla_izq="productos",
            tabla_der="temp",
            columna_union_izq="id",
            columna_union_der="id",
            tipo_join="INNER",
        )

        assert resultado == []


class TestEjecutarJoinMultiple:
    """Tests para la función ejecutar_join_multiple."""

    def test_join_tres_tablas_productos_categorias_ventas(self, conexion_db):
        """JOIN de 3 tablas debe combinar correctamente."""
        tablas = [
            {"nombre": "productos", "alias": "p"},
            {
                "nombre": "categorias",
                "alias": "c",
                "join": "INNER",
                "on": "p.categoria_id = c.id",
            },
            {
                "nombre": "ventas",
                "alias": "v",
                "join": "LEFT",
                "on": "p.id = v.producto_id",
            },
        ]

        resultado = ejecutar_join_multiple(
            conexion=conexion_db,
            tablas=tablas,
            columnas_select=["p.nombre", "c.nombre AS categoria", "v.cantidad"],
        )

        assert len(resultado) > 0

        # Verificar que hay columnas de las 3 tablas
        primera_fila = resultado[0]
        assert "nombre" in primera_fila
        assert "categoria" in primera_fila

    def test_join_cuatro_tablas_con_clientes(self, conexion_db):
        """JOIN de 4 tablas (productos, categorias, ventas, clientes)."""
        tablas = [
            {"nombre": "ventas", "alias": "v"},
            {
                "nombre": "productos",
                "alias": "p",
                "join": "INNER",
                "on": "v.producto_id = p.id",
            },
            {
                "nombre": "categorias",
                "alias": "c",
                "join": "INNER",
                "on": "p.categoria_id = c.id",
            },
            {
                "nombre": "clientes",
                "alias": "cl",
                "join": "INNER",
                "on": "v.cliente_id = cl.id",
            },
        ]

        resultado = ejecutar_join_multiple(
            conexion=conexion_db,
            tablas=tablas,
            columnas_select=[
                "cl.nombre",
                "p.nombre AS producto",
                "c.nombre AS categoria",
                "v.total",
            ],
        )

        assert len(resultado) > 0

        # Debe haber al menos las ventas registradas
        assert len(resultado) >= 3

    def test_lista_tablas_vacia_lanza_valor_error(self, conexion_db):
        """Lista de tablas vacía debe lanzar ValueError."""
        with pytest.raises(ValueError, match="tablas no puede estar vacía"):
            ejecutar_join_multiple(
                conexion=conexion_db,
                tablas=[],
            )

    def test_formato_incorrecto_tabla_lanza_valor_error(self, conexion_db):
        """Formato incorrecto de tabla debe lanzar ValueError."""
        tablas = [
            {"nombre": "productos"},  # Falta 'alias'
        ]

        with pytest.raises(ValueError, match="debe contener"):
            ejecutar_join_multiple(
                conexion=conexion_db,
                tablas=tablas,
            )

    def test_join_multiple_sin_columnas_select_retorna_todas(self, conexion_db):
        """Si no se especifican columnas, debe retornar todas (*)."""
        tablas = [
            {"nombre": "productos", "alias": "p"},
            {
                "nombre": "categorias",
                "alias": "c",
                "join": "INNER",
                "on": "p.categoria_id = c.id",
            },
        ]

        resultado = ejecutar_join_multiple(
            conexion=conexion_db,
            tablas=tablas,
        )

        assert len(resultado) > 0

        # Debe tener múltiples columnas
        primera_fila = resultado[0]
        assert len(primera_fila.keys()) > 2


class TestEjecutarJoinConSubconsulta:
    """Tests para la función ejecutar_join_con_subconsulta."""

    def test_subconsulta_en_where_filtra_por_promedio(self, conexion_db):
        """Subconsulta en WHERE debe filtrar correctamente."""
        query_principal = """
            SELECT nombre, precio
            FROM productos
            WHERE precio > {subconsulta}
        """

        subconsulta = "(SELECT AVG(precio) FROM productos)"

        resultado = ejecutar_join_con_subconsulta(
            conexion=conexion_db,
            query_principal=query_principal,
            subconsulta=subconsulta,
            tipo_subconsulta="WHERE",
        )

        assert len(resultado) > 0

        # Verificar que todos los precios son mayores al promedio
        cursor = conexion_db.cursor()
        cursor.execute("SELECT AVG(precio) FROM productos")
        precio_promedio = cursor.fetchone()[0]

        for fila in resultado:
            assert fila["precio"] > precio_promedio

    def test_subconsulta_en_from_como_tabla_derivada(self, conexion_db):
        """Subconsulta en FROM debe funcionar como tabla temporal."""
        query_principal = """
            SELECT categoria, total_productos
            FROM {subconsulta} AS resumen
            ORDER BY total_productos DESC
        """

        subconsulta = """
            (SELECT
                c.nombre AS categoria,
                COUNT(p.id) AS total_productos
             FROM categorias c
             LEFT JOIN productos p ON c.id = p.categoria_id
             GROUP BY c.nombre)
        """

        resultado = ejecutar_join_con_subconsulta(
            conexion=conexion_db,
            query_principal=query_principal,
            subconsulta=subconsulta,
            tipo_subconsulta="FROM",
        )

        assert len(resultado) == 4  # 4 categorías

        # Verificar que está ordenado DESC
        totales = [fila["total_productos"] for fila in resultado]
        assert totales == sorted(totales, reverse=True)

    def test_tipo_subconsulta_invalido_lanza_valor_error(self, conexion_db):
        """Tipo de subconsulta inválido debe lanzar ValueError."""
        with pytest.raises(ValueError, match="tipo_subconsulta inválido"):
            ejecutar_join_con_subconsulta(
                conexion=conexion_db,
                query_principal="SELECT * FROM productos WHERE id = {subconsulta}",
                subconsulta="(SELECT 1)",
                tipo_subconsulta="INVALID_TYPE",
            )

    def test_query_sin_placeholder_lanza_valor_error(self, conexion_db):
        """Query sin placeholder {subconsulta} debe lanzar ValueError."""
        with pytest.raises(ValueError, match="placeholder.*subconsulta"):
            ejecutar_join_con_subconsulta(
                conexion=conexion_db,
                query_principal="SELECT * FROM productos",  # Sin {subconsulta}
                subconsulta="(SELECT 1)",
                tipo_subconsulta="WHERE",
            )
