"""Tests para el módulo tracking_progreso."""

import tempfile
from pathlib import Path

import pytest

from evaluaciones.tracking_progreso import (
    calcular_nivel,
    calcular_nota_media,
    cargar_progreso,
    guardar_progreso,
    puede_obtener_certificado,
    registrar_examen,
)


class TestCalcularNivel:
    """Tests para calcular_nivel."""

    def test_nivel_1_sin_xp(self):
        """Nivel 1 con 0 XP."""
        assert calcular_nivel(0) == 1

    def test_nivel_1_con_poco_xp(self):
        """Nivel 1 con XP bajo el umbral."""
        assert calcular_nivel(50) == 1

    def test_nivel_2(self):
        """Nivel 2 con XP suficiente."""
        assert calcular_nivel(100) == 2
        assert calcular_nivel(200) == 2

    def test_nivel_10_maximo(self):
        """Nivel máximo con mucho XP."""
        assert calcular_nivel(5000) == 10
        assert calcular_nivel(10000) == 10


class TestCargarGuardarProgreso:
    """Tests para cargar y guardar progreso."""

    def test_cargar_nuevo_estudiante(self):
        """Cargar crea datos nuevos si no existe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            datos = cargar_progreso("Test User", Path(tmpdir))
            assert datos["nombre"] == "Test User"
            assert datos["xp_total"] == 0
            assert datos["nivel"] == 1
            assert datos["examenes"] == {}

    def test_guardar_y_cargar(self):
        """Guardar y cargar preserva datos."""
        with tempfile.TemporaryDirectory() as tmpdir:
            datos_original = {
                "nombre": "Test User",
                "fecha_inicio": "2025-01-01",
                "examenes": {},
                "xp_total": 500,
                "nivel": 3,
                "logros": ["test_logro"],
            }

            ruta = guardar_progreso(datos_original, Path(tmpdir))
            assert Path(ruta).exists()

            datos_cargado = cargar_progreso("Test User", Path(tmpdir))
            assert datos_cargado["xp_total"] == 500
            assert datos_cargado["nivel"] == 3


class TestRegistrarExamen:
    """Tests para registrar_examen."""

    def test_examen_aprobado(self):
        """Registrar examen aprobado actualiza XP."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {},
            "xp_total": 0,
            "nivel": 1,
            "logros": [],
        }

        datos, logros = registrar_examen(datos, 1, 80)

        assert datos["examenes"]["1"]["aprobado"] is True
        assert datos["examenes"]["1"]["puntuacion"] == 80
        assert datos["xp_total"] == 100  # XP básico

    def test_examen_con_excelencia(self):
        """Examen con nota >= 90 da XP bonus."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {},
            "xp_total": 0,
            "nivel": 1,
            "logros": [],
        }

        datos, logros = registrar_examen(datos, 1, 95)

        assert datos["xp_total"] == 150  # 100 base + 50 bonus
        assert "excelencia_m1" in datos["logros"]

    def test_examen_no_aprobado(self):
        """Examen no aprobado no da XP."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {},
            "xp_total": 0,
            "nivel": 1,
            "logros": [],
        }

        datos, logros = registrar_examen(datos, 1, 50)

        assert datos["examenes"]["1"]["aprobado"] is False
        assert datos["xp_total"] == 0

    def test_modulo_invalido_raises_error(self):
        """Módulo fuera de rango lanza error."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {},
            "xp_total": 0,
            "nivel": 1,
            "logros": [],
        }

        with pytest.raises(ValueError, match="Módulo inválido"):
            registrar_examen(datos, 15, 80)

    def test_puntuacion_invalida_raises_error(self):
        """Puntuación fuera de rango lanza error."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {},
            "xp_total": 0,
            "nivel": 1,
            "logros": [],
        }

        with pytest.raises(ValueError, match="Puntuación inválida"):
            registrar_examen(datos, 1, 150)

    def test_contador_intentos(self):
        """Los intentos se incrementan correctamente."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {},
            "xp_total": 0,
            "nivel": 1,
            "logros": [],
        }

        datos, _ = registrar_examen(datos, 1, 50)
        assert datos["examenes"]["1"]["intentos"] == 1

        datos, _ = registrar_examen(datos, 1, 60)
        assert datos["examenes"]["1"]["intentos"] == 2


class TestCalcularNotaMedia:
    """Tests para calcular_nota_media."""

    def test_sin_examenes(self):
        """Sin exámenes retorna 0."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {},
            "xp_total": 0,
            "nivel": 1,
            "logros": [],
        }

        assert calcular_nota_media(datos) == 0.0

    def test_con_examenes_aprobados(self):
        """Calcula media de exámenes aprobados."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {
                "1": {
                    "modulo": 1,
                    "puntuacion": 80,
                    "aprobado": True,
                    "intentos": 1,
                    "fecha": "",
                },
                "2": {
                    "modulo": 2,
                    "puntuacion": 90,
                    "aprobado": True,
                    "intentos": 1,
                    "fecha": "",
                },
            },
            "xp_total": 200,
            "nivel": 2,
            "logros": [],
        }

        # (80 + 90) / 2 / 10 = 8.5
        assert calcular_nota_media(datos) == 8.5

    def test_ignora_no_aprobados(self):
        """Ignora exámenes no aprobados en la media."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {
                "1": {
                    "modulo": 1,
                    "puntuacion": 80,
                    "aprobado": True,
                    "intentos": 1,
                    "fecha": "",
                },
                "2": {
                    "modulo": 2,
                    "puntuacion": 50,
                    "aprobado": False,
                    "intentos": 1,
                    "fecha": "",
                },
            },
            "xp_total": 100,
            "nivel": 1,
            "logros": [],
        }

        # Solo cuenta el 80
        assert calcular_nota_media(datos) == 8.0


class TestPuedeObtenerCertificado:
    """Tests para puede_obtener_certificado."""

    def test_no_puede_sin_todos_modulos(self):
        """No puede obtener certificado sin completar todos los módulos."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {
                "1": {
                    "modulo": 1,
                    "puntuacion": 80,
                    "aprobado": True,
                    "intentos": 1,
                    "fecha": "",
                },
            },
            "xp_total": 100,
            "nivel": 1,
            "logros": [],
        }

        puede, mensaje = puede_obtener_certificado(datos)
        assert puede is False
        assert "Faltan 9 módulos" in mensaje

    def test_puede_con_todos_aprobados(self):
        """Puede obtener certificado con todos aprobados."""
        datos = {
            "nombre": "Test",
            "fecha_inicio": "2025-01-01",
            "examenes": {
                str(i): {
                    "modulo": i,
                    "puntuacion": 80,
                    "aprobado": True,
                    "intentos": 1,
                    "fecha": "",
                }
                for i in range(1, 11)
            },
            "xp_total": 1000,
            "nivel": 5,
            "logros": ["programa_completo"],
        }

        puede, mensaje = puede_obtener_certificado(datos)
        assert puede is True
        assert "Felicidades" in mensaje
