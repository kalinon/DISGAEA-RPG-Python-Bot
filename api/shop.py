from abc import ABCMeta

from api.player import Player


class Shop(Player, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def shop_equipment_items(self):
        data = self.rpc('shop/equipment_items', {})
        return data

    def shop_equipment_shop(self):
        data = self.rpc('shop/equipment_shop', {})
        return data

    def shop_buy_equipment(self, item_type, itemid):
        data = self.rpc('shop/buy_equipment', {"item_type": item_type, "ids": [itemid]})
        return data

    def shop_change_equipment_items(self, shop_rank=1):
        data = self.rpc('shop/change_equipment_items', {"shop_rank": shop_rank})
        return data

    def buyAll(self, minrarity=None):
        items = self.shop_equipment_items()['result']['_items']
        for i in items:
            if i['sold_flg']:    continue
            if minrarity is not None and i['rarity'] < minrarity:    continue
            self.log('found item:%s rare:%s' % (i['id'], i['rarity']))
            self.shop_buy_equipment(item_type=i['item_type'], itemid=i['id'])

    def shop_buy_item(self, itemid, quantity):
        data = self.rpc('shop/buy_item', {"id": itemid, "quantity": quantity})
        return data

    def shop_sell_equipment(self, sell_equipments):
        data = self.rpc('shop/sell_equipment', {"sell_equipments": sell_equipments})
        return data

    # max_innocent_rank (effect_rank)
    #   ancient = 11+
    #   legendary = 9-10
    #   rare = 5-8
    #   common = 1-4
    def sellItems(self, max_rarity=40, max_rank=100, keep_max_lvl=False, only_max_lvl=False, max_innocent_rank=10,
                  max_innocent_type=8):
        self.player_equipments()
        self.player_weapons()
        selling, skipping = self.filter_items(
            skip_max_lvl=keep_max_lvl, max_innocent_rank=max_innocent_rank, max_innocent_type=max_innocent_type,
            max_rank=max_rank, max_rarity=max_rarity,
            only_max_lvl=only_max_lvl)

        self.log('skipping %s items' % skipping)
        if len(selling) >= 1:
            self.shop_sell_equipment(selling)

    def filter_items(self, skip_max_lvl=False, max_innocent_rank=10, max_innocent_type=8, max_rank=100, max_rarity=40,
                     only_max_lvl=False, skip_equipped=True, skip_locked=True):
        selling = []
        skipping = 0
        for w in self.weapons:
            if not self.check_item(item=w, max_rarity=max_rarity, max_rank=max_rank,
                                   skip_max_lvl=skip_max_lvl, only_max_lvl=only_max_lvl,
                                   skip_equipped=skip_equipped, skip_locked=skip_locked,
                                   max_innocent_rank=max_innocent_rank, max_innocent_type=max_innocent_type):
                skipping += 1
                continue
            self.log_sell(w)
            selling.append({'eqtype': 1, 'eqid': w['id']})
        for w in self.equipments:
            if not self.check_item(item=w, max_rarity=max_rarity, max_rank=max_rank,
                                   skip_max_lvl=skip_max_lvl, only_max_lvl=only_max_lvl,
                                   skip_equipped=skip_equipped, skip_locked=skip_locked,
                                   max_innocent_rank=max_innocent_rank, max_innocent_type=max_innocent_type):
                skipping += 1
                continue
            self.log_sell(w)
            selling.append({'eqtype': 2, 'eqid': w['id']})
        return selling, skipping

    def log_sell(self, w):
        item = self.getWeapon(w['m_weapon_id']) if 'm_weapon_id' in w else self.getEquip(w['m_equipment_id'])
        self.log(
            '[-] sell item: "%s" rarity: %s rank: %s lv: %s lv_max: %s locked: %s' %
            (item['name'], w['rarity_value'], self.get_item_rank(w), w['lv'],
             w['lv_max'], w['lock_flg'])
        )

    def check_item(self, item: object, max_rarity: int = 99, max_rank: int = 39,
                   min_rarity: int = 0, min_rank: int = 0,
                   skip_max_lvl: bool = False, only_max_lvl: bool = False,
                   skip_equipped: bool = False, skip_locked: bool = True,
                   max_innocent_rank: int = 8, max_innocent_type: int = 8,
                   min_innocent_rank: int = 0, min_innocent_type: int = 0) -> bool:
        if skip_max_lvl and item['lv'] == item['lv_max']:
            # self.log('skip due to lv_max')
            return False
        if skip_locked and item['lock_flg']:
            # self.log('skip due to lock_flg')
            return False

        rank = self.get_item_rank(item)
        if rank > max_rank:
            # self.log('skip due to max_rank')
            return False
        if rank < min_rank:
            # self.log('skip due to min_rank')
            return False

        if item['rarity_value'] > max_rarity:
            # self.log('skip due to max_rarity')
            return False
        if item['rarity_value'] < min_rarity:
            # self.log('skip due to min_rarity')
            return False

        if skip_equipped and item['set_chara_id'] != 0:
            # self.log('skip due to equipped to char')
            return False

        innos = self.get_item_innocents(item)
        if min_innocent_rank > 0 or min_innocent_type > 0:
            if len(innos) == 0:
                return False

        for i in innos:
            if i and i['effect_rank'] > max_innocent_rank:
                # self.log('skip due to max_innocent_rank')
                return False
            if i['innocent_type'] > max_innocent_type:
                # self.log('skip due to max_innocent_type')
                return False

            if i and i['effect_rank'] < min_innocent_rank:
                # self.log('skip due to min_innocent_rank')
                return False
            if i['innocent_type'] < min_innocent_type:
                # self.log('skip due to min_innocent_type')
                return False

        if only_max_lvl and item['lv'] < item['lv_max']:
            # self.log('skip due to only_max_lvl')
            return False
        return True
