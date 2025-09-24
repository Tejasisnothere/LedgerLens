import pandas as pd
import numpy as np
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

class GraphPipeline:
    def __init__(self):
        self.df = pd.read_csv(os.path.join(DATA_DIR, "rawData.csv"))


    def dataframe_to_graph(self):
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df = self.df.sort_values(by='date', ignore_index=True)
        return {
            "x": self.df['date'].dt.strftime("%Y-%m-%d").tolist(),
            "y": self.df['profit'].tolist()
        }

    
