import os
from Market_Skinout import Skinout
from Market_Buff import Buff
from Market_Skinport import Skinport
from Market_Steam import Steam
from Market_Bitskins import Bitskins
import csv

# Read from Skin_names.txt for the skins names to be analyzed
def readSkinNames():
    skinList = []
    with open("skins_names.txt", "r") as file:
        for line in file:
            skinList.append(line.strip())
    return skinList

# Read from app.conf for the cookie and other possible settings
def getSettings():
    required_fields = ["Cookie"]
    settings = {}
    with open("app.conf", "r") as file:
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
        os.makedirs("Output")
    if not os.path.exists("app.conf"):
        with open("app.conf", "w") as file:
            file.write("Cookie: \n")


initializeDirectory()
appSettings = getSettings()

buff = Buff(appSettings["Cookie"])
skinport = Skinport()
steam = Steam()
# bitskins = Bitskins()
skinout = Skinout()


Markets = [skinout, buff, skinport, steam]


# UI for the program that allows the user to select buy markets and sell markets, and then prompts the user to select which of those markets to update with new data. Depending on selection, the program will update the data for the selected markets and then generate the profit summary and CSV file.

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
                        print ("Writing " + Markets[i].__class__.__name__ + " data to file")
                        Markets[i].writeToFile()
                else:
                    for i in buy_markets:
                        Markets[i].readFromFile()
                if updateSellMarkets == "y":
                    for i in sell_markets:
                        Markets[i].initializeMarketData()
                        print ("Writing " + Markets[i].__class__.__name__ + " data to file")
                        Markets[i].writeToFile()
                else:
                    for i in sell_markets:
                        Markets[i].readFromFile()

                print ("Starting analysis...")
                # Read the skins names file and store the names in a list. Then, for each skin name, get the price from each of the selected buy markets and then store only the lowest price and the market it came from. Then, for every skin that made it into the list, get the price from each of the selected sell markets and then store only the highest price and the market it came from. 
                skinsList = readSkinNames()
                profitSummary = []
                buyPrice = []
                for skinName in skinsList:
                    skinPrice = []
                    for i in buy_markets:
                        price = Markets[i].getPrice(skinName)
                        if price is not None:
                            skinPrice.append({"name": skinName,"market": type(Markets[i]), "price": price})
                    if skinPrice:
                        minPrice = min(skinPrice, key=lambda x: x["price"])
                        buyPrice.append(minPrice)
                
                for skin in buyPrice:
                    skinPrice = []
                    for i in sell_markets:
                        price = Markets[i].getPrice(skin["name"])
                        if price is not None:
                            skinPrice.append({"name": skin["name"],"market": type(Markets[i]), "price": price})
                    if skinPrice:
                        maxPrice = max(skinPrice, key=lambda x: x["price"])
                        profitSummary.append(
                            {
                                "Name": skin["name"],
                                "Relative Profit": (maxPrice["price"] / skin["price"]),
                                "Profit": (maxPrice["price"] - skin["price"]),
                                "Buy Market": skin["market"].__name__,
                                "Buy Price": skin["price"],
                                "Sell Market": maxPrice["market"].__name__,
                                "Sell Price": maxPrice["price"],
                            }
                        )
                

                sortedProfitSummary = sorted(
                    profitSummary, key=lambda x: x["Relative Profit"], reverse=True
                )
                
                print ("Analysis complete. Generating CSV file...")

                # Generate a CSV file with the following columns: Name, Relative Profit, Profit, Buy Market, Buy Price, Sell Market, Sell Price.
                # Sort the rows by Relative Profit in descending order.
                # Only include rows where Profit > 0 and Buy Market != "Buff"

                # Assuming sortedProfitSummary is the list containing the profit summary data

                filteredSummary = [
                    row
                    for row in sortedProfitSummary
                    if row["Profit"] > 0 and row["Buy Market"] != "Buff"
                ]

                csv_file = "Output/profit_summary.csv"

                with open(csv_file, mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=["Name", "Relative Profit", "Profit", "Buy Market", "Buy Price", "Sell Market", "Sell Price"])
                    writer.writeheader()
                    writer.writerows(filteredSummary)
        case "4":
            steam.initializeMarketData()
            steam.writeToFile()
            steam.writeSkinNamesToFile()
        case "5":
            keepGoingMenu = False