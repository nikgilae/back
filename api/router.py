from fastapi import APIRouter, HTTPException
from typing import List

from schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
import services.task as task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    return task_service.create_task(task)


@router.get("/", response_model=List[TaskResponse])
def get_all_tasks():
    return task_service.get_all_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = task_service.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_data: TaskUpdate):
    task = task_service.update_task(task_id, updated_data)

    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Задача не найдена")