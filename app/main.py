from datetime import datetime
from fastapi import FastAPI
from app.database import ping_db, posts_collection
from app.models import PostCreate

# Initialize FastAPI application instance
app = FastAPI(title="Wink_Blog")


@app.get("/")
def read_root() -> dict:
    db_status: str = ping_db()
    
    return {
        "status": "ok",
        "database": db_status
    }


@app.post("/posts", status_code=201)
def create_post(post: PostCreate) -> dict:
    # Convert Pydantic validation model into a Python dictionary
    post_dict: dict = post.model_dump()
    post_dict["author"] = "Brian Fox"  # Force author to always be Brian Fox
    post_dict["created_at"] = datetime.utcnow()
    
    # Insert document into MongoDB 'posts' collection
    result = posts_collection.insert_one(post_dict)
    
    # Return response payload with stringified MongoDB ObjectId
    return {
        "id": str(result.inserted_id),
        "title": post_dict["title"],
        "body": post_dict["body"],
        "hashtags": post_dict["hashtags"],
        "status": post_dict["status"],
        "author": post_dict["author"],
        "created_at": post_dict["created_at"].isoformat(),
        "message": "Post created successfully"
    }



@app.get("/posts")
def get_posts() -> list[dict]:
    posts: list[dict] = []
    for post in posts_collection.find():
        post["_id"] = str(post["_id"])  # Convert MongoDB ObjectId to string for JSON serialization
        posts.append(post)
    return posts

