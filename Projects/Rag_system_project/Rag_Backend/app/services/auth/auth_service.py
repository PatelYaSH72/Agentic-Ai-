from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from datetime import datetime, timedelta, timezone
from app.models.refresh_token import RefreshToken
from app.core.config import settings
from app.core.security import create_access_token


class AuthService:

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
    ) -> User | None:

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        if not user.is_active:
            return None

        return user

    @staticmethod
    def create_tokens(
        db: Session,
        user: User,
    ) -> dict:

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        refresh_token = create_refresh_token()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def __init__(self, db: Session):
        self.db = db

        self.user_repository = UserRepository(db)

    def register_user(
        self,
        user_data: UserCreate,
    ) -> User:

        existing_user = (
            self.user_repository.get_by_email(
                user_data.email
            )
        )

        if existing_user:

            raise ValueError(
                "Email is already registered"
            )

        hashed_password = hash_password(
            user_data.password
        )

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hashed_password,
        )

        return self.user_repository.create(
            new_user
        )

    

    def login_user(
            self,
            email: str,
            password: str,
            
        ) -> dict:
           

            user = self.user_repository.get_by_email(
                email
            )

            if not user:

                raise ValueError(
                    "Invalid email or password"
                )

            is_password_valid = verify_password(
                password,
                user.password_hash,
            )

            if not is_password_valid:

                raise ValueError(
                    "Invalid email or password"
                )

            access_token = create_access_token(
                data={
                    "sub": str(user.id)
                }
            )

            refresh_token = create_refresh_token()

            refresh_token_record = RefreshToken(
                token=refresh_token,
                user_id=user.id,
                expires_at=(
                    datetime.now(timezone.utc)
                    + timedelta(
                        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
                    )
                ),
            )

            self.db.add(refresh_token_record)
            self.db.commit()

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token_value: str,
    ) -> str:

        refresh_token = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token == refresh_token_value,
                RefreshToken.is_revoked == False,
            )
            .first()
        )

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        if refresh_token.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired",
            )

        access_token = create_access_token(
            data={
                "sub": str(refresh_token.user_id)
            }
        )

        return access_token

    @staticmethod
    def revoke_refresh_token(
        db: Session,
        refresh_token_value: str,
    ):
        refresh_token = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token == refresh_token_value,
                RefreshToken.is_revoked == False,
            )
            .first()
        )

        if refresh_token:
            refresh_token.is_revoked = True
            db.commit()