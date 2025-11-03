"""
Service for handling course content.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict
from app.config import settings
from app.schemas.content import Module, ModuleSummary, Topic, TopicContent


class ContentService:
    """Service for managing course content."""

    # Mapping of module directories
    MODULES = [
        {"id": "modulo-01-fundamentos", "number": 1, "title": "Fundamentos de Programación"},
        {"id": "modulo-02-sql", "number": 2, "title": "Bases de Datos y SQL"},
        {"id": "modulo-03-ingenieria-datos", "number": 3, "title": "Ingeniería de Datos Core"},
        {"id": "modulo-04-apis-scraping", "number": 4, "title": "APIs y Web Scraping"},
        {"id": "modulo-05-bases-datos-avanzadas", "number": 5, "title": "Bases de Datos Avanzadas"},
        {"id": "modulo-06-airflow", "number": 6, "title": "Orquestación con Airflow"},
    ]

    # Status mapping based on README
    MODULE_STATUS = {
        "modulo-01-fundamentos": "completed",
        "modulo-02-sql": "in_progress",
        "modulo-03-ingenieria-datos": "in_progress",
        "modulo-04-apis-scraping": "completed",
        "modulo-05-bases-datos-avanzadas": "in_progress",
        "modulo-06-airflow": "locked",
    }

    def __init__(self):
        """Initialize content service."""
        self.base_path = Path(settings.content_base_path)

    def get_all_modules(self) -> List[ModuleSummary]:
        """
        Get all course modules.

        Returns:
            List of module summaries
        """
        modules = []
        for module_data in self.MODULES:
            module_path = self.base_path / module_data["id"]

            # Check if module exists
            if not module_path.exists():
                continue

            # Count topics
            topic_count = len(self._get_topics_for_module(module_data["id"]))

            modules.append(
                ModuleSummary(
                    id=module_data["id"],
                    number=module_data["number"],
                    title=module_data["title"],
                    status=self.MODULE_STATUS.get(module_data["id"], "locked"),
                    progress_percentage=self._calculate_module_progress(module_data["id"]),
                    topic_count=topic_count,
                )
            )

        return modules

    def get_module(self, module_id: str) -> Optional[Module]:
        """
        Get a specific module with its topics.

        Args:
            module_id: Module identifier

        Returns:
            Module with topics or None
        """
        module_data = next((m for m in self.MODULES if m["id"] == module_id), None)
        if not module_data:
            return None

        module_path = self.base_path / module_id
        if not module_path.exists():
            return None

        topics = self._get_topics_for_module(module_id)

        return Module(
            id=module_id,
            number=module_data["number"],
            title=module_data["title"],
            status=self.MODULE_STATUS.get(module_id, "locked"),
            progress_percentage=self._calculate_module_progress(module_id),
            topics=topics,
        )

    def get_topic_content(
        self, module_id: str, topic_id: str, section: str
    ) -> Optional[str]:
        """
        Get content for a specific topic section.

        Args:
            module_id: Module identifier
            topic_id: Topic identifier
            section: Section name (teoria, ejemplos, ejercicios, proyecto)

        Returns:
            Markdown content or None
        """
        # Map section to file name
        section_files = {
            "teoria": "01-TEORIA.md",
            "ejemplos": "02-EJEMPLOS.md",
            "ejercicios": "03-EJERCICIOS.md",
            "proyecto": "04-proyecto-practico/README.md",
        }

        if section not in section_files:
            return None

        file_path = self.base_path / module_id / topic_id / section_files[section]

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def _get_topics_for_module(self, module_id: str) -> List[Topic]:
        """Get all topics for a module."""
        module_path = self.base_path / module_id
        topics = []

        if not module_path.exists():
            return topics

        # Find all tema-* directories
        for item in sorted(module_path.iterdir()):
            if item.is_dir() and item.name.startswith("tema-"):
                # Extract topic number and name
                parts = item.name.split("-", 2)
                if len(parts) >= 3:
                    topic_number = int(parts[1])
                    topic_name = parts[2].replace("-", " ").title()

                    # Check which sections exist
                    available_sections = []
                    if (item / "01-TEORIA.md").exists():
                        available_sections.append("teoria")
                    if (item / "02-EJEMPLOS.md").exists():
                        available_sections.append("ejemplos")
                    if (item / "03-EJERCICIOS.md").exists():
                        available_sections.append("ejercicios")
                    if (item / "04-proyecto-practico").exists():
                        available_sections.append("proyecto")

                    topics.append(
                        Topic(
                            id=item.name,
                            number=topic_number,
                            title=topic_name,
                            completed=False,  # TODO: Get from user progress
                            available_sections=available_sections,
                        )
                    )

        return topics

    def _calculate_module_progress(self, module_id: str) -> int:
        """Calculate progress percentage for a module."""
        # For MVP, use hardcoded values based on README
        progress_map = {
            "modulo-01-fundamentos": 100,
            "modulo-02-sql": 33,
            "modulo-03-ingenieria-datos": 33,
            "modulo-04-apis-scraping": 100,
            "modulo-05-bases-datos-avanzadas": 33,
            "modulo-06-airflow": 0,
        }
        return progress_map.get(module_id, 0)
