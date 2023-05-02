from asyncpg import exceptions
from sqlalchemy import exc
from sqlmodel import Session

from backend.exceptions.TodoDuplicationException import TodoDuplicationException
from backend.models.Todo import Todo
from backend.response import CreateTodoRequest


class UserTodoService:
    def __init__(self, session: Session):
        self.session = session

    async def create_todo(self, user_id: int, data: CreateTodoRequest):
        try:
            new_todo = Todo(label=data.label, user_id=user_id)

            self.session.add(new_todo)
            await self.session.commit()

            return new_todo
        except (exc.IntegrityError, exceptions.UniqueViolationError):
            raise TodoDuplicationException(f"Todo [{data.label}] already exists")
        except Exception as e:
            raise Exception(e)
