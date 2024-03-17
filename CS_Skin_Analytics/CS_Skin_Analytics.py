import os
from typing import List
from StaticAnalytics import StaticAnalytics
from Market_LisSkins import LisSkins
from Market_Base import Market_Base
from Market_Skinout import Skinout
from Market_Buff import Buff
from Market_Skinport import Skinport
from Market_Steam import Steam
import psycopg2
import sqlalchemy


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

# Read from db.conf for the database settings
def getDBSettings():
    required_fields = ["dbname", "user", "password", "host", "port"]
    settings = {}
    with open("db.conf", "r", encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split(": ")
            settings[key] = value

    for field in required_fields:
        if field not in settings:
            raise ValueError(f"Required field {field} not found in db.conf")

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


initializeDirectory()
appSettings = getSettings()
DBSettings = getDBSettings()

connection_string = 'postgresql+psycopg2://'+DBSettings["user"]+':'+DBSettings["password"]+'@'+DBSettings["host"]+':'+DBSettings["port"]+'/'+DBSettings["dbname"]
connection_string = connection_string.replace("%", "%25")
engine = sqlalchemy.create_engine(connection_string)

buff = Buff(appSettings["Cookie"], engine)
skinport = Skinport(engine)
steam = Steam(engine)
lisskins = LisSkins(engine)
skinout = Skinout(engine)

Markets: List[Market_Base] = [skinout, buff, skinport, steam, lisskins]

while True:
    print("Please select an option:")
    print("1. Static Analysis")
    print("2. Monitoring")
    print("3. Exit")
    option = input("Enter option number: ")
    match option:
        case "1":
            static = StaticAnalytics(Markets)
            static.run()
        case "2":
            print("Monitoring not yet implemented")
        case "3":
            break
        case _:
            print("Invalid option")
            break
