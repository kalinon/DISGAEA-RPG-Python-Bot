from typing import Iterable

from api.constants import EquipmentType
from api.game_data import GameData
from api.logger import Logger
from api.options import Options


class PlayerData:
    def __init__(self, options):
        self.gd: GameData = GameData()
        self.o: Options = options
        self.decks: [dict[Iterable]] = []
        self.gems: [dict[Iterable]] = []
        self.items: [dict[Iterable]] = []
        self.weapons: [dict[Iterable]] = []
        self.equipment: [dict[Iterable]] = []
        self.innocents: [dict[Iterable]] = []
        self.characters: [dict[Iterable]] = []
        self.character_collections: [dict[Iterable]] = []

    @property
    def get_current_deck(self):
        return self.deck(self.o.team_num) if self.o.auto_rebirth else []

    def deck(self, team_num: int = None):
        if team_num is None:
            deck_index = self.o.deck_index
        else:
            deck_index = team_num - 1

        deck = self.decks[deck_index]
        d = []
        for x in deck['t_character_ids']:
            if deck['t_character_ids'][x] != 0:
                d.append(deck['t_character_ids'][x])
        return d

    def get_character_by_id(self, _id: int):
        for i in self.characters:
            if i['id'] == _id:
                return i
        return None

    def get_character_by_m_character_id(self, m_character_id: int):
        character = next((x for x in self.characters if x['m_character_id'] == m_character_id), None)        
        return character

    def get_character_collection_by_id(self, _id: int):
        for i in self.character_collections:
            if i['id'] == _id:
                return i
        return None

    def get_character_collection_by_mid(self, _id: int):
        for i in self.character_collections:
            if i['m_character_id'] == _id:
                return i
        return None

    # Returns a list of player items with matching m_item_id
    def get_item_by_m_item_id(self, m_item_id):
        item = next((x for x in self.items if x['m_item_id']== m_item_id),None)
        return item

    def get_item_by_id(self, iid):
        for i in self.items:
            if i['id'] == iid:
                return i
        return None

    def update_items(self, result):
        if 't_items' in result:
            for item in result['t_items']:
                if 'id' in item:
                    index = self.items.index(self.get_item_by_id(item['id']))
                    self.items[index] = item

    def get_weapon_by_id(self, eid):
        for w in self.weapons:
            if w['id'] == eid:
                return w
        return None

    def get_equipment_by_id(self, eid):
        for w in self.equipment:
            if w['id'] == eid:
                return w
        return None

    def get_innocent_by_id(self, iid):
        for inno in self.innocents:
            if inno['id'] == iid:
                return inno
        return None

    def update_equip(self, result):
        if 't_weapon' in result:
            index = self.weapons.index(self.get_weapon_by_id(result['t_weapon']['id']))
            self.weapons[index] = result['t_weapon']
        elif 't_equipment' in result:
            index = self.equipment.index(self.get_equipment_by_id(result['t_equipment']['id']))
            self.equipment[index] = result['t_equipment']
        else:
            Logger.warn("unable to update item from result")

    def update_innocent(self, inno):
        old_inno = self.get_innocent_by_id(inno['id'])
        index = self.innocents.index(old_inno)
        self.innocents[index] = inno

    # e can be an equipment id or actual equipment/weapon
    def get_item_innocents(self, e):
        if isinstance(e, int):
            place_id = e
        elif 'm_weapon_id' in e:
            place_id = e['id']
        elif 'm_equipment_id' in e:
            place_id = e['id']
        elif 'id' in e:
            place_id = e['id']
        else:
            raise Exception('unable to determine item id')

        equipment_innocents = []
        for i in self.innocents:
            if i['place_id'] == place_id:
                equipment_innocents.append(i)
        return equipment_innocents

    # Will check item against provided settings and return True if it meets the criteria
    def check_item(self, item: dict,
                   max_rarity: int = 99, min_rarity: int = 0,
                   max_item_rank: int = 39, min_item_rank: int = 0,
                   max_item_level: int = 9999, min_item_level: int = 0,
                   skip_max_lvl: bool = False, only_max_lvl: bool = False,
                   skip_equipped: bool = False, skip_locked: bool = True,
                   max_innocent_rank: int = 8, max_innocent_type: int = 8,
                   min_innocent_rank: int = 0, min_innocent_type: int = 0,
                   min_inocent_count:int = 0, max_inocent_count:int = 999,
                   item_type: int = 0) -> bool:

        # Change this to DEBUG (10) or INFO (20) if you want to see logs
        log_level = 0
        if log_level > 0:
            self.__log_item("checking", item)

        equip_type = self.get_equip_type(item)
        rank = self.gd.get_item_rank(item)

        if 0 < item_type != equip_type:
            Logger.log('skip due to item_type', log_level)
            return False
        if skip_max_lvl and item['lv'] == item['lv_max']:
            Logger.log('skip due to lv_max', log_level)
            return False
        if skip_locked and item['lock_flg']:
            Logger.log('skip due to lock_flg', log_level)
            return False
        if item['lv'] > max_item_level:
            Logger.log('skip due to max_item_level', log_level)
            return False
        if item['lv'] < min_item_level:
            Logger.log('skip due to min_item_level', log_level)
            return False
        if rank > max_item_rank:
            Logger.log('skip due to max_item_rank', log_level)
            return False
        if rank < min_item_rank:
            Logger.log('skip due to min_item_rank', log_level)
            return False
        if item['rarity_value'] > max_rarity:
            Logger.log('skip due to max_rarity', log_level)
            return False
        if item['rarity_value'] < min_rarity:
            Logger.log('skip due to min_rarity', log_level)
            return False
        if skip_equipped and item['set_chara_id'] != 0:
            Logger.log('skip due to equipped to char', log_level)
            return False

        innos = self.get_item_innocents(item)
        if len(innos) > max_inocent_count:
            Logger.log('skip due to max innocent count', log_level)
            return False

        if len(innos) < min_inocent_count:
            Logger.log('skip due to min innocent count', log_level)
            return False

        if min_innocent_rank > 0 or min_innocent_type > 0:
            if len(innos) == 0:
                Logger.log('skip due to missing innocent', log_level)
                return False

        for i in innos:
            if i and i['effect_rank'] > max_innocent_rank:
                Logger.log('skip due to max_innocent_rank', log_level)
                return False
            if i['innocent_type'] > max_innocent_type:
                Logger.log('skip due to max_innocent_type', log_level)
                return False

            if i and i['effect_rank'] < min_innocent_rank:
                Logger.log('skip due to min_innocent_rank', log_level)
                return False
            if i['innocent_type'] < min_innocent_type:
                Logger.log('skip due to min_innocent_type', log_level)
                return False

        if only_max_lvl and item['lv'] < item['lv_max']:
            Logger.log('skip due to only_max_lvl', log_level)
            return False            

        Logger.log('item passed check', log_level)
        return True

    def filter_items(self, max_rarity: int = 99, min_rarity: int = 0,
                     max_item_rank: int = 39, min_item_rank: int = 0,
                     max_item_level: int = 9999, min_item_level: int = 0,
                     skip_max_lvl: bool = False, only_max_lvl: bool = False,
                     skip_equipped: bool = False, skip_locked: bool = True,
                     max_innocent_rank: int = 8, max_innocent_type: int = 8,
                     min_innocent_rank: int = 0, min_innocent_type: int = 0,
                     min_inocent_count: int = 0, max_inocent_count: int = 999,
                     item_type=0):
        matches = []
        skipping = 0
        for w in (self.weapons + self.equipment):
            result = self.check_item(item=w, max_rarity=max_rarity, max_item_rank=max_item_rank,
                                     min_rarity=min_rarity, min_item_rank=min_item_rank,
                                     max_item_level=max_item_level, min_item_level=min_item_level,
                                     skip_max_lvl=skip_max_lvl, only_max_lvl=only_max_lvl,
                                     skip_equipped=skip_equipped, skip_locked=skip_locked,
                                     max_innocent_rank=max_innocent_rank, max_innocent_type=max_innocent_type,
                                     min_innocent_rank=min_innocent_rank, min_innocent_type=min_innocent_type,
                                     min_inocent_count=min_inocent_count, max_inocent_count= max_inocent_count,
                                     item_type=item_type)
            if not result:
                skipping += 1
                continue
            matches.append(w)
        return matches, skipping

    def get_equip_type(self, item):
        return EquipmentType.WEAPON if 'm_weapon_id' in item else EquipmentType.ARMOR

    def innocent_get_all_of_type(self, m_innocent_id, only_unequipped):
        innocents_of_type = [x for x in self.innocents if x['m_innocent_id'] == m_innocent_id]
        if only_unequipped:
            innocents_of_type = [x for x in innocents_of_type if x['place_id'] == 0 and x['place'] == 0]
        return innocents_of_type

    def __log_item(self, msg, w):
        item = self.gd.get_weapon(w['m_weapon_id']) if 'm_weapon_id' in w else self.gd.get_weapon(w['m_equipment_id'])
        Logger.info(
            '%s: "%s" rarity: %s rank: %s lv: %s lv_max: %s locked: %s' %
            (msg, item['name'], w['rarity_value'], self.gd.get_item_rank(w), w['lv'],
             w['lv_max'], w['lock_flg'])
        )
