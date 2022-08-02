import datetime
from dateutil import parser
from api.player import Player


class Gatcha(Player):
    def __init__(self):
        super().__init__()

    def get_free_gacha(self):
        res = self.client.gacha_available()
        if len(res['result']['private_gachas']) > 0:
            self.client.gacha_do(is_gacha_free=True, price=0, item_type=2, num=1, m_gacha_id=100001, item_id=0)

    def is_free_gacha_available(self):
        player_data = self.player_index()
        last_free_gacha_at_string = player_data['result']['status']['last_free_gacha_at']
        last_free_gacha_at_string_date = parser.parse(last_free_gacha_at_string)
        serverTime = datetime.datetime.utcnow() + datetime.timedelta(hours=-4)
        return serverTime.date() > last_free_gacha_at_string_date.date()
