import os
from typing import List
from Market_LisSkins import LisSkins
from Market_Base import Market_Base
from Market_Skinout import Skinout
from Market_Buff import Buff
from Market_Skinport import Skinport
from Market_Steam import Steam
from Market_Bitskins import Bitskins
import pandas as pd
import csv


# Read from Skin_names.txt for the skins names to be analyzed
def readSkinNames():
    skinList = []
    with open("skins_names.txt", "r", encoding="utf-8") as file:
        for line in file:
            skinList.append(line.strip())
    return skinList


# Read from app.conf for the cookie and other possible settings
def getSettings():
    required_fields = ["Cookie"]
    settings = {}
    with open("app.conf", "r", encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split(": ")
            settings[key] = value

    for field in required_fields:
        if field not in settings:
            raise ValueError(f"Required field {field} not found in app.conf")

    return settings


# Create the Output directory if it doesn't exist. Create the app.conf file if it doesn't exist.
def initializeDirectory():
    if not os.path.exists("Output"):
        print("Output directory not found. Creating directory...")
        os.makedirs("Output")
    if not os.path.exists("app.conf"):
        print("app.conf not found. Creating file...")
        with open("app.conf", "w", encoding="utf-8") as file:
            file.write("Cookie: (Insert Cookie Here)\n")
        input("Please insert your cookie into app.conf and then press enter")


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


def getGrowthRate(days):
    if days <= 8:
        return growthRates.loc[growthRates["Days"] == days].iloc[0]["Growth Rate"]
    else:
        return None


initializeDirectory()
appSettings = getSettings()

buff = Buff(appSettings["Cookie"])
skinport = Skinport()
steam = Steam()
lisskins = LisSkins()
skinout = Skinout()


Markets: List[Market_Base] = [skinout, buff, skinport, steam, lisskins]


# UI for the program that allows the user to select buy markets and sell markets, and then prompts the user to select
# which of those markets to update with new data. Depending on selection, the program will update the data for the
# selected markets and then generate the profit summary and CSV file.

buy_markets = None
sell_markets = None
updateBuyMarkets = None
updateSellMarkets = None
keepGoingMenu = True
while keepGoingMenu:
    print("Please select an option:")
    print("1. Select buy markets")
    print("2. Select sell markets")
    print("3. Generate profit summary")
    print("4. Generate Skins Names file")
    print("5. Exit")

    option = input("Enter option number: ")
    match option:
        case "1":
            keepGoing = True
            while keepGoing:
                print("Select buy markets:")
                for i in range(len(Markets)):
                    print(f"{i + 1}. {Markets[i].__class__.__name__}")
                buy_markets = input("Enter comma-separated list of numbers: ")
                buy_markets = [int(i) - 1 for i in buy_markets.split(",")]
                if all([i in range(len(Markets)) for i in buy_markets]):
                    keepGoing = False
                    print("Would you like to update the selected markets? (y/n)")
                    updateBuyMarkets = input("Enter option: ")
                else:
                    print("Invalid input. Please try again.")

        case "2":
            keepGoing = True
            while keepGoing:
                print("Select sell markets:")
                for i in range(len(Markets)):
                    print(f"{i + 1}. {Markets[i].__class__.__name__}")
                sell_markets = input("Enter comma-separated list of numbers: ")
                sell_markets = [int(i) - 1 for i in sell_markets.split(",")]
                if all([i in range(len(Markets)) for i in sell_markets]):
                    keepGoing = False
                    print("Would you like to update the selected markets? (y/n)")
                    updateSellMarkets = input("Enter option: ")
                else:
                    print("Invalid input. Please try again.")

        case "3":
            if buy_markets is not None and sell_markets is not None:
                if updateBuyMarkets == "y":
                    for i in buy_markets:
                        Markets[i].initializeMarketData()
                        print(
                            "Writing " + Markets[i].__class__.__name__ + " data to file"
                        )
                        Markets[i].writeToFile()
                else:
                    for i in buy_markets:
                        Markets[i].readFromFile()
                if updateSellMarkets == "y":
                    for i in sell_markets:
                        Markets[i].initializeMarketData()
                        print(
                            "Writing " + Markets[i].__class__.__name__ + " data to file"
                        )
                        Markets[i].writeToFile()
                else:
                    for i in sell_markets:
                        Markets[i].readFromFile()

                print("Sorting prices...")
                # Read the skins names file and store the names in a list. Then, for each skin name, get the price
                # from each of the selected buy markets and then store only the lowest price and the market it came
                # from. Then, for every skin that made it into the list, get the price from each of the selected sell
                # markets and then store only the highest price and the market it came from.
                skinsList = readSkinNames()
                profitSummary = pd.DataFrame(
                    columns=[
                        "Name",
                        "Buy Market",
                        "Buy Price",
                        "Sell Market",
                        "Sell Price",
                    ]
                )
                tempSummary = []
                buyPrice = []
                for skinName in skinsList:
                    skinPrice = []
                    for i in buy_markets:
                        price = Markets[i].getPrice(skinName)
                        unlockTime = Markets[i].getUnlockTime(skinName)
                        if price is not None:
                            skinPrice.append(
                                {
                                    "name": skinName,
                                    "market": type(Markets[i]),
                                    "price": price,
                                    "unlockTime": unlockTime,
                                }
                            )
                    if skinPrice:
                        minPrice = min(skinPrice, key=lambda x: x["price"])
                        buyPrice.append(minPrice)

                for skin in buyPrice:
                    skinPrice = []
                    for i in sell_markets:
                        price = Markets[i].getSalePrice(skin["name"])
                        if price is not None:
                            skinPrice.append(
                                {
                                    "name": skin["name"],
                                    "market": type(Markets[i]),
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
                print("Starting Analysis...")
                profitSummary["Relative Profit"] = profitSummary.apply(
                    lambda x: x["Sell Price"] / x["Buy Price"], axis=1
                )
                profitSummary["Profit"] = profitSummary.apply(
                    lambda x: x["Sell Price"] - x["Buy Price"], axis=1
                )
                profitSummary["Time Efficiency"] = profitSummary.apply(
                    lambda x: x["Relative Profit"]
                    / (getGrowthRate(x["Unlock Time"]))
                    * 100,
                    axis=1,
                )

                profitSummary.sort_values(
                    by=["Time Efficiency"], ascending=False, inplace=True
                )

                print("Analysis complete. Generating CSV file...")

                # Generate a CSV file with the following columns: Name, Relative Profit, Profit, Buy Market,
                # Buy Price, Sell Market, Sell Price.
                profitSummary.to_csv("Output/profit_summary.csv", index=False)

        case "4":
            buff.initializeMarketData()
            buff.writeToFile()
            buff.writeSkinNamesToFile()
        case "5":
            keepGoingMenu = False
