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
    # Build the query
    query = {"turbine_id": turbine_id}

    # Retrieve the documents from MongoDB
    documents = list(collection.find(query, projection={"_id": False}).limit(20))

    # Convert large floats to strings
    for document in documents:
        for key in document.keys():
        # for key in ["Prod. 1", "Prod. 2", "BtrStd 1", "BtrStd 2"]:
            # if key in document:
            document[key] = str(document[key])
    # for document in documents:
    #     for key, value in document.items():
    #         try:
    #             dumps({key: value})
    #         except (TypeError, OverflowError):
    #             logging.error(f"Error serializing field {key} with value {value}")

    return documents

if __name__ == "__main__":
    run("mainEnv:app", host ="0.0.0.0", port=8000, reload=True)