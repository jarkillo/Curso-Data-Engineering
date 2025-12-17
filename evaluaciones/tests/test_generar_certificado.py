"""Tests para el módulo generar_certificado."""

import tempfile
from pathlib import Path

import pytest

from evaluaciones.generar_certificado import (
    crear_certificado,
    generar_codigo_verificacion,
    verificar_certificado,
)


class TestGenerarCodigoVerificacion:
    """Tests para generar_codigo_verificacion."""

    def test_genera_codigo_12_caracteres(self):
        """El código tiene 12 caracteres."""
        codigo = generar_codigo_verificacion("Juan", "2025-01-01", 8.5)
        assert len(codigo) == 12

    def test_codigo_es_mayusculas(self):
        """El código está en mayúsculas."""
        codigo = generar_codigo_verificacion("Juan", "2025-01-01", 8.5)
        assert codigo == codigo.upper()

    def test_mismo_input_mismo_codigo(self):
        """El mismo input genera el mismo código."""
        codigo1 = generar_codigo_verificacion("Juan", "2025-01-01", 8.5)
        codigo2 = generar_codigo_verificacion("Juan", "2025-01-01", 8.5)
        assert codigo1 == codigo2

    def test_diferente_input_diferente_codigo(self):
        """Inputs diferentes generan códigos diferentes."""
        codigo1 = generar_codigo_verificacion("Juan", "2025-01-01", 8.5)
        codigo2 = generar_codigo_verificacion("Maria", "2025-01-01", 8.5)
        assert codigo1 != codigo2


class TestVerificarCertificado:
    """Tests para verificar_certificado."""

    def test_verificacion_correcta(self):
        """Verifica correctamente un certificado válido."""
        codigo = generar_codigo_verificacion("Juan García", "2025-01-15", 8.75)
        assert verificar_certificado(codigo, "Juan García", "2025-01-15", 8.75) is True

    def test_verificacion_incorrecta_nombre(self):
        """Detecta nombre incorrecto."""
        codigo = generar_codigo_verificacion("Juan García", "2025-01-15", 8.75)
        assert verificar_certificado(codigo, "Juan Perez", "2025-01-15", 8.75) is False

    def test_verificacion_incorrecta_fecha(self):
        """Detecta fecha incorrecta."""
        codigo = generar_codigo_verificacion("Juan García", "2025-01-15", 8.75)
        assert verificar_certificado(codigo, "Juan García", "2025-01-16", 8.75) is False

    def test_verificacion_incorrecta_nota(self):
        """Detecta nota incorrecta."""
        codigo = generar_codigo_verificacion("Juan García", "2025-01-15", 8.75)
        assert verificar_certificado(codigo, "Juan García", "2025-01-15", 9.0) is False


class TestCrearCertificado:
    """Tests para crear_certificado."""

    def test_nombre_vacio_raises_error(self):
        """Nombre vacío lanza ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            crear_certificado("", 8.5)

    def test_nombre_espacios_raises_error(self):
        """Nombre solo espacios lanza ValueError."""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            crear_certificado("   ", 8.5)

    def test_nota_invalida_raises_error(self):
        """Nota fuera de rango lanza ValueError."""
        with pytest.raises(ValueError, match="entre 0 y 10"):
            crear_certificado("Juan", 15.0)

    def test_nota_baja_raises_error(self):
        """Nota menor a 7.0 lanza ValueError."""
        with pytest.raises(ValueError, match="mínima de 7.0"):
            crear_certificado("Juan", 6.5)

    def test_crea_pdf_exitosamente(self):
        """Crea el archivo PDF correctamente."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ruta = crear_certificado(
                nombre_estudiante="Juan García Test",
                nota_media=8.5,
                fecha_completado="2025-01-15",
                directorio_salida=tmpdir,
            )

            assert Path(ruta).exists()
            assert ruta.endswith(".pdf")
            assert "juan_garcia_test" in ruta.lower()

    def test_crea_directorio_si_no_existe(self):
        """Crea el directorio de salida si no existe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = Path(tmpdir) / "nuevo" / "subdirectorio"

            ruta = crear_certificado(
                nombre_estudiante="Test User",
                nota_media=7.5,
                directorio_salida=str(subdir),
            )

            assert subdir.exists()
            assert Path(ruta).exists()

    def test_diferentes_calificaciones(self):
        """Genera certificados con diferentes calificaciones."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Notable (7.0-8.9)
            ruta1 = crear_certificado("Test1", 7.5, directorio_salida=tmpdir)
            assert Path(ruta1).exists()

            # Sobresaliente (9.0-9.4)
            ruta2 = crear_certificado("Test2", 9.2, directorio_salida=tmpdir)
            assert Path(ruta2).exists()

            # Matrícula de Honor (9.5+)
            ruta3 = crear_certificado("Test3", 9.8, directorio_salida=tmpdir)
            assert Path(ruta3).exists()
