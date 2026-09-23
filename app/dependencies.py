import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.database import posts_collection
from app.repositories.base import PostRepository
from app.repositories.mongo_post_repo import MongoPostRepository
from app.services.post_service import PostService

load_dotenv()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

security = HTTPBearer()


def verify_admin_token(
    authentication: HTTPAuthorizationCredentials = Security(security),
) -> str:
    if authentication.credentials != ADMIN_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authentication.credentials


def get_post_repository() -> PostRepository:
    """Dependency provider for PostRepository (DIP)."""
    return MongoPostRepository(collection=posts_collection)


def get_post_service(
    repository: PostRepository = Depends(get_post_repository),
) -> PostService:
    """Dependency provider for PostService (DIP & SRP)."""
    return PostService(repository=repository)
