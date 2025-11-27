"""
API routes for user progress.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ProgressSummary(BaseModel):
    """User progress summary."""

    total_modules: int = 10
    completed_modules: int = 4
    total_topics: int = 31
    completed_topics: int = 13
    overall_percentage: int = 40


@router.get("/", response_model=ProgressSummary)
async def get_progress():
    """
    Get overall user progress.

    Returns:
        Progress summary

    Note:
        For MVP, returns hardcoded values from README.
        In future, will calculate from database.
    """
    return ProgressSummary(
        total_modules=10,
        completed_modules=4,
        total_topics=31,
        completed_topics=13,
        overall_percentage=40,
    )
