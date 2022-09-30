import datetime
from api.constants import Mission_Status

from dateutil import parser

from api.constants import Constants
from main import API

a = API()
a.config(
    sess=Constants.session_id,
    uin=Constants.user_id,
    wait=0,
    region=2,
    device=2
)
a.quick_login()

## Specify event team to be used here
event_team = 5
raid_team = 6

## Specify stages with daily 500% bonus
from data import data as gamedata
dic = gamedata['stages']
daily_bonus_stage_IDS = [1178101209, 1178102209, 1178103209, 1178104210, 1178105209, 1178101309, 1178102309, 1178103309, 1178104310, 1178105309]

for stageID in daily_bonus_stage_IDS:
    a.doQuest(m_stage_id=stageID, team_num=event_team)
    a.raid_share_own_boss(party_to_use=raid_team)

# Buy 5 AP pots daily
product_data = a.client.shop_index()['result']['shop_buy_products']['_items']
ap_pot = next((x for x in product_data if x['m_product_id'] == 278001),None)
if ap_pot is not None and ap_pot['buy_num'] == 0:
    a.client.shop_buy_item(itemid=278001, quantity=5)

# Claim daily missions
r = a.client.story_event_daily_missions()
mission_ids = []
for mission in r['result']['missions']:
    if mission['status'] == Mission_Status.Cleared:
        mission_ids.append(mission['id'])
if len(mission_ids) > 0:
    a.client.story_event_claim_daily_missions(mission_ids)
