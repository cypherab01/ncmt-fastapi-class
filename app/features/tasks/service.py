from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Task, User
from app.features.tasks.schemas import CreateTask, UpdateTask


class TaskAlreadyExistError(Exception): ...


class TaskNotFound(Exception): ...


class TaskService:
    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.current_user = current_user

    async def create(self, payload: CreateTask) -> Task:
        stmt = select(Task).where(Task.title == payload.title)
        result = await self.db.execute(stmt)
        existing_task = result.scalar_one_or_none()

        if existing_task is not None:
            raise TaskAlreadyExistError()

        task = Task(**payload.model_dump(), user_id=self.current_user.id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_by_id(self, task_id: UUID) -> Task:
        stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == self.current_user.id,
        )
        result = await self.db.execute(stmt)
        data = result.scalar_one_or_none()

        if data is None:
            raise TaskNotFound()

        return data

    async def list(self):
        stmt = select(Task).where(Task.user_id == self.current_user.id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, task_id: UUID, payload: UpdateTask) -> Task:
        task = await self.get_by_id(task_id)

        data = payload.model_dump(exclude_unset=True)

        stmt = (
            update(Task)
            .where(
                Task.id == task_id,
                Task.user_id == self.current_user.id,
            )
            .values(**data)
            .returning(Task)
        )
        await self.db.execute(stmt)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task_id: UUID) -> None:
        task = await self.get_by_id(task_id)
        await self.db.delete(task)
        await self.db.commit()
