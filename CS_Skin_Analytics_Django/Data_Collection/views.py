from typing import List
from django.shortcuts import render
import json
from django.http import JsonResponse
from .services import RequestParser
from . import tasks
from rest_framework.decorators import api_view
from django.core.cache import cache
# Create your views here.
    
@api_view(['POST'])
def collect(request):
    try:
        marketsToUpdateStr: List[dict] = RequestParser.parseCollectRequestParams(request)
        # Attempt to start the Celery task
        if(cache.get('collection-lock')):
            return JsonResponse({'error': 'Data Collection is already in progress'}, status=409)
        result = tasks.marketDataCollectionJob.delay(marketsToUpdateStr)
        return JsonResponse({'message': 'Data Collection Initialized successfully'})  # Respond immediately
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
