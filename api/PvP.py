import datetime
from abc import ABCMeta
import random
from api.base import Base
from dateutil import parser

from api.constants import Constants, Mission_Status


class PvP(Base, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def pvp_do_battle(self, pvp_team:int=1):
        current_orbs = self.pvp_get_remaining_orbs()
        if current_orbs == 0:
            self.log("No PvP orbs remaining.")
            return
        
        while current_orbs > 0:
            oponent = self.pvp_select_opponent()
            oponent_details = self.client.pvp_enemy_player_detail(t_player_id=oponent['t_player_id'])
            self.log(f"Battling player {oponent['user_name']} - Ranking {oponent['ranking']}. Orbs remaining: {current_orbs}")
            battle_start_data =self.client.pvp_start_battle(pvp_team, oponent['t_player_id'])
            battle_end_data = self.client.pvp_battle_give_up()
            self.client.pvp_info()
            current_orbs -=1


    def pvp_select_opponent(self):
        opponent_data = self.client.pvp_enemy_player_list()
        pos = random.randint(0, len(opponent_data['result']['enemy_players'])-1)	
        random_oponent = opponent_data['result']['enemy_players'][pos]
        return random_oponent

    def pvp_get_remaining_orbs(self):
        pvp_data = self.client.pvp_info()
        return pvp_data['result']['t_arena']['act']