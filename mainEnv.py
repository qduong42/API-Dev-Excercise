from fastapi import FastAPI
from pymongo import MongoClient
from uvicorn import run

# import os
# from dotenv import load_dotenv
# load_dotenv()

from dotenv import dotenv_values
config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")



app = FastAPI()

# Connect to MongoDB
client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/")
db = client["jsonplaceholder"]
posts_collection = db["posts"]
comments_collection = db["comments"]

# Endpoint to get the total number of posts and comments for each user
@app.get("/user_stats")
async def user_stats():
    pipeline = [
        {
            "$group": {
                "_id": "$userId", 
                "total_posts": {"$sum": 1}
                # "total_comments":  {"$cond": [{"$eq": ["$name", None]}, 1, 0]}
                }
		},
        {
            "$lookup":{
                
			}
		}
	]
    result = list(posts_collection.aggregate(pipeline))
    return result


if __name__ == "__main__":
    run("main:app", host ="0.0.0.0", port=8000, reload=True)