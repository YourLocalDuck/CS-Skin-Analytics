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
        skinsList = self.readSkinNames()
        buyMarketItemData = [pd.DataFrame(columns=["Item", "Price", "Sale Price", "Unlock Time"])]
                  
        
    def sortData(self):
        print("Sorting prices...")
        # Read the skins names file and store the names in a list. Then, for each skin name, get the price
        # from each of the selected buy markets and then store only the lowest price and the market it came
        # from. Then, for every skin that made it into the list, get the price from each of the selected sell
        # markets and then store only the highest price and the market it came from.
        tempSummary = []
        buy_prices = []
        skinsList = self.readSkinNames()
        profitSummary = pd.DataFrame(
                    columns=[
                        "Name",
                        "Buy Market",
                        "Buy Price",
                        "Sell Market",
                        "Sell Price",
                    ]
                )
        for skinName in skinsList:
            skinPrice = []
            for market in self.buy_markets:
                price = market.getPrice(skinName)
                unlockTime = market.getUnlockTime(skinName)
                if price is not None:
                    skinPrice.append(
                        {
                            "name": skinName,
                            "market": type(market),
                            "price": price,
                            "unlockTime": unlockTime,
                        }
                    )
            if skinPrice:
                minPrice = min(skinPrice, key=lambda x: x["price"])
                buy_prices.append(minPrice)
                
        for skin in buy_prices:
            skinPrice = []
            for market in self.sell_markets:
                price = market.getSalePrice(skin["name"])
                if price is not None:
                    skinPrice.append(
                        {
                            "name": skin["name"],
                            "market": type(market),
                            "price": price,
                        }
                    )
            if skinPrice:
                maxPrice = max(skinPrice, key=lambda x: x["price"])
                tempSummary.append(
                    pd.DataFrame(
                        {
                            "Name": skin["name"],
                            "Buy Market": skin["market"].__name__,
                            "Buy Price": skin["price"],
                            "Sell Market": maxPrice["market"].__name__,
                            "Sell Price": maxPrice["price"],
                            "Unlock Time": skin["unlockTime"],
                        },
                        index=[0],
                    )
                )  # idk what the index does but it works

        profitSummary = pd.concat(tempSummary, ignore_index=True)
        return profitSummary

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
        