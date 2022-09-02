from api.constants import EquipmentType, Innocent_ID, Fish_Fleet_Survey_Duration
from main import API

a = API()
# a.setProxy("127.0.0.1:8080")
a.o.wait = 0
a.o.set_region(2)
a.o.set_device(3)
a.quick_login()

codes = []

for code in codes:
    a.client.boltrend_exchange_code(code)


def farm_event_stage(times: int, stage_id: int, team: int, rebirth: bool, raid_team=None):
    for i in range(times):
        do_quest(stage_id, True, team_num=team, auto_rebirth=rebirth, raid_team=raid_team)


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
        refine_items(min_rarity=89, min_item_rank=40, limit=5)
        items = a.items_to_upgrade()

    if len(items) == 0:
        a.log_err('No items to farm! Where they all at?')
        exit(1)

    a.log('found %s items to upgrade' % len(items))

    # This runs item-world to level all your items.
    a.upgrade_items(only_weapons=only_weapons, ensure_drops=True, item_limit=item_limit, items=items)


def do_gate(gate, team, rebirth, raid_team=None):
    a.log("[*] running gate {}".format(gate['m_stage_id']))
    current = int(gate['challenge_num'])
    _max = int(gate['challenge_max'])
    while current < _max:
        do_quest(gate['m_stage_id'], True, team_num=team, auto_rebirth=rebirth, raid_team=raid_team)
        current += 1


def do_gates(gates_data, gem_team=7, hl_team=8, exp_team=None, raid_team=None):
    team = None
    rebirth = None
    a.log("- checking gates")
    for data in gates_data:
        a.log("- checking gate {}".format(data['m_area_id']))
        if data['m_area_id'] == 50102:
            team = hl_team
            rebirth = False
        elif data['m_area_id'] == 50107 or data['m_area_id'] == 50108:
            team = gem_team
            rebirth = False
        elif exp_team is not None:
            team = exp_team
            rebirth = True

        for gate in data['gate_stage_data']:
            if a.current_ap < 10:
                a.log('Too low on ap to do gates')
                return
            if team and rebirth:
                do_gate(gate, team, rebirth, raid_team=raid_team)


def daily(gem_team: int = 22, hl_team: int = 21, exp_team=None):
    a.get_mail_and_rewards()
    send_sardines()

    # Buy items from HL shop
    a.buy_daily_items_from_shop()

    # Do gates
    gates_data = a.client.player_gates()['result']
    do_gates(gates_data, gem_team=gem_team, hl_team=hl_team, exp_team=exp_team)


# Will return an array of event area ids based on the event id.
# clear_event([1132101, 1132102, 1132103, 1132104, 1132105])
def get_event_areas(event_id):
    tmp = event_id * 1000
    return [tmp + 101, tmp + 102, tmp + 103, tmp + 104, tmp + 105]


def clear_event(area_lt, team_num, raid_team: int):
    a.o.use_potions = True
    dic = a.gd.stages
    rank = [1, 2, 3]
    for k in rank:
        for i in area_lt:
            new_lt = [x for x in dic if x["m_area_id"] == i and x["rank"] == k]
            for c in new_lt:
                do_quest(c['id'], True, team_num, True, raid_team=raid_team)
    a.o.use_potions = False


def use_ap(stage_id, event_team: int = 1, raid_team=None):
    a.log("[*] using ap")

    if stage_id is None:
        for i in range(1, 5):
            for unit_id in a.pd.deck(i):
                a.do_axel_contest(unit_id, 1000)
    else:
        times = int(a.current_ap / 30)
        farm_event_stage(stage_id=stage_id, team=event_team, times=times, rebirth=True, raid_team=raid_team)


def clear_inbox():
    a.log("[*] clearing inbox")
    clean_inv()
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
        else:
            a.sell_items(max_rarity=39, max_item_rank=40, skip_max_lvl=True, only_max_lvl=False,
                         max_innocent_rank=4, max_innocent_type=Innocent_ID.RES)

        last_id = new_last_id


def do_quest(stage_id, use_tower_attack: bool = False, team_num=None, auto_rebirth=None, raid_team=None):
    if auto_rebirth is None:
        auto_rebirth = a.o.auto_rebirth

    a.doQuest(stage_id, use_tower_attack=use_tower_attack, team_num=team_num, auto_rebirth=auto_rebirth)
    a.raid_check_and_send()
    if raid_team is not None:
        a.do_raids(raid_team)


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


def train_innocents(innocent_type: int, initial_innocent_rank: int = 8, max_innocent_rank: int = 9):
    innocents_trained = 0
    tickets_finished = False
    all_available_innocents = a.pd.innocent_get_all_of_type(innocent_type, only_unequipped=True)
    for innocent in all_available_innocents:
        if tickets_finished:
            break

        effect_rank = innocent['effect_rank']
        if effect_rank < initial_innocent_rank or effect_rank >= max_innocent_rank:
            continue
        a.log(f"Found innocent to train. Starting value: {innocent['effect_values'][0]}")
        attempts = 0
        innocents_trained += 1
        while effect_rank < max_innocent_rank:
            res = a.client.innocent_training(innocent['id'])
            if ('api_error' in res and 'message' in res['api_error'] and
                    res['api_error']['message'] == 'Not enough item.'):
                a.log("No caretaker tickets left")
                tickets_finished = True
                break
            effect_rank = res['result']['after_t_data']['innocents'][0]['effect_rank']
            a.log(
                f"\tTrained innocent with result {a.innocent_get_training_result(res['result']['training_result'])} "
                f"- Current value: {res['result']['after_t_data']['innocents'][0]['effect_values'][0]}")
            attempts += 1
        a.log(f"\tUpgraded innocent to Legendary. Finished training. Total attempts: {attempts}")
    a.log(f"No innocents left to train. Total innocents trained: {innocents_trained}")


def send_sardines():
    # Send sardines
    player_data = a.client.player_index()
    if player_data['result']['act_give_count']['act_send_count'] == 0:
        a.client.friend_send_sardines()


def complete_story(team_num=9, raid_team=None):
    a.o.team_num = team_num
    a.o.auto_rebirth = True
    a.o.use_potions = True
    # for i in range(141, 175):
    a.completeStory(raid_team=raid_team)
    a.o.use_potions = False


def raid_claim():
    a.raid_claim_all_point_rewards()
    a.raid_claim_all_boss_rewards()
    # a.raid_exchange_surplus_points()
    a.raid_spin_innocent_roulette()


def loop(team=9, rebirth: bool = False, farm_stage_id=None,
         only_weapons=False, iw_team: int = None, raid_team: int = None, event_team: int = None,
         gem_team: int = None, hl_team: int = None, exp_team: int = None,
         ap_limit: int = 6000,
         ):
    # Set defaults
    a.o.auto_rebirth = rebirth
    a.o.team_num = team

    if iw_team is None:
        iw_team = team
    if raid_team is None:
        raid_team = team
    if event_team is None:
        event_team = team
    if gem_team is None:
        gem_team = team
    if hl_team is None:
        hl_team = team
    if exp_team is None:
        exp_team = team

    if a.current_ap >= ap_limit:
        use_ap(stage_id=farm_stage_id, raid_team=raid_team)

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
        raid_claim()

        a.log("- train innocents")
        # Train innocents
        for i in a.gd.innocent_types:
            train_innocents(i["ID"])
        # Train all EXP innocents to max level
        train_innocents(Innocent_ID.EXP, initial_innocent_rank=0, max_innocent_rank=10)
        # Train all SPD innocents to max level
        train_innocents(Innocent_ID.SPD, initial_innocent_rank=0, max_innocent_rank=10)

        clean_inv()

        if a.current_ap >= ap_limit:
            a.log("- doing gates")
            gates_data = a.client.player_gates()['result']
            do_gates(gates_data, gem_team=gem_team, hl_team=hl_team, exp_team=exp_team, raid_team=raid_team)
            use_ap(stage_id=farm_stage_id, event_team=event_team)

        a.log("- farming item world")
        farm_item_world(
            team=iw_team, min_rarity=0, min_rank=40,
            min_item_rank=40, min_item_level=0,
            only_weapons=only_weapons, item_limit=2
        )

        # clear_inbox()


def clean_inv():
    a.log("- donate equipment")
    a.etna_donate_innocents(max_innocent_rank=4, max_innocent_type=Innocent_ID.RES)
    a.etna_resort_donate_items(max_item_rarity=69, remove_innocents=True)
    a.etna_donate_innocents(max_innocent_rank=4, max_innocent_type=Innocent_ID.HL)
    a.etna_resort_get_all_daily_rewards()
    a.log("- selling excess items")
    a.sell_items(max_item_rank=39, skip_max_lvl=True, only_max_lvl=False, remove_innocents=True)
    # a.sell_items(max_item_rank=40, max_rarity=80, max_innocent_rank=7, max_innocent_type=Innocent_ID.RES)
    a.sell_r40_commons_with_no_innocents()


# clear_inbox()
# complete_story(team_num=9, raid_team=23)

# # Uncomment to clear a new event area. Provide the first 4 digits of the m_area_id.
# clear_event(get_event_areas(1162), team_num=9, raid_team=23)

# 1162105311 - Extra+ (HL)
# 1162105312 - Extra+ (EXP)
# 1162105313 - Extra+ (1★)
# 1162201103 - Hidden Stage -HARD-
# do_quest(1162105312, team_num=9, auto_rebirth=True)

# Daily tasks
daily(gem_team=22, hl_team=21, exp_team=None)

# Full loop
loop(
    team=9, rebirth=True, farm_stage_id=1162105313,
    raid_team=23, iw_team=9, event_team=9,
    gem_team=22, hl_team=21, exp_team=None,
    ap_limit=1000,
)
