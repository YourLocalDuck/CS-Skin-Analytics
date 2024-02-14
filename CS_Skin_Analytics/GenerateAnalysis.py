from typing import List
import pandas as pd
from Market_Base import Market_Base


class Generate_Analysis:
    def __init__(self, buy_markets: List[Market_Base], sell_markets: List[Market_Base]):
        self.buy_markets = buy_markets
        self.sell_markets = sell_markets
        self.buyMarketItemData = []
        self.sellMarketItemData = []

    # Read from Skin_names.txt for the skins names to be analyzed
    def readSkinNames(self):
        skinList = []
        with open("skins_names.txt", "r", encoding="utf-8") as file:
            for line in file:
                skinList.append(line.strip())
        return skinList

    def getData(self):

        for market in self.buy_markets:
            self.buyMarketItemData.append(market.getFilteredData())
        print(self.buyMarketItemData)
        for market in self.sell_markets:
            self.sellMarketItemData.append(market.getFilteredData())
        print(self.sellMarketItemData)

    def sortData(self):
        buyMarket = pd.DataFrame(self.buyMarketItemData)
        sellMarket = pd.DataFrame(self.sellMarketItemData)
        mergedMarket = pd.merge(buyMarket, sellMarket, on="Item", suffixes=("_B", "_S"))
        return mergedMarket

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
