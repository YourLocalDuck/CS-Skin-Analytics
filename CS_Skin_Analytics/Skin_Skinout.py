class Skin_Skinout:
    def __init__(self, id, market_hash_name, name, name_id, stickers, price, img, locked, unlock_time, total_count, in_cart, *args, **kwargs) -> None:
        self.id = id
        self.market_hash_name = market_hash_name
        self.name = name
        self.name_id = name_id
        self.stickers = stickers
        self.price = float(price)
        self.img = img
        self.locked = locked
        self.unlock_time = unlock_time
        self.total_count = total_count
        self.in_cart = in_cart
        self.extra = kwargs