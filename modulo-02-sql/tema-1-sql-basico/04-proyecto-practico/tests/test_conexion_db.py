"""
Tests para el módulo de conexión a base de datos.

Estos tests validan la clase ConexionSQLite siguiendo TDD.
"""

import os
import sqlite3
import tempfile

import pytest


class TestConexionSQLiteInit:
    """Tests para __init__ de ConexionSQLite."""

    def test_crear_conexion_en_memoria(self):
        """Debe crear conexión a base de datos en memoria."""
        from src.conexion_db import ConexionSQLite

        conn = ConexionSQLite(":memory:")
        assert conn.conexion is not None
        assert isinstance(conn.conexion, sqlite3.Connection)
        conn.cerrar()

    def test_crear_conexion_a_archivo(self):
        """Debe crear conexión a archivo de base de datos."""
        from src.conexion_db import ConexionSQLite

        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            ruta_temp = tmp.name

        try:
            conn = ConexionSQLite(ruta_temp)
            assert conn.conexion is not None
            conn.cerrar()
        finally:
            if os.path.exists(ruta_temp):
                os.unlink(ruta_temp)

    def test_con_ruta_invalida_lanza_error(self):
        """Debe lanzar error si la ruta es inválida."""
        from src.conexion_db import ConexionSQLite

        with pytest.raises((sqlite3.Error, ValueError)):
            ConexionSQLite("/ruta/invalida/que/no/existe/base.db")


class TestConexionSQLiteEjecutarQuery:
    """Tests para ejecutar_query."""

    def test_ejecutar_select_simple(self, db_en_memoria):
        """Debe ejecutar SELECT simple y retornar resultados."""
        from src.conexion_db import ConexionSQLite

        # Crear conexión usando la fixture
        conn = ConexionSQLite(":memory:")

        # Crear tabla de prueba
        conn.conexion.execute(
            """
            CREATE TABLE test (id INTEGER, nombre TEXT)
        """
        )
        conn.conexion.execute(
            """
            INSERT INTO test VALUES (1, 'Producto A'), (2, 'Producto B')
        """
        )
        conn.conexion.commit()

        # Ejecutar query
        resultados = conn.ejecutar_query("SELECT * FROM test")

        assert len(resultados) == 2
        assert resultados[0]["id"] == 1
        assert resultados[0]["nombre"] == "Producto A"
        assert resultados[1]["id"] == 2
        assert resultados[1]["nombre"] == "Producto B"

        conn.cerrar()

    def test_ejecutar_query_con_parametros(self):
        """Debe ejecutar query con parámetros de forma segura."""
        from src.conexion_db import ConexionSQLite

        conn = ConexionSQLite(":memory:")

        conn.conexion.execute(
            """
            CREATE TABLE test (id INTEGER, nombre TEXT)
        """
        )
        conn.conexion.execute(
            """
            INSERT INTO test VALUES (1, 'Producto A'), (2, 'Producto B')
        """
        )
        conn.conexion.commit()

        # Query con parámetros
        resultados = conn.ejecutar_query("SELECT * FROM test WHERE id = ?", (1,))

        assert len(resultados) == 1
        assert resultados[0]["id"] == 1

        conn.cerrar()

    def test_ejecutar_query_sin_resultados(self):
        """Debe retornar lista vacía si no hay resultados."""
        from src.conexion_db import ConexionSQLite

        conn = ConexionSQLite(":memory:")

        conn.conexion.execute(
            """
            CREATE TABLE test (id INTEGER, nombre TEXT)
        """
        )
        conn.conexion.commit()

        resultados = conn.ejecutar_query("SELECT * FROM test")

        assert resultados == []

        conn.cerrar()

    def test_ejecutar_query_invalida_lanza_error(self):
        """Debe lanzar error si la query es inválida."""
        from src.conexion_db import ConexionSQLite

        conn = ConexionSQLite(":memory:")

        with pytest.raises(sqlite3.Error):
            conn.ejecutar_query("SELECT * FROM tabla_inexistente")

        conn.cerrar()

    def test_resultados_son_diccionarios(self):
        """Los resultados deben ser diccionarios, no tuplas."""
        from src.conexion_db import ConexionSQLite

        conn = ConexionSQLite(":memory:")

        conn.conexion.execute(
            """
            CREATE TABLE test (id INTEGER, nombre TEXT)
        """
        )
        conn.conexion.execute(
            """
            INSERT INTO test VALUES (1, 'Producto A')
        """
        )
        conn.conexion.commit()

        resultados = conn.ejecutar_query("SELECT * FROM test")

        assert isinstance(resultados[0], dict)
        assert "id" in resultados[0]
        assert "nombre" in resultados[0]

        conn.cerrar()


class TestConexionSQLiteCerrar:
    """Tests para cerrar conexión."""

    def test_cerrar_conexion(self):
        """Debe cerrar la conexión correctamente."""
        from src.conexion_db import ConexionSQLite

        conn = ConexionSQLite(":memory:")
        conn.cerrar()

        # Intentar ejecutar query después de cerrar debe fallar
        with pytest.raises(sqlite3.ProgrammingError):
            conn.conexion.execute("SELECT 1")

    def test_cerrar_conexion_ya_cerrada_no_lanza_error(self):
        """Cerrar una conexión ya cerrada no debe lanzar error."""
        from src.conexion_db import ConexionSQLite

        conn = ConexionSQLite(":memory:")
        conn.cerrar()

        # No debe lanzar error
        conn.cerrar()


class TestConexionSQLiteContextManager:
    """Tests para uso como context manager (with)."""

    def test_usar_con_with_statement(self):
        """Debe funcionar como context manager."""
        from src.conexion_db import ConexionSQLite

        with ConexionSQLite(":memory:") as conn:
            conn.conexion.execute(
                """
                CREATE TABLE test (id INTEGER)
            """
            )
            conn.conexion.execute("INSERT INTO test VALUES (1)")
            conn.conexion.commit()

            resultados = conn.ejecutar_query("SELECT * FROM test")
            assert len(resultados) == 1

        # La conexión debe estar cerrada después del with
        with pytest.raises(sqlite3.ProgrammingError):
            conn.conexion.execute("SELECT 1")

    def test_context_manager_cierra_en_excepcion(self):
        """Debe cerrar conexión incluso si hay excepción."""
        from src.conexion_db import ConexionSQLite

        try:
            with ConexionSQLite(":memory:") as conn:
                conn.conexion.execute(
                    """
                    CREATE TABLE test (id INTEGER)
                """
                )
                raise ValueError("Error de prueba")
        except ValueError:
            pass

        # La conexión debe estar cerrada
        with pytest.raises(sqlite3.ProgrammingError):
            conn.conexion.execute("SELECT 1")
