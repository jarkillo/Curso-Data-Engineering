"""
Fixtures compartidas para tests del proyecto Scraper Masivo Optimizado

Este archivo contiene fixtures de pytest que se utilizan en múltiples
archivos de tests.
"""

import contextlib
import os
import tempfile

import pytest


@pytest.fixture
def directorio_temporal():
    """
    Crea un directorio temporal para tests.
    Se limpia automáticamente después del test.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def archivo_cache_test(tmp_path):
    """
    Crea un archivo de cache temporal para tests.
    """
    archivo = tmp_path / "test_cache.db"
    yield str(archivo)

    # Limpiar archivos generados por shelve
    for ext in ["", ".db", ".dat", ".bak", ".dir"]:
        with contextlib.suppress(FileNotFoundError):
            os.remove(str(archivo) + ext)


@pytest.fixture
def mock_urls():
    """
    Retorna lista de URLs de prueba.
    """
    return [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        "https://jsonplaceholder.typicode.com/posts/4",
        "https://jsonplaceholder.typicode.com/posts/5",
    ]


@pytest.fixture
def mock_headers():
    """
    Retorna headers HTTP de prueba.
    """
    return {"User-Agent": "TestBot/1.0", "Accept": "application/json"}
