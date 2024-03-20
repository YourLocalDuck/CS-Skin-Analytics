from django.shortcuts import render
import json
from django.http import JsonResponse
from .services import DataCollector
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def collectBuff163(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if (data.get('Cookies') is None) or (data.get('Cookies') == ''):
                return JsonResponse({'error': 'Invalid Cookies'}, status=400)
            
            else:
                # Initiate the collection of data
                buff = DataCollector.Buff163(data.get('Cookies'))
                return JsonResponse({'message': 'Data Collection Initialized successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt # This is temporary
def collectSkinout(request):
    if request.method == 'POST':
        try:
            # Initiate the collection of data
            skinout = DataCollector.Skinout()
            skinout.initializeMarketData()
            return JsonResponse({'message': 'Data Collection Initialized successfully'}) # This is never reached since initializeMarketData() is a a long job
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def collectSkinport(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Initiate the collection of data
            return JsonResponse({'message': 'Data Collection Initialized successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def collectSteam(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Initiate the collection of data
            return JsonResponse({'message': 'Data Collection Initialized successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)