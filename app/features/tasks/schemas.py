from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    description: str

class UpdateTask(BaseModel):
    title: str
    description: str

class ReadTask(BaseModel):
    title: str
    description: str
