from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user

from app.core.database import get_db
from app.core.security import create_access_token

from app.models.refresh_token import RefreshToken
from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

from app.services.auth.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    auth_service = AuthService(db)

    try:

        user = auth_service.register_user(
            user_data
        )

        return user

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = AuthService.authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token_data = AuthService.create_tokens(
        db=db,
        user=user,
    )

    return TokenResponse(
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_type=token_data["token_type"],
    )

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):

    return current_user

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token
            == token_data.refresh_token
        )
        .first()
    )

    if not refresh_token:

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if refresh_token.is_revoked:

        raise HTTPException(
            status_code=401,
            detail="Refresh token has been revoked",
        )

    if refresh_token.expires_at < datetime.now(
        timezone.utc
    ):

        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired",
        )

    new_access_token = create_access_token(
        data={
            "sub": str(
                refresh_token.user_id
            )
        }
    )

    return {
        "access_token": new_access_token,
        "refresh_token": token_data.refresh_token,
        "token_type": "bearer",
    }

@router.post(
    "/logout",
)
def logout(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token
            == token_data.refresh_token
        )
        .first()
    )

    if refresh_token:

        refresh_token.is_revoked = True

        db.commit()

    return {
        "message": "Successfully logged out"
    }