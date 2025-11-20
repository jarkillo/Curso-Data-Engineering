"""Tests para metrics_collector.py - Siguiendo TDD."""

from datetime import datetime

from src.metrics_collector import (
    PipelineMetrics,
    calcular_throughput,
    exportar_metricas_json,
)


class TestPipelineMetrics:
    """Tests para clase PipelineMetrics."""

    def test_inicializacion(self):
        """Debe inicializar correctamente."""
        metricas = PipelineMetrics(start_time=datetime.now())

        assert metricas.rows_extracted == 0
        assert metricas.success is False

    def test_finalizar_calcula_duracion(self):
        """Debe calcular duración al finalizar."""
        metricas = PipelineMetrics(start_time=datetime.now())
        metricas.finalize()

        assert metricas.end_time is not None
        assert metricas.duration_seconds >= 0

    def test_to_dict_incluye_todos_campos(self):
        """Debe convertir a dict con todos los campos."""
        metricas = PipelineMetrics(start_time=datetime.now())
        metricas.rows_extracted = 100
        metricas.finalize()

        dict_metricas = metricas.to_dict()

        assert "start_time" in dict_metricas
        assert "rows_extracted" in dict_metricas
        assert dict_metricas["rows_extracted"] == 100


class TestCalcularThroughput:
    """Tests para calcular_throughput."""

    def test_calculo_correcto(self):
        """Debe calcular throughput correctamente."""
        throughput = calcular_throughput(1000, 10.0)
        assert throughput == 100.0

    def test_duracion_cero_retorna_cero(self):
        """Si duración es 0, debe retornar 0."""
        throughput = calcular_throughput(1000, 0.0)
        assert throughput == 0.0


class TestExportarMetricasJson:
    """Tests para exportar_metricas_json."""

    def test_exporta_archivo(self, directorio_temporal):
        """Debe exportar métricas a JSON."""
        metricas = PipelineMetrics(start_time=datetime.now())
        metricas.rows_extracted = 100
        metricas.finalize()

        archivo_json = directorio_temporal / "metricas.json"
        exportar_metricas_json(metricas, str(archivo_json))

        assert archivo_json.exists()

    def test_archivo_es_json_valido(self, directorio_temporal):
        """El archivo debe ser JSON válido."""
        import json

        metricas = PipelineMetrics(start_time=datetime.now())
        metricas.finalize()

        archivo_json = directorio_temporal / "metricas.json"
        exportar_metricas_json(metricas, str(archivo_json))

        # Leer y parsear
        contenido = json.loads(archivo_json.read_text())
        assert "start_time" in contenido
