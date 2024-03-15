from functools import lru_cache
import time
from Market_Base import Market_Base
import json
import requests
import pandas as pd
import concurrent.futures

## API Reverse Engineered.


class Buff(Market_Base):
    def __init__(self, header):
        # Obtain Worth of CNY in USD using exchange-rate-api
        exchange_rates = requests.get("https://open.er-api.com/v6/latest/CNY")
        self.exchange_rate = exchange_rates.json()["rates"]["USD"]

        self.file_path = "Output/buff_data.json"
        self.url = "https://buff.163.com"
        self.header = {"Cookie": str(header)}
        self.params = {
            "game": "csgo",
            "page_size": "80",
            "page_num": "1",
        }
        self.skins = pd.DataFrame()
        
    def doRequest(self, url, params, headers):
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            print(f"Buff: Request failed with status code {response.status_code}")
            return None
        
    def fetchPage(self, page, maxpage):
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                params = {
                    "game": "csgo",
                    "page_size": "80",
                    "page_num": page,
                }
                print(f"Buff: Updating Page {page} of {maxpage}")
                response = self.doRequest(self.url + "/api/market/goods", params, headers=self.header)
                if response is not None:
                    skin_data = response.get("items", [])
                    return pd.DataFrame(skin_data)
                else:
                    print(f"Buff: Failed to fetch page {page}, attempt {attempt + 1}")
            except Exception as e:
                print(f"Buff: Exception occurred while fetching page {page}, attempt {attempt + 1}: {e}")
                time.sleep(attempt)
        while True:        
            print(f"Failed to fetch page {page} after {max_attempts} attempts")
        return None

    def initializeMarketData(self):
        print("Buff: Updating Page 1 of ?")
        payload = self.doRequest(self.url + "/api/market/goods", self.params, self.header)
        if payload is not None:
            skin_data = payload.get("items", [])
            self.skins = pd.DataFrame(skin_data)
            page_count = payload.get("total_page", 0)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future_to_page = {executor.submit(self.fetchPage, page, page_count): page for page in range(2, page_count + 1)}
                for future in concurrent.futures.as_completed(future_to_page):
                    page = future_to_page[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print(f"Buff: Page {page} generated an exception: {exc}")
                    else:
                        self.skins = pd.concat([self.skins, data], ignore_index=True)
        else:
            print(f"Buff: Could not reach API: Request failed")

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
            return float(row["sell_min_price"]) * self.exchange_rate
        
    def salePriceFromPrice(self, price):
        return float(price) * 0.975

    def getSalePrice(self, itemname):
        price = self.getPrice(itemname)
        if price is None:
            return None
        else:
            return self.salePriceFromPrice(price)

    def getUnlockTime(self, itemname):
        return 0
    
    def getFilteredData(self):
        subset = self.skins[["market_hash_name", "sell_min_price"]]
        subset = subset.rename(columns={"market_hash_name": "name", "sell_min_price": "price"})
        subset["price"] = subset["price"] * self.exchange_rate
        subset["unlockTime"] = 0
        subset["SalePrice"] = subset.apply(
                    lambda x: self.salePriceFromPrice(x["price"]), axis=1
                )
        subset["Source Market"] = "Buff"
        return subset

    def writeToFile(self):
        self.skins.to_json(self.file_path, orient="records")

    def readFromFile(self):
        self.skins = pd.read_json(self.file_path, orient="records")

    def writeSkinNamesToFile(self):
        with open("skins_names.txt", "w", encoding="utf-8") as file:
            for index, row in self.skins.iterrows():
                file.write(row["market_hash_name"] + "\n")
