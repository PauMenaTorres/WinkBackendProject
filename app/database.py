import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve MongoDB connection string from environment variables
raw_uri: str = os.getenv("MONGODB_URI", "")
uri: str = raw_uri + "/?appName=Cluster0"

# Initialize MongoDB client with Stable API version 1
client: MongoClient = MongoClient(uri, server_api=ServerApi('1'))

# Access the target database and collection
db = client["wink_blog"]
posts_collection = db["posts"]


def ping_db() -> str:
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        return f"Database error: {e}"


if __name__ == "__main__":
    print(ping_db())

