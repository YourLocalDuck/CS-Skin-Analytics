from typing import List
from django.shortcuts import render
import json
from django.http import JsonResponse
from .services import RequestParser
from .services import DataCollector
from . import tasks
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
# Create your views here.
    
@csrf_exempt # This is temporary
def collect(request):
    if request.method == 'POST':
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
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
