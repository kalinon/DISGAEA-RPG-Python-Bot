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

a.o.use_potions = True
event_team = 8
raid_farming_team = 7

##Run entire event
from data import data as gamedata
dic = gamedata['stages']
area_lt =  [1189101, 1189102, 1189103, 1189104, 1189105]
rank = [1,2,3]

for k in rank:
    for i in area_lt:
        new_lt = [x for x in dic if x["m_area_id"]==i and x["rank"]==k]
        for i in new_lt:
            a.doQuest(m_stage_id=i['id'], team_num=event_team)
            a.raid_share_own_boss(party_to_use=raid_farming_team)