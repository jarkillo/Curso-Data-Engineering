"""
Tests para cargador_incremental.py.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

from pathlib import Path

import pandas as pd
import pytest
from src.cargador_incremental import (
    guardar_checkpoint,
    incremental_load,
    incremental_load_con_validacion,
    leer_checkpoint,
)


class TestCheckpoint:
    """Tests para manejo de checkpoint."""

    def test_guardar_checkpoint_crea_archivo(self, archivo_checkpoint_temporal):
        """Debe crear archivo de checkpoint."""
        guardar_checkpoint(100, archivo_checkpoint_temporal)

        assert Path(archivo_checkpoint_temporal).exists()

    def test_leer_checkpoint_retorna_valor_correcto(self, archivo_checkpoint_temporal):
        """Debe leer el valor guardado."""
        guardar_checkpoint(250, archivo_checkpoint_temporal)

        ultimo_id = leer_checkpoint(archivo_checkpoint_temporal)

        assert ultimo_id == 250

    def test_leer_checkpoint_archivo_no_existe_retorna_cero(self, directorio_temporal):
        """Si el archivo no existe, debe retornar 0."""
        checkpoint_inexistente = directorio_temporal / "no_existe.txt"

        ultimo_id = leer_checkpoint(str(checkpoint_inexistente))

        assert ultimo_id == 0

    def test_checkpoint_con_timestamp(self, archivo_checkpoint_temporal):
        """Debe poder guardar y leer timestamps."""
        timestamp = pd.Timestamp("2024-01-15 10:30:00")

        guardar_checkpoint(str(timestamp), archivo_checkpoint_temporal)
        checkpoint_leido = leer_checkpoint(archivo_checkpoint_temporal)

        assert checkpoint_leido == str(timestamp)


class TestIncrementalLoad:
    """Tests para incremental_load."""

    def test_primera_carga_sin_checkpoint(
        self, df_con_fecha, engine_temporal, archivo_checkpoint_temporal
    ):
        """Primera carga debe procesar todos los registros."""
        resultado = incremental_load(
            df_con_fecha,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        assert resultado["procesados"] == len(df_con_fecha)
        assert resultado["cargados"] == len(df_con_fecha)
        assert resultado["omitidos"] == 0

    def test_segunda_carga_con_checkpoint_omite_antiguos(
        self, df_con_fecha, engine_temporal, archivo_checkpoint_temporal
    ):
        """Segunda carga debe omitir registros ya procesados."""
        # Primera carga
        incremental_load(
            df_con_fecha,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        # Segunda carga con los mismos datos
        resultado = incremental_load(
            df_con_fecha,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        assert resultado["cargados"] == 0
        assert resultado["omitidos"] == len(df_con_fecha)

    def test_carga_solo_registros_nuevos(
        self, df_con_fecha, engine_temporal, archivo_checkpoint_temporal
    ):
        """Debe cargar solo registros con timestamp mayor al checkpoint."""
        # Cargar primeros 5 registros
        df_primeros = df_con_fecha.head(5)
        incremental_load(
            df_primeros,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        # Intentar cargar todos (incluye los 5 ya cargados + 5 nuevos)
        resultado = incremental_load(
            df_con_fecha,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        assert resultado["cargados"] == 5  # Solo los nuevos
        assert resultado["omitidos"] == 5  # Los ya procesados

    def test_actualiza_checkpoint_con_timestamp_maximo(
        self, df_con_fecha, engine_temporal, archivo_checkpoint_temporal
    ):
        """Debe actualizar checkpoint con el timestamp máximo."""
        incremental_load(
            df_con_fecha,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        checkpoint = pd.Timestamp(leer_checkpoint(archivo_checkpoint_temporal))
        timestamp_max = df_con_fecha["timestamp"].max()

        assert checkpoint == timestamp_max

    def test_dataframe_vacio_no_levanta_error(
        self, engine_temporal, archivo_checkpoint_temporal
    ):
        """DataFrame vacío debe manejarse sin error."""
        df_vacio = pd.DataFrame({"timestamp": [], "valor": []})

        resultado = incremental_load(
            df_vacio, engine_temporal, "tabla", "timestamp", archivo_checkpoint_temporal
        )

        assert resultado["procesados"] == 0
        assert resultado["cargados"] == 0

    def test_columna_timestamp_no_existe_levanta_error(
        self, df_simple, engine_temporal, archivo_checkpoint_temporal
    ):
        """Debe levantar error si la columna de timestamp no existe."""
        with pytest.raises(ValueError, match="no existe"):
            incremental_load(
                df_simple,
                engine_temporal,
                "tabla",
                "columna_inexistente",
                archivo_checkpoint_temporal,
            )


class TestIncrementalLoadConValidacion:
    """Tests para incremental_load_con_validacion."""

    def test_valida_y_carga_datos_correctos(
        self, df_con_fecha, engine_temporal, archivo_checkpoint_temporal
    ):
        """Debe validar y cargar datos correctos."""
        resultado = incremental_load_con_validacion(
            df_con_fecha,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
            columnas_requeridas=["id", "timestamp", "valor"],
        )

        assert resultado["valido"] is True
        assert resultado["cargados"] == len(df_con_fecha)

    def test_detecta_columnas_faltantes(
        self, df_con_fecha, engine_temporal, archivo_checkpoint_temporal
    ):
        """Debe detectar columnas faltantes."""
        resultado = incremental_load_con_validacion(
            df_con_fecha,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
            columnas_requeridas=["id", "columna_inexistente"],
        )

        assert resultado["valido"] is False
        assert "Faltan columnas" in resultado["mensaje"]

    def test_filtra_registros_invalidos_antes_de_cargar(
        self, engine_temporal, archivo_checkpoint_temporal
    ):
        """Debe filtrar registros inválidos antes de cargar."""
        df_con_invalidos = pd.DataFrame(
            {
                "id": [1, 2, None, 4],  # ID nulo
                "timestamp": pd.date_range("2024-01-15", periods=4, freq="h"),
                "valor": [100, 200, 300, 400],
            }
        )

        resultado = incremental_load_con_validacion(
            df_con_invalidos,
            engine_temporal,
            "tabla",
            "timestamp",
            archivo_checkpoint_temporal,
            columnas_no_nulas=["id"],
        )

        assert resultado["cargados"] == 3  # Solo los válidos
        assert resultado["invalidos"] == 1  # El que tiene ID nulo

    def test_maneja_timestamps_con_timezone(
        self, engine_temporal, archivo_checkpoint_temporal
    ):
        """Should handle timezone-aware timestamps without error."""
        from src.cargador_incremental import incremental_load

        # Crear DataFrame con timestamps timezone-aware (UTC)
        df_tz_aware = pd.DataFrame(
            {
                "id": [1, 2, 3],
                "timestamp": pd.date_range("2024-01-15", periods=3, freq="h", tz="UTC"),
                "valor": [100, 200, 300],
            }
        )

        # Primera carga (sin checkpoint previo)
        resultado = incremental_load(
            df_tz_aware,
            engine_temporal,
            "tabla_tz",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        # Debe cargar todos los registros sin error
        assert resultado["cargados"] == 3
        assert resultado["procesados"] == 3
        assert resultado["omitidos"] == 0

        # Segunda carga con solo 1 registro nuevo
        df_nuevo = pd.DataFrame(
            {
                "id": [4],
                "timestamp": pd.date_range("2024-01-15 03:00", periods=1, tz="UTC"),
                "valor": [400],
            }
        )

        resultado2 = incremental_load(
            df_nuevo,
            engine_temporal,
            "tabla_tz",
            "timestamp",
            archivo_checkpoint_temporal,
        )

        # Solo debe cargar el nuevo
        assert resultado2["cargados"] == 1
        assert resultado2["omitidos"] == 0
