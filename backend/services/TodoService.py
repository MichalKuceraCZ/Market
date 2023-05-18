from sqlmodel import Session, select, delete, update
from sqlalchemy import exc
import asyncpg

from exceptions.TodoDuplicationException import TodoDuplicationException
from models.Todo import Todo
from request.CreateTodoRequest import CreateTodoRequest


class TodoService:
    def __init__(self, session: Session):
        self.session = session

    async def create_batch(self, data: list[CreateTodoRequest]):
        # self.session.begin()
        # for item in data:
        #     self.create_todo(item)
        try:
            new_todos = []
            for item in data:
                new_todos.append(Todo(label=item.label))

            self.session.add_all(new_todos)
            await self.session.commit()

            return new_todos
        except (exc.IntegrityError, asyncpg.exceptions.UniqueViolationError) as e:
            raise TodoDuplicationException("Todo already exists")

    async def create_todo(self, data: CreateTodoRequest):
        new_todo = Todo(label=data.label)

        self.session.add(new_todo)
        await self.session.commit()

        return new_todo

    async def get_todos(self, page: int, limit: int):
        query = (
            select(Todo)
            .limit(limit)
            .offset(page * limit)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_todo(self, todo_id: int):
        # first, one, scalar
        query = (
            select(Todo)
            .where(Todo.todo_id == todo_id)
        )

        result = await self.session.execute(query)
        return result.one()

    async def delete_todo(self, todo_id: int):
        query = (
            delete(Todo)
            .where(Todo.todo_id == todo_id)
        )

        await self.session.execute(query)
        await self.session.commit()

    async def update_todo(self, todo: CreateTodoRequest):
        query = (
            update(Todo)
            .values(label=todo.label)
            .where(Todo.todo_id == todo.todo_id)
        )

        await self.session.execute(query)
        await self.session.commit()

        # todo = Todo() # epic query ktere mi to ziska
        # todo.label = todo.label
# micro task Queue
# setTimeout, Promise
