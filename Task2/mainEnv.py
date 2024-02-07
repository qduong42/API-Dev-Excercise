from fastapi import FastAPI, Query
from pymongo import MongoClient
from uvicorn import run
from dotenv import dotenv_values
from datetime import datetime
from typing import Optional

from json import dumps, JSONDecodeError
import logging

logging.basicConfig(level=logging.ERROR)
config = dotenv_values(".env")
mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")

app = FastAPI()

client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/")
db = client["task2"]  # Replace with your database name
collection_name = "turbine_data"
collection = db[collection_name]

# @app.get("/turbine_data/")
# def get_turbine_data(
#     turbine_id: int = Query(None, title="Turbine ID"),
#     start_time: datetime = Query(None, title="Start Time"),
#     end_time: datetime = Query(None, title="End Time")
# ):
#     query = {}
#     if turbine_id is not None:
#         query["turbine_id"] = turbine_id
#     if start_time is not None and end_time is not None:
#         query["timestamp"] = {"$gte": start_time, "$lte": end_time}
    
#     results = collection.find(query, {"_id": 0}).sort("timestamp")
#     return list(results)

# from fastapi import FastAPI, Query
# from datetime import datetime
# from typing import Optional
# from pymongo import MongoClient
@app.get("/")
async def root():
  return {"available endpoint":"/turbine_data"}

@app.get("/turbine_data")
async def get_turbine_data(turbine_id: int):
    query = {"turbine_id": turbine_id}
    documents = list(collection.find(query, projection={"_id": False}).skip(1).limit(50))
    return documents

if __name__ == "__main__":
    run("mainEnv:app", host ="0.0.0.0", port=8000, reload=True)