from fastapi import APIRouter, Depends, HTTPException, status

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
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = await auth_service.authorize(data)

    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return LoginResponse(
        token=token.token,
    )
