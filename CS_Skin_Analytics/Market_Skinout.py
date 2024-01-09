import requests
import pandas as pd


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
        all_skins = []
        response = requests.get(self.url+'/api/market/items' , params=self.params)
        if response.status_code == 200:
            payload = response.json()
            skin_data = payload.get('items', [])
            self.skins = pd.DataFrame(skin_data)
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
                    all_skins.append(pd.DataFrame(skin_data))
                    page = payload.get('page', 0)
                    page_count = payload.get('page_count', 0)
                else:
                    print(f"Request failed with status code {response.status_code}")
            self.skins = pd.concat(all_skins, ignore_index=True)
        else: 
            print(f"Request failed with status code {response.status_code}")

    def getPrice(self, itemname):
        # Look for a row with the item name, and if it exists, return the price. Otherwise, return None.
        row = self.skins.loc[self.skins['name'] == itemname]
        if row.empty:
            return None
        else:
            return row.iloc[0]['price']

    def writeToFile(self):
        self.skins.to_json(self.file_path, orient='records')
            
    def readFromFile(self):
        self.skins = pd.read_json(self.file_path, orient='records')
        