from abc import ABC, abstractmethod
import pandas as pd
import requests
from django.conf import settings
import sqlalchemy


class Market_Base(ABC):
    @abstractmethod
    def readFromDB(self):
        pass
    
    @abstractmethod
    def getFilteredData(self):
        pass
    
class Buff163(Market_Base):
    # Initialize conversion rate, and db from which to read data.
    def __init__(self, dbEngine, params) -> None:
        exchange_rates = requests.get("https://open.er-api.com/v6/latest/CNY")
        self.exchange_rate = exchange_rates.json()["rates"]["USD"]
        self.skins = pd.DataFrame()
        self.dbEngine = dbEngine
        self.readFromDB(params)
    
    # Read the latest data from the database into a dataframe.
    def readFromDB(self, params):
        query = "SELECT DISTINCT ON (market_hash_name) * FROM buff163_data WHERE 1=1"
        
        query_params = {}
        
        if 'min_price' in params:
            query += " AND sell_min_price >= %(min_price)s"
            query_params['min_price'] = params['min_price']
        if 'max_price' in params:
            query += " AND sell_min_price <= %(max_price)s"
            query_params['max_price'] = params['max_price']
            
        query += " ORDER BY market_hash_name, created_at DESC;"
        self.skins = pd.read_sql(query, self.dbEngine, params=query_params)
        
    # Format data for use in the application.
    def getFilteredData(self):
        subset = self.skins[["market_hash_name", "sell_min_price"]]
        subset = subset.rename(
            columns={"market_hash_name": "name", "sell_min_price": "price"}
        )
        subset["price"] = subset["price"] * self.exchange_rate
        subset["unlockTime"] = 0
        subset["SalePrice"] = subset.apply(
            lambda x: self.salePriceFromPrice(x["price"]), axis=1
        )
        subset["Source Market"] = "Buff"
        return subset
    
class Skinout(Market_Base):
    def __init__(self, dbEngine, params) -> None:
        self.skins = pd.DataFrame()
        self.dbEngine = dbEngine
        self.readFromDB(params)
        
    def readFromDB(self, params):
        query = "SELECT DISTINCT ON (market_hash_name) * FROM skinout_data WHERE 1=1"
        query_params = {}
        
        if 'min_price' in params:
            query += " AND price >= %(min_price)s"
            query_params['min_price'] = params['min_price']
        if 'max_price' in params:
            query += " AND price <= %(max_price)s"
            query_params['max_price'] = params['max_price']
            
        query += " ORDER BY market_hash_name, created_at DESC;"
        self.skins = pd.read_sql(query, self.dbEngine, params=query_params)
        
    def salePriceFromPrice(self, price):
        return float(price) * 0.9
        
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
    
class Skinport(Market_Base):
    def __init__(self, dbEngine, params) -> None:
        self.skins = pd.DataFrame()
        self.dbEngine = dbEngine
        self.readFromDB(params)
        
    def readFromDB(self, params):
        query = "SELECT DISTINCT ON (market_hash_name) * FROM skinport_data WHERE 1=1"
        query_params = {}
        
        if 'min_price' in params:
            query += " AND min_price >= %(min_price)s"
            query_params['min_price'] = params['min_price']
        if 'max_price' in params:
            query += " AND min_price <= %(max_price)s"
            query_params['max_price'] = params['max_price']
            
        query += " ORDER BY market_hash_name, created_at DESC;"
        self.skins = pd.read_sql(query, self.dbEngine, params=query_params)
        
    def salePriceFromPrice(self, price):
        if price < 1000:
            return float(price) * 0.83
        else:
            return float(price) * 0.94
        
    def getFilteredData(self):
        subset = self.skins[["market_hash_name", "min_price"]]
        subset = subset.rename(
            columns={"market_hash_name": "name", "min_price": "price"}
        )
        subset["unlockTime"] = 0
        subset["SalePrice"] = subset.apply(
            lambda x: self.salePriceFromPrice(x["price"]), axis=1
        )
        subset["Source Market"] = "Skinport"
        return subset
    
class Steam(Market_Base):
    def __init__(self, dbEngine, params) -> None:
        self.skins = pd.DataFrame()
        self.dbEngine = dbEngine
        self.readFromDB(params)
        
    def readFromDB(self, params):
        query = "SELECT DISTINCT ON (hash_name) * FROM steam_data WHERE 1=1"
        query_params = {}
        
        if 'min_price' in params:
            query += " AND sell_price >= %(min_price)s"
            query_params['min_price'] = params['min_price']
        if 'max_price' in params:
            query += " AND sell_price <= %(max_price)s"
            query_params['max_price'] = params['max_price']
            
        query += " ORDER BY hash_name, created_at DESC;"
        self.skins = pd.read_sql(query, self.dbEngine, params=query_params)
        
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
    
def getDBEngine():
    connStr = 'postgresql+psycopg2://'+settings.DATABASES.get('default').get('USER')+':'+settings.DATABASES.get('default').get('PASSWORD')+'@'+settings.DATABASES.get('default').get('HOST')+':'+settings.DATABASES.get('default').get('PORT')+'/'+settings.DATABASES.get('default').get('NAME')
    connStr = connStr.replace("%", "%25")
    return sqlalchemy.create_engine(connStr) 
                     
def marketFactory(market_dict: dict):
    try:
        engine = getDBEngine()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return None
    
    match market_dict.get('market').lower():
        case 'skinout':
            return Skinout(engine, market_dict.get('params'))
        case 'buff163':
            return Buff163(engine, market_dict.get('params'))
        case 'skinport':
            return Skinport(engine, market_dict.get('params'))
        case 'steam':
            return Steam(engine, market_dict.get('params'))
        case _:
            raise ValueError(f"Unknown market: {market_dict.get('name')}")