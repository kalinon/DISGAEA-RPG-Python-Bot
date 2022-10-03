from api.constants import Constants, Item_World_Mode, Item_World_Drop_Mode
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

# a.setActiveParty(5)
# a.minrarity(95)
max_innocent_rank = 5  # do not donate items with innocents above this rank
max_item_rarity = 40  # do not donate items above this rarity
max_item_rank = 40  # do not donate items above this rank
min_item_rank_to_run = 40  # do not run IW for items below this rank
batch_size = 15
batches_to_run = 3

# Specify which party you want to use to farm raid bosses. 0 to disable it
raid_party_to_use = 0

a.options.min_item_rank = 40 # lowest item rank to run
a.options.min_item_rarity = 0 # lowest item rarity to run
# select if you want to run only weapons, equipments or all items (default option)
# Item_World_Mode.Run_Weapons_Only Item_World_Mode.Run_Equipment_Only Item_World_Mode.Run_All_Items
a.options.item_world_mode = Item_World_Mode.Run_All_Items 
# set to Item_World_Drop_Mode.Drop_Weapons_Only if you want to get only weapons
a.options.item_world_drop_mode = Item_World_Drop_Mode.Drop_All_Items
# set to true to ensure drops on every boss stage. If false the bot won't retry boss stages
a.options.item_world_ensure_drops = True

# Will run through X items in a batch
# Uncomment lines inside the loop to activate additional functionality (check depository status, donate items, farm raid...)
# item_limit is the number of item clears after which the bot checks the depository/raid/IW expedition status

batch_count = 0
while batch_count < batches_to_run:
    item_count = 0
    while item_count < batch_size:
        a.upgrade_items(item_limit=1)

        ## Uncomment this line for automatically fetching maxed items from the depository and filling it again with new items
        # a.etna_resort_check_deposit_status(max_innocent_rank, max_item_rank, max_item_rarity)

        ## Uncomment this line to check the status of item world survey after every clear
        # a.item_survey_complete_and_start_again(min_item_rank_to_deposit=40, auto_donate=True)        

        ## Uncomment this line to farm raid bosses after every clear
        # if raid_party_to_use != 0:
        #     a.raid_farm_shared_bosses(party_to_use= raid_party_to_use)

        item_count += 1
    a.etna_resort_donate_items(max_innocent_rank, max_item_rank, max_item_rarity)
    #a.sell_r40_commons_with_no_innocents(item_count=20)
    batch_count += 1

a.etna_resort_get_all_daily_rewards()