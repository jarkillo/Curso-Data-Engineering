"""
API routes for game system.
"""

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.game import (
    Achievement,
    AddXPRequest,
    GameStateResponse,
    Mission,
    MissionAttempt,
    MissionResult,
)
from app.services.game_service import GameService

router = APIRouter()
game_service = GameService()


def parse_json_list(value: str | None) -> list:
    """Parse JSON string to list."""
    if not value:
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []


@router.get("/state", response_model=GameStateResponse)
async def get_game_state(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get current game state."""
    game_state = game_service.get_or_create_game_state(db, current_user.id)
    return game_service.get_game_state_response(game_state)


@router.get("/missions", response_model=list[Mission])
async def get_missions(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get all available missions with their quiz questions."""
    game_state = game_service.get_or_create_game_state(db, current_user.id)
    completed = parse_json_list(game_state.completed_missions)
    return game_service.get_available_missions(completed)


@router.get("/achievements", response_model=list[Achievement])
async def get_achievements(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get all achievements."""
    game_state = game_service.get_or_create_game_state(db, current_user.id)
    unlocked = parse_json_list(game_state.unlocked_achievements)
    return game_service.get_achievements(unlocked)


@router.post("/mission/{mission_id}/complete", response_model=MissionResult)
async def complete_mission(
    mission_id: str,
    attempt: MissionAttempt,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Complete a mission by answering quiz questions.

    - Must answer all questions correctly to pass
    - Can retry missions but won't earn XP again
    """
    game_state = game_service.get_or_create_game_state(db, current_user.id)

    # Find mission
    mission = game_service.get_mission_by_id(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Parse current completed missions
    completed_missions = parse_json_list(game_state.completed_missions)
    is_retry = mission_id in completed_missions

    # Evaluate answers
    correct, total = game_service.evaluate_mission_answers(mission_id, attempt.answers)

    # Need all correct to pass
    if correct < total:
        return MissionResult(
            success=False,
            correct_answers=correct,
            total_questions=total,
            xp_earned=0,
            message=f"Respuestas correctas: {correct}/{total}. ¡Inténtalo de nuevo!",
            is_retry=is_retry,
        )

    # Mission passed!
    xp_earned = 0

    # Only award XP on first completion
    if not is_retry:
        xp_earned = mission["xp_reward"]

        # Add to completed missions
        completed_missions.append(mission_id)
        game_state.completed_missions = json.dumps(completed_missions)

        # Add XP
        game_state.xp += xp_earned
        game_state.total_xp_earned += xp_earned

        # Check level up
        while game_state.xp >= game_service._calculate_xp_for_next_level(
            game_state.level
        ):
            xp_needed = game_service._calculate_xp_for_next_level(game_state.level)
            game_state.xp -= xp_needed
            game_state.level += 1

        # Parse current achievements
        unlocked_achievements = parse_json_list(game_state.unlocked_achievements)

        # First mission achievement
        if (
            len(completed_missions) == 1
            and "first_mission" not in unlocked_achievements
        ):
            unlocked_achievements.append("first_mission")

        # Perfect score achievement (always check on perfect)
        if correct == total and "perfect_score" not in unlocked_achievements:
            unlocked_achievements.append("perfect_score")

        # Level 5 achievement
        if game_state.level >= 5 and "level_5" not in unlocked_achievements:
            unlocked_achievements.append("level_5")

        # Save achievements back as JSON
        game_state.unlocked_achievements = json.dumps(unlocked_achievements)

        db.commit()
        db.refresh(game_state)

    message = "¡Misión completada!"
    if is_retry:
        message = "¡Bien hecho! Ya habías completado esta misión, así que no ganas XP adicional."
    elif xp_earned > 0:
        message = f"¡Misión completada! +{xp_earned} XP"

    return MissionResult(
        success=True,
        correct_answers=correct,
        total_questions=total,
        xp_earned=xp_earned,
        message=message,
        is_retry=is_retry,
    )


@router.post("/xp", response_model=GameStateResponse)
async def add_xp(
    request: AddXPRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add XP to player."""
    game_state = game_service.get_or_create_game_state(db, current_user.id)

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
