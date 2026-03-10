from schemas.tasks import TaskCreate, TaskUpdate

tasks_db: dict[int, dict] = {}
next_id: int = 1


def create_task(task: TaskCreate) -> dict:
    global next_id

    new_task = {
        "id": next_id,
        "title": task.title,
        "description": task.description,
        "is_done": task.is_done,
    }

    tasks_db[next_id] = new_task
    next_id += 1

    return new_task


def get_all_tasks() -> list:
    return list(tasks_db.values())


def get_task_by_id(task_id: int) -> dict | None:
    return tasks_db.get(task_id)


def update_task(task_id: int, updated_data: TaskUpdate) -> dict | None:
    task = tasks_db.get(task_id)

    if task is None:
        return None

    changes = updated_data.model_dump(exclude_unset=True)
    task.update(changes)

    return task


def delete_task(task_id: int) -> bool:
    task = tasks_db.get(task_id)

    if task is None:
        return False

    del tasks_db[task_id]
    return True