from datetime import datetime, timedelta

from dotenv import dotenv_values
from pydantic import BaseModel
from jose import jwt

ALGORITHM = "HS256"
config_data = dotenv_values("./.env")
SECRET_KEY = config_data.get("SECRET_KEY")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(Token):
    username: str


def create_access_token(data: dict):
    expire_time = 30

    expire = datetime.utcnow() + timedelta(minutes=expire_time)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
