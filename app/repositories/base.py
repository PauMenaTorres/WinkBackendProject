from abc import ABC, abstractmethod
from typing import Any


class PostRepository(ABC):
    """Abstract interface for Post persistence operations."""

    @abstractmethod
    def get_all(self, status: str | None = None, hashtag: str | None = None) -> list[dict[str, Any]]:
        """Retrieve all posts matching the optional status and hashtag filters."""
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> dict[str, Any] | None:
        """Retrieve a single post by its ID."""
        pass

    @abstractmethod
    def create(self, post_data: dict[str, Any]) -> dict[str, Any]:
        """Persist a new post and return the saved document with its string id."""
        pass

    @abstractmethod
    def update_status(self, post_id: str, status: str) -> dict[str, Any] | None:
        """Update the status of a post and return the updated document if found."""
        pass

    @abstractmethod
    def delete(self, post_id: str) -> bool:
        """Delete a post by ID. Return True if deleted, False if not found."""
        pass
