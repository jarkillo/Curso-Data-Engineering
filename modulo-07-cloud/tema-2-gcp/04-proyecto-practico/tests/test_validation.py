"""
Tests para el módulo validation.py

Tests exhaustivos para validación de registros de pacientes.
"""

from datetime import datetime, timedelta

import pytest

from src.validation import (
    validar_diagnostico,
    validar_edad,
    validar_fecha_nacimiento,
    validar_paciente_id,
    validar_registro_completo,
)


class TestValidarPacienteId:
    """Tests para validar_paciente_id()"""

    def test_formato_correcto_con_p_mayuscula(self):
        """Debe aceptar formato P seguido de números"""
        es_valido, _ = validar_paciente_id("P001")
        assert es_valido is True

    def test_formato_correcto_con_varios_digitos(self):
        """Debe aceptar diferentes números de dígitos"""
        assert validar_paciente_id("P1")[0] is True
        assert validar_paciente_id("P12")[0] is True
        assert validar_paciente_id("P123")[0] is True
        assert validar_paciente_id("P1234")[0] is True

    def test_rechazar_id_vacio(self):
        """Debe rechazar string vacío"""
        es_valido, mensaje = validar_paciente_id("")
        assert es_valido is False
        assert "vacío" in mensaje.lower() or "requerido" in mensaje.lower()

    def test_rechazar_sin_letra_p(self):
        """Debe rechazar IDs sin letra P"""
        es_valido, mensaje = validar_paciente_id("001")
        assert es_valido is False
        assert "p" in mensaje.lower() or "formato" in mensaje.lower()

    def test_rechazar_p_minuscula(self):
        """Debe rechazar p minúscula"""
        es_valido, mensaje = validar_paciente_id("p001")
        assert es_valido is False

    def test_rechazar_sin_numeros(self):
        """Debe rechazar P sin números"""
        es_valido, mensaje = validar_paciente_id("P")
        assert es_valido is False

    def test_rechazar_con_letras_despues(self):
        """Debe rechazar letras después de números"""
        es_valido, mensaje = validar_paciente_id("P001ABC")
        assert es_valido is False

    def test_rechazar_espacios(self):
        """Debe rechazar IDs con espacios"""
        es_valido, mensaje = validar_paciente_id("P 001")
        assert es_valido is False


class TestValidarEdad:
    """Tests para validar_edad()"""

    def test_edad_valida_positiva(self):
        """Debe aceptar edades positivas"""
        es_valido, _ = validar_edad(25)
        assert es_valido is True

    def test_edad_cero_valida(self):
        """Debe aceptar edad 0 (recién nacidos)"""
        es_valido, _ = validar_edad(0)
        assert es_valido is True

    def test_edad_maxima_razonable(self):
        """Debe aceptar edades hasta 120 años"""
        es_valido, _ = validar_edad(120)
        assert es_valido is True

    def test_rechazar_edad_negativa(self):
        """Debe rechazar edades negativas"""
        es_valido, mensaje = validar_edad(-1)
        assert es_valido is False
        assert "negativa" in mensaje.lower() or "mayor" in mensaje.lower()

    def test_rechazar_edad_excesiva(self):
        """Debe rechazar edades > 120"""
        es_valido, mensaje = validar_edad(121)
        assert es_valido is False
        assert "120" in mensaje or "excesiva" in mensaje.lower()

    def test_rechazar_edad_string(self):
        """Debe rechazar strings"""
        es_valido, mensaje = validar_edad("veinticinco")
        assert es_valido is False
        assert "tipo" in mensaje.lower() or "número" in mensaje.lower()

    def test_rechazar_edad_float(self):
        """Debe rechazar floats"""
        es_valido, mensaje = validar_edad(25.5)
        assert es_valido is False
        assert "entero" in mensaje.lower() or "tipo" in mensaje.lower()

    def test_rechazar_edad_none(self):
        """Debe rechazar None"""
        es_valido, mensaje = validar_edad(None)
        assert es_valido is False

    def test_aceptar_edad_string_numerico(self):
        """Debe convertir strings numéricos válidos"""
        es_valido, _ = validar_edad("25")
        assert es_valido is True


class TestValidarDiagnostico:
    """Tests para validar_diagnostico()"""

    def test_diagnostico_valido(self):
        """Debe aceptar diagnósticos válidos"""
        es_valido, _ = validar_diagnostico("Diabetes")
        assert es_valido is True

    def test_diagnostico_con_espacios(self):
        """Debe aceptar diagnósticos con espacios"""
        es_valido, _ = validar_diagnostico("Diabetes Tipo 2")
        assert es_valido is True

    def test_diagnostico_con_tildes(self):
        """Debe aceptar diagnósticos con tildes"""
        es_valido, _ = validar_diagnostico("Hipertensión")
        assert es_valido is True

    def test_rechazar_diagnostico_vacio(self):
        """Debe rechazar string vacío"""
        es_valido, mensaje = validar_diagnostico("")
        assert es_valido is False
        assert "vacío" in mensaje.lower() or "requerido" in mensaje.lower()

    def test_rechazar_diagnostico_solo_espacios(self):
        """Debe rechazar strings con solo espacios"""
        es_valido, mensaje = validar_diagnostico("   ")
        assert es_valido is False

    def test_rechazar_diagnostico_demasiado_corto(self):
        """Debe rechazar diagnósticos muy cortos (<3 caracteres)"""
        es_valido, mensaje = validar_diagnostico("AB")
        assert es_valido is False
        assert "corto" in mensaje.lower() or "minimo" in mensaje.lower()

    def test_rechazar_diagnostico_none(self):
        """Debe rechazar None"""
        es_valido, mensaje = validar_diagnostico(None)
        assert es_valido is False


class TestValidarFechaNacimiento:
    """Tests para validar_fecha_nacimiento()"""

    def test_fecha_valida_formato_iso(self):
        """Debe aceptar fecha en formato ISO (YYYY-MM-DD)"""
        es_valido, _ = validar_fecha_nacimiento("1990-01-15")
        assert es_valido is True

    def test_fecha_valida_antigua(self):
        """Debe aceptar fechas antiguas (100+ años atrás)"""
        es_valido, _ = validar_fecha_nacimiento("1920-05-20")
        assert es_valido is True

    def test_rechazar_fecha_futura(self):
        """Debe rechazar fechas futuras"""
        fecha_futura = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        es_valido, mensaje = validar_fecha_nacimiento(fecha_futura)
        assert es_valido is False
        assert "futura" in mensaje.lower()

    def test_rechazar_formato_incorrecto_dd_mm_yyyy(self):
        """Debe rechazar formato DD-MM-YYYY"""
        es_valido, mensaje = validar_fecha_nacimiento("15-01-1990")
        assert es_valido is False
        assert "formato" in mensaje.lower()

    def test_rechazar_formato_incorrecto_mm_dd_yyyy(self):
        """Debe rechazar formato MM-DD-YYYY"""
        es_valido, mensaje = validar_fecha_nacimiento("01-15-1990")
        assert es_valido is False

    def test_rechazar_fecha_invalida(self):
        """Debe rechazar fechas inválidas (ej: 30 de febrero)"""
        es_valido, mensaje = validar_fecha_nacimiento("1990-02-30")
        assert es_valido is False
        assert "inválida" in mensaje.lower() or "formato" in mensaje.lower()

    def test_rechazar_fecha_string_vacio(self):
        """Debe rechazar string vacío"""
        es_valido, mensaje = validar_fecha_nacimiento("")
        assert es_valido is False

    def test_rechazar_fecha_none(self):
        """Debe rechazar None"""
        es_valido, mensaje = validar_fecha_nacimiento(None)
        assert es_valido is False

    def test_aceptar_fecha_hoy(self):
        """Debe aceptar fecha de hoy (recién nacidos)"""
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        es_valido, _ = validar_fecha_nacimiento(fecha_hoy)
        assert es_valido is True


class TestValidarRegistroCompleto:
    """Tests para validar_registro_completo()"""

    def test_registro_valido_completo(self):
        """Debe aceptar registro válido con todos los campos"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
            "fecha_nacimiento": "1980-01-15",
        }
        es_valido, _ = validar_registro_completo(registro)
        assert es_valido is True

    def test_rechazar_registro_sin_paciente_id(self):
        """Debe rechazar registro sin paciente_id"""
        registro = {
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False
        assert "paciente_id" in mensaje.lower()

    def test_rechazar_registro_sin_nombre(self):
        """Debe rechazar registro sin nombre"""
        registro = {
            "paciente_id": "P001",
            "edad": 45,
            "diagnostico": "Diabetes",
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False
        assert "nombre" in mensaje.lower()

    def test_rechazar_registro_sin_edad(self):
        """Debe rechazar registro sin edad"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "diagnostico": "Diabetes",
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False
        assert "edad" in mensaje.lower()

    def test_rechazar_registro_sin_diagnostico(self):
        """Debe rechazar registro sin diagnóstico"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False
        assert "diagnostico" in mensaje.lower()

    def test_rechazar_registro_con_paciente_id_invalido(self):
        """Debe rechazar registro con paciente_id inválido"""
        registro = {
            "paciente_id": "invalid",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False
        assert "paciente_id" in mensaje.lower()

    def test_rechazar_registro_con_edad_negativa(self):
        """Debe rechazar registro con edad negativa"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": -5,
            "diagnostico": "Diabetes",
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False
        assert "edad" in mensaje.lower()

    def test_rechazar_registro_con_diagnostico_vacio(self):
        """Debe rechazar registro con diagnóstico vacío"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "",
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False

    def test_aceptar_registro_sin_fecha_nacimiento(self):
        """Debe aceptar registro sin fecha_nacimiento (campo opcional)"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
        }
        es_valido, _ = validar_registro_completo(registro)
        assert es_valido is True

    def test_rechazar_registro_con_fecha_nacimiento_invalida(self):
        """Debe rechazar registro con fecha_nacimiento inválida"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
            "fecha_nacimiento": "invalid-date",
        }
        es_valido, mensaje = validar_registro_completo(registro)
        assert es_valido is False
        assert "fecha" in mensaje.lower()


# Fixtures
@pytest.fixture
def registro_valido():
    """Fixture con registro válido para reutilizar"""
    return {
        "paciente_id": "P001",
        "nombre": "Juan Pérez",
        "edad": 45,
        "diagnostico": "Diabetes Tipo 2",
        "fecha_nacimiento": "1980-01-15",
    }


@pytest.fixture
def registro_invalido():
    """Fixture con registro inválido"""
    return {
        "paciente_id": "invalid",
        "nombre": "",
        "edad": -1,
        "diagnostico": "D",
    }
