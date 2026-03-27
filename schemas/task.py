from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Заголовок должен быть не короче 3 символов")
        if len(value) > 100:
            raise ValueError("Заголовок должен быть не длиннее 100 символов")
        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Заголовок должен быть не короче 3 символов")
        if len(value) > 100:
            raise ValueError("Заголовок должен быть не длиннее 100 символов")
        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_done: bool

model_config = ConfigDict(from_attributes=True)