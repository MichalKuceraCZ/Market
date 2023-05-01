from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    birthdate: str  # 1991-01-01
    username: str
    password: str
