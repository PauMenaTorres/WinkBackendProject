from fastapi import FastAPI
from app.database import ping_db
from app.routers.posts import router as posts_router

# Initialize FastAPI application instance
app = FastAPI(title="Wink_Blog")

# Register routers
app.include_router(posts_router)


@app.get("/")
def root():
    db_status = ping_db()
    return {"status": "ok", "database": db_status}