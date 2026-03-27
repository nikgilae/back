from sqlalchemy.orm import Session
from models.comment import Comment
from schemas.comment import CommentCreate


def get_all(db: Session, task_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.task_id == task_id).all()


def create(db: Session, data: CommentCreate, task_id: int, author_id: int) -> Comment:
    comment = Comment(
        content=data.content,
        task_id=task_id,
        author_id=author_id,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment