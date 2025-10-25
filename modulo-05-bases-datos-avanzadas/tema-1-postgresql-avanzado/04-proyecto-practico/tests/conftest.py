"""
Configuración de pytest para tests de PostgreSQL.

Proporciona fixtures reutilizables para tests.
"""

import os

import pytest


@pytest.fixture(scope="session")
def test_db_config():
    """
    Configuración de base de datos para tests.

    Returns:
        dict: Configuración de conexión
    """
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "user": os.getenv("POSTGRES_USER", "dataeng_user"),
        "password": os.getenv("POSTGRES_PASSWORD", "DataEng2025!SecurePass"),
        "database": os.getenv("POSTGRES_DB", "dataeng_db"),
    }


@pytest.fixture
def conn_mock():  # noqa: C901
    """
    Mock de conexión para tests que no requieren BD real.

    Returns:
        Mock de conexión
    """

    class MockConnection:
        def __init__(self):
            self.closed = 0

        def close(self):
            self.closed = 1

        def cursor(self):
            return MockCursor()

        def commit(self):
            pass

        def rollback(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    class MockCursor:
        def __init__(self):
            self.rowcount = 1

        def execute(self, query, params=None):
            pass

        def fetchall(self):
            return []

        def fetchone(self):
            return (1,)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    return MockConnection()
