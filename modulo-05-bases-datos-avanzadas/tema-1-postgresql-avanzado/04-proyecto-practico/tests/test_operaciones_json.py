"""
Tests para el módulo de operaciones JSON.

Incluye tests para inserción, consulta y actualización de datos JSONB.
"""

from unittest.mock import Mock

import psycopg2
import pytest
from src.operaciones_json import (
    actualizar_campo_json,
    consultar_json_por_campo,
    insertar_json,
)


class TestInsertarJson:
    """Tests para la función insertar_json."""

    def test_insertar_json_exitoso(self):
        """Debe insertar JSON y retornar ID."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (42,)
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        datos = {"user": "ana", "edad": 30}
        id_insertado = insertar_json(mock_conn, "eventos", "datos", datos)

        assert id_insertado == 42
        mock_conn.commit.assert_called_once()

    def test_insertar_json_datos_no_dict(self):
        """Debe lanzar TypeError si datos no es diccionario."""
        mock_conn = Mock()

        with pytest.raises(TypeError, match="deben ser un diccionario"):
            insertar_json(mock_conn, "tabla", "columna", "not_a_dict")

        with pytest.raises(TypeError, match="deben ser un diccionario"):
            insertar_json(mock_conn, "tabla", "columna", [1, 2, 3])

    def test_insertar_json_tabla_vacia(self):
        """Debe lanzar ValueError si tabla está vacía."""
        mock_conn = Mock()

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            insertar_json(mock_conn, "", "columna", {})

    def test_insertar_json_columna_vacia(self):
        """Debe lanzar ValueError si columna_json está vacía."""
        mock_conn = Mock()

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            insertar_json(mock_conn, "tabla", "", {})

    def test_insertar_json_error_db(self):
        """Debe lanzar psycopg2.Error si falla inserción."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = psycopg2.Error("DB error")
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        with pytest.raises(psycopg2.Error, match="Error al insertar JSON"):
            insertar_json(mock_conn, "tabla", "columna", {"key": "value"})

        mock_conn.rollback.assert_called_once()

    def test_insertar_json_sin_id_retornado(self):
        """Debe lanzar error si no se obtiene ID."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        with pytest.raises(psycopg2.Error, match="No se pudo obtener el ID"):
            insertar_json(mock_conn, "tabla", "columna", {})


class TestConsultarJsonPorCampo:
    """Tests para la función consultar_json_por_campo."""

    def test_consultar_json_encuentra_resultados(self):
        """Debe retornar lista de resultados encontrados."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, {"user": "ana", "edad": 30}),
            (2, {"user": "ana", "edad": 25}),
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        resultados = consultar_json_por_campo(
            mock_conn, "eventos", "datos", "user", "ana"
        )

        assert len(resultados) == 2
        assert resultados[0]["id"] == 1
        assert resultados[0]["datos"]["user"] == "ana"

    def test_consultar_json_sin_resultados(self):
        """Debe retornar lista vacía si no encuentra resultados."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        resultados = consultar_json_por_campo(
            mock_conn, "eventos", "datos", "user", "no_existe"
        )

        assert resultados == []

    def test_consultar_json_parametros_vacios(self):
        """Debe lanzar ValueError si parámetros están vacíos."""
        mock_conn = Mock()

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            consultar_json_por_campo(mock_conn, "", "columna", "campo", "valor")

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            consultar_json_por_campo(mock_conn, "tabla", "", "campo", "valor")

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            consultar_json_por_campo(mock_conn, "tabla", "columna", "", "valor")

    def test_consultar_json_error_db(self):
        """Debe lanzar psycopg2.Error si falla consulta."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = psycopg2.Error("DB error")
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        with pytest.raises(psycopg2.Error, match="Error al consultar JSON"):
            consultar_json_por_campo(mock_conn, "tabla", "columna", "campo", "valor")


class TestActualizarCampoJson:
    """Tests para la función actualizar_campo_json."""

    def test_actualizar_campo_json_exitoso(self):
        """Debe actualizar campo y retornar True."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        resultado = actualizar_campo_json(
            mock_conn, "eventos", "datos", 1, "status", "procesado"
        )

        assert resultado is True
        mock_conn.commit.assert_called_once()

    def test_actualizar_campo_json_sin_filas_afectadas(self):
        """Debe retornar False si no se actualizó ninguna fila."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        resultado = actualizar_campo_json(
            mock_conn, "eventos", "datos", 999, "status", "procesado"
        )

        assert resultado is False

    def test_actualizar_campo_json_parametros_vacios(self):
        """Debe lanzar ValueError si parámetros están vacíos."""
        mock_conn = Mock()

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            actualizar_campo_json(mock_conn, "", "columna", 1, "campo", "valor")

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            actualizar_campo_json(mock_conn, "tabla", "", 1, "campo", "valor")

        with pytest.raises(ValueError, match="no pueden estar vacíos"):
            actualizar_campo_json(mock_conn, "tabla", "columna", 1, "", "valor")

    def test_actualizar_campo_json_id_invalido(self):
        """Debe lanzar ValueError si ID es ≤ 0."""
        mock_conn = Mock()

        with pytest.raises(ValueError, match="debe ser mayor a 0"):
            actualizar_campo_json(mock_conn, "tabla", "columna", 0, "campo", "valor")

        with pytest.raises(ValueError, match="debe ser mayor a 0"):
            actualizar_campo_json(mock_conn, "tabla", "columna", -1, "campo", "valor")

    def test_actualizar_campo_json_error_db(self):
        """Debe lanzar psycopg2.Error si falla actualización."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = psycopg2.Error("DB error")
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        with pytest.raises(psycopg2.Error, match="Error al actualizar campo JSON"):
            actualizar_campo_json(mock_conn, "tabla", "columna", 1, "campo", "valor")

        mock_conn.rollback.assert_called_once()

    def test_actualizar_campo_json_con_valor_numerico(self):
        """Debe actualizar campo con valor numérico."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        resultado = actualizar_campo_json(
            mock_conn, "eventos", "datos", 1, "contador", 42
        )

        assert resultado is True

    def test_actualizar_campo_json_con_valor_bool(self):
        """Debe actualizar campo con valor booleano."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        resultado = actualizar_campo_json(
            mock_conn, "eventos", "datos", 1, "activo", True
        )

        assert resultado is True
