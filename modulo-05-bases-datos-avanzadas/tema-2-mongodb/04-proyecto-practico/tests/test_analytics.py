"""
Tests para el módulo analytics.

Proyecto: Sistema de Análisis de Logs con MongoDB
"""

import pytest

from src.analytics import (
    calcular_tasa_error,
    detectar_anomalias,
    generar_reporte_resumen,
    identificar_servicios_criticos,
)


class TestCalcularTasaError:
    """Tests para calcular_tasa_error."""

    def test_tasa_error_con_errores(self):
        """Debe calcular correctamente la tasa de error."""
        logs = [
            {"nivel": "ERROR"},
            {"nivel": "ERROR"},
            {"nivel": "INFO"},
            {"nivel": "WARNING"},
            {"nivel": "INFO"},
        ]

        tasa = calcular_tasa_error(logs)

        assert tasa == 40.0  # 2 errores de 5 logs = 40%

    def test_tasa_error_sin_errores(self):
        """Debe retornar 0 si no hay errores."""
        logs = [
            {"nivel": "INFO"},
            {"nivel": "WARNING"},
            {"nivel": "INFO"},
        ]

        tasa = calcular_tasa_error(logs)

        assert tasa == 0.0

    def test_tasa_error_todos_errores(self):
        """Debe retornar 100 si todos son errores."""
        logs = [
            {"nivel": "ERROR"},
            {"nivel": "ERROR"},
            {"nivel": "ERROR"},
        ]

        tasa = calcular_tasa_error(logs)

        assert tasa == 100.0

    def test_tasa_error_lista_vacia(self):
        """Debe lanzar ValueError si la lista está vacía."""
        with pytest.raises(ValueError, match="Lista de logs no puede estar vacía"):
            calcular_tasa_error([])

    def test_tasa_error_precision_dos_decimales(self):
        """Debe retornar con 2 decimales de precisión."""
        logs = [
            {"nivel": "ERROR"},
            {"nivel": "INFO"},
            {"nivel": "INFO"},
        ]

        tasa = calcular_tasa_error(logs)

        assert round(tasa, 2) == 33.33


class TestIdentificarServiciosCriticos:
    """Tests para identificar_servicios_criticos."""

    def test_identificar_servicios_criticos_basico(self):
        """Debe identificar servicios con alta tasa de error."""
        logs = [
            {"servicio": "UserService", "nivel": "ERROR"},
            {"servicio": "UserService", "nivel": "ERROR"},
            {"servicio": "UserService", "nivel": "INFO"},
            {"servicio": "PaymentService", "nivel": "ERROR"},
            {"servicio": "PaymentService", "nivel": "INFO"},
            {"servicio": "AuthService", "nivel": "INFO"},
            {"servicio": "AuthService", "nivel": "INFO"},
        ]

        criticos = identificar_servicios_criticos(logs, umbral_error=50.0)

        assert len(criticos) >= 1
        assert any(s["servicio"] == "UserService" for s in criticos)

    def test_identificar_servicios_criticos_con_umbral(self):
        """Debe respetar el umbral de error especificado."""
        logs = [
            {"servicio": "Service1", "nivel": "ERROR"},
            {"servicio": "Service1", "nivel": "INFO"},
            {"servicio": "Service2", "nivel": "INFO"},
            {"servicio": "Service2", "nivel": "INFO"},
        ]

        criticos = identificar_servicios_criticos(logs, umbral_error=40.0)

        # Service1 tiene 50% error, debería estar
        assert any(s["servicio"] == "Service1" for s in criticos)
        # Service2 tiene 0% error, no debería estar
        assert not any(s["servicio"] == "Service2" for s in criticos)

    def test_identificar_servicios_criticos_lista_vacia(self):
        """Debe lanzar ValueError si lista está vacía."""
        with pytest.raises(ValueError, match="Lista de logs no puede estar vacía"):
            identificar_servicios_criticos([])

    def test_identificar_servicios_criticos_incluye_metricas(self):
        """Debe incluir métricas del servicio."""
        logs = [
            {"servicio": "TestService", "nivel": "ERROR"},
            {"servicio": "TestService", "nivel": "ERROR"},
            {"servicio": "TestService", "nivel": "INFO"},
        ]

        criticos = identificar_servicios_criticos(logs, umbral_error=50.0)

        servicio = criticos[0]
        assert "servicio" in servicio
        assert "total_logs" in servicio or "tasa_error" in servicio


class TestGenerarReporteResumen:
    """Tests para generar_reporte_resumen."""

    def test_generar_reporte_basico(self):
        """Debe generar reporte con métricas básicas."""
        logs = [
            {"nivel": "ERROR", "servicio": "Service1"},
            {"nivel": "INFO", "servicio": "Service1"},
            {"nivel": "WARNING", "servicio": "Service2"},
            {"nivel": "INFO", "servicio": "Service2"},
        ]

        reporte = generar_reporte_resumen(logs)

        assert isinstance(reporte, dict)
        assert "total_logs" in reporte
        assert reporte["total_logs"] == 4

    def test_generar_reporte_con_conteos_por_nivel(self):
        """Debe incluir conteos por nivel de severidad."""
        logs = [
            {"nivel": "ERROR", "servicio": "Service1"},
            {"nivel": "ERROR", "servicio": "Service1"},
            {"nivel": "INFO", "servicio": "Service2"},
            {"nivel": "WARNING", "servicio": "Service2"},
        ]

        reporte = generar_reporte_resumen(logs)

        assert "errores" in reporte or "total_errores" in reporte
        assert "warnings" in reporte or "total_warnings" in reporte

    def test_generar_reporte_con_servicios(self):
        """Debe incluir información de servicios."""
        logs = [
            {"nivel": "ERROR", "servicio": "Service1"},
            {"nivel": "INFO", "servicio": "Service2"},
            {"nivel": "INFO", "servicio": "Service3"},
        ]

        reporte = generar_reporte_resumen(logs)

        assert "total_servicios" in reporte or "servicios_unicos" in reporte

    def test_generar_reporte_lista_vacia(self):
        """Debe lanzar ValueError si lista está vacía."""
        with pytest.raises(ValueError, match="Lista de logs no puede estar vacía"):
            generar_reporte_resumen([])

    def test_generar_reporte_incluye_tasa_error(self):
        """Debe incluir tasa de error en el reporte."""
        logs = [
            {"nivel": "ERROR", "servicio": "Service1"},
            {"nivel": "INFO", "servicio": "Service1"},
        ]

        reporte = generar_reporte_resumen(logs)

        assert "tasa_error" in reporte


class TestDetectarAnomalias:
    """Tests para detectar_anomalias."""

    def test_detectar_anomalias_basico(self):
        """Debe detectar anomalías en logs."""
        logs = [
            {"servicio": "Service1", "nivel": "ERROR", "tiempo_respuesta": 5000},
            {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 100},
            {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 120},
            {"servicio": "Service2", "nivel": "ERROR", "tiempo_respuesta": 50},
        ]

        anomalias = detectar_anomalias(logs)

        assert isinstance(anomalias, list)

    def test_detectar_anomalias_por_tiempo_respuesta(self):
        """Debe detectar anomalías de tiempo de respuesta alto."""
        logs = [
            {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 100},
            {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 120},
            {"servicio": "Service1", "nivel": "WARNING", "tiempo_respuesta": 5000},
        ]

        anomalias = detectar_anomalias(logs, umbral_tiempo=1000)

        assert len(anomalias) >= 1
        # Debe incluir el log con tiempo 5000
        assert any(a.get("tiempo_respuesta") == 5000 for a in anomalias)

    def test_detectar_anomalias_servicios_con_muchos_errores(self):
        """Debe detectar servicios con cantidad anormal de errores."""
        logs = []
        # Service1 con muchos errores
        for _ in range(50):
            logs.append({"servicio": "Service1", "nivel": "ERROR"})
        # Service2 con pocos errores
        for _ in range(5):
            logs.append({"servicio": "Service2", "nivel": "INFO"})

        anomalias = detectar_anomalias(logs)

        # Debería detectar Service1 como anómalo
        assert len(anomalias) >= 1

    def test_detectar_anomalias_lista_vacia(self):
        """Debe retornar lista vacía si no hay logs."""
        anomalias = detectar_anomalias([])

        assert anomalias == []

    def test_detectar_anomalias_sin_anomalias(self):
        """Debe retornar lista vacía si no hay anomalías."""
        logs = [
            {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 100},
            {"servicio": "Service1", "nivel": "INFO", "tiempo_respuesta": 110},
            {"servicio": "Service2", "nivel": "INFO", "tiempo_respuesta": 95},
        ]

        anomalias = detectar_anomalias(logs, umbral_tiempo=5000)

        assert len(anomalias) == 0
