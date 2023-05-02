from backend.database import async_session
from backend.services.TodoService import TodoService
from backend.services.UserService import UserService
from backend.services.UserTodoService import UserTodoService


async def get_todo_service():
    async with async_session() as session:
        async with session.begin():
            yield TodoService(session)


async def get_user_service():
    async with async_session() as session:
        async with session.begin():
            yield UserService(session)


async def get_user_todo_service():
    async with async_session() as session:
        async with session.begin():
            yield UserTodoService(session)
