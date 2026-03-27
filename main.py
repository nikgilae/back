from fastapi import FastAPI
from database import engine, Base
from api.router import router as tasks_router
from api.auth import router as auth_router
from api.comments import router as comments_router
from exceptions import TaskNotFound, CommentNotFound, task_not_found_handler, comment_not_found_handler

import models.user
import models.task
import models.comment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(TaskNotFound, task_not_found_handler)
app.add_exception_handler(CommentNotFound, comment_not_found_handler)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(comments_router)


@app.get("/")
def root():
    return {"message": "Todo API работает"}