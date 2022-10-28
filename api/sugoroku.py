from abc import ABCMeta

from api.base import Base

from api.constants import Mission_Status, Constants


class Sugoroku(Base, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    
