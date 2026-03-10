from fastapi import FastAPI
from api.router import router as tasks_router

app = FastAPI()

app.include_router(tasks_router)


@app.get("/")
def root():
    return {"message": "Todo API работает"}