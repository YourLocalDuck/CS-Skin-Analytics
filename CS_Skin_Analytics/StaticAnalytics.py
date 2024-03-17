from typing import List
from Market_Base import Market_Base
from GenerateAnalysis import Generate_Analysis
import concurrent.futures


class StaticAnalytics:
    def __init__(self, Markets: List[Market_Base]):
        self.Markets = Markets

    def run(self):
        # UI for the program that allows the user to select buy markets and sell markets, and then prompts the user to select
        # which of those markets to update with new data. Depending on selection, the program will update the data for the
        # selected markets and then generate the profit summary and CSV file.

        buy_markets = None
        sell_markets = None
        updateBuyMarkets = None
        updateSellMarkets = None
        while True:
            print("Please select an option:")
            print("1. Select buy markets")
            print("2. Select sell markets")
            print("3. Generate profit summary")
            print("4. Exit")

            option = input("Enter option number: ")
            match option:

                case "1":
                    buy_markets, updateBuyMarkets = self.select_markets(
                        "Select buy markets:"
                    )

                case "2":
                    sell_markets, updateSellMarkets = self.select_markets(
                        "Select sell markets:"
                    )

                case "3":
                    if buy_markets is not None and sell_markets is not None:
                        with concurrent.futures.ThreadPoolExecutor(
                            max_workers=5
                        ) as executor:
                            if updateBuyMarkets == "y":
                                for market in buy_markets:
                                    executor.submit(market.initializeMarketData)
                            else:
                                for market in buy_markets:
                                    executor.submit(market.readFromDB)
                            if updateSellMarkets == "y":
                                for market in sell_markets:
                                    executor.submit(market.initializeMarketData)
                            else:
                                for market in sell_markets:
                                    executor.submit(market.readFromDB)
                                    
                        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                            for market in buy_markets + sell_markets:
                                executor.submit(self.writeToDB, market)
                            executor.submit(self.generateAnalysis, buy_markets, sell_markets)

                case "4":
                    break

                case _:
                    print("Invalid option. Please try again.")

    def select_markets(self, message):
        while True:
            print(message)
            for i in range(len(self.Markets)):
                print(f"{i + 1}. {self.Markets[i].__class__.__name__}")
            marketsInput = input("Enter comma-separated list of numbers: ")
            try:
                marketsInput = [int(i) - 1 for i in marketsInput.split(",")]
            except ValueError:
                print("Invalid input. Please try again.")
                continue
            else:
                if all([i in range(len(self.Markets)) for i in marketsInput]):
                    markets = [self.Markets[i] for i in marketsInput]
                    print("Would you like to update the selected markets? (y/n)")
                    updateMarkets = input("Enter option: ")
                    if not updateMarkets in ["y", "n"]:
                        print("Invalid input. Please try again.")
                        continue
                    break
                else:
                    print("Invalid input. Please try again.")
        return markets, updateMarkets
    
    def writeToDB(self, market: Market_Base):
        print("Writing " + market.__class__.__name__ + " data to Database")
        market.writeToDB()
        
    def generateAnalysis(self, buy_markets, sell_markets):
        print("Sorting prices...")
        analyze = Generate_Analysis(buy_markets, sell_markets)
        analyze.getData()
        analyze.sortData()
        analyze.analyzeData()
        print("Analysis complete")
