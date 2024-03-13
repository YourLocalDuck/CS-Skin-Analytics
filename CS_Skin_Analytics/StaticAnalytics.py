from GenerateAnalysis import Generate_Analysis

class StaticAnalytics:
    def __init__(self, Markets: []):
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
                    buy_markets, updateBuyMarkets = self.select_markets("Select buy markets:")

                case "2":
                    sell_markets, updateSellMarkets = self.select_markets("Select sell markets:")

                case "3":
                    if buy_markets is not None and sell_markets is not None:
                        if updateBuyMarkets == "y":
                            for i in buy_markets:
                                i.initializeMarketData()
                                print(
                                    "Writing " + i.__class__.__name__ + " data to file"
                                )
                                i.writeToFile()
                        else:
                            for i in buy_markets:
                                i.readFromFile()
                        if updateSellMarkets == "y":
                            for i in sell_markets:
                                i.initializeMarketData()
                                print(
                                    "Writing " + i.__class__.__name__ + " data to file"
                                )
                                i.writeToFile()
                        else:
                            for i in sell_markets:
                                i.readFromFile()

                        print("Sorting prices...") # 2/7/2024 Below: To implement using GenerateAnalyis.py
                        # Read the skins names file and store the names in a list. Then, for each skin name, get the price
                        # from each of the selected buy markets and then store only the lowest price and the market it came
                        # from. Then, for every skin that made it into the list, get the price from each of the selected sell
                        # markets and then store only the highest price and the market it came from.
                        analyze = Generate_Analysis(buy_markets, sell_markets)
                        analyze.readSkinNames()
                        analyze.getData()
                        analyze.sortData()

                case "4":
                    keepGoingMenu = False
    
    def select_markets(self, message):
                    keepGoing = True
                    while keepGoing:
                        print(message)
                        for i in range(len(self.Markets)):
                            print(f"{i + 1}. {self.Markets[i].__class__.__name__}")
                        marketsInput = input("Enter comma-separated list of numbers: ")
                        marketsInput = [int(i) - 1 for i in marketsInput.split(",")]
                        if all([i in range(len(self.Markets)) for i in marketsInput]):
                            keepGoing = False
                            markets = [self.Markets[i] for i in marketsInput]
                            print("Would you like to update the selected markets? (y/n)")
                            updateMarkets = input("Enter option: ")
                        else:
                            print("Invalid input. Please try again.")
                    return markets, updateMarkets