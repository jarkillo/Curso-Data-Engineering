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

    def test_configura_logger_con_archivo(self, tmp_path):
        """Should configure logger with file handler."""
        from src.utilidades import configurar_logging

        log_file = tmp_path / "test.log"
        logger = configurar_logging(nivel="INFO", archivo=str(log_file))

        # Debe tener 2 handlers: consola y archivo
        assert len(logger.handlers) == 2

        # Escribir un mensaje
        logger.info("Mensaje de prueba")

        # Verificar que el archivo existe y tiene contenido
        assert log_file.exists()
        contenido = log_file.read_text(encoding="utf-8")
        assert "Mensaje de prueba" in contenido

    def test_configura_logger_crea_directorio_para_archivo(self, tmp_path):
        """Should create directory for log file if it doesn't exist."""
        from src.utilidades import configurar_logging

        log_file = tmp_path / "subdir" / "test.log"
        logger = configurar_logging(nivel="INFO", archivo=str(log_file))

        logger.info("Test")

        assert log_file.parent.exists()
        assert log_file.exists()


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

    def test_mide_tiempo_rapido_muestra_milisegundos(self, capsys):
        """Should show milliseconds for fast operations."""
        from src.utilidades import medir_tiempo

        with medir_tiempo("Operación rápida"):
            pass  # Operación instantánea

        captured = capsys.readouterr()
        assert "ms" in captured.out


class TestGenerarReporteResumen:
    """Tests para generar_reporte_resumen()."""

    def test_genera_reporte_basico(self):
        """Should generate basic report with dimensions and facts."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "dimensiones": {"DimFecha": 365, "DimProducto": 100},
            "fact_tables": {"FactVentas": 10000},
            "tiempo_total": 5.23,
            "errores": [],
        }

        reporte = generar_reporte_resumen(estadisticas)

        assert "DimFecha" in reporte
        assert "DimProducto" in reporte
        assert "FactVentas" in reporte
        assert "COMPLETADO EXITOSAMENTE" in reporte

    def test_genera_reporte_con_errores(self):
        """Should show errors in report."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "dimensiones": {"DimFecha": 365},
            "fact_tables": {"FactVentas": 0},
            "tiempo_total": 1.5,
            "errores": ["Error de validación", "Conexión fallida"],
        }

        reporte = generar_reporte_resumen(estadisticas)

        assert "Error de validación" in reporte
        assert "Conexión fallida" in reporte
        assert "CON ERRORES" in reporte

    def test_falla_con_estadisticas_vacias(self):
        """Should raise ValueError if estadisticas is empty."""
        from src.utilidades import generar_reporte_resumen

        with pytest.raises(ValueError, match="no puede estar vacío"):
            generar_reporte_resumen({})

    def test_falla_sin_dimensiones(self):
        """Should raise ValueError if dimensiones key is missing."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "fact_tables": {"FactVentas": 100},
            "tiempo_total": 1.0,
        }

        with pytest.raises(ValueError, match="Falta clave requerida"):
            generar_reporte_resumen(estadisticas)

    def test_falla_sin_fact_tables(self):
        """Should raise ValueError if fact_tables key is missing."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "dimensiones": {"DimFecha": 365},
            "tiempo_total": 1.0,
        }

        with pytest.raises(ValueError, match="Falta clave requerida"):
            generar_reporte_resumen(estadisticas)

    def test_falla_sin_tiempo_total(self):
        """Should raise ValueError if tiempo_total key is missing."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "dimensiones": {"DimFecha": 365},
            "fact_tables": {"FactVentas": 100},
        }

        with pytest.raises(ValueError, match="Falta clave requerida"):
            generar_reporte_resumen(estadisticas)

    def test_tiempo_en_milisegundos(self):
        """Should show time in milliseconds if less than 1 second."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "dimensiones": {"DimFecha": 10},
            "fact_tables": {"FactVentas": 50},
            "tiempo_total": 0.5,
            "errores": [],
        }

        reporte = generar_reporte_resumen(estadisticas)

        assert "ms" in reporte

    def test_tiempo_en_segundos(self):
        """Should show time in seconds if >= 1 second."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "dimensiones": {"DimFecha": 10},
            "fact_tables": {"FactVentas": 50},
            "tiempo_total": 2.5,
            "errores": [],
        }

        reporte = generar_reporte_resumen(estadisticas)

        assert "segundos" in reporte

    def test_calcula_totales_correctamente(self):
        """Should calculate totals correctly."""
        from src.utilidades import generar_reporte_resumen

        estadisticas = {
            "dimensiones": {"DimFecha": 100, "DimProducto": 50},
            "fact_tables": {"FactVentas": 1000},
            "tiempo_total": 1.0,
        }

        reporte = generar_reporte_resumen(estadisticas)

        # Total dimensiones = 100 + 50 = 150
        assert "150" in reporte
        # Total fact tables = 1000
        assert "1,000" in reporte


class TestValidarArchivoEdgeCases:
    """Tests adicionales para validar_archivo_existe."""

    def test_falla_si_ruta_es_directorio(self, tmp_path):
        """Should raise ValueError if path is a directory."""
        from src.utilidades import validar_archivo_existe

        with pytest.raises(ValueError, match="no es un archivo"):
            validar_archivo_existe(str(tmp_path))


class TestImprimirTablaEdgeCases:
    """Tests adicionales para imprimir_tabla."""

    def test_imprime_mensaje_si_datos_vacios(self, capsys):
        """Should print message if data is empty."""
        from src.utilidades import imprimir_tabla

        imprimir_tabla([], headers=["col1", "col2"])

        captured = capsys.readouterr()
        assert "No hay datos" in captured.out
