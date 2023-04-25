from sqlmodel import SQLModel, Field

import sqlalchemy as sa


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(sa_column=sa.Column(sa.TEXT, nullable=False, unique=True))
