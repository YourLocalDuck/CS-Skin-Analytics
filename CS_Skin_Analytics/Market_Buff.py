from functools import lru_cache
import json
import requests
import pandas as pd


## API Reverse Engineered.

class Buff:
    def __init__(self, header):
        # Obtain Worth of CNY in USD using exchange-rate-api
        exchange_rates = requests.get('https://open.er-api.com/v6/latest/CNY')
        self.exchange_rate = exchange_rates.json()['rates']['USD']
        
        self.file_path = 'Output/buff_data.json'
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
        all_skins = []
        response = requests.get(self.url+'/api/market/goods' , params=self.params, headers=self.header)
        if response.status_code == 200:
            payload = response.json().get('data', {})
            skin_data = payload.get('items', [])
            self.skins = pd.DataFrame(skin_data)
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
                    all_skins.append(pd.DataFrame(skin_data))
                    page = payload.get('page_num', 0)
                    page_count = payload.get('total_page', 0)
                else:
                    print(f"Request failed with status code {response.status_code}")
            self.skins = pd.concat(all_skins, ignore_index=True)
            
    @lru_cache(maxsize=1)
    def _getItemRow(self, itemname):
        row = self.skins.loc[self.skins['market_hash_name'] == itemname]
        if row.empty:
            return None
        else:
            return row.iloc[0]
                    
    def getPrice(self, itemname):
        row = self._getItemRow(itemname)
        if row is None:
            return None
        else:
            return float(row['sell_min_price']) * self.exchange_rate
        
    def getSalePrice(self, itemname):
        price = self.getPrice(itemname)
        if price is None:
            return None
        else:
            return price * 0.975
        
    def getUnlockTime(self, itemname):
        return None
        
    def writeToFile(self):
        self.skins.to_json(self.file_path, orient='records')

    def readFromFile(self):
        self.skins = pd.read_json(self.file_path, orient='records')
            
    def writeSkinNamesToFile(self):
        with open('skins_names.txt', 'w', encoding='utf-8') as file:
            for index, row in self.skins.iterrows():
                file.write(row['market_hash_name'] + '\n')