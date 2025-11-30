"""
Service for game logic.
"""

import json

from sqlalchemy.orm import Session

from app.models.game import GameState
from app.schemas.game import Achievement, GameStateResponse, GameStats, Mission


class GameService:
    """Service for managing game state and logic."""

    # XP required per level (from original game)
    XP_PER_LEVEL = [
        0,
        100,
        250,
        450,
        700,
        1000,
        1400,
        1900,
        2500,
        3200,
        4000,
        5000,
        6200,
        7600,
        9200,
        11000,
        13000,
        15500,
        18500,
        22000,
    ]

    # Ranks (from original game)
    RANKS = [
        {"level": 0, "name": "Trainee", "emoji": "🎓"},
        {"level": 3, "name": "Junior Data Engineer", "emoji": "💼"},
        {"level": 7, "name": "Data Engineer", "emoji": "🔧"},
        {"level": 12, "name": "Senior Data Engineer", "emoji": "⭐"},
        {"level": 17, "name": "Lead Data Engineer", "emoji": "👑"},
        {"level": 20, "name": "Data Architect", "emoji": "🏆"},
    ]

    # Predefined missions
    MISSIONS = [
        {
            "id": "mission-1-python-stats",
            "title": "Tu Primera Función Estadística",
            "description": "Implementa funciones de estadística descriptiva en Python",
            "module": 1,
            "tema": 1,
            "xp_reward": 100,
        },
        {
            "id": "mission-2-csv-processor",
            "title": "Procesador de CSV Profesional",
            "description": "Crea un sistema robusto de procesamiento de archivos CSV",
            "module": 1,
            "tema": 2,
            "xp_reward": 150,
        },
        {
            "id": "mission-3-logging-system",
            "title": "Sistema de Logging Avanzado",
            "description": "Implementa un sistema de logging configurable para pipelines",
            "module": 1,
            "tema": 3,
            "xp_reward": 120,
        },
        {
            "id": "mission-4-sql-basics",
            "title": "Domina SQL Básico",
            "description": "Crea queries SQL para consultar bases de datos",
            "module": 2,
            "tema": 1,
            "xp_reward": 150,
        },
    ]

    # Achievements
    ACHIEVEMENTS = [
        {
            "key": "first_mission",
            "name": "Primera Misión",
            "description": "Completa tu primera misión",
            "emoji": "🎯",
        },
        {
            "key": "level_5",
            "name": "Junior Engineer",
            "description": "Alcanza el nivel 5",
            "emoji": "💼",
        },
        {
            "key": "module_1_complete",
            "name": "Fundamentos Dominados",
            "description": "Completa el Módulo 1",
            "emoji": "📚",
        },
    ]

    def get_or_create_game_state(self, db: Session, user_id: int = 1) -> GameState:
        """
        Get or create game state for a user.

        Args:
            db: Database session
            user_id: User ID (default 1 for MVP)

        Returns:
            Game state
        """
        game_state = db.query(GameState).filter(GameState.user_id == user_id).first()

        if not game_state:
            game_state = GameState(
                user_id=user_id,
                player_name="Player",
                completed_missions=json.dumps([]),
                unlocked_achievements=json.dumps([]),
                unlocked_technologies=json.dumps(["Python", "Git"]),
                stats=json.dumps(
                    {
                        "lines_of_code": 0,
                        "tests_passed": 0,
                        "bugs_fixed": 0,
                        "projects_completed": 0,
                        "study_hours": 0,
                        "exercises_solved": 0,
                    }
                ),
            )
            db.add(game_state)
            db.commit()
            db.refresh(game_state)

        return game_state

    def _parse_json_field(self, value: str | None, default: list | dict) -> list | dict:
        """Parse JSON field from database."""
        if not value:
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return default

    def get_game_state_response(self, game_state: GameState) -> GameStateResponse:
        """
        Convert GameState model to response schema.

        Args:
            game_state: Database game state

        Returns:
            Game state response
        """
        current_rank = self._get_rank_at_level(game_state.level)
        next_rank = self._get_next_rank(game_state.level)
        xp_for_next = self._calculate_xp_for_next_level(game_state.level)

        # Parse JSON fields
        completed_missions = self._parse_json_field(game_state.completed_missions, [])
        unlocked_achievements = self._parse_json_field(
            game_state.unlocked_achievements, []
        )
        unlocked_technologies = self._parse_json_field(
            game_state.unlocked_technologies, []
        )
        stats_dict = self._parse_json_field(game_state.stats, {})

        return GameStateResponse(
            player_name=game_state.player_name,
            level=game_state.level,
            xp=game_state.xp,
            total_xp_earned=game_state.total_xp_earned,
            current_module=game_state.current_module,
            current_tema=game_state.current_tema,
            completed_missions=completed_missions,
            unlocked_achievements=unlocked_achievements,
            unlocked_technologies=unlocked_technologies,
            stats=GameStats(**stats_dict) if stats_dict else GameStats(),
            created_at=game_state.created_at,
            last_played=game_state.last_played,
            play_time_minutes=game_state.play_time_minutes,
            current_rank=current_rank,
            next_rank=next_rank,
            xp_for_next_level=xp_for_next,
        )

    def get_available_missions(self, completed_missions: list[str]) -> list[Mission]:
        """Get all available missions."""
        missions = []
        for mission_data in self.MISSIONS:
            is_completed = mission_data["id"] in completed_missions
            missions.append(
                Mission(
                    id=mission_data["id"],
                    title=mission_data["title"],
                    description=mission_data["description"],
                    module=mission_data["module"],
                    tema=mission_data["tema"],
                    xp_reward=mission_data["xp_reward"],
                    is_completed=is_completed,
                    is_available=True,
                )
            )
        return missions

    def get_achievements(self, unlocked_achievements: list[str]) -> list[Achievement]:
        """Get all achievements."""
        achievements = []
        for ach_data in self.ACHIEVEMENTS:
            is_unlocked = ach_data["key"] in unlocked_achievements
            achievements.append(
                Achievement(
                    key=ach_data["key"],
                    name=ach_data["name"],
                    description=ach_data["description"],
                    emoji=ach_data["emoji"],
                    is_unlocked=is_unlocked,
                )
            )
        return achievements

    def _get_rank_at_level(self, level: int) -> dict:
        """Get rank at specific level."""
        for i in range(len(self.RANKS) - 1, -1, -1):
            if level >= self.RANKS[i]["level"]:
                return self.RANKS[i]
        return self.RANKS[0]

    def _get_next_rank(self, level: int) -> dict | None:
        """Get next rank to unlock."""
        for rank in self.RANKS:
            if level < rank["level"]:
                return rank
        return None  # Max rank

    def _calculate_xp_for_next_level(self, level: int) -> int:
        """Calculate XP needed for next level."""
        if level >= len(self.XP_PER_LEVEL):
            return 999999  # Max level
        return self.XP_PER_LEVEL[level]
