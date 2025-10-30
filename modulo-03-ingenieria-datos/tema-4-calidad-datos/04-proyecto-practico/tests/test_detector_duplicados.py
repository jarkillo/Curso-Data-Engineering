"""Tests para detector_duplicados.py - Metodología TDD - Cobertura >90%."""

import pandas as pd
import pytest

# Imports que se implementarán
from src.detector_duplicados import (
    detectar_duplicados_exactos,
    detectar_duplicados_fuzzy,
    eliminar_duplicados_con_estrategia,
    generar_reporte_duplicados,
    marcar_duplicados_probables,
)


class TestDetectarDuplicadosExactos:
    """Tests para detectar_duplicados_exactos."""

    def test_sin_duplicados(self, df_basico):
        """Verifica detección correcta cuando no hay duplicados."""
        duplicados = detectar_duplicados_exactos(df_basico, ["id"])

        assert duplicados.sum() == 0

    def test_con_duplicados(self, df_con_duplicados):
        """Verifica detección de duplicados exactos."""
        duplicados = detectar_duplicados_exactos(df_con_duplicados, ["id"])

        assert duplicados.sum() > 0
        assert duplicados.sum() == 4  # 2 pares de duplicados = 4 registros

    def test_multiples_columnas(self):
        """Verifica detección con múltiples columnas."""
        df = pd.DataFrame(
            {
                "nombre": ["Ana", "Ana", "Luis"],
                "apellido": ["García", "López", "García"],
            }
        )

        # Solo nombre duplicado
        dup_nombre = detectar_duplicados_exactos(df, ["nombre"])
        assert dup_nombre.sum() == 2

        # Nombre + apellido (sin duplicados)
        dup_ambos = detectar_duplicados_exactos(df, ["nombre", "apellido"])
        assert dup_ambos.sum() == 0

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            detectar_duplicados_exactos(df_vacio, ["id"])

    def test_columna_no_existe(self, df_basico):
        """Verifica manejo de columna inexistente."""
        with pytest.raises(KeyError, match="no existe"):
            detectar_duplicados_exactos(df_basico, ["columna_inexistente"])


class TestDetectarDuplicadosFuzzy:
    """Tests para detectar_duplicados_fuzzy."""

    def test_nombres_identicos(self):
        """Verifica que detecta nombres muy similares."""
        df = pd.DataFrame({"nombre": ["Juan Pérez", "Juan Perez", "María López"]})

        duplicados = detectar_duplicados_fuzzy(df, "nombre", umbral=90)

        # Debe detectar Juan Pérez vs Juan Perez
        assert len(duplicados) >= 1
        if len(duplicados) > 0:
            assert duplicados.iloc[0]["score"] >= 90

    def test_nombres_similares(self, df_nombres_similares):
        """Verifica detección de nombres similares."""
        duplicados = detectar_duplicados_fuzzy(
            df_nombres_similares, "nombre", umbral=85
        )

        # Debe encontrar al menos los pares con/sin tildes
        assert len(duplicados) >= 3

    def test_umbral_alto(self, df_nombres_similares):
        """Verifica que umbral alto reduce matches."""
        duplicados_bajo = detectar_duplicados_fuzzy(
            df_nombres_similares, "nombre", umbral=70
        )
        duplicados_alto = detectar_duplicados_fuzzy(
            df_nombres_similares, "nombre", umbral=95
        )

        assert len(duplicados_bajo) >= len(duplicados_alto)

    def test_sin_duplicados_fuzzy(self):
        """Verifica cuando no hay duplicados fuzzy."""
        df = pd.DataFrame({"nombre": ["Ana García", "Luis Martín", "Pedro Sánchez"]})

        duplicados = detectar_duplicados_fuzzy(df, "nombre", umbral=85)

        assert len(duplicados) == 0

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            detectar_duplicados_fuzzy(df_vacio, "nombre")


class TestEliminarDuplicadosConEstrategia:
    """Tests para eliminar_duplicados_con_estrategia."""

    def test_estrategia_primero(self, df_con_duplicados):
        """Verifica estrategia 'primero'."""
        registros_originales = len(df_con_duplicados)
        df_limpio = eliminar_duplicados_con_estrategia(
            df_con_duplicados, ["id"], estrategia="primero"
        )

        assert len(df_limpio) < registros_originales
        assert df_limpio["id"].is_unique

    def test_estrategia_ultimo(self, df_con_duplicados):
        """Verifica estrategia 'ultimo'."""
        df_limpio = eliminar_duplicados_con_estrategia(
            df_con_duplicados, ["id"], estrategia="ultimo"
        )

        assert df_limpio["id"].is_unique

    def test_estrategia_mas_completo(self, df_con_nulos):
        """Verifica estrategia 'mas_completo'."""
        # Añadir duplicados con diferentes niveles de completitud
        df = pd.DataFrame(
            {
                "id": [1, 1, 2, 2],
                "nombre": ["Ana", "Ana", "Luis", None],
                "email": [None, "ana@email.com", "luis@email.com", "luis@email.com"],
                "telefono": ["611111111", "611111111", None, "622222222"],
            }
        )

        df_limpio = eliminar_duplicados_con_estrategia(
            df, ["id"], estrategia="mas_completo"
        )

        assert len(df_limpio) == 2
        # Debe mantener el registro más completo del id=1
        registro_id1 = df_limpio[df_limpio["id"] == 1].iloc[0]
        assert pd.notna(registro_id1["email"])

    def test_estrategia_invalida(self, df_con_duplicados):
        """Verifica manejo de estrategia inválida."""
        with pytest.raises(ValueError, match="Estrategia"):
            eliminar_duplicados_con_estrategia(
                df_con_duplicados, ["id"], estrategia="estrategia_invalida"
            )

    def test_sin_duplicados(self, df_basico):
        """Verifica que no modifica DataFrame sin duplicados."""
        df_limpio = eliminar_duplicados_con_estrategia(df_basico, ["id"])

        assert len(df_limpio) == len(df_basico)


class TestMarcarDuplicadosProbables:
    """Tests para marcar_duplicados_probables."""

    def test_marcar_duplicados(self, df_con_duplicados):
        """Verifica marcado correcto de duplicados."""
        df_marcado = marcar_duplicados_probables(df_con_duplicados, ["id"])

        assert "es_duplicado" in df_marcado.columns
        assert df_marcado["es_duplicado"].dtype == bool
        assert df_marcado["es_duplicado"].sum() > 0

    def test_sin_duplicados(self, df_basico):
        """Verifica que marca False cuando no hay duplicados."""
        df_marcado = marcar_duplicados_probables(df_basico, ["id"])

        assert "es_duplicado" in df_marcado.columns
        assert df_marcado["es_duplicado"].sum() == 0

    def test_multiples_columnas(self):
        """Verifica marcado con múltiples columnas."""
        df = pd.DataFrame(
            {
                "nombre": ["Ana", "Ana", "Luis"],
                "apellido": ["García", "García", "López"],
            }
        )

        df_marcado = marcar_duplicados_probables(df, ["nombre", "apellido"])

        assert df_marcado["es_duplicado"].sum() == 2  # Las dos Ana García

    def test_dataframe_no_modificado(self, df_con_duplicados):
        """Verifica que no modifica el DataFrame original."""
        df_marcado = marcar_duplicados_probables(df_con_duplicados, ["id"])

        assert "es_duplicado" not in df_con_duplicados.columns
        assert "es_duplicado" in df_marcado.columns


class TestGenerarReporteDuplicados:
    """Tests para generar_reporte_duplicados."""

    def test_reporte_sin_duplicados(self, df_basico):
        """Verifica reporte cuando no hay duplicados."""
        reporte = generar_reporte_duplicados(df_basico, ["id"])

        assert reporte["total_registros"] == len(df_basico)
        assert reporte["registros_duplicados"] == 0
        assert reporte["porcentaje_duplicados"] == 0.0

    def test_reporte_con_duplicados(self, df_con_duplicados):
        """Verifica reporte con duplicados."""
        reporte = generar_reporte_duplicados(df_con_duplicados, ["id"])

        assert reporte["total_registros"] == len(df_con_duplicados)
        assert reporte["registros_duplicados"] > 0
        assert reporte["porcentaje_duplicados"] > 0
        assert "grupos_duplicados" in reporte

    def test_conteo_grupos(self):
        """Verifica conteo correcto de grupos."""
        df = pd.DataFrame({"id": [1, 1, 2, 2, 2, 3]})

        reporte = generar_reporte_duplicados(df, ["id"])

        assert reporte["grupos_duplicados"] == 2  # id=1 (2 veces) e id=2 (3 veces)
        assert reporte["registros_duplicados"] == 5  # Todos excepto id=3

    def test_estadisticas_incluidas(self, df_con_duplicados):
        """Verifica que incluye todas las estadísticas necesarias."""
        reporte = generar_reporte_duplicados(df_con_duplicados, ["id"])

        campos_requeridos = [
            "total_registros",
            "registros_duplicados",
            "registros_unicos",
            "porcentaje_duplicados",
            "grupos_duplicados",
        ]

        for campo in campos_requeridos:
            assert campo in reporte

    def test_dataframe_vacio(self, df_vacio):
        """Verifica que falla con DataFrame vacío."""
        with pytest.raises(ValueError, match="vacío"):
            generar_reporte_duplicados(df_vacio, ["id"])
