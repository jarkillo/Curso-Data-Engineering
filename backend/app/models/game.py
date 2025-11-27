"""
Game state model for progress tracking.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class GameState(Base):
    """Game state model for tracking player progress."""

    __tablename__ = "game_states"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Player info
    player_name = Column(String(50), nullable=False)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    total_xp_earned = Column(Integer, default=0)

    # Progress
    current_module = Column(Integer, default=1)
    current_tema = Column(Integer, default=1)

    # JSON stored as text (SQLite compatible)
    completed_missions = Column(Text, default="[]")  # JSON array
    unlocked_achievements = Column(Text, default="[]")  # JSON array
    unlocked_technologies = Column(Text, default="[]")  # JSON array

    # Stats stored as JSON
    stats = Column(Text, default="{}")  # JSON object

    # Time tracking
    play_time_minutes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_played = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", backref="game_state")
