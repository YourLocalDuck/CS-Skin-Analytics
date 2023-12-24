from Market_Skinout import Skinout
from Market_Buff import Buff
from Market_Skinport import Skinport
from Market_Steam import Steam
from Market_Bitskins import Bitskins
import csv


def readSkinNames():
    skinList = []
    with open('skins_names.txt', 'r') as file:
            for line in file:
                skinList.append(line.strip())
    return skinList

def getSettings():
    required_fields = ['Cookie']
    settings = {}
    with open('app.conf', 'r') as file:
        for line in file:
            key, value = line.strip().split(': ')
            settings[key] = value

    for field in required_fields:
        if field not in settings:
            raise ValueError(f"Required field {field} not found in app.conf")

    return settings

appSettings = getSettings()
buff = Buff(appSettings['Cookie'])
buff.initializeMarketData()
buff.writeToFile()
#buff.readFromFile()
#skinport = Skinport()
#steam = Steam()
#bitskins = Bitskins()
skinout = Skinout()
skinout.initializeMarketData()
skinout.writeToFile()
#skinout.readFromFile()
#steam.readFromFile()

Markets = [ skinout, buff ]

#target = r"AK-47 | The Empress (Factory New)"
"""target = r"★ Survival Knife | Scorched (Well-Worn)"

#priceSP = SP.getPrice("10 Year Birthday Sticker Capsule")
#priceB = B.getBuffPrice("10 Year Birthday Sticker Capsule")
#priceS = bitskins.getPrice(target)
S.readFromFile()
#S.initializeMarketData()
#S.writeToFile()

#S.writeSkinNamesToFile()

print(len(S.skins))
priceSteam = S.getPrice(target)
print(priceSteam)
print(readSkinNames())"""

skinsList = readSkinNames()
profitSummary = []
for skinName in skinsList:
    skinPrice = []
    for market in Markets:
        price = market.getPrice(skinName)
        if price is not None:
            skinPrice.append({"market": type(market), "price": price})
    if skinPrice:
        maxPrice = max(skinPrice, key=lambda x:x['price'])
        minPrice = min(skinPrice, key=lambda x:x['price'])
        profitSummary.append({"Name": skinName,"Relative Profit": (maxPrice['price']/minPrice['price']), "Profit": (maxPrice['price'] - minPrice['price']), "Buy Market": minPrice['market'].__name__, "Buy Price": minPrice['price'], "Sell Market": maxPrice['market'].__name__, "Sell Price": maxPrice['price']})
        
sortedProfitSummary = sorted(profitSummary, key=lambda x: x["Relative Profit"], reverse=True)

for i in sortedProfitSummary:
    if (i["Profit"] > 0):
        print(i)
        
# Generate a CSV file with the following columns: Name, Relative Profit, Profit, Buy Market, Buy Price, Sell Market, Sell Price.
# Sort the rows by Relative Profit in descending order.
# Only include rows where Profit > 0 and Buy Market != "Buff"

# Assuming sortedProfitSummary is the list containing the profit summary data

filteredSummary = [row for row in sortedProfitSummary if row["Profit"] > 0 and row["Buy Market"] != "Buff"]

csv_file = "profit_summary.csv"

with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Relative Profit", "Profit", "Buy Market", "Buy Price", "Sell Market", "Sell Price"])
    writer.writeheader()
    writer.writerows(filteredSummary)

sortedSummary = sorted(filteredSummary, key=lambda x: x["Relative Profit"], reverse=True)
