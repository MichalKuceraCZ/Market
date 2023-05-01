from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_session

from backend.services import UserService
from database import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


market_list = []


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/login")
async def login():
    return login


async def get_user_service():
    async with async_session() as session:
        async with session.begin():
            yield UserService(session)

include_router(user_router, prefix="/api/v1")