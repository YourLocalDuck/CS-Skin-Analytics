import json
import requests

from Skin_Skinout import Skin_Skinout

## API Reverse Engineered.

class Skinout:
    def __init__(self) -> None:
        self.file_path = 'Output/skinout_data.json'
        self.url = "https://skinout.gg"
        self.params = {
            "sort": "popularity_desc",
            "page": 1,
        }
        self.skins = []
    
    def initializeMarketData(self):
        response = requests.get(self.url+'/api/market/items' , params=self.params)
        if response.status_code == 200:
            payload = response.json()
            skin_data = payload.get('items', [])
            self.skins = [Skin_Skinout(**data) for data in skin_data]
            page = payload.get('page', 0)
            page_count = payload.get('page_count', 0)
            while (page < page_count):
                params = {
                    "sort": "popularity_desc",
                    "page": page+1,
                }
                print("Updating Page "+ str(page+1) + " of " + str(page_count))
                response = requests.get(self.url+'/api/market/items' , params=params)
                if response.status_code == 200:
                    print("Success")
                    payload = response.json()
                    skin_data = payload.get('items', [])
                    self.skins += [Skin_Skinout(**data) for data in skin_data]
                    page = payload.get('page', 0)
                    page_count = payload.get('page_count', 0)
                else:
                    print(f"Request failed with status code {response.status_code}")
        else: 
            print(f"Request failed with status code {response.status_code}")
            
    def getPrice(self, itemname):
        item = None
        for i in self.skins:
            if(i.market_hash_name == itemname):
                item = i
        if item is not None:
            return item.price
        else:
            return None
    
    def writeToFile(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.skins, file, default=lambda x: x.__dict__, indent=4)
            
    def readFromFile(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            skins_data = json.load(file)
        for data in skins_data:
            self.skins.append(Skin_Skinout(**data))
        