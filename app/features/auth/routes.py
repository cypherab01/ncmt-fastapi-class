from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.core.config import settings
from app.features.auth.dependencies import get_auth_service
from app.features.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)
from app.features.auth.service import (
    AuthService,
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
)

router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        await auth_service.register(data)

    except UsernameAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    return RegisterResponse(
        message="User created successfully",
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    data: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = await auth_service.authorize(data)

    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # ✅ Set cookie here
    response.set_cookie(
        key="access_token",
        value=token.token,
        httponly=True,
        secure=True,  # use True in production (HTTPS)
        samesite="lax",  # "strict" if you want tighter security
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # match your JWT expiry
    )

    return LoginResponse(
        token=token.token,
    )
