from pydantic import BaseModel


class ApiResponse(BaseModel):
    message: str
    data: dict | list | str | None
