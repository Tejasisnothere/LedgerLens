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
    category: str       # The category selected by the user
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



@app.get('/predict/{inv_id}/')
def predict(inv_id):
    dip = DataIngestionPipeline()
    dip.get_data(inv_id=inv_id)
    mod = ModelPipeline()
    dates = mod.pipeline(cat="groceries", confid=50)
    dates.drop(columns=['yhat', 'trend', 'upper_bound', 'lower_bound'],inplace=True)



    return {"success":"True", "data":dates}


# @app.get('/graph/{inv_id}')
# def graph(inv_id, request: Request):
#     dip = DataIngestionPipeline()
#     df = dip.get_data(inv_id=inv_id)
#     profit_df = total_profit_by_category(df)

#     df['date'] = pd.to_datetime(df['date'],errors='coerce')
#     data = {
#         "x": df["date"].dt.strftime("%Y-%m-%d").tolist(),
#         "y": df["profit"].tolist(),
#     }

#     return templates.TemplateResponse("graph.html", {"request": request, "data": data})


@app.get('/graph/{inv_id}')
def graph(inv_id: str, request: Request):
    """
    This endpoint fetches data for a given inventory ID, processes it into the
    format required by the D3.js dashboard, and renders the HTML page.
    """
    dip = DataIngestionPipeline()
    df = dip.get_data(inv_id=inv_id)

    # --- Data Processing for D3.js ---
    
    # 1. Ensure the DataFrame is not empty
    if df.empty:
        expenses_data = []
    else:
        # 2. Rename 'profit' to 'amount' to match the frontend's expectation
        df.rename(columns={'profit': 'amount'}, inplace=True)

        # 3. Ensure the 'date' column is a string in 'YYYY-MM-DD' format
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        # 4. Select only the columns needed by the frontend to keep the payload small
        required_columns = ['date', 'amount', 'category', 'quantity', 'name']
        df_subset = df[required_columns]

        # 5. Convert the processed DataFrame to a list of dictionaries (JSON array)
        expenses_data = df_subset.to_dict('records')

    # --- Render the Template ---
    return templates.TemplateResponse(
        "graph.html", 
        {
            "request": request,
            "inv_id": inv_id,
            "expenses_data": expenses_data  # Pass the full dataset to the template
        }
    )




@app.get('/displayGraph')
async def home(request: Request):
    pass



if __name__ == "__main__":
    uvicorn.run("application:app", host="127.0.0.1", port=8000, reload=True)


