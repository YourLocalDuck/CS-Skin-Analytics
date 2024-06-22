import json
import pandas as pd
from .Market import *

# Method for parsing the request parameters for the GET request to /analytics/profit-summary
def parseSummaryRequest(params):
    buyMarketsJSON = params.get("buy_markets", [])
    sellMarketsJSON = params.get("sell_markets", [])
    buyMarketItemData = []
    sellMarketItemData = []
    for market in buyMarketsJSON:
        buyMarketItemData.append(marketFactory(market).getFilteredData())
    buyMarketItemData = pd.concat(buyMarketItemData)
    for market in sellMarketsJSON:
        sellMarketItemData.append(marketFactory(market).getFilteredData())
    sellMarketItemData = pd.concat(sellMarketItemData)
    
    # Merge the two dataframes on the name column
    profitSummary = pd.merge(
        buyMarketItemData,
        sellMarketItemData,
        on="name",
        how="inner",
        suffixes=("_buy", "_sell"),
    )
    
    # Clean up useless columns, rename columns, and add new columns

    # Clean up useless columns
    profitSummary = profitSummary.drop(
        columns=["unlockTime_sell", "SalePrice_buy", "price_sell"]
    )

    # Rename columns
    profitSummary = profitSummary.rename(
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
    profitSummary["Profit"] = (
        profitSummary["Sell Price"] - profitSummary["Buy Price"]
    )
    # Relative Profit
    profitSummary["Relative Profit"] = (
       profitSummary["Profit"] / profitSummary["Buy Price"]
    )
        
    return profitSummary.to_json(orient='records')