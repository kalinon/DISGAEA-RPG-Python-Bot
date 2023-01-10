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

## Run stages with daily 500% bonus
from data import data as gamedata
dic = gamedata['stages']
rank = [1,2,3]
for k in rank:
    for area_id in Constants.Current_Story_Event_Area_IDs:
        bonus_stage = [x for x in dic if x["m_area_id"]==area_id and x["rank"]==k and x["no"] == 5]
        a.doQuest(m_stage_id=bonus_stage[0]['id'], team_num=event_team)
        a.raid_share_own_boss(party_to_use=raid_team)

# Buy 5 AP pots daily
a.event_buy_daily_AP(289001)

# Claim daily missions
a.event_claim_daily_missions()

# Claim event missions
a.event_claim_story_missions()

# Claim character missions
a.event_claim_character_missions()