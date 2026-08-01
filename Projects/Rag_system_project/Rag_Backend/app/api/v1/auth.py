from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
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


# ============================================================
# REGISTER
# ============================================================

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


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = AuthService.authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
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

# ============================================================
# CURRENT USER
# ============================================================

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


# ============================================================
# REFRESH ACCESS TOKEN
# ============================================================

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    access_token = AuthService.refresh_access_token(
        db=db,
        refresh_token_value=token_data.refresh_token,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ============================================================
# LOGOUT
# ============================================================

@router.post(
    "/logout",
)
def logout(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    AuthService.revoke_refresh_token(
        db=db,
        refresh_token_value=token_data.refresh_token,
    )

    return {
        "message": "Successfully logged out"
    }