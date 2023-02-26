import os
from main import API

os.environ["STEAM_LOGIN"] = 'true'
os.environ["DRPG_EMAIL"] = ""
os.environ["DRPG_PASS"] = ""
os.environ["DRPG_SIGN"] = ""

a = API()
a.o.wait = 0
a.o.set_region(2)
a.o.set_device(3)
a.quick_login()
