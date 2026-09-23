from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.exceptions import InvalidIdException, PostNotFoundException
from app.database import ping_db
from app.dependencies import ADMIN_TOKEN
from app.routers.blog import router as blog_router
from app.routers.cms import router as cms_router

description = f"""
## REST API backend for Wink Blog & CMS

### Features
* **Blog (Public)**: Public access to published articles and hashtag filtering.
* **CMS (Content Management System)**: Editorial management (create, publish, delete, filter).

### Authentication
CMS endpoints require HTTP Bearer authentication.
* **Static Admin Token**: `{ADMIN_TOKEN}`
* Click the **Authorize** button above or send `Authorization: Bearer <token>` in your request header.
"""

# Initialize FastAPI application instance
app = FastAPI(
    title="Wink Blog & CMS API",
    description=description
)

# Enable CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(PostNotFoundException)
async def post_not_found_exception_handler(request: Request, exc: PostNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(InvalidIdException)
async def invalid_id_exception_handler(request: Request, exc: InvalidIdException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


# Register routers
app.include_router(blog_router)
app.include_router(cms_router)


@app.get("/")
def root():
    db_status = ping_db()
    return {"status": "ok", "database": db_status}