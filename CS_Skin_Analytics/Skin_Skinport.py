class Skin_Skinport:
    def __init__(self, market_hash_name, currency, suggested_price, item_page, market_page, min_price, max_price, mean_price, median_price, quantity, created_at, updated_at, *args, **kwargs):
        self.market_hash_name = market_hash_name
        self.currency = currency
        self.suggested_price = suggested_price
        self.item_page = item_page
        self.market_page = market_page
        self.min_price = min_price
        self.max_price = max_price
        self.mean_price = mean_price
        self.median_price = median_price
        self.quantity = quantity
        self.created_at = created_at
        self.updated_at = updated_at
        self.extra = kwargs