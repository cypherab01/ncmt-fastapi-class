import uuid
from uuid import UUID as PyUUID

from sqlalchemy import text, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base
from app.db.mixin_id import MixinID


class User(Base, MixinID):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    password: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )


class Task(Base, MixinID):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
