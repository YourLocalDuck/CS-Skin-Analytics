from typing import List
import pandas as pd
from Market_Base import Market_Base

class Generate_Analysis:
    def __init__(self, buy_markets: List[Market_Base], sell_markets: List[Market_Base]):
        self.buy_markets = buy_markets
        self.sell_markets = sell_markets
        
    # Read from Skin_names.txt for the skins names to be analyzed
    def readSkinNames():
        skinList = []
        with open("skins_names.txt", "r", encoding="utf-8") as file:
            for line in file:
                skinList.append(line.strip())
        return skinList
    
    def getData(self):
        buyMarketItemData = []
        sellMarketItemData = []
        for market in self.buy_markets:
            buyMarketItemData.append(market.formatData())
        for market in self.sell_markets:
            sellMarketItemData.append(market.formatData())
                
        
    def sortData(self):
        pass
    
    def generateAnalysis(self, itemname):
        price = self.market.getPrice(itemname)
        sale_price = self.market.getSalePrice(itemname)
        unlock_time = self.market.getUnlockTime(itemname)
        return pd.DataFrame(
            {
                "Item": [itemname],
                "Price": [price],
                "Sale Price": [sale_price],
                "Unlock Time": [unlock_time],
            }
        )
        