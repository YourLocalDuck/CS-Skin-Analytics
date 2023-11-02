import requests
import time
import json
from Skin_Steam import Skin_Steam

class Steam:
    def __init__(self) -> None:
        self.url = "https://steamcommunity.com"
        self.params = {
            "query": "appid:730",
            "start": 0,
            "count": 100,
            "norender": 1,
        }
        self.skins = []
        self.file_path = 'skins_data.json'

    def initializeMarketData(self):
        response = requests.get(self.url+'/market/search/render/' , params=self.params)
        if response.status_code == 200:
            payload = response.json()
            skin_data = payload.get('results', [])
            self.skins = [Skin_Steam(**data) for data in skin_data]
            skin_start = payload.get('start', 0)
            skin_pagesize = payload.get('pagesize', 0)
            skin_total_count = payload.get('total_count', 0)
            while ((skin_start + skin_pagesize) < skin_total_count/8):  # Get rid of /8
                params = {
                "query": "appid:730",
                "start": skin_start + skin_pagesize,
                "count": 100,
                "norender": 1,
                }
                print("Trying start "+ str(skin_start+skin_pagesize))
                response = requests.get(self.url+'/market/search/render/' , params=params)
                if response.status_code == 200:
                    print("hit")
                    payload = response.json()
                    skin_data = payload.get('results', [])
                    self.skins += [Skin_Steam(**data) for data in skin_data]
                    skin_start = payload.get('start', 0)
                    skin_pagesize = payload.get('pagesize', 0)
                    skin_total_count = payload.get('total_count', 0)
                else:
                    print(f"Request failed with status code {response.status_code}")
                    if {response.status_code == 429}:
                        print("sleeping")
                        time.sleep(300)
                
        else:
            print(f"Request failed with status code {response.status_code}")
            if {response.status_code == 429}:
                print("sleeping")
                time.sleep(300)
                
    def getPrice(self, itemname):
        item = None
        for i in self.skins:
            if(i.hash_name == itemname):
                item = i
        if item is not None:
            return item.sell_price
        else:
            return None
    
    def writeToFile(self) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(self.skins, file, default=lambda x: x.__dict__, indent=4)
            
    def readFromFile(self) -> None:
        with open(self.file_path, 'r') as file:
            skins_data = json.load(file)
        for data in skins_data:
            skin = Skin_Steam(**data)
            self.skins.append(skin)
    