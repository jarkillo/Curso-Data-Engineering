"""
Authentication service.
"""

from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister
from app.utils.jwt import create_access_token
from app.utils.password import hash_password, verify_password


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Created user

        Raises:
            HTTPException: If email or username already exists
        """
        # Check if email exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Check if username exists
        existing_username = (
            db.query(User).filter(User.username == user_data.username).first()
        )
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # Create new user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> User | None:
        """
        Authenticate a user with email and password.

        Args:
            db: Database session
            login_data: Login credentials

        Returns:
            User if authenticated, None otherwise
        """
        user = db.query(User).filter(User.email == login_data.email).first()

        if not user:
            return None

        if not verify_password(login_data.password, user.password_hash):
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        return user

    @staticmethod
    def create_user_token(user: User) -> str:
        """
        Create JWT token for user.

        Args:
            user: User to create token for

        Returns:
            JWT token
        """
        token_data = {"sub": str(user.id), "email": user.email}
        return create_access_token(token_data)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """
        Get user by ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User or None
        """
        return db.query(User).filter(User.id == user_id).first()
