from Buff import Buff
from Skinport import skinport


SP = skinport()
B = Buff("Device-Id=0tXtERd0sm5fiXXBQg5V; client_id=R-KUx6DTG_hCnH8XwngB2Q; Locale-Supported=en; game=csgo; csrf_token=ImRjNDg4YjI0M2Y4NzdhNGFjNTMzMTAxNTIzZjRmM2UzOWM0NDEzMDQi.GCJESw.Z1vmWEwqmdTGAr5N6nKOHOA5tYc")
priceSP = SP.getSkinportPrice("10 Year Birthday Sticker Capsule")
priceB = B.getBuffPrice("10 Year Birthday Sticker Capsule")

print(priceB)