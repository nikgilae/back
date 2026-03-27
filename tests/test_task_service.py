import pytest
from unittest.mock import MagicMock
from schemas.task import TaskCreate
from exceptions import TaskNotFound
import services.task as task_service


def test_create_task():
    mock_db = MagicMock()
    mock_task = {"id": 1, "title": "Тест", "description": None, "is_done": False, "owner_id": 1}

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("repositories.task.create", lambda db, task, owner_id: mock_task)
        result = task_service.create(mock_db, TaskCreate(title="Тест"), owner_id=1)
        assert result["title"] == "Тест"


def test_get_by_id_not_found():
    mock_db = MagicMock()

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("repositories.task.get_by_id", lambda db, task_id, owner_id: None)
        with pytest.raises(TaskNotFound):
            task_service.get_by_id(mock_db, task_id=999, owner_id=1)