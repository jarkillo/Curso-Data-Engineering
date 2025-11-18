"""Tests para batch_processor.py - Siguiendo TDD."""

import pandas as pd
from src.batch_processor import calcular_num_lotes, dividir_en_lotes, procesar_en_lotes


class TestDividirEnLotes:
    """Tests para dividir_en_lotes."""

    def test_divide_correctamente(self, df_simple):
        """Debe dividir DataFrame en lotes del tamaño especificado."""
        lotes = list(dividir_en_lotes(df_simple, batch_size=2))

        assert len(lotes) == 3  # 5 filas / 2 = 3 lotes (2, 2, 1)
        assert len(lotes[0]) == 2
        assert len(lotes[1]) == 2
        assert len(lotes[2]) == 1

    def test_batch_size_mayor_que_dataframe(self, df_simple):
        """Si batch_size > len(df), debe retornar un solo lote."""
        lotes = list(dividir_en_lotes(df_simple, batch_size=100))

        assert len(lotes) == 1
        assert len(lotes[0]) == len(df_simple)

    def test_lotes_mantienen_datos_completos(self, df_grande):
        """Todos los lotes juntos deben contener todos los datos."""
        lotes = list(dividir_en_lotes(df_grande, batch_size=1000))

        total_filas = sum(len(lote) for lote in lotes)
        assert total_filas == len(df_grande)


class TestProcesarEnLotes:
    """Tests para procesar_en_lotes."""

    def test_procesa_todos_los_lotes(self, df_grande, engine_temporal):
        """Debe procesar todos los lotes."""
        resultado = procesar_en_lotes(
            df_grande, engine_temporal, "tabla", batch_size=1000
        )

        assert resultado["total_filas"] == len(df_grande)
        assert resultado["num_lotes"] == 10  # 10K / 1K = 10

    def test_carga_es_completa(self, df_grande, engine_temporal):
        """Todas las filas deben cargarse."""
        procesar_en_lotes(df_grande, engine_temporal, "tabla", batch_size=1000)

        total_bd = pd.read_sql(
            "SELECT COUNT(*) as total FROM tabla", engine_temporal
        ).iloc[0]["total"]
        assert total_bd == len(df_grande)


class TestCalcularNumLotes:
    """Tests para calcular_num_lotes."""

    def test_calculo_exacto(self):
        """Debe calcular correctamente el número de lotes."""
        assert calcular_num_lotes(1000, 100) == 10
        assert calcular_num_lotes(1001, 100) == 11
        assert calcular_num_lotes(99, 100) == 1
