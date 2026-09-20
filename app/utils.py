from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException


def parse_object_id(post_id: str) -> ObjectId:
    try:
        return ObjectId(post_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID")
