from fastapi import APIRouter, Depends, status

from app.dependencies import get_post_service, verify_admin_token
from app.models import PostCreate, PostResponse, PostStatus
from app.services.post_service import PostService

router = APIRouter(prefix="/cms/posts",
    tags=["Content Management System"],
    dependencies=[Depends(verify_admin_token)],
)


@router.get("/", response_model=list[PostResponse])
def get_all_posts_cms(
    status: PostStatus | None = None,
    hashtag: str | None = None,
    service: PostService = Depends(get_post_service),
):
    """List all posts for CMS management, with optional status and hashtag filters."""
    return service.get_cms_posts(status=status, hashtag=hashtag)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: PostCreate,
    service: PostService = Depends(get_post_service),
):
    """Create a new post in draft status with Brian Fox as default author."""
    return service.create_post(post_data=post)


@router.patch("/{post_id}/publish", response_model=PostResponse)
def publish_post(
    post_id: str,
    service: PostService = Depends(get_post_service),
):
    """Publish an existing post by ID."""
    return service.publish_post(post_id=post_id)


@router.delete("/{post_id}")
def delete_post(
    post_id: str,
    service: PostService = Depends(get_post_service),
):
    """Delete a post by ID."""
    service.delete_post(post_id=post_id)
    return {"message": f"Post with id {post_id} deleted"}
