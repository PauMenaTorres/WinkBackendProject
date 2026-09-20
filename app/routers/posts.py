from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Query
from pymongo import ReturnDocument

from app.database import posts_collection
from app.models import PostCreate, PostResponse, PostStatus

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=201, response_model=PostResponse)
def create_post(post: PostCreate):
    post_dict = post.model_dump()
    post_dict["author"] = "Brian Fox"
    post_dict["status"] = PostStatus.DRAFT.value
    post_dict["created_at"] = datetime.now(timezone.utc)

    result = posts_collection.insert_one(post_dict)

    post_dict["id"] = str(result.inserted_id)
    return post_dict


@router.get("/", response_model=list[PostResponse])
def get_posts(status: PostStatus | None = None):
    query = {}
    if status:
        query["status"] = status.value

    posts = []
    for doc in posts_collection.find(query):
        doc["id"] = str(doc["_id"])
        posts.append(doc)
    return posts


@router.delete("/{post_id}")
def delete_post(post_id: str):
    try:
        obj_id = ObjectId(post_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = posts_collection.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": f"Post with id {post_id} deleted"}