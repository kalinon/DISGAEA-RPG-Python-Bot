import datetime
from abc import ABCMeta

from dateutil import parser

from api import Shop
from api.constants import Constants, Mission_Status


class Event(Shop, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def event_claim_daily_missions(self):
        r = self.client.story_event_daily_missions()
        mission_ids = []
        incomplete_mission_ids = []
        
        for mission in r['result']['missions']:
            if mission['status'] == Mission_Status.Cleared:
                mission_ids.append(mission['id'])
            if mission['status'] == Mission_Status.Not_Completed:
                incomplete_mission_ids.append(mission['id'])
        if len(mission_ids) > 0:
            self.client.story_event_claim_daily_missions(mission_ids)
            self.log(f"Claimed {len(mission_ids)} daily missions")
        if len(incomplete_mission_ids) > 0:
            self.log(f"Daily missions to be completed: {len(incomplete_mission_ids)}")

    def event_claim_missions(self):
        r = self.client.story_event_missions()
        mission_ids = []
        incomplete_mission_ids = []
        
        for mission in r['result']['missions']:
            if mission['status'] == Mission_Status.Cleared:
                mission_ids.append(mission['id'])
            if mission['status'] == Mission_Status.Not_Completed:
                incomplete_mission_ids.append(mission['id'])
        if len(mission_ids) > 0:
            self.client.story_event_claim_missions(mission_ids)
            self.log(f"Claimed {len(mission_ids)} missions")
        if len(incomplete_mission_ids) > 0:
            self.log(f"Missions to be completed: {len(incomplete_mission_ids)}")

    ## TODO: is that ID static??
    def event_buy_daily_AP(self):
        product_data = self.client.shop_index()['result']['shop_buy_products']['_items']
        ap_pot = next((x for x in product_data if x['m_product_id'] == 278001),None)
        if ap_pot is not None and ap_pot['buy_num'] == 0:
            self.client.shop_buy_item(itemid=278001, quantity=5)
