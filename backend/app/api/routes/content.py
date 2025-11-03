"""
API routes for course content.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.content import Module, ModuleSummary, ContentResponse
from app.services.content_service import ContentService

router = APIRouter()
content_service = ContentService()


@router.get("/modules", response_model=List[ModuleSummary])
async def get_modules():
    """
    Get all course modules.

    Returns:
        List of module summaries
    """
    return content_service.get_all_modules()


@router.get("/modules/{module_id}", response_model=Module)
async def get_module(module_id: str):
    """
    Get a specific module with its topics.

    Args:
        module_id: Module identifier (e.g., 'modulo-01-fundamentos')

    Returns:
        Module with topics

    Raises:
        HTTPException: If module not found
    """
    module = content_service.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.get("/content/{module_id}/{topic_id}/{section}", response_model=ContentResponse)
async def get_content(module_id: str, topic_id: str, section: str):
    """
    Get content for a specific topic section.

    Args:
        module_id: Module identifier
        topic_id: Topic identifier (e.g., 'tema-1-sql-basico')
        section: Section name ('teoria', 'ejemplos', 'ejercicios', 'proyecto')

    Returns:
        Content response with markdown

    Raises:
        HTTPException: If content not found
    """
    content = content_service.get_topic_content(module_id, topic_id, section)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return ContentResponse(
        module_id=module_id,
        topic_id=topic_id,
        section=section,
        content=content,
    )
