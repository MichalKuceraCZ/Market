import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

import sqlalchemy as sa


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False))
    last_name: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False))
    birthdate: datetime.date = Field(sa_column=sa.Column(sa.Date, nullable=False))

    username: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False, unique=True))
    email: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False, unique=True))

    created_at: datetime.datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), default=sa.func.now()))

    passwords: list["UserPassword"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "joined"})
    todos: list["Todo"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "joined"})
