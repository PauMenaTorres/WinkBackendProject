from typing import Any
import pytest
from fastapi.testclient import TestClient
from app.core.exceptions import PostNotFoundException
from app.dependencies import ADMIN_TOKEN, get_post_repository
from app.main import app
from app.models import PostCreate, PostStatus
from app.repositories.base import PostRepository
from app.services.post_service import PostService



class FakePostRepository(PostRepository):
    def __init__(self) -> None:
        self.posts: dict[str, dict[str, Any]] = {}
        self._next_id = 1

    def get_all(self, status: str | None = None, hashtag: str | None = None) -> list[dict[str, Any]]:
        results = list(self.posts.values())
        if status is not None:
            results = [p for p in results if p.get("status") == status]
        if hashtag is not None:
            results = [p for p in results if hashtag in p.get("hashtags", [])]
        return results

    def get_by_id(self, post_id: str) -> dict[str, Any] | None:
        return self.posts.get(post_id)

    def create(self, post_data: dict[str, Any]) -> dict[str, Any]:
        post_id = str(self._next_id)
        self._next_id += 1
        saved = {**post_data, "id": post_id}
        self.posts[post_id] = saved
        return saved

    def update_status(self, post_id: str, status: str) -> dict[str, Any] | None:
        if post_id not in self.posts:
            return None
        self.posts[post_id]["status"] = status
        return self.posts[post_id]

    def delete(self, post_id: str) -> bool:
        if post_id in self.posts:
            del self.posts[post_id]
            return True
        return False


def test_create_post_enforces_author_and_draft_status():
    repo = FakePostRepository()
    service = PostService(repository=repo)

    post_input = PostCreate(
        title="SOLID in Python",
        body="Applying SOLID principles to FastAPI",
        hashtags=["python", "solid", "fastapi"],
    )

    created = service.create_post(post_input)

    assert created["id"] == "1"
    assert created["author"] == "Brian Fox"
    assert created["status"] == PostStatus.DRAFT.value
    assert created["title"] == "SOLID in Python"
    assert "created_at" in created


def test_public_posts_only_show_published():
    repo = FakePostRepository()
    service = PostService(repository=repo)

    draft_post = service.create_post(PostCreate(title="Draft 1", body="draft body"))
    published_post = service.create_post(PostCreate(title="Pub 1", body="pub body", hashtags=["tech"]))
    service.publish_post(published_post["id"])

    # Blog readers should only see published posts
    public_posts = service.get_public_posts()
    assert len(public_posts) == 1
    assert public_posts[0]["id"] == published_post["id"]

    # Filter by hashtag
    matching = service.get_public_posts(hashtag="tech")
    assert len(matching) == 1
    non_matching = service.get_public_posts(hashtag="nonexistent")
    assert len(non_matching) == 0


def test_get_public_post_by_id_raises_if_draft():
    repo = FakePostRepository()
    service = PostService(repository=repo)

    draft = service.create_post(PostCreate(title="Hidden Draft", body="secret"))

    with pytest.raises(PostNotFoundException):
        service.get_public_post_by_id(draft["id"])


def test_publish_and_delete_post():
    repo = FakePostRepository()
    service = PostService(repository=repo)

    post = service.create_post(PostCreate(title="To be published", body="content"))
    assert post["status"] == PostStatus.DRAFT.value

    published = service.publish_post(post["id"])
    assert published["status"] == PostStatus.PUBLISHED.value

    deleted = service.delete_post(post["id"])
    assert deleted is True

    # Subsequent delete should raise PostNotFoundException
    with pytest.raises(PostNotFoundException):
        service.delete_post(post["id"])

def test_cms_can_list_all_posts_including_drafts():
    repo = FakePostRepository()
    service = PostService(repository=repo)

    service.create_post(PostCreate(title="Draft CMS", body="body"))
    pub = service.create_post(PostCreate(title="Pub CMS", body="body"))
    service.publish_post(pub["id"])

    all_posts = service.get_cms_posts()
    assert len(all_posts) == 2

    drafts_only = service.get_cms_posts(status=PostStatus.DRAFT)
    assert len(drafts_only) == 1
    assert drafts_only[0]["status"] == PostStatus.DRAFT.value


def test_publish_non_existent_post_raises_exception():
    repo = FakePostRepository()
    service = PostService(repository=repo)

    with pytest.raises(PostNotFoundException):
        service.publish_post("non-existent-id")


def test_cms_endpoint_requires_valid_bearer_token():
    fake_repo = FakePostRepository()
    app.dependency_overrides[get_post_repository] = lambda: fake_repo
    client = TestClient(app)

    response_no_token = client.post("/cms/posts/", json={"title": "Test", "body": "Body"})
    assert response_no_token.status_code == 401

    headers = {"Authorization": f"Bearer {ADMIN_TOKEN or 'wink_secret_hardcoded_token_2026'}"}
    response_with_token = client.post(
        "/cms/posts/",
        json={"title": "Test Auth", "body": "Body Auth"},
        headers=headers,
    )
    assert response_with_token.status_code == 201

    app.dependency_overrides.clear()