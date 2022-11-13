from abc import ABCMeta

from api.base import Base
from api.constants import Constants


class Bingo(Base, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()

    def bingo_is_spin_available(self):
        data = self.client.bingo_index()
        return len(data['result']['t_bingo_data']['bingo_indexes']) < len(
            data['result']['t_bingo_data']['display_numbers']) and not data['result']['t_bingo_data']['drew_today']

    def bingo_claim_free_rewards(self):
        data = self.client.bingo_index()
        free_reward_positions = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
        bingo_rewards = data['result']['rewards']
        free_rewards = [bingo_rewards[i] for i in free_reward_positions]
        available_free_rewards = [x for x in free_rewards if x['status'] == 1]
        if len(available_free_rewards) > 0:
            self.log(f"Claiming {len(available_free_rewards)} free rewards...")
        for reward in available_free_rewards:
            self.client.bingo_receive_reward([reward['id']])
        self.log("Finished claiming free rewards.")

    def bingo_spin_roulette(self):
        if self.bingo_is_spin_available():
            spin_result = self.client.bingo_lottery(Constants.Current_Bingo_ID, False)
            spin_index = spin_result['result']['t_bingo_data']['last_bingo_index']
            self.log(
                f"Spinning Bingo: Obtained number {spin_result['result']['t_bingo_data']['display_numbers'][spin_index]}.")
            free_reward_positions = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
            bingo_rewards = spin_result['result']['rewards']
            free_rewards = [bingo_rewards[i] for i in free_reward_positions]
            available_free_rewards = [x for x in free_rewards if x['status'] == 1]
            if len(available_free_rewards) > 0:
                print(f"There are {len(available_free_rewards)} free rewards available to claim.")
