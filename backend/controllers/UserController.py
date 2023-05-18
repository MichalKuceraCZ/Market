from fastapi import APIRouter, status, Body, Depends, Response, HTTPException
import json

from auth.token import create_access_token
from auth.user import get_current_user
from deps import get_user_service
from errors.ErrosResponse import ErrorResponse
from exceptions.UserNotFoundException import UserNotFoundException
from request.ChangePasswordRequest import ChangePasswordRequest
from request.LoginRequest import LoginRequest
from request.UserCreateRequest import UserCreateRequest
from controllers.request_example import change_password_examples
from response.GetByUsernameResponse import GetByUsernameResponse
from services.UserService import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(*,
                      data: UserCreateRequest = Body(),
                      user_service: UserService = Depends(get_user_service),
                      ):
    new_user = await user_service.create_user(data)
    return new_user


@user_router.post("/login")
async def login_user(*,
                     data: LoginRequest = Body(),
                     user_service: UserService = Depends(get_user_service),
                     ):
    try:
        user = await user_service.login(data)

        access_token = create_access_token(data={"sub": user.username})

        return Response(status_code=status.HTTP_200_OK, content=json.dumps({
            "access_token": access_token, "token_type": "bearer"
        }))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Something went wrong",
                "code": "INTERNAL_SERVER",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )


# http://localhost:8080/api/v1/users/password
# http://localhost:8080/api/v1/users/{user_id}/todos


@user_router.patch("/password", status_code=status.HTTP_204_NO_CONTENT,
                   responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
                   )
async def change_password(*,
                          data: ChangePasswordRequest = Body(..., examples=change_password_examples),
                          user_service: UserService = Depends(get_user_service),
                          current_user: GetByUsernameResponse = Depends(get_current_user),
                          ):
    try:
        await user_service.change_password(current_user, data)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": str(e),
                "code": "INVALID_PASSWORD",
                "status_code": status.HTTP_400_BAD_REQUEST,
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
