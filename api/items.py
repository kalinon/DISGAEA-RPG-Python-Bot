from api.shop import Shop


class Items(Shop):
    def remove_innocents(self, e):
        innos = self.get_item_innocents(e)
        if len(innos) > 0:
            ids = []
            for i in innos:
                ids.append(i['id'])
            data = self.rpc("innocent/remove_all", {"t_innocent_ids": ids, "cost": 0})
            if data['result']['after_t_data']:
                self.update_equip_detail(e)
                for i in data['result']['after_t_data']['innocents']:
                    self.update_innocent(i)
            return data
        return {}

    def get_weapon_by_id(self, eid):
        for w in self.weapons:
            if w['id'] == eid:
                return w
        return None

    def get_equipment_by_id(self, eid):
        for w in self.equipments:
            if w['id'] == eid:
                return w
        return None

    def get_innocent_by_id(self, iid):
        for inno in self.innocents:
            if inno['id'] == iid:
                return inno
        return None

    def update_equip_detail(self, e, innos=[]):
        equip_type = 1 if self.get_weapon_by_id(e['id']) else 2
        data = self.rpc("player/update_equip_detail", {
            't_equip_id': e['id'],
            'equip_type': equip_type,
            'lock_flg': e['lock_flg'],
            'innocent_auto_obey_flg': e['innocent_auto_obey_flg'],
            'change_innocent_list': innos
        })
        if 't_weapon' in data['result']:
            index = self.weapons.index(e)
            self.weapons[index] = data['result']['t_weapon']
        elif 't_equipment' in data['result']:
            index = self.equipments.index(e)
            self.equipments[index] = data['result']['t_equipment']
        else:
            self.log("unable to update item with id: {0}".format(e['id']))

    def update_innocent(self, inno):
        old_inno = self.get_innocent_by_id(inno['id'])
        index = self.innocents.index(old_inno)
        self.innocents[index] = inno

    def kingdom_weapon_equipment_entry(self, weap_ids=[], equip_ids=[]):
        data = self.rpc("kingdom/weapon_equipment_entry", {'t_weapon_ids': weap_ids, 't_equipment_ids': equip_ids})
        if len(weap_ids) > 0:
            self.player_weapons(updated_at=0, page=1)
        if len(equip_ids) > 0:
            self.player_equipments(updated_at=0, page=1)
        return data

    def kingdom_innocent_entry(self, innocent_ids=[]):
        data = self.rpc("kingdom/innocent_entry", {'t_innocent_ids': innocent_ids})
        self.player_innocents(updated_at=0, page=1)
        return data

    # innocent_type
    #   1 = HP
    #   2 = ATK
    #   3 = DEF
    #   4 = INT
    #   5 = RES
    #   6 = SPD
    #   7 = EXP Boost
    #   8 = HL Boost
    #   9 = WM Enhancer
    #   10 = Skill Enhancer
    #   11 = HP Amplifier
    #   12 = ATK Amplifier
    #   13 = DEF Amplifier
    #   14 = INT Amplifier
    #   15 = RES Amplifier
    #   16 = Axe ATK Boost
    #   17+ = ????
    # max_innocent_rank (effect_rank)
    #   ancient = 11+
    #   legendary = 9-10
    #   rare = 5-8
    #   common = 1-4
    def etna_donate(self, max_rarity=40, max_innocent_rank=8, max_innocent_type=8):
        self.etna_donate_items(max_rarity=max_rarity, max_innocent_rank=max_innocent_rank,
                               max_innocent_type=max_innocent_type)

        self.etna_donate_innocents(max_innocent_rank, max_innocent_type)

        # Refresh data
        self.player_equipments()
        self.player_weapons()
        self.player_innocents()

    def _filter_innocent(self, i, max_innocent_rank, max_innocent_type):
        if i['place_id'] > 0:
            return False
        if i['effect_rank'] > max_innocent_rank:
            return False
        if i['innocent_type'] > max_innocent_type:
            return False

        return True

    def etna_donate_innocents(self, max_innocent_rank=8, max_innocent_type=8):
        self.player_innocents()
        innos = []
        skipping = 0
        for i in self.innocents:
            if not self._filter_innocent(i, max_innocent_rank, max_innocent_type):
                skipping += 1
                continue
            innos.append(i['id'])

        self.log('donate - skipping %s innocents' % skipping)
        if len(innos) > 0:
            for batch in (innos[i:i + 20] for i in range(0, len(innos), 20)):
                self.kingdom_innocent_entry(innocent_ids=batch)

    def etna_donate_items(self, max_rarity=40, max_rank=100, max_innocent_rank=10, max_innocent_type=8):
        self.player_equipments()
        self.player_weapons()
        self.player_innocents()

        items = []
        weaps = []

        selling, skipping = self.filter_items(False, max_innocent_rank, max_innocent_type, max_rank, max_rarity, True)

        self.log('donate - skipping %s items' % skipping)
        if len(selling) > 0:
            for i in selling:
                e = self.get_equipment_by_id(i['eqid']) or self.get_weapon_by_id(i['eqid'])
                self.log_donate(e)
                try:
                    self.remove_innocents(e)
                    if i['eqtype'] == 1:
                        weaps.append(i['eqid'])
                    if i['eqtype'] == 2:
                        items.append(i['eqid'])
                except:
                    e = None

        for batch in (items[i:i + 20] for i in range(0, len(items), 20)):
            self.kingdom_weapon_equipment_entry(equip_ids=batch)
        for batch in (weaps[i:i + 20] for i in range(0, len(weaps), 20)):
            self.kingdom_weapon_equipment_entry(weap_ids=batch)

    def log_donate(self, w):
        item = self.getWeapon(w['m_weapon_id']) if 'm_weapon_id' in w else self.getEquip(w['m_equipment_id'])
        self.log(
            '[-] donate item: "%s" rarity: %s rank: %s lv: %s lv_max: %s locked: %s' %
            (item['name'], w['rarity_value'], self.get_item_rank(w), w['lv'],
             w['lv_max'], w['lock_flg'])
        )
