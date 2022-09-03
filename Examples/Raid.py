from api.constants import Constants
import time
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

# List of all raid methods
# Make sure the raid constants have the correct value on the constants file
# The following values need to be updated for every raid
# Current_Raid_ID = 165
# Current_Raid_Event_Point_Gacha = 61
# Current_Raid_Innocent_Regular_Roulette = 62
# Current_Raid_Innocent_Special_Roulette = 63

# claims rewards for all boss battles
a.raid_claim_all_boss_rewards()

# claim all point rewards
a.raid_claim_all_point_rewards()

#exchange excess points for HL
a.raid_claim_surplus_points()

# Spin innocent roulette
a.raid_spin_innocent_roulette()

# Party that will be used to farm raids. Use the party with innocent boost characters
raid_farming_party = 5
boss_count = 0

# Farm raid bosses until script is stopped
while True:
    
    player_data = a.client.player_index()
    
    ### DO STUFF HERE
    available_raid_bosses = a.raid_find_all_available_bosses()
    for raid_boss in available_raid_bosses:        
        raid_stage_id = a.raid_find_stageid(raid_boss['m_raid_boss_id'], raid_boss['level'])
        if raid_stage_id != 0:
            battle_start_data = a.raid_battle_start(raid_stage_id, raid_boss['id'], raid_farming_party)
            battle_end_data = a.raid_battle_end_giveup(raid_stage_id, raid_boss['id'])
            boss_count +=1
            print(f"Farmed boss with level {raid_boss['level']}. Total bosses farmed: {boss_count}")

    time.sleep(10)