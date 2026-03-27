from sqlalchemy.orm import Session
from schemas.comment import CommentCreate
from exceptions import TaskNotFound
import repositories.task as task_repo
import repositories.comment as comment_repo


def get_all(db: Session, task_id: int, owner_id: int):
    task = task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        raise TaskNotFound()
    return comment_repo.get_all(db, task_id)


def create(db: Session, data: CommentCreate, task_id: int, owner_id: int, author_id: int):
    task = task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        raise TaskNotFound()
    return comment_repo.create(db, data, task_id, author_id)