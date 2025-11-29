"""
Schemas for authentication.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """User registration request."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str | None = None


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

    user_id: int | None = None
    email: str | None = None


class UserResponse(BaseModel):
    """User information response."""

    id: int
    email: str
    username: str
    full_name: str | None = None
    is_active: bool
    is_verified: bool
    tier: str
    created_at: datetime
    last_login: datetime | None = None

    class Config:
        from_attributes = True
