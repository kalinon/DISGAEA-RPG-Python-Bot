import datetime

from dateutil import parser

from api.constants import Constants
from main import API

a = API()
a.config(
    sess=Constants.session_id,
    uin=Constants.user_id,
    wait=0,
    region=2,
    device=2
)
a.dologin()

# Send sardines
player_data = a.client.player_index()
if player_data['result']['act_give_count']['act_send_count'] == 0:
    a.client.friend_send_sardines()

# Buy items from HL shop
a.buy_daily_items_from_shop()

# Buy equipments with innocents. Will use free shop refreshes
shop_rank = player_data['result']['status']['shop_rank']
a.buy_all_equipment_with_innocents(shop_rank)
# Sell all items with innocents that are below max_innocent_rank (5=rare)
# max_item_rank is the highest item rank to be sold
a.innocent_safe_sell_items(max_innocent_rank=5, max_item_rank=10)

# Use free gacha
if a.is_free_gacha_available():
    print("free gacha available")
    a.get_free_gacha()

# Spin bingo
a.do_bingo()

# Calculate when AP is filled
player_data = a.client.player_index()
current_ap = player_data['result']['status']['act']
max_ap = player_data['result']['status']['act_max']
ap_filled_date = datetime.datetime.now() + datetime.timedelta(minutes=(max_ap - current_ap) * 2)

# Server time is utc -4. Spins available every 8 hours
lastRouleteTimeString = a.client.hospital_index()['result']['last_hospital_at']
lastRouletteTime = parser.parse(lastRouleteTimeString)
utcminus4time = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
if utcminus4time > lastRouletteTime + datetime.timedelta(hours=8):
    result = a.client.hospital_roulette()