"""
Schemas for course content.
"""

from pydantic import BaseModel


class TopicContent(BaseModel):
    """Content of a topic section."""

    section: str  # 'teoria', 'ejemplos', 'ejercicios', 'proyecto'
    content: str  # Markdown content
    file_path: str


class Topic(BaseModel):
    """A topic within a module."""

    id: str  # e.g., "tema-1-sql-basico"
    number: int  # 1, 2, 3...
    title: str  # "SQL Básico"
    description: str | None = None
    completed: bool = False
    coverage: int | None = None  # Test coverage percentage
    available_sections: list[
        str
    ] = []  # ['teoria', 'ejemplos', 'ejercicios', 'proyecto']


class Module(BaseModel):
    """A course module."""

    id: str  # e.g., "modulo-01-fundamentos"
    number: int  # 1, 2, 3...
    title: str  # "Fundamentos de Programación"
    description: str | None = None
    status: str  # "completed", "in_progress", "locked"
    progress_percentage: int = 0
    topics: list[Topic] = []


class ModuleSummary(BaseModel):
    """Summary of a module without topics."""

    id: str
    number: int
    title: str
    description: str | None = None
    status: str
    progress_percentage: int = 0
    topic_count: int = 0


class ContentResponse(BaseModel):
    """Response with markdown content."""

    module_id: str
    topic_id: str
    section: str
    content: str
    metadata: dict | None = None
