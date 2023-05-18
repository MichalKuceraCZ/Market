from fastapi import APIRouter, status, Body, Depends, HTTPException

from auth.user import get_current_user
from deps import get_user_todo_service
from exceptions.TodoDuplicationException import TodoDuplicationException
from request.CreateTodoRequest import CreateTodoRequest
from response.GetByUsernameResponse import GetByUsernameResponse
from services.UserTodoService import UserTodoService

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
