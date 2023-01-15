
import os
from api import constants
from api.constants import Constants, Battle_Finish_Mode
from main import API

os.environ["STEAM_LOGIN"] = 'true'
os.environ["DRPG_EMAIL"] = ""
os.environ["DRPG_PASS"] = ""
os.environ["DRPG_SIGN"] = ""
a = API()

a.config(
    wait=0,
    region=2,
    device=3
)
a.quick_login()

#  Choose the battle finish mode. Random is chosen by default
#  Battle_Finish_Mode.Random_Finish randomly choose which unit kills each enemy (default mode)
#  Battle_Finish_Mode.Tower_Finish all enemies are killed using tower attack, exp is shared evenly
#  Battle_Finish_Mode.Single_Character the character on the leader slot will kill all enemies and get all exp
finish_mode = finish_mode = Battle_Finish_Mode.Tower_Finish

# Select which gates to run 
exp_gates_to_run = [5010120, 5010121, 5010122, 5010123, 5010124, 5010125]

# Select how many times to run the gates
number_of_runs = 3

# Specify a team to use
team_to_use = 5

# Specify the exp equipment preset
exp_equipment_preset = 4

# Apply the equipment preset to the team
a.client.apply_equipment_preset_to_team(team_number=team_to_use, equipment_preset=exp_equipment_preset)

## AUTO REINCARNATION
## If a.o.auto_rebirth is set to True, all characters will auto reincarnate
## Additionally, if auto_rebirth_character_ids is set, only the characters in the list will be autoreincarnated. Only works if a.o.auto_rebirth is set to True
## auto_rebirth_character_ids is optional, use if you want to reincarnate specific characters instead of the entire team
a.o.auto_rebirth = True
a.o.auto_rebirth_character_ids = [] # Example a.o.auto_rebirth_character_ids = [200039465, 108512864, 42749175]

## The characters you specify will automatically super reincarnate after a gate if they hit level 9999
characters_to_super_reincarnate = [] # Example characters_to_super_reincarnate = [200039465, 108512864, 42749175]

## Specify a friend with an exp boosting evility if you have it, leave empty for selecting it at random
help_t_player_id = 495151

a.o.use_potions = True

## Select option 1 or option 2

#### OPTION 1 - Run only a set of gates. Specify the number of runs
count = 0 
i=0
## Run the gates the specified number of times. After every gate the bot will check if any character can be super reincarnated
while i < number_of_runs:
    for gate_id in exp_gates_to_run:
        a.doQuest(m_stage_id=gate_id, team_num=team_to_use, auto_rebirth = a.o.auto_rebirth, help_t_player_id=help_t_player_id, finish_mode = Battle_Finish_Mode.Single_Character)
        for character_id in characters_to_super_reincarnate:
            a.super_reincarnate(character_id=character_id)
    i+=1

#### OPTION 2 - Run all gates
gates_data = a.client.player_gates()['result']
for data in gates_data:
    if data['m_area_id'] != 50101:
        continue
    for gate in data['gate_stage_data']:
        current = int(gate['challenge_num'])
        _max = int(gate['challenge_max'])
        while current < _max:
            a.doQuest(m_stage_id=gate['m_stage_id'], team_num=team_to_use, auto_rebirth = a.o.auto_rebirth, help_t_player_id=help_t_player_id, finish_mode = Battle_Finish_Mode.Single_Character)
            for character_id in characters_to_super_reincarnate:
                a.super_reincarnate(character_id=character_id)
            current += 1

## Specify whether you want to use gate keys
use_gate_keys = True
keys_to_use = 5
gate_to_run_with_keys = 5010125

if use_gate_keys:
    i=0
    while i<keys_to_use:
        a.client.item_use_gate_key(m_area_id = 50101, m_stage_id = gate_to_run_with_keys)
        a.doQuest(m_stage_id=gate_to_run_with_keys, team_num=team_to_use, auto_rebirth = a.o.auto_rebirth, help_t_player_id=help_t_player_id, finish_mode = Battle_Finish_Mode.Single_Character)
        for character_id in characters_to_super_reincarnate:
            a.super_reincarnate(character_id=character_id)
        i+=1