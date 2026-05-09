from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.token import IssuedToken, create_access_token
from app.db.models import User
from app.features.auth.schemas import RegisterRequest, LoginRequest


class UsernameAlreadyExistsException(Exception): ...


class InvalidCredentialsException(Exception): ...


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: RegisterRequest) -> User:
        existing_user = await self._get_by_username(username=data.username)

        if existing_user:
            raise UsernameAlreadyExistsException()

        user = User(
            username=data.username,
            password=data.password,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authorize(self, data: LoginRequest) -> IssuedToken:
        existing_user = await self._get_by_username(username=data.username)

        if not existing_user:
            raise InvalidCredentialsException()

        if existing_user.password != data.password:
            raise InvalidCredentialsException()

        issued = create_access_token(
            user_id=existing_user.id,
            username=existing_user.username,
        )

        return IssuedToken(token=issued.token)

    async def _get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
