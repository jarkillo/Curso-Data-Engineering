"""
Tests para el módulo aggregation_builder.

Proyecto: Sistema de Análisis de Logs con MongoDB
"""

import pytest

from src.aggregation_builder import (
    construir_pipeline_errores,
    construir_pipeline_metricas_tiempo,
    construir_pipeline_por_servicio,
    construir_pipeline_top_usuarios,
)


class TestConstruirPipelineErrores:
    """Tests para construir_pipeline_errores."""

    def test_pipeline_errores_basico(self):
        """Debe construir pipeline para filtrar errores entre fechas."""
        pipeline = construir_pipeline_errores("2024-11-01", "2024-11-30")

        assert isinstance(pipeline, list)
        assert len(pipeline) >= 2  # Al menos $match y $group

        # Verificar que tiene $match
        tiene_match = any(stage.get("$match") for stage in pipeline)
        assert tiene_match, "Pipeline debe contener etapa $match"

        # Verificar que filtra por nivel ERROR
        match_stage = next(stage["$match"] for stage in pipeline if "$match" in stage)
        assert "nivel" in match_stage

    def test_pipeline_errores_con_fechas(self):
        """Debe incluir filtro de fechas en el pipeline."""
        fecha_inicio = "2024-11-01"
        fecha_fin = "2024-11-30"

        pipeline = construir_pipeline_errores(fecha_inicio, fecha_fin)

        match_stage = next(stage["$match"] for stage in pipeline if "$match" in stage)
        assert "timestamp" in match_stage or "$and" in match_stage

    def test_pipeline_errores_invalido_lanza_error(self):
        """Debe lanzar ValueError si las fechas son inválidas."""
        with pytest.raises(ValueError, match="Fecha de inicio inválida"):
            construir_pipeline_errores("fecha-invalida", "2024-11-30")

    def test_pipeline_errores_fecha_inicio_vacia(self):
        """Debe lanzar ValueError si fecha_inicio está vacía."""
        with pytest.raises(ValueError, match="Fecha de inicio no puede estar vacía"):
            construir_pipeline_errores("", "2024-11-30")

    def test_pipeline_errores_tiene_group(self):
        """Debe tener etapa $group para agrupar errores."""
        pipeline = construir_pipeline_errores("2024-11-01", "2024-11-30")

        tiene_group = any(stage.get("$group") for stage in pipeline)
        assert tiene_group, "Pipeline debe contener etapa $group"


class TestConstruirPipelinePorServicio:
    """Tests para construir_pipeline_por_servicio."""

    def test_pipeline_por_servicio_basico(self):
        """Debe construir pipeline para agrupar por servicio."""
        pipeline = construir_pipeline_por_servicio()

        assert isinstance(pipeline, list)
        assert len(pipeline) >= 1

        # Debe tener $group
        tiene_group = any(stage.get("$group") for stage in pipeline)
        assert tiene_group, "Pipeline debe contener $group"

    def test_pipeline_por_servicio_agrupa_por_servicio(self):
        """Debe agrupar por campo servicio."""
        pipeline = construir_pipeline_por_servicio()

        group_stage = next(stage["$group"] for stage in pipeline if "$group" in stage)
        assert group_stage["_id"] == "$servicio"

    def test_pipeline_por_servicio_cuenta_logs(self):
        """Debe contar cantidad de logs por servicio."""
        pipeline = construir_pipeline_por_servicio()

        group_stage = next(stage["$group"] for stage in pipeline if "$group" in stage)
        assert "total_logs" in group_stage or "count" in group_stage

    def test_pipeline_por_servicio_tiene_sort(self):
        """Debe tener etapa $sort para ordenar resultados."""
        pipeline = construir_pipeline_por_servicio()

        tiene_sort = any(stage.get("$sort") for stage in pipeline)
        assert tiene_sort, "Pipeline debe contener $sort"


class TestConstruirPipelineTopUsuarios:
    """Tests para construir_pipeline_top_usuarios."""

    def test_pipeline_top_usuarios_con_limite(self):
        """Debe construir pipeline con límite especificado."""
        limite = 10
        pipeline = construir_pipeline_top_usuarios(limite)

        assert isinstance(pipeline, list)

        # Debe tener $limit
        tiene_limit = any(stage.get("$limit") for stage in pipeline)
        assert tiene_limit, "Pipeline debe contener $limit"

        limit_stage = next(stage for stage in pipeline if "$limit" in stage)
        assert limit_stage["$limit"] == limite

    def test_pipeline_top_usuarios_limite_negativo_lanza_error(self):
        """Debe lanzar ValueError si límite es negativo."""
        with pytest.raises(ValueError, match="Límite debe ser mayor que 0"):
            construir_pipeline_top_usuarios(-5)

    def test_pipeline_top_usuarios_limite_cero_lanza_error(self):
        """Debe lanzar ValueError si límite es cero."""
        with pytest.raises(ValueError, match="Límite debe ser mayor que 0"):
            construir_pipeline_top_usuarios(0)

    def test_pipeline_top_usuarios_tiene_group(self):
        """Debe agrupar por usuario."""
        pipeline = construir_pipeline_top_usuarios(10)

        tiene_group = any(stage.get("$group") for stage in pipeline)
        assert tiene_group, "Pipeline debe contener $group"

    def test_pipeline_top_usuarios_ordena_descendente(self):
        """Debe ordenar de mayor a menor."""
        pipeline = construir_pipeline_top_usuarios(10)

        sort_stage = next(stage["$sort"] for stage in pipeline if "$sort" in stage)
        # Verificar que algún campo tiene orden -1 (descendente)
        assert any(valor == -1 for valor in sort_stage.values())


class TestConstruirPipelineMetricasTiempo:
    """Tests para construir_pipeline_metricas_tiempo."""

    def test_pipeline_metricas_tiempo_basico(self):
        """Debe construir pipeline para métricas temporales."""
        pipeline = construir_pipeline_metricas_tiempo()

        assert isinstance(pipeline, list)
        assert len(pipeline) >= 2

    def test_pipeline_metricas_tiempo_tiene_project(self):
        """Debe tener etapa $project para extraer campos de fecha."""
        pipeline = construir_pipeline_metricas_tiempo()

        tiene_project = any(stage.get("$project") for stage in pipeline)
        assert tiene_project, "Pipeline debe contener $project"

    def test_pipeline_metricas_tiempo_agrupa_por_fecha(self):
        """Debe agrupar por campos temporales (día, hora, etc)."""
        pipeline = construir_pipeline_metricas_tiempo()

        group_stage = next(stage["$group"] for stage in pipeline if "$group" in stage)
        assert "_id" in group_stage

    def test_pipeline_metricas_tiempo_tiene_sort(self):
        """Debe ordenar por tiempo."""
        pipeline = construir_pipeline_metricas_tiempo()

        tiene_sort = any(stage.get("$sort") for stage in pipeline)
        assert tiene_sort, "Pipeline debe contener $sort"
