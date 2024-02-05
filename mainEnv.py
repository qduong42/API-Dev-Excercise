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
comments_collection = db["comments"]


# Endpoint to get the total number of posts and comments for each user
# 2 Collections should be aggregated to show 1 set of values.
@app.get("/user_stats")
async def user_stats():
    pipeline = [
  {
    "$group": {
      "_id": "$userId",
      "total comments": {"$sum": 1},
    },
  },
  {
    "$lookup": {
      "from": "posts",
      "localField": "_id",
      "foreignField": "userId",
      "as": "posts_info",
    },
  },
  {
    "$addFields": {
      "total posts": {
        "$size": "$posts_info",
      },
    },
  },
    {
    "$project": {
      "posts_info": 0,
    },
  }
]
    result = list(comments_collection.aggregate(pipeline))
    return result


if __name__ == "__main__":
    run("mainEnv:app", host ="0.0.0.0", port=8000, reload=True)
