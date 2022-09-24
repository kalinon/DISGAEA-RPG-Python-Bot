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
effect_id = Alchemy_Effect_Type.Star_Damage

# roll until this % is achieved
effect_target = 30

# Set this to true if you want the effect to have a unique innocent
# NOTE: Looking for a max effect with a unique innocent can use all your prism, use with care
unique_innocent = False

# Set this to true if you want all 4 effects to be unlocked. 
# It will keep rolling until the desired effect is obtained with all 4 effects unlocked, so they can be individually rerolled later
# set to false if rolling only for innocent boost
all_effects_unlocked = True

a.etna_resort_roll_alchemy_effect(item_id, effect_target=effect_target, effect_id=effect_id, unique_innocent=unique_innocent, all_effects_unlocked=all_effects_unlocked)

# This method allows to specify a set of effects to look for
# The bot will roll the item until any of the effects specified is maxed
# Example alchemy_effects = [Alchemy_Effect_Type.CritDmg, Alchemy_Effect_Type.CritRate, Alchemy_Effect_Type.Fire_Damage, Alchemy_Effect_Type.Wind_Damage]
# If the bot rolls 20% CRT OR 100% CRD or 30% Fire OR 30% Wind, it will stop r

alchemy_effects = [Alchemy_Effect_Type.CritDmg, Alchemy_Effect_Type.CritRate, Alchemy_Effect_Type.Fire_Damage, Alchemy_Effect_Type.Wind_Damage]
a.etna_resort_roll_until_maxed_effect(item_id=item_id, alchemy_effects=alchemy_effects, unique_innocent=unique_innocent, all_effects_unlocked=all_effects_unlocked)

# Specify what slot you want to reroll
place_no = 3
# Specify effect to reroll for
alchemy_effect_id = Alchemy_Effect_Type.Star_Damage
# Optional. Specify a threshold for the roll, 0 to keep rolling until max value
effect_target=1

# Reroll a slot until a specific effect is obtained with max value/specified value
a.etna_resort_reroll_effect(item_id=item_id, alchemy_effect_id=alchemy_effect_id, place_no=place_no, effect_target=0)