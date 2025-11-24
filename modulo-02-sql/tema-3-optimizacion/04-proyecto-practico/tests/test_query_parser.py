"""
Tests para query_parser.py

Siguiendo TDD: Tests escritos ANTES de la implementación.
"""

import pytest

from src.query_parser import (
    detectar_funciones_en_where,
    detectar_select_asterisco,
    extraer_columnas_select,
    extraer_columnas_where,
    extraer_joins,
    extraer_tablas,
)


class TestExtraerTablas:
    """Tests para extraer_tablas()."""

    def test_query_simple_una_tabla(self):
        """Debe extraer nombre de tabla en consulta simple."""
        query = "SELECT * FROM usuarios"
        resultado = extraer_tablas(query)
        assert resultado == ["usuarios"]

    def test_query_con_join_dos_tablas(self):
        """Debe extraer ambas tablas en JOIN."""
        query = "SELECT * FROM usuarios u JOIN pedidos p ON u.id = p.usuario_id"
        resultado = extraer_tablas(query)
        assert set(resultado) == {"usuarios", "pedidos"}

    def test_query_con_tres_tablas(self):
        """Debe extraer tres tablas."""
        query = """
        SELECT * FROM usuarios u
        JOIN pedidos p ON u.id = p.usuario_id
        JOIN productos pr ON p.producto_id = pr.id
        """
        resultado = extraer_tablas(query)
        assert set(resultado) == {"usuarios", "pedidos", "productos"}

    def test_query_vacio_levanta_error(self):
        """Debe levantar ValueError si query está vacío."""
        with pytest.raises(ValueError, match="vacío"):
            extraer_tablas("")

    def test_query_sin_from_levanta_error(self):
        """Debe levantar ValueError si no tiene FROM."""
        with pytest.raises(ValueError, match="FROM"):
            extraer_tablas("SELECT 1+1")


class TestExtraerColumnasWhere:
    """Tests para extraer_columnas_where()."""

    def test_where_una_columna(self):
        """Debe extraer columna en WHERE simple."""
        query = "SELECT * FROM usuarios WHERE email = 'test@example.com'"
        resultado = extraer_columnas_where(query)
        assert resultado == ["email"]

    def test_where_multiple_columnas(self):
        """Debe extraer todas las columnas en WHERE con AND."""
        query = "SELECT * FROM usuarios WHERE edad > 25 AND ciudad = 'Madrid' AND activo = true"
        resultado = extraer_columnas_where(query)
        assert set(resultado) == {"edad", "ciudad", "activo"}

    def test_where_con_or(self):
        """Debe extraer columnas con OR."""
        query = "SELECT * FROM productos WHERE categoria = 'A' OR categoria = 'B'"
        resultado = extraer_columnas_where(query)
        assert "categoria" in resultado

    def test_sin_where_retorna_lista_vacia(self):
        """Debe retornar lista vacía si no hay WHERE."""
        query = "SELECT * FROM usuarios"
        resultado = extraer_columnas_where(query)
        assert resultado == []

    def test_where_con_funcion_extrae_columna(self):
        """Debe extraer columna aunque tenga función."""
        query = "SELECT * FROM ventas WHERE YEAR(fecha) = 2024"
        resultado = extraer_columnas_where(query)
        assert "fecha" in resultado


class TestExtraerColumnasSelect:
    """Tests para extraer_columnas_select()."""

    def test_select_columnas_especificas(self):
        """Debe extraer columnas nombradas en SELECT."""
        query = "SELECT id, nombre, email FROM usuarios"
        resultado = extraer_columnas_select(query)
        assert set(resultado) == {"id", "nombre", "email"}

    def test_select_asterisco_retorna_asterisco(self):
        """Debe retornar ['*'] si usa SELECT *."""
        query = "SELECT * FROM usuarios"
        resultado = extraer_columnas_select(query)
        assert resultado == ["*"]

    def test_select_con_alias(self):
        """Debe extraer columnas ignorando alias."""
        query = "SELECT u.id, u.nombre as nombre_completo FROM usuarios u"
        resultado = extraer_columnas_select(query)
        assert "id" in resultado
        assert "nombre" in resultado

    def test_select_con_agregaciones(self):
        """Debe extraer columnas dentro de agregaciones."""
        query = "SELECT COUNT(id), SUM(monto) FROM ventas"
        resultado = extraer_columnas_select(query)
        assert "id" in resultado
        assert "monto" in resultado


class TestDetectarSelectAsterisco:
    """Tests para detectar_select_asterisco()."""

    def test_detecta_select_asterisco(self):
        """Debe retornar True si usa SELECT *."""
        query = "SELECT * FROM usuarios"
        assert detectar_select_asterisco(query) is True

    def test_no_detecta_cuando_columnas_especificas(self):
        """Debe retornar False si selecciona columnas específicas."""
        query = "SELECT id, nombre FROM usuarios"
        assert detectar_select_asterisco(query) is False

    def test_detecta_asterisco_con_alias(self):
        """Debe detectar SELECT u.* con alias de tabla."""
        query = "SELECT u.* FROM usuarios u"
        assert detectar_select_asterisco(query) is True


class TestDetectarFuncionesEnWhere:
    """Tests para detectar_funciones_en_where()."""

    def test_detecta_year_en_where(self):
        """Debe detectar función YEAR() en WHERE."""
        query = "SELECT * FROM ventas WHERE YEAR(fecha) = 2024"
        resultado = detectar_funciones_en_where(query)
        assert "YEAR" in resultado["funciones"]
        assert "fecha" in resultado["columnas_afectadas"]

    def test_detecta_upper_en_where(self):
        """Debe detectar función UPPER() en WHERE."""
        query = "SELECT * FROM usuarios WHERE UPPER(email) = 'TEST@EXAMPLE.COM'"
        resultado = detectar_funciones_en_where(query)
        assert "UPPER" in resultado["funciones"]
        assert "email" in resultado["columnas_afectadas"]

    def test_detecta_multiples_funciones(self):
        """Debe detectar múltiples funciones en WHERE."""
        query = "SELECT * FROM datos WHERE DATE(timestamp) = '2024-01-01' AND LOWER(nombre) = 'test'"
        resultado = detectar_funciones_en_where(query)
        assert len(resultado["funciones"]) >= 2
        assert "DATE" in resultado["funciones"]
        assert "LOWER" in resultado["funciones"]

    def test_sin_funciones_retorna_listas_vacias(self):
        """Debe retornar listas vacías si no hay funciones."""
        query = "SELECT * FROM usuarios WHERE edad > 25"
        resultado = detectar_funciones_en_where(query)
        assert resultado["funciones"] == []
        assert resultado["columnas_afectadas"] == []


class TestExtraerJoins:
    """Tests para extraer_joins()."""

    def test_detecta_inner_join(self):
        """Debe detectar INNER JOIN."""
        query = "SELECT * FROM usuarios u INNER JOIN pedidos p ON u.id = p.usuario_id"
        resultado = extraer_joins(query)
        assert len(resultado) == 1
        assert resultado[0]["tipo"] == "INNER JOIN"
        assert resultado[0]["tabla"] == "pedidos"

    def test_detecta_left_join(self):
        """Debe detectar LEFT JOIN."""
        query = "SELECT * FROM usuarios u LEFT JOIN pedidos p ON u.id = p.usuario_id"
        resultado = extraer_joins(query)
        assert resultado[0]["tipo"] == "LEFT JOIN"

    def test_detecta_multiple_joins(self):
        """Debe detectar múltiples JOINs."""
        query = """
        SELECT * FROM usuarios u
        INNER JOIN pedidos p ON u.id = p.usuario_id
        LEFT JOIN productos pr ON p.producto_id = pr.id
        """
        resultado = extraer_joins(query)
        assert len(resultado) == 2

    def test_sin_joins_retorna_lista_vacia(self):
        """Debe retornar lista vacía si no hay JOINs."""
        query = "SELECT * FROM usuarios WHERE edad > 25"
        resultado = extraer_joins(query)
        assert resultado == []

    def test_extrae_columnas_join(self):
        """Debe extraer columnas en condición de JOIN."""
        query = "SELECT * FROM usuarios u INNER JOIN pedidos p ON u.id = p.usuario_id"
        resultado = extraer_joins(query)
        assert "id" in resultado[0]["columnas_join"]
        assert "usuario_id" in resultado[0]["columnas_join"]
