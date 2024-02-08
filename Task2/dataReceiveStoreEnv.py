import pandas as pd
from pymongo import MongoClient
from dotenv import dotenv_values  # So we do not need to work with os env values
from io import StringIO
import requests
from termcolor import colored

def get_mongo_collection(db_name, collection_name):
    config = dotenv_values(".env")
    mongo_username = config.get("MONGO_INITDB_ROOT_USERNAME")
    mongo_password = config.get("MONGO_INITDB_ROOT_PASSWORD")
    client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@127.0.0.1:27017/")
    db = client[db_name]
    collection = db[collection_name]
    print(colored("Creating indexes for Dat/Zeit and turbine_id", 'green'))
    collection.create_index([("Dat/Zeit", 1), ("turbine_id", 1)])
    return collection

def download_and_parse_csv(csv_url, turbine_id):
    print(colored("Downloading data from url", 'green'))
    response = requests.get(csv_url)
    if response.status_code == 200:
        print(colored("Data downloaded from url", 'blue'))
        print(colored("Parsing to dataframe", 'green'))
        df = pd.read_csv(StringIO(response.text), skipinitialspace=True, sep=';', on_bad_lines='warn')
        df['turbine_id'] = turbine_id
        df['Dat/Zeit'] = pd.to_datetime(df['Dat/Zeit'], format="%d.%m.%Y, %H:%M")
        print(colored(f"Parse completed with code: {response.status_code}", "green"))
        return df
    else:
        print(colored(f"Failed to download the file. Status code: {response.status_code}", "red"))
        return pd.DataFrame()

def insert_records_to_db(df, collection):
    records_to_insert = df.to_dict(orient='records')
    i = 0
    df_len = len(df.index)
    for item in records_to_insert:
        if pd.isnull(item["Dat/Zeit"]):
            item["Dat/Zeit"] = None
        unique_values = {"Dat/Zeit": item["Dat/Zeit"], "turbine_id": item["turbine_id"]}
        existing_document = collection.find_one(unique_values)
        if not existing_document:
            collection.insert_one(item)
        i += 1
        if (i % 1000) == 0:
            print(colored(f"{i} of {df_len} records processed", "blue"))
    print(colored(f"{df_len} records processed", "blue"))

def load_csv_to_mongodb(csv_url, turbine_id, db_name, collection_name):
    try:
        collection = get_mongo_collection(db_name, collection_name)
        df = download_and_parse_csv(csv_url, turbine_id)
        print(colored(f"Inserting data of turbine id:{turbine_id} into DB. Only unique values with regards to turbine id and time are inserted", 'green'))
        insert_records_to_db(df, collection)
        print(colored("Data inserted into DB", 'blue'))
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")

load_csv_to_mongodb("https://nextcloud.turbit.com/s/GTbSwKkMnFrKC7A/download/Turbine1.csv", turbine_id=1, db_name="task2", collection_name="turbine_data")
load_csv_to_mongodb("https://nextcloud.turbit.com/s/G3bwdkrXx6Kmxs3/download/Turbine2.csv", turbine_id=2, db_name="task2", collection_name="turbine_data")
