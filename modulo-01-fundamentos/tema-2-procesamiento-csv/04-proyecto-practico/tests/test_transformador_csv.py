"""
Tests para el módulo de transformación de archivos CSV.

Siguiendo TDD: Tests escritos PRIMERO, implementación después.
"""

import pytest

from src.transformador_csv import agregar_columna, consolidar_csvs, filtrar_filas


class TestFiltrarFilas:
    """Tests para la función filtrar_filas."""

    def test_con_condicion_simple_filtra_correctamente(self):
        """Debe filtrar filas según la condición."""
        # Arrange
        datos = [
            {"nombre": "Ana", "edad": "25", "ciudad": "Madrid"},
            {"nombre": "Luis", "edad": "30", "ciudad": "Barcelona"},
            {"nombre": "María", "edad": "28", "ciudad": "Madrid"}
        ]

        # Act
        resultado = filtrar_filas(datos, lambda fila: fila["ciudad"] == "Madrid")

        # Assert
        assert len(resultado) == 2
        assert resultado[0]["nombre"] == "Ana"
        assert resultado[1]["nombre"] == "María"

    def test_con_condicion_numerica(self):
        """Debe filtrar con condiciones numéricas."""
        # Arrange
        datos = [
            {"producto": "A", "precio": "10.50"},
            {"producto": "B", "precio": "25.00"},
            {"producto": "C", "precio": "15.75"}
        ]

        # Act
        resultado = filtrar_filas(
            datos,
            lambda fila: float(fila["precio"]) > 15.0
        )

        # Assert
        assert len(resultado) == 2
        assert resultado[0]["producto"] == "B"
        assert resultado[1]["producto"] == "C"

    def test_con_lista_vacia_retorna_lista_vacia(self):
        """Con lista vacía, debe retornar lista vacía."""
        # Arrange
        datos = []

        # Act
        resultado = filtrar_filas(datos, lambda fila: True)

        # Assert
        assert resultado == []

    def test_con_condicion_que_no_cumple_nadie_retorna_vacia(self):
        """Si ninguna fila cumple la condición, retorna lista vacía."""
        # Arrange
        datos = [
            {"nombre": "Ana", "edad": "25"},
            {"nombre": "Luis", "edad": "30"}
        ]

        # Act
        resultado = filtrar_filas(datos, lambda fila: fila["nombre"] == "Pedro")

        # Assert
        assert resultado == []


class TestAgregarColumna:
    """Tests para la función agregar_columna."""

    def test_con_funcion_simple_agrega_columna(self):
        """Debe agregar una nueva columna calculada."""
        # Arrange
        datos = [
            {"nombre": "Ana", "edad": "25"},
            {"nombre": "Luis", "edad": "30"}
        ]

        # Act
        resultado = agregar_columna(
            datos,
            "mayor_edad",
            lambda fila: "Sí" if int(fila["edad"]) >= 18 else "No"
        )

        # Assert
        assert len(resultado) == 2
        assert resultado[0]["mayor_edad"] == "Sí"
        assert resultado[1]["mayor_edad"] == "Sí"
        # Verificar que las columnas originales siguen ahí
        assert resultado[0]["nombre"] == "Ana"

    def test_con_calculo_numerico(self):
        """Debe agregar columna con cálculo numérico."""
        # Arrange
        datos = [
            {"producto": "A", "precio": "10.00", "cantidad": "2"},
            {"producto": "B", "precio": "15.50", "cantidad": "3"}
        ]

        # Act
        resultado = agregar_columna(
            datos,
            "total",
            lambda fila: str(float(fila["precio"]) * int(fila["cantidad"]))
        )

        # Assert
        assert resultado[0]["total"] == "20.0"
        assert resultado[1]["total"] == "46.5"

    def test_con_lista_vacia_retorna_lista_vacia(self):
        """Con lista vacía, debe retornar lista vacía."""
        # Arrange
        datos = []

        # Act
        resultado = agregar_columna(datos, "nueva", lambda fila: "valor")

        # Assert
        assert resultado == []

    def test_no_modifica_lista_original(self):
        """No debe modificar la lista original (función pura)."""
        # Arrange
        datos = [{"nombre": "Ana", "edad": "25"}]

        # Act
        resultado = agregar_columna(datos, "nueva", lambda fila: "valor")

        # Assert
        assert "nueva" not in datos[0]
        assert "nueva" in resultado[0]


class TestConsolidarCsvs:
    """Tests para la función consolidar_csvs."""

    def test_con_dos_archivos_consolida_correctamente(self, tmp_path):
        """Debe consolidar múltiples archivos CSV."""
        # Arrange
        archivo1 = tmp_path / "a.csv"
        archivo1.write_text(
            "nombre,edad\n"
            "Ana,25\n"
            "Luis,30\n",
            encoding="utf-8"
        )

        archivo2 = tmp_path / "b.csv"
        archivo2.write_text(
            "nombre,edad\n"
            "María,28\n"
            "Pedro,35\n",
            encoding="utf-8"
        )

        archivos = [str(archivo1), str(archivo2)]
        archivo_salida = tmp_path / "consolidado.csv"

        # Act
        consolidar_csvs(archivos, str(archivo_salida))

        # Assert
        assert archivo_salida.exists()

        # Verificar contenido
        with open(archivo_salida, "r", encoding="utf-8") as f:
            contenido = f.read()
            assert "Ana" in contenido
            assert "Luis" in contenido
            assert "María" in contenido
            assert "Pedro" in contenido

    def test_con_archivos_diferentes_headers_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si los headers no coinciden."""
        # Arrange
        archivo1 = tmp_path / "a.csv"
        archivo1.write_text(
            "nombre,edad\n"
            "Ana,25\n",
            encoding="utf-8"
        )

        archivo2 = tmp_path / "b.csv"
        archivo2.write_text(
            "name,age\n"
            "Luis,30\n",
            encoding="utf-8"
        )

        archivos = [str(archivo1), str(archivo2)]
        archivo_salida = tmp_path / "consolidado.csv"

        # Act & Assert
        with pytest.raises(ValueError, match="headers diferentes"):
            consolidar_csvs(archivos, str(archivo_salida))

    def test_con_lista_vacia_lanza_value_error(self, tmp_path):
        """Debe lanzar ValueError si la lista de archivos está vacía."""
        # Arrange
        archivos = []
        archivo_salida = tmp_path / "consolidado.csv"

        # Act & Assert
        with pytest.raises(ValueError, match="al menos un archivo"):
            consolidar_csvs(archivos, str(archivo_salida))

    def test_con_archivo_inexistente_lanza_file_not_found_error(self, tmp_path):
        """Debe lanzar FileNotFoundError si algún archivo no existe."""
        # Arrange
        archivos = ["inexistente1.csv", "inexistente2.csv"]
        archivo_salida = tmp_path / "consolidado.csv"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            consolidar_csvs(archivos, str(archivo_salida))
