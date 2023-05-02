from pydantic import BaseModel


class ErrorResponse(BaseModel):
    messages: str
    code: str
    status_code: int
