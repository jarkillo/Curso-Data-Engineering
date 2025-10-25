"""
Tests para el módulo de conexión a PostgreSQL.

Incluye tests para crear, cerrar y ejecutar queries en conexiones.
"""

from unittest.mock import Mock, patch

import psycopg2
import pytest
from src.conexion import cerrar_conexion, crear_conexion, ejecutar_query


class TestCrearConexion:
    """Tests para la función crear_conexion."""

    def test_crear_conexion_con_parametros(self):
        """Debe crear conexión con parámetros explícitos."""
        with patch("psycopg2.connect") as mock_connect:
            mock_conn = Mock()
            mock_connect.return_value = mock_conn

            conn = crear_conexion(
                host="localhost",
                port=5432,
                user="test_user",
                password="test_pass",
                database="test_db",
            )

            assert conn == mock_conn
            mock_connect.assert_called_once()

    def test_crear_conexion_sin_credenciales_lanza_error(self):
        """Debe lanzar ValueError si faltan credenciales."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="Faltan credenciales"):
                crear_conexion()

    def test_crear_conexion_usa_variables_entorno(self):
        """Debe usar variables de entorno si no se pasan parámetros."""
        env_vars = {
            "POSTGRES_HOST": "env_host",
            "POSTGRES_PORT": "5433",
            "POSTGRES_USER": "env_user",
            "POSTGRES_PASSWORD": "env_pass",
            "POSTGRES_DB": "env_db",
        }

        with patch.dict("os.environ", env_vars):
            with patch("psycopg2.connect") as mock_connect:
                mock_conn = Mock()
                mock_connect.return_value = mock_conn

                conn = crear_conexion()

                assert conn == mock_conn
                call_args = mock_connect.call_args[1]
                assert call_args["host"] == "env_host"
                assert call_args["port"] == 5433
                assert call_args["user"] == "env_user"

    def test_crear_conexion_error_psycopg2(self):
        """Debe propagar error de psycopg2 si falla conexión."""
        with patch("psycopg2.connect") as mock_connect:
            mock_connect.side_effect = psycopg2.Error("Connection failed")

            with pytest.raises(psycopg2.Error, match="Error al conectar"):
                crear_conexion(
                    host="localhost",
                    port=5432,
                    user="user",
                    password="pass",
                    database="db",
                )


class TestCerrarConexion:
    """Tests para la función cerrar_conexion."""

    def test_cerrar_conexion_exitosa(self, conn_mock):
        """Debe cerrar conexión correctamente."""
        cerrar_conexion(conn_mock)
        assert conn_mock.closed == 1

    def test_cerrar_conexion_ya_cerrada(self):
        """No debe fallar si la conexión ya está cerrada."""
        mock_conn = Mock()
        mock_conn.closed = 1

        # No debe lanzar error
        cerrar_conexion(mock_conn)

    def test_cerrar_conexion_tipo_invalido(self):
        """Debe lanzar TypeError si no es una conexión."""
        with pytest.raises(TypeError, match="conexión psycopg2"):
            cerrar_conexion("not_a_connection")

        with pytest.raises(TypeError, match="conexión psycopg2"):
            cerrar_conexion(123)


class TestEjecutarQuery:
    """Tests para la función ejecutar_query."""

    def test_ejecutar_query_select_simple(self, conn_mock):
        """Debe ejecutar SELECT y retornar resultados."""
        query = "SELECT 1 + 1"
        resultados = ejecutar_query(conn_mock, query)

        assert isinstance(resultados, list)

    def test_ejecutar_query_con_parametros(self, conn_mock):
        """Debe ejecutar query con parámetros."""
        query = "SELECT * FROM tabla WHERE id = %s"
        params = (1,)

        resultados = ejecutar_query(conn_mock, query, params)
        assert isinstance(resultados, list)

    def test_ejecutar_query_conexion_invalida(self):
        """Debe lanzar TypeError si conn no es válida."""
        with pytest.raises(TypeError, match="conexión psycopg2"):
            ejecutar_query("not_a_connection", "SELECT 1")

    def test_ejecutar_query_error_sql(self):
        """Debe lanzar psycopg2.Error si falla la query."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = psycopg2.Error("SQL error")
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        with pytest.raises(psycopg2.Error, match="Error al ejecutar query"):
            ejecutar_query(mock_conn, "INVALID SQL")
