import requests
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()
mongo_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@127.0.0.1:27017/")
db = client["jsonplaceholder"]
collection = db["posts"]

response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts_data = response.json()
collection.insert_many(posts_data)

collection = db["comments"]
response = requests.get("https://jsonplaceholder.typicode.com/comments")
comments_data = response.json()
collection.insert_many(comments_data)
collection.update_many( {}, {"$rename" : {"postId": "userId"}})


