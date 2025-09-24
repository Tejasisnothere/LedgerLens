import requests
from dotenv import load_dotenv
import os
import sys
from datetime import datetime


country = "IN"



response = requests.get(f"https://holidays.abstractapi.com/v1/?api_key=4840260c617b4c6995c3e83654d795df&country={country}&year=2025&month=8&day=27")
print(response.status_code)
print(response.content)


class EventBasedRecommendationPipeline:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv("EVENT_KEY")
        self.date = datetime.now()

    
    def getEvent(self, date=None):
        if(date==None):
            date = self.date
        
        month = date.month
        day = date.day
        year = date.year


        response = requests.get(f"https://holidays.abstractapi.com/v1/?api_key={self.key}&country={country}&year={year}&month={month}&day={day}")
        print(response)

        
