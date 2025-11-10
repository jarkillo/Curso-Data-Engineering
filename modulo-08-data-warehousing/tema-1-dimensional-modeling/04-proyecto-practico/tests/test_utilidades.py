"""
Tests para utilidades.py.

Tests escritos PRIMERO siguiendo TDD para módulo de utilidades y helpers.
Cobertura objetivo: ≥80%.
"""

import logging
import sys
from pathlib import Path

import pytest

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestConfiguracionLogging:
    """Tests para configurar_logging()."""

    def test_configura_logger_con_nivel_info(self):
        """Should configure logger with INFO level."""
        from src.utilidades import configurar_logging

        logger = configurar_logging(nivel="INFO")

        assert isinstance(logger, logging.Logger)
        assert logger.level == logging.INFO

    def test_configura_logger_con_nivel_debug(self):
        """Should configure logger with DEBUG level."""
        from src.utilidades import configurar_logging

        logger = configurar_logging(nivel="DEBUG")

        assert logger.level == logging.DEBUG

    def test_logger_tiene_handlers(self):
        """Should have at least one handler configured."""
        from src.utilidades import configurar_logging

        logger = configurar_logging()

        assert len(logger.handlers) > 0


class TestFormatearNumero:
    """Tests para formatear_numero()."""

    def test_formatea_entero(self):
        """Should format integer with thousand separators."""
        from src.utilidades import formatear_numero

        resultado = formatear_numero(1234567)

        assert resultado == "1,234,567"

    def test_formatea_float_con_decimales(self):
        """Should format float with specified decimal places."""
        from src.utilidades import formatear_numero

        resultado = formatear_numero(1234.5678, decimales=2)

        assert resultado == "1,234.57"

    def test_formatea_float_sin_decimales(self):
        """Should format float without decimals when decimales=0."""
        from src.utilidades import formatear_numero

        resultado = formatear_numero(1234.5678, decimales=0)

        assert resultado == "1,235"


class TestFormatearPorcentaje:
    """Tests para formatear_porcentaje()."""

    def test_formatea_porcentaje_basico(self):
        """Should format percentage from decimal."""
        from src.utilidades import formatear_porcentaje

        resultado = formatear_porcentaje(0.1234, decimales=2)

        assert resultado == "12.34%"

    def test_formatea_porcentaje_sin_decimales(self):
        """Should format percentage without decimals."""
        from src.utilidades import formatear_porcentaje

        resultado = formatear_porcentaje(0.1234, decimales=0)

        assert resultado == "12%"

    def test_formatea_100_porciento(self):
        """Should format 100% correctly."""
        from src.utilidades import formatear_porcentaje

        resultado = formatear_porcentaje(1.0, decimales=1)

        assert resultado == "100.0%"


class TestImprimirTabla:
    """Tests para imprimir_tabla()."""

    def test_imprime_tabla_con_headers(self, capsys):
        """Should print table with headers."""
        from src.utilidades import imprimir_tabla

        datos = [
            {"nombre": "Juan", "edad": 30, "ciudad": "CDMX"},
            {"nombre": "María", "edad": 25, "ciudad": "GDL"},
        ]

        imprimir_tabla(datos, headers=["nombre", "edad", "ciudad"])

        captured = capsys.readouterr()
        assert "Juan" in captured.out
        assert "María" in captured.out
        assert "CDMX" in captured.out

    def test_imprime_tabla_con_titulo(self, capsys):
        """Should print table with title."""
        from src.utilidades import imprimir_tabla

        datos = [{"nombre": "Juan", "edad": 30}]

        imprimir_tabla(datos, headers=["nombre", "edad"], titulo="Usuarios")

        captured = capsys.readouterr()
        assert "Usuarios" in captured.out


class TestValidarArchivo:
    """Tests para validar_archivo_existe()."""

    def test_valida_archivo_existente(self, tmp_path):
        """Should return True if file exists."""
        from src.utilidades import validar_archivo_existe

        # Crear archivo temporal
        archivo = tmp_path / "test.txt"
        archivo.write_text("test")

        resultado = validar_archivo_existe(str(archivo))

        assert resultado is True

    def test_falla_si_archivo_no_existe(self):
        """Should raise FileNotFoundError if file doesn't exist."""
        from src.utilidades import validar_archivo_existe

        with pytest.raises(FileNotFoundError):
            validar_archivo_existe("archivo_inexistente.txt")


class TestCrearDirectorio:
    """Tests para crear_directorio_si_no_existe()."""

    def test_crea_directorio(self, tmp_path):
        """Should create directory if it doesn't exist."""
        from src.utilidades import crear_directorio_si_no_existe

        nuevo_dir = tmp_path / "nuevo_directorio"

        crear_directorio_si_no_existe(str(nuevo_dir))

        assert nuevo_dir.exists()
        assert nuevo_dir.is_dir()

    def test_no_falla_si_directorio_existe(self, tmp_path):
        """Should not fail if directory already exists."""
        from src.utilidades import crear_directorio_si_no_existe

        # No debería lanzar error
        crear_directorio_si_no_existe(str(tmp_path))

        assert tmp_path.exists()


class TestMedirTiempo:
    """Tests para medir_tiempo context manager."""

    def test_mide_tiempo_correctamente(self, capsys):
        """Should measure and print execution time."""
        import time

        from src.utilidades import medir_tiempo

        with medir_tiempo("Operación de prueba"):
            time.sleep(0.1)  # Simular operación

        captured = capsys.readouterr()
        assert "Operación de prueba" in captured.out
        assert "segundos" in captured.out or "ms" in captured.out
