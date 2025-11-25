"""
Tests para módulo de validación de calidad.

Siguiendo metodología TDD - Tests escritos antes de implementación.
"""

import pandas as pd
import pytest

from src.validador import (
    generar_reporte_calidad,
    validar_esquema_silver,
    validar_rangos_longitud,
    validar_sin_duplicados,
)


class TestValidarEsquemaSilver:
    """Tests para validación de esquema Silver."""

    def test_valida_dataframe_correcto(self, df_noticias_silver):
        """DataFrame válido debe pasar validación."""
        # No debe levantar excepción
        validar_esquema_silver(df_noticias_silver)

    def test_falla_si_falta_columna(self):
        """Debe fallar si falta columna requerida."""
        df_invalido = pd.DataFrame(
            {
                "titulo": ["Test"],
                # Falta 'fecha_publicacion'
            }
        )

        with pytest.raises(Exception):  # Pandera levanta SchemaError
            validar_esquema_silver(df_invalido)

    def test_falla_si_tipo_incorrecto(self):
        """Debe fallar si tipo de dato es incorrecto."""
        df_invalido = pd.DataFrame(
            {
                "id": ["texto_no_numero"],  # Debería ser int
                "titulo": ["Test"],
                "fecha_publicacion": pd.to_datetime(["2024-01-01"]),
            }
        )

        with pytest.raises(Exception):
            validar_esquema_silver(df_invalido)


class TestValidarSinDuplicados:
    """Tests para validación de duplicados."""

    def test_sin_duplicados_retorna_true(self):
        """DataFrame sin duplicados debe retornar True."""
        df = pd.DataFrame({"id": [1, 2, 3], "titulo": ["A", "B", "C"]})

        resultado = validar_sin_duplicados(df, "id")

        assert resultado["valido"]
        assert resultado["duplicados"] == 0

    def test_con_duplicados_retorna_false(self):
        """DataFrame con duplicados debe retornar False."""
        df = pd.DataFrame(
            {"id": [1, 2, 2, 3], "titulo": ["A", "B", "B2", "C"]}  # ID 2 duplicado
        )

        resultado = validar_sin_duplicados(df, "id")

        assert not resultado["valido"]
        assert resultado["duplicados"] == 1  # 1 ID duplicado (el 2)


class TestValidarRangosLongitud:
    """Tests para validación de rangos de longitud."""

    def test_longitudes_dentro_de_rango(self):
        """Longitudes dentro del rango deben pasar."""
        df = pd.DataFrame(
            {"longitud_contenido": [50, 100, 150], "longitud_titulo": [10, 20, 30]}
        )

        resultado = validar_rangos_longitud(
            df, columna="longitud_contenido", min_val=10, max_val=200
        )

        assert resultado["valido"]
        assert resultado["fuera_de_rango"] == 0

    def test_detecta_valores_fuera_de_rango(self):
        """Debe detectar valores fuera del rango."""
        df = pd.DataFrame(
            {"longitud_contenido": [5, 100, 250]}  # 5 y 250 fuera de [10, 200]
        )

        resultado = validar_rangos_longitud(
            df, columna="longitud_contenido", min_val=10, max_val=200
        )

        assert not resultado["valido"]
        assert resultado["fuera_de_rango"] == 2


class TestGenerarReporteCalidad:
    """Tests para generación de reporte de calidad."""

    def test_genera_reporte_completo(self, df_noticias_silver):
        """Debe generar reporte con todas las secciones."""
        reporte = generar_reporte_calidad(df_noticias_silver)

        assert "total_registros" in reporte
        assert "esquema_valido" in reporte
        assert "duplicados" in reporte
        assert "longitudes_validas" in reporte

    def test_total_registros_correcto(self, df_noticias_silver):
        """Total de registros debe ser correcto."""
        reporte = generar_reporte_calidad(df_noticias_silver)

        assert reporte["total_registros"] == len(df_noticias_silver)

    def test_esquema_valido_es_boolean(self, df_noticias_silver):
        """Campo esquema_valido debe ser boolean."""
        reporte = generar_reporte_calidad(df_noticias_silver)

        assert isinstance(reporte["esquema_valido"], bool)

    def test_duplicados_tiene_conteo(self, df_noticias_silver):
        """Campo duplicados debe tener información de conteo."""
        reporte = generar_reporte_calidad(df_noticias_silver)

        assert "total" in reporte["duplicados"]
        assert isinstance(reporte["duplicados"]["total"], int)

    def test_longitudes_validas_tiene_resultado(self, df_noticias_silver):
        """Campo longitudes_validas debe tener resultado."""
        reporte = generar_reporte_calidad(df_noticias_silver)

        assert "contenido" in reporte["longitudes_validas"]
        assert "titulo" in reporte["longitudes_validas"]
