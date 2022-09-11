import json

from main import API

a = API()
# a.setProxy("127.0.0.1:8080")
a.o.wait = 0
a.o.set_region(2)
a.o.set_device(3)


def read_file(file_path):
    file = open(file_path)
    data = json.loads(file.read())
    file.close()
    return data


def load_data():
    data = read_file('player_data.json')
    a.pd.decks = data['decks']
    a.pd.gems = data['gems']
    a.pd.items = data['items']
    a.pd.weapons = data['weapons']
    a.pd.equipment = data['equipment']
    a.pd.innocents = data['innocents']
    a.pd.characters = data['characters']
    a.pd.character_collections = data['character_collections']
    a.pd.clear_stages = data['clear_stages']
    a.pd.stage_missions = data['stage_missions']
    return data['extra_data']['app_constants']


def complete_recipes(skip_equipped: bool = False):
    inno_blacklist = [x['id'] for x in a.find_recipe_innocents(True)]
    tickets_used = {}
    tickets_to_buy = {}
    conversions = []

    for recipe in a.gd.innocent_recipes:
        # if recipe['id'] != 1:
        #     continue

        materials = recipe['materials']
        mat_map = {material['id']: a.find_recipe_material_innocents(material) for material in materials}
        missing = 0
        missing_mats = []
        for mat in materials:
            # if we are missing mats, lets see if we can find an innocent to convert
            if len(mat_map[mat['id']]) == 0:
                missing += 1
                missing_mats.append(mat)
        # if there are none missing, then recipe can be completed
        if missing == 0:
            a.log('recipe %s can be completed!' % recipe['name'])
            continue
        else:
            a.log('recipe %s is missing %d materials' % (recipe['name'], missing))

        # gather all the possible conversions
        innocent_conversions = innocents_to_convert(recipe)
        for mat in missing_mats:
            for data in innocent_conversions:
                i = a.pd.get_innocent_by_id(data['subject_id'])
                # Skip equipped if true and on an equipment
                if skip_equipped and i['place_id'] > 0:
                    continue

                # skip if it's not the right material
                if data['material_id'] != mat['id']:
                    continue

                # Skip if it's in the blacklist
                if data['subject_id'] in inno_blacklist:
                    continue

                # Check if we have tickets
                ticket_item_def = a.gd.get_ranch_ticket(data['target_character_id'])
                ticket_item = a.pd.get_item_by_id(data['ticket_id'])
                if ticket_item['id'] not in tickets_used:
                    tickets_used[ticket_item['id']] = 0
                # Skip if we are out of tickets to convert
                if tickets_used[ticket_item['id']] >= ticket_item['num']:
                    if ticket_item_def['id'] not in tickets_to_buy:
                        tickets_to_buy[ticket_item_def['id']] = 0
                    tickets_to_buy[ticket_item_def['id']] += 1
                    continue

                # If we are here we can do this conversion
                conversions.append(data)
                inno_blacklist.append(data['subject_id'])
                tickets_used[ticket_item['id']] += 1
                break
    conversions.sort(key=sort_data)
    for data in conversions:
        log_conversion(data)


def sort_data(e):
    return e['target_character_id']


def log_conversion(data):
    recipe = a.gd.get_innocent_recipe(data['recipe_id'])

    # Grab human-readable names
    target_type_name = a.gd.get_innocent_type(data['target_innocent_id'])['name']
    target_char = a.gd.get_character(data['target_character_id'])
    target_char_name = "%s %s" % (
        target_char['name'], target_char['linkage_character_ids'].index(data['target_character_id']) + 1)

    subject_char = a.gd.get_character(data['subject_character_id'])
    subject_char_name = "%s %s" % (
        subject_char['name'], subject_char['linkage_character_ids'].index(data['subject_character_id']) + 1)

    i = a.pd.get_innocent_by_id(data['subject_id'])

    ticket_item_def = a.gd.get_ranch_ticket(data['target_character_id'])
    ticket_item = a.pd.get_item_by_id(data['ticket_id'])

    rank = a.gd.get_innocent_rank(i['effect_rank'])

    # a.log(
    #     'complete_recipes - %s - want to convert '
    #     'innocent: [id: %s, type: "%s", char: "%s", rank: %s, value: %s] to type "%s" - ticket: "%s"' % (
    #         recipe['name'],
    #         data['subject_id'],
    #         target_type_name,
    #         subject_char_name,
    #         a.gd.get_innocent_rank(i['effect_rank']),
    #         i['effect_values'][0],
    #         target_char_name,
    #         ticket_item_def['name'],
    #     ))

    print('ticket: "%s" -> "%s" : "%s" %s' % (
        ticket_item_def['name'], target_type_name, subject_char_name, i['effect_values'][0]))


# will provide a list of innocents that could be converted to complete recipe
def innocents_to_convert(recipe):
    conversions = []
    materials = recipe['materials']
    map = {material['id']: a.find_recipe_material_innocents(material) for material in materials}
    for mat in materials:
        # if we are missing mats, lets see if we can find an innocent to convert
        if len(map[mat['id']]) == 0:
            min_r, max_r = a.gd.get_innocent_rank_min_max(mat['rank'])
            m_character_id = mat['m_character_id']
            m_innocent_id = mat['m_innocent_id']

            # Gather ticket info for conversion
            ticket_item_def = a.gd.get_ranch_ticket(m_character_id)
            ticket_item = a.pd.get_item_by_m_item_id(ticket_item_def['id'])

            # a.log('complete_recipes - %s - missing materials, mat_id: %s' % (recipe['name'], mat['id']))
            # look for an innocent with matching rank and type
            for i in a.pd.innocents:
                if min_r <= i['effect_rank'] <= max_r and i['m_innocent_id'] == m_innocent_id:
                    conversions.append({
                        'recipe_id': recipe['id'],
                        'material_id': mat['id'],
                        'target_character_id': m_character_id,
                        'target_innocent_id': m_innocent_id,
                        'subject_id': i['id'],
                        'subject_character_id': i['m_character_id'],
                        'subject_innocent_id': m_innocent_id,
                        'ticket_id': ticket_item['id'],
                    })

                    # conversions.append((
                    #     recipe['name'],
                    #     target_type_name,
                    #     i['id'],
                    #     target_char_name,
                    #     i['effect_rank'],
                    #     subject_char_name,
                    # ))
    return conversions


a.quick_login()
a.dump_player_data("./player_data.json")

# If you want to run this offline, then comment out above, and uncomment below.
# load_data()

complete_recipes(skip_equipped=True)
