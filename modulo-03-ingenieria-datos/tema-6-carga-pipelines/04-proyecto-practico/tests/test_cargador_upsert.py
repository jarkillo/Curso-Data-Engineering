"""
Tests para cargador_upsert.py.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import pandas as pd
import pytest
from src.cargador_upsert import detectar_cambios, upsert, upsert_con_metricas


class TestUpsert:
    """Tests para upsert básico."""

    def test_inserta_registros_nuevos(self, df_simple, engine_temporal):
        """Debe insertar registros que no existen."""
        upsert(df_simple, engine_temporal, "tabla", "id")

        df_leido = pd.read_sql("SELECT * FROM tabla ORDER BY id", engine_temporal)
        assert len(df_leido) == len(df_simple)

    def test_actualiza_registros_existentes(self, df_simple, engine_temporal):
        """Debe actualizar registros que ya existen."""
        # Cargar datos iniciales
        df_simple.to_sql("tabla", engine_temporal, index=False)

        # Datos modificados
        df_modificado = df_simple.copy()
        df_modificado.loc[df_modificado["id"] == 2, "valor"] = 999

        upsert(df_modificado, engine_temporal, "tabla", "id")

        # Verificar actualización
        df_leido = pd.read_sql("SELECT * FROM tabla WHERE id = 2", engine_temporal)
        assert df_leido.iloc[0]["valor"] == 999

    def test_inserta_y_actualiza_simultaneamente(self, df_simple, engine_temporal):
        """Debe insertar nuevos y actualizar existentes."""
        # Cargar primeros 3 registros
        df_inicial = df_simple.head(3)
        df_inicial.to_sql("tabla", engine_temporal, index=False)

        # Datos mixtos: 2 existentes modificados + 2 nuevos
        df_mixto = pd.DataFrame(
            {
                "id": [2, 3, 6, 7],  # 2,3 existen, 6,7 son nuevos
                "nombre": ["Luis Updated", "María Updated", "Nueva1", "Nueva2"],
                "valor": [999, 888, 600, 700],
            }
        )

        upsert(df_mixto, engine_temporal, "tabla", "id")

        # Verificar
        df_leido = pd.read_sql("SELECT * FROM tabla ORDER BY id", engine_temporal)
        assert len(df_leido) == 5  # 1 (sin tocar) + 2 (actualizados) + 2 (nuevos)

    def test_columna_clave_no_existe_levanta_error(self, df_simple, engine_temporal):
        """Debe levantar error si la columna clave no existe."""
        with pytest.raises(ValueError, match="no existe"):
            upsert(df_simple, engine_temporal, "tabla", "columna_inexistente")


class TestUpsertConMetricas:
    """Tests para upsert con métricas."""

    def test_primera_carga_solo_inserts(self, df_simple, engine_temporal):
        """Primera carga debe ser solo inserts."""
        resultado = upsert_con_metricas(df_simple, engine_temporal, "tabla", "id")

        assert resultado["inserts"] == len(df_simple)
        assert resultado["updates"] == 0

    def test_segunda_carga_solo_updates(self, df_simple, engine_temporal):
        """Segunda carga con mismos IDs debe ser solo updates."""
        # Primera carga
        upsert_con_metricas(df_simple, engine_temporal, "tabla", "id")

        # Segunda carga con mismos IDs
        df_modificado = df_simple.copy()
        df_modificado["valor"] = df_modificado["valor"] * 2

        resultado = upsert_con_metricas(df_modificado, engine_temporal, "tabla", "id")

        assert resultado["inserts"] == 0
        assert resultado["updates"] == len(df_simple)

    def test_carga_mixta_inserts_y_updates(self, df_simple, engine_temporal):
        """Carga con registros nuevos y existentes."""
        # Cargar primeros 3
        df_inicial = df_simple.head(3)
        upsert_con_metricas(df_inicial, engine_temporal, "tabla", "id")

        # Cargar todos (3 existentes + 2 nuevos)
        resultado = upsert_con_metricas(df_simple, engine_temporal, "tabla", "id")

        assert resultado["inserts"] == 2
        assert resultado["updates"] == 3


class TestDetectarCambios:
    """Tests para detectar cambios."""

    def test_detecta_registros_nuevos(self, df_simple, engine_temporal):
        """Debe identificar registros que no existen en BD."""
        # Cargar algunos registros
        df_simple.head(2).to_sql("tabla", engine_temporal, index=False)

        df_nuevos, df_existentes = detectar_cambios(
            df_simple, engine_temporal, "tabla", "id"
        )

        assert len(df_nuevos) == 3  # IDs 3, 4, 5
        assert len(df_existentes) == 2  # IDs 1, 2

    def test_tabla_vacia_todos_son_nuevos(self, df_simple, engine_temporal):
        """Si tabla no existe, todos son nuevos."""
        df_nuevos, df_existentes = detectar_cambios(
            df_simple, engine_temporal, "tabla_no_existe", "id"
        )

        assert len(df_nuevos) == len(df_simple)
        assert len(df_existentes) == 0


class TestUpsertSeguridad:
    """Tests de seguridad para upsert."""

    def test_maneja_claves_con_quotes_sin_sql_injection(self, engine_temporal):
        """Should handle keys with quotes without SQL injection."""
        from src.cargador_upsert import upsert

        # Crear datos con claves que contienen quotes (potencial SQL injection)
        df_peligroso = pd.DataFrame(
            {
                "codigo": ["ABC'123", "DEF\"456", "GHI'; DROP TABLE test; --"],
                "valor": [100, 200, 300],
            }
        )

        # Primera carga - debe funcionar sin error
        upsert(df_peligroso, engine_temporal, "tabla_segura", "codigo")

        # Verificar que se cargaron los 3 registros
        resultado = pd.read_sql("SELECT * FROM tabla_segura", engine_temporal)
        assert len(resultado) == 3

        # Segunda carga con mismas claves (debe actualizar sin SQL injection)
        df_actualizacion = pd.DataFrame(
            {
                "codigo": ["ABC'123", "DEF\"456", "GHI'; DROP TABLE test; --"],
                "valor": [999, 888, 777],
            }
        )

        upsert(df_actualizacion, engine_temporal, "tabla_segura", "codigo")

        # Verificar que sigue habiendo 3 registros (no se duplicaron)
        resultado = pd.read_sql("SELECT * FROM tabla_segura", engine_temporal)
        assert len(resultado) == 3

        # Verificar que los valores se actualizaron
        assert set(resultado["valor"].tolist()) == {999, 888, 777}

    def test_maneja_claves_con_comas(self, engine_temporal):
        """Should handle keys containing commas."""
        from src.cargador_upsert import upsert

        # Claves con comas (podrían romper el parsing del IN clause)
        df_comas = pd.DataFrame(
            {
                "codigo": ["A,B,C", "D,E,F", "G,H,I"],
                "valor": [100, 200, 300],
            }
        )

        # Debe funcionar sin error
        upsert(df_comas, engine_temporal, "tabla_comas", "codigo")

        resultado = pd.read_sql("SELECT * FROM tabla_comas", engine_temporal)
        assert len(resultado) == 3
        assert "A,B,C" in resultado["codigo"].tolist()
