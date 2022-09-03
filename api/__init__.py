from abc import ABC

from api.axel_contest import AxelContest
from api.battle import Battle
from api.bingo import Bingo
from api.etna_resort import EtnaResort
from api.fish_fleet import FishFleet
from api.gatcha import Gatcha
from api.item_survey import ItemSurvey
from api.raid import Raid
from api.spar_space import SparSpace


class BaseAPI(Bingo, Raid, AxelContest, SparSpace, FishFleet, Gatcha, Battle, EtnaResort, ItemSurvey, ABC):
    def __init__(self):
        super().__init__()
