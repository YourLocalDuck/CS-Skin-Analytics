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
            print(marketsToUpdateStr)
            tasks.marketDataCollectionJob.delay(marketsToUpdateStr)
            return JsonResponse({'message': 'Data Collection Initialized successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
