from uuid import UUID

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(RegisterRequest): ...


class LoginResponse(BaseModel):
    token: str


class User(BaseModel):
    id: UUID
    username: str
    email: str


class RegisterResponse(BaseModel):
    message: str
