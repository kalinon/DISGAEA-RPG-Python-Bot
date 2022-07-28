import os

from main import API

# from data import data as gamedata

a = API()
# a.setProxy("127.0.0.1:8080")
a.sess = os.getenv('DRPG_TOKEN')
a.uin = os.getenv('DRPG_UIN')
a.setRegion(2)
a.setDevice(2)
a.quick_login()

codes = [
    # "drpgxhayzink",
    # "drpgxredcloud",
    # "drpgxoreimova2",
    # "DRPGXberto",
    # "DRPGXFG",
]

for code in codes:
    a.boltrend_exchange_code(code)


def farm_event_stage(times, stage_id, team):
    a.setTeamNum(team)
    for i in range(times):
        do_quest(stage_id)


def farm_item_world(team=1, min_rarity=0, min_rank=0, min_item_rank=0, min_item_level=0, only_weapons=False):
    # Change the party: 1-9
    a.setTeamNum(team)
    # This changes the minimum rarity of equipments found in the item-world. 1 = common, 40 = rare, 70 = Legendary
    a.minrarity(min_rarity)
    # This changes the min rank of equipments found in the item-world
    a.minrank(min_rank)
    # Only upgrade items that have this # of levels or greater
    a.minItemLevel(min_item_level)
    # Only upgrade items with the following rank
    a.minItemRank(min_item_rank)
    # This runs item-world to level all your items.
    a.upgradeItems(only_weapons=only_weapons)


def do_gate(gate, team):
    a.log("[*] running gate {}".format(gate['m_stage_id']))
    current = int(gate['challenge_num'])
    max = int(gate['challenge_max'])
    while current < max:
        a.setTeamNum(team)
        do_quest(gate['m_stage_id'])
        current += 1


def do_gates(gates_data, gem_team=7, hl_team=8):
    print("- checking gates")
    team = 1
    for data in gates_data:
        print("- checking gate {}".format(data['m_area_id']))
        if data['m_area_id'] == 50102:
            team = hl_team
        elif data['m_area_id'] == 50107 or data['m_area_id'] == 50108:
            team = gem_team
        else:
            # skip exp gates
            continue

        for gate in data['gate_stage_data']:
            do_gate(gate, team)


def daily(bts=False, team=9):
    a.get_mail_and_rewards()

    if bts:
        a.setTeamNum(team)
        # Do BTS Events
        # 1132201101 - BTS Extra -EASY-
        # 1132201102 - BTS Extra -NORMAL-
        # 1132201103 - BTS Extra -HARD-
        for _ in range(10):
            do_quest(1132201103)

    # Do gates
    gates_data = a.player_gates()['result']
    do_gates(gates_data, gem_team=7, hl_team=8)


# Will return an array of event area ids based on the event id.
# clear_event([1132101, 1132102, 1132103, 1132104, 1132105])
def get_event_areas(event_id):
    tmp = event_id * 1000
    return [tmp + 101, tmp + 102, tmp + 103, tmp + 104, tmp + 105]


def clear_event(area_lt):
    dic = a.stages()
    rank = [1, 2, 3]
    for k in rank:
        for i in area_lt:
            new_lt = [x for x in dic if x["m_area_id"] == i and x["rank"] == k]
            for c in new_lt:
                do_quest(c['id'])


def use_ap(stage_id):
    a.log("[*] using ap")
    times = int(a.current_ap / 30)
    farm_event_stage(stage_id=stage_id, team=5, times=times)


def clear_inbox():
    a.log("[*] clearing inbox")
    ids = a.present_index(conditions=[0, 1, 2, 3, 4, 99], order=1)['result']['_items']
    last_id = None
    while len(ids) > 0:
        a.getmail()
        a.sellItems(max_rarity=69, max_rank=40, keep_max_lvl=True, only_max_lvl=False,
                    max_innocent_rank=8, max_innocent_type=8)
        ids = a.present_index(conditions=[0, 1, 2, 3, 4, 99], order=1)['result']['_items']
        if len(ids) == 0:
            break
        new_last_id = ids[-1]
        if new_last_id == last_id:
            print("- inbox is empty or didnt change")
            break
        last_id = new_last_id


def do_quest(stage_id):
    a.doQuest(stage_id)
    a.raid_check_and_send()


def refine_items(max_rarity: int = 99, max_rank: int = 9999, min_rarity: int = 90, min_rank: int = 40):
    a.log('[*] looking for items to refine')
    weapons = []
    equipments = []
    for i in a.weapons:
        if not a.check_item(item=i, max_rarity=max_rarity, max_rank=max_rank,
                            min_rarity=min_rarity, min_rank=min_rank,
                            skip_max_lvl=False, only_max_lvl=True,
                            skip_equipped=False, skip_locked=False,
                            max_innocent_rank=99, max_innocent_type=99,
                            min_innocent_rank=0, min_innocent_type=0):
            continue
        weapons.append(i)

    for i in a.equipments:
        if not a.check_item(item=i, max_rarity=max_rarity, max_rank=max_rank,
                            min_rarity=min_rarity, min_rank=min_rank,
                            skip_max_lvl=False, only_max_lvl=True,
                            skip_equipped=False, skip_locked=False,
                            max_innocent_rank=99, max_innocent_type=99,
                            min_innocent_rank=0, min_innocent_type=0):
            continue
        equipments.append(i)

    a.log('[*] refine_items: found %s weapons and %s equipment to refine' % (len(weapons), len(equipments)))

    for i in weapons:
        a.workshop_refine(i)
    for i in equipments:
        a.workshop_refine(i)


def loop(team=9, rebirth=False, farm_stage_id=313515, only_weapons=False):
    a.autoRebirth(rebirth)
    a.setTeamNum(team)

    if a.current_ap >= 6000:
        # if farm_stage_id is None:
        #     a.do_axel_contest_multiple_characters(6)
        # else:
        use_ap(stage_id=farm_stage_id)

    for i in range(30):
        print("- claiming rewards")
        a.get_mail_and_rewards()

        print("- farming item world")
        farm_item_world(team=team, min_rarity=0, min_rank=40, min_item_rank=40, min_item_level=0,
                        only_weapons=only_weapons)

        print("- donate equipment")
        a.etna_donate(max_rarity=69, max_innocent_rank=8, max_innocent_type=5)
        a.etna_donate(max_rarity=69, max_innocent_rank=4, max_innocent_type=8)
        refine_items(min_rarity=95, min_rank=40)
        a.etna_get_all_rewards()

        print("- selling items")
        a.sellItems(max_rarity=69, max_rank=40, keep_max_lvl=False, only_max_lvl=True, max_innocent_rank=8,
                    max_innocent_type=8)

        if a.current_ap >= 6000:
            use_ap(stage_id=farm_stage_id)

    clear_inbox()


# clear_inbox()

# a.do_axel_contest_multiple_characters(2)
# farm_event_stage(stage_id=114710104, times=10, team=6)
# do_quest(108410101)

# Daily tasks
daily(bts=False)

# a.autoRebirth(True)
# a.setTeamNum(9)

# # Uncomment to clear a new event area. Provide the first 4 digits of the m_area_id.
# clear_event(get_event_areas(1142))

# 314109 - misc stage
# 1142105310 - Extra+ (HL)
# 1142105311 - Extra+ (EXP)
# 1142105312 - Extra+ (1★)
# 114710104 - Defensive Battle 4

# farm_event_stage(1, 1142105312, team=9)

# Full loop
loop(team=9, rebirth=True, farm_stage_id=1142105312)
