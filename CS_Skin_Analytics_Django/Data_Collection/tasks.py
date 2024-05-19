from typing import List
from celery import shared_task
from .services import DataCollector
import concurrent.futures

@shared_task
def marketDataCollectionJob(marketsDict: List[dict]):
    markets = []
    for market in marketsDict:
        markets.append(DataCollector.create_market(market))
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for market in markets:
            executor.submit(market.initializeMarketData)
