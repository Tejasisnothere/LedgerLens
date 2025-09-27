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
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

application = FastAPI()

app = application



from pydantic import BaseModel

class GraphRequest(BaseModel):
    category: str      
    graph_type: str    

def dataframe_to_graph(df):
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ignore_index=True)
        return {
            "x": df['date'].dt.strftime("%Y-%m-%d").tolist(),
            "y": df['profit'].tolist()
        }


def total_profit_by_category(df: pd.DataFrame):
    
    if "category" not in df.columns or "profit" not in df.columns:
        raise ValueError("DataFrame must contain 'category' and 'profit' columns")
    
    print( df.groupby("category", as_index=False)["profit"].sum().rename(columns={"profit": "total_profit"}))




@app.get("/predict/{inv_id}")
def predict(inv_id: str, request: Request):
    """
    Runs the prediction pipeline for a given inventory ID and displays
    the results on the animated predictions page.
    """
    dip = DataIngestionPipeline()
    dip.get_data(inv_id=inv_id) # This line seems to fetch data, but it's not used below. Assuming the model pipeline uses it internally.
    
    categories = ["groceries", "beverages", "personal", "household", "clothing", "festive", "stationary", "health"]
    strResp = []

    for cat in categories:
        mod = ModelPipeline()
        dates = mod.pipeline(cat=cat, confid=50)
        
        # Skip if the model pipeline returns nothing for this category
        if dates is None or dates.empty:
            continue
            
        try:
            # Drop unnecessary columns if they exist
            cols_to_drop = ['yhat', 'trend', 'upper_bound', 'lower_bound']
            existing_cols_to_drop = [col for col in cols_to_drop if col in dates.columns]
            if existing_cols_to_drop:
                dates.drop(columns=existing_cols_to_drop, inplace=True)
        except Exception as e:
            print(f"Could not drop columns for category {cat}: {e}")
            continue

        # --- This is your logic, integrated to match the required output ---
        strtypes = {
            "above": f"The product sales of {cat} is expected to rise on ",
            "below": f"The product sales of {cat} is expected to drop on "
        }
        
        df_rise = dates[dates['exceeds'] == 'above']
        df_drop = dates[dates['exceeds'] == 'below']

        for _, row in df_rise.iterrows():
            d = row['date']
            strResp.append(strtypes["above"] + f"{d}")
        
        for _, row in df_drop.iterrows():
            d = row['date']
            strResp.append(strtypes["below"] + f"{d}")
    
    
    return templates.TemplateResponse(
        "prediction.html", 
        {"request": request, "data": strResp}
    )

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})



@app.get('/graph/{inv_id}')
def graph(inv_id: str, request: Request):
   
    dip = DataIngestionPipeline()
    df = dip.get_data(inv_id=inv_id)


    if df.empty:
        expenses_data = []
    else:
        df.rename(columns={'profit': 'amount'}, inplace=True)

        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        required_columns = ['date', 'amount', 'category', 'quantity', 'name']
        df_subset = df[required_columns]

        expenses_data = df_subset.to_dict('records')

    return templates.TemplateResponse(
        "graph.html", 
        {
            "request": request,
            "inv_id": inv_id,
            "expenses_data": expenses_data 
        }
    )





if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000, reload=True)


