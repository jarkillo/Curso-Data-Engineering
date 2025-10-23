"""Tests para el módulo de utilidades (logging y métricas)."""

import logging
import time

import pytest
from src.utilidades import (
    calcular_metricas_pipeline,
    configurar_logging,
    formatear_fecha,
)


class TestConfigurarLogging:
    """Tests para la función configurar_logging."""

    def test_configura_logger_con_nivel_info(self):
        """Debe configurar el logger con nivel INFO."""
        configurar_logging("INFO")

        # Verificar que el logger está configurado
        logger = logging.getLogger()
        assert logger.level == logging.INFO

    def test_configura_logger_con_nivel_debug(self):
        """Debe configurar el logger con nivel DEBUG."""
        configurar_logging("DEBUG")

        logger = logging.getLogger()
        assert logger.level == logging.DEBUG

    def test_configura_logger_con_nivel_warning(self):
        """Debe configurar el logger con nivel WARNING."""
        configurar_logging("WARNING")

        logger = logging.getLogger()
        assert logger.level == logging.WARNING


class TestCalcularMetricasPipeline:
    """Tests para la función calcular_metricas_pipeline."""

    def test_calcula_tiempo_transcurrido(self):
        """Debe calcular correctamente el tiempo transcurrido."""
        inicio = time.time()
        time.sleep(0.1)  # Esperar 100ms

        metricas = calcular_metricas_pipeline(inicio, 100)

        assert "tiempo_segundos" in metricas
        assert metricas["tiempo_segundos"] >= 0.1
        assert metricas["tiempo_segundos"] < 1.0  # No debe tardar más de 1s

    def test_calcula_filas_por_segundo(self):
        """Debe calcular filas por segundo correctamente."""
        inicio = time.time()
        time.sleep(0.1)

        metricas = calcular_metricas_pipeline(inicio, 1000)

        assert "filas_por_segundo" in metricas
        assert metricas["filas_por_segundo"] > 0

    def test_con_cero_filas_no_falla(self):
        """No debe fallar si num_filas es 0."""
        inicio = time.time()
        time.sleep(0.1)

        metricas = calcular_metricas_pipeline(inicio, 0)

        assert metricas["filas_por_segundo"] == 0

    def test_redondea_resultados(self):
        """Debe redondear los resultados a 2 decimales."""
        inicio = time.time()
        time.sleep(0.1)

        metricas = calcular_metricas_pipeline(inicio, 1000)

        # Verificar que tienen máximo 2 decimales
        tiempo_str = str(metricas["tiempo_segundos"])
        if "." in tiempo_str:
            decimales = len(tiempo_str.split(".")[1])
            assert decimales <= 2


class TestFormatearFecha:
    """Tests para la función formatear_fecha."""

    def test_con_fecha_valida_retorna_fecha(self):
        """Debe retornar la fecha si el formato es válido."""
        fecha = "2025-10-23"

        resultado = formatear_fecha(fecha)

        assert resultado == "2025-10-23"

    def test_con_formato_invalido_lanza_value_error(self):
        """Debe lanzar ValueError si el formato es inválido."""
        with pytest.raises(ValueError, match="(?i)formato.*inv"):
            formatear_fecha("23/10/2025")

    def test_con_fecha_invalida_lanza_value_error(self):
        """Debe lanzar ValueError si la fecha no existe."""
        with pytest.raises(ValueError, match="(?i)fecha.*inv"):
            formatear_fecha("2025-02-30")  # Febrero no tiene 30 días

    def test_con_string_vacio_lanza_value_error(self):
        """Debe lanzar ValueError si el string está vacío."""
        with pytest.raises(ValueError):
            formatear_fecha("")

    def test_con_none_lanza_type_error(self):
        """Debe lanzar TypeError si se pasa None."""
        with pytest.raises(TypeError):
            formatear_fecha(None)
