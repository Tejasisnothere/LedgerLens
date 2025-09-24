from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
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
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)



class DataIngestionPipeline:
    def __init__(self):
        self.client = None
        self.db = None
        self.wallet = None
        self.load_mongo()

    def load_mongo(self):
        try:
            load_dotenv()
            mongo_url = os.getenv("MONGO_URL")
            client = MongoClient(mongo_url)

            self.db = client["test"]
            self.wallet = self.db["wallets"]
            self.transactions = self.db["transactions"]
            
            
            
            for doc in self.wallet.find():
                print(doc)

            for doc in self.transactions.find():
                print(doc)

        except Exception as e:
            logging.info("Error")
            raise CustomException(e,sys)

    

    def get_data(self):
        for doc in self.wallet.find():
            print(doc)



class UserRequest(BaseModel):
    user_id: str



# db = client["test"]
# logs = db["logs"]
# items = db["items"]
# events = db["events"]