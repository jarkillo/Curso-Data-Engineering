"""
Tests para cargador_full.py.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import pandas as pd
import pytest
from sqlalchemy import text

from src.cargador_full import (
    full_load,
    full_load_con_validacion,
    full_load_idempotente,
    verificar_carga_exitosa,
)


class TestFullLoad:
    """Tests para full_load básico."""

    def test_full_load_tabla_nueva(self, df_simple, engine_temporal):
        """Debe cargar datos en tabla nueva."""
        num_cargados = full_load(df_simple, engine_temporal, "tabla_nueva")

        assert num_cargados == len(df_simple)

        # Verificar que se cargaron
        df_leido = pd.read_sql("SELECT * FROM tabla_nueva", engine_temporal)
        assert len(df_leido) == len(df_simple)

    def test_full_load_reemplaza_datos_existentes(self, df_simple, engine_temporal):
        """Debe reemplazar datos existentes completamente."""
        # Cargar datos iniciales
        df_simple.to_sql("tabla_existente", engine_temporal, index=False)

        # Cargar datos diferentes
        df_nuevos = pd.DataFrame(
            {"id": [10, 20, 30], "nombre": ["X", "Y", "Z"], "valor": [999, 888, 777]}
        )

        num_cargados = full_load(df_nuevos, engine_temporal, "tabla_existente")

        assert num_cargados == len(df_nuevos)

        # Verificar que solo están los nuevos
        df_leido = pd.read_sql("SELECT * FROM tabla_existente", engine_temporal)
        assert len(df_leido) == len(df_nuevos)
        assert df_leido["id"].tolist() == [10, 20, 30]

    def test_full_load_dataframe_vacio_levanta_error(self, engine_temporal):
        """DataFrame vacío debe levantar ValueError."""
        df_vacio = pd.DataFrame()

        with pytest.raises(ValueError, match="vacío"):
            full_load(df_vacio, engine_temporal, "tabla")

    def test_full_load_usa_transaccion(self, df_simple, engine_temporal):
        """Si falla durante carga, debe hacer rollback."""
        # Crear tabla con constraint
        with engine_temporal.begin() as conn:
            conn.execute(
                text(
                    """
                CREATE TABLE tabla_con_constraint (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    valor INTEGER
                )
            """
                )
            )

        # Intentar cargar DataFrame con ID duplicado (violará PRIMARY KEY)
        df_con_duplicado = pd.DataFrame(
            {
                "id": [1, 1, 3],  # ID duplicado
                "nombre": ["Ana", "Luis", "María"],
                "valor": [100, 200, 150],
            }
        )

        with pytest.raises(Exception):
            full_load(df_con_duplicado, engine_temporal, "tabla_con_constraint")

        # Verificar que no se cargó nada (rollback exitoso)
        df_leido = pd.read_sql("SELECT * FROM tabla_con_constraint", engine_temporal)
        assert len(df_leido) == 0

    def test_full_load_retorna_cero_si_no_carga_nada(self, engine_temporal):
        """Si no se carga nada por algún motivo, debe retornar 0."""
        df_vacio = pd.DataFrame({"id": [], "valor": []})

        with pytest.raises(ValueError, match="vacío"):
            full_load(df_vacio, engine_temporal, "tabla")


class TestFullLoadConValidacion:
    """Tests para full_load_con_validacion."""

    def test_valida_y_carga_datos_correctos(self, df_simple, engine_temporal):
        """Debe validar y cargar si datos son correctos."""
        resultado = full_load_con_validacion(
            df_simple,
            engine_temporal,
            "tabla",
            columnas_requeridas=["id", "nombre", "valor"],
        )

        assert resultado["cargados"] == len(df_simple)
        assert resultado["invalidos"] == 0
        assert resultado["valido"] is True

    def test_detecta_columnas_faltantes(self, df_simple, engine_temporal):
        """Debe detectar si faltan columnas requeridas."""
        resultado = full_load_con_validacion(
            df_simple,
            engine_temporal,
            "tabla",
            columnas_requeridas=["id", "nombre", "email"],  # email no existe
        )

        assert resultado["valido"] is False
        assert "email" in resultado["mensaje"]

    def test_no_carga_si_validacion_falla(self, df_simple, engine_temporal):
        """No debe cargar datos si la validación falla."""
        full_load_con_validacion(
            df_simple,
            engine_temporal,
            "tabla",
            columnas_requeridas=["id", "columna_inexistente"],
        )

        # Verificar que no se creó la tabla
        with pytest.raises(Exception):
            pd.read_sql("SELECT * FROM tabla", engine_temporal)

    def test_detecta_valores_nulos_en_columnas_criticas(
        self, df_invalido, engine_temporal
    ):
        """Debe detectar valores nulos en columnas críticas."""
        resultado = full_load_con_validacion(
            df_invalido, engine_temporal, "tabla", columnas_no_nulas=["id"]
        )

        assert resultado["valido"] is False
        assert resultado["invalidos"] > 0


class TestFullLoadIdempotente:
    """Tests para full_load_idempotente."""

    def test_primera_carga_exitosa(self, df_simple, engine_temporal):
        """Primera ejecución debe cargar todos los datos."""
        resultado = full_load_idempotente(df_simple, engine_temporal, "tabla")

        assert resultado["cargados"] == len(df_simple)
        assert resultado["operacion"] == "insert"

    def test_segunda_carga_reemplaza_datos(self, df_simple, engine_temporal):
        """Segunda ejecución debe reemplazar datos completamente."""
        # Primera carga
        full_load_idempotente(df_simple, engine_temporal, "tabla")

        # Segunda carga con datos diferentes
        df_nuevos = pd.DataFrame(
            {"id": [10, 20], "nombre": ["X", "Y"], "valor": [999, 888]}
        )

        resultado = full_load_idempotente(df_nuevos, engine_temporal, "tabla")

        assert resultado["cargados"] == len(df_nuevos)
        assert resultado["operacion"] == "replace"

        # Verificar que solo están los nuevos datos
        df_leido = pd.read_sql("SELECT * FROM tabla", engine_temporal)
        assert len(df_leido) == len(df_nuevos)

    def test_multiple_ejecuciones_mismo_resultado(self, df_simple, engine_temporal):
        """Ejecutar 10 veces debe producir el mismo resultado."""
        for _ in range(10):
            full_load_idempotente(df_simple, engine_temporal, "tabla")

        df_leido = pd.read_sql("SELECT * FROM tabla", engine_temporal)
        assert len(df_leido) == len(df_simple)


class TestVerificarCargaExitosa:
    """Tests para verificar_carga_exitosa."""

    def test_verificacion_exitosa_cuando_conteos_coinciden(
        self, df_simple, engine_temporal
    ):
        """Debe retornar True si los conteos coinciden."""
        full_load(df_simple, engine_temporal, "tabla")

        exito = verificar_carga_exitosa(df_simple, engine_temporal, "tabla")

        assert exito

    def test_verificacion_falla_si_conteos_difieren(self, df_simple, engine_temporal):
        """Debe retornar False si los conteos difieren."""
        # Cargar solo parte de los datos
        df_parcial = df_simple.head(2)
        full_load(df_parcial, engine_temporal, "tabla")

        # Verificar con DataFrame completo
        exito = verificar_carga_exitosa(df_simple, engine_temporal, "tabla")

        assert not exito

    def test_verificacion_falla_si_tabla_no_existe(self, df_simple, engine_temporal):
        """Debe levantar ValueError si la tabla no existe."""
        with pytest.raises(ValueError, match="No se pudo verificar tabla"):
            verificar_carga_exitosa(df_simple, engine_temporal, "tabla_inexistente")
