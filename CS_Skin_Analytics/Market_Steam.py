import requests
import time
import json
import pandas as pd

# API Reverse Engineered.

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
        self.file_path = 'Output/steam_data.json'

    def initializeMarketData(self):
        all_skins = []
        response = requests.get(self.url+'/market/search/render/' , params=self.params)
        if response.status_code == 200:
            payload = response.json()
            skin_data = payload.get('results', [])
            self.skins = pd.DataFrame(skin_data)
            skin_start = payload.get('start', 0)
            skin_pagesize = payload.get('pagesize', 0)
            skin_total_count = payload.get('total_count', 0)
            while ((skin_start + skin_pagesize) < skin_total_count):
                params = {
                "query": "appid:730",
                "start": skin_start + skin_pagesize,
                "count": 100,
                "norender": 1,
                }
                print("Updating Item "+ str(skin_start+skin_pagesize) + " of " + str(skin_total_count))
                response = requests.get(self.url+'/market/search/render/' , params=params)
                if response.status_code == 200:
                    print("Success")
                    payload = response.json()
                    skin_data = payload.get('results', [])
                    all_skins.append(pd.DataFrame(skin_data))
                    skin_start = payload.get('start', 0)
                    skin_pagesize = payload.get('pagesize', 0)
                    skin_total_count = payload.get('total_count', 0)
                else:
                    print(f"Request failed with status code {response.status_code}")
                    if {response.status_code == 429}:
                        print("Hit Rate Limit. Waiting 5 minutes...")
                        time.sleep(300)
            self.skins = pd.concat(all_skins, ignore_index=True)
                
        else:
            print(f"Request failed with status code {response.status_code}")
            if {response.status_code == 429}:
                print("Hit Rate Limit. Waiting 5 minutes.")
                time.sleep(300)
                self.initializeMarketData()
                
    def getPrice(self, itemname):
        # Look for a row with the item name, and if it exists, return the price. Otherwise, return None.
        row = self.skins.loc[self.skins['hash_name'] == itemname]
        if row.empty:
            return None
        else:
            return float(row.iloc[0]['sell_min_price']) * .01
    
    def writeToFile(self) -> None:
        self.skins.to_json(self.file_path, orient='records')
            
    def readFromFile(self) -> None:
        self.skins = pd.read_json(self.file_path, orient='records')
            
    def writeSkinNamesToFile(self) -> None:
        with open('skins_names.txt', 'w', encoding='utf-8') as file:
            for index, row in self.skins.iterrows():
                file.write(row['hash_name'] + '\n')