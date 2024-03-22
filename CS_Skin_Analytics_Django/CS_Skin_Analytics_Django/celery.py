## UNFINISHED ##############################################

from celery import Celery
from Data_Collection.services import DataCollector

app = Celery('CSA', broker='pyamqp://guest@localhost//')

@app.task
def initialize_market_data():
    skinout = DataCollector.Skinout()
    skinout.initializeMarketData()