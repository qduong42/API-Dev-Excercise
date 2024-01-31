import requests
from pymongo import MongoClient

client = MongoClient("mongodb://root:example@localhost:27017/")
db = client["jsonplaceholder"]
collection = db["posts"]

response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts_data = response.json()

collection.insert_many(posts_data)
