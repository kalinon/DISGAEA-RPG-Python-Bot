import os

from main import API
from data import data as gamedata

a = API()
# a.setProxy("127.0.0.1:8080")
a.sess = os.getenv('DRPG_TOKEN')
a.uin = os.getenv('DRPG_UIN')
a.setRegion(2)
a.setDevice(2)
a.dologin()

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
        a.doQuest(stage_id)
        a.raid_check_and_send()


def farm_item_world(team=1, min_rarity=40, min_rank=0, min_item_rank=0, min_item_level=0, only_weapons=False):
    a.onlyWeapons(only_weapons)
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
    a.upgradeItems()


def do_gate(gate, team):
    print("- running gate {}".format(gate['m_stage_id']))
    current = int(gate['challenge_num'])
    max = int(gate['challenge_max'])
    while current < max:
        a.setTeamNum(team)
        a.doQuest(gate['m_stage_id'])
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


def daily():
    a.get_mail_and_rewards()
    gates_data = a.player_gates()['result']
    do_gates(gates_data, gem_team=7, hl_team=8)


# Will return an array of event area ids based on the event id.
# clear_event([1132101, 1132102, 1132103, 1132104, 1132105])
def get_event_areas(event_id):
    tmp = event_id * 1000
    return [tmp + 101, tmp + 102, tmp + 103, tmp + 104, tmp + 105]


def clear_event(area_lt):
    dic = gamedata['stages']
    rank = [1, 2, 3]
    for k in rank:
        for i in area_lt:
            new_lt = [x for x in dic if x["m_area_id"] == i and x["rank"] == k]
            for c in new_lt:
                a.doQuest(c['id'])
                a.raid_check_and_send()


def use_ap(stage_id):
    print("- using ap")
    times = int(a.current_ap / 30)
    farm_event_stage(stage_id=stage_id, team=5, times=times)


def clear_inbox():
    print("- clearing inbox")
    ids = a.present_index(conditions=[0, 1, 2, 3, 4, 99], order=1)['result']['_items']
    last_id = None
    while len(ids) > 0:
        a.getmail()
        a.sellItems(max_rarity=69, max_rank=40, keep_max_lvl=True, only_max_lvl=False, max_innocent_rank=8,
                    max_innocent_type=8)
        ids = a.present_index(conditions=[0, 1, 2, 3, 4, 99], order=1)['result']['_items']
        new_last_id = ids[-1]
        if new_last_id == last_id:
            print("- inbox is empty or didnt change")
            break
        last_id = new_last_id


def loop(team=9, rebirth=False, farm_stage_id=313515):
    a.autoRebirth(rebirth)
    a.setTeamNum(team)

    if a.current_ap >= 6000:
        use_ap(stage_id=farm_stage_id)

    for i in range(30):
        print("- claiming rewards")
        a.get_mail_and_rewards()

        print("- farming item world")
        farm_item_world(team=team, min_rarity=0, min_rank=40, min_item_rank=40, min_item_level=0, only_weapons=False)

        print("- donate equipment")
        a.etna_donate(max_rarity=69, max_innocent_rank=8, max_innocent_type=5)
        a.etna_donate(max_rarity=69, max_innocent_rank=4, max_innocent_type=8)

        print("- selling items")
        a.sellItems(max_rarity=69, max_rank=40, keep_max_lvl=False, only_max_lvl=True, max_innocent_rank=8,
                    max_innocent_type=8)

        if a.current_ap >= 6000:
            use_ap(stage_id=farm_stage_id)

    clear_inbox()


# Daily tasks
daily()

# a.autoRebirth(True)
# a.setTeamNum(9)

# # Uncomment to clear a new event area. Provide the first 4 digits of the m_area_id.
# clear_event(get_event_areas(1132))

# 1132105312 - misc stage
# 1090105310 - Extra+ (HL)
# 1090105311 - Extra+ (EXP)
# 1090105312 - Extra+ (1★)
# farm_event_stage(1, 1090105312, team=9)

# Full loop
loop(team=9, rebirth=True, farm_stage_id=1132105312)
