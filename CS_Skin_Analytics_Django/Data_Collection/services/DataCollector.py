import json
import time
import requests
import pandas as pd
import concurrent.futures
from abc import ABC, abstractmethod
from django.conf import settings
import sqlalchemy


class Market_Base(ABC):
    @abstractmethod
    def initializeMarketData(self):
        pass
    
    @abstractmethod
    def writeToDB(self):
        pass

## API Reverse Engineered.

class Buff163(Market_Base):
    def __init__(self, cookie, dbEngine) -> None:
        # Obtain Worth of CNY in USD using exchange-rate-api
        exchange_rates = requests.get("https://open.er-api.com/v6/latest/CNY")
        self.exchange_rate = exchange_rates.json()["rates"]["USD"]
        
        self.url = "https://buff.163.com"
        self.header = {"Cookie": str(cookie)}
        self.params = {
            "game": "csgo",
            "page_size": "80",
            "page_num": "1",
        }
        self.skins = pd.DataFrame()
        self.dbEngine = dbEngine

    def doRequest(self, url, params, headers):
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            print(f"Buff: Request failed with status code {response.status_code}")
            return None

    def fetchPage(self, page, maxpage, pages):
        if page not in pages:
            return None
        else:
            pages.remove(page)
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                params = {
                    "game": "csgo",
                    "page_size": "80",
                    "page_num": page,
                }
                print(f"Buff: Updating Page {page} of {maxpage}")
                response = self.doRequest(
                    self.url + "/api/market/goods", params, headers=self.header
                )
                if response is not None:
                    skin_data = response.get("items", [])
                    return pd.DataFrame(skin_data)
                else:
                    print(f"Buff: Failed to fetch page {page}, attempt {attempt + 1}")
                    time.sleep(attempt)
            except Exception as e:
                print(
                    f"Buff: Exception occurred while fetching page {page}, attempt {attempt + 1}: {e}"
                )
                time.sleep(attempt)
                
        print(f"Buff: Failed to fetch page {page} after {max_attempts} attempts")
        return None

    def initializeMarketData(self):
        print("Buff: Updating Page 1 of ?")
        payload = self.doRequest(
            self.url + "/api/market/goods", self.params, self.header
        )
        if payload is not None:
            skin_data = payload.get("items", [])
            self.skins = pd.DataFrame(skin_data)
            page_count = payload.get("total_page", 0)
            pages = list(range(2, page_count + 1))

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future_to_page = {
                    executor.submit(self.fetchPage, page, page_count, pages): page
                    for page in range(2, page_count + 1)
                }
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
            
    def writeToDB(self):
        dataToWrite = self.skins.drop(columns=["appid", "bookmarked", "can_search_by_tournament", "description", "game", "goods_info", "has_buff_price_history", "name", "short_name", "steam_market_url"])
        dataToWrite = dataToWrite.sort_values(by=["market_hash_name"], ascending=[True])
        dataToWrite = dataToWrite.rename(columns={"id": "item_id"})
        dataToWrite = dataToWrite.drop_duplicates(subset=["market_hash_name"]) # Remove duplicates, need to check if this is the best way to do this.
        try:
            dataToWrite.to_sql(
                "buff163_data", self.dbEngine, if_exists="append", index=False
            )
        except Exception as e:
            print(f"Buff: Failed to write to database: {e}")
            
## API Reverse Engineered.
class Skinout(Market_Base):
    def __init__(self, dbEngine) -> None:
        self.url = "https://skinout.gg"
        self.params = {
            "sort": "popularity_desc",
            "page": 1,
        }
        self.skins = pd.DataFrame()
        self.dbEngine = dbEngine
        
    def doRequest(self, url, params):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Skinout: Request failed with status code {response.status_code}")
            return None

    def fetchPage(self, page, maxpage, pages):
        if page not in pages:
            return None
        else:
            pages.remove(page)
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                params = {
                    "sort": "popularity_desc",
                    "page": page,
                }
                print(f"Skinout: Skinout: Updating Page {page} of {maxpage}")
                response = self.doRequest(self.url + "/api/market/items", params)
                if response is not None:
                    skin_data = response.get("items", [])
                    return pd.DataFrame(skin_data)
                else:
                    print(
                        f"Skinout: Failed to fetch page {page}, attempt {attempt + 1}"
                    )
            except Exception as e:
                print(
                    f"Skinout: Exception occurred while fetching page {page}, attempt {attempt + 1}: {e}"
                )
                time.sleep(attempt)

        print(f"Skinout: Failed to fetch page {page} after {max_attempts} attempts")
        return None

    def initializeMarketData(self):
        print("Skinout: Updating Page 1 of ?")
        response = self.doRequest(self.url + "/api/market/items", self.params)
        if response is not None:
            payload = response
            skin_data = payload.get("items", [])
            self.skins = pd.DataFrame(skin_data)
            page_count = payload.get("page_count", 0)
            pages = list(range(2, page_count + 1))

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_page = {
                    executor.submit(self.fetchPage, page, page_count, pages): page
                    for page in range(2, page_count + 1)
                }
                for future in concurrent.futures.as_completed(future_to_page):
                    page = future_to_page[future]
                    try:
                        data = future.result()
                    except Exception as exc:
                        print(f"Page {page} generated an exception: {exc}")
                    else:
                        self.skins = pd.concat([self.skins, data], ignore_index=True)
        else:
            print(f"Skinout: Could not reach API: Request failed")
            
    def writeToDB(self):
        dataToWrite = self.skins.drop(columns=["name", "name_id", "img", "in_cart"])
        dataToWrite["stickers"] = dataToWrite["stickers"].apply(json.dumps)
        dataToWrite = dataToWrite.sort_values(by=["market_hash_name"], ascending=[True])
        dataToWrite = dataToWrite.rename(columns={"id": "item_id"})
        dataToWrite = dataToWrite.drop_duplicates(subset=["market_hash_name"]) # Remove duplicates, need to check if this is the best way to do this.
        try:
            dataToWrite.to_sql(
                "skinout_data", self.dbEngine, if_exists="append", index=False
            )
        except Exception as e:
            print(f"Skinout: Failed to write to database: {e}")
            
class Skinport(Market_Base):
    def __init__(self, dbEngine) -> None:
        self.file_path = "Output/skinport_data.json"
        self.url = "https://api.skinport.com"
        self.params = {
            "app_id": 730,
            "currency": "USD",
        }
        self.dbEngine = dbEngine

    def initializeMarketData(self):
        print("Skinport: Updating Page 1 of 1")
        response = requests.get(self.url + "/v1/items", params=self.params)
        if response.status_code == 200:
            payload = response.json()
            self.skins = pd.DataFrame(payload)
        else:
            print(f"Request failed with status code {response.status_code}")
            
    def writeToDB(self):
        dataToWrite = self.skins.drop(columns=["currency", "item_page", "market_page", "created_at", "updated_at"])
        try:
            dataToWrite.to_sql(
                "skinport_data", self.dbEngine, if_exists="append", index=False
            )
        except Exception as e:
            print(f"Skinport: Failed to write to database: {e}")
            
class Steam(Market_Base):
    def __init__(self, dbEngine) -> None:
        self.url = "https://steamcommunity.com"
        self.params = {
            "query": "appid:730",
            "start": 0,
            "count": 100,
            "norender": 1,
        }
        self.skins = []
        self.file_path = "Output/steam_data.json"
        self.dbEngine = dbEngine

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
                
    def writeToDB(self) -> None:
        dataToWrite = self.skins.drop(columns=["name", "app_icon", "app_name", "asset_description", "extra", "sell_price_text"])
        dataToWrite = dataToWrite.drop_duplicates(subset=["hash_name"])
        try:
            dataToWrite.to_sql(
                "steam_data", self.dbEngine, if_exists="append", index=False
            )
        except Exception as e:
            print(f"Steam: Failed to write to database: {e}")
            
def getDBEngine():
    connStr = 'postgresql+psycopg2://'+settings.DATABASES.get('default').get('USER')+':'+settings.DATABASES.get('default').get('PASSWORD')+'@'+settings.DATABASES.get('default').get('HOST')+':'+settings.DATABASES.get('default').get('PORT')+'/'+settings.DATABASES.get('default').get('NAME')
    connStr = connStr.replace("%", "%25")
    return sqlalchemy.create_engine(connStr) 
                     
def create_market(market_dict: dict):
    try:
        engine = getDBEngine()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return None
    
    match market_dict.get('name').lower():
        case 'skinout':
            return Skinout(engine)
        case 'buff163':
            return Buff163(market_dict.get('cookie'), engine)
        case 'skinport':
            return Skinport(engine)
        case 'steam':
            return Steam(engine)
        case _:
            raise ValueError(f"Unknown market: {market_dict.get('name')}")