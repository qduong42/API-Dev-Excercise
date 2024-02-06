import requests
import pymongo
from pymongo import MongoClient
from dotenv import dotenv_values  # So we do not need to work with os env values

config = dotenv_values(".env")
mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")

client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@127.0.0.1:27017/")

db = client["task1"]


def insert_data_from_url(collection, url, unique_fields):
    response = requests.get(url)
    data = response.json()
    for item in data:
        unique_values = {key: item[key] for key in unique_fields}
        existing_document = collection.find_one(unique_values)
        if not existing_document:
            collection.insert_one(item)


collection_posts = db["posts"]
collection_posts.create_index([('id', pymongo.ASCENDING)], unique=True)
unique_posts_fields = ["userId", "title", "body"]
insert_data_from_url(collection_posts, "https://jsonplaceholder.typicode.com/posts", unique_posts_fields)

collection_comments = db["comments"]
collection_comments.create_index([('id', pymongo.ASCENDING)], unique=True)
unique_comments_fields = ["name", "email", "body"]
insert_data_from_url(collection_comments, "https://jsonplaceholder.typicode.com/comments", unique_comments_fields)
collection_comments.update_many({}, {"$rename": {"postId": "userId"}})
