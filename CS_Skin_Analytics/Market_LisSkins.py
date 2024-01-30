from functools import lru_cache
import pandas as pd
from Market_Base import Market_Base

class LisSkins(Market_Base):
    def __init__(self):
        self.file_path = 'Output/lisskins_data.json'
        self.skins = []
        self.readFromFile()
        
    @lru_cache(maxsize=1)
    def _getItemRow(self, itemname):
        row = self.skins.loc[(self.skins['name'] + " " + self.skins['WEAR']) == itemname]
        if row.empty:
            return None
        else:
            return row.iloc[0]
        
    def getPrice(self, itemname):
        row = self._getItemRow(itemname)
        if row is None:
            return None
        else:
            return float(row['price'][:-1])
        
    def getSalePrice(self, itemname):
        price = self.getPrice(itemname)
        if price is None:
            return None
        else:
            return price * 0.9
    
    def getUnlockTime(self, itemname):
        row = self._getItemRow(itemname)
        if row is None:
            return None
        else:
            unlock_time = row['unlockTime']
            if not unlock_time:
                return 0
            if "days" in unlock_time:
                return int(unlock_time.split(" ")[0])
            elif "hours" in unlock_time:
                return 1
            elif "min" in unlock_time:
                return 0
            else:
                return None
    
    def initializeMarketData(self, itemname): 
        return 0
        
    def readFromFile(self):
        self.skins = pd.read_json(self.file_path, orient='records')

    def writeToFile(self): # Do something with this
        return