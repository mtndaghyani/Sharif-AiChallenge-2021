from random import randint

from Model import *
from classes.utilities.local_map import LocalMap
from classes.utilities.none_cell import NoneCell


class Agent:
    def __init__(self):
        print("Agent created!")
        self.game = None
        self.local_map = None
        self.path_to_follow = []
        self._targets = {"RESOURCE": lambda cell: cell.resource_value > 0,
                         "HOME": lambda cell: cell.x == self.game.baseX and cell.y == self.game.baseY,
                         "NEAREST_INVISIBLE": lambda cell: cell.type == -1}

    def initialize(self, game):
        self.game = game
        self.local_map = LocalMap(self.game)

    def get_answer(self):
        self.local_map.update_map()
        pass

    @staticmethod
    def get_random_direction():
        return [Direction.DOWN, Direction.UP, Direction.RIGHT, Direction.LEFT][randint(0, 3)]

