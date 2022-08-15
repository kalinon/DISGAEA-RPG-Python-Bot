import os

from api.constants import Constants, EquipmentType, Innocent_ID, Fish_Fleet_Survey_Duration
from main import API

a = API()
# a.setProxy("127.0.0.1:8080")
a.config(
    sess=os.getenv('DRPG_TOKEN', default=Constants.session_id),
    uin=os.getenv('DRPG_UIN', default=Constants.user_id),
    wait=0,
    region=2,
    device=2
)
a.quick_login()

codes = [
    # "drpgxhayzink",
    # "drpgxredcloud",
    # "drpgxoreimova2",
    # "DRPGXberto",
    # "DRPGXFG",
]

for code in codes:
    a.client.boltrend_exchange_code(code)


def farm_event_stage(times, stage_id, team):
    a.o.team_num = team
    for i in range(times):
        do_quest(stage_id)


def farm_item_world(team=1, min_rarity=0, min_rank=0, min_item_rank=0, min_item_level=0, only_weapons=False,
                    item_limit=None):
    # Change the party: 1-9
    a.o.team_num = team
    # This changes the minimum rarity of equipments found in the item-world. 1 = common, 40 = rare, 70 = Legendary
    a.o.min_rarity = min_rarity
    # This changes the min rank of equipments found in the item-world
    a.o.min_rank = min_rank
    # Only upgrade items that have this # of levels or greater
    a.o.min_item_level = min_item_level
    # Only upgrade items with the following rank
    a.o.min_item_rank = min_item_rank

    items = a.items_to_upgrade()
    if len(items) == 0:
        refine_items(min_rarity=89, min_item_rank=40, limit=1)
        items = a.items_to_upgrade()

    if len(items) == 0:
        a.log_err('No items to farm! Where they all at?')
        exit(1)

    a.log('found %s items to upgrade' % len(items))

    # This runs item-world to level all your items.
    a.upgrade_items(only_weapons=only_weapons, ensure_drops=True, item_limit=item_limit, items=items)


def do_gate(gate, team):
    a.log("[*] running gate {}".format(gate['m_stage_id']))
    current = int(gate['challenge_num'])
    _max = int(gate['challenge_max'])
    while current < _max:
        a.o.team_num = team
        do_quest(gate['m_stage_id'])
        current += 1


def do_gates(gates_data, gem_team=7, hl_team=8):
    a.log("- checking gates")
    for data in gates_data:
        a.log("- checking gate {}".format(data['m_area_id']))
        if data['m_area_id'] == 50102:
            team = hl_team
        elif data['m_area_id'] == 50107 or data['m_area_id'] == 50108:
            team = gem_team
        else:
            # skip exp gates
            continue

        for gate in data['gate_stage_data']:
            if a.current_ap < 10:
                a.log('Too low on ap to do gates')
                return
            do_gate(gate, team)


def daily(bts: bool = False, team: int = 9, gem_team: int = 22, hl_team: int = 21):
    a.get_mail_and_rewards()
    send_sardines()

    # Buy items from HL shop
    # a.buy_daily_items_from_shop()

    if bts:
        a.o.team_num = team
        # Do BTS Events
        # 1132201101 - BTS Extra -EASY-
        # 1132201102 - BTS Extra -NORMAL-
        # 1132201103 - BTS Extra -HARD-
        for _ in range(10):
            do_quest(1132201103)

    # Do gates
    gates_data = a.client.player_gates()['result']
    do_gates(gates_data, gem_team=gem_team, hl_team=hl_team)


# Will return an array of event area ids based on the event id.
# clear_event([1132101, 1132102, 1132103, 1132104, 1132105])
def get_event_areas(event_id):
    tmp = event_id * 1000
    return [tmp + 101, tmp + 102, tmp + 103, tmp + 104, tmp + 105]


def clear_event(area_lt):
    dic = a.gd.stages
    rank = [1, 2, 3]
    for k in rank:
        for i in area_lt:
            new_lt = [x for x in dic if x["m_area_id"] == i and x["rank"] == k]
            for c in new_lt:
                do_quest(c['id'])


def use_ap(stage_id, event_team: int = 1):
    a.log("[*] using ap")

    if stage_id is None:
        for i in range(1, 5):
            for unit_id in a.pd.deck(i):
                a.do_axel_contest(unit_id, 1000)
    else:
        times = int(a.current_ap / 30)
        farm_event_stage(stage_id=stage_id, team=event_team, times=times)


def clear_inbox():
    a.log("[*] clearing inbox")
    ids = a.client.present_index(conditions=[0, 1, 2, 3, 4, 99], order=1)['result']['_items']
    last_id = None
    while len(ids) > 0:
        a.get_mail()

        ids = a.client.present_index(conditions=[0, 1, 2, 3, 4, 99], order=1)['result']['_items']
        if len(ids) == 0:
            break
        new_last_id = ids[-1]
        if new_last_id == last_id:
            a.log("- inbox is empty or didnt change")
            break
        # else:
        #     a.sell_items(max_rarity=69, max_item_rank=40, keep_max_lvl=True, only_max_lvl=False,
        #                  max_innocent_rank=8, max_innocent_type=Innocent_ID.HL)
        last_id = new_last_id


def do_quest(stage_id):
    a.doQuest(stage_id)
    a.raid_check_and_send()


def refine_items(max_rarity: int = 99, max_item_rank: int = 9999, min_rarity: int = 90, min_item_rank: int = 40,
                 limit=None):
    a.log('[*] looking for items to refine')
    weapons = []
    equipments = []

    items, skipped = a.pd.filter_items(max_rarity=max_rarity, max_item_rank=max_item_rank,
                                       min_rarity=min_rarity, min_item_rank=min_item_rank,
                                       skip_max_lvl=False, only_max_lvl=True,
                                       skip_equipped=False, skip_locked=False,
                                       max_innocent_rank=99, max_innocent_type=99,
                                       min_innocent_rank=0, min_innocent_type=0)

    if limit is not None:
        items = items[0:limit]

    for item in items:
        equip_type = a.pd.get_equip_type(item)
        if equip_type == EquipmentType.WEAPON:
            weapons.append(item)
        else:
            equipments.append(item)

    a.log('[*] refine_items: found %s weapons and %s equipment to refine' % (len(weapons), len(equipments)))

    for i in weapons:
        a.etna_resort_refine_item(i['id'])
    for i in equipments:
        a.etna_resort_refine_item(i['id'])


def send_sardines():
    # Send sardines
    player_data = a.client.player_index()
    if player_data['result']['act_give_count']['act_send_count'] == 0:
        a.client.friend_send_sardines()


def loop(team=9, rebirth: bool = False, farm_stage_id=None,
         only_weapons=False, iw_team: int = None, raid_team: int = None, event_team: int = None):
    a.o.auto_rebirth = rebirth
    a.o.team_num = team

    if iw_team is None:
        iw_team = team
    if raid_team is None:
        raid_team = team
    if event_team is None:
        event_team = team

    if a.current_ap >= 1000:
        use_ap(stage_id=farm_stage_id)

    while True:
        a.log("- claiming rewards and hospital")
        a.get_mail_and_rewards()
        a.spin_hospital()

        a.log("- checking item world survey")
        a.item_survey_complete_and_start_again(min_item_rank_to_deposit=40, auto_donate=True)

        a.log("- checking expeditions")
        a.survey_complete_all_expeditions_and_start_again(use_bribes=True, hours=Fish_Fleet_Survey_Duration.HOURS_24)

        a.log("- checking raids")
        a.do_raids(raid_team)

        a.log("- farming item world")
        farm_item_world(team=iw_team, min_rarity=0, min_rank=40, min_item_rank=40, min_item_level=0,
                        only_weapons=only_weapons, item_limit=5)

        a.log("- donate equipment")
        a.etna_donate_innocents(max_innocent_rank=4, max_innocent_type=Innocent_ID.RES)
        a.etna_resort_donate_items(max_item_rarity=69, max_innocent_rank=8, max_innocent_type=Innocent_ID.RES)
        a.etna_resort_donate_items(max_item_rarity=69, max_innocent_rank=4, max_innocent_type=8)
        a.etna_resort_get_all_daily_rewards()

        a.log("- selling excess items")
        a.sell_items(max_item_rank=39, skip_max_lvl=True, only_max_lvl=False,
                     max_innocent_rank=8, max_innocent_type=Innocent_ID.HL)
        a.sell_items(max_rarity=69, max_item_rank=39, skip_max_lvl=True, only_max_lvl=False, max_innocent_rank=8,
                     max_innocent_type=Innocent_ID.RES)

        if a.current_ap >= 1000:
            use_ap(stage_id=farm_stage_id, event_team=event_team)


# clear_inbox()

# a.do_axel_contest_multiple_characters(2)
# farm_event_stage(stage_id=114710104, times=10, team=6)
# do_quest(108410101)

# Daily tasks
daily(bts=False, gem_team=22, hl_team=21)

# a.autoRebirth(True)
# a.setTeamNum(9)

# # Uncomment to clear a new event area. Provide the first 4 digits of the m_area_id.
# clear_event(get_event_areas(1154))

# 314109 - misc stage
# 1154105310 - Extra+ (HL)
# 1154105311 - Extra+ (EXP)
# 1154105312 - Extra+ (1★)
# 114710104 - Defensive Battle 4

# farm_event_stage(1, 1154105312, team=9)
# a.etna_donate_innocents(max_innocent_rank=4, max_innocent_type=Innocent_ID.RES)
# items, skip = a.pd.filter_items(only_max_lvl=True, skip_equipped=True)
# for item in items:
#     a.remove_innocents(item)


# Full loop
loop(team=9, raid_team=23, iw_team=22, event_team=9, rebirth=True, farm_stage_id=1154105312)
