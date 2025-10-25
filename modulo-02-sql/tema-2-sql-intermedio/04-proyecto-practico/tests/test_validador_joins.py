"""
Tests para el módulo validador_joins.

TDD: Estos tests se escribieron PRIMERO, antes de la implementación.
"""

import sqlite3

import pytest
from src.validador_joins import (
    contar_filas_join,
    detectar_producto_cartesiano,
    validar_resultado_join,
)


class TestValidarResultadoJoin:
    """Tests para la función validar_resultado_join."""

    def test_inner_join_resultado_valido(self):
        """INNER JOIN con resultado <= min(izq, der) es válido."""
        es_valido, mensaje = validar_resultado_join(
            filas_tabla_izq=100,
            filas_tabla_der=10,
            filas_resultado=8,
            tipo_join="INNER",
        )

        assert es_valido is True

    def test_inner_join_resultado_mayor_a_ambas_tablas_es_invalido(self):
        """INNER JOIN con resultado > ambas tablas es sospechoso."""
        es_valido, mensaje = validar_resultado_join(
            filas_tabla_izq=100,
            filas_tabla_der=10,
            filas_resultado=150,
            tipo_join="INNER",
        )

        assert es_valido is False
        assert "cartesian" in mensaje.lower() or "duplicación" in mensaje.lower()

    def test_left_join_resultado_menor_a_tabla_izq_es_invalido(self):
        """LEFT JOIN debe retornar al menos todas las filas de la izquierda."""
        es_valido, mensaje = validar_resultado_join(
            filas_tabla_izq=100,
            filas_tabla_der=10,
            filas_resultado=50,
            tipo_join="LEFT",
        )

        assert es_valido is False
        assert "pérdida" in mensaje.lower() or "menor" in mensaje.lower()

    def test_left_join_resultado_igual_a_tabla_izq_es_valido(self):
        """LEFT JOIN con resultado = tabla izq es válido."""
        es_valido, mensaje = validar_resultado_join(
            filas_tabla_izq=100,
            filas_tabla_der=10,
            filas_resultado=100,
            tipo_join="LEFT",
        )

        assert es_valido is True

    def test_full_join_resultado_menor_a_max_tablas_es_invalido(self):
        """FULL JOIN debe retornar al menos max(izq, der) filas."""
        es_valido, mensaje = validar_resultado_join(
            filas_tabla_izq=100,
            filas_tabla_der=50,
            filas_resultado=75,
            tipo_join="FULL",
        )

        assert es_valido is False

    def test_tipo_join_invalido_lanza_valor_error(self):
        """Tipo de JOIN inválido debe lanzar ValueError."""
        with pytest.raises(ValueError, match="tipo_join inválido"):
            validar_resultado_join(
                filas_tabla_izq=100,
                filas_tabla_der=10,
                filas_resultado=50,
                tipo_join="INVALID_JOIN",
            )


class TestDetectarProductoCartesiano:
    """Tests para la función detectar_producto_cartesiano."""

    def test_resultado_igual_a_producto_es_cartesiano(self):
        """Si resultado = izq × der, es producto cartesiano."""
        es_cartesiano, mensaje = detectar_producto_cartesiano(
            filas_izq=100, filas_der=50, filas_resultado=5000  # 100 × 50 = 5000
        )

        assert es_cartesiano is True
        assert "cartesian" in mensaje.lower() or "producto" in mensaje.lower()

    def test_resultado_cercano_a_producto_es_cartesiano(self):
        """Si resultado > 80% del producto, es sospechoso."""
        es_cartesiano, mensaje = detectar_producto_cartesiano(
            filas_izq=100,
            filas_der=50,
            filas_resultado=4500,  # 90% de 5000
            umbral=0.8,
        )

        assert es_cartesiano is True

    def test_resultado_pequeño_no_es_cartesiano(self):
        """Resultado pequeño no es producto cartesiano."""
        es_cartesiano, mensaje = detectar_producto_cartesiano(
            filas_izq=100, filas_der=50, filas_resultado=100  # Solo 100 filas
        )

        assert es_cartesiano is False

    def test_umbral_personalizado_funciona(self):
        """Umbral personalizado debe funcionar correctamente."""
        # Con umbral 0.5, 2500 (50% de 5000) debería detectarse
        es_cartesiano, _ = detectar_producto_cartesiano(
            filas_izq=100, filas_der=50, filas_resultado=2600, umbral=0.5
        )

        assert es_cartesiano is True

    def test_filas_cero_no_lanza_error(self):
        """Filas en 0 no debe causar división por cero."""
        es_cartesiano, mensaje = detectar_producto_cartesiano(
            filas_izq=0, filas_der=50, filas_resultado=0
        )

        # No debe lanzar excepción
        assert es_cartesiano is False


class TestContarFilasJoin:
    """Tests para la función contar_filas_join."""

    def test_cuenta_filas_de_tablas_y_resultado(self, conexion_db):
        """Debe contar correctamente filas de ambas tablas y resultado."""
        query_join = """
            SELECT p.*, c.nombre AS categoria
            FROM productos p
            INNER JOIN categorias c ON p.categoria_id = c.id
        """

        conteo = contar_filas_join(
            conexion=conexion_db,
            tabla_izq="productos",
            tabla_der="categorias",
            query_join=query_join,
        )

        assert "filas_izq" in conteo
        assert "filas_der" in conteo
        assert "filas_resultado" in conteo
        assert "ratio" in conteo

        # Verificar valores
        assert conteo["filas_izq"] == 10  # 10 productos en total
        assert conteo["filas_der"] == 4  # 4 categorías
        assert conteo["filas_resultado"] > 0

    def test_ratio_es_calculado_correctamente(self, conexion_db):
        """Ratio debe ser resultado / (izq × der)."""
        query_join = """
            SELECT * FROM productos p INNER JOIN categorias c
            ON p.categoria_id = c.id
        """

        conteo = contar_filas_join(
            conexion=conexion_db,
            tabla_izq="productos",
            tabla_der="categorias",
            query_join=query_join,
        )

        esperado_ratio = conteo["filas_resultado"] / (
            conteo["filas_izq"] * conteo["filas_der"]
        )

        assert abs(conteo["ratio"] - esperado_ratio) < 0.01  # Tolerancia

    def test_query_invalida_lanza_sqlite_error(self, conexion_db):
        """Query SQL inválida debe lanzar sqlite3.Error."""
        with pytest.raises(sqlite3.Error):
            contar_filas_join(
                conexion=conexion_db,
                tabla_izq="productos",
                tabla_der="categorias",
                query_join="SELECT * FROM tabla_no_existe",
            )
