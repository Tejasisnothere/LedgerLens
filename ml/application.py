from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
import sys
import pandas as pd
import numpy as np
from pydantic import BaseModel
from src.exception import CustomException
from src.logger import logging
from src.components.dataIngestion import DataIngestionPipeline
from fastapi.templating import Jinja2Templates
import uvicorn
from src.components.graphPipeline import GraphPipeline
from datetime import datetime, timedelta
from src.components.model import ModelPipeline


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

application = FastAPI()

app = application


from pydantic import BaseModel

class GraphRequest(BaseModel):
    category: str       # The category selected by the user
    graph_type: str    

def dataframe_to_graph(df):
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ignore_index=True)
        return {
            "x": df['date'].dt.strftime("%Y-%m-%d").tolist(),
            "y": df['profit'].tolist()
        }


@app.get('/predict/{inv_id}')
def predict(inv_id):
    dip = DataIngestionPipeline()
    output = dip.get_data(inv_id=inv_id)
    mod = ModelPipeline()
    dates = mod.pipeline(cat="groceries", confid=50)
    dates.drop(columns=['yhat', 'trend', 'upper_bound', 'lower_bound'],inplace=True)

    return {"success":"True", "data":dates}



@app.get('/graph/{inv_id}/{category}')
async def graph(inv_id, request: Request):
    global inv
    inv = inv_id
    dip = DataIngestionPipeline()
    dip.get_data(inv_id=inv_id)
    gp = GraphPipeline()
    graph_data = gp.dataframe_to_graph()
    
    return templates.TemplateResponse("graph.html", {"request": request, "data": graph_data})
    
@app.post("/graph-data/")
async def get_graph_data( req: GraphRequest):
    
    global inv
    
    dip = DataIngestionPipeline()
    dip.get_data(inv_id=inv)
    gp = GraphPipeline()
    # graph_data = gp.cat_dataframe_to_graph(req.category)


    
    return {
        "data": gp.cat_dataframe_to_graph(req.category),
        "graph_type": req.graph_type
    }



@app.get('/displayGraph')
async def home(request: Request):
    pass



if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000, reload=True)