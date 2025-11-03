"""
API routes for game system.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.game import GameStateResponse, Mission, Achievement, AddXPRequest
from app.services.game_service import GameService

router = APIRouter()
game_service = GameService()


@router.get("/state", response_model=GameStateResponse)
async def get_game_state(db: Session = Depends(get_db)):
    """
    Get current game state.

    Returns:
        Game state with all player information
    """
    game_state = game_service.get_or_create_game_state(db)
    return game_service.get_game_state_response(game_state)


@router.get("/missions", response_model=List[Mission])
async def get_missions(db: Session = Depends(get_db)):
    """
    Get all available missions.

    Returns:
        List of missions with completion status
    """
    game_state = game_service.get_or_create_game_state(db)
    return game_service.get_available_missions(game_state.completed_missions or [])


@router.get("/achievements", response_model=List[Achievement])
async def get_achievements(db: Session = Depends(get_db)):
    """
    Get all achievements.

    Returns:
        List of achievements with unlock status
    """
    game_state = game_service.get_or_create_game_state(db)
    return game_service.get_achievements(game_state.unlocked_achievements or [])


@router.post("/mission/{mission_id}/complete", response_model=GameStateResponse)
async def complete_mission(mission_id: str, db: Session = Depends(get_db)):
    """
    Complete a mission and award XP.

    Args:
        mission_id: Mission identifier

    Returns:
        Updated game state

    Raises:
        HTTPException: If mission not found or already completed
    """
    game_state = game_service.get_or_create_game_state(db)

    # Find mission
    mission = next(
        (m for m in game_service.MISSIONS if m["id"] == mission_id), None
    )
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Check if already completed
    if mission_id in (game_state.completed_missions or []):
        raise HTTPException(status_code=400, detail="Mission already completed")

    # Add to completed missions
    if game_state.completed_missions is None:
        game_state.completed_missions = []
    game_state.completed_missions.append(mission_id)

    # Add XP
    game_state.xp += mission["xp_reward"]
    game_state.total_xp_earned += mission["xp_reward"]

    # Check level up
    while game_state.xp >= game_service._calculate_xp_for_next_level(game_state.level):
        xp_needed = game_service._calculate_xp_for_next_level(game_state.level)
        game_state.xp -= xp_needed
        game_state.level += 1

    # Check achievements
    if game_state.unlocked_achievements is None:
        game_state.unlocked_achievements = []

    # First mission achievement
    if len(game_state.completed_missions) == 1 and "first_mission" not in game_state.unlocked_achievements:
        game_state.unlocked_achievements.append("first_mission")

    # Level 5 achievement
    if game_state.level >= 5 and "level_5" not in game_state.unlocked_achievements:
        game_state.unlocked_achievements.append("level_5")

    db.commit()
    db.refresh(game_state)

    return game_service.get_game_state_response(game_state)


@router.post("/xp", response_model=GameStateResponse)
async def add_xp(request: AddXPRequest, db: Session = Depends(get_db)):
    """
    Add XP to player.

    Args:
        request: XP amount and reason

    Returns:
        Updated game state
    """
    game_state = game_service.get_or_create_game_state(db)

    # Add XP
    game_state.xp += request.amount
    game_state.total_xp_earned += request.amount

    # Check level up
    while game_state.xp >= game_service._calculate_xp_for_next_level(game_state.level):
        xp_needed = game_service._calculate_xp_for_next_level(game_state.level)
        game_state.xp -= xp_needed
        game_state.level += 1

    db.commit()
    db.refresh(game_state)

    return game_service.get_game_state_response(game_state)
