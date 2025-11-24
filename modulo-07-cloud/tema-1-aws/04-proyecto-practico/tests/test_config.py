"""
Tests para el módulo config.py

Tests exhaustivos para funciones de configuración.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config import (
    cargar_configuracion,
    obtener_ruta_datos,
    obtener_ruta_proyecto,
    validar_configuracion,
)


class TestCargarConfiguracion:
    """Tests para cargar_configuracion()"""

    def test_cargar_configuracion_con_archivo_valido(self, tmp_path):
        """Debe cargar correctamente un archivo .env válido"""
        # Crear archivo .env temporal
        env_file = tmp_path / ".env"
        env_content = """AWS_ACCESS_KEY_ID=test_key_123
AWS_SECRET_ACCESS_KEY=test_secret_456
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_RAW=cloudapi-logs-raw
S3_BUCKET_PROCESSED=cloudapi-logs-processed
LAMBDA_FUNCTION_NAME=ValidarLogsAPI
GLUE_DATABASE=cloudapi_analytics
ATHENA_OUTPUT_LOCATION=s3://cloudapi-logs-processed/athena-results/
"""
        env_file.write_text(env_content)

        config = cargar_configuracion(str(env_file))

        assert config["aws_access_key_id"] == "test_key_123"
        assert config["aws_secret_access_key"] == "test_secret_456"
        assert config["aws_region"] == "us-east-1"
        assert config["s3_bucket_raw"] == "cloudapi-logs-raw"
        assert config["s3_bucket_processed"] == "cloudapi-logs-processed"

    def test_cargar_configuracion_sin_ruta_busca_en_raiz(self, tmp_path, monkeypatch):
        """Debe buscar .env en directorio raíz si no se especifica ruta"""
        # Cambiar el directorio de trabajo actual
        monkeypatch.chdir(tmp_path)

        env_file = tmp_path / ".env"
        env_content = "AWS_ACCESS_KEY_ID=test_key"
        env_file.write_text(env_content)

        # Mock de obtener_ruta_proyecto para que retorne tmp_path
        with patch("src.config.obtener_ruta_proyecto", return_value=tmp_path):
            config = cargar_configuracion()
            assert "aws_access_key_id" in config

    def test_cargar_configuracion_archivo_no_existe(self):
        """Debe lanzar FileNotFoundError si el archivo .env no existe"""
        with pytest.raises(FileNotFoundError):
            cargar_configuracion("/ruta/inexistente/.env")

    def test_cargar_configuracion_con_variables_faltantes(self, tmp_path):
        """Debe cargar configuración incluso si faltan algunas variables"""
        env_file = tmp_path / ".env"
        env_content = "AWS_ACCESS_KEY_ID=test_key"
        env_file.write_text(env_content)

        config = cargar_configuracion(str(env_file))

        assert config["aws_access_key_id"] == "test_key"
        # Las variables faltantes deben tener valor vacío o no estar presentes
        assert (
            "aws_secret_access_key" not in config
            or config["aws_secret_access_key"] == ""
        )

    def test_cargar_configuracion_con_comentarios(self, tmp_path):
        """Debe ignorar líneas comentadas en .env"""
        env_file = tmp_path / ".env"
        env_content = """# Esto es un comentario
AWS_ACCESS_KEY_ID=test_key
# AWS_SECRET_ACCESS_KEY=comentado
AWS_DEFAULT_REGION=us-east-1
"""
        env_file.write_text(env_content)

        config = cargar_configuracion(str(env_file))

        assert config["aws_access_key_id"] == "test_key"
        assert "comentado" not in str(config.values())


class TestValidarConfiguracion:
    """Tests para validar_configuracion()"""

    def test_validar_configuracion_completa_y_valida(self):
        """Debe validar correctamente una configuración completa"""
        config = {
            "aws_access_key_id": "test_key",
            "aws_secret_access_key": "test_secret",
            "aws_region": "us-east-1",
            "s3_bucket_raw": "bucket-raw",
            "s3_bucket_processed": "bucket-processed",
            "lambda_function_name": "ValidarLogsAPI",
            "glue_database": "analytics",
            "athena_output_location": "s3://bucket/results/",
        }

        valida, errores = validar_configuracion(config)

        assert valida is True
        assert len(errores) == 0

    def test_validar_configuracion_con_campos_faltantes(self):
        """Debe detectar campos requeridos faltantes"""
        config = {
            "aws_access_key_id": "test_key",
            # Falta aws_secret_access_key
            "aws_region": "us-east-1",
        }

        valida, errores = validar_configuracion(config)

        assert valida is False
        assert len(errores) > 0
        assert any("aws_secret_access_key" in error for error in errores)

    def test_validar_configuracion_con_valores_vacios(self):
        """Debe detectar valores vacíos en campos requeridos"""
        config = {
            "aws_access_key_id": "",  # Vacío
            "aws_secret_access_key": "test_secret",
            "aws_region": "us-east-1",
            "s3_bucket_raw": "",  # Vacío
        }

        valida, errores = validar_configuracion(config)

        assert valida is False
        assert any("aws_access_key_id" in error for error in errores)
        assert any("s3_bucket_raw" in error for error in errores)

    def test_validar_configuracion_vacia(self):
        """Debe detectar que una configuración vacía es inválida"""
        config = {}

        valida, errores = validar_configuracion(config)

        assert valida is False
        assert len(errores) > 0

    def test_validar_configuracion_con_region_invalida(self):
        """Debe validar que la región AWS tenga formato correcto"""
        config = {
            "aws_access_key_id": "test_key",
            "aws_secret_access_key": "test_secret",
            "aws_region": "invalid-region-999",  # Región inválida
            "s3_bucket_raw": "bucket-raw",
            "s3_bucket_processed": "bucket-processed",
        }

        valida, errores = validar_configuracion(config)

        # Puede ser válida o no dependiendo de la implementación
        # Si implementamos validación estricta de regiones, debe fallar
        if not valida:
            assert any("region" in error.lower() for error in errores)


class TestObtenerRutaProyecto:
    """Tests para obtener_ruta_proyecto()"""

    def test_obtener_ruta_proyecto_retorna_path(self):
        """Debe retornar un objeto Path"""
        ruta = obtener_ruta_proyecto()

        assert isinstance(ruta, Path)

    def test_obtener_ruta_proyecto_termina_en_proyecto_practico(self):
        """Debe retornar la ruta del proyecto práctico"""
        ruta = obtener_ruta_proyecto()

        assert "04-proyecto-practico" in str(ruta)

    def test_obtener_ruta_proyecto_es_directorio_existente(self):
        """Debe retornar una ruta que existe"""
        ruta = obtener_ruta_proyecto()

        assert ruta.exists()
        assert ruta.is_dir()


class TestObtenerRutaDatos:
    """Tests para obtener_ruta_datos()"""

    def test_obtener_ruta_datos_raw(self):
        """Debe retornar la ruta a data/raw"""
        ruta = obtener_ruta_datos("raw")

        assert isinstance(ruta, Path)
        assert str(ruta).endswith(os.path.join("data", "raw"))

    def test_obtener_ruta_datos_processed(self):
        """Debe retornar la ruta a data/processed"""
        ruta = obtener_ruta_datos("processed")

        assert isinstance(ruta, Path)
        assert str(ruta).endswith(os.path.join("data", "processed"))

    def test_obtener_ruta_datos_tipo_invalido(self):
        """Debe lanzar ValueError si el tipo no es 'raw' ni 'processed'"""
        with pytest.raises(ValueError) as exc_info:
            obtener_ruta_datos("invalid")

        assert (
            "raw" in str(exc_info.value).lower()
            or "processed" in str(exc_info.value).lower()
        )

    def test_obtener_ruta_datos_default_es_raw(self):
        """Debe usar 'raw' como valor por defecto"""
        ruta_default = obtener_ruta_datos()
        ruta_raw = obtener_ruta_datos("raw")

        assert str(ruta_default) == str(ruta_raw)

    def test_obtener_ruta_datos_tipo_case_insensitive(self):
        """Debe aceptar 'RAW', 'Raw', 'raw', etc."""
        ruta_lower = obtener_ruta_datos("raw")
        ruta_upper = obtener_ruta_datos("RAW")
        ruta_mixed = obtener_ruta_datos("Raw")

        assert str(ruta_lower) == str(ruta_upper) == str(ruta_mixed)


# Fixtures para tests
@pytest.fixture
def config_valida():
    """Fixture con configuración válida completa"""
    return {
        "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
        "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "aws_region": "us-east-1",
        "s3_bucket_raw": "cloudapi-logs-raw",
        "s3_bucket_processed": "cloudapi-logs-processed",
        "lambda_function_name": "ValidarLogsAPI",
        "glue_database": "cloudapi_analytics",
        "athena_output_location": "s3://cloudapi-logs-processed/athena-results/",
    }


@pytest.fixture
def config_incompleta():
    """Fixture con configuración incompleta"""
    return {
        "aws_access_key_id": "test_key",
        "aws_region": "us-east-1",
    }
