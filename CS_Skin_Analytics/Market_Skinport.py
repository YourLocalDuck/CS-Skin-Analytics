from functools import lru_cache
from Market_Base import Market_Base
import json
import requests
import pandas as pd


class Skinport(Market_Base):
    def __init__(self):
        self.file_path = "Output/skinport_data.json"
        self.url = "https://api.skinport.com"
        self.params = {
            "app_id": 730,
            "currency": "USD",
        }

    def initializeMarketData(self):
        response = requests.get(self.url + "/v1/items", params=self.params)
        if response.status_code == 200:
            payload = response.json()
            self.skins = pd.DataFrame(payload)
        else:
            print(f"Request failed with status code {response.status_code}")

    @lru_cache(maxsize=1)
    def _getItemRow(self, itemname):
        row = self.skins.loc[self.skins["market_hash_name"] == itemname]
        if row.empty:
            return None
        else:
            return row.iloc[0]

    def getPrice(self, itemname):
        row = self._getItemRow(itemname)
        if row is None:
            return None
        else:
            return float(row["min_price"])

    def getSalePrice(self, itemname):
        price = self.getPrice(itemname)
        if price is None:
            return None
        elif price < 1000:
            return price * 0.83
        else:
            return price * 0.94

    def getUnlockTime(self, itemname):
        return 0

    def writeToFile(self):
        self.skins.to_json(self.file_path, orient="records")

    def readFromFile(self):
        self.skins = pd.read_json(self.file_path, orient="records")
