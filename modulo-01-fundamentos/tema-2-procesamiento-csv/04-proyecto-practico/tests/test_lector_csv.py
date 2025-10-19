"""
Tests para el módulo de lectura de archivos CSV.

Siguiendo TDD: Tests escritos PRIMERO, implementación después.
"""

import pytest

from src.lector_csv import (
    detectar_delimitador,
    leer_csv,
    validar_archivo_existe,
)


class TestValidarArchivoExiste:
    """Tests para la función validar_archivo_existe."""

    def test_con_archivo_existente_no_lanza_error(self, tmp_path):
        """No debe lanzar error si el archivo existe."""
        # Arrange
        archivo = tmp_path / "existe.csv"
        archivo.write_text("datos", encoding="utf-8")

        # Act & Assert (no debe lanzar excepción)
        validar_archivo_existe(str(archivo))

    def test_con_archivo_inexistente_lanza_file_not_found_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="no existe"):
            validar_archivo_existe("inexistente.csv")

    def test_con_archivo_vacio_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si el archivo está vacío."""
        # Arrange
        archivo = tmp_path / "vacio.csv"
        archivo.write_text("", encoding="utf-8")

        # Act & Assert
        with pytest.raises(ValueError, match="está vacío"):
            validar_archivo_existe(str(archivo))


class TestDetectarDelimitador:
    """Tests para la función detectar_delimitador."""

    def test_con_delimitador_coma(self, tmp_path):
        """Debe detectar correctamente el delimitador coma."""
        # Arrange
        archivo = tmp_path / "coma.csv"
        archivo.write_text(
            "nombre,edad,ciudad\n"
            "Ana,25,Madrid\n",
            encoding="utf-8"
        )

        # Act
        resultado = detectar_delimitador(str(archivo))

        # Assert
        assert resultado == ","

    def test_con_delimitador_punto_y_coma(self, tmp_path):
        """Debe detectar correctamente el delimitador punto y coma."""
        # Arrange
        archivo = tmp_path / "punto_coma.csv"
        archivo.write_text(
            "nombre;edad;ciudad\n"
            "Ana;25;Madrid\n",
            encoding="utf-8"
        )

        # Act
        resultado = detectar_delimitador(str(archivo))

        # Assert
        assert resultado == ";"

    def test_con_delimitador_tabulador(self, tmp_path):
        """Debe detectar correctamente el delimitador tabulador."""
        # Arrange
        archivo = tmp_path / "tab.csv"
        archivo.write_text(
            "nombre\tedad\tciudad\n"
            "Ana\t25\tMadrid\n",
            encoding="utf-8"
        )

        # Act
        resultado = detectar_delimitador(str(archivo))

        # Assert
        assert resultado == "\t"

    def test_con_archivo_inexistente_lanza_file_not_found_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="no existe"):
            detectar_delimitador("inexistente.csv")


class TestLeerCsv:
    """Tests para la función leer_csv."""

    def test_con_archivo_valido_retorna_lista_de_diccionarios(self, tmp_path):
        """Debe retornar una lista de diccionarios con los datos."""
        # Arrange
        archivo = tmp_path / "datos.csv"
        archivo.write_text(
            "nombre,edad,ciudad\n"
            "Ana,25,Madrid\n"
            "Luis,30,Barcelona\n",
            encoding="utf-8"
        )

        # Act
        resultado = leer_csv(str(archivo))

        # Assert
        assert len(resultado) == 2
        assert resultado[0] == {"nombre": "Ana", "edad": "25", "ciudad": "Madrid"}
        assert resultado[1] == {"nombre": "Luis", "edad": "30", "ciudad": "Barcelona"}

    def test_con_archivo_solo_header_retorna_lista_vacia(self, tmp_path):
        """Con solo header, debe retornar lista vacía."""
        # Arrange
        archivo = tmp_path / "solo_header.csv"
        archivo.write_text("nombre,edad,ciudad\n", encoding="utf-8")

        # Act
        resultado = leer_csv(str(archivo))

        # Assert
        assert resultado == []

    def test_con_delimitador_especificado(self, tmp_path):
        """Debe usar el delimitador especificado."""
        # Arrange
        archivo = tmp_path / "europeo.csv"
        archivo.write_text(
            "nombre;edad;ciudad\n"
            "Ana;25;Madrid\n",
            encoding="utf-8"
        )

        # Act
        resultado = leer_csv(str(archivo), delimitador=";")

        # Assert
        assert len(resultado) == 1
        assert resultado[0] == {"nombre": "Ana", "edad": "25", "ciudad": "Madrid"}

    def test_con_encoding_especificado(self, tmp_path):
        """Debe usar el encoding especificado."""
        # Arrange
        archivo = tmp_path / "utf8.csv"
        archivo.write_text(
            "nombre,ciudad\n"
            "José,Málaga\n",
            encoding="utf-8"
        )

        # Act
        resultado = leer_csv(str(archivo), encoding="utf-8")

        # Assert
        assert resultado[0]["nombre"] == "José"
        assert resultado[0]["ciudad"] == "Málaga"

    def test_con_archivo_inexistente_lanza_file_not_found_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="no existe"):
            leer_csv("inexistente.csv")

    def test_con_archivo_vacio_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si el archivo está vacío."""
        # Arrange
        archivo = tmp_path / "vacio.csv"
        archivo.write_text("", encoding="utf-8")

        # Act & Assert
        with pytest.raises(ValueError, match="está vacío"):
            leer_csv(str(archivo))
