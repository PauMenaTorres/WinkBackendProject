from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class PostCreate(BaseModel):
    title: str
    body: str
    hashtags: list[str] = Field(default_factory=list)


class PostResponse(BaseModel):
    id: str
    title: str
    body: str
    hashtags: list[str]
    status: PostStatus
    author: str
    created_at: datetime
