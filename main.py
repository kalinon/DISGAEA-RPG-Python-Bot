# -*- coding: utf-8 -*-
import datetime
from api.constants import Item_World_Mode

from dateutil import parser

from api import BaseAPI
from api.constants import Constants


class API(BaseAPI):
    def __init__(self):
        super().__init__()

    def config(self, sess: str, uin: str, wait: int = 0, region: int = 1, device: int = 1):
        self.o.sess = sess
        self.o.uin = uin
        self.o.wait = wait
        self.o.set_region(region)
        self.o.set_device(device)

    def get_mail_and_rewards(self):
        self.client.trophy_get_reward_daily()
        for i in range(5):
            self.client.trophy_get_reward()
        for i in range(5):
            self.get_mail()

    def dofarm(self):
        # self.buyRare()
        self.get_mail_and_rewards()
        if True:
            for i in [9, 8, 7, 6, 1012, 1011, 101, 101, 101, 101, 101]:
                self.client.shop_buy_item(itemid=i, quantity=1)

        if True:
            for i in [31, 8, 7, 1, 19, 21, 29, 24, 2, 6, 25, 26]:
                self.client.sub_tutorial_read(m_sub_tutorial_id=i)

        self.completeStory()

    def quick_login(self):
        self.client.login()
        self.player_characters(True)
        self.player_weapons(True)
        self.player_weapon_effects(True)
        self.player_equipment(True)
        self.player_equipment_effects(True)
        self.player_items(True)
        self.player_innocents(True)

        data = self.client.player_index()
        if 'result' in data:
            self.o.current_ap = int(data['result']['status']['act'])

        self.player_character_collections()
        self.player_decks()

        self.player_stone_sum()

    def dologin(self):
        self.client.login()
        self.client.app_constants()
        self.client.player_tutorial()
        self.client.battle_status()
        # player/profile
        # player/sync
        self.player_characters(True)
        self.player_weapons(True)
        self.client.player_weapon_effects(updated_at=0, page=1)
        self.player_equipment(True)
        self.client.player_equipment_effects(updated_at=0, page=1)
        self.player_items(True)
        self.client.player_clear_stages(updated_at=0, page=1)
        self.client.player_stage_missions(updated_at=0, page=1)
        self.player_innocents(True)
        data= self.client.player_index()
        if 'result' in data:
            self.o.current_ap = int(data['result']['status']['act'])
        self.client.player_agendas()
        self.client.player_boosts()
        self.player_character_collections()
        self.player_decks()
        self.client.friend_index()
        self.client.player_home_customizes()
        self.client.passport_index()
        self.player_stone_sum()
        self.client.player_sub_tutorials()
        self.client.system_version_manage()
        self.client.player_gates()
        self.client.event_index()
        self.client.stage_boost_index()
        self.client.information_popup()
        self.client.player_character_mana_potions()
        self.client.potential_current()
        self.client.potential_conditions()
        self.client.character_boosts()
        self.client.survey_index()
        self.client.kingdom_entries()
        self.client.breeding_center_list()
        self.client.trophy_daily_requests()
        self.client.weapon_equipment_update_effect_unconfirmed()
        self.client.memory_index()
        self.client.battle_skip_parties()
        # boltrend/subscriptions
        self.client.login_update()

    def addAccount(self):
        self.player_stone_sum()
        self.get_mail()
        self.get_mail()

    def get_mail(self):
        did = set()
        while 1:
            ids = self.client.present_index(conditions=[0, 1, 2, 3, 4, 99],
                                            order=1)['result']['_items']
            msgs = []
            for i in ids:
                if i['id'] in did: continue
                msgs.append(i['id'])
                did.add(i['id'])
            if len(msgs) >= 1:
                self.client.present_receive(
                    receive_ids=msgs[0:len(msgs) if len(msgs) <= 20 else 20],
                    conditions=[0, 1, 2, 3, 4, 99],
                    order=1)
            else:
                break
    
    def present_receive_ap(self):
        present_data = self.client.present_index(conditions=[4],order=0)
        ap = next((x for x in present_data['result']['_items'] if x['present_id'] == 2501), None)
        if ap is not None:
            self.client.present_receive(receive_ids =[ap['id']], order=0, conditions=[4])
            print(f"Claimed {ap['present_num']} AP")
            self.o.current_ap += int(ap['present_num'])

    def present_receive_all_except_equip_and_AP(self):
        initial_nq = self.player_stone_sum()['result']['_items'][0]['num']
        current_nq = initial_nq
        present_data = self.client.present_index(conditions=[0,1,3,99],order=0)
        while len(present_data['result']['_items']) > 0:
            item_ids = []
            for item in present_data['result']['_items']:
                item_ids.append(item['id'])
            if len(item_ids) > 0:
                data =self.client.present_receive(receive_ids = item_ids, order=0, conditions=[0,1,3,99])
                print(f"Claimed {len(item_ids)} presents")
                if len(data['result']['stones']) > 0:
                    current_nq = data['result']['stones'][0]['num']
            present_data = self.client.present_index(conditions=[0,1,3,99],order=0)
        if current_nq > initial_nq:
            self.log(f"Total Nether Quartz gained: {current_nq - initial_nq}")
        self.log("Finished claiming presents.")

    def doQuest(self, m_stage_id=101102, use_tower_attack: bool = False, team_num=None, auto_rebirth: bool = None,
                help_t_player_id: int = 0, send_friend_request:bool=False):
        if auto_rebirth is None:
            auto_rebirth = self.o.auto_rebirth

        stage = self.gd.get_stage(m_stage_id)
        self.log('doing quest:%s [%s]' % (stage['name'], m_stage_id))
        if stage['exp'] == 0:
            return self.client.battle_story(m_stage_id)

        if stage['act'] > self.current_ap:
            if self.o.use_potions:
                self.log('not enough ap. using potion')
                rr = self.client.item_use(use_item_id=301, use_item_num=1)
                if 'api_error' in rr and rr['api_error']['code'] == 12009:
                    self.log_err('unable to use potion')
                    return None
            else:
                self.log('not enough ap')
                return

        if team_num is None:
            team_num = self.o.team_num

        deck = []
        if auto_rebirth:
            deck = self.pd.deck(team_num)

        if help_t_player_id != 0:
            help_player = self.battle_help_get_friend_by_id(help_t_player_id)
        else:
            help_player = self.client.battle_help_list()['result']['help_players'][0]

        start = self.client.battle_start(
            m_stage_id=m_stage_id, help_t_player_id=help_player['t_player_id'],
            help_t_character_id=help_player['t_character']['id'], act=stage['act'],
            help_t_character_lv=help_player['t_character']['lv'],
            deck_no=team_num, deck=deck,
        )

        if 'result' not in start:
            return

        exp_data = self.get_battle_exp_data_tower_finish(start) if use_tower_attack else self.get_battle_exp_data(start)

        end = self.client.battle_end(
            battle_exp_data=exp_data, m_stage_id=m_stage_id,
            battle_type=1, result=1)
        res = self.parseReward(end)

        if not self.is_helper_in_friend_list(help_player['t_player_id']) and send_friend_request:
            self.log(f"Send friend request to {help_player['name']} - Rank {help_player['rank']}")
            self.client.friend_send_request(help_player['t_player_id'])

        return res

    def do_conquest_battle(self, m_stage_id=101102, t_character_ids=[]):
        stage = self.gd.get_stage(m_stage_id)
        self.log('doing conquest battle:%s [%s]' % (stage['name'], m_stage_id))
        start = self.client.battle_start(
            m_stage_id=m_stage_id,
            help_t_player_id=0,
            help_t_character_id=0,
            act=stage['act'],
            help_t_character_lv=0,
            character_ids=t_character_ids)
        if 'result' not in start:
            return
        end = self.client.battle_end(battle_exp_data=self.get_battle_exp_data(start),
                                     m_stage_id=m_stage_id,
                                     battle_type=1,
                                     result=1)
        res = self.parseReward(end)
        return res

    def upgrade_items(self, item_limit: int = None, items=None):
        if items is None:
            items = self.items_to_upgrade()
        if item_limit is not None and len(items) > int(item_limit):
            items = items[0:item_limit]
        self.upgrade_item_list(items)

    def upgrade_item_list(self, items):
        if len(items) == 0:
            self.log_err('No items found to upgrade')

        for w in items:
            self.client.trophy_get_reward_repetition()
            self.log_upgrade_item(w)
            while 1:
                if not self.doItemWorld(
                        equipment_id=w['id'],
                        equipment_type=self.pd.get_equip_type(w)
                ):
                    break

    # Will return a list of items that match the upgrade options filter
    def items_to_upgrade(self):
        weapons = self.player_weapons(False)
        equipments = self.player_equipment(False)

        if self.options.item_world_mode == Item_World_Mode.Run_Weapons_Only:
            items  = weapons
        elif self.options.item_world_mode == Item_World_Mode.Run_Equipment_Only:
            items  = equipments
        else:
            items = equipments + weapons
            
        item_list = []
        for w in filter(self.__item_filter, items):
            item_list.append(w)
        return item_list

    def __item_filter(self, e, i_filter=None):
        if i_filter is None:
            i_filter = {
                'min_item_rank': self.o.min_item_rank,
                'min_item_rarity': self.o.min_item_rarity,
                'min_item_level': self.o.min_item_level,
                'lv_max': False,
            }

        if self.gd.get_item_rank(e) < i_filter['min_item_rank']:
            return False
        if e['rarity_value'] < i_filter['min_item_rarity']:
            return False
        if e['lv_max'] < i_filter['min_item_level']:
            return False
        if i_filter['lv_max'] is False and e['lv'] >= e['lv_max']:
            return False
        return True

    def log_upgrade_item(self, w):
        item = self.gd.get_weapon(w['m_weapon_id']) if 'm_weapon_id' in w else self.gd.get_equipment(
            w['m_equipment_id'])
        self.log(
            '[*] upgrade item: "%s" rarity: %s rank: %s lv: %s lv_max: %s locked: %s' %
            (item['name'], w['rarity_value'], self.gd.get_item_rank(w), w['lv'],
             w['lv_max'], w['lock_flg'])
        )

    def Complete_Overlord_Tower(self, team_no:int=1):
        tower_level =1
        while tower_level <= Constants.Highest_Tower_Level:
            self.log(f"Clearing Overlord Tower level {tower_level}...")
            start = self.client.tower_start(m_tower_no=tower_level, deck_no=team_no)
            end = self.client.battle_end(battle_exp_data=self.get_battle_exp_data(start), m_tower_no=tower_level,
                                        m_stage_id=0,
                                        battle_type=4, result=1)
            tower_level+=1
        self.log("Completed Overlod Tower")
        

    def doItemWorld(self, equipment_id=None, equipment_type=1):
        if equipment_id is None:
            self.log_err('missing equip')
            return
        start, result = self.__start_item_world(equipment_id, equipment_type)

        # Loop until we get a good result, should also prevent too deep recursion
        while result != 1:
            if start is None:
                return False
            stage = start['result']['stage']
            self.log('stage: %s - did not drop anything good, retrying..' % stage)
            self.client.battle_end(
                m_stage_id=0,
                result=result,
                battle_type=start['result']['battle_type'],
                equipment_type=start['result']['equipment_type'],
                equipment_id=start['result']['equipment_id'],
            )
            start, result = self.__start_item_world(equipment_id, equipment_type)

        # End the battle and keep the equipment
        end = self.client.battle_end(
            battle_exp_data=self.get_battle_exp_data(start),
            m_stage_id=0,
            result=result,
            battle_type=start['result']['battle_type'],
            equipment_type=start['result']['equipment_type'],
            equipment_id=start['result']['equipment_id'],
        )

        res = self.get_weapon_diff(end)
        if res:
            self.log(res)
        return res

    def __start_item_world(self, equipment_id, equipment_type):
        start = self.client.item_world_start(equipment_id, equipment_type=equipment_type,
                                             deck_no=self.o.team_num,
                                             deck=self.pd.deck(self.o.team_num) if self.o.auto_rebirth else [])
        if start is None or 'result' not in start:
            return None, None

        result = self.parse_start(start)

        return start, result

    def getGain(self, t):
        for j in self.pd.items:
            if j['m_item_id'] == t['m_item_id']:
                return t['num'] - j['num']

    def parseReward(self, end):
        drop_result = end
        event_points = drop_result['result']['after_t_event']['point'] if drop_result['result']['after_t_event'] else 0
        drop_result = drop_result['result']['drop_result']
        for e in drop_result:
            if e == 'after_t_item':
                for t in drop_result[e]:
                    i = self.gd.get_item(t['m_item_id'])
                    self.log('%s +%s' % (i['name'], self.getGain(t)))
            elif e == 'drop_character':
                for t in drop_result[e]:
                    self.log('unit:%s lv:%s rarity:%s*' % (
                        self.gd.get_character(t['m_character_id'])['class_name'], t['lv'], t['rarity']))
            elif e == 'stones':
                self.log('+%s nether quartz' % (drop_result[e][0]['num'] - self.pd.gems))
        if event_points > 0:
            self.log('%s event points' % event_points)

        return drop_result

    def getDone(self):
        stages = set()
        r = self.player_clear_stages()
        if len(r) <= 0:
            return
        for i in r:
            if i['clear_num'] >= 1:
                stages.add(i['m_stage_id'])
        return stages

    def getAreaStages(self, m_area_id):
        ss = []
        for s in self.gd.stages:
            if s['m_area_id'] == m_area_id:
                ss.append(s)
        return ss

    def completeStory(self, m_area_id=None, limit=None, farming_all=False, raid_team=None):
        ss = []
        for s in self.gd.stages:
            ss.append(s['id'])
        ss.sort(reverse=False)
        i = 0
        blacklist = set()

        complete = self.getDone()
        for rank in [1, 2, 3]:
            for s in ss:
                if limit is not None and i >= limit:
                    return False
                stage = self.gd.get_stage(s)
                if m_area_id is not None and m_area_id != stage['m_area_id']:
                    continue
                if stage['rank'] != rank: continue

                # Skip non story areas
                if m_area_id is None and stage['m_area_id'] > 1000: continue

                if not farming_all and s in complete:
                    self.log('already complete - area: %s stage: %s rank: %s name: %s' % (
                        stage['m_area_id'], s, rank, stage['name']
                    ))
                    continue
                if not stage['appear_m_stage_id'] in complete:
                    self.log('not unlocked - area: %s stage: %s rank: %s name: %s' % (
                        stage['m_area_id'], s, rank, stage['name']
                    ))
                    continue

                if stage['m_area_id'] in blacklist:
                    continue
                try:
                    self.doQuest(s, auto_rebirth=self.o.auto_rebirth)
                    complete.add(s)
                    self.raid_check_and_send()
                    if raid_team is not None:
                        self.do_raids(raid_team)
                except KeyboardInterrupt:
                    return False
                except:
                    self.log_err('failed stage: %s area: %s' % (s, stage['m_area_id']))
                    blacklist.add(stage['m_area_id'])
                    continue
                self.player_stone_sum()
                self.player_items()
                i += 1

    def useCodes(self, codes):
        for c in codes:
            self.client.boltrend_exchange_code(c)
        self.get_mail()

    def spin_hospital(self):
        # Server time is utc -4. Spins available every 8 hours
        last_roulete_time_string = self.client.hospital_index()['result']['last_hospital_at']
        last_roulette_time = parser.parse(last_roulete_time_string)
        utcminus4time = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
        if utcminus4time > last_roulette_time + datetime.timedelta(hours=8):
            self.client.hospital_roulette()

    def do_bingo(self):
        self.client.bingo_index(Constants.Current_Bingo_ID)
        if self.bingo_is_spin_available():
            spin_result = self.client.bingo_lottery(Constants.Current_Bingo_ID, False)
            spin_index = spin_result['result']['t_bingo_data']['last_bingo_index']
            self.log(
                f"Bingo spinned. Obtained number {spin_result['result']['t_bingo_data']['display_numbers'][spin_index]}.")
            free_reward_positions = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
            bingo_rewards = spin_result['result']['rewards']
            free_rewards = [bingo_rewards[i] for i in free_reward_positions]
            available_free_rewards = [x for x in free_rewards if x['status'] == 1]
            if len(available_free_rewards) > 0:
                print(f"There are {len(available_free_rewards)} free rewards available to claim.")

    def is_helper_in_friend_list(self, player_id):
        all_friends = self.client.friend_index()['result']['friends']
        friend = next((x for x in all_friends if x['id'] == player_id), None)
        return friend is not None


    def dump_player_data(self, file_path: str):
        self.player_stone_sum()
        self.player_decks(True)
        self.player_items(True)
        self.player_weapons(True)
        self.player_equipment(True)
        self.player_innocents(True)
        self.player_characters(True)
        self.player_character_collections(True)
        self.getDone()
        self.player_stage_missions(True)
        self.pd.dump_to_file(file_path, {
            "app_constants": self.client.app_constants()['result'],
        })
