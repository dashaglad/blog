from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class PostCreateRequest(BaseModel):
    title: str = Field(max_length=255)
    content: str


class PostUpdateRequest(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    content: str | None = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
