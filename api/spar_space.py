import random
from abc import ABCMeta

import jwt

from api.player import Player


class SparSpace(Player, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def do_spar_space(self, stage_id, character_ids, deck_no, memory_ids=[], actions=100):
        start = self.client.battle_start(
            m_stage_id=stage_id,
            deck_no=deck_no,
            character_ids=character_ids,
            act=0,
            raid_status_id=0,
            memory_ids=memory_ids,
        )
        self.check_resp(start)
        battle_exp = self.get_battle_exp_data_spar_space(start, character_ids)
        iv = self.client.c.randomiv()
        common_battle_result = self.client.common_battle_result_jwt(iv, command_count=100)
        division_battle_result = self.get_division_battle_result_jwt(iv, 100)
        end = self.client.battle_end(
            current_iv=iv,
            battle_exp_data=battle_exp,
            skip_party_update_flg=True,
            m_stage_id=stage_id,
            m_tower_no=0,
            equipment_id=0,
            equipment_type=0,
            raid_status_id=0,
            raid_battle_result='',
            battle_type=1,
            result=1,
            common_battle_result='eyJhbGciOiJIUzI1NiJ9.eyJoZmJtNzg0a2hrMjYzOXBmIjoiIiwieXBiMjgydXR0eno3NjJ3eCI6NDcyM' \
                                 'Dg1NDQ4LCJkcHBjYmV3OW16OGN1d3duIjo1NjMzNTc3LCJ6YWNzdjZqZXY0aXd6anptIjowLCJreXF5bmk' \
                                 'zbm5tM2kyYXFhIjowLCJlY2htNnRodHpjajR5dHl0IjowLCJla3VzdmFwZ3BwaWszNWpqIjowLCJ4YTVlM' \
                                 'zIybWdlajRmNHlxIjoxMH0.VxO5cmCnMcn_4csZfq8U_XQnJcew9Snxh0d2LbILK7Y',
            division_battle_result='eyJhbGciOiJIUzI1NiJ9.eyJoZmJtNzg0a2hrMjYzOXBmIjoiIiwieXBiMjgydXR0eno3NjJ3eCI6NDc' \
                                   'yMDg1NDQ4LCJkcHBjYmV3OW16OGN1d3duIjo1NjMzNTc3LCJ6YWNzdjZqZXY0aXd6anptIjowLCJreXF' \
                                   '5bmkzbm5tM2kyYXFhIjowLCJlY2htNnRodHpjajR5dHl0IjowLCJla3VzdmFwZ3BwaWszNWpqIjowLCJ' \
                                   '4YTVlMzIybWdlajRmNHlxIjoxMH0.VxO5cmCnMcn_4csZfq8U_XQnJcew9Snxh0d2LbILK7Y',
        )
        return end

    def get_battle_exp_data_spar_space(self, start, character_ids):
        res = []
        for d in start['result']['enemy_list']:
            for r in d:
                res.append({
                    "finish_member_ids": character_ids,
                    "finish_type": random.choice([1, 2, 3]),
                    "m_enemy_id": d[r]
                })
        return res

    def get_division_battle_result_jwt(self, iv, action_count: int = 5, remaining_hp: int = 0):
        data = {
            "bzhzhah3a7x9p7a3": action_count,
            "kircbaup94cuh38r": remaining_hp,
            "th5dwswy27c72kxp": []
        }
        return jwt.encode(data, iv, algorithm="HS256")
