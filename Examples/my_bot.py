from api.constants import Innocent_ID
from bot import Bot, get_event_areas
from main import API

a = API()
# a.setProxy("127.0.0.1:8080")
a.o.wait = 0
a.o.set_region(2)
a.o.set_device(3)
a.quick_login()

codes = []

bot = Bot(api=a)
bot.use_codes(codes)

# a.dump_player_data("./player_data.json")
# exit(0)

# bot.complete_story(team_num=9, raid_team=23)

# # Uncomment to clear a new event area. Provide the first 4 digits of the m_area_id.
# bot.clear_event(get_event_areas(1228), team_num=26, raid_team=23)

# 1228105311 - Extra+ (HL)
# 1228105312 - Extra+ (EXP)
# 1228105313 - Extra+ (1★)
# 1228201103 - Hidden Stage -HARD-

# bot.do_quest(1228201103, team_num=2, auto_rebirth=True)
# bot.clear_inbox()
# exit(0)
# Daily tasks
bot.do_quest(1230101001, team_num=2, auto_rebirth=True)
bot.do_quest(1228201103, team_num=2, auto_rebirth=True)

bot.daily(gem_team=22, hl_team=21, exp_team=24)

# Full loop
bot.loop(
    team=26, rebirth=True, farm_stage_id=1228105313,
    hl_team=21, gem_team=22, raid_team=23,
    exp_team=24, iw_team=25, event_team=26,
    ap_limit=200, pvp_team=None,
)
