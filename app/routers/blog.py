from fastapi import APIRouter, Depends

from app.dependencies import get_post_service
from app.models import PostResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/blog/posts", tags=["Blog"])


@router.get("/", response_model=list[PostResponse])
def get_public_posts(
    hashtag: str | None = None,
    service: PostService = Depends(get_post_service),
):
    """Retrieve all published posts, optionally filtered by hashtag."""
    return service.get_public_posts(hashtag=hashtag)


@router.get("/{post_id}", response_model=PostResponse)
def get_public_post_by_id(
    post_id: str,
    service: PostService = Depends(get_post_service),
):
    """Retrieve a single published post by ID."""
    return service.get_public_post_by_id(post_id=post_id)
