from ast import Constant
import datetime
from abc import ABCMeta

from dateutil import parser

from api.constants import Constants
from api.player import Player


class ItemSurvey(Player, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def item_survey_complete_and_start_again(self, min_item_rank_to_deposit = 40, auto_donate=True):
        serverDateTime = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
        weapons_finished = []
        equipments_finished = []
        iw_survey_data = self.client.item_world_survey_index()
        
        for item in iw_survey_data['result']['t_weapons']:         
            item_survey_end_time = self.item_world_survey_get_item_return_time(item)
            if(serverDateTime > item_survey_end_time):
                weapons_finished.append(item['id'])

        for item in iw_survey_data['result']['t_equipments']:         
            item_survey_end_time = self.item_world_survey_get_item_return_time(item)
            if(serverDateTime > item_survey_end_time):
                equipments_finished.append(item['id'])

        if(len(weapons_finished) > 0 or len(equipments_finished)> 0):            
            self.client.item_world_survey_end(weapons_finished, equipments_finished, False)
            if(auto_donate):
                self.client.kingdom_weapon_equipment_entry(weap_ids=weapons_finished, equip_ids=equipments_finished)
        
        iw_survey_data = self.client.item_world_survey_index()
        free_slots = Constants.Item_Survey_Deposit_Size - len(iw_survey_data['result']['t_weapons']) - len(iw_survey_data['result']['t_equipments'])
        if(free_slots > 0):
            self.item_world_survey_fill(free_slots, min_item_rank_to_deposit)

    def item_world_survey_get_return_time(self):
        iw_survey_data = self.client.item_world_survey_index()
            #If available slots
        if(len(iw_survey_data['result']['t_equipments']) + len(iw_survey_data['result']['t_weapons']) < Constants.Item_Survey_Deposit_Size):
            return datetime.datetime.min

        closest_survey_end_time = datetime.datetime.max
        for item in iw_survey_data['result']['t_weapons']:
            item_survey_end_time = self.item_world_survey_get_item_return_time(item)
            if (item_survey_end_time < closest_survey_end_time):
                closest_survey_end_time = item_survey_end_time

        for item in iw_survey_data['result']['t_equipments']:
            item_survey_end_time = self.item_world_survey_get_item_return_time(item)
            if (item_survey_end_time < closest_survey_end_time):
                closest_survey_end_time = item_survey_end_time
            
        return closest_survey_end_time

    def item_world_survey_get_item_return_time(self, item):
        end_time_string = item['item_world_survey_end_at']
        if(end_time_string != ''):
            end_time_datetime = parser.parse(end_time_string)
            return end_time_datetime
        return datetime.datetime.min

    # Will first try to fill the depository with items with rare innocents (any rank)
    # Rest of spots will be filled with any item of specified rank (r40 by default)
    def item_world_survey_fill(self, free_slots=10, min_item_rank_to_deposit = 40):
        if(free_slots == 0):
            iw_survey_data = self.client.item_world_survey_index()
            free_slots = Constants.Item_Survey_Deposit_Size - len(iw_survey_data['result']['t_weapons']) - len(iw_survey_data['result']['t_equipments'])
        
        if(free_slots > 0):
            print(f"\tSearching for {free_slots} items for item world survey...") 

            self.client.player_weapons(True)
            self.client.player_equipments(True)
            weapons_to_deposit =[]
            equipments_to_deposit =[]
            weapons_lvl1 = [x for x in self.pd.weapons if x['lv'] <= 1 and x['set_chara_id'] == 0 and not x['lock_flg']]
            equips_lvl1 = [x for x in self.pd.equipment if x['lv'] <= 1 and x['set_chara_id'] == 0 and not x['lock_flg']]

            equipments_to_deposit = self.iwe_generate_array_for_deposit(equips_lvl1, free_slots, min_item_rank_to_deposit)
            
            # If deposit cannot be filled with only equipment, find weapons to finish filling
            if(len(equipments_to_deposit) < free_slots):
                free_slots = free_slots - len(equipments_to_deposit)
                weapons_to_deposit = self.iwe_generate_array_for_deposit(weapons_lvl1, free_slots, min_item_rank_to_deposit)                 
            
            if(len(weapons_to_deposit) > 0 or len(equipments_to_deposit) > 0):
                self.client.item_world_survey_start(weapons_to_deposit, equipments_to_deposit)

   # Look for items with specified criteria
    def iwe_generate_array_for_deposit(self, all_items, deposit_free_slots, min_item_rank_to_deposit = 40, max_rarity_to_deposit = 40):
        deposit_count=0
        items_to_deposit =[]
        max_innocent_rank = 5

        for item in all_items:
            # Fill with items with specific conditions (normally r40 commons with no rare iinocents)
            item_innocents  = self.client.player_innocents(item['id'])           
            rare_innocents = [x for x in item_innocents if x['effect_rank'] >= max_innocent_rank]
            if(len(rare_innocents) > 0):
                continue
            item_rank = self.gd.get_item_rank(item)
            if(item['rarity_value'] > max_rarity_to_deposit or item_rank < min_item_rank_to_deposit):
                continue
            items_to_deposit.append(item['id'])
            deposit_count+=1
            if(deposit_count == deposit_free_slots):
                break          
        return items_to_deposit
