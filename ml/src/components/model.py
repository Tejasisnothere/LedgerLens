import sys
from sklearn.metrics import mean_absolute_percentage_error, r2_score
import os
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(DATA_DIR, exist_ok=True)

class ModelPipeline:

    def __init__(self, file_name="rawData.csv", period=10):
        self.file_name = file_name
        self.cols = ["groceries", "beverages", "personal", "household", "clothing", "festive", "stationary", "health"]
        self.prop = Prophet()
        self.period = period

    def load_dataset(self):
        try:
            self.df = pd.read_csv(os.path.join(DATA_DIR, self.file_name))
            

        except Exception as e:
            raise CustomException(e, sys)
        
    def categorizeDF(self, cat):
        self.newdf = self.df[self.df['category'] == cat].copy()
        self.newdf.rename(columns={
            "profit": "y",
            "date": "ds"
        }, inplace=True)

        self.newdf['ds'] = pd.to_datetime(self.newdf['ds'])

        self.prop.fit(self.newdf)
        self.future = self.prop.make_future_dataframe(self.period)
        self.forecast = self.prop.predict(self.future)
        self.forecast['ds'] = pd.to_datetime(self.forecast['ds'])

    
    def map_value(self, value, x1_min, x1_max, x2_min, x2_max):
        if x1_max == x1_min:
            raise ValueError("Source range min and max cannot be equal.")
        return x2_min + ((value - x1_min) / (x1_max - x1_min)) * (x2_max - x2_min)

    

    def finalization(self):
        y_min = self.newdf['y'].min()
        y_max = self.newdf['y'].max()

        yhat_max = self.forecast['yhat'].max()
        yhat_min = self.forecast['yhat'].min()


        sensitive_vals = []
        
        for index, row in self.forecast.iterrows():
            
            mpvalue = self.map_value(row['yhat'], yhat_min, yhat_max, y_min, y_max)
            sensitive_vals.append(mpvalue)

        self.forecast['sensitive_vals'] = sensitive_vals

                
    def plot(self):
        plt.figure(figsize=(12, 6)) # Make the plot bigger

        # Plot the first 100 days for clarity
        plt.plot(self.newdf['ds'][:100], self.newdf['y'][:100], color='red', label="Actual Values", linewidth=2)
        plt.plot(self.forecast['ds'][:100], self.forecast['sensitive_vals'][:100], color='orange', label="Mapped Predicted Values", linestyle='--')
        plt.plot(self.forecast['ds'][:100], self.forecast['yhat'][:100], color='blue', label="Predicted Values (yhat)")
        plt.plot(self.forecast['ds'][:100], self.forecast['yhat_upper'][:100], color='cyan', label="Prediction Bound")
        plt.plot(self.forecast['ds'][:100], self.forecast['yhat_lower'][:100], color='cyan')
        plt.plot(self.forecast['ds'][:100], self.forecast['trend'][:100], color='purple', label="Trend", linestyle=':')


        plt.legend()
        plt.title("Prophet Forecast vs Actual Sales")
        plt.xlabel("Date")
        plt.ylabel("Sales Amount")
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.show()

    def calc_metrics(self):
        merged = pd.merge(self.newdf, self.forecast[['ds', 'yhat']], on='ds', how='inner')

        y_true = merged['y']
        y_pred = merged['yhat']

        mape = mean_absolute_percentage_error(y_true, y_pred) * 100

        print(f"MAPE (lower is better): {mape:.2f}%")
        print(f"Forecast Accuracy: {100 - mape:.2f}%")


    
    def pipeline(self, confid, cat="groceries"):
        if cat not in self.cols:
            return
        self.load_dataset()
        self.categorizeDF(cat=cat)
        self.newdf['ds'] = pd.to_datetime(self.newdf['ds'])
        self.forecast['ds'] = pd.to_datetime(self.forecast['ds'])

        self.finalization()
        # self.plot()
        self.calc_metrics()

        return self.check_confidence_surpass(confidence_percent=confid)

    def check_confidence_surpass(self, confidence_percent):
        results = []

        # Calculate confidence band limits
        self.forecast['upper_bound'] = self.forecast['trend'] * (1 + confidence_percent / 100)
        self.forecast['lower_bound'] = self.forecast['trend'] * (1 - confidence_percent / 100)

        # Check forecasted period
        future_dates = self.forecast.tail(self.period)  # Last N days

        for _, row in future_dates.iterrows():
            if row['yhat'] > row['upper_bound'] or row['yhat'] < row['lower_bound']:
                results.append({
                    "date": row['ds'],
                    "yhat": row['yhat'],
                    "trend": row['trend'],
                    "upper_bound": row['upper_bound'],
                    "lower_bound": row['lower_bound'],
                    "exceeds": "above" if row['yhat'] > row['upper_bound'] else "below"
                })

        return pd.DataFrame(results)




# m = ModelPipeline("rawData.csv")
# dates = m.pipeline(cat="household", confid=50) 
# print(dates)
