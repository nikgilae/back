from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from api.dependencies import get_current_user
from models.user import User
import services.task as task_service

router = APIRouter(prefix="/v1/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.create(db, task, current_user.id)


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.get_all(db, current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.get_by_id(db, task_id, current_user.id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_service.update(db, task_id, updated_data, current_user.id)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task_service.delete(db, task_id, current_user.id)