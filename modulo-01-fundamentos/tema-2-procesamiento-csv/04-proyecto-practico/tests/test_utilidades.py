"""
Tests para el módulo de utilidades CSV.

Siguiendo TDD: Tests escritos PRIMERO, implementación después.
"""

import pytest

from src.utilidades import contar_filas, obtener_headers


class TestContarFilas:
    """Tests para la función contar_filas."""

    def test_con_archivo_con_datos(self, tmp_path):
        """Debe contar correctamente las filas de datos (sin header)."""
        # Arrange
        archivo = tmp_path / "datos.csv"
        archivo.write_text(
            "nombre,edad\n"
            "Ana,25\n"
            "Luis,30\n"
            "María,28\n",
            encoding="utf-8"
        )

        # Act
        resultado = contar_filas(str(archivo))

        # Assert
        assert resultado == 3

    def test_con_archivo_solo_header(self, tmp_path):
        """Con solo header, debe retornar 0."""
        # Arrange
        archivo = tmp_path / "solo_header.csv"
        archivo.write_text("nombre,edad\n", encoding="utf-8")

        # Act
        resultado = contar_filas(str(archivo))

        # Assert
        assert resultado == 0

    def test_con_archivo_vacio_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si el archivo está vacío."""
        # Arrange
        archivo = tmp_path / "vacio.csv"
        archivo.write_text("", encoding="utf-8")

        # Act & Assert
        with pytest.raises(ValueError, match="está vacío"):
            contar_filas(str(archivo))

    def test_con_archivo_inexistente_lanza_file_not_found_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="no existe"):
            contar_filas("archivo_inexistente.csv")


class TestObtenerHeaders:
    """Tests para la función obtener_headers."""

    def test_con_archivo_valido(self, tmp_path):
        """Debe retornar la lista de headers correctamente."""
        # Arrange
        archivo = tmp_path / "datos.csv"
        archivo.write_text(
            "nombre,edad,ciudad\n"
            "Ana,25,Madrid\n",
            encoding="utf-8"
        )

        # Act
        resultado = obtener_headers(str(archivo))

        # Assert
        assert resultado == ["nombre", "edad", "ciudad"]

    def test_con_headers_vacios(self, tmp_path):
        """Con headers vacíos, debe retornar lista vacía."""
        # Arrange
        archivo = tmp_path / "sin_headers.csv"
        archivo.write_text("\n", encoding="utf-8")

        # Act
        resultado = obtener_headers(str(archivo))

        # Assert
        assert resultado == []

    def test_con_archivo_vacio_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si el archivo está vacío."""
        # Arrange
        archivo = tmp_path / "vacio.csv"
        archivo.write_text("", encoding="utf-8")

        # Act & Assert
        with pytest.raises(ValueError, match="está vacío"):
            obtener_headers(str(archivo))

    def test_con_archivo_inexistente_lanza_file_not_found_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="no existe"):
            obtener_headers("archivo_inexistente.csv")

    def test_con_delimitador_punto_y_coma(self, tmp_path):
        """Debe funcionar con delimitador punto y coma."""
        # Arrange
        archivo = tmp_path / "europeo.csv"
        archivo.write_text(
            "nombre;edad;ciudad\n"
            "Ana;25;Madrid\n",
            encoding="utf-8"
        )

        # Act
        resultado = obtener_headers(str(archivo), delimitador=";")

        # Assert
        assert resultado == ["nombre", "edad", "ciudad"]
