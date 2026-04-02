from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate


async def get_all(db: AsyncSession, owner_id: int) -> list[Task]:
    result = await db.execute(select(Task).where(Task.owner_id == owner_id))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, task_id: int, owner_id: int) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, task: TaskCreate, owner_id: int) -> Task:
    new_task = Task(
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        owner_id=owner_id,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def update(db: AsyncSession, task: Task, updated_data: TaskUpdate) -> Task:
    changes = updated_data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task


async def delete(db: AsyncSession, task: Task) -> None:
    await db.delete(task)
    await db.commit()