from functools import lru_cache
from Market_Base import Market_Base
import requests
import time
import pandas as pd

# API Reverse Engineered.


class Steam(Market_Base):
    def __init__(self) -> None:
        self.url = "https://steamcommunity.com"
        self.params = {
            "query": "appid:730",
            "start": 0,
            "count": 100,
            "norender": 1,
        }
        self.skins = []
        self.file_path = "Output/steam_data.json"

    def initializeMarketData(self):
        all_skins = []
        print("Steam: Updating Item 1 of ?")
        response = requests.get(self.url + "/market/search/render/", params=self.params)
        if response.status_code == 200:
            payload = response.json()
            skin_data = payload.get("results", [])
            self.skins = pd.DataFrame(skin_data)
            skin_start = payload.get("start", 0)
            skin_pagesize = payload.get("pagesize", 0)
            skin_total_count = payload.get("total_count", 0)
            while (skin_start + skin_pagesize) < skin_total_count:
                params = {
                    "query": "appid:730",
                    "start": skin_start + skin_pagesize,
                    "count": 100,
                    "norender": 1,
                }
                print(
                    "Steam: Updating Item "
                    + str(skin_start + skin_pagesize)
                    + " of "
                    + str(skin_total_count)
                )
                response = requests.get(
                    self.url + "/market/search/render/", params=params
                )
                if response.status_code == 200:
                    payload = response.json()
                    skin_data = payload.get("results", [])
                    all_skins.append(pd.DataFrame(skin_data))
                    skin_start = payload.get("start", 0)
                    skin_pagesize = payload.get("pagesize", 0)
                    skin_total_count = payload.get("total_count", 0)
                else:
                    print(
                        f"Steam: Request failed with status code {response.status_code}"
                    )
                    if {response.status_code == 429}:
                        print("Steam: Hit Rate Limit. Waiting 5 minutes...")
                        time.sleep(300)
            self.skins = pd.concat(all_skins, ignore_index=True)

        else:
            print(f"Steam: Request failed with status code {response.status_code}")
            if {response.status_code == 429}:
                print("Steam: Hit Rate Limit. Waiting 5 minutes.")
                time.sleep(300)
                self.initializeMarketData()

    @lru_cache(maxsize=1)
    def _getItemRow(self, itemname):
        row = self.skins.loc[self.skins["hash_name"] == itemname]
        if row.empty:
            return None
        else:
            return row.iloc[0]

    def getPrice(self, itemname):
        row = self._getItemRow(itemname)
        if row is None:
            return None
        else:
            return float(row["sell_price"]) * 0.01

    def salePriceFromPrice(self, price):
        return float(price) * 0.85

    def getSalePrice(self, itemname):
        price = self.getPrice(itemname)
        if price is None:
            return None
        else:
            return self.salePriceFromPrice(price)

    def getUnlockTime(self, itemname):
        return 0

    def getFilteredData(self):
        subset = self.skins[["hash_name", "sell_price"]]
        subset = subset.rename(columns={"hash_name": "name", "sell_price": "price"})
        subset["price"] = subset.apply(lambda x: float(x["price"]) * 0.01, axis=1)
        subset["unlockTime"] = 0
        subset["SalePrice"] = subset.apply(
            lambda x: self.salePriceFromPrice(x["price"]), axis=1
        )
        subset["Source Market"] = "Steam"
        return subset

    def writeToFile(self) -> None:
        self.skins.to_json(self.file_path, orient="records")

    def readFromFile(self) -> None:
        self.skins = pd.read_json(self.file_path, orient="records")

    def writeSkinNamesToFile(self) -> None:
        with open("skins_names.txt", "w", encoding="utf-8") as file:
            for index, row in self.skins.iterrows():
                file.write(row["hash_name"] + "\n")
