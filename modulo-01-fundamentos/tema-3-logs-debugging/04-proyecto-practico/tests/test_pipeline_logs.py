"""
Tests para las funciones de pipeline con logging integrado.

Siguiendo TDD: Tests escritos PRIMERO, implementación DESPUÉS.
"""

import csv
import logging
import pytest
from src.pipeline_logs import procesar_con_logs, validar_datos_con_logs


class TestProcesarConLogs:
    """Tests para la función procesar_con_logs."""

    def test_procesar_con_logs_con_archivo_csv_valido(self, tmp_path, caplog):
        """Debe procesar archivo CSV válido y loggear cada paso."""
        # Crear archivo CSV de prueba
        archivo_csv = tmp_path / "ventas.csv"
        with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["id", "producto", "precio", "cantidad"]
            )
            writer.writeheader()
            writer.writerow(
                {"id": "1", "producto": "Laptop", "precio": "1000", "cantidad": "2"}
            )
            writer.writerow(
                {"id": "2", "producto": "Mouse", "precio": "25", "cantidad": "5"}
            )
            writer.writerow(
                {"id": "3", "producto": "Teclado", "precio": "75", "cantidad": "3"}
            )

        # Procesar con logs
        with caplog.at_level(logging.INFO):
            resultado = procesar_con_logs(str(archivo_csv))

        # Verificar resultado
        assert resultado is not None
        assert "total_registros" in resultado
        assert resultado["total_registros"] == 3
        assert "registros_procesados" in resultado
        assert resultado["registros_procesados"] == 3

        # Verificar que se loggearon los pasos
        assert any(
            "Iniciando procesamiento" in record.message for record in caplog.records
        )
        assert any("Leyendo archivo CSV" in record.message for record in caplog.records)
        assert any(
            "Procesados 3 registros" in record.message for record in caplog.records
        )
        assert any(
            "Procesamiento completado exitosamente" in record.message
            for record in caplog.records
        )

    def test_procesar_con_logs_con_archivo_vacio(self, tmp_path, caplog):
        """Debe manejar archivo CSV vacío y loggear advertencia."""
        archivo_csv = tmp_path / "vacio.csv"
        with open(archivo_csv, "w", encoding="utf-8") as f:
            f.write("id,producto,precio,cantidad\n")  # Solo headers

        with caplog.at_level(logging.WARNING):
            resultado = procesar_con_logs(str(archivo_csv))

        assert resultado["total_registros"] == 0
        assert any("WARNING" in record.levelname for record in caplog.records)
        assert any("vacío" in record.message.lower() for record in caplog.records)

    def test_procesar_con_logs_con_archivo_inexistente(self, caplog):
        """Debe loggear error si el archivo no existe."""
        with caplog.at_level(logging.ERROR):
            with pytest.raises(FileNotFoundError):
                procesar_con_logs("archivo_inexistente.csv")

        assert any("ERROR" in record.levelname for record in caplog.records)
        assert any(
            "no encontrado" in record.message.lower()
            or "no existe" in record.message.lower()
            for record in caplog.records
        )

    def test_procesar_con_logs_con_datos_invalidos(self, tmp_path, caplog):
        """Debe loggear errores de validación de datos."""
        archivo_csv = tmp_path / "invalidos.csv"
        with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["id", "producto", "precio", "cantidad"]
            )
            writer.writeheader()
            writer.writerow(
                {"id": "1", "producto": "Laptop", "precio": "INVALIDO", "cantidad": "2"}
            )
            writer.writerow(
                {"id": "2", "producto": "Mouse", "precio": "25", "cantidad": "5"}
            )

        with caplog.at_level(logging.WARNING):
            procesar_con_logs(str(archivo_csv))

        # Debe procesar lo que pueda y loggear advertencias
        assert any(
            "WARNING" in record.levelname or "ERROR" in record.levelname
            for record in caplog.records
        )

    def test_procesar_con_logs_con_ruta_none_lanza_type_error(self):
        """Debe lanzar TypeError si la ruta es None."""
        with pytest.raises(TypeError):
            procesar_con_logs(None)

    def test_procesar_con_logs_con_ruta_vacia_lanza_value_error(self):
        """Debe lanzar ValueError si la ruta está vacía."""
        with pytest.raises(
            ValueError, match="La ruta del archivo no puede estar vacía"
        ):
            procesar_con_logs("")

    def test_procesar_con_logs_retorna_estadisticas_completas(self, tmp_path):
        """Debe retornar estadísticas completas del procesamiento."""
        archivo_csv = tmp_path / "stats.csv"
        with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["id", "producto", "precio", "cantidad"]
            )
            writer.writeheader()
            writer.writerow(
                {"id": "1", "producto": "A", "precio": "100", "cantidad": "1"}
            )
            writer.writerow(
                {"id": "2", "producto": "B", "precio": "200", "cantidad": "2"}
            )

        resultado = procesar_con_logs(str(archivo_csv))

        # Verificar estructura del resultado
        assert "total_registros" in resultado
        assert "registros_procesados" in resultado
        assert "registros_con_error" in resultado
        assert "tiempo_procesamiento" in resultado
        assert isinstance(resultado["tiempo_procesamiento"], float)

    def test_procesar_con_logs_con_logger_personalizado(self, tmp_path):
        """Debe permitir usar un logger personalizado."""
        archivo_csv = tmp_path / "custom.csv"
        with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, fieldnames=["id", "producto", "precio", "cantidad"]
            )
            writer.writeheader()
            writer.writerow(
                {"id": "1", "producto": "Test", "precio": "50", "cantidad": "1"}
            )

        # Crear logger personalizado
        logger_custom = logging.getLogger("mi_logger_custom")
        logger_custom.setLevel(logging.DEBUG)

        resultado = procesar_con_logs(str(archivo_csv), logger=logger_custom)

        assert resultado is not None
        assert resultado["total_registros"] == 1


class TestValidarDatosConLogs:
    """Tests para la función validar_datos_con_logs."""

    def test_validar_datos_con_logs_con_datos_validos(self, caplog):
        """Debe validar datos correctos sin errores."""
        datos = [
            {"id": "1", "nombre": "Juan", "edad": "25", "email": "juan@example.com"},
            {"id": "2", "nombre": "María", "edad": "30", "email": "maria@example.com"},
        ]

        with caplog.at_level(logging.INFO):
            resultado = validar_datos_con_logs(datos)

        assert resultado["validos"] == 2
        assert resultado["invalidos"] == 0
        assert len(resultado["errores"]) == 0
        assert any(
            "Validación completada" in record.message for record in caplog.records
        )

    def test_validar_datos_con_logs_con_datos_invalidos(self, caplog):
        """Debe detectar y loggear datos inválidos."""
        datos = [
            {"id": "1", "nombre": "Juan", "edad": "25", "email": "juan@example.com"},
            {
                "id": "2",
                "nombre": "",
                "edad": "30",
                "email": "invalido",
            },  # Nombre vacío, email inválido
            {
                "id": "3",
                "nombre": "Pedro",
                "edad": "-5",
                "email": "pedro@example.com",
            },  # Edad negativa
        ]

        with caplog.at_level(logging.WARNING):
            resultado = validar_datos_con_logs(datos)

        assert resultado["validos"] < len(datos)
        assert resultado["invalidos"] > 0
        assert len(resultado["errores"]) > 0
        assert any("WARNING" in record.levelname for record in caplog.records)

    def test_validar_datos_con_logs_con_lista_vacia(self, caplog):
        """Debe manejar lista vacía correctamente."""
        with caplog.at_level(logging.WARNING):
            resultado = validar_datos_con_logs([])

        assert resultado["validos"] == 0
        assert resultado["invalidos"] == 0
        assert any("vacía" in record.message.lower() for record in caplog.records)

    def test_validar_datos_con_logs_con_none_lanza_type_error(self):
        """Debe lanzar TypeError si los datos son None."""
        with pytest.raises(TypeError):
            validar_datos_con_logs(None)

    def test_validar_datos_con_logs_con_tipo_incorrecto_lanza_type_error(self):
        """Debe lanzar TypeError si los datos no son lista."""
        with pytest.raises(TypeError, match="Los datos deben ser una lista"):
            validar_datos_con_logs("no es una lista")

    def test_validar_datos_con_logs_con_campos_requeridos(self, caplog):
        """Debe validar campos requeridos."""
        datos = [
            {"id": "1", "nombre": "Juan"},  # Falta 'edad'
            {"id": "2", "nombre": "María", "edad": "30"},
        ]

        campos_requeridos = ["id", "nombre", "edad"]

        with caplog.at_level(logging.WARNING):
            resultado = validar_datos_con_logs(
                datos, campos_requeridos=campos_requeridos
            )

        assert resultado["invalidos"] > 0
        assert any(
            "campo requerido" in error.lower() or "falta" in error.lower()
            for error in resultado["errores"]
        )

    def test_validar_datos_con_logs_retorna_estructura_completa(self):
        """Debe retornar estructura completa con estadísticas."""
        datos = [
            {"id": "1", "nombre": "Test", "edad": "25", "email": "test@example.com"},
        ]

        resultado = validar_datos_con_logs(datos)

        # Verificar estructura
        assert "validos" in resultado
        assert "invalidos" in resultado
        assert "total" in resultado
        assert "errores" in resultado
        assert "porcentaje_validos" in resultado
        assert isinstance(resultado["validos"], int)
        assert isinstance(resultado["invalidos"], int)
        assert isinstance(resultado["total"], int)
        assert isinstance(resultado["errores"], list)
        assert isinstance(resultado["porcentaje_validos"], float)

    def test_validar_datos_con_logs_con_validador_personalizado(self, caplog):
        """Debe permitir usar función de validación personalizada."""
        datos = [
            {"id": "1", "valor": "100"},
            {"id": "2", "valor": "50"},
            {"id": "3", "valor": "200"},
        ]

        def validador_custom(registro):
            """Valida que el valor sea menor a 150."""
            return int(registro.get("valor", 0)) < 150

        with caplog.at_level(logging.INFO):
            resultado = validar_datos_con_logs(
                datos, validador_personalizado=validador_custom
            )

        # Solo 2 registros deben ser válidos (100 y 50)
        assert resultado["validos"] == 2
        assert resultado["invalidos"] == 1

    def test_validar_datos_con_logs_con_logger_personalizado(self):
        """Debe permitir usar un logger personalizado."""
        datos = [
            {"id": "1", "nombre": "Test", "edad": "25"},
        ]

        logger_custom = logging.getLogger("validador_custom")
        logger_custom.setLevel(logging.DEBUG)

        resultado = validar_datos_con_logs(datos, logger=logger_custom)

        assert resultado is not None
        assert resultado["validos"] == 1

    def test_validar_datos_con_logs_calcula_porcentaje_correctamente(self):
        """Debe calcular el porcentaje de válidos correctamente."""
        datos = [
            {"id": "1", "nombre": "A", "edad": "25", "email": "a@example.com"},
            {"id": "2", "nombre": "B", "edad": "30", "email": "b@example.com"},
            {
                "id": "3",
                "nombre": "",
                "edad": "35",
                "email": "c@example.com",
            },  # Inválido
            {"id": "4", "nombre": "D", "edad": "40", "email": "d@example.com"},
        ]

        resultado = validar_datos_con_logs(datos)

        # 3 de 4 válidos = 75%
        assert resultado["total"] == 4
        assert resultado["porcentaje_validos"] == pytest.approx(75.0, rel=0.1)
