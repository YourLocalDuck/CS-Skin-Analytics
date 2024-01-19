import requests
from Market_Base import Market_Base
class Bitskins(Market_Base):
    def __init__(self) -> None:
        self.URL = "https://api.bitskins.com"
        
    def initializeMarketData(self):
        self.payload = requests.get(self.URL+"/market/insell/730").json()
        
    def getPrice(self, itemname):
        item = None
        for i in self.payload['list']:
            if(i['name'] == itemname):
                item = i
        if item is not None:
            return item['price_min']*.001
        else:
            return None