import pandas as pd
from pymongo import MongoClient
from dotenv import dotenv_values  # So we do not need to work with os env values
from io import StringIO  # Import StringIO from the io module
import requests

config = dotenv_values(".env")
mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")

client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@127.0.0.1:27017/")
db_name = "task2"
db = client[db_name]

collection_name = "turbine_data"
collection = db[collection_name]

#""",      ep=';', na_values=[''] """
def load_csv_to_mongodb(csv_url, turbine_id):
    try:
        response = requests.get(csv_url)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text), skipinitialspace=True, sep=';', on_bad_lines='warn')
            df['turbine_id'] = turbine_id
            records_to_insert = df.to_dict(orient='records')
            # collection.insert_many(records)
            collection.create_index([("Dat/Zeit", 1), ("turbine_id", 1)])
            for record in records_to_insert:
                collection.update_one(
                    {"Dat/Zeit": record["Dat/Zeit"], "turbine_id": record["turbine_id"]},
                {"$addToSet": {"data": record}},
                upsert=True
                )
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except pd.errors.ParserError as e:
            print(f"ParserError: {e}")    
# Load     ata for Turbine 1
load_csv_to_mongodb("https://nextcloud.turbit.com/s/GTbSwKkMnFrKC7A/download/Turbine1.csv", turbine_id=1)

# Load data for Turbine 2
load_csv_to_mongodb("https://nextcloud.turbit.com/s/G3bwdkrXx6Kmxs3/download/Turbine2.csv", turbine_id=2)
