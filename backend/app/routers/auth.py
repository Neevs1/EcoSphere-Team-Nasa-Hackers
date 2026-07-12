from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.security import (
    verify_password,
    create_access_token,
)
from app.database.db import get_db
from app.models.user import User
from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    UserResponse,
)


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login with email and password",
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    stmt = select(User).where(
        User.email == payload.email
    )
    user = db.scalars(stmt).first()

    if user is None or not verify_password(
        payload.password, user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive.",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
        }
    )

    return LoginResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@auth_router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user info",
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return UserResponse.model_validate(
        current_user
    )
