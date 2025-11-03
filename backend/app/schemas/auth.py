"""
Schemas for authentication.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """User registration request."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login request."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data encoded in JWT token."""

    user_id: Optional[int] = None
    email: Optional[str] = None


class UserResponse(BaseModel):
    """User information response."""

    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    tier: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
