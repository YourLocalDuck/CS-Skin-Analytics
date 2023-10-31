import requests
class skinport():
    def __init__(self):
        self.url = "https://api.skinport.com"
        self.params = {
            "app_id": 730,
            "currency": "USD",
        }
        self.initializeMarketData()
        
    def initializeMarketData(self):
        self.payload = requests.get(self.url+'/v1/items' , params=self.params).json()
        
    def getPrice(self, itemname):
        for i in self.payload:
            if(i['market_hash_name'] == itemname):
                item = i
        return item['min_price']
    