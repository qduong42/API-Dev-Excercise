from fastapi import FastAPI, Query
from pymongo import MongoClient
from uvicorn import run
from dotenv import dotenv_values
from datetime import datetime
from typing import Optional

from json import dumps, JSONDecodeError

config = dotenv_values(".env")
mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")

app = FastAPI()

client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/")
db = client["task2"]  # Replace with your database name
collection_name = "turbine_data"
collection = db[collection_name]

@app.get("/")
async def root():
  return {"available endpoint":"/turbine_data"}

@app.get("/turbine_data")
async def get_turbine_data(turbine_id: Optional[int] = Query(None), start_time: Optional[str] = Query(None), end_time: Optional[str] = Query(None)):
    if start_time is not None:
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        # "2016-02-01T00:50:00"
    if end_time is not None:
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    
    if start_time is None or end_time is None:
        limit = 1000
    else:
        limit = 0
    
    query = {}
    if turbine_id is not None:
        query = {"turbine_id": turbine_id}
    if start_time is not None:
        query["Dat/Zeit"] = {"$gte": start_time}
    if end_time is not None:
        query.setdefault("Dat/Zeit", {}).update({"$lte": end_time})
    documents = list(collection.find(query, projection={"_id": False}).skip(1).limit(limit))
    return documents

if __name__ == "__main__":
    run("mainEnv:app", host ="0.0.0.0", port=8000, reload=True)