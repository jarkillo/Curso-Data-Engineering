"""Tests placeholder - Master en Ingeniería de Datos.

Este archivo es un placeholder para que pytest pueda ejecutarse.
Los tests reales se añadirán en cada módulo correspondiente.
"""


def test_placeholder() -> None:
    """Test placeholder para que pytest no falle."""
    assert True, "Test placeholder debe pasar siempre"


def test_python_version() -> None:
    """Verificar que estamos usando Python 3.13+."""
    import sys

    assert sys.version_info >= (3, 13), "Debe usar Python 3.13 o superior"
