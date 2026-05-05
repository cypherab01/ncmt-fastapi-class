import uuid
from uuid import UUID as PyUUID

from sqlalchemy import text, String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )


