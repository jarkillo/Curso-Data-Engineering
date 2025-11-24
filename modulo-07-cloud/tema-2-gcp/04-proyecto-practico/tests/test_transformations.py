"""
Tests para el módulo transformations.py

Tests exhaustivos para transformaciones ETL de registros de pacientes.
"""

from datetime import datetime

import pytest

from src.transformations import (
    calcular_edad_desde_fecha_nacimiento,
    categorizar_nivel_riesgo,
    categorizar_por_edad,
    enriquecer_registro,
    limpiar_nulls,
    normalizar_fechas,
)


class TestLimpiarNulls:
    """Tests para limpiar_nulls()"""

    def test_mantener_registros_completos(self):
        """Debe mantener registros sin nulls"""
        datos = [
            {
                "paciente_id": "P001",
                "nombre": "Juan Pérez",
                "edad": 45,
                "diagnostico": "Diabetes",
            },
            {
                "paciente_id": "P002",
                "nombre": "María García",
                "edad": 32,
                "diagnostico": "Hipertensión",
            },
        ]

        resultado = limpiar_nulls(datos)

        assert len(resultado) == 2
        assert resultado[0]["paciente_id"] == "P001"
        assert resultado[1]["paciente_id"] == "P002"

    def test_eliminar_registros_con_nulls_en_campos_criticos(self):
        """Debe eliminar registros con nulls en campos críticos"""
        datos = [
            {
                "paciente_id": "P001",
                "nombre": "Juan Pérez",
                "edad": 45,
                "diagnostico": "Diabetes",
            },
            {
                "paciente_id": None,  # Null en campo crítico
                "nombre": "María García",
                "edad": 32,
                "diagnostico": "Hipertensión",
            },
            {
                "paciente_id": "P003",
                "nombre": None,  # Null en campo crítico
                "edad": 50,
                "diagnostico": "Colesterol",
            },
        ]

        resultado = limpiar_nulls(datos)

        assert len(resultado) == 1
        assert resultado[0]["paciente_id"] == "P001"

    def test_lista_vacia(self):
        """Debe manejar lista vacía"""
        resultado = limpiar_nulls([])
        assert resultado == []

    def test_no_modifica_original(self):
        """No debe modificar la lista original"""
        datos = [
            {
                "paciente_id": "P001",
                "nombre": "Juan",
                "edad": 45,
                "diagnostico": "Diabetes",
            }
        ]
        original_len = len(datos)

        limpiar_nulls(datos)

        assert len(datos) == original_len


class TestNormalizarFechas:
    """Tests para normalizar_fechas()"""

    def test_normalizar_fecha_formato_estandar(self):
        """Debe normalizar fechas al formato YYYY-MM-DD"""
        datos = [
            {"paciente_id": "P001", "fecha_registro": "15/01/2025"},
            {"paciente_id": "P002", "fecha_registro": "2025-01-20"},
        ]

        resultado = normalizar_fechas(datos)

        # Debe convertir al formato ISO
        assert "-" in resultado[0]["fecha_registro"]
        assert len(resultado[0]["fecha_registro"]) == 10  # YYYY-MM-DD

    def test_mantener_fechas_ya_normalizadas(self):
        """Debe mantener fechas ya en formato correcto"""
        datos = [{"paciente_id": "P001", "fecha_registro": "2025-01-15"}]

        resultado = normalizar_fechas(datos)

        assert resultado[0]["fecha_registro"] == "2025-01-15"

    def test_manejar_registros_sin_fecha(self):
        """Debe manejar registros sin campo fecha"""
        datos = [{"paciente_id": "P001", "nombre": "Juan"}]

        resultado = normalizar_fechas(datos)

        assert len(resultado) == 1
        assert "fecha_registro" not in resultado[0]


class TestCalcularEdadDesdeFechaNacimiento:
    """Tests para calcular_edad_desde_fecha_nacimiento()"""

    def test_calcular_edad_correcta(self):
        """Debe calcular edad correctamente"""
        # Fecha hace 45 años
        fecha_hace_45_anos = (
            datetime.now().replace(year=datetime.now().year - 45).strftime("%Y-%m-%d")
        )

        edad = calcular_edad_desde_fecha_nacimiento(fecha_hace_45_anos)

        assert edad == 45

    def test_calcular_edad_recien_nacido(self):
        """Debe calcular edad 0 para recién nacidos"""
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")

        edad = calcular_edad_desde_fecha_nacimiento(fecha_hoy)

        assert edad == 0

    def test_calcular_edad_persona_mayor(self):
        """Debe calcular edad para personas mayores (80+)"""
        fecha_hace_85_anos = (
            datetime.now().replace(year=datetime.now().year - 85).strftime("%Y-%m-%d")
        )

        edad = calcular_edad_desde_fecha_nacimiento(fecha_hace_85_anos)

        assert edad == 85

    def test_manejar_fecha_invalida(self):
        """Debe manejar fechas inválidas retornando None"""
        edad = calcular_edad_desde_fecha_nacimiento("fecha-invalida")

        assert edad is None


class TestCategorizarPorEdad:
    """Tests para categorizar_por_edad()"""

    def test_categorizar_nino(self):
        """Debe categorizar menores de 18 como 'niño'"""
        assert categorizar_por_edad(5) == "niño"
        assert categorizar_por_edad(17) == "niño"

    def test_categorizar_adulto(self):
        """Debe categorizar 18-64 como 'adulto'"""
        assert categorizar_por_edad(18) == "adulto"
        assert categorizar_por_edad(45) == "adulto"
        assert categorizar_por_edad(64) == "adulto"

    def test_categorizar_mayor(self):
        """Debe categorizar 65+ como 'mayor'"""
        assert categorizar_por_edad(65) == "mayor"
        assert categorizar_por_edad(80) == "mayor"

    def test_categorizar_edad_cero(self):
        """Debe categorizar edad 0 como 'niño'"""
        assert categorizar_por_edad(0) == "niño"


class TestCategorizarNivelRiesgo:
    """Tests para categorizar_nivel_riesgo()"""

    def test_riesgo_bajo_joven_sin_condiciones(self):
        """Debe categorizar riesgo bajo para jóvenes sin condiciones"""
        registro = {
            "edad": 25,
            "diagnostico": "Chequeo general",
        }

        riesgo = categorizar_nivel_riesgo(registro)

        assert riesgo == "bajo"

    def test_riesgo_medio_adulto_diabetes(self):
        """Debe categorizar riesgo medio para adultos con diabetes"""
        registro = {
            "edad": 45,
            "diagnostico": "Diabetes",
        }

        riesgo = categorizar_nivel_riesgo(registro)

        assert riesgo == "medio"

    def test_riesgo_alto_mayor_hipertension(self):
        """Debe categorizar riesgo alto para mayores con hipertensión"""
        registro = {
            "edad": 70,
            "diagnostico": "Hipertensión",
        }

        riesgo = categorizar_nivel_riesgo(registro)

        assert riesgo == "alto"

    def test_riesgo_alto_mayor_diabetes(self):
        """Debe categorizar riesgo alto para mayores con diabetes"""
        registro = {
            "edad": 68,
            "diagnostico": "Diabetes Tipo 2",
        }

        riesgo = categorizar_nivel_riesgo(registro)

        assert riesgo == "alto"

    def test_riesgo_bajo_adulto_sin_condiciones_criticas(self):
        """Debe categorizar riesgo bajo para adultos sin condiciones críticas"""
        registro = {
            "edad": 50,
            "diagnostico": "Colesterol Alto",
        }

        riesgo = categorizar_nivel_riesgo(registro)

        assert riesgo == "bajo"


class TestEnriquecerRegistro:
    """Tests para enriquecer_registro()"""

    def test_agregar_campos_calculados(self):
        """Debe agregar campos calculados al registro"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
            "fecha_nacimiento": "1980-01-15",
        }

        enriquecido = enriquecer_registro(registro)

        # Debe tener campos adicionales
        assert "categoria_edad" in enriquecido
        assert "nivel_riesgo" in enriquecido
        assert "fecha_procesamiento" in enriquecido

    def test_categoria_edad_correcta(self):
        """Debe calcular categoría de edad correctamente"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 70,
            "diagnostico": "Hipertensión",
        }

        enriquecido = enriquecer_registro(registro)

        assert enriquecido["categoria_edad"] == "mayor"

    def test_nivel_riesgo_correcto(self):
        """Debe calcular nivel de riesgo correctamente"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 68,
            "diagnostico": "Diabetes",
        }

        enriquecido = enriquecer_registro(registro)

        assert enriquecido["nivel_riesgo"] == "alto"

    def test_agregar_timestamp_procesamiento(self):
        """Debe agregar timestamp de procesamiento"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
        }

        enriquecido = enriquecer_registro(registro)

        assert "fecha_procesamiento" in enriquecido
        # Debe ser un timestamp válido (formato ISO)
        assert "T" in enriquecido["fecha_procesamiento"]

    def test_no_modificar_registro_original(self):
        """No debe modificar el registro original"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
        }

        enriquecido = enriquecer_registro(registro)

        assert "categoria_edad" not in registro  # Original no modificado
        assert "categoria_edad" in enriquecido  # Enriquecido sí tiene el campo

    def test_mantener_campos_originales(self):
        """Debe mantener todos los campos originales"""
        registro = {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
            "hospital": "Hospital Central",
        }

        enriquecido = enriquecer_registro(registro)

        assert enriquecido["paciente_id"] == "P001"
        assert enriquecido["nombre"] == "Juan Pérez"
        assert enriquecido["edad"] == 45
        assert enriquecido["diagnostico"] == "Diabetes"
        assert enriquecido["hospital"] == "Hospital Central"


# Fixtures
@pytest.fixture
def registros_sample():
    """Fixture con registros de ejemplo"""
    return [
        {
            "paciente_id": "P001",
            "nombre": "Juan Pérez",
            "edad": 45,
            "diagnostico": "Diabetes",
            "fecha_registro": "2025-01-15",
        },
        {
            "paciente_id": "P002",
            "nombre": "María García",
            "edad": 32,
            "diagnostico": "Hipertensión",
            "fecha_registro": "2025-01-16",
        },
        {
            "paciente_id": "P003",
            "nombre": "Carlos López",
            "edad": 68,
            "diagnostico": "Diabetes Tipo 2",
            "fecha_registro": "2025-01-17",
        },
    ]
