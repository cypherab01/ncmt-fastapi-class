from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.features.tasks import service
from app.features.tasks.schemas import CreateTask, UpdateTask
from app.features.tasks.service import TaskService

router = APIRouter(tags=["Tasks"], prefix="/tasks")


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(db)


@router.post("")
async def create_task(
    payload: CreateTask, task_service: TaskService = Depends(get_task_service)
):
    return await task_service.create(payload)


@router.get("")
async def list_task(task_service: TaskService = Depends(get_task_service)):
    return await task_service.list()


@router.get("/{task_id}")
async def get_task(
    task_id: UUID, task_service: TaskService = Depends(get_task_service)
):
    return await task_service.get_by_id(task_id)


@router.patch("/{task_id}")
async def get_task(
    task_id: UUID,
    payload: UpdateTask,
    task_service: TaskService = Depends(get_task_service),
):
    return await task_service.update(task_id, payload)


@router.delete("/{task_id}")
async def get_task(
    task_id: UUID, task_service: TaskService = Depends(get_task_service)
):
    return await task_service.delete(task_id)


@router.get("/tasks/user/{user_id}")
async def get_task_by_user(
    user_id: UUID, task_service: TaskService = Depends(get_task_service)
):
    return await task_service.get_by_user_id(user_id)
