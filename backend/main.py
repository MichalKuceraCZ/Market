from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controllers.TodoControllers import todo_router
from controllers.UserController import user_router
from controllers.UserTodoControler import user_todo_router
from database import init_db
from errors.ErrorHandlers import register_error_handlers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def index():
    return {"status": "Api is running"}


app.include_router(todo_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(user_todo_router, prefix="/api/v1")

register_error_handlers(app)
