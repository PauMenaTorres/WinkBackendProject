from typing import Any
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from pymongo.collection import Collection

from app.core.exceptions import InvalidIdException
from app.repositories.base import PostRepository


class MongoPostRepository(PostRepository):
    """MongoDB implementation of PostRepository"""

    def __init__(self, collection: Collection) -> None:
        self.collection = collection

    def _to_object_id(self, post_id: str) -> ObjectId:
        try:
            return ObjectId(post_id)
        except InvalidId:
            raise InvalidIdException("Invalid ID")

    def get_all(self, status: str | None = None, hashtag: str | None = None) -> list[dict[str, Any]]:
        query: dict[str, Any] = {}
        if status is not None:
            query["status"] = status
        if hashtag is not None:
            query["hashtags"] = hashtag

        posts: list[dict[str, Any]] = []
        for doc in self.collection.find(query).sort("created_at", -1):
            doc["id"] = str(doc["_id"])
            posts.append(doc)
        return posts

    def get_by_id(self, post_id: str) -> dict[str, Any] | None:
        obj_id = self._to_object_id(post_id)
        doc = self.collection.find_one({"_id": obj_id})
        if doc is not None:
            doc["id"] = str(doc["_id"])
        return doc

    def create(self, post_data: dict[str, Any]) -> dict[str, Any]:
        result = self.collection.insert_one(post_data)
        post_data["id"] = str(result.inserted_id)
        return post_data

    def update_status(self, post_id: str, status: str) -> dict[str, Any] | None:
        obj_id = self._to_object_id(post_id)
        updated_doc = self.collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": {"status": status}},
            return_document=ReturnDocument.AFTER,
        )
        if updated_doc is not None:
            updated_doc["id"] = str(updated_doc["_id"])
        return updated_doc

    def delete(self, post_id: str) -> bool:
        obj_id = self._to_object_id(post_id)
        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0
