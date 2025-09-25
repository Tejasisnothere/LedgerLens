from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo import MongoClient
from pydantic import BaseModel
from src.logger import logging
from src.exception import CustomException
import sys
import pandas as pd
import os
from dotenv import load_dotenv


logging.info("App started")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)



class DataIngestionPipeline:
    def __init__(self):
        self.client = None
        self.db = None
        self.logs = None
        self.load_mongo()

    def load_mongo(self):
        try:
            load_dotenv()
            mongo_url = os.getenv("MONGO_URL")
            self.client = MongoClient(mongo_url)

            self.db = self.client["LedgerLens"]
            self.logs = self.db["logs"]
            
            
            logging.info("Mongo connection established")
            

        except Exception as e:
            logging.info("Error")
            raise CustomException(e,sys)
        
    

   

    def get_data(self, inv_id):
        df = pd.DataFrame(data={
            'date': [],
            'name': [],
            'quantity': [],
            'category': [],
            'profit': []
        })

        for doc in self.logs.find({"logOfInv": ObjectId(inv_id)}):
            name = doc['name']
            category = doc['category']
            date = doc['createdAt']
            quantity = doc['quantity']
            profit = doc['profit']

            newdf = pd.DataFrame(data={
                'date': [date],
                'name': [name],
                'quantity': [quantity],
                'category': [category],
                'profit': [profit]
            })

            df = pd.concat([df,newdf],ignore_index=True)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.date
        df = df.sort_values(by='date', ignore_index=True)
        df.to_csv(os.path.join(DATA_DIR, "rawData.csv"), index=False)
        
        return df

        


class UserRequest(BaseModel):
    user_id: str


if __name__ == "__main__":
    con = DataIngestionPipeline()
    con.load_mongo()
    con.get_data("67f59b2b8e1a6c17f4a9c8d2")

# db = client["test"]
# logs = db["logs"]
# items = db["items"]
# events = db["events"]