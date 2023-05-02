from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from backend.controllers.TodoControllers import todo_router
from backend.controllers.UserController import user_router
from backend.errors.ErrorHandlers import register_error_handlers
from database import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


class Todo(BaseModel):
    id: Optional[int]
    label: str


todos = []


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/login")
async def login():
    return login

app.include_router(todo_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(user_todo_router, prefix="/api/v1")

register_error_handlers(app)