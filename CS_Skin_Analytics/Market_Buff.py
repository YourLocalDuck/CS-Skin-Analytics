import json
import requests
import currency_converter

from Skin_Buff import Skin_Buff

## API Reverse Engineered.

class Buff:
    converter = currency_converter.CurrencyConverter() 
    def __init__(self, header):
        self.exchange_rate = self.converter.convert(1, 'CNY', 'USD')
        self.file_path = 'buff_data.json'
        self.url = "https://buff.163.com"
        self.header = {
            "Cookie": str(header)
        }
        self.params = {
            "game" : "csgo",
            "page_size" : "80",
            "page_num" : "1",
        }
        self.skins = []

    def initializeMarketData(self):
        response = requests.get(self.url+'/api/market/goods' , params=self.params, headers=self.header)
        if response.status_code == 200:
            payload = response.json().get('data', {})
            skin_data = payload.get('items', [])
            self.skins = [Skin_Buff(**data) for data in skin_data]
            page = payload.get('page_num', 0)
            page_count = payload.get('total_page', 0)
            while (page < page_count):
                params = {
                    "game" : "csgo",
                    "page_size" : "80",
                    "page_num" : page+1,
                }
                print("Updating Page "+ str(page+1) + " of " + str(page_count))
                response = requests.get(self.url+'/api/market/goods' , params=params, headers=self.header)
                if response.status_code == 200:
                    print("Success")
                    payload = response.json().get('data', {})
                    skin_data = payload.get('items', [])
                    self.skins += [Skin_Buff(**data) for data in skin_data]
                    page = payload.get('page_num', 0)
                    page_count = payload.get('total_page', 0)
                else:
                    print(f"Request failed with status code {response.status_code}")
                    
    def getPrice(self, itemname):
        item = None
        for i in self.skins:
            if(i.market_hash_name == itemname):
                item = i
        if item is not None:
            return item.sell_min_price * self.exchange_rate
        else:
            return None
        
    def writeToFile(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.skins, file, default=lambda x: x.__dict__, indent=4)

    def readFromFile(self):
        with open(self.file_path, 'r') as file:
            skins_data = json.load(file)
        for data in skins_data:
            skin = Skin_Buff(**data)
            self.skins.append(skin)