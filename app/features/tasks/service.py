from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.tasks.schemas import CreateTask, UpdateTask
from app.db.models import Task
from sqlalchemy import select

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: CreateTask):
        task = Task(title=payload.title, description=payload.description)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_by_id(self, task_id: UUID) -> Task | None:
        stmt =  select(Task).where(Task.id == task_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self):
        stmt  = select(Task)
        result = await self.db.execute(stmt)
        return result.scalars().all()



    async def update(self, task_id: UUID, payload: UpdateTask):
        task = await self.get_by_id(task_id)
        if not task:
            return None

        task.title = payload.title
        task.description = payload.description

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task_id: UUID) -> bool:
        task = await self.get_by_id(task_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True
