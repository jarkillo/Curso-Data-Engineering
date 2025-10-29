"""
Tests para el módulo de notificaciones.

Siguiendo metodología TDD - Red, Green, Refactor
"""

import tempfile
from pathlib import Path


def test_simular_notificacion_gerente(capsys):
    """Test: simular_notificacion_gerente imprime mensaje correcto"""
    from src.notificaciones import simular_notificacion_gerente

    simular_notificacion_gerente(total=6500.0, cliente_top="C001")

    captured = capsys.readouterr()
    assert "[NOTIFICACIÓN]" in captured.out
    assert "6500" in captured.out or "6500.0" in captured.out
    assert "C001" in captured.out


def test_guardar_log_ejecucion():
    """Test: guardar_log_ejecucion crea archivo con mensaje"""
    from src.notificaciones import guardar_log_ejecucion

    with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as tmp:
        ruta_tmp = tmp.name

    try:
        mensaje = "Ejecución completada exitosamente"
        guardar_log_ejecucion(mensaje, ruta_tmp)

        assert Path(ruta_tmp).exists()
        with open(ruta_tmp, "r", encoding="utf-8") as f:
            contenido = f.read()
        assert mensaje in contenido
    finally:
        Path(ruta_tmp).unlink()


def test_guardar_log_ejecucion_crea_directorio_si_no_existe():
    """Test: guardar_log_ejecucion crea el directorio padre si no existe"""
    from src.notificaciones import guardar_log_ejecucion

    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_tmp = Path(tmpdir) / "logs" / "subdir" / "ejecucion.log"

        mensaje = "Test de log"
        guardar_log_ejecucion(mensaje, str(ruta_tmp))

        assert ruta_tmp.exists()
        with open(ruta_tmp, "r", encoding="utf-8") as f:
            contenido = f.read()
        assert mensaje in contenido
