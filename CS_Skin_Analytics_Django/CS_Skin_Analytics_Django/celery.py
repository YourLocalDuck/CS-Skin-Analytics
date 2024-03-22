## UNFINISHED ##############################################

from typing import List
from celery import Celery
from Data_Collection.services import DataCollector

app = Celery('CS_Skin_Analytics_Django', broker='pyamqp://guest@localhost//')

@app.task
def initialize_market_data(markets: List[DataCollector.Market_Base]):
    for market in markets:
        match(market):
            case market == "skinout":
                
        market = DataCollector.Skinout()
        market.initializeMarketData()
        print(f"Market {market} initialized")