import random
from abc import ABCMeta

from api import Player


class Battle(Player, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()
        self.min_rank = 0
        self.min_item_level = 0
        self.min_item_rank = 0
        self.min_item_rarity = 0
        self.only_weapons = False
        self.auto_rebirth = False

    def autoRebirth(self, i):
        self.auto_rebirth = bool(i)

    def minrank(self, i):
        self.min_rank = int(i)

    def minItemLevel(self, i):
        self.min_item_level = int(i)

    def minItemRank(self, i):
        self.min_item_rank = int(i)

    def minItemRarity(self, i):
        self.min_item_rarity = int(i)

    def onlyWeapons(self, i):
        self.only_weapons = bool(i)

    def battle_status(self):
        data = self.rpc('battle/status', {})
        return data

    def battle_help_list(self):
        data = self.rpc('battle/help_list', {})
        return data

    def battle_start(self, m_stage_id, help_t_player_id, help_t_character_id, act, help_t_character_lv):
        data = self.rpc('battle/start',
                        {"t_character_ids": [], "t_deck_no": self.teamNum(), "m_stage_id": m_stage_id,
                         "m_guest_character_id": 0, "help_t_player_id": help_t_player_id, "t_raid_status_id": 0,
                         "help_t_character_id": help_t_character_id, "auto_rebirth_t_character_ids": [], "act": act,
                         "help_t_character_lv": help_t_character_lv})
        return data

    def battle_start_event(self, m_stage_id, help_t_player_id, help_t_character_id, act, help_t_character_lv):
        data = self.rpc('battle/start',
                        {"t_character_ids": [], "t_deck_no": self.teamNum(), "m_stage_id": m_stage_id,
                         "m_guest_character_id": 0, "help_t_player_id": help_t_player_id, "t_raid_status_id": 0,
                         "help_t_character_id": help_t_character_id, "auto_rebirth_t_character_ids": [], "act": act,
                         "help_t_character_lv": help_t_character_lv})
        return data

    def battle_start_event2(self, m_stage_id, help_t_player_id, help_t_character_id, act, help_t_character_lv):
        data = self.rpc('battle/start',
                        {"t_character_ids": [], "t_deck_no": self.teamNum(), "m_stage_id": m_stage_id,
                         "m_guest_character_id": 0, "help_t_player_id": help_t_player_id, "t_raid_status_id": 0,
                         "help_t_character_id": help_t_character_id, "auto_rebirth_t_character_ids": [], "act": act,
                         "help_t_character_lv": help_t_character_lv})
        return data

    def battle_end(self, battle_exp_data, m_stage_id, battle_type, result, command_count, equipment_id=0,
                   equipment_type=0, m_tower_no=0):
        data = self.rpc('battle/end',
                        {"battle_exp_data": battle_exp_data, "equipment_type": equipment_type, "steal_hl_num": 0,
                         "m_tower_no": m_tower_no, "raid_battle_result": "", "m_stage_id": m_stage_id,
                         "total_receive_damage": 0, "equipment_id": equipment_id, "killed_character_num": 0,
                         "t_raid_status_id": 0, "battle_type": battle_type, "result": result, "innocent_dead_flg": 0,
                         "tower_attack_num": 0,
                         "common_battle_result": "eyJhbGciOiJIUzI1NiJ9.eyJoZmJtNzg0a2hrMjYzOXBmIjoiMSwxLDEiLCJ5cGIyODJ1dHR6ejc2Mnd4Ijo5MDY3NDE5NzQsImRwcGNiZXc5bXo4Y3V3d24iOjAsInphY3N2NmpldjRpd3pqem0iOjAsImt5cXluaTNubm0zaTJhcWEiOjAsImVjaG02dGh0emNqNHl0eXQiOjAsImVrdXN2YXBncHBpazM1amoiOjAsInhhNWUzMjJtZ2VqNGY0eXEiOjJ9.4kuAV7qO3Rp5Bq1ikSHbn5nPxhvjsg5POnnlFNDlEu0",
                         "command_count": command_count, "prinny_bomb_num": 0})

        return data

    def getbattle_exp_data(self, start):
        res = []
        for d in start['result']['enemy_list']:
            for r in d:
                res.append(
                    {"finish_member_ids": self.deck, "finish_type": random.choice([1, 2, 3]), "m_enemy_id": d[r]})
        return res

    def battle_story(self, m_stage_id):
        data = self.rpc('battle/story', {"m_stage_id": m_stage_id})
        return data

    def item_world_start(self, equipment_id, equipment_type=1):
        data = self.rpc('item_world/start',
                        {"equipment_type": equipment_type, "t_deck_no": self.teamNum(), "equipment_id": equipment_id,
                         "auto_rebirth_t_character_ids": self.deck if self.auto_rebirth else []})
        return data

    def getDiffWeapon(self, i):
        if not i or 'result' not in i or (
                'after_t_weapon' not in i['result'] and 'after_t_equipment' not in i['result']):
            return False
        stuff = self.weapons if 'after_t_weapon' in i['result'] else self.equipments
        i = i['result']['after_t_weapon' if 'after_t_weapon' in i['result'] else 'after_t_equipment']
        res = [str(i['id'])]
        for k, w in enumerate(stuff):
            if w['id'] == i['id']:
                for j in i:
                    if i[j] != w[j]:
                        s = '%s: %s -> %s' % (j, w[j], i[j])
                        res.append(s)
                stuff[k] = i
        return ', '.join(res)

    def item_filter(self, e, i_filter=None):
        if i_filter is None:
            i_filter = {
                'min_item_rank': self.min_item_rank,
                'min_item_rarity': self.min_item_rarity,
                'min_item_level': self.min_item_level,
                'lv_max': False,
            }

        if self.get_item_rank(e) < i_filter['min_item_rank']:
            return False
        if e['rarity_value'] < i_filter['min_item_rarity']:
            return False
        if e['lv_max'] < i_filter['min_item_level']:
            return False
        if i_filter['lv_max'] is False and e['lv'] >= e['lv_max']:
            return False
        return True

    def weapon_filter(self, e):
        return self.item_filter(e, {
            'min_item_rank': self.min_item_rank,
            'min_item_rarity': self.min_item_rarity,
            'min_item_level': self.min_item_level,
            'lv_max': False,
        })

    def equip_filter(self, e):
        return self.item_filter(e, {
            'min_item_rank': self.min_item_rank,
            'min_item_rarity': self.min_item_rarity,
            'min_item_level': self.min_item_level,
            'lv_max': False,
        })

    def tower_start(self, m_tower_no):
        data = self.rpc('tower/start', {"t_deck_no": self.teamNum(), "m_tower_no": m_tower_no})
        return data

    def parseStart(self, start):
        if 'result' in start and 'reward_id' in start['result']:
            reward_id = start['result']['reward_id']
            if start['result']['stage'] in {30, 60, 90, 100}:
                if reward_id == [101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101]:
                    return 5
                # self.log(reward_id)
                for j, r in enumerate(reward_id):
                    if r == 101:
                        continue
                    equipment_type = start['result']['reward_type'][j]
                    item = self.getWeapon(r) if equipment_type == 3 else self.getEquip(r)
                    rank = self.get_item_rank(item)

                    if item is None:
                        item = {'name': r}
                    self.log(
                        '[+] found item: "%s" with rarity: %s rank: %s' %
                        (item['name'], start['result']['reward_rarity'][j], rank)
                    )

                    # Only farm weapons
                    if self.only_weapons and equipment_type != 3:
                        return 5
                    if hasattr(self, 'min_item_rank') and rank < self.min_rank:
                        return 5
                    if hasattr(self, 'minrare') and start['result']['reward_rarity'][j] < self.minrare:
                        return 5
        return 1

    def raid_send_help_request(self, raid_id):
        data = self.rpc('raid/help', {"t_raid_status_id": raid_id})
        return data

    def raid_get_all_bosses(self):
        data = self.rpc('raid/index', {})
        return data['result']['t_raid_statuses']

    # Will check for raid bosses and will send help requests if active ones are found.
    def raid_check_and_send(self):
        all_bosses = self.raid_get_all_bosses()
        if len(all_bosses) > 0:
            self.log("Number of raid bosses found %d" % len(all_bosses))

        for i in all_bosses:
            if not i['is_discoverer']:
                if i['current_battle_count'] < 1:
                    self.log('There is a shared boss to fight')
                continue
            if not i['is_send_help']:
                sharing_result = self.raid_send_help_request(i['id'])
                self.log("Shared boss with %s users" % sharing_result['result']['send_help_count'])

    def axel_context_battle_start(self, act, m_character_id, t_character_ids):
        data = self.rpc('character_contest/start',
                        {"act": act, "m_character_id": m_character_id, "t_character_ids": t_character_ids})
        return data

    def axel_context_battle_end(self, m_character_id, battle_exp_data, common_battle_result):
        data = self.rpc('battle/end', {
            "m_stage_id": 0,
            "m_tower_no": 0,
            "equipment_id": 0,
            "equipment_type": 0,
            "innocent_dead_flg": 0,
            "t_raid_status_id": 0,
            "raid_battle_result": "",
            "m_character_id": m_character_id,
            "division_battle_result": "",
            "battle_type": 7,
            "result": 1,
            "battle_exp_data": battle_exp_data,
            "common_battle_result": common_battle_result,
            "skip_party_update_flg": True
        })
        return data

    def do_axel_contest(self, unit_id, highest_stage_to_clear=1000):
        unit = self.find_character_by_id(unit_id)
        if unit is None:
            self.log("Unit not found. Exiting...")
            return
        c = self.getChar(unit['m_character_id'])
        unit_name = ''
        if c is not None:
            unit_name = c['name']
        last_cleared_stage = unit['contest_stage']
        self.log(f"Started Axel Contest for {unit_name} - Last cleared stage: {last_cleared_stage}")

        while last_cleared_stage < highest_stage_to_clear:
            start = self.axel_context_battle_start(self.get_axel_stage_energy_cost(last_cleared_stage),
                                                   unit['m_character_id'], [unit_id])
            end = self.axel_context_battle_end(
                unit['m_character_id'],
                self.get_battle_exp_data_axel_contest(start, [unit_id]),
                "eyJhbGciOiJIUzI1NiJ9.eyJoZmJtNzg0a2hrMjYzOXBmIjoiIiwieXBiMjgydXR0eno3NjJ3eCI6ODY4MTY2ODE1OCwiZHBwY2JldzltejhjdXd3biI6MCwiemFjc3Y2amV2NGl3emp6bSI6NCwia3lxeW5pM25ubTNpMmFxYSI6MCwiZWNobTZ0aHR6Y2o0eXR5dCI6MCwiZWt1c3ZhcGdwcGlrMzVqaiI6MCwieGE1ZTMyMm1nZWo0ZjR5cSI6MH0.NudHEcTQfUUuOaNr9vsFiJkQwaw4nTL6yjK93jXzqLY"
            )
            last_cleared_stage = end['result']['after_t_character_collections'][0]['contest_stage']
            self.log(f"Cleared stage for {last_cleared_stage} for unit {unit_name}.")

        self.log(f"Finished running Axel Contest for {unit_name} - Last cleared stage: {last_cleared_stage}")

    def get_battle_exp_data_axel_contest(self, start, unitID):
        res = []
        for d in start['result']['enemy_list']:
            for r in d:
                res.append({
                    "finish_member_ids": unitID,
                    "finish_type": 1,
                    "m_enemy_id": d[r]
                })
        return res

    def get_axel_stage_energy_cost(self, last_cleared_stage):
        if last_cleared_stage < 49:
            return 1
        if last_cleared_stage < 99:
            return 2
        if last_cleared_stage < 199:
            return 3
        if last_cleared_stage < 299:
            return 4
        if last_cleared_stage < 399:
            return 5
        if last_cleared_stage < 499:
            return 6
        return 7
