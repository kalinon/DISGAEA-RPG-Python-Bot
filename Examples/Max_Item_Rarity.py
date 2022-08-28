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
if(item is None):
    item = a.pd.get_equipment_by_id(item_id)    

item_rarity = item['rarity_value']
prinny_steel = a.pd.get_item_by_m_item_id(Items.Prinny_Steel.value)['num']
a.log(f"Upgrading item to rarity 100. Starting Rarity: {item['rarity_value']}. Current prinny steel: {prinny_steel}")

while True:
    if item_rarity == 100:
        a.log("Item is already rarity 100")
        break
    if prinny_steel < 3:
        a.log("Not enough prinny steel to refine item")
        break
        
    item_rarity = a.etna_resort_refine_item(item['id'])
    a.upgrade_items(items=[item])
    a.player_items(True)
    prinny_steel = a.pd.get_item_by_m_item_id(Items.Prinny_Steel.value)['num']
    a.log(f"Equipment rarity increased. Current rarity: {item_rarity}. Current prinny steel: {prinny_steel}")

    if(raid_farming_party != 0):
        a.raid_farm_shared_bosses(raid_farming_party)