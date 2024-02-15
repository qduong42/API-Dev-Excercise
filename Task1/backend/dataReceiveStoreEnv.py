import requests
import pymongo
from pymongo import MongoClient
from dotenv import dotenv_values  # So we do not need to work with os env values
from termcolor import colored
import time


config = dotenv_values(".env")
mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")

MAX_RETRIES = 3
RETRY_INTERVAL_SECONDS = 5

def connect_to_mongodb():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@mongo")
            db = client["task1"]
            return db
        except pymongo.errors.ConnectionFailure as e:
            print(colored(f"Connection error: {e}. Retrying...", "red"))
            retries += 1
            time.sleep(RETRY_INTERVAL_SECONDS)
    print(colored(f"Failed to connect after {MAX_RETRIES} retries. Exiting.", "red"))
    exit(1)



def insert_data_from_url(collection, url, unique_fields):
    response = requests.get(url)
    data = response.json()
    for item in data:
        unique_values = {key: item[key] for key in unique_fields}
        existing_document = collection.find_one(unique_values)
        if not existing_document:
            collection.insert_one(item)

if __name__ == "__main__":
    try:
        db = connect_to_mongodb()
        collection_posts = db["posts"]
        print(colored("Creating index for posts id", "green"))
        collection_posts.create_index([("id", pymongo.ASCENDING)], unique=True)
        unique_posts_fields = ["userId", "title", "body"]
        print(colored("Inserting data from url for posts", "green"))
        insert_data_from_url(collection_posts, "https://jsonplaceholder.typicode.com/posts", unique_posts_fields)

        collection_comments = db["comments"]
        print(colored("Creating index for comments id", "green"))
        collection_comments.create_index([("id", pymongo.ASCENDING)], unique=True)
        unique_comments_fields = ["name", "email", "body"]
        print(colored("Inserting data from url for comments", "green"))
        insert_data_from_url(collection_comments, "https://jsonplaceholder.typicode.com/comments", unique_comments_fields)

        print(colored("Updating postId to userId in comments", "green"))
        collection_comments.update_many({}, {"$rename": {"postId": "userId"}})
    except Exception as e:
        print(colored(f"Error: {e}", "red"))
        exit(1)