from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status
from starlette.responses import Response

from backend.main import get_user_service
from backend.request import UserCreateRequest, LoginRequest
from backend.services import UserService

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
        await user_service.login(data)

        return Response(status_code=status.HTTP_200_OK)

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
