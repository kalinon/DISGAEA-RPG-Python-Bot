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
## This script rerolls an item until a certain % boost is reached, ignoring all other rolls
## Specify and item ID, effect and a target boost. The script will keep rerolling until the target boost is reached
## If unique_innocent is set to true, the bot will keep rerolling until a target % is reached and the unique innocent is included in the list
## If user runs out of HL or priprism the script will stop execution
## Use a.print_team_info(team_num) to get the ID of the item

# Item to be rolled
item_id = 24184231

# Type of effect to roll for
effect_id = Alchemy_Effect_Type.Innocent_Effect

# roll until this % is achieved
effect_target = 40

# Set this to true if you want the effect to have a unique innocent
# NOTE: Looking for a max effect with a unique innocent can use all your prism, use with care
unique_innocent = False

a.etna_resort_roll_alchemy_effect(item_id, effect_target=effect_target, effect_id=effect_id, unique_innocent=unique_innocent)
