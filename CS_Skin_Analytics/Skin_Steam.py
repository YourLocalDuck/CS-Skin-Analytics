class Skin_Steam:
    def __init__(self, name, hash_name, sell_listings, sell_price, sell_price_text, app_icon, app_name, asset_description, sale_price_text, *args, **kwargs) -> None:
        self.name = name
        self.hash_name = hash_name
        self.sell_listings = sell_listings
        self.sell_price = sell_price
        self.sell_price_text = sell_price_text
        self.app_icon = app_icon
        self.app_name = app_name
        self.asset_description = asset_description
        self.sale_price_text = sale_price_text
        self.extra = kwargs