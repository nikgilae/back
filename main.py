from fastapi import FastAPI
from database import engine, Base
from api.router import router as tasks_router
from api.auth import router as auth_router

import models.user
import models.task

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Todo API работает"}