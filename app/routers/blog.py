from fastapi import APIRouter, HTTPException

from app.database import posts_collection
from app.models import PostResponse, PostStatus
from app.utils import parse_object_id

router = APIRouter(prefix="/blog/posts", tags=["Blog"])


@router.get("/", response_model=list[PostResponse])
def get_public_posts(hashtag: str | None = None):
    query = {"status": PostStatus.PUBLISHED.value}
    if hashtag:
        query["hashtags"] = hashtag

    posts = []
    for doc in posts_collection.find(query).sort("created_at", -1):
        doc["id"] = str(doc["_id"])
        posts.append(doc)
    return posts


@router.get("/{post_id}", response_model=PostResponse)
def get_public_post_by_id(post_id: str):
    obj_id = parse_object_id(post_id)

    post = posts_collection.find_one({"_id": obj_id, "status": PostStatus.PUBLISHED.value})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not published")
    post["id"] = str(post["_id"])
    return post
