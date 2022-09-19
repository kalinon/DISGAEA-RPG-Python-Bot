from api.constants import Constants, Alchemy_Effect_Type
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
item_id = 24184231

# roll until this % is achieved
boost_target = 40

a.etna_resort_roll_alchemy_effect(item_id, boost_target=boost_target, effect_id=Alchemy_Effect_Type.Innocent_Effect)
