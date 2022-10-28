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
a.event_buy_daily_AP()

# Claim daily missions
a.event_claim_daily_missions()

# Claim event missions
a.event_claim_story_missions()

# Claim character missions
a.event_claim_character_missions()