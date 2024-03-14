from functools import lru_cache
from Market_Base import Market_Base
import requests
import pandas as pd

## API Reverse Engineered.


class Skinout(Market_Base):
    def __init__(self) -> None:
        self.file_path = "Output/skinout_data.json"
        self.url = "https://skinout.gg"
        self.params = {
            "sort": "popularity_desc",
            "page": 1,
        }
        self.skins = pd.DataFrame()

    def initializeMarketData(self):
        all_skins = []
        print("Updating Page " + "1 of ?")
        response = requests.get(self.url + "/api/market/items", params=self.params)
        if response.status_code == 200:
            payload = response.json()
            skin_data = payload.get("items", [])
            self.skins = pd.DataFrame(skin_data)
            page = payload.get("page", 0)
            page_count = payload.get("page_count", 0)
            while page < page_count:
                params = {
                    "sort": "popularity_desc",
                    "page": page + 1,
                }
                print("Updating Page " + str(page + 1) + " of " + str(page_count))
                response = requests.get(self.url + "/api/market/items", params=params)
                if response.status_code == 200:
                    print("Success")
                    payload = response.json()
                    skin_data = payload.get("items", [])
                    all_skins.append(pd.DataFrame(skin_data))
                    page = payload.get("page", 0)
                    page_count = payload.get("page_count", 0)
                else:
                    print(f"Request failed with status code {response.status_code}")
            self.skins = pd.concat(all_skins, ignore_index=True)
        else:
            print(f"Could not reach API: Request failed with status code {response.status_code}")

    @lru_cache(maxsize=1)
    def _getItemRow(self, itemname):
        row = self.skins.loc[self.skins["name"] == itemname]
        if row.empty:
            return None
        else:
            return row.iloc[0]

    def getPrice(self, itemname):
        row = self._getItemRow(itemname)
        if row is None:
            return None
        else:
            return float(row["price"])

    def salePriceFromPrice(self, price):
        return float(price) * 0.9

    def getSalePrice(self, itemname):
        price = self.getPrice(itemname)
        if price is None:
            return None
        else:
            return self.salePriceFromPrice(price)

    def formattedUnlockTime(self, unlock_time):
        if unlock_time == False:
            return 0
        if "days" in unlock_time:
            return int(unlock_time.split(" ")[0])
        elif "hours" in unlock_time:
            return 1
        elif "min" in unlock_time:
            return 0
        else:
            return None

    def getUnlockTime(self, itemname):
        # Unlock time will be in the dataframe as a string. It will be formatted like "8 days" or "11 hours". Convert this to an integer representing the number of hours until the item is unlocked.
        row = self._getItemRow(itemname)
        if row is None:
            return None
        else:
            unlock_time = row["unlock_time"]
            return self.formattedUnlockTime(unlock_time)

    def getFilteredData(self):
        subset = self.skins[["market_hash_name", "price", "unlock_time"]]
        subset = subset.rename(
            columns={
                "market_hash_name": "name",
                "price": "price",
                "unlock_time": "unlockTime",
            }
        )
        subset["unlockTime"] = subset.apply(
            lambda x: self.formattedUnlockTime(x["unlockTime"]), axis=1
        )
        subset["SalePrice"] = subset.apply(
            lambda x: self.salePriceFromPrice(x["price"]), axis=1
        )
        subset["Source Market"] = "Skinout"
        return subset

    def writeToFile(self):
        self.skins.to_json(self.file_path, orient="records")

    def readFromFile(self):
        self.skins = pd.read_json(self.file_path, orient="records")
