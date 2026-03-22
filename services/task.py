from sqlalchemy.orm import Session
from schemas.tasks import TaskCreate, TaskUpdate
import repositories.task as task_repo


def get_all(db: Session, owner_id: int):
    return task_repo.get_all(db, owner_id)


def get_by_id(db: Session, task_id: int, owner_id: int):
    return task_repo.get_by_id(db, task_id, owner_id)


def create(db: Session, task: TaskCreate, owner_id: int):
    return task_repo.create(db, task, owner_id)


def update(db: Session, task_id: int, updated_data: TaskUpdate, owner_id: int):
    task = task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        return None
    return task_repo.update(db, task, updated_data)


def delete(db: Session, task_id: int, owner_id: int) -> bool:
    task = task_repo.get_by_id(db, task_id, owner_id)
    if task is None:
        return False
    task_repo.delete(db, task)
    return True