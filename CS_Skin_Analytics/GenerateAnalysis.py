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
        buyMarkets = self.buyMarketItemData[0]  # Start with the first DataFrame
        for df in self.buy_markets[1:]:
            buyMarkets = pd.merge(buyMarkets, df, on='name', how='inner')
        sellMarkets = self.sell_markets[0]  # Start with the first DataFrame
        for df in self.sell_markets[1:]:
            sellMarkets = pd.merge(sellMarkets, df, on='name', how='inner')
        sortedMarkets = pd.merge(buyMarkets, sellMarkets, on="name", how='inner', suffixes=("_B", "_S"))
        return sortedMarkets
