import requests
from pymongo import MongoClient

client = MongoClient("mongodb://root:example@localhost:27017/")

db = client["jsonplaceholder"]


def insert_data_from_url(collection, url):
    response = requests.get(url)
    data = response.json()
    for item in data:
        query = {key: item[key] for key in item if key != 'id'}
        existing_document = collection.find_one(query)
        if not existing_document:
            collection.insert_one(item)


collection_posts = db["posts"]
collection_comments = db["comments"]
insert_data_from_url(collection_posts, "https://jsonplaceholder.typicode.com/posts")
insert_data_from_url(collection_comments, "https://jsonplaceholder.typicode.com/comments")
collection_comments.update_many({}, {"$rename": {"postId": "userId"}})
