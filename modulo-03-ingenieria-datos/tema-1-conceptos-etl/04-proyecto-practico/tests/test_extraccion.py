"""Tests para el módulo de extracción de datos."""

import pytest

from src.extraccion import extraer_clientes, extraer_productos, extraer_ventas, leer_csv


class TestLeerCsv:
    """Tests para la función leer_csv."""

    def test_leer_csv_con_archivo_valido(self, tmp_path):
        """Debe leer correctamente un archivo CSV válido."""
        # Arrange
        archivo = tmp_path / "test.csv"
        archivo.write_text(
            "id,nombre,valor\n1,Producto A,100\n2,Producto B,200", encoding="utf-8"
        )

        # Act
        resultado = leer_csv(str(archivo))

        # Assert
        assert len(resultado) == 2
        assert resultado[0] == {"id": "1", "nombre": "Producto A", "valor": "100"}
        assert resultado[1] == {"id": "2", "nombre": "Producto B", "valor": "200"}

    def test_leer_csv_con_archivo_vacio_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si el archivo solo tiene header."""
        # Arrange
        archivo = tmp_path / "vacio.csv"
        archivo.write_text("id,nombre,valor\n", encoding="utf-8")

        # Act & Assert
        with pytest.raises(ValueError, match="está vacío"):
            leer_csv(str(archivo))

    def test_leer_csv_con_archivo_inexistente_lanza_file_not_found(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            leer_csv("archivo_que_no_existe.csv")

    def test_leer_csv_con_none_lanza_type_error(self):
        """Debe lanzar TypeError si se pasa None."""
        with pytest.raises(TypeError):
            leer_csv(None)


class TestExtraerVentas:
    """Tests para la función extraer_ventas."""

    def test_extraer_ventas_con_datos_validos(self, tmp_path):
        """Debe extraer ventas y convertir tipos de datos."""
        # Arrange
        archivo = tmp_path / "ventas.csv"
        archivo.write_text(
            "venta_id,fecha,producto_id,cliente_id,cantidad,precio_unitario\n"
            "1,2025-10-01,101,1001,2,899.99\n"
            "2,2025-10-01,102,1002,5,29.99\n",
            encoding="utf-8",
        )

        # Act
        resultado = extraer_ventas(str(archivo))

        # Assert
        assert len(resultado) == 2
        assert resultado[0]["venta_id"] == 1
        assert resultado[0]["producto_id"] == 101
        assert resultado[0]["cliente_id"] == 1001
        assert resultado[0]["cantidad"] == 2
        assert resultado[0]["precio_unitario"] == 899.99
        assert resultado[0]["fecha"] == "2025-10-01"

    def test_extraer_ventas_con_archivo_inexistente_lanza_file_not_found(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            extraer_ventas("ventas_inexistentes.csv")

    def test_extraer_ventas_con_columnas_faltantes_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si faltan columnas requeridas."""
        # Arrange
        archivo = tmp_path / "ventas_invalidas.csv"
        archivo.write_text("venta_id,fecha\n1,2025-10-01\n", encoding="utf-8")

        # Act & Assert
        with pytest.raises(ValueError, match="columnas requeridas"):
            extraer_ventas(str(archivo))


class TestExtraerProductos:
    """Tests para la función extraer_productos."""

    def test_extraer_productos_con_datos_validos(self, tmp_path):
        """Debe extraer productos y convertir tipos de datos."""
        # Arrange
        archivo = tmp_path / "productos.csv"
        archivo.write_text(
            "producto_id,nombre,categoria,stock\n"
            "101,Laptop Dell,Computadoras,50\n"
            "102,Mouse Logitech,Accesorios,200\n",
            encoding="utf-8",
        )

        # Act
        resultado = extraer_productos(str(archivo))

        # Assert
        assert len(resultado) == 2
        assert resultado[0]["producto_id"] == 101
        assert resultado[0]["nombre"] == "Laptop Dell"
        assert resultado[0]["categoria"] == "Computadoras"
        assert resultado[0]["stock"] == 50

    def test_extraer_productos_con_archivo_inexistente_lanza_file_not_found(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            extraer_productos("productos_inexistentes.csv")


class TestExtraerClientes:
    """Tests para la función extraer_clientes."""

    def test_extraer_clientes_con_datos_validos(self, tmp_path):
        """Debe extraer clientes correctamente."""
        # Arrange
        archivo = tmp_path / "clientes.csv"
        archivo.write_text(
            "cliente_id,nombre,email,ciudad\n"
            "1001,Juan Perez,juan@example.com,Madrid\n"
            "1002,Maria Garcia,maria@example.com,Barcelona\n",
            encoding="utf-8",
        )

        # Act
        resultado = extraer_clientes(str(archivo))

        # Assert
        assert len(resultado) == 2
        assert resultado[0]["cliente_id"] == 1001
        assert resultado[0]["nombre"] == "Juan Perez"
        assert resultado[0]["email"] == "juan@example.com"
        assert resultado[0]["ciudad"] == "Madrid"

    def test_extraer_clientes_con_archivo_inexistente_lanza_file_not_found(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            extraer_clientes("clientes_inexistentes.csv")
