"""
Tests para el módulo de validación de archivos CSV.

Siguiendo TDD: Tests escritos PRIMERO, implementación después.
"""

import pytest

from src.validador_csv import validar_fila, validar_headers, validar_tipo_dato


class TestValidarHeaders:
    """Tests para la función validar_headers."""

    def test_con_headers_correctos_retorna_true(self, tmp_path):
        """Debe retornar True si los headers coinciden."""
        # Arrange
        archivo = tmp_path / "datos.csv"
        archivo.write_text(
            "nombre,edad,ciudad\n"
            "Ana,25,Madrid\n",
            encoding="utf-8"
        )
        headers_esperados = ["nombre", "edad", "ciudad"]

        # Act
        resultado = validar_headers(str(archivo), headers_esperados)

        # Assert
        assert resultado is True

    def test_con_headers_incorrectos_retorna_false(self, tmp_path):
        """Debe retornar False si los headers no coinciden."""
        # Arrange
        archivo = tmp_path / "datos.csv"
        archivo.write_text(
            "name,age,city\n"
            "Ana,25,Madrid\n",
            encoding="utf-8"
        )
        headers_esperados = ["nombre", "edad", "ciudad"]

        # Act
        resultado = validar_headers(str(archivo), headers_esperados)

        # Assert
        assert resultado is False

    def test_con_headers_en_diferente_orden_retorna_false(self, tmp_path):
        """Debe retornar False si el orden de headers es diferente."""
        # Arrange
        archivo = tmp_path / "datos.csv"
        archivo.write_text(
            "edad,nombre,ciudad\n"
            "25,Ana,Madrid\n",
            encoding="utf-8"
        )
        headers_esperados = ["nombre", "edad", "ciudad"]

        # Act
        resultado = validar_headers(str(archivo), headers_esperados)

        # Assert
        assert resultado is False

    def test_con_archivo_inexistente_lanza_file_not_found_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        # Act & Assert
        with pytest.raises(FileNotFoundError, match="no existe"):
            validar_headers("inexistente.csv", ["nombre"])


class TestValidarTipoDato:
    """Tests para la función validar_tipo_dato."""

    def test_con_entero_valido_retorna_true(self):
        """Debe retornar True si el valor es un entero válido."""
        # Act & Assert
        assert validar_tipo_dato("25", int) is True
        assert validar_tipo_dato("0", int) is True
        assert validar_tipo_dato("-10", int) is True

    def test_con_entero_invalido_retorna_false(self):
        """Debe retornar False si el valor no es un entero."""
        # Act & Assert
        assert validar_tipo_dato("25.5", int) is False
        assert validar_tipo_dato("abc", int) is False
        assert validar_tipo_dato("", int) is False

    def test_con_float_valido_retorna_true(self):
        """Debe retornar True si el valor es un float válido."""
        # Act & Assert
        assert validar_tipo_dato("25.5", float) is True
        assert validar_tipo_dato("25", float) is True
        assert validar_tipo_dato("-10.3", float) is True

    def test_con_float_invalido_retorna_false(self):
        """Debe retornar False si el valor no es un float."""
        # Act & Assert
        assert validar_tipo_dato("abc", float) is False
        assert validar_tipo_dato("", float) is False

    def test_con_string_siempre_retorna_true(self):
        """Con tipo str, siempre debe retornar True."""
        # Act & Assert
        assert validar_tipo_dato("cualquier cosa", str) is True
        assert validar_tipo_dato("", str) is True
        assert validar_tipo_dato("123", str) is True


class TestValidarFila:
    """Tests para la función validar_fila."""

    def test_con_fila_valida_retorna_lista_vacia(self):
        """Con fila válida, debe retornar lista vacía de errores."""
        # Arrange
        fila = {"nombre": "Ana", "edad": "25", "ciudad": "Madrid"}
        validaciones = {
            "nombre": str,
            "edad": int,
            "ciudad": str
        }

        # Act
        errores = validar_fila(fila, validaciones)

        # Assert
        assert errores == []

    def test_con_tipo_incorrecto_retorna_error(self):
        """Con tipo incorrecto, debe retornar error."""
        # Arrange
        fila = {"nombre": "Ana", "edad": "abc", "ciudad": "Madrid"}
        validaciones = {
            "nombre": str,
            "edad": int,
            "ciudad": str
        }

        # Act
        errores = validar_fila(fila, validaciones)

        # Assert
        assert len(errores) == 1
        assert "edad" in errores[0]
        assert "tipo inválido" in errores[0]

    def test_con_valor_vacio_retorna_error(self):
        """Con valor vacío, debe retornar error."""
        # Arrange
        fila = {"nombre": "", "edad": "25", "ciudad": "Madrid"}
        validaciones = {
            "nombre": str,
            "edad": int,
            "ciudad": str
        }

        # Act
        errores = validar_fila(fila, validaciones)

        # Assert
        assert len(errores) == 1
        assert "nombre" in errores[0]
        assert "vacío" in errores[0]

    def test_con_columna_faltante_retorna_error(self):
        """Con columna faltante, debe retornar error."""
        # Arrange
        fila = {"nombre": "Ana", "edad": "25"}  # Falta 'ciudad'
        validaciones = {
            "nombre": str,
            "edad": int,
            "ciudad": str
        }

        # Act
        errores = validar_fila(fila, validaciones)

        # Assert
        assert len(errores) == 1
        assert "ciudad" in errores[0]
        assert "falta" in errores[0]

    def test_con_multiples_errores_retorna_todos(self):
        """Con múltiples errores, debe retornarlos todos."""
        # Arrange
        fila = {"nombre": "", "edad": "abc", "ciudad": "Madrid"}
        validaciones = {
            "nombre": str,
            "edad": int,
            "ciudad": str
        }

        # Act
        errores = validar_fila(fila, validaciones)

        # Assert
        assert len(errores) == 2
