"""
Tests para validar formato de código Terraform.

Valida que todo el código esté formateado correctamente según estándar.
"""

import subprocess
from pathlib import Path

import pytest


class TestTerraformFormat:
    """Tests para terraform fmt"""

    def test_format_check_all_terraform_files(self):
        """Debe verificar que todos los archivos .tf estén formateados"""
        terraform_root = Path(__file__).parent.parent / "terraform"

        result = subprocess.run(
            ["terraform", "fmt", "-check", "-recursive"],
            cwd=terraform_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            # Si hay archivos sin formatear, mostrarlos
            unformatted_files = result.stdout.strip()
            pytest.fail(
                f"Archivos sin formatear correctamente:\\n{unformatted_files}\\n\\n"
                f"Ejecuta: terraform fmt -recursive"
            )

        assert result.returncode == 0, "Algunos archivos no están formateados"

    def test_format_environments_directory(self):
        """Debe verificar formato en directorio environments"""
        env_path = Path(__file__).parent.parent / "terraform" / "environments"

        if not env_path.exists():
            pytest.skip("Directorio environments no existe")

        result = subprocess.run(
            ["terraform", "fmt", "-check", "-recursive"],
            cwd=env_path,
            capture_output=True,
            text=True,
        )

        assert (
            result.returncode == 0
        ), f"Archivos sin formatear en environments: {result.stdout}"

    def test_format_modules_directory(self):
        """Debe verificar formato en directorio modules"""
        modules_path = Path(__file__).parent.parent / "terraform" / "modules"

        if not modules_path.exists():
            pytest.skip("Directorio modules no existe")

        result = subprocess.run(
            ["terraform", "fmt", "-check", "-recursive"],
            cwd=modules_path,
            capture_output=True,
            text=True,
        )

        assert (
            result.returncode == 0
        ), f"Archivos sin formatear en modules: {result.stdout}"

    def test_no_trailing_whitespace(self):
        """Debe verificar que no haya espacios al final de líneas"""
        terraform_root = Path(__file__).parent.parent / "terraform"

        # Buscar todos los archivos .tf
        tf_files = list(terraform_root.rglob("*.tf"))

        files_with_trailing = []

        for tf_file in tf_files:
            with open(tf_file, encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    # Verificar espacios al final (antes del \\n)
                    if line.rstrip("\\n") != line.rstrip():
                        files_with_trailing.append(f"{tf_file}:{line_num}")

        if files_with_trailing:
            pytest.fail(
                "Archivos con espacios al final de línea:\\n"
                + "\\n".join(files_with_trailing[:10])  # Mostrar máximo 10
            )

        assert len(files_with_trailing) == 0

    def test_consistent_indentation(self):
        """Debe verificar que la indentación sea consistente (2 espacios)"""
        terraform_root = Path(__file__).parent.parent / "terraform"

        # Buscar todos los archivos .tf
        tf_files = list(terraform_root.rglob("*.tf"))

        files_with_tabs = []

        for tf_file in tf_files:
            with open(tf_file, encoding="utf-8") as f:
                content = f.read()
                if "\\t" in content:
                    files_with_tabs.append(str(tf_file))

        if files_with_tabs:
            pytest.fail(
                "Archivos con tabs en vez de espacios:\\n" + "\\n".join(files_with_tabs)
            )

        assert len(files_with_tabs) == 0, "Usar espacios en vez de tabs"
