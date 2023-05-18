from pydantic import BaseModel


class TodoCreateRequest(BaseModel):
    todo_id: int
    label: str
