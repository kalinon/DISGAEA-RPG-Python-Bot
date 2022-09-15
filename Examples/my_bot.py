from bot import Bot
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

# bot.clear_inbox()
# exit(0)

# bot.complete_story(team_num=9, raid_team=23)

# # Uncomment to clear a new event area. Provide the first 4 digits of the m_area_id.
# bot.clear_event(bot.get_event_areas(1178), team_num=9, raid_team=23)

# 1178105311 - Extra+ (HL)
# 1178105312 - Extra+ (EXP)
# 1178105313 - Extra+ (1★)
# 1178201103 - Hidden Stage -HARD-
# bot.do_quest(1178105312, team_num=9, auto_rebirth=True)

# Daily tasks
bot.daily(gem_team=22, hl_team=21, exp_team=None)

# Full loop
bot.loop(
    team=9, rebirth=True, farm_stage_id=1178105312,
    raid_team=23, iw_team=9, event_team=9,
    gem_team=22, hl_team=21, exp_team=None,
    ap_limit=5000,
)
