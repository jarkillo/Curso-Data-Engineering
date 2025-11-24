"""
Tests para orquestador del pipeline completo.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

from src.pipeline import ejecutar_pipeline_completo


class TestEjecutarPipelineCompleto:
    """Tests para ejecución del pipeline completo."""

    def test_ejecuta_pipeline_exitosamente(self, engine_temporal, directorio_temporal):
        """Debe ejecutar pipeline completo sin errores."""
        resultado = ejecutar_pipeline_completo(
            num_noticias=10,
            engine=engine_temporal,
            directorio_salida=directorio_temporal,
        )

        assert resultado["exito"]
        assert resultado["registros_extraidos"] == 10

    def test_retorna_metricas_completas(self, engine_temporal, directorio_temporal):
        """Debe retornar métricas completas."""
        resultado = ejecutar_pipeline_completo(
            num_noticias=5,
            engine=engine_temporal,
            directorio_salida=directorio_temporal,
        )

        assert "registros_extraidos" in resultado
        assert "registros_silver" in resultado
        assert "registros_gold" in resultado
        assert "exito" in resultado

    def test_maneja_error_gracefully(self, engine_temporal, directorio_temporal):
        """Debe manejar errores sin crash."""
        # Número de noticias inválido
        resultado = ejecutar_pipeline_completo(
            num_noticias=0,  # Inválido
            engine=engine_temporal,
            directorio_salida=directorio_temporal,
        )

        assert not resultado["exito"]
        assert "error" in resultado
