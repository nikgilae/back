from fastapi import Request
from fastapi.responses import JSONResponse


class TaskNotFound(Exception):
    pass


class CommentNotFound(Exception):
    pass


async def task_not_found_handler(request: Request, exc: TaskNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "TASK_NOT_FOUND", "message": "Задача не найдена"}},
    )


async def comment_not_found_handler(request: Request, exc: CommentNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "COMMENT_NOT_FOUND", "message": "Комментарий не найден"}},
    )