import json

from api.game_data import GameData
from api.options import Options
from api.player_data import PlayerData

options: Options = Options(region=1, device=1)
pd: PlayerData = PlayerData(options)
gd: GameData = GameData()


def load_data():
    data = read_file('player_data.json')
    pd.decks = data['decks']
    pd.gems = data['gems']
    pd.items = data['items']
    pd.weapons = data['weapons']
    pd.equipment = data['equipment']
    pd.innocents = data['innocents']
    pd.characters = data['characters']
    pd.character_collections = data['character_collections']
    pd.clear_stages = data['clear_stages']
    pd.stage_missions = data['stage_missions']
    return data['extra_data']['app_constants']


def read_file(file_path):
    file = open(file_path)
    data = json.loads(file.read())
    file.close()
    return data


app_constants = load_data()


# dump_dir = '/Users/homans/Downloads/DMP_p2/'
# inno_data = {
#     "defs": read_file(dump_dir + 'MasterInnocentData.json'),
#     "effect_values": read_file(dump_dir + 'MasterInnocentEffectValueData.json'),
#     "recipes": read_file(dump_dir + 'MasterInnocentRecipeData.json'),
#     "recipe_materials": read_file(dump_dir + 'MasterInnocentRecipeMaterialData.json'),
#     "trainers": read_file(dump_dir + 'MasterInnocentTrainerData.json'),
# }
#
# recipes = []
# for recipe in inno_data['recipes']:
#     recipe['materials'] = []
#     for mat in inno_data['recipe_materials']:
#         if mat['m_innocent_recipe_id'] != recipe['id']:
#             continue
#         recipe['materials'].append(mat)
#     recipes.append(recipe)
#
# file = open('data/innocent_recipes.json', 'w')
# file.write(json.dumps(recipes, indent=2))
# file.close()

def find_innocent(innocent_id: int, character_id: int, rank: int):
    min_rank, max_rank = gd.get_innocent_rank_min_max(rank)

    innos = []
    for i in pd.innocents:
        if i['m_innocent_id'] != innocent_id:
            continue
        if i['m_character_id'] != character_id:
            continue
        if max_rank >= i['effect_rank']:
            innos.append(i)
    return innos


def find_recipe_innocents():
    innos = []
    for i in pd.innocents:
        if i['m_innocent_id'] in gd.innocent_recipe_map:
            if i['m_character_id'] in gd.innocent_recipe_map[i['m_innocent_id']]:
                rank = gd.get_innocent_rank(i['effect_rank'])
                if rank in gd.innocent_recipe_map[i['m_innocent_id']][i['m_character_id']]:
                    innos.append(i)
    return innos


print(len(find_recipe_innocents()))
