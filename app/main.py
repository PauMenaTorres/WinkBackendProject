from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import ping_db
from app.routers.blog import router as blog_router
from app.routers.cms import router as cms_router

# Initialize FastAPI application instance
app = FastAPI(
    title="Wink Blog & CMS API",
    description="REST API backend for Blog (Public Readers) and CMS (Content Management System)"
)

# Register routers
app.include_router(blog_router)
app.include_router(cms_router)


@app.get("/")
def root():
    db_status = ping_db()
    return {"status": "ok", "database": db_status}