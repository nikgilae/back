from sqlalchemy.ext.asyncio import AsyncSession
from schemas.comment import CommentCreate
from exceptions import TaskNotFound
import repositories.task as task_repo
import repositories.comment as comment_repo


async def get_all(db: AsyncSession, task_id: int, owner_id: int):
    task = await task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        raise TaskNotFound()
    return await comment_repo.get_all(db, task_id)


async def create(db: AsyncSession, data: CommentCreate, task_id: int, owner_id: int, author_id: int):
    task = await task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        raise TaskNotFound()
    return await comment_repo.create(db, data, task_id, author_id)