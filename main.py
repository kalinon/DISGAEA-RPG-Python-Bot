# -*- coding: utf-8 -*-
import requests
import string
import random
from data import data as gamedata
from api import BaseAPI

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

head = {'version_check': 0, 'signup': 1, 'login': 1, 'rpc': 2}


class API(BaseAPI):
    def __init__(self):
        super().__init__()
        self.items = None
        self.gems = None
        self.done = set()

    def passport_index(self):
        data = self.rpc('passport/index', {})
        return data

    def get_mail_and_rewards(self):
        self.trophy_get_reward_daily()
        self.trophy_get_reward()
        self.trophy_get_reward()
        self.trophy_get_reward()
        self.trophy_get_reward()
        self.trophy_get_reward()
        self.getmail()
        self.getmail()
        self.getmail()
        self.getmail()
        self.getmail()

    def dofarm(self):
        # self.buyRare()
        self.get_mail_and_rewards()
        if True:
            self.shop_buy_item(itemid=9, quantity=1)
            self.shop_buy_item(itemid=8, quantity=1)
            self.shop_buy_item(itemid=7, quantity=1)
            self.shop_buy_item(itemid=6, quantity=1)
            self.shop_buy_item(itemid=1012, quantity=1)
            self.shop_buy_item(itemid=1011, quantity=1)
            self.shop_buy_item(itemid=101, quantity=1)
            self.shop_buy_item(itemid=101, quantity=1)
            self.shop_buy_item(itemid=101, quantity=1)
            self.shop_buy_item(itemid=101, quantity=1)
            self.shop_buy_item(itemid=101, quantity=1)
        if True:
            self.sub_tutorial_read(m_sub_tutorial_id=31)
            self.sub_tutorial_read(m_sub_tutorial_id=8)
            self.sub_tutorial_read(m_sub_tutorial_id=7)
            self.sub_tutorial_read(m_sub_tutorial_id=1)
            self.sub_tutorial_read(m_sub_tutorial_id=19)
            self.sub_tutorial_read(m_sub_tutorial_id=21)
            self.sub_tutorial_read(m_sub_tutorial_id=29)
            self.sub_tutorial_read(m_sub_tutorial_id=24)
            self.sub_tutorial_read(m_sub_tutorial_id=2)
            self.sub_tutorial_read(m_sub_tutorial_id=6)
            self.sub_tutorial_read(m_sub_tutorial_id=25)
            self.sub_tutorial_read(m_sub_tutorial_id=26)
        self.completeStory()

    def quick_login(self):
        self.login()
        self.player_characters(updated_at=0, page=1)
        self.player_weapons(updated_at=0, page=1)
        self.player_weapon_effects(updated_at=0, page=1)
        self.player_equipments(updated_at=0, page=1)
        self.player_equipment_effects(updated_at=0, page=1)
        self.player_items(updated_at=0, page=1)
        self.player_innocents(updated_at=0, page=1)
        self.player_index()
        self.player_character_collections()
        self.player_decks()
        self.player_stone_sum()
        self.player_characters(updated_at=0, page=1)

    def dologin(self):
        self.login()
        self.app_constants()
        self.player_tutorial()
        self.battle_status()
        # player/profile
        # player/sync
        self.player_characters(updated_at=0, page=1)
        self.player_weapons(updated_at=0, page=1)
        self.player_weapon_effects(updated_at=0, page=1)
        self.player_equipments(updated_at=0, page=1)
        self.player_equipment_effects(updated_at=0, page=1)
        self.player_items(updated_at=0, page=1)
        self.player_clear_stages(updated_at=0, page=1)
        self.player_stage_missions(updated_at=0, page=1)
        self.player_innocents(updated_at=0, page=1)
        self.player_index()
        self.player_agendas()
        self.player_boosts()
        self.player_character_collections()
        self.player_decks()
        self.friend_index()
        self.player_home_customizes()
        self.passport_index()
        self.player_stone_sum()
        self.player_sub_tutorials()
        self.system_version_manage()
        self.player_gates()
        self.event_index()
        self.stage_boost_index()
        self.information_popup()
        self.player_character_mana_potions()
        self.potential_current()
        self.potential_conditions()
        self.character_boosts()
        self.survey_index()
        self.kingdom_entries()
        self.breeding_center_list()
        self.trophy_daily_requests()
        self.weapon_equipment_update_effect_unconfirmed()
        self.memory_index()
        self.battle_skip_parties()
        # boltrend/subscriptions
        self.player_characters(updated_at=0, page=1)

    def addAccount(self):
        self.player_stone_sum()
        self.getmail()
        self.getmail()

    def trophy_beginner_missions(self, sheet_type=None):
        data = self.rpc('trophy/beginner_missions', {} if sheet_type is None else {'sheet_type': sheet_type})
        return data

    def raid_ranking_reward(self):
        data = self.rpc('raid/ranking_reward', {})
        return data

    def sub_tutorial_read(self, m_sub_tutorial_id):
        data = self.rpc('sub_tutorial/read', {"m_sub_tutorial_id": m_sub_tutorial_id})
        return data

    def present_history(self):
        data = self.rpc('present/history', {})
        return data

    def boltrend_exchange_code(self, code):
        data = self.rpc('boltrend/exchange_code', {"code": code})
        return data

    def rndAlp(self, n):
        return ''.join([random.choice(string.ascii_lowercase) for x in range(random.randint(n - 1, n))])

    def rndUser(self):
        return self.rndAlp(7).title()

    def doQuest(self, m_stage_id=101102):
        stage = self.getStage(m_stage_id)
        self.log('doing quest:%s [%s]' % (stage['name'], m_stage_id))
        if stage['exp'] == 0:
            return self.battle_story(m_stage_id)

        if stage['act'] > self.current_ap:
            self.log('not enough ap')
            return

        help_players = self.battle_help_list()['result']['help_players'][0]
        start = self.battle_start(m_stage_id=m_stage_id, help_t_player_id=help_players['t_player_id'],
                                  help_t_character_id=help_players['t_character']['id'], act=stage['act'],
                                  help_t_character_lv=help_players['t_character']['lv'])
        if 'result' not in start:
            return
        self.battle_help_list()
        end = self.battle_end(battle_exp_data=self.getbattle_exp_data(start), m_stage_id=m_stage_id, battle_type=1,
                              result=1, command_count=9)
        res = self.parseReward(end)
        return res

    def upgradeItems(self, only_weapons=False):
        self.player_innocents()

        self.player_weapons()
        self.upgrade_items(self.weapons, equipment_type=1)

        if only_weapons is False:
            self.player_equipments()
            self.upgrade_items(self.equipments, equipment_type=2)

    def upgrade_items(self, items, equipment_type):
        for w in filter(self.weapon_filter, items):
            self.trophy_get_reward_repetition()
            self.getmail()
            self.log_upgrade_item(w)
            while 1:
                if not self.doItemWorld(w['id'], equipment_type=equipment_type):
                    break

    def log_upgrade_item(self, w):
        item = self.getWeapon(w['m_weapon_id']) if 'm_weapon_id' in w else self.getEquip(w['m_equipment_id'])
        self.log(
            '[*] upgrade item: "%s" rarity: %s rank: %s lv: %s lv_max: %s locked: %s' %
            (item['name'], w['rarity_value'], self.get_item_rank(w), w['lv'],
             w['lv_max'], w['lock_flg'])
        )

    def doTower(self, m_tower_no=1):
        start = self.tower_start(m_tower_no)
        end = self.battle_end(battle_exp_data=self.getbattle_exp_data(start), m_tower_no=m_tower_no, m_stage_id=0,
                              battle_type=4, result=1, command_count=9)
        return end

    def doItemWorld(self, equipment_id=None, equipment_type=1):
        if equipment_id is None:
            self.log('missing equip')
            return
        start = self.item_world_start(equipment_id, equipment_type=equipment_type)

        if start is None or 'result' not in start:
            return False

        result = self.parseStart(start)
        end = self.battle_end(battle_exp_data=self.getbattle_exp_data(start), m_stage_id=0, battle_type=5,
                              result=result, command_count=9, equipment_type=equipment_type, equipment_id=equipment_id)
        res = self.getDiffWeapon(end)
        if res:
            self.log(res)
        if result == 5:
            self.log('did not drop anything good, retrying..')
            return self.doItemWorld(equipment_id=equipment_id, equipment_type=equipment_type)
        return res

    def getGain(self, t):
        for j in self.items:
            if j['m_item_id'] == t['m_item_id']:
                return t['num'] - j['num']

    def parseReward(self, end):
        drop_result = end
        rpcid = drop_result['id']
        event_points = drop_result['result']['after_t_event']['point'] if drop_result['result']['after_t_event'] else 0
        current_id = drop_result['result']['after_t_stage_current']['current_id']
        drop_result = drop_result['result']['drop_result']
        for e in drop_result:
            if e == 'after_t_item':
                for t in drop_result[e]:
                    i = self.getItem(t['m_item_id'])
                    self.log('%s +%s' % (i['name'], self.getGain(t)))
            elif e == 'drop_character':
                for t in drop_result[e]:
                    self.log('unit:%s lv:%s rarity:%s*' % (
                        self.getChar(t['m_character_id'])['class_name'], t['lv'], t['rarity']))
            elif e == 'stones':
                self.log('+%s nether quartz' % (drop_result[e][0]['num'] - self.gems))
        if event_points > 0:
            self.log('%s event points' % (event_points))

        return drop_result

    def getDone(self, page=1):
        if not hasattr(self, 'done'):
            self.done = set()
        r = self.player_clear_stages(updated_at=0, page=page)['result']['_items']
        if len(r) <= 0:
            return
        for i in r:
            if i['clear_num'] >= 1:
                self.done.add(i['m_stage_id'])
        return self.getDone(page + 1)

    def getAreaStages(self, m_area_id):
        ss = []
        for s in self.stages():
            if s['m_area_id'] == m_area_id:
                ss.append(s)
        return ss

    def completeStory(self, m_area_id=None, limit=None, farmingAll=False):
        if not farmingAll:
            self.getDone()
        ss = []
        for s in self.stages():
            ss.append(s['id'])
        ss.sort(reverse=False)
        # ss=sorted(ss)
        i = 0
        blacklist = set()
        for s in ss:
            if limit is not None and i >= limit:
                return False
            # print(s,self.getStage(s)['m_area_id'])
            if m_area_id is not None and m_area_id != self.getStage(s)['m_area_id']:
                continue
            if not farmingAll and s in self.done:
                continue
            if self.getStage(s)['m_area_id'] in blacklist:
                continue
            try:
                self.doQuest(s)
            except KeyboardInterrupt:
                return False
            except:
                # print(traceback.format_exc())
                self.log('failed %s %s' % (s, self.getStage(s)['m_area_id']))
                # return False
                blacklist.add(self.getStage(s)['m_area_id'])
                continue
            self.player_stone_sum()
            self.player_items()
            i += 1

    def useCodes(self):
        for c in ['5uf6dyc6gh', 'dp9GVSSnXG', 'dupj4kjfc3', 'f7wtnxk65h', 'j5zysmkvvv', 'ju56hvdwhz', 'nfefnysyy5',
                  'skfcqwykif', 'sqzvquhtqp', 'tcv5saaskw', 'xnv2ndstwp']:
            self.boltrend_exchange_code(c)
        self.getmail()

# if __name__ == "__main__":
#     a = API()
#     if False:
#         a.password = '26eYVYpYVdbwpPkq'
#         a.uuid = 'e08ed5d9-61a6-4055-a18e-9795d8f40f47'
#         a.dologin()
#     else:
#         a.reroll()
