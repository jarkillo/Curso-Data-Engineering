"""
Tests para validaciones.py.

Tests escritos PRIMERO siguiendo TDD para módulo de validaciones.
Cobertura objetivo: ≥90% (módulo crítico para calidad de datos).
"""

import pandas as pd


class TestValidarNoNulos:
    """Tests para la función validar_no_nulos."""

    def test_datos_completos_sin_nulos(self):
        """Should return valid when no nulls in required fields."""
        from src.validaciones import validar_no_nulos

        df = pd.DataFrame(
            [
                {"cliente_id": 1, "nombre": "Juan", "email": "juan@test.com"},
                {"cliente_id": 2, "nombre": "María", "email": "maria@test.com"},
            ]
        )

        resultado = validar_no_nulos(df, ["cliente_id", "nombre", "email"])

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_detecta_nulos_en_campo_obligatorio(self):
        """Should detect nulls in required fields."""
        from src.validaciones import validar_no_nulos

        df = pd.DataFrame(
            [
                {"cliente_id": 1, "nombre": "Juan", "email": "juan@test.com"},
                {"cliente_id": 2, "nombre": None, "email": "maria@test.com"},
                {"cliente_id": 3, "nombre": "Pedro", "email": None},
            ]
        )

        resultado = validar_no_nulos(df, ["cliente_id", "nombre", "email"])

        assert not resultado["is_valid"]
        assert len(resultado["errors"]) == 2
        assert "nombre" in resultado["errors"][0]
        assert "email" in resultado["errors"][1]

    def test_dataframe_vacio_es_valido(self):
        """Should return valid for empty DataFrame."""
        from src.validaciones import validar_no_nulos

        df = pd.DataFrame()

        resultado = validar_no_nulos(df, ["campo1", "campo2"])

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_campo_no_existe_en_dataframe(self):
        """Should report error when required field doesn't exist."""
        from src.validaciones import validar_no_nulos

        df = pd.DataFrame([{"id": 1, "nombre": "Juan"}])

        resultado = validar_no_nulos(df, ["id", "campo_inexistente"])

        assert not resultado["is_valid"]
        assert "campo_inexistente" in resultado["errors"][0]
        assert "no existe" in resultado["errors"][0]


class TestValidarRangos:
    """Tests para la función validar_rangos."""

    def test_valores_dentro_de_rango(self):
        """Should return valid when values are within range."""
        from src.validaciones import validar_rangos

        df = pd.DataFrame(
            [
                {"edad": 25, "precio": 100.0},
                {"edad": 30, "precio": 500.0},
                {"edad": 45, "precio": 1000.0},
            ]
        )

        rangos = {"edad": (18, 100), "precio": (0, 10000)}

        resultado = validar_rangos(df, rangos)

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_detecta_valores_fuera_de_rango(self):
        """Should detect values outside allowed range."""
        from src.validaciones import validar_rangos

        df = pd.DataFrame(
            [
                {"edad": 25, "precio": 100.0},
                {"edad": 150, "precio": 500.0},  # edad fuera de rango
                {"edad": 30, "precio": -50.0},  # precio negativo
            ]
        )

        rangos = {"edad": (18, 100), "precio": (0, 10000)}

        resultado = validar_rangos(df, rangos)

        assert not resultado["is_valid"]
        assert len(resultado["errors"]) == 2
        assert "edad" in resultado["errors"][0]
        assert "precio" in resultado["errors"][1]

    def test_rango_None_permite_cualquier_valor(self):
        """Should allow any value when range is None."""
        from src.validaciones import validar_rangos

        df = pd.DataFrame([{"edad": 150, "nombre": "Juan"}])

        rangos = {"edad": None, "nombre": None}  # Sin límites

        resultado = validar_rangos(df, rangos)

        assert resultado["is_valid"]

    def test_dataframe_vacio_es_valido(self):
        """Should return valid for empty DataFrame."""
        from src.validaciones import validar_rangos

        df = pd.DataFrame()

        resultado = validar_rangos(df, {"edad": (0, 100)})

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_campo_no_existe_en_dataframe(self):
        """Should report error when field doesn't exist."""
        from src.validaciones import validar_rangos

        df = pd.DataFrame([{"edad": 25}])

        resultado = validar_rangos(df, {"campo_inexistente": (0, 100)})

        assert not resultado["is_valid"]
        assert "campo_inexistente" in resultado["errors"][0]
        assert "no existe" in resultado["errors"][0]


class TestValidarTipos:
    """Tests para la función validar_tipos."""

    def test_tipos_correctos(self):
        """Should return valid when types match."""
        from src.validaciones import validar_tipos

        df = pd.DataFrame(
            [
                {"cliente_id": 1, "nombre": "Juan", "precio": 100.5},
                {"cliente_id": 2, "nombre": "María", "precio": 200.0},
            ]
        )

        tipos_esperados = {"cliente_id": int, "nombre": str, "precio": float}

        resultado = validar_tipos(df, tipos_esperados)

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_detecta_tipos_incorrectos(self):
        """Should detect incorrect types."""
        from src.validaciones import validar_tipos

        df = pd.DataFrame(
            [
                {"cliente_id": "1", "nombre": "Juan", "precio": 100.5},  # ID es string
                {
                    "cliente_id": 2,
                    "nombre": 123,
                    "precio": "200",
                },  # nombre y precio incorrectos
            ]
        )

        tipos_esperados = {"cliente_id": int, "nombre": str, "precio": float}

        resultado = validar_tipos(df, tipos_esperados)

        assert not resultado["is_valid"]
        assert len(resultado["errors"]) > 0

    def test_dataframe_vacio_es_valido(self):
        """Should return valid for empty DataFrame."""
        from src.validaciones import validar_tipos

        df = pd.DataFrame()

        resultado = validar_tipos(df, {"id": int})

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_campo_no_existe_en_dataframe(self):
        """Should report error when field doesn't exist."""
        from src.validaciones import validar_tipos

        df = pd.DataFrame([{"id": 1}])

        resultado = validar_tipos(df, {"campo_inexistente": int})

        assert not resultado["is_valid"]
        assert "campo_inexistente" in resultado["errors"][0]
        assert "no existe" in resultado["errors"][0]


class TestValidarIntegridadReferencial:
    """Tests para la función validar_integridad_referencial."""

    def test_todas_las_fk_existen(self):
        """Should return valid when all FKs exist."""
        from src.validaciones import validar_integridad_referencial

        df_fact = pd.DataFrame(
            [
                {"venta_id": 1, "producto_id": 10, "cliente_id": 100},
                {"venta_id": 2, "producto_id": 20, "cliente_id": 200},
            ]
        )

        df_productos = pd.DataFrame([{"producto_id": 10}, {"producto_id": 20}])

        df_clientes = pd.DataFrame([{"cliente_id": 100}, {"cliente_id": 200}])

        relaciones = {
            "producto_id": df_productos,
            "cliente_id": df_clientes,
        }

        resultado = validar_integridad_referencial(df_fact, relaciones)

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_detecta_fk_faltantes(self):
        """Should detect missing FK references."""
        from src.validaciones import validar_integridad_referencial

        df_fact = pd.DataFrame(
            [
                {"venta_id": 1, "producto_id": 10, "cliente_id": 100},
                {
                    "venta_id": 2,
                    "producto_id": 99,
                    "cliente_id": 200,
                },  # producto_id 99 no existe
                {
                    "venta_id": 3,
                    "producto_id": 20,
                    "cliente_id": 999,
                },  # cliente_id 999 no existe
            ]
        )

        df_productos = pd.DataFrame([{"producto_id": 10}, {"producto_id": 20}])

        df_clientes = pd.DataFrame([{"cliente_id": 100}, {"cliente_id": 200}])

        relaciones = {
            "producto_id": df_productos,
            "cliente_id": df_clientes,
        }

        resultado = validar_integridad_referencial(df_fact, relaciones)

        assert not resultado["is_valid"]
        assert len(resultado["errors"]) == 2
        assert "producto_id" in resultado["errors"][0]
        assert "cliente_id" in resultado["errors"][1]

    def test_dataframe_vacio_es_valido(self):
        """Should return valid for empty DataFrame."""
        from src.validaciones import validar_integridad_referencial

        df = pd.DataFrame()
        df_ref = pd.DataFrame([{"producto_id": 1}])

        resultado = validar_integridad_referencial(df, {"producto_id": df_ref})

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_campo_fk_no_existe_en_dataframe(self):
        """Should report error when FK field doesn't exist in main DataFrame."""
        from src.validaciones import validar_integridad_referencial

        df = pd.DataFrame([{"id": 1}])
        df_ref = pd.DataFrame([{"producto_id": 1}])

        resultado = validar_integridad_referencial(df, {"producto_id": df_ref})

        assert not resultado["is_valid"]
        assert "producto_id" in resultado["errors"][0]
        assert "no existe en DataFrame" in resultado["errors"][0]

    def test_campo_fk_no_existe_en_tabla_referencia(self):
        """Should report error when FK field doesn't exist in reference table."""
        from src.validaciones import validar_integridad_referencial

        df = pd.DataFrame([{"producto_id": 1}])
        df_ref = pd.DataFrame([{"id": 1}])  # No tiene producto_id

        resultado = validar_integridad_referencial(df, {"producto_id": df_ref})

        assert not resultado["is_valid"]
        assert "producto_id" in resultado["errors"][0]
        assert "tabla de referencia" in resultado["errors"][0]


class TestValidarUnicidad:
    """Tests para la función validar_unicidad."""

    def test_campos_unicos_validos(self):
        """Should return valid when fields are unique."""
        from src.validaciones import validar_unicidad

        df = pd.DataFrame(
            [
                {"cliente_id": 1, "email": "juan@test.com"},
                {"cliente_id": 2, "email": "maria@test.com"},
                {"cliente_id": 3, "email": "pedro@test.com"},
            ]
        )

        resultado = validar_unicidad(df, ["cliente_id", "email"])

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_detecta_duplicados(self):
        """Should detect duplicate values."""
        from src.validaciones import validar_unicidad

        df = pd.DataFrame(
            [
                {"cliente_id": 1, "email": "juan@test.com"},
                {"cliente_id": 2, "email": "maria@test.com"},
                {"cliente_id": 1, "email": "pedro@test.com"},  # cliente_id duplicado
                {"cliente_id": 3, "email": "juan@test.com"},  # email duplicado
            ]
        )

        resultado = validar_unicidad(df, ["cliente_id", "email"])

        assert not resultado["is_valid"]
        assert len(resultado["errors"]) == 2
        assert "cliente_id" in resultado["errors"][0]
        assert "email" in resultado["errors"][1]

    def test_combinacion_campos_unica(self):
        """Should validate uniqueness of field combinations."""
        from src.validaciones import validar_unicidad

        df = pd.DataFrame(
            [
                {"cliente_id": 1, "producto_id": 10},
                {"cliente_id": 1, "producto_id": 20},  # OK: combinación única
                {"cliente_id": 2, "producto_id": 10},  # OK: combinación única
                {"cliente_id": 1, "producto_id": 10},  # DUPLICADO: misma combinación
            ]
        )

        resultado = validar_unicidad(df, [["cliente_id", "producto_id"]])

        assert not resultado["is_valid"]
        assert len(resultado["errors"]) == 1

    def test_dataframe_vacio_es_valido(self):
        """Should return valid for empty DataFrame."""
        from src.validaciones import validar_unicidad

        df = pd.DataFrame()

        resultado = validar_unicidad(df, ["id"])

        assert resultado["is_valid"]
        assert len(resultado["errors"]) == 0

    def test_campo_simple_no_existe(self):
        """Should report error when simple field doesn't exist."""
        from src.validaciones import validar_unicidad

        df = pd.DataFrame([{"id": 1}])

        resultado = validar_unicidad(df, ["campo_inexistente"])

        assert not resultado["is_valid"]
        assert "campo_inexistente" in resultado["errors"][0]
        assert "no existe" in resultado["errors"][0]

    def test_campos_combinacion_no_existen(self):
        """Should report error when combination fields don't exist."""
        from src.validaciones import validar_unicidad

        df = pd.DataFrame([{"id": 1}])

        resultado = validar_unicidad(df, [["campo1", "campo2"]])

        assert not resultado["is_valid"]
        assert "campo1" in resultado["errors"][0] or "campo2" in resultado["errors"][0]
