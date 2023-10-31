import requests
import currency_converter

class Buff:
    converter = currency_converter.CurrencyConverter() 
    def __init__(self, header):
        self.header = {
            "Cookie": str(header)
        }
    def getBuffPrice(self, itemname):
        URL = "https://buff.163.com/api/market/goods"
        params = {
            "game" : "csgo",
            "page_num" : "1",
            "search" : str(itemname)
        }
        r = requests.get(URL, params=params, headers=self.header).json()
        priceCNY = r["data"]["items"][0]["sell_min_price"]
        priceUSD = self.converter.convert(priceCNY, 'CNY', 'USD')
        return round(priceUSD, 2)