from pydantic import BaseModel, field_validator, ConfigDict


class CommentCreate(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 1:
            raise ValueError("Комментарий не может быть пустым")
        if len(value) > 500:
            raise ValueError("Комментарий не может быть длиннее 500 символов")
        return value


class CommentResponse(BaseModel):
    id: int
    content: str
    task_id: int
    author_id: int

model_config = ConfigDict(from_attributes=True)