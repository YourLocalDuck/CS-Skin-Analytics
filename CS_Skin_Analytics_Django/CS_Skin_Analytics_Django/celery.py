from typing import List
from celery import Celery
from Data_Collection.services import DataCollector
from django.core.cache import cache

app = Celery('CS_Skin_Analytics_Django', broker='pyamqp://guest@localhost//')
app.autodiscover_tasks()