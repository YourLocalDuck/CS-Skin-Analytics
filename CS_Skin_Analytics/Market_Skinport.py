import requests
from Skin_Skinport import Skin_Skinport
class Skinport():
    def __init__(self):
        self.url = "https://api.skinport.com"
        self.params = {
            "app_id": 730,
            "currency": "USD",
        }
        self.initializeMarketData()
        
    def initializeMarketData(self):
        response = requests.get(self.url+'/v1/items' , params=self.params)
        if response.status_code == 200:
            payload = response.json()
            self.skins = [Skin_Skinport(**data) for data in payload]
        else:
            print(f"Request failed with status code {response.status_code}")
        
    def getPrice(self, itemname):
        item = None
        for i in self.skins:
            if(i.market_hash_name == itemname):
                item = i
        if item is not None:
            return item.min_price
        else:
            return None
    