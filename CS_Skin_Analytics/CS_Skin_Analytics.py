from Market_Buff import Buff
from Market_Skinport import skinport
from Market_Steam import Steam
from Market_Bitskins import Bitskins


#SP = skinport()
B = Buff("Device-Id=0tXtERd0sm5fiXXBQg5V; client_id=R-KUx6DTG_hCnH8XwngB2Q; Locale-Supported=en; game=csgo; csrf_token=ImRjNDg4YjI0M2Y4NzdhNGFjNTMzMTAxNTIzZjRmM2UzOWM0NDEzMDQi.GCJESw.Z1vmWEwqmdTGAr5N6nKOHOA5tYc")
#S = Steam()
bitskins = Bitskins()

#target = r"AK-47 | The Empress (Factory New)"
target = r"★ Survival Knife | Scorched (Well-Worn)"

#priceSP = SP.getPrice("10 Year Birthday Sticker Capsule")
#priceB = B.getBuffPrice("10 Year Birthday Sticker Capsule")
priceS = bitskins.getPrice(target)

print(priceS)