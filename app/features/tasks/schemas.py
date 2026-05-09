from uuid import UUID

from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    description: str
    user_id: UUID


class UpdateTask(BaseModel):
    title: str
    description: str
    user_id: UUID


class ReadTask(BaseModel):
    title: str
    description: str
    user_id: UUID
