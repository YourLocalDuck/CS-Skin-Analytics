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
        df = pd.concat(self.buyMarketItemData)
        df.to_csv("test3.csv")
        print(df)