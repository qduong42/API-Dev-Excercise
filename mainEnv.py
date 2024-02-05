from fastapi import FastAPI
from pymongo import MongoClient
from uvicorn import run
from dotenv import dotenv_values

config = dotenv_values(".env")
mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")

app = FastAPI()
client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/")
db = client["jsonplaceholder"]
posts_collection = db["posts"]
# comments_collection = db["comments"]


# Endpoint to get the total number of posts and comments for each user
# 2 Collections should be aggregated to show 1 set of values.
@app.get("/user_stats")
async def user_stats():
    pipeline = [
        {
            "$lookup": {
                "from": "comments",
                "localField": "userId",
                "foreignField": "userId",
                "as": "comments_info"
            }
        },
        {
            "$group": {
                "_id": "$userId",
                "total_posts": {"$sum": 1},
                "total_comments": {"$sum": {"$size": "$comments_info"}}
            }
        }
    ]
    lookup_result = list(posts_collection.aggregate(pipeline[:1]))
    print("Lookup Result:", lookup_result)

    # Execute the full pipeline
    result = list(posts_collection.aggregate(pipeline))
    print("Final Result:", result)

    return result
if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8080, reload=True)
