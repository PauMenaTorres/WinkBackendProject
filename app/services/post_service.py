from datetime import datetime, timezone
from typing import Any

from app.core.exceptions import PostNotFoundException
from app.models import PostCreate, PostStatus
from app.repositories.base import PostRepository


class PostService:
    """Business logic service for Post management.
    
    Orchestrates business rules, invariants, and operations on posts
    independent of the underlying storage engine or web framework.
    """

    DEFAULT_AUTHOR = "Brian Fox"

    def __init__(self, repository: PostRepository) -> None:
        self.repository = repository

    def get_public_posts(self, hashtag: str | None = None) -> list[dict[str, Any]]:
        """Retrieve all published posts, optionally filtered by hashtag."""
        return self.repository.get_all(
            status=PostStatus.PUBLISHED.value,
            hashtag=hashtag,
        )

    def get_public_post_by_id(self, post_id: str) -> dict[str, Any]:
        """Retrieve a specific published post by ID.
        
        Raises PostNotFoundException if the post does not exist or is not published.
        """
        post = self.repository.get_by_id(post_id)
        if not post or post.get("status") != PostStatus.PUBLISHED.value:
            raise PostNotFoundException("Post not found or not published")
        return post

    def get_cms_posts(self, status: PostStatus | None = None, hashtag: str | None = None) -> list[dict[str, Any]]:
        """Retrieve all posts for CMS management with optional filters."""
        status_value = status.value if status else None
        return self.repository.get_all(status=status_value, hashtag=hashtag)

    def create_post(self, post_data: PostCreate) -> dict[str, Any]:
        """Create a new post enforcing business invariants:
        
        - Author is always Brian Fox
        - Default status is draft
        - Created at is set to current UTC timestamp
        """
        payload = post_data.model_dump()
        payload["author"] = self.DEFAULT_AUTHOR
        payload["status"] = PostStatus.DRAFT.value
        payload["created_at"] = datetime.now(timezone.utc)

        return self.repository.create(payload)

    def publish_post(self, post_id: str) -> dict[str, Any]:
        """Publish an existing post by changing its status to 'published'.
        
        Raises PostNotFoundException if post does not exist.
        """
        updated = self.repository.update_status(post_id, PostStatus.PUBLISHED.value)
        if not updated:
            raise PostNotFoundException("Post not found")
        return updated

    def delete_post(self, post_id: str) -> bool:
        """Delete a post by ID.
        
        Raises PostNotFoundException if post does not exist.
        """
        deleted = self.repository.delete(post_id)
        if not deleted:
            raise PostNotFoundException("Post not found")
        return True
