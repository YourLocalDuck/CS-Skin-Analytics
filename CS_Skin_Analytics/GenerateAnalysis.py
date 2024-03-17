from typing import List
import pandas as pd
from Market_Base import Market_Base


class Generate_Analysis:
    def __init__(self, buy_markets: List[Market_Base], sell_markets: List[Market_Base]):
        self.buy_markets = buy_markets
        self.sell_markets = sell_markets
        self.buyMarketItemData = []
        self.sellMarketItemData = []
        self.profitSummary = pd.DataFrame()

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
        self.buyMarketItemData = pd.concat(self.buyMarketItemData)
        for market in self.sell_markets:
            self.sellMarketItemData.append(market.getFilteredData())
        self.sellMarketItemData = pd.concat(self.sellMarketItemData)

    def sortData(self):
        # Lowest Buy Price by finding the minimum price for each item in the buyMarketItemData, and dropping the other entries for that item
        self.buyMarketItemData["price"] = self.buyMarketItemData["price"].astype(float)
        self.buyMarketItemData = (
            self.buyMarketItemData.sort_values(by=["price"], ascending=True)
            .drop_duplicates("name")
            .sort_index()
        )

        # Highest Sell Price by finding the maximum price for each item in the sellMarketItemData, and dropping the other entries for that item
        self.sellMarketItemData["price"] = self.sellMarketItemData["price"].astype(
            float
        )
        self.sellMarketItemData = (
            self.sellMarketItemData.sort_values(by=["price"], ascending=False)
            .drop_duplicates("name")
            .sort_index()
        )

        # Merge the two dataframes on the name column
        self.profitSummary = pd.merge(
            self.buyMarketItemData,
            self.sellMarketItemData,
            on="name",
            how="inner",
            suffixes=("_buy", "_sell"),
        )

    def analyzeData(self):
        # Clean up useless columns, rename columns, and add new columns

        # Clean up useless columns
        self.profitSummary = self.profitSummary.drop(
            columns=["unlockTime_sell", "SalePrice_buy", "price_sell"]
        )

        # Rename columns
        self.profitSummary = self.profitSummary.rename(
            columns={
                "price_buy": "Buy Price",
                "unlockTime_buy": "Unlock Time",
                "SalePrice_sell": "Sell Price",
                "Source Market_buy": "Buy Market",
                "Source Market_sell": "Sell Market",
            }
        )

        # Add analysis columns
        # Profit
        self.profitSummary["Profit"] = (
            self.profitSummary["Sell Price"] - self.profitSummary["Buy Price"]
        )
        # Relative Profit
        self.profitSummary["Relative Profit"] = (
            self.profitSummary["Profit"] / self.profitSummary["Buy Price"]
        )

        # Time Efficiency
        # Input hours and return an expected growth percentage to compute the time efficiency of trades. This data is taken from a compound interest formula with an expected growth rate of 10x per year.
        # Expected growth rate per unit of time has 10 days added to it for 8 days in lock and 2 days to sell.
        growthRates = pd.DataFrame(
            {
                "Days": [0, 1, 2, 3, 4, 5, 6, 7, 8],
                "Growth Rate": [
                    1.06515,
                    1.07186,
                    1.07864,
                    1.08550,
                    1.09240,
                    1.09922,
                    1.10607,
                    1.11292,
                    1.11976,
                ],
            }
        )

        self.profitSummary = pd.merge(
            self.profitSummary,
            growthRates,
            left_on="Unlock Time",
            right_on="Days",
            how="left",
        )

        self.profitSummary["Time Efficiency"] = (
            self.profitSummary["Relative Profit"]
            / self.profitSummary["Growth Rate"]
            * 100
        )

        self.profitSummary = self.profitSummary.drop(columns=["Days", "Growth Rate"])

        # Output File
        self.profitSummary = self.profitSummary.sort_values(
            by=["Time Efficiency"], ascending=False
        )
        self.profitSummary.to_csv("Output/profit_summary.csv", index=False)
