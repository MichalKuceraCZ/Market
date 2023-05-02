

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from backend.exceptions import TodoDuplicationException
from backend.response import CreateTodoRequest, GetByUsernameResponse
from backend.services import UserTodoService
from backend.services.UserDatabaseService import get_user_todo_service

user_todo_router = APIRouter(
    prefix="/users/todos",
    tags=["User todos"],
)


@user_todo_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(*,
                      todo: CreateTodoRequest = Body(),
                      user_todo_service: UserTodoService = Depends(get_user_todo_service),
                      current_user: GetByUsernameResponse = Depends(get_current_user),
                      ):
    try:
        new_todo = await user_todo_service.create_todo(current_user.user_id, todo)
        return new_todo
    except TodoDuplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": str(e),
                "code": "TODO_DUPLICATION_ERROR",
                "status_code": status.HTTP_409_CONFLICT,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Something went wrong",
                "code": "INTERNAL_SERVER",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )
