import time
import requests
import pandas as pd
import concurrent.futures
from abc import ABC, abstractmethod


class Market_Base(ABC):
    @abstractmethod
    def __init(self):
        pass
    
    @abstractmethod
    def initializeMarketData(self):
        pass

## API Reverse Engineered.

class Buff163():
    def __init__(self, cookie) -> None:
        self.url = "https://buff.163.com"
        self.header = {"Cookie": str(cookie)}
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
            
## API Reverse Engineered.
class Skinout():
    def __init__(self) -> None:
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
            
            
def create_market(market_name: str):
    match market_name.lower():
        case 'skinout':
            return Skinout()
        case 'buff163':
            return Buff163()
        case _:
            raise ValueError(f"Unknown market: {market_name}")