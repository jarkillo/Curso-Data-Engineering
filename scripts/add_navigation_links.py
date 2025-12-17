#!/usr/bin/env python3
"""
Script para añadir enlaces de navegación al final de cada archivo del curso.

Añade enlaces "Anterior" y "Siguiente" para facilitar la navegación entre:
- Archivos dentro de un tema (01-TEORIA → 02-EJEMPLOS → 03-EJERCICIOS → proyecto)
- Temas dentro de un módulo
- Módulos del curso
"""

import os
import re
from pathlib import Path


def get_module_order() -> list[dict]:
    """Define el orden de módulos y sus temas."""
    return [
        {
            "path": "modulo-01-fundamentos",
            "name": "Módulo 1: Fundamentos",
            "topics": [
                {"path": "tema-1-python-estadistica", "name": "Python y Estadística"},
                {"path": "tema-2-procesamiento-csv", "name": "Procesamiento CSV"},
                {"path": "tema-3-logs-debugging", "name": "Logs y Debugging"},
            ],
        },
        {
            "path": "modulo-02-sql",
            "name": "Módulo 2: SQL",
            "topics": [
                {"path": "tema-1-sql-basico", "name": "SQL Básico"},
                {"path": "tema-2-sql-intermedio", "name": "SQL Intermedio"},
                {"path": "tema-3-optimizacion", "name": "Optimización SQL"},
            ],
        },
        {
            "path": "modulo-03-ingenieria-datos",
            "name": "Módulo 3: Ingeniería de Datos",
            "topics": [
                {"path": "tema-1-conceptos-etl", "name": "Conceptos ETL"},
                {"path": "tema-2-extraccion", "name": "Extracción"},
                {"path": "tema-3-transformacion", "name": "Transformación"},
                {"path": "tema-4-calidad-datos", "name": "Calidad de Datos"},
                {"path": "tema-5-formatos-modernos", "name": "Formatos Modernos"},
                {"path": "tema-6-carga-pipelines", "name": "Carga y Pipelines"},
            ],
        },
        {
            "path": "modulo-04-apis-scraping",
            "name": "Módulo 4: APIs y Web Scraping",
            "topics": [
                {"path": "tema-1-apis-rest", "name": "APIs REST"},
                {"path": "tema-2-web-scraping", "name": "Web Scraping"},
                {
                    "path": "tema-3-rate-limiting-caching",
                    "name": "Rate Limiting y Caching",
                },
            ],
        },
        {
            "path": "modulo-05-bases-datos-avanzadas",
            "name": "Módulo 5: Bases de Datos Avanzadas",
            "topics": [
                {"path": "tema-1-postgresql-avanzado", "name": "PostgreSQL Avanzado"},
                {"path": "tema-2-mongodb", "name": "MongoDB"},
                {"path": "tema-3-modelado-datos", "name": "Modelado de Datos"},
            ],
        },
        {
            "path": "modulo-06-airflow",
            "name": "Módulo 6: Apache Airflow",
            "topics": [
                {"path": "tema-1-introduccion", "name": "Introducción a Airflow"},
                {"path": "tema-2-intermedio", "name": "Airflow Intermedio"},
            ],
        },
        {
            "path": "modulo-07-cloud",
            "name": "Módulo 7: Cloud Computing",
            "topics": [
                {"path": "tema-1-aws", "name": "AWS"},
                {"path": "tema-2-gcp", "name": "Google Cloud Platform"},
                {"path": "tema-3-iac", "name": "Infrastructure as Code"},
            ],
        },
        {
            "path": "modulo-08-data-warehousing",
            "name": "Módulo 8: Data Warehousing",
            "topics": [
                {"path": "tema-1-dimensional-modeling", "name": "Modelado Dimensional"},
                {"path": "tema-2-herramientas-dwh", "name": "Herramientas DWH"},
                {"path": "tema-3-analytics-bi", "name": "Analytics y BI"},
            ],
        },
        {
            "path": "modulo-09-spark",
            "name": "Módulo 9: Spark y Big Data",
            "topics": [
                {"path": "tema-1-introduccion", "name": "Introducción a Spark"},
                {"path": "tema-2-optimizacion", "name": "Optimización Spark"},
                {"path": "tema-3-streaming", "name": "Spark Streaming"},
            ],
        },
        {
            "path": "modulo-10-ml-data-engineers",
            "name": "Módulo 10: ML para Data Engineers",
            "topics": [
                {"path": "tema-1-feature-engineering", "name": "Feature Engineering"},
                {"path": "tema-2-pipelines-ml", "name": "Pipelines ML"},
                {"path": "tema-3-mlops", "name": "MLOps"},
            ],
        },
    ]


def get_files_in_topic(
    base_path: Path, module_path: str, topic_path: str
) -> list[dict]:
    """Obtiene los archivos de un tema en orden."""
    topic_dir = base_path / module_path / topic_path
    files = []

    # Archivos principales en orden
    main_files = ["01-TEORIA.md", "02-EJEMPLOS.md", "03-EJERCICIOS.md"]

    for f in main_files:
        file_path = topic_dir / f
        if file_path.exists():
            files.append(
                {
                    "path": file_path,
                    "name": f.replace(".md", "").replace("-", " ").title(),
                }
            )

    # Proyecto práctico (puede estar en 04-proyecto-practico o proyecto-practico)
    for project_dir in ["04-proyecto-practico", "proyecto-practico"]:
        readme_path = topic_dir / project_dir / "README.md"
        if readme_path.exists():
            files.append({"path": readme_path, "name": "Proyecto Práctico"})
            break

    return files


def build_navigation_sequence(base_path: Path) -> list[dict]:
    """Construye la secuencia completa de navegación."""
    modules = get_module_order()
    sequence = []

    for module in modules:
        for topic in module["topics"]:
            files = get_files_in_topic(base_path, module["path"], topic["path"])
            for file_info in files:
                sequence.append(
                    {
                        "path": file_info["path"],
                        "file_name": file_info["name"],
                        "topic_name": topic["name"],
                        "module_name": module["name"],
                    }
                )

    return sequence


def calculate_relative_path(from_path: Path, to_path: Path) -> str:
    """Calcula la ruta relativa entre dos archivos."""
    try:
        return os.path.relpath(to_path, from_path.parent).replace("\\", "/")
    except ValueError:
        # En Windows, si están en diferentes drives
        return str(to_path).replace("\\", "/")


def create_navigation_block(
    current: dict,
    prev_item: dict | None,
    next_item: dict | None,
) -> str:
    """Crea el bloque de navegación en markdown."""
    lines = [
        "",
        "---",
        "",
        "## 🧭 Navegación",
        "",
    ]

    nav_items = []

    if prev_item:
        rel_path = calculate_relative_path(current["path"], prev_item["path"])
        prev_label = f"{prev_item['file_name']}"
        if prev_item["topic_name"] != current["topic_name"]:
            prev_label = f"{prev_item['topic_name']} - {prev_item['file_name']}"
        if prev_item["module_name"] != current["module_name"]:
            prev_label = f"{prev_item['module_name']}: {prev_item['topic_name']}"
        nav_items.append(f"⬅️ **Anterior**: [{prev_label}]({rel_path})")

    if next_item:
        rel_path = calculate_relative_path(current["path"], next_item["path"])
        next_label = f"{next_item['file_name']}"
        if next_item["topic_name"] != current["topic_name"]:
            next_label = f"{next_item['topic_name']} - {next_item['file_name']}"
        if next_item["module_name"] != current["module_name"]:
            next_label = f"{next_item['module_name']}: {next_item['topic_name']}"
        nav_items.append(f"➡️ **Siguiente**: [{next_label}]({rel_path})")

    if nav_items:
        lines.append(" | ".join(nav_items))
    else:
        lines.append("*Este es el último archivo del curso.*")

    lines.append("")

    return "\n".join(lines)


def remove_existing_navigation(content: str) -> str:
    """Elimina bloques de navegación existentes."""
    # Patrón para encontrar el bloque de navegación
    pattern = r"\n---\n\n## 🧭 Navegación\n.*?(?=\n---\n|$)"
    content = re.sub(pattern, "", content, flags=re.DOTALL)

    # También eliminar si está al final sin --- posterior
    pattern2 = r"\n---\n\n## 🧭 Navegación\n.*$"
    content = re.sub(pattern2, "", content, flags=re.DOTALL)

    return content.rstrip()


def add_navigation_to_file(
    file_path: Path,
    nav_block: str,
    dry_run: bool = False,
) -> bool:
    """Añade navegación a un archivo."""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Eliminar navegación existente
        content = remove_existing_navigation(content)

        # Añadir nueva navegación
        new_content = content + nav_block

        if dry_run:
            print(f"[DRY RUN] Would update: {file_path}")
            return True

        file_path.write_text(new_content, encoding="utf-8")
        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main(base_path: str, dry_run: bool = False) -> None:
    """Función principal."""
    base = Path(base_path)

    if not base.exists():
        print(f"Error: Path does not exist: {base}")
        return

    print(f"📚 Añadiendo navegación al curso en: {base}")
    print(f"{'[DRY RUN] ' if dry_run else ''}Procesando archivos...\n")

    sequence = build_navigation_sequence(base)

    print(f"Encontrados {len(sequence)} archivos para procesar.\n")

    updated = 0
    errors = 0

    for i, item in enumerate(sequence):
        prev_item = sequence[i - 1] if i > 0 else None
        next_item = sequence[i + 1] if i < len(sequence) - 1 else None

        nav_block = create_navigation_block(item, prev_item, next_item)

        if add_navigation_to_file(item["path"], nav_block, dry_run):
            updated += 1
            status = "✅"
        else:
            errors += 1
            status = "❌"

        # Mostrar progreso
        rel_path = item["path"].relative_to(base)
        print(f"{status} {rel_path}")

    print(f"\n{'=' * 50}")
    print(f"✅ Actualizados: {updated}")
    print(f"❌ Errores: {errors}")
    print(f"📁 Total: {len(sequence)}")


if __name__ == "__main__":
    import sys

    # Fix encoding for Windows console
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    # Detectar el directorio base del curso
    script_dir = Path(__file__).parent
    course_dir = script_dir.parent

    # Verificar argumentos
    dry_run = "--dry-run" in sys.argv

    main(str(course_dir), dry_run=dry_run)
