from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

config = dotenv_values("./.env")
username = config.get("DB_USERNAME")
password = config.get("DB_PASSWORD")
dbname = config.get("DB_NAME")
db_port = config.get("DB_PORT")
db_host = config.get("DB_HOST")


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@{db_host}:{db_port}/{dbname}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)


async def init_db():
    from models.User import User
    from models.Todo import Todo

    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)
