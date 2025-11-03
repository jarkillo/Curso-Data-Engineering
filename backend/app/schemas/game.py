"""
Schemas for game system.
"""

from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel


class GameStats(BaseModel):
    """Player statistics."""

    lines_of_code: int = 0
    tests_passed: int = 0
    bugs_fixed: int = 0
    projects_completed: int = 0
    study_hours: int = 0
    exercises_solved: int = 0


class GameStateResponse(BaseModel):
    """Current game state."""

    player_name: str
    level: int
    xp: int
    total_xp_earned: int
    current_module: int
    current_tema: int
    completed_missions: List[str]
    unlocked_achievements: List[str]
    unlocked_technologies: List[str]
    stats: GameStats
    created_at: datetime
    last_played: datetime
    play_time_minutes: int

    # Calculated fields
    current_rank: Optional[Dict] = None
    next_rank: Optional[Dict] = None
    xp_for_next_level: Optional[int] = None


class Mission(BaseModel):
    """A game mission."""

    id: str
    title: str
    description: str
    module: int
    tema: int
    xp_reward: int
    requirements: List[str] = []
    is_completed: bool = False
    is_available: bool = True


class Achievement(BaseModel):
    """A game achievement."""

    key: str
    name: str
    description: str
    emoji: str
    is_unlocked: bool = False


class AddXPRequest(BaseModel):
    """Request to add XP."""

    amount: int
    reason: Optional[str] = None
