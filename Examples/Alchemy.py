from api.constants import Constants, Items, Alchemy_Effect_Type
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

## EXPLANATION
## This script rerolls an item until a certain innocent % boost is reached, ignoring all other rolls
## Specify and item ID and a target boost. The script will keep rerolling until the target boost is reached
## If user runs out of HL or priprism the script will stop execution
## Use a.print_team_info(team_num) to get the ID of the item

# Item to be rolled
item_id = 15259368

# roll until this % is achieved
boost_target = 40

if not a.etna_resort_can_item_be_rolled(item_id):
    a.log("Item has effects(s) locked and cannot be rolled. Exiting...")
    exit(1)

e = a.pd.get_weapon_by_id(item_id)
if e is not None:
    item_type = 3
else:
    item_type = 4
    e = a.pd.get_equipment_by_id(item_id)

effect = 0
attempt_count = 0

prism_count = a.pd.get_item_by_m_item_id(Items.PriPrism.value)['num']
current_hl = a.pd.get_item_by_m_item_id(Items.HL.value)['num']
a.log(f"Rerolling item - Priprism count: {prism_count} - Current HL: {current_hl}")

while effect < boost_target and prism_count > 0 and current_hl > Constants.Alchemy_Alchemize_Cost:
    res = a.client.etna_resort_add_alchemy_effects(item_type, item_id)
    effects = res['result']['after_t_data']['equipment_effects']
    innocent_effect = next(
        (x for x in effects if x['m_equipment_effect_type_id'] == Alchemy_Effect_Type.Innocent_Effect), None)
    effect = innocent_effect['effect_value']
    attempt_count += 1
    prism_count -= 1
    if prism_count == 0:
        a.log("Ran out of priprism. Exiting...")
    current_hl -= Constants.Alchemy_Alchemize_Cost
    if current_hl < Constants.Alchemy_Alchemize_Cost:
        a.log("Ran out of HL. Exiting...")

a.log(f"Rolled {effect}% innocent boost - Attempt count: {attempt_count} - Priprism left: {prism_count}")
