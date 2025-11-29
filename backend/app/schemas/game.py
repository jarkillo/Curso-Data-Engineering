"""
Schemas for game system.
"""

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
    completed_missions: list[str]
    unlocked_achievements: list[str]
    unlocked_technologies: list[str]
    stats: GameStats
    created_at: datetime
    last_played: datetime
    play_time_minutes: int

    # Calculated fields
    current_rank: dict | None = None
    next_rank: dict | None = None
    xp_for_next_level: int | None = None


class Mission(BaseModel):
    """A game mission."""

    id: str
    title: str
    description: str
    module: int
    tema: int
    xp_reward: int
    requirements: list[str] = []
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
    reason: str | None = None
