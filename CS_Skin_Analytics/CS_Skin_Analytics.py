from Market_Skinout import Skinout
from Market_Buff import Buff
from Market_Skinport import Skinport
from Market_Steam import Steam
from Market_Bitskins import Bitskins


def readSkinNames():
    skinList = []
    with open('skins_names.txt', 'r') as file:
            for line in file:
                skinList.append(line.strip())
    return skinList

skinport = Skinport()
steam = Steam()
bitskins = Bitskins()
skinout = Skinout()
steam.readFromFile()

Markets = [skinport, steam, bitskins, skinout]

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
        profitSummary.append({"Name": skinName,"Profit": (maxPrice['price']-minPrice['price']),"Buy Market": minPrice['market'].__name__, "Buy Price": minPrice['price'], "Sell Market": maxPrice['market'].__name__, "Sell Price": maxPrice['price']})
        
sortedProfitSummary = sorted(profitSummary, key=lambda x: x["Profit"], reverse=True)

for i in sortedProfitSummary:
    print(i)