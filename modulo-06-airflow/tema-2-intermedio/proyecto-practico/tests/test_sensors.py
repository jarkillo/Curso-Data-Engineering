"""
Tests para el módulo de sensors.

Siguiendo metodología TDD - Red, Green, Refactor
"""

import os
import tempfile
from pathlib import Path


def test_verificar_archivo_existe_cuando_archivo_presente():
    """Test: verificar_archivo_existe retorna True si el archivo existe"""
    from src.sensors import verificar_archivo_existe

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        ruta_tmp = tmp.name
        tmp.write(b"contenido de prueba")

    try:
        resultado = verificar_archivo_existe(ruta_tmp)
        assert resultado is True
    finally:
        os.unlink(ruta_tmp)


def test_verificar_archivo_existe_cuando_archivo_ausente():
    """Test: verificar_archivo_existe retorna False si el archivo no existe"""
    from src.sensors import verificar_archivo_existe

    ruta_inexistente = "/ruta/que/no/existe/archivo.csv"
    resultado = verificar_archivo_existe(ruta_inexistente)
    assert resultado is False


def test_verificar_archivo_existe_con_path_object():
    """Test: verificar_archivo_existe funciona con objetos Path"""
    from src.sensors import verificar_archivo_existe

    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        ruta_tmp = Path(tmp.name)
        tmp.write(b"contenido de prueba")

    try:
        resultado = verificar_archivo_existe(str(ruta_tmp))
        assert resultado is True
    finally:
        os.unlink(ruta_tmp)
