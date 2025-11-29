"""
Tests para validar sintaxis de código Terraform.

Valida que todos los ambientes y módulos tengan sintaxis correcta.
"""

import subprocess
from pathlib import Path

import pytest


class TestTerraformValidate:
    """Tests para terraform validate"""

    def test_validate_dev_environment(self):
        """Debe validar ambiente dev sin errores"""
        env_path = Path(__file__).parent.parent / "terraform" / "environments" / "dev"

        # terraform init
        result_init = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=env_path,
            capture_output=True,
            text=True,
        )

        assert result_init.returncode == 0, f"Error en init: {result_init.stderr}"

        # terraform validate
        result_validate = subprocess.run(
            ["terraform", "validate"], cwd=env_path, capture_output=True, text=True
        )

        assert result_validate.returncode == 0, (
            f"Error en validate: {result_validate.stderr}"
        )
        assert "Success!" in result_validate.stdout

    def test_validate_staging_environment(self):
        """Debe validar ambiente staging sin errores"""
        env_path = (
            Path(__file__).parent.parent / "terraform" / "environments" / "staging"
        )

        # terraform init
        result_init = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=env_path,
            capture_output=True,
            text=True,
        )

        assert result_init.returncode == 0, f"Error en init: {result_init.stderr}"

        # terraform validate
        result_validate = subprocess.run(
            ["terraform", "validate"], cwd=env_path, capture_output=True, text=True
        )

        assert result_validate.returncode == 0, (
            f"Error en validate: {result_validate.stderr}"
        )
        assert "Success!" in result_validate.stdout

    def test_validate_prod_environment(self):
        """Debe validar ambiente prod sin errores"""
        env_path = Path(__file__).parent.parent / "terraform" / "environments" / "prod"

        # terraform init
        result_init = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=env_path,
            capture_output=True,
            text=True,
        )

        assert result_init.returncode == 0, f"Error en init: {result_init.stderr}"

        # terraform validate
        result_validate = subprocess.run(
            ["terraform", "validate"], cwd=env_path, capture_output=True, text=True
        )

        assert result_validate.returncode == 0, (
            f"Error en validate: {result_validate.stderr}"
        )
        assert "Success!" in result_validate.stdout

    def test_validate_data_lake_module(self):
        """Debe validar módulo data-lake sin errores"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "data-lake"
        )

        if not module_path.exists():
            pytest.skip("Módulo data-lake no existe aún")

        # terraform init
        result_init = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=module_path,
            capture_output=True,
            text=True,
        )

        assert result_init.returncode == 0, f"Error en init: {result_init.stderr}"

        # terraform validate
        result_validate = subprocess.run(
            ["terraform", "validate"], cwd=module_path, capture_output=True, text=True
        )

        assert result_validate.returncode == 0, (
            f"Error en validate: {result_validate.stderr}"
        )
        assert "Success!" in result_validate.stdout

    def test_validate_lambda_etl_module(self):
        """Debe validar módulo lambda-etl sin errores"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "lambda-etl"
        )

        if not module_path.exists():
            pytest.skip("Módulo lambda-etl no existe aún")

        # terraform init
        result_init = subprocess.run(
            ["terraform", "init", "-backend=false"],
            cwd=module_path,
            capture_output=True,
            text=True,
        )

        assert result_init.returncode == 0, f"Error en init: {result_init.stderr}"

        # terraform validate
        result_validate = subprocess.run(
            ["terraform", "validate"], cwd=module_path, capture_output=True, text=True
        )

        assert result_validate.returncode == 0, (
            f"Error en validate: {result_validate.stderr}"
        )
        assert "Success!" in result_validate.stdout


class TestTerraformVersions:
    """Tests para versiones de Terraform y providers"""

    def test_terraform_version_installed(self):
        """Debe tener Terraform instalado"""
        result = subprocess.run(
            ["terraform", "version"], capture_output=True, text=True
        )

        assert result.returncode == 0
        assert "Terraform" in result.stdout

    def test_terraform_version_minimum(self):
        """Debe tener versión mínima de Terraform (>= 1.0)"""
        result = subprocess.run(
            ["terraform", "version"], capture_output=True, text=True
        )

        # Extraer versión (ej: "Terraform v1.5.7")
        version_line = result.stdout.split("\n")[0]
        version = version_line.split("v")[1].split("-")[0]  # "1.5.7"

        major_version = int(version.split(".")[0])

        assert major_version >= 1, f"Versión muy antigua: {version}. Se requiere >= 1.0"
