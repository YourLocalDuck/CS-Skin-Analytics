from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import GenerateAnalysis
import json
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def getProfitSummary(request):
    params = request.body.decode('utf-8')
    params = json.loads(params)
    if not params.get('buy_markets') or not params.get('sell_markets'):
        return Response({'error': 'Invalid Request. Missing Buy Market, Sell Market or both'}, status=status.HTTP_404_NOT_FOUND)
    response = Response(GenerateAnalysis.parseSummaryRequest(params))
    return response