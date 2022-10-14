from abc import ABCMeta

from api.base import Base

from api.constants import Mission_Status, Constants


class Event(Base, metaclass=ABCMeta):
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

    def event_claim_story_missions(self):
        r = self.client.story_event_missions()
        mission_ids = []
        incomplete_mission_ids = []

        # character missions and story missions have to be claimed separately
        character_mission_id = (Constants.Current_Story_Event_ID * 1000) + 500
        
        for mission in r['result']['missions']:
            if mission['status'] == Mission_Status.Cleared and mission['id'] < character_mission_id:
                mission_ids.append(mission['id'])
            if mission['status'] == Mission_Status.Not_Completed and mission['id'] < character_mission_id:
                incomplete_mission_ids.append(mission['id'])
        if len(mission_ids) > 0:
            self.client.story_event_claim_missions(mission_ids)
            self.log(f"Claimed {len(mission_ids)} story missions")
        if len(incomplete_mission_ids) > 0:
            self.log(f"Story missions to be completed: {len(incomplete_mission_ids)}")

    def event_claim_character_missions(self):
        r = self.client.story_event_missions()
        mission_ids = []
        incomplete_mission_ids = []

        # character missions and story missions have to be claimed separately
        character_mission_id = (Constants.Current_Story_Event_ID * 1000) + 500
        
        for mission in r['result']['missions']:
            if mission['status'] == Mission_Status.Cleared and mission['id'] >= character_mission_id:
                mission_ids.append(mission['id'])
            if mission['status'] == Mission_Status.Not_Completed and mission['id'] >= character_mission_id:
                incomplete_mission_ids.append(mission['id'])
        if len(mission_ids) > 0:
            self.client.story_event_claim_missions(mission_ids)
            self.log(f"Claimed {len(mission_ids)} character missions")
        if len(incomplete_mission_ids) > 0:
            self.log(f"Character missions to be completed: {len(incomplete_mission_ids)}")

    ## TODO: is that ID static??
    def event_buy_daily_AP(self, ap_id:int):
        product_data = self.client.shop_index()['result']['shop_buy_products']['_items']
        ap_pot = next((x for x in product_data if x['m_product_id'] == ap_id),None)
        if ap_pot is not None and ap_pot['buy_num'] == 0:
            self.client.shop_buy_item(itemid=ap_id, quantity=5)
