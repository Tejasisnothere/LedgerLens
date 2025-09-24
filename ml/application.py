from fastapi import FastAPI
import os
from dotenv import load_dotenv
import sys
from pydantic import BaseModel
from src.exception import CustomException
from src.logger import logging
from src.components.dataIngestion import DataIngestionPipeline


application = FastAPI()

app = application



@app.get('/predict/{inv_id}')
def predict(inv_id):
    dip = DataIngestionPipeline()
    dip.get_data(inv_id=inv_id)

@app.get('/graph/{inv_id}')
def graph(inv_id):
    
    pass
