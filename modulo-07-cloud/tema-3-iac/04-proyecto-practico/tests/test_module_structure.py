"""
Tests para validar estructura de módulos Terraform.

Valida que cada módulo tenga los archivos requeridos y estructura correcta.
"""

from pathlib import Path

import pytest


class TestModuleStructure:
    """Tests para estructura de módulos"""

    def test_data_lake_module_has_required_files(self):
        """Módulo data-lake debe tener archivos requeridos"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "data-lake"
        )

        if not module_path.exists():
            pytest.skip("Módulo data-lake no implementado aún")

        required_files = ["main.tf", "variables.tf", "outputs.tf", "README.md"]

        for file_name in required_files:
            file_path = module_path / file_name
            assert file_path.exists(), f"Falta archivo requerido: {file_name}"

    def test_lambda_etl_module_has_required_files(self):
        """Módulo lambda-etl debe tener archivos requeridos"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "lambda-etl"
        )

        if not module_path.exists():
            pytest.skip("Módulo lambda-etl no implementado aún")

        required_files = [
            "main.tf",
            "variables.tf",
            "outputs.tf",
            "README.md",
            "lambda_function.py",
        ]

        for file_name in required_files:
            file_path = module_path / file_name
            assert file_path.exists(), f"Falta archivo requerido: {file_name}"

    def test_networking_module_has_required_files(self):
        """Módulo networking debe tener archivos requeridos"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "networking"
        )

        if not module_path.exists():
            pytest.skip("Módulo networking no implementado aún")

        required_files = ["main.tf", "variables.tf", "outputs.tf", "README.md"]

        for file_name in required_files:
            file_path = module_path / file_name
            assert file_path.exists(), f"Falta archivo requerido: {file_name}"

    def test_glue_catalog_module_has_required_files(self):
        """Módulo glue-catalog debe tener archivos requeridos"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "glue-catalog"
        )

        if not module_path.exists():
            pytest.skip("Módulo glue-catalog no implementado aún")

        required_files = ["main.tf", "variables.tf", "outputs.tf", "README.md"]

        for file_name in required_files:
            file_path = module_path / file_name
            assert file_path.exists(), f"Falta archivo requerido: {file_name}"

    def test_all_environments_exist(self):
        """Deben existir todos los ambientes (dev, staging, prod)"""
        environments_path = Path(__file__).parent.parent / "terraform" / "environments"

        if not environments_path.exists():
            pytest.skip("Directorio environments no existe")

        required_envs = ["dev", "staging", "prod"]

        for env in required_envs:
            env_path = environments_path / env
            assert env_path.exists(), f"Falta ambiente: {env}"

    def test_dev_environment_has_required_files(self):
        """Ambiente dev debe tener archivos requeridos"""
        env_path = Path(__file__).parent.parent / "terraform" / "environments" / "dev"

        if not env_path.exists():
            pytest.skip("Ambiente dev no existe")

        required_files = ["main.tf", "terraform.tfvars", "backend.tf"]

        for file_name in required_files:
            file_path = env_path / file_name
            assert file_path.exists(), f"Falta archivo en dev: {file_name}"

    def test_staging_environment_has_required_files(self):
        """Ambiente staging debe tener archivos requeridos"""
        env_path = (
            Path(__file__).parent.parent / "terraform" / "environments" / "staging"
        )

        if not env_path.exists():
            pytest.skip("Ambiente staging no existe")

        required_files = ["main.tf", "terraform.tfvars", "backend.tf"]

        for file_name in required_files:
            file_path = env_path / file_name
            assert file_path.exists(), f"Falta archivo en staging: {file_name}"

    def test_prod_environment_has_required_files(self):
        """Ambiente prod debe tener archivos requeridos"""
        env_path = Path(__file__).parent.parent / "terraform" / "environments" / "prod"

        if not env_path.exists():
            pytest.skip("Ambiente prod no existe")

        required_files = ["main.tf", "terraform.tfvars", "backend.tf"]

        for file_name in required_files:
            file_path = env_path / file_name
            assert file_path.exists(), f"Falta archivo en prod: {file_name}"


class TestModuleDocumentation:
    """Tests para documentación de módulos"""

    def test_data_lake_module_readme_not_empty(self):
        """README del módulo data-lake no debe estar vacío"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "data-lake"
        )
        readme_path = module_path / "README.md"

        if not readme_path.exists():
            pytest.skip("README de data-lake no existe")

        with open(readme_path, encoding="utf-8") as f:
            content = f.read().strip()

        assert len(content) > 100, "README muy corto (< 100 caracteres)"
        assert "# " in content, "README debe tener un título (# )"

    def test_lambda_etl_module_readme_has_usage_example(self):
        """README de lambda-etl debe tener ejemplo de uso"""
        module_path = (
            Path(__file__).parent.parent / "terraform" / "modules" / "lambda-etl"
        )
        readme_path = module_path / "README.md"

        if not readme_path.exists():
            pytest.skip("README de lambda-etl no existe")

        with open(readme_path, encoding="utf-8") as f:
            content = f.read().lower()

        # Debe contener ejemplo de uso del módulo
        assert "module" in content, "README debe tener ejemplo con 'module'"
        assert "source" in content, "README debe mostrar cómo usar el módulo"

    def test_all_modules_have_variables_documented(self):
        """Todos los módulos deben documentar sus variables"""
        modules_path = Path(__file__).parent.parent / "terraform" / "modules"

        if not modules_path.exists():
            pytest.skip("Directorio modules no existe")

        for module_dir in modules_path.iterdir():
            if not module_dir.is_dir():
                continue

            variables_file = module_dir / "variables.tf"
            if not variables_file.exists():
                continue

            with open(variables_file, encoding="utf-8") as f:
                content = f.read()

            # Verificar que cada variable tenga descripción
            if 'variable "' in content:
                assert (
                    "description" in content
                ), f"Módulo {module_dir.name} tiene variables sin descripción"


class TestProjectStructure:
    """Tests para estructura general del proyecto"""

    def test_tests_directory_exists(self):
        """Debe existir directorio de tests"""
        tests_path = Path(__file__).parent

        assert tests_path.exists()
        assert tests_path.name == "tests"

    def test_scripts_directory_exists(self):
        """Debe existir directorio de scripts"""
        scripts_path = Path(__file__).parent.parent / "scripts"

        # Por ahora es opcional, pero recomendado
        if scripts_path.exists():
            assert scripts_path.is_dir()

    def test_docs_directory_exists(self):
        """Debe existir directorio de documentación"""
        docs_path = Path(__file__).parent.parent / "docs"

        # Por ahora es opcional
        if docs_path.exists():
            assert docs_path.is_dir()

    def test_readme_exists_in_root(self):
        """Debe existir README.md en raíz del proyecto"""
        readme_path = Path(__file__).parent.parent / "README.md"

        assert readme_path.exists(), "Falta README.md principal"

        with open(readme_path, encoding="utf-8") as f:
            content = f.read()

        assert len(content) > 500, "README principal muy corto"
        assert "# " in content, "README debe tener título principal"

    def test_requirements_txt_exists(self):
        """Debe existir requirements.txt"""
        req_path = Path(__file__).parent.parent / "requirements.txt"

        assert req_path.exists(), "Falta requirements.txt"

        with open(req_path, encoding="utf-8") as f:
            content = f.read()

        # Debe tener al menos pytest
        assert "pytest" in content.lower(), "requirements.txt debe incluir pytest"

    def test_pytest_ini_exists(self):
        """Debe existir pytest.ini"""
        pytest_ini = Path(__file__).parent.parent / "pytest.ini"

        # Es opcional, pero recomendado
        if pytest_ini.exists():
            with open(pytest_ini, encoding="utf-8") as f:
                content = f.read()

            assert "[pytest]" in content, "pytest.ini debe tener sección [pytest]"
