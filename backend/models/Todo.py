import datetime

from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship
from typing import Optional

import sqlalchemy as sa

from models.User import User


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    todo_id: Optional[int] = Field(default=None, primary_key=True)
    label: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False))  # VARCHAR
    user_id: int = Field(
        sa_column=sa.Column(
            sa.Integer,
            sa.ForeignKey(User.user_id, ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )
    )

    created_at: datetime.datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.now()))

    user: User = Relationship(back_populates="todos", sa_relationship_kwargs={"lazy": "joined"})

    __table_args__ = (
        UniqueConstraint("label", "user_id", name="unique_todos_label_user_id"),
    )
