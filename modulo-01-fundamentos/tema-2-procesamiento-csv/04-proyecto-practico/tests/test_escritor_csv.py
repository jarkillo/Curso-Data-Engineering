"""
Tests para el módulo de escritura de archivos CSV.

Siguiendo TDD: Tests escritos PRIMERO, implementación después.
"""

import csv

import pytest

from src.escritor_csv import escribir_csv


class TestEscribirCsv:
    """Tests para la función escribir_csv."""

    def test_con_lista_de_diccionarios_crea_archivo(self, tmp_path):
        """Debe crear un archivo CSV con los datos correctos."""
        # Arrange
        datos = [
            {"nombre": "Ana", "edad": "25", "ciudad": "Madrid"},
            {"nombre": "Luis", "edad": "30", "ciudad": "Barcelona"}
        ]
        archivo_salida = tmp_path / "salida.csv"

        # Act
        escribir_csv(datos, str(archivo_salida))

        # Assert
        assert archivo_salida.exists()

        # Verificar contenido
        with open(archivo_salida, "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            filas = list(lector)
            assert len(filas) == 2
            assert filas[0]["nombre"] == "Ana"
            assert filas[1]["nombre"] == "Luis"

    def test_con_lista_vacia_crea_archivo_solo_con_headers(self, tmp_path):
        """Con lista vacía, debe crear archivo solo con headers."""
        # Arrange
        datos = []
        headers = ["nombre", "edad", "ciudad"]
        archivo_salida = tmp_path / "vacio.csv"

        # Act
        escribir_csv(datos, str(archivo_salida), headers=headers)

        # Assert
        assert archivo_salida.exists()

        # Verificar contenido
        with open(archivo_salida, "r", encoding="utf-8") as f:
            contenido = f.read()
            assert "nombre,edad,ciudad" in contenido

    def test_con_delimitador_especificado(self, tmp_path):
        """Debe usar el delimitador especificado."""
        # Arrange
        datos = [{"nombre": "Ana", "edad": "25"}]
        archivo_salida = tmp_path / "europeo.csv"

        # Act
        escribir_csv(datos, str(archivo_salida), delimitador=";")

        # Assert
        with open(archivo_salida, "r", encoding="utf-8") as f:
            contenido = f.read()
            assert ";" in contenido
            assert "nombre;edad" in contenido

    def test_con_encoding_especificado(self, tmp_path):
        """Debe usar el encoding especificado."""
        # Arrange
        datos = [{"nombre": "José", "ciudad": "Málaga"}]
        archivo_salida = tmp_path / "utf8.csv"

        # Act
        escribir_csv(datos, str(archivo_salida), encoding="utf-8")

        # Assert
        with open(archivo_salida, "r", encoding="utf-8") as f:
            contenido = f.read()
            assert "José" in contenido
            assert "Málaga" in contenido

    def test_con_datos_vacios_y_sin_headers_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si datos vacíos y no se especifican headers."""
        # Arrange
        datos = []
        archivo_salida = tmp_path / "error.csv"

        # Act & Assert
        with pytest.raises(ValueError, match="headers"):
            escribir_csv(datos, str(archivo_salida))

    def test_sobrescribe_archivo_existente(self, tmp_path):
        """Debe sobrescribir el archivo si ya existe."""
        # Arrange
        archivo_salida = tmp_path / "existente.csv"
        archivo_salida.write_text("contenido viejo", encoding="utf-8")

        datos = [{"nombre": "Ana"}]

        # Act
        escribir_csv(datos, str(archivo_salida))

        # Assert
        with open(archivo_salida, "r", encoding="utf-8") as f:
            contenido = f.read()
            assert "contenido viejo" not in contenido
            assert "Ana" in contenido
