from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api.router import router as tasks_router
from api.auth import router as auth_router
from api.comments import router as comments_router
from api.upload import router as upload_router
from api.system import router as system_router
from exceptions import TaskNotFound, CommentNotFound, task_not_found_handler, comment_not_found_handler

import models.user
import models.task
import models.comment


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(TaskNotFound, task_not_found_handler)
app.add_exception_handler(CommentNotFound, comment_not_found_handler)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(comments_router)
app.include_router(upload_router)
app.include_router(system_router)


@app.get("/")
async def root():
    return {"message": "Todo API работает"}