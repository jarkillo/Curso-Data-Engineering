"""Tests para pipeline_manager.py - Siguiendo TDD."""

import pandas as pd
import pytest
from src.pipeline_manager import (
    ejecutar_pipeline,
    seleccionar_estrategia_carga,
    validar_datos_pipeline,
)


class TestSeleccionarEstrategiaCarga:
    """Tests para selección automática de estrategia."""

    def test_dataset_pequeño_usa_full_load(self):
        """Dataset <1K filas debe usar full load."""
        df_pequeño = pd.DataFrame({"id": range(500)})
        estrategia = seleccionar_estrategia_carga(df_pequeño)

        assert estrategia == "full"

    def test_dataset_grande_con_timestamp_usa_incremental(self):
        """Dataset grande con timestamp debe usar incremental."""
        df_grande = pd.DataFrame(
            {
                "id": range(5000),
                "timestamp": pd.date_range("2024-01-01", periods=5000, freq="h"),
            }
        )
        estrategia = seleccionar_estrategia_carga(df_grande)

        assert estrategia == "incremental"

    def test_dataset_grande_con_id_usa_upsert(self):
        """Dataset grande con ID pero sin timestamp debe usar upsert."""
        df_grande = pd.DataFrame({"id": range(5000), "valor": range(5000)})
        estrategia = seleccionar_estrategia_carga(df_grande)

        assert estrategia == "upsert"


class TestValidarDatosPipeline:
    """Tests para validación de datos."""

    def test_datos_validos_pasan(self, df_simple):
        """Datos válidos deben pasar validación."""
        df_valido, df_invalido = validar_datos_pipeline(
            df_simple, columnas_requeridas=["id", "nombre", "valor"]
        )

        assert len(df_valido) == len(df_simple)
        assert len(df_invalido) == 0

    def test_detecta_nulos(self, df_invalido):
        """Debe detectar y separar registros con nulos."""
        df_valido, df_invalido_resultado = validar_datos_pipeline(
            df_invalido, columnas_no_nulas=["id", "valor"]
        )

        assert len(df_invalido_resultado) > 0

    def test_columnas_faltantes_levanta_error(self, df_simple):
        """Debe levantar error si faltan columnas requeridas."""
        with pytest.raises(ValueError, match="Faltan columnas"):
            validar_datos_pipeline(
                df_simple, columnas_requeridas=["id", "columna_inexistente"]
            )


class TestEjecutarPipeline:
    """Tests para ejecución completa del pipeline."""

    def test_pipeline_full_load_exitoso(self, df_simple, engine_temporal):
        """Pipeline con full load debe ejecutarse exitosamente."""
        resultado = ejecutar_pipeline(
            df_simple, engine_temporal, "tabla", estrategia="full"
        )

        assert resultado.success is True
        assert resultado.rows_loaded == len(df_simple)

    def test_pipeline_incremental_exitoso(
        self, df_con_fecha, engine_temporal, archivo_checkpoint_temporal
    ):
        """Pipeline con incremental debe ejecutarse exitosamente."""
        resultado = ejecutar_pipeline(
            df_con_fecha,
            engine_temporal,
            "tabla",
            estrategia="incremental",
            columna_timestamp="timestamp",
            checkpoint_file=archivo_checkpoint_temporal,
        )

        assert resultado.success is True
        assert resultado.rows_loaded == len(df_con_fecha)

    def test_pipeline_upsert_exitoso(self, df_simple, engine_temporal):
        """Pipeline con upsert debe ejecutarse exitosamente."""
        resultado = ejecutar_pipeline(
            df_simple, engine_temporal, "tabla", estrategia="upsert", columna_clave="id"
        )

        assert resultado.success is True
        assert resultado.rows_loaded == len(df_simple)

    def test_pipeline_maneja_errores(self, engine_temporal):
        """Pipeline debe capturar y reportar errores."""
        df_invalido = pd.DataFrame()  # DataFrame vacío

        resultado = ejecutar_pipeline(
            df_invalido, engine_temporal, "tabla", estrategia="full"
        )

        assert resultado.success is False
        assert resultado.error_message != ""

    def test_pipeline_con_validacion(self, df_simple, engine_temporal):
        """Pipeline con validación debe filtrar inválidos."""
        resultado = ejecutar_pipeline(
            df_simple,
            engine_temporal,
            "tabla",
            estrategia="full",
            validar=True,
            columnas_requeridas=["id", "nombre", "valor"],
        )

        assert resultado.success is True
        assert resultado.rows_validated == len(df_simple)
