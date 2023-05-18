from fastapi import APIRouter

from fastapi import Body, HTTPException, status, Response, Depends, Query
from typing import Annotated

from deps import get_todo_service
from errors.ErrosResponse import ErrorResponse
from exceptions.TodoDuplicationException import TodoDuplicationException
from models.Todo import Todo
from request.CreateTodoRequest import CreateTodoRequest
from services.TodoService import TodoService


# http://localhost:8000/api/v1/todos

todo_router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


@todo_router.get("/", response_model=list[Todo])
async def get_todos(*,
                    todo_service: TodoService = Depends(get_todo_service),
                    page: Annotated[int, Query()],
                    limit: Annotated[int, Query()],
                    ):
    todos = await todo_service.get_todos(page, limit)
    return todos


# http://localhost:8000/todos/1


@todo_router.get("/{todo_id}")
async def get_todo(*,
                   todo_service: TodoService = Depends(get_todo_service),
                   todo_id: int):
    todo = await todo_service.get_todo(todo_id)
    return todo

    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail={
    #         "message": f"Todo [{todo_id}] not found",
    #         "code": "TODO_NOT_FOUND",
    #         "status_code": status.HTTP_404_NOT_FOUND,
    #     })


@todo_router.post("/", status_code=status.HTTP_201_CREATED, response_model=list[Todo],
                  responses={409: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def create_todo(*, todo_service: TodoService = Depends(get_todo_service),
                      new_todos: list[CreateTodoRequest] = Body()):
    try:
        new_todos = await todo_service.create_batch(new_todos)

        return new_todos
    except TodoDuplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": str(e),  # Email [tomas.svojanovsky11@gmail.com] already exists
                "code": "TODO_DUPLICATION_ERROR",
                "status_code": status.HTTP_409_CONFLICT,
            }
        )
    except Exception:  # fallback, to je kdyz na neco zapomenete
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Something went wrong",
                "code": "INTERNAL_SERVER",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )

    # return Response(status_code=status.HTTP_201_CREATED)


# [DELETE] http://localhost:8000/todos/1


@todo_router.delete("/{todo_id}")
async def delete_todo(
        *,
        todo_service: TodoService = Depends(get_todo_service),
        todo_id: int):
    await todo_service.delete_todo(todo_id)

    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail={
    #         "message": f"Todo [{todo_id}] not found",
    #         "code": "TODO_NOT_FOUND",
    #         "status_code": status.HTTP_404_NOT_FOUND,
    #     })


@todo_router.patch("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        *,
        new_todo: CreateTodoRequest = Body(),
        todo_service: TodoService = Depends(get_todo_service)):
    print("Toto je update")
    await todo_service.update_todo(new_todo)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # for todo in todos:
    #     if todo.id == new_todo.id:
    #         todo.label = new_todo.label
    #         return Response(status_code=status.HTTP_204_NO_CONTENT)

    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail={
    #         "message": f"Todo [{new_todo.id}] not found",
    #         "code": "TODO_NOT_FOUND",
    #         "status_code": status.HTTP_404_NOT_FOUND,
    #     })
