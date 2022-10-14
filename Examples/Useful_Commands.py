from api.constants import Constants
from main import API

a = API()

#################################################################################################################################
## List of useful commands, pick whichever ones you like to build your script
##################################################################################################################################

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

# Receives AP from present box
a.present_receive_ap()

# Claims all items from mailbox except equipments and AP
a.present_receive_all_except_equip_and_AP()

# Redeem code
a.client.boltrend_exchange_code('Ainuko0925')