from data import data as gamedata


class GameData:
    def __init__(self):
        self.stages = gamedata['stages']
        self.items = gamedata['items']
        self.characters = gamedata['characters']
        self.stages = gamedata['stages']
        self.weapons = gamedata['weapon']
        self.equipment = gamedata['equip']
        self.innocent_types = gamedata['innocent_types']
        self.equipment_effect_type = gamedata['equipment_effect_type']
        self.innocent_recipes = gamedata['innocent_recipes']
        self.innocent_recipe_map = self.__create_recipe_map()

    def __create_recipe_map(self):
        innocent_recipe_map = {}
        for recipe in self.innocent_recipes:
            for mat in recipe['materials']:
                inno_id = mat['m_innocent_id']
                if inno_id not in innocent_recipe_map:
                    innocent_recipe_map[inno_id] = {}
                char_id = mat['m_character_id']
                if char_id not in innocent_recipe_map[inno_id]:
                    innocent_recipe_map[inno_id][char_id] = []
                innocent_recipe_map[inno_id][char_id].append(mat['rank'])
        return innocent_recipe_map

    def get_equipment(self, i):
        for w in self.equipment:
            if w['id'] == i:
                return w
        return None

    def get_weapon(self, i):
        for w in self.weapons:
            if w['id'] == i:
                return w
        return None

    def get_stage(self, i):
        i = int(i)
        for s in self.stages:
            if i == s['id']:
                return s

    def get_item(self, i):
        for s in self.items:
            if i == s['id']:
                return s

    def get_character(self, i):
        for s in self.characters:
            if i == s['id']:
                return s

    def get_item_rank(self, e):
        item_rank = 140
        if 'm_weapon_id' in e:
            weapon = self.get_weapon(e['m_weapon_id'])
            if weapon is not None:
                item_rank = weapon['item_rank']
        elif 'm_equipment_id' in e:
            equip = self.get_equipment(e['m_equipment_id'])
            if equip is not None:
                item_rank = equip['item_rank']
        elif 'item_rank' in e:
            item_rank = e['item_rank']
        else:
            raise Exception('unable to determine item rank')
        if item_rank > 100:
            item_rank = item_rank - 100
        return item_rank

    def get_alchemy_effect(self, i):
        for s in self.equipment_effect_type:
            if i == s['id']:
                return s

    def get_innocent_type(self, iid: int):
        for x in self.innocent_types:
            if iid == x['id']:
                return x

    def get_innocent_rank_min_max(self, rank: int):
        if rank == 1:
            return 1, 4
        elif rank == 2:
            return 5, 8
        elif rank == 3:
            return 9, 10
        elif rank == 4:
            return 11, 99
        else:
            raise Exception('Unknown innocent rank of %s' % rank)

    def get_innocent_rank(self, effect_rank: int):
        if 1 <= effect_rank <= 4:
            return 1
        elif 5 <= effect_rank <= 8:
            return 2
        elif 9 <= effect_rank <= 10:
            return 3
        elif 11 <= effect_rank:
            return 4
        else:
            raise Exception('Unknown innocent effect rank of %s' % effect_rank)

    def get_ranch_ticket(self, m_character_id: int):
        for item in self.items:
            if 'Ranch Ticket' not in item['name']: continue
            if 'effect_value' in item and m_character_id in item['effect_value']:
                return item

    def get_innocent_recipe(self, rid: int):
        for x in self.innocent_recipes:
            if rid == x['id']:
                return x
