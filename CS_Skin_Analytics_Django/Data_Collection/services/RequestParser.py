import json


def parseCollectRequestParams(request):
    # Extract parameters from the request
    params = request.body.decode('utf-8')
    params = json.loads(params)
    
    # Parse parameters and build dictionary of markets to update
    marketsToUpdate = params.get("markets", [])
    print(marketsToUpdate)
    for marketString in marketsToUpdate():
        print(marketString)
        ##if key.startswith("market_") and value.lower() in ["true", "false"]:
        #    marketName = key[len("market_") :]
        #    updateFlag = value.lower() == "true"
        #    marketsToUpdate[marketName] = updateFlag

    return marketsToUpdate
