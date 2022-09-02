# DISGAEA RPG Bot written in Python

requirements:

- `pip install requests`
- `pip install python-dateutil`
- `pip install jwt`
- license key (get it from https://disgaea.codedbots.com, once you have the license key put it into `codedbots.py` on
  line 12)

![bot running](https://raw.github.com/Mila432/DISGAEA-RPG-Python-Bot/master/1.png)

features:

- use serial codes
- finish all quests
- farm single quests
- farm full EPs
- every quest is finished with 3\*
- buy rare items from shop
- use free summons
- overlords tower supported
- farm item world for both weapons & armor
- catching innocents while farming item world
- multi region support gl & jp (need jp proxy)
- proxy support
- leech raid bosses
- run Axel contest
- automate fish fleet and item survey

## Auto login

1. go to <https://p-public.service.boltrend.com/oauthOs?appid=287&lang=en>
2. open developer tools -> network (ensure persist logs is on)
3. login via webpage
4. inspect the first requests payload, it should look something like:

    ```json
    {
      "appId": "287",
      "account": "<string>",
      "password": "<string>",
      "channel": 3,
      "captchaId": "",
      "validate": "",
      "sourceId": "",
      "sign": "<string>"
    }
    ```
5. Using the variables above set the following environmental variables:
    ```shell
    export STEAM_LOGIN='true'
    export DRPG_EMAIL="<account value>"
    export DRPG_PASS="<password value>"
    export DRPG_SIGN="<sign value>"
    ```
6. be sure to set your device to 3
    ```python
    a = API()
    a.o.wait = 0
    a.o.set_region(2)
    a.o.set_device(3)
    a.quick_login()
    ```

### Set envs using python

If you dont know how to set envs or are on window or w/e use this at the start of your bot script:

```python
import os

os.environ["STEAM_LOGIN"] = 'true'
os.environ["DRPG_EMAIL"] = "<account value>"
os.environ["DRPG_PASS"] = "<password value>"
os.environ["DRPG_SIGN"] = "<sign value>"

from main import API

a = API()
a.o.wait = 0
a.o.set_region(2)
a.o.set_device(3)
a.quick_login()
```