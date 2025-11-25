"""
Tests para el módulo validation.py

Tests exhaustivos para funciones de validación de logs de API.
"""

import pytest

from src.validation import (
    validar_endpoint,
    validar_ip_address,
    validar_log_api,
    validar_lote_logs,
    validar_metodo_http,
    validar_response_time,
    validar_status_code,
    validar_timestamp,
)


class TestValidarLogApi:
    """Tests para validar_log_api()"""

    def test_validar_log_completo_y_valido(self):
        """Debe validar correctamente un log completo"""
        log = {
            "timestamp": "2025-01-15T10:30:45Z",
            "endpoint": "/api/users",
            "method": "GET",
            "status_code": 200,
            "response_time_ms": 145,
            "user_id": "user_12345",
            "ip_address": "192.168.1.100",
        }

        valido, error = validar_log_api(log)

        assert valido is True
        assert error == ""

    def test_validar_log_con_campo_faltante(self):
        """Debe detectar campos faltantes"""
        log = {
            "timestamp": "2025-01-15T10:30:45Z",
            "endpoint": "/api/users",
            # Falta 'method'
            "status_code": 200,
        }

        valido, error = validar_log_api(log)

        assert valido is False
        assert "method" in error.lower()

    def test_validar_log_con_timestamp_invalido(self):
        """Debe detectar timestamp inválido"""
        log = {
            "timestamp": "2025-13-45",  # Fecha inválida
            "endpoint": "/api/users",
            "method": "GET",
            "status_code": 200,
            "response_time_ms": 145,
            "user_id": "user_1",
            "ip_address": "192.168.1.1",
        }

        valido, error = validar_log_api(log)

        assert valido is False
        assert "timestamp" in error.lower()

    def test_validar_log_con_status_code_invalido(self):
        """Debe detectar status code inválido"""
        log = {
            "timestamp": "2025-01-15T10:30:45Z",
            "endpoint": "/api/users",
            "method": "GET",
            "status_code": 999,  # Status code inválido
            "response_time_ms": 145,
            "user_id": "user_1",
            "ip_address": "192.168.1.1",
        }

        valido, error = validar_log_api(log)

        assert valido is False
        assert "status" in error.lower()


class TestValidarTimestamp:
    """Tests para validar_timestamp()"""

    @pytest.mark.parametrize(
        "timestamp",
        [
            "2025-01-15T10:30:45Z",
            "2025-01-15T10:30:45.123Z",
            "2025-12-31T23:59:59Z",
        ],
    )
    def test_timestamps_validos(self, timestamp):
        """Debe aceptar timestamps ISO 8601 válidos"""
        valido, error = validar_timestamp(timestamp)

        assert valido is True
        assert error == ""

    @pytest.mark.parametrize(
        "timestamp",
        [
            "2025-13-45",  # Mes inválido
            "15/01/2025",  # Formato incorrecto
            "invalid",
            "",
            "2025-01-32T10:30:45Z",  # Día inválido
        ],
    )
    def test_timestamps_invalidos(self, timestamp):
        """Debe rechazar timestamps inválidos"""
        valido, error = validar_timestamp(timestamp)

        assert valido is False
        assert error != ""


class TestValidarEndpoint:
    """Tests para validar_endpoint()"""

    @pytest.mark.parametrize(
        "endpoint",
        [
            "/api/users",
            "/api/v1/posts",
            "/health_check",
            "/api/users/12345",
        ],
    )
    def test_endpoints_validos(self, endpoint):
        """Debe aceptar endpoints válidos"""
        valido, error = validar_endpoint(endpoint)

        assert valido is True
        assert error == ""

    @pytest.mark.parametrize(
        "endpoint",
        [
            "api/users",  # Sin barra inicial
            "",
            "/api/<script>alert()</script>",  # Caracteres no permitidos
            "a" * 201,  # Muy largo
        ],
    )
    def test_endpoints_invalidos(self, endpoint):
        """Debe rechazar endpoints inválidos"""
        valido, error = validar_endpoint(endpoint)

        assert valido is False
        assert error != ""


class TestValidarMetodoHttp:
    """Tests para validar_metodo_http()"""

    @pytest.mark.parametrize(
        "metodo", ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
    )
    def test_metodos_validos(self, metodo):
        """Debe aceptar métodos HTTP estándar"""
        valido, error = validar_metodo_http(metodo)

        assert valido is True
        assert error == ""

    @pytest.mark.parametrize("metodo", ["INVALID", "get", "", "G E T"])
    def test_metodos_invalidos(self, metodo):
        """Debe rechazar métodos HTTP inválidos"""
        valido, error = validar_metodo_http(metodo)

        assert valido is False
        assert error != ""


class TestValidarStatusCode:
    """Tests para validar_status_code()"""

    @pytest.mark.parametrize("status", [100, 200, 201, 301, 404, 500, 503])
    def test_status_codes_validos(self, status):
        """Debe aceptar status codes válidos"""
        valido, error = validar_status_code(status)

        assert valido is True
        assert error == ""

    @pytest.mark.parametrize("status", [99, 600, 0, -1, 1000])
    def test_status_codes_invalidos(self, status):
        """Debe rechazar status codes fuera de rango"""
        valido, error = validar_status_code(status)

        assert valido is False
        assert error != ""


class TestValidarResponseTime:
    """Tests para validar_response_time()"""

    @pytest.mark.parametrize("tiempo", [0, 1, 100, 1000, 5000, 0.5, 123.45])
    def test_response_times_validos(self, tiempo):
        """Debe aceptar tiempos de respuesta válidos"""
        valido, error = validar_response_time(tiempo)

        assert valido is True
        assert error == ""

    @pytest.mark.parametrize("tiempo", [-1, -100, -0.1])
    def test_response_times_negativos(self, tiempo):
        """Debe rechazar tiempos de respuesta negativos"""
        valido, error = validar_response_time(tiempo)

        assert valido is False
        assert "negativo" in error.lower() or "menor" in error.lower()


class TestValidarIpAddress:
    """Tests para validar_ip_address()"""

    @pytest.mark.parametrize(
        "ip",
        [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1",
            "255.255.255.255",
            "0.0.0.0",
        ],
    )
    def test_ips_validas(self, ip):
        """Debe aceptar IPs válidas"""
        valido, error = validar_ip_address(ip)

        assert valido is True
        assert error == ""

    @pytest.mark.parametrize(
        "ip",
        [
            "999.999.999.999",
            "192.168.1",
            "192.168.1.1.1",
            "invalid",
            "",
        ],
    )
    def test_ips_invalidas(self, ip):
        """Debe rechazar IPs inválidas"""
        valido, error = validar_ip_address(ip)

        assert valido is False
        assert error != ""


class TestValidarLoteLogs:
    """Tests para validar_lote_logs()"""

    def test_validar_lote_todos_validos(self):
        """Debe procesar correctamente un lote con todos logs válidos"""
        logs = [
            {
                "timestamp": "2025-01-15T10:30:45Z",
                "endpoint": "/api/users",
                "method": "GET",
                "status_code": 200,
                "response_time_ms": 145,
                "user_id": "user_1",
                "ip_address": "192.168.1.1",
            },
            {
                "timestamp": "2025-01-15T10:30:46Z",
                "endpoint": "/api/posts",
                "method": "POST",
                "status_code": 201,
                "response_time_ms": 234,
                "user_id": "user_2",
                "ip_address": "192.168.1.2",
            },
        ]

        stats = validar_lote_logs(logs)

        assert stats["total"] == 2
        assert stats["validos"] == 2
        assert stats["invalidos"] == 0
        assert stats["tasa_validez"] == 100.0

    def test_validar_lote_con_invalidos(self):
        """Debe detectar y contar logs inválidos"""
        logs = [
            {
                "timestamp": "2025-01-15T10:30:45Z",
                "endpoint": "/api/users",
                "method": "GET",
                "status_code": 200,
                "response_time_ms": 145,
                "user_id": "user_1",
                "ip_address": "192.168.1.1",
            },
            {"timestamp": "invalid", "endpoint": "/api/posts"},  # Inválido
            {
                "timestamp": "2025-01-15T10:30:47Z",
                "endpoint": "api/comments",  # Sin barra inicial
                "method": "GET",
                "status_code": 200,
                "response_time_ms": 89,
                "user_id": "user_3",
                "ip_address": "192.168.1.3",
            },
        ]

        stats = validar_lote_logs(logs)

        assert stats["total"] == 3
        assert stats["validos"] == 1
        assert stats["invalidos"] == 2
        assert abs(stats["tasa_validez"] - 33.33) < 0.1

    def test_validar_lote_vacio(self):
        """Debe manejar correctamente un lote vacío"""
        logs = []

        stats = validar_lote_logs(logs)

        assert stats["total"] == 0
        assert stats["validos"] == 0
        assert stats["invalidos"] == 0
        assert stats["tasa_validez"] == 0.0


# Fixtures
@pytest.fixture
def log_valido():
    """Fixture con un log válido"""
    return {
        "timestamp": "2025-01-15T10:30:45Z",
        "endpoint": "/api/users",
        "method": "GET",
        "status_code": 200,
        "response_time_ms": 145,
        "user_id": "user_12345",
        "ip_address": "192.168.1.100",
    }


@pytest.fixture
def log_invalido():
    """Fixture con un log inválido"""
    return {
        "timestamp": "invalid",
        "endpoint": "api/users",  # Sin barra
        "method": "INVALID",
        "status_code": 999,
        "response_time_ms": -10,
    }
