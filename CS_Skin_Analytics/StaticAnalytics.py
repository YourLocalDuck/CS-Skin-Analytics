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
                    keepGoing = True
                    while keepGoing:
                        print("Select buy markets:")
                        for i in range(len(self.Markets)):
                            print(f"{i + 1}. {self.Markets[i].__class__.__name__}")
                        buyMarketsInput = input("Enter comma-separated list of numbers: ")
                        buyMarketsInput = [self.int(i) - 1 for i in buy_markets.split(",")]
                        if all([i in range(len(self.Markets)) for i in buy_markets]):
                            keepGoing = False
                            buy_markets = [self.Markets[i] for i in buy_markets]
                            print("Would you like to update the selected markets? (y/n)")
                            updateBuyMarkets = input("Enter option: ")
                        else:
                            print("Invalid input. Please try again.")

                case "2":
                    keepGoing = True
                    while keepGoing:
                        print("Select sell markets:")
                        for i in range(len(self.Markets)):
                            print(f"{i + 1}. {self.Markets[i].__class__.__name__}")
                        sellMarketsInput = input("Enter comma-separated list of numbers: ")
                        sellMarketsInput = [int(i) - 1 for i in sell_markets.split(",")]
                        if all([i in range(len(self.Markets)) for i in sell_markets]):
                            keepGoing = False
                            sell_markets = [self.Markets[i] for i in sell_markets]
                            print("Would you like to update the selected markets? (y/n)")
                            updateSellMarkets = input("Enter option: ")
                        else:
                            print("Invalid input. Please try again.")

                case "3":
                    if buy_markets is not None and sell_markets is not None:
                        if updateBuyMarkets == "y":
                            for i in buy_markets:
                                self.Markets[i].initializeMarketData()
                                print(
                                    "Writing " + self.Markets[i].__class__.__name__ + " data to file"
                                )
                                self.Markets[i].writeToFile()
                        else:
                            for i in buy_markets:
                                self.Markets[i].readFromFile()
                        if updateSellMarkets == "y":
                            for i in sell_markets:
                                self.Markets[i].initializeMarketData()
                                print(
                                    "Writing " + self.Markets[i].__class__.__name__ + " data to file"
                                )
                                self.Markets[i].writeToFile()
                        else:
                            for i in sell_markets:
                                self.Markets[i].readFromFile()

                        print("Sorting prices...") # 2/7/2024 Below: To implement using GenerateAnalyis.py
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
                    keepGoingMenu = False