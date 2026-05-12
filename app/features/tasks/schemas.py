from uuid import UUID

from pydantic import BaseModel, Field


class CreateTask(BaseModel):
    title: str = Field(max_length=50, min_length=10)
    description: str


class UpdateTask(BaseModel):
    title: str
    description: str


class ReadTask(BaseModel):
    title: str
    description: str
    id: UUID
    user_id: UUID

    model_config = {"from_attributes": True}
