import os
from typing import List
from StaticAnalytics import StaticAnalytics
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

static = StaticAnalytics(Markets)
static.run()