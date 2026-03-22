from sqlalchemy.orm import Session
from models.task import Task
from schemas.tasks import TaskCreate, TaskUpdate


def get_all(db: Session, owner_id: int) -> list[Task]:
    return db.query(Task).filter(Task.owner_id == owner_id).all()


def get_by_id(db: Session, task_id: int, owner_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def create(db: Session, task: TaskCreate, owner_id: int) -> Task:
    new_task = Task(
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        owner_id=owner_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update(db: Session, task: Task, updated_data: TaskUpdate) -> Task:
    changes = updated_data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()