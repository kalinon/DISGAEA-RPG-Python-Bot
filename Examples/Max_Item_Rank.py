from api.constants import Constants, Items
from main import API

a = API()
a.config(
    sess=Constants.session_id,
    uin=Constants.user_id,
    wait=0,
    region=2,
    device=2
)
a.quick_login()

item_id = 25921095
raid_farming_party = 7

item = a.pd.get_weapon_by_id(item_id)
if item is None:
    item = a.pd.get_equipment_by_id(item_id)    

current_hl = a.pd.get_item_by_m_item_id(Items.HL.value)['num']
remake_count = item['remake_count']
hl_needed = (10 - remake_count) * 1000000

a.log(f"Upgrading item to rank 50. Starting Rank: {remake_count}. HL needed: {hl_needed}")

while True:
    if remake_count == 10:
        a.log("Item is already rank 50")
        break
    if current_hl < 1000000:
        a.log("Not enough money to remake")
        break
        
    a.etna_resort_remake_item(item['id'])
    a.upgrade_items(items=[item])
    remake_count += 1
    a.player_items(True)
    current_hl = a.pd.get_item_by_m_item_id(Items.HL.value)['num']
    a.log(f"Equipment rank increased. Current rank: {remake_count}. Current HL: {current_hl}")

    if raid_farming_party != 0:
        a.raid_farm_shared_bosses(raid_farming_party)