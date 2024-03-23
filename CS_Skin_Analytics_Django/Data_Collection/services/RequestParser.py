import json


def parseCollectRequestParams(request):
    # Extract parameters from the request
    params = request.body.decode('utf-8')
    params = json.loads(params)
    
    # Parse parameters and build dictionary of markets to update
    marketsToUpdate = params.get("markets", [])

    return marketsToUpdate
