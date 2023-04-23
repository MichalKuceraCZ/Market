from sqlmodel import SQLModel, Field
import sqlalchemy as sa


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(default=None, primary_key=True)
    username: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False, unique=True))
