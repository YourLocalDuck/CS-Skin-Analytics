class Skin_Buff:
    def __init__(self, appid, bookmarked, buy_max_price, buy_num, can_bargain, can_search_by_tournament, description, game, goods_info, has_buff_price_history, id, market_hash_name, market_min_price, name, quick_price, sell_min_price, sell_num, sell_reference_price, short_name, steam_market_url, transacted_num, **kwargs) -> None:
        self.appid = appid
        self.bookmarked = bookmarked
        self.buy_max_price = buy_max_price
        self.buy_num = buy_num
        self.can_bargain = can_bargain
        self.can_search_by_tournament = can_search_by_tournament
        self.description = description
        self.game = game
        self.goods_info = goods_info
        self.has_buff_price_history = has_buff_price_history
        self.id = id
        self.market_hash_name = market_hash_name
        self.market_min_price = market_min_price
        self.name = name
        self.quick_price = quick_price
        self.sell_min_price = float(sell_min_price)
        self.sell_num = sell_num
        self.sell_reference_price = sell_reference_price
        self.short_name = short_name
        self.steam_market_url = steam_market_url
        self.transacted_num = transacted_num
        self.extra = kwargs