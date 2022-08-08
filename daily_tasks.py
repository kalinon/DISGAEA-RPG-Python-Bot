import datetime
import os

from dateutil import parser

from api.constants import Constants
from main import API

a = API()
a.config(
    sess=os.getenv('DRPG_TOKEN', default=Constants.session_id),
    uin=os.getenv('DRPG_UIN', default=Constants.user_id),
    wait=0,
    region=2,
    device=2
)

a.quick_login()

# Send sardines
player_data = a.client.player_index()
if player_data['result']['act_give_count']['act_send_count'] == 0:
    a.client.friend_send_sardines()

# Buy items from HL shop
a.buy_daily_items_from_shop()

# Use free gacha
if(a.is_free_gacha_available()):
    print("free gacha available")
    a.get_free_gacha()

# Spin bingo
if a.bingo_is_spin_available():
    spin_result = a.client.bingo_lottery(Constants.Current_Bingo_ID, False)
    spin_index = spin_result['result']['t_bingo_data']['last_bingo_index']
    print(f"Bingo spinned. Obtained number {spin_result['result']['t_bingo_data']['display_numbers'][spin_index]}.")
    free_reward_positions = [0,3,6,9,12,15,18,21,24,27,30,33]
    bingo_rewards =  spin_result['result']['rewards']
    free_rewards = [ bingo_rewards[i] for i in free_reward_positions ]
    available_free_rewards = [x for x in free_rewards if x['status'] == 1]  
    if(len(available_free_rewards) > 0):
        print(f"There are {len(available_free_rewards)} free rewards available to claim.")
        #a.bingo_claim_free_rewards()

#Uncomment to sell common items with no important innocents to clear inventory space
#a.shop_free_inventory_space(True, False, 5)
#a.shop_free_inventory_space(False, True, 20)
#Buy items from HL shop
a.buy_daily_items_from_shop()
# Buy all items with innocents, refresh shop, sell items without rare innos
a.buy_all_equipment_with_innocents(32)
a.innocent_safe_sell_items(minimumEffectRank=5, minimumItemRank=32)