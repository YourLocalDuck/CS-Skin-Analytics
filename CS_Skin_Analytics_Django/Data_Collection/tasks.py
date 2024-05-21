from typing import List
from celery import shared_task
from .services import DataCollector
import concurrent.futures
from contextlib import contextmanager
from django.core.cache import cache
import time

LOCK_EXPIRE = 60 * 60  # Lock expires in 1 hour

@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    
    try:
        yield status
    finally:
        cache.delete(lock_id)


@shared_task(bind=True)
def marketDataCollectionJob(task, marketsDict: List[dict]):  
    lock_id = 'collection-lock'
    oid = task.request.id
    with memcache_lock(lock_id, oid) as acquired:
        if not acquired:
            return {'status': 'failed', 'error': 'Task is already running.'}
        try:
            markets = []
            for market in marketsDict:
                markets.append(DataCollector.create_market(market))
                
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                for market in markets:
                    executor.submit(market.initializeMarketData)
            return {'status': 'completed'}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
