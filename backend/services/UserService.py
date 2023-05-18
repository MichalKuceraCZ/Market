import datetime

from sqlmodel import Session, select

from auth.password import hash_password, verify_password
from exceptions.UserNotFoundException import UserNotFoundException
from models.User import User
from models.UserPassword import UserPassword
from request.ChangePasswordRequest import ChangePasswordRequest
from request.LoginRequest import LoginRequest
from request.UserCreateRequest import UserCreateRequest
from response.GetByUsernameResponse import GetByUsernameResponse


class UserService:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, data: UserCreateRequest):
        try:
            new_user = User(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                birthdate=data.birthdate,
                username=data.username,
                passwords=[UserPassword(value=hash_password(data.password))],
            )

            self.session.add(new_user)
            await self.session.commit()

            return new_user
        except Exception as e:
            raise Exception(e)

    async def login(self, data: LoginRequest):
        user = await self.get_by_username(data.username)

        if user is None:
            raise UserNotFoundException("Username or password is invalid")

        if not verify_password(data.password, user.password):
            raise UserNotFoundException("Username or password is invalid")

        return user

    async def get_by_username(self, username: str) -> GetByUsernameResponse:
        query = (
            select(User.user_id, User.username, User.email, UserPassword.value.label("password"))
            .join(UserPassword)
            .where(User.username == username)
            .limit(1)
        )

        result = await self.session.execute(query)
        return result.first()

    async def change_password(self, user: GetByUsernameResponse, data: ChangePasswordRequest):
        if not verify_password(data.old_password, user.password):
            raise UserNotFoundException("Password is invalid")

        query = (
            select(UserPassword)
            .where(UserPassword.user_id == user.user_id)
            .limit(1)
        )

        password_data = await self.session.execute(query)
        user_password: UserPassword = password_data.scalars().first()

        user_password.value = hash_password(data.new_password)
        user_password.updated_at = datetime.datetime.now()

        await self.session.commit()

        # query = (

        #     update(UserPassword)
        #     .values(value=hash_password(data.new_password), updated_at=datetime.datetime.now())
        #     .where(UserPassword.user_id == user.user_id)
        # )
        #
        # await self.session.execute(query)
