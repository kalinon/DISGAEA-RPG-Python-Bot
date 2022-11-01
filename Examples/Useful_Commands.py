from api.constants import Constants, Battle_Finish_Mode
from main import API

a = API()

#################################################################################################################################
## List of useful commands, pick whichever ones you like to build your script
#################################################################################################################################

# Complete overlord Tower
a.Complete_Overlord_Tower()

# Use Gate Keys - needs area ID and stage ID
m_area_id = 50101
m_stage_id = 5010125
a.client.item_use_gate_key(m_area_id = m_area_id, m_stage_id = m_stage_id)

# Prints data for a specific team
a.print_team_info(team_num=4)

# Sells common items with no rare or above innocents. You can choose to sell either weapons or equipments and the number of items to sell
a.shop_free_inventory_space(sell_weapons=True, sell_equiment=False, items_to_sell=30)
a.shop_free_inventory_space(sell_weapons=False, sell_equiment=True, items_to_sell=30)

# Sells all r40 items with no innocents
a.sell_r40_commons_with_no_innocents()

# Redeem code
a.client.boltrend_exchange_code('Ainuko0925')

#################################################################################################################################
## Present box methods
#################################################################################################################################

# Claims AP from present box
a.present_receive_ap()

# Claims all items from mailbox except equipments and AP
a.present_receive_all_except_equip_and_AP()

# Claims equipments from the present box until inventory is full
a.present_receive_equipment()

##########################################################################
# DoQuest parameters
###########################################################################

# team_to_use: specify which team to use to clear the quest
team_to_use = 5

# Friend ID. Specify a friend to use for a quest, useful for gates. Use the friend_print_full_list to get the id first
a.friend_print_full_list()
help_t_player_id = 0

# send_friend_request, set to True to automatically send a friend request after clearing the quest
send_friend_request = True

#  Choose the battle finish mode. Random is chosen by default
#  Battle_Finish_Mode.Random_Finish randomly choose which unit kills each enemy
#  Battle_Finish_Mode.Tower_Finish all enemies are killed using tower attack, exp is shared evenly
#  Battle_Finish_Mode.Single_Character the character on the leader slot will kill all enemies and get all exp
finish_mode = Battle_Finish_Mode.Single_Character

a.doQuest(m_stage_id=m_stage_id, team_num=team_to_use, help_t_player_id=help_t_player_id, send_friend_request=send_friend_request, finish_mode=finish_mode)