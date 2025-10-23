"""
Tests para el módulo de validaciones.

Estos tests validan las funciones de validación de inputs
siguiendo metodología TDD (Test-Driven Development).
"""

import os
import tempfile

import pytest


class TestValidarPrecioPositivo:
    """Tests para validar_precio_positivo."""

    def test_con_precio_positivo_valido(self):
        """Debe pasar sin errores con precio positivo."""
        from src.validaciones import validar_precio_positivo

        # No debe lanzar excepción
        validar_precio_positivo(100.0)
        validar_precio_positivo(0.01)
        validar_precio_positivo(999999.99)

    def test_con_precio_cero_lanza_value_error(self):
        """Debe lanzar ValueError si precio es cero."""
        from src.validaciones import validar_precio_positivo

        with pytest.raises(ValueError, match="debe ser mayor a cero"):
            validar_precio_positivo(0.0)

    def test_con_precio_negativo_lanza_value_error(self):
        """Debe lanzar ValueError si precio es negativo."""
        from src.validaciones import validar_precio_positivo

        with pytest.raises(ValueError, match="debe ser mayor a cero"):
            validar_precio_positivo(-10.5)

    def test_con_string_lanza_type_error(self):
        """Debe lanzar TypeError si precio no es numérico."""
        from src.validaciones import validar_precio_positivo

        with pytest.raises(TypeError, match="debe ser un número"):
            validar_precio_positivo("100")

    def test_con_none_lanza_type_error(self):
        """Debe lanzar TypeError si precio es None."""
        from src.validaciones import validar_precio_positivo

        with pytest.raises(TypeError, match="debe ser un número"):
            validar_precio_positivo(None)


class TestValidarCategoriaNoVacia:
    """Tests para validar_categoria_no_vacia."""

    def test_con_categoria_valida(self):
        """Debe pasar sin errores con categoría válida."""
        from src.validaciones import validar_categoria_no_vacia

        validar_categoria_no_vacia("Accesorios")
        validar_categoria_no_vacia("Computadoras")
        validar_categoria_no_vacia("A")  # Un solo carácter es válido

    def test_con_categoria_vacia_lanza_value_error(self):
        """Debe lanzar ValueError si categoría está vacía."""
        from src.validaciones import validar_categoria_no_vacia

        with pytest.raises(ValueError, match="no puede estar vacía"):
            validar_categoria_no_vacia("")

    def test_con_categoria_solo_espacios_lanza_value_error(self):
        """Debe lanzar ValueError si categoría es solo espacios."""
        from src.validaciones import validar_categoria_no_vacia

        with pytest.raises(ValueError, match="no puede estar vacía"):
            validar_categoria_no_vacia("   ")

    def test_con_numero_lanza_type_error(self):
        """Debe lanzar TypeError si categoría no es string."""
        from src.validaciones import validar_categoria_no_vacia

        with pytest.raises(TypeError, match="debe ser un string"):
            validar_categoria_no_vacia(123)

    def test_con_none_lanza_type_error(self):
        """Debe lanzar TypeError si categoría es None."""
        from src.validaciones import validar_categoria_no_vacia

        with pytest.raises(TypeError, match="debe ser un string"):
            validar_categoria_no_vacia(None)


class TestValidarNumeroPositivo:
    """Tests para validar_numero_positivo."""

    def test_con_numero_positivo_valido(self):
        """Debe pasar sin errores con número positivo."""
        from src.validaciones import validar_numero_positivo

        validar_numero_positivo(1, "n")
        validar_numero_positivo(100, "limite")
        validar_numero_positivo(999999, "cantidad")

    def test_con_numero_cero_lanza_value_error(self):
        """Debe lanzar ValueError si número es cero."""
        from src.validaciones import validar_numero_positivo

        with pytest.raises(ValueError, match="debe ser mayor a cero"):
            validar_numero_positivo(0, "n")

    def test_con_numero_negativo_lanza_value_error(self):
        """Debe lanzar ValueError si número es negativo."""
        from src.validaciones import validar_numero_positivo

        with pytest.raises(ValueError, match="debe ser mayor a cero"):
            validar_numero_positivo(-5, "cantidad")

    def test_con_float_lanza_type_error(self):
        """Debe lanzar TypeError si número es float."""
        from src.validaciones import validar_numero_positivo

        with pytest.raises(TypeError, match="debe ser un entero"):
            validar_numero_positivo(5.5, "n")

    def test_con_string_lanza_type_error(self):
        """Debe lanzar TypeError si número es string."""
        from src.validaciones import validar_numero_positivo

        with pytest.raises(TypeError, match="debe ser un entero"):
            validar_numero_positivo("5", "n")

    def test_mensaje_error_incluye_nombre_parametro(self):
        """El mensaje de error debe incluir el nombre del parámetro."""
        from src.validaciones import validar_numero_positivo

        with pytest.raises(ValueError, match="limite"):
            validar_numero_positivo(0, "limite")


class TestValidarRutaDbExiste:
    """Tests para validar_ruta_db_existe."""

    def test_con_ruta_existente(self):
        """Debe pasar sin errores si el archivo existe."""
        from src.validaciones import validar_ruta_db_existe

        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            ruta_temp = tmp.name

        try:
            validar_ruta_db_existe(ruta_temp)
        finally:
            os.unlink(ruta_temp)

    def test_con_ruta_no_existente_lanza_file_not_found_error(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        from src.validaciones import validar_ruta_db_existe

        with pytest.raises(FileNotFoundError, match="no existe"):
            validar_ruta_db_existe("/ruta/inexistente/base.db")

    def test_con_ruta_vacia_lanza_value_error(self):
        """Debe lanzar ValueError si la ruta está vacía."""
        from src.validaciones import validar_ruta_db_existe

        with pytest.raises(ValueError, match="no puede estar vacía"):
            validar_ruta_db_existe("")

    def test_con_ruta_none_lanza_type_error(self):
        """Debe lanzar TypeError si la ruta es None."""
        from src.validaciones import validar_ruta_db_existe

        with pytest.raises(TypeError, match="debe ser un string"):
            validar_ruta_db_existe(None)
