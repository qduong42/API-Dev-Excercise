from fastapi import FastAPI
from pymongo import MongoClient
from uvicorn import run

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["jsonplaceholder"]
posts_collection = db["posts"]

# Endpoint to get the total number of posts and comments for each user
@app.get("/user_stats/new")
async def user_stats():
    pipeline = [
        {"$group": {"_id": "$userId", "total_posts": {"$sum": 1}, "total_comments": {"$sum": "$comments"}}}
    ]
    result = list(posts_collection.aggregate(pipeline))
    return result



if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=100, reload=True)