from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.session import get_db
from app.features.auth.dependencies import get_current_user
from app.features.tasks.schemas import CreateTask, UpdateTask, ReadTask
from app.features.tasks.service import (
    TaskService,
    TaskAlreadyExistError,
    TaskNotFound,
)

router = APIRouter(tags=["Tasks"], prefix="/tasks")


def get_task_service(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskService:
    return TaskService(db, current_user)


@router.post("", response_model=ReadTask)
async def create_task(
    payload: CreateTask,
    task_service: TaskService = Depends(get_task_service),
):
    try:
        return await task_service.create(payload)

    except TaskAlreadyExistError:
        raise HTTPException(status_code=400, detail="Task already exists")


@router.get("")
async def list_task(task_service: TaskService = Depends(get_task_service)):
    return await task_service.list()


@router.get("/{task_id}")
async def get_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service),
):
    try:
        return await task_service.get_by_id(task_id)

    except TaskNotFound:
        raise HTTPException(status_code=400, detail="Task not found")


@router.patch("/{task_id}")
async def update_task(
    task_id: UUID,
    payload: UpdateTask,
    task_service: TaskService = Depends(get_task_service),
):
    try:
        return await task_service.update(task_id, payload)

    except TaskNotFound:
        raise HTTPException(status_code=400, detail="Task not found")


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service),
):
    try:
        await task_service.delete(task_id)

    except TaskNotFound:
        raise HTTPException(status_code=400, detail="Task not found")
