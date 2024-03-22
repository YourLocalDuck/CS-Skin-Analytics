from django.shortcuts import render
import json
from django.http import JsonResponse
from .services import DataCollector
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
    
@csrf_exempt # This is temporary
def collect(request):
    if request.method == 'POST':
        try:
            print(request)
            # Initiate the collection of data
            # skinout = DataCollector.Skinout()
            # skinout.initializeMarketData()
            return JsonResponse({'message': 'Data Collection Initialized successfully'}) # This is never reached since initializeMarketData() is a a long job
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
