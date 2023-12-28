import json
import requests
from Skin_Skinport import Skin_Skinport
class Skinport():
    def __init__(self):
        self.file_path = 'Output/skinport_data.json'
        self.url = "https://api.skinport.com"
        self.params = {
            "app_id": 730,
            "currency": "USD",
        }
        
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
        
    def writeToFile(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.skins, f, default=lambda o: o.__dict__, indent=4)
    
    def readFromFile(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.skins = json.load(f)