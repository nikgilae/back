from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.comment import Comment
from schemas.comment import CommentCreate


async def get_all(db: AsyncSession, task_id: int) -> list[Comment]:
    result = await db.execute(select(Comment).where(Comment.task_id == task_id))
    return result.scalars().all()


async def create(db: AsyncSession, data: CommentCreate, task_id: int, author_id: int) -> Comment:
    comment = Comment(
        content=data.content,
        task_id=task_id,
        author_id=author_id,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment