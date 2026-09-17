from enum import Enum
from pydantic import BaseModel, Field, field_validator


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"

class PostCreate(BaseModel):
    title: str
    body: str
    hashtags: list[str] = Field(default_factory="list")
    status: PostStatus = PostStatus.DRAFT
    author: str = "Brian Fox"



