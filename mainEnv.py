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
# posts_collection = db["posts"]
comments_collection = db["comments"]


# Endpoint to get the total number of posts and comments for each user
# 2 Collections should be aggregated to show 1 set of values.
@app.get("/user_stats/new")
async def user_stats():
    # pipeline = [
#   {
#     "$group": {
#       "_id": "$userId",
#       "total comments": {"$sum": 1},
#     },
#   },
#   {
#     "$lookup": {
#       "from": "posts",
#       "localField": "_id",
#       "foreignField": "userId",
#       "as": "posts_info",
#     },
#   },
#   {
#     "$addFields": {
#       "total posts": {
#         "$size": "$posts_info",
#       },
#     },
#   },
#     {
#     "$project": {
#       "posts_info": 0,
#     },
#   },
#   {
#     "$project":{
#       "_id": 1,
#       "total posts": 1,
#       "total comments": 1
#     }
#   }
# ]
    # result = list(comments_collection.aggregate(pipeline))
    result = list(comments_collection)
    return result


if __name__ == "__main__":
    run("main:app", host ="0.0.0.0", port=8000, reload=True)
