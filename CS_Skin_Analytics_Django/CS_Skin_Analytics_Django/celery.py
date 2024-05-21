from typing import List
from celery import Celery
from Data_Collection.services import DataCollector
from django.core.cache import cache
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CS_Skin_Analytics_Django.settings')
app = Celery('CS_Skin_Analytics_Django')
app.autodiscover_tasks()
app.config_from_object('django.conf:settings', namespace='CELERY')