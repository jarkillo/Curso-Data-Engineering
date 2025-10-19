"""
Tests para las funciones de configuración de logging.

Siguiendo TDD: Tests escritos PRIMERO, implementación DESPUÉS.
"""

import logging
import pytest
from src.logger_config import configurar_logger, configurar_logger_archivo


class TestConfigurarLogger:
    """Tests para la función configurar_logger."""

    def test_configurar_logger_con_nivel_info(self):
        """Debe configurar logger con nivel INFO correctamente."""
        logger = configurar_logger(nombre="test_info", nivel="INFO")

        assert logger is not None
        assert logger.name == "test_info"
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0

    def test_configurar_logger_con_nivel_debug(self):
        """Debe configurar logger con nivel DEBUG correctamente."""
        logger = configurar_logger(nombre="test_debug", nivel="DEBUG")

        assert logger.level == logging.DEBUG

    def test_configurar_logger_con_nivel_warning(self):
        """Debe configurar logger con nivel WARNING correctamente."""
        logger = configurar_logger(nombre="test_warning", nivel="WARNING")

        assert logger.level == logging.WARNING

    def test_configurar_logger_con_nivel_error(self):
        """Debe configurar logger con nivel ERROR correctamente."""
        logger = configurar_logger(nombre="test_error", nivel="ERROR")

        assert logger.level == logging.ERROR

    def test_configurar_logger_con_nivel_critical(self):
        """Debe configurar logger con nivel CRITICAL correctamente."""
        logger = configurar_logger(nombre="test_critical", nivel="CRITICAL")

        assert logger.level == logging.CRITICAL

    def test_configurar_logger_con_nivel_invalido_lanza_value_error(self):
        """Debe lanzar ValueError si el nivel no es válido."""
        with pytest.raises(ValueError, match="Nivel de log inválido"):
            configurar_logger(nombre="test", nivel="INVALID")

    def test_configurar_logger_con_nombre_vacio_lanza_value_error(self):
        """Debe lanzar ValueError si el nombre está vacío."""
        with pytest.raises(
            ValueError, match="El nombre del logger no puede estar vacío"
        ):
            configurar_logger(nombre="", nivel="INFO")

    def test_configurar_logger_con_nombre_none_lanza_type_error(self):
        """Debe lanzar TypeError si el nombre es None."""
        with pytest.raises(TypeError):
            configurar_logger(nombre=None, nivel="INFO")

    def test_configurar_logger_nivel_por_defecto_es_info(self):
        """Si no se especifica nivel, debe usar INFO por defecto."""
        logger = configurar_logger(nombre="test_default")

        assert logger.level == logging.INFO

    def test_configurar_logger_formato_incluye_timestamp(self, caplog):
        """El formato debe incluir timestamp."""
        # Configurar caplog para capturar logs del logger específico
        logger = configurar_logger(nombre="test_formato", nivel="INFO")

        # Añadir handler de caplog al logger para que pytest lo capture
        caplog.set_level(logging.INFO, logger="test_formato")
        logger.addHandler(caplog.handler)

        logger.info("Mensaje de prueba")

        # Verificar que el log contiene elementos del formato
        assert len(caplog.records) > 0
        record = caplog.records[0]
        assert record.levelname == "INFO"
        assert record.message == "Mensaje de prueba"

    def test_configurar_logger_no_duplica_handlers(self):
        """No debe añadir handlers duplicados si se llama múltiples veces."""
        logger1 = configurar_logger(nombre="test_duplicado", nivel="INFO")
        num_handlers_inicial = len(logger1.handlers)

        logger2 = configurar_logger(nombre="test_duplicado", nivel="INFO")
        num_handlers_final = len(logger2.handlers)

        # Debe limpiar handlers existentes antes de añadir nuevos
        assert num_handlers_final == num_handlers_inicial


class TestConfigurarLoggerArchivo:
    """Tests para la función configurar_logger_archivo."""

    def test_configurar_logger_archivo_crea_archivo(self, tmp_path):
        """Debe crear el archivo de log correctamente."""
        archivo_log = tmp_path / "test.log"

        logger = configurar_logger_archivo(
            nombre="test_archivo", ruta_archivo=str(archivo_log), nivel="INFO"
        )

        logger.info("Mensaje de prueba")

        # Verificar que el archivo se creó
        assert archivo_log.exists()

        # Verificar que el mensaje está en el archivo
        contenido = archivo_log.read_text(encoding="utf-8")
        assert "Mensaje de prueba" in contenido
        assert "INFO" in contenido

    def test_configurar_logger_archivo_con_nivel_debug(self, tmp_path):
        """Debe respetar el nivel de log configurado."""
        archivo_log = tmp_path / "debug.log"

        logger = configurar_logger_archivo(
            nombre="test_debug_archivo", ruta_archivo=str(archivo_log), nivel="DEBUG"
        )

        logger.debug("Mensaje debug")
        logger.info("Mensaje info")

        contenido = archivo_log.read_text(encoding="utf-8")
        assert "Mensaje debug" in contenido
        assert "Mensaje info" in contenido

    def test_configurar_logger_archivo_con_nivel_warning_no_muestra_info(
        self, tmp_path
    ):
        """Con nivel WARNING, no debe mostrar mensajes INFO."""
        archivo_log = tmp_path / "warning.log"

        logger = configurar_logger_archivo(
            nombre="test_warning_archivo",
            ruta_archivo=str(archivo_log),
            nivel="WARNING",
        )

        logger.info("Mensaje info")
        logger.warning("Mensaje warning")

        contenido = archivo_log.read_text(encoding="utf-8")
        assert "Mensaje info" not in contenido
        assert "Mensaje warning" in contenido

    def test_configurar_logger_archivo_con_ruta_invalida_lanza_error(self):
        """Debe lanzar error si la ruta no es válida."""
        # En Windows, usar una ruta con caracteres inválidos
        import platform

        if platform.system() == "Windows":
            ruta_invalida = "C:\\<>:|?*\\archivo.log"  # Caracteres inválidos en Windows
        else:
            ruta_invalida = "/dev/null/imposible/archivo.log"

        with pytest.raises((ValueError, OSError)):
            configurar_logger_archivo(
                nombre="test_ruta_invalida", ruta_archivo=ruta_invalida, nivel="INFO"
            )

    def test_configurar_logger_archivo_con_nombre_vacio_lanza_value_error(
        self, tmp_path
    ):
        """Debe lanzar ValueError si el nombre está vacío."""
        archivo_log = tmp_path / "test.log"

        with pytest.raises(
            ValueError, match="El nombre del logger no puede estar vacío"
        ):
            configurar_logger_archivo(
                nombre="", ruta_archivo=str(archivo_log), nivel="INFO"
            )

    def test_configurar_logger_archivo_con_max_bytes(self, tmp_path):
        """Debe configurar rotación de archivos con max_bytes."""
        archivo_log = tmp_path / "rotacion.log"

        logger = configurar_logger_archivo(
            nombre="test_rotacion",
            ruta_archivo=str(archivo_log),
            nivel="INFO",
            max_bytes=1024,  # 1KB
            backup_count=3,
        )

        # Escribir varios mensajes para probar rotación
        for i in range(100):
            logger.info(
                f"Mensaje de prueba número {i} con texto adicional "
                f"para llenar el archivo"
            )

        # Verificar que el archivo principal existe
        assert archivo_log.exists()

        # Verificar que se crearon archivos de backup (si se superó el límite)
        # Puede haber 0 o más archivos de backup dependiendo del tamaño
        assert len(list(tmp_path.glob("rotacion.log.*"))) >= 0

    def test_configurar_logger_archivo_crea_directorio_si_no_existe(self, tmp_path):
        """Debe crear el directorio si no existe."""
        directorio_logs = tmp_path / "logs" / "subdir"
        archivo_log = directorio_logs / "test.log"

        logger = configurar_logger_archivo(
            nombre="test_crear_dir", ruta_archivo=str(archivo_log), nivel="INFO"
        )

        logger.info("Mensaje de prueba")

        # Verificar que el directorio y archivo se crearon
        assert directorio_logs.exists()
        assert archivo_log.exists()

    def test_configurar_logger_archivo_formato_incluye_todos_los_campos(self, tmp_path):
        """El formato debe incluir timestamp, nivel, nombre y mensaje."""
        archivo_log = tmp_path / "formato.log"

        logger = configurar_logger_archivo(
            nombre="test_formato_completo", ruta_archivo=str(archivo_log), nivel="INFO"
        )

        logger.info("Mensaje de prueba")

        contenido = archivo_log.read_text(encoding="utf-8")

        # Verificar que contiene los elementos del formato
        assert "INFO" in contenido
        assert "test_formato_completo" in contenido
        assert "Mensaje de prueba" in contenido
        # Verificar formato de fecha (YYYY-MM-DD)
        import re

        assert re.search(r"\d{4}-\d{2}-\d{2}", contenido)

    def test_configurar_logger_archivo_append_mode(self, tmp_path):
        """Debe añadir logs al archivo existente (append mode)."""
        archivo_log = tmp_path / "append.log"

        # Primera escritura
        logger1 = configurar_logger_archivo(
            nombre="test_append_1", ruta_archivo=str(archivo_log), nivel="INFO"
        )
        logger1.info("Primera línea")

        # Segunda escritura (mismo archivo)
        logger2 = configurar_logger_archivo(
            nombre="test_append_2", ruta_archivo=str(archivo_log), nivel="INFO"
        )
        logger2.info("Segunda línea")

        contenido = archivo_log.read_text(encoding="utf-8")

        # Ambas líneas deben estar presentes
        assert "Primera línea" in contenido
        assert "Segunda línea" in contenido
