from functools import lru_cache
import time
from Market_Base import Market_Base
import requests
import pandas as pd
import concurrent.futures

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
        
    def doRequest(self, url, params):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
        
    def fetchPage(self, page, maxpage):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                params = {
                    "sort": "popularity_desc",
                    "page": page,
                }
                print(f"Updating Page {page} of {maxpage}")
                response = self.doRequest(self.url + "/api/market/items", params)
                if response is not None:
                    skin_data = response.get("items", [])
                    return pd.DataFrame(skin_data)
                else:
                    print(f"Failed to fetch page {page}, attempt {attempt + 1}")
            except Exception as e:
                print(f"Exception occurred while fetching page {page}, attempt {attempt + 1}: {e}")
        print(f"Failed to fetch page {page} after {max_attempts} attempts")
        return None

    def initializeMarketData(self):
        response = self.doRequest(self.url + "/api/market/items", self.params)
        if response is not None:
            payload = response
            skin_data = payload.get("items", [])
            self.skins = pd.DataFrame(skin_data)
            page_count = payload.get("page_count", 0)

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_page = {executor.submit(self.fetchPage, page, page_count): page for page in range(2, page_count + 1)}
                for future in concurrent.futures.as_completed(future_to_page):
                    page = future_to_page[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print(f"Page {page} generated an exception: {exc}")
                    else:
                        self.skins = pd.concat([self.skins, data], ignore_index=True)
        else:
            print(f"Could not reach API: Request failed")

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
