from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo import ReturnDocument

from app.database import posts_collection
from app.dependencies import verify_admin_token
from app.models import PostCreate, PostResponse, PostStatus

router = APIRouter(prefix="/posts", tags=["Posts"])


def parse_object_id(post_id: str) -> ObjectId:
    try:
        return ObjectId(post_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID")


@router.post("/", status_code=201, response_model=PostResponse, dependencies=[Depends(verify_admin_token)])
def create_post(post: PostCreate):
    post_dict = post.model_dump()
    post_dict["author"] = "Brian Fox"
    post_dict["status"] = PostStatus.DRAFT.value
    post_dict["created_at"] = datetime.now(timezone.utc)

    result = posts_collection.insert_one(post_dict)

    post_dict["id"] = str(result.inserted_id)
    return post_dict


@router.get("/", response_model=list[PostResponse])
def get_posts(status: PostStatus | None = None, hashtag: str | None = None):

    query = {}
    if status:
        query["status"] = status.value
    if hashtag:
        query["hashtags"] = hashtag

    posts = []
    for doc in posts_collection.find(query):
        doc["id"] = str(doc["_id"])
        posts.append(doc)
    return posts


@router.get("/{post_id}", response_model=PostResponse)
def get_post_by_id(post_id: str):
    obj_id = parse_object_id(post_id)

    post = posts_collection.find_one({"_id": obj_id})
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post["id"] = str(post["_id"])
    return post


@router.patch("/{post_id}/publish", response_model=PostResponse, dependencies=[Depends(verify_admin_token)])
def publish_post(post_id: str):
    obj_id = parse_object_id(post_id)

    updated_doc = posts_collection.find_one_and_update(
        {"_id": obj_id},
        {"$set": {"status": PostStatus.PUBLISHED.value}},
        return_document=ReturnDocument.AFTER,
    )

    if not updated_doc:
        raise HTTPException(status_code=404, detail="Post not found")

    updated_doc["id"] = str(updated_doc["_id"])
    return updated_doc


@router.delete("/{post_id}", dependencies=[Depends(verify_admin_token)])
def delete_post(post_id: str):
    obj_id = parse_object_id(post_id)

    result = posts_collection.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": f"Post with id {post_id} deleted"}