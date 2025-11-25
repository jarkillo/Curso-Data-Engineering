"""
Tests para el módulo log_processor.

Proyecto: Sistema de Análisis de Logs con MongoDB
"""

from datetime import datetime

import pytest

from src.log_processor import (
    extraer_nivel_severidad,
    normalizar_timestamp,
    parsear_log_entry,
    validar_log_entry,
)


class TestParsearLogEntry:
    """Tests para parsear_log_entry."""

    def test_parsear_log_valido(self):
        """Debe parsear correctamente un log válido."""
        log_string = (
            "2024-11-12 14:30:45 | ERROR | UserService | Database connection failed"
        )

        resultado = parsear_log_entry(log_string)

        assert resultado["timestamp"] == "2024-11-12 14:30:45"
        assert resultado["nivel"] == "ERROR"
        assert resultado["servicio"] == "UserService"
        assert resultado["mensaje"] == "Database connection failed"

    def test_parsear_log_con_info(self):
        """Debe parsear log con nivel INFO."""
        log_string = (
            "2024-11-12 10:15:30 | INFO | AuthService | User logged in successfully"
        )

        resultado = parsear_log_entry(log_string)

        assert resultado["nivel"] == "INFO"
        assert resultado["servicio"] == "AuthService"

    def test_parsear_log_vacio_lanza_error(self):
        """Debe lanzar ValueError si el log está vacío."""
        with pytest.raises(ValueError, match="Log string no puede estar vacío"):
            parsear_log_entry("")

    def test_parsear_log_formato_invalido(self):
        """Debe lanzar ValueError si el formato es inválido."""
        log_invalido = "log sin formato correcto"

        with pytest.raises(ValueError, match="Formato de log inválido"):
            parsear_log_entry(log_invalido)

    def test_parsear_log_con_warning(self):
        """Debe parsear log con nivel WARNING."""
        log_string = "2024-11-12 16:45:00 | WARNING | PaymentService | High response time detected"

        resultado = parsear_log_entry(log_string)

        assert resultado["nivel"] == "WARNING"
        assert resultado["mensaje"] == "High response time detected"


class TestValidarLogEntry:
    """Tests para validar_log_entry."""

    def test_validar_log_completo(self):
        """Debe validar correctamente un log con todos los campos."""
        log_entry = {
            "timestamp": "2024-11-12 14:30:45",
            "nivel": "ERROR",
            "servicio": "UserService",
            "mensaje": "Database connection failed",
        }

        # No debe lanzar error
        validar_log_entry(log_entry)

    def test_validar_log_sin_timestamp(self):
        """Debe lanzar ValueError si falta timestamp."""
        log_entry = {"nivel": "ERROR", "servicio": "UserService", "mensaje": "Test"}

        with pytest.raises(ValueError, match="Campo 'timestamp' es obligatorio"):
            validar_log_entry(log_entry)

    def test_validar_log_sin_nivel(self):
        """Debe lanzar ValueError si falta nivel."""
        log_entry = {
            "timestamp": "2024-11-12 14:30:45",
            "servicio": "UserService",
            "mensaje": "Test",
        }

        with pytest.raises(ValueError, match="Campo 'nivel' es obligatorio"):
            validar_log_entry(log_entry)

    def test_validar_log_sin_servicio(self):
        """Debe lanzar ValueError si falta servicio."""
        log_entry = {
            "timestamp": "2024-11-12 14:30:45",
            "nivel": "ERROR",
            "mensaje": "Test",
        }

        with pytest.raises(ValueError, match="Campo 'servicio' es obligatorio"):
            validar_log_entry(log_entry)

    def test_validar_log_sin_mensaje(self):
        """Debe lanzar ValueError si falta mensaje."""
        log_entry = {
            "timestamp": "2024-11-12 14:30:45",
            "nivel": "ERROR",
            "servicio": "UserService",
        }

        with pytest.raises(ValueError, match="Campo 'mensaje' es obligatorio"):
            validar_log_entry(log_entry)


class TestNormalizarTimestamp:
    """Tests para normalizar_timestamp."""

    def test_normalizar_timestamp_valido(self):
        """Debe convertir timestamp string a datetime."""
        timestamp_str = "2024-11-12 14:30:45"

        resultado = normalizar_timestamp(timestamp_str)

        assert isinstance(resultado, datetime)
        assert resultado.year == 2024
        assert resultado.month == 11
        assert resultado.day == 12
        assert resultado.hour == 14
        assert resultado.minute == 30
        assert resultado.second == 45

    def test_normalizar_timestamp_formato_alternativo(self):
        """Debe manejar formato de timestamp ISO."""
        timestamp_str = "2024-11-12T10:15:30"

        resultado = normalizar_timestamp(timestamp_str)

        assert isinstance(resultado, datetime)
        assert resultado.hour == 10
        assert resultado.minute == 15

    def test_normalizar_timestamp_invalido(self):
        """Debe lanzar ValueError si el formato es inválido."""
        with pytest.raises(ValueError, match="Formato de timestamp inválido"):
            normalizar_timestamp("fecha-invalida")

    def test_normalizar_timestamp_vacio(self):
        """Debe lanzar ValueError si timestamp está vacío."""
        with pytest.raises(ValueError, match="Timestamp no puede estar vacío"):
            normalizar_timestamp("")


class TestExtraerNivelSeveridad:
    """Tests para extraer_nivel_severidad."""

    def test_extraer_nivel_error(self):
        """Debe extraer nivel ERROR correctamente."""
        log_entry = {"nivel": "ERROR"}

        resultado = extraer_nivel_severidad(log_entry)

        assert resultado == "ERROR"

    def test_extraer_nivel_warning(self):
        """Debe extraer nivel WARNING correctamente."""
        log_entry = {"nivel": "WARNING"}

        resultado = extraer_nivel_severidad(log_entry)

        assert resultado == "WARNING"

    def test_extraer_nivel_info(self):
        """Debe extraer nivel INFO correctamente."""
        log_entry = {"nivel": "INFO"}

        resultado = extraer_nivel_severidad(log_entry)

        assert resultado == "INFO"

    def test_extraer_nivel_sin_campo_lanza_error(self):
        """Debe lanzar KeyError si no existe el campo nivel."""
        log_entry = {"mensaje": "test"}

        with pytest.raises(KeyError, match="Campo 'nivel' no encontrado"):
            extraer_nivel_severidad(log_entry)

    def test_extraer_nivel_invalido_lanza_error(self):
        """Debe lanzar ValueError si el nivel no es válido."""
        log_entry = {"nivel": "INVALID"}

        with pytest.raises(ValueError, match="Nivel de severidad inválido"):
            extraer_nivel_severidad(log_entry)
