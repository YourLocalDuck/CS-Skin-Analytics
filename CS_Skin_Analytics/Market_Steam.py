import requests

class Steam:
    def __init__(self) -> None:
        self.URL = "https://steamcommunity.com"
    def getPrice(self, itemname):
        params = {
            "country": "US",
            "currency": 1,
            "appid": 730,
            "market_hash_name": itemname,
        }
        payload = requests.get(self.URL+"/market/priceoverview/", params=params).json()
        return(payload["lowest_price"])