from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task import TaskCreate, TaskUpdate
from exceptions import TaskNotFound
import repositories.task as task_repo


async def get_all(db: AsyncSession, owner_id: int):
    return await task_repo.get_all(db, owner_id)


async def get_by_id(db: AsyncSession, task_id: int, owner_id: int):
    task = await task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        raise TaskNotFound()
    return task


async def create(db: AsyncSession, task: TaskCreate, owner_id: int):
    return await task_repo.create(db, task, owner_id)


async def update(db: AsyncSession, task_id: int, updated_data: TaskUpdate, owner_id: int):
    task = await task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        raise TaskNotFound()
    return await task_repo.update(db, task, updated_data)


async def delete(db: AsyncSession, task_id: int, owner_id: int) -> None:
    task = await task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        raise TaskNotFound()
    await task_repo.delete(db, task)