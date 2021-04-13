from Model import *
from classes.utilities.local_map import LocalMap


class Agent:
    def __init__(self):
        print("Agent created!")
        self.game = None
        self.local_map = None
        self.path_to_follow = []
        self._targets = {"RESOURCE": lambda cell: cell.resource_value > 0,
                         "HOME": lambda cell: cell.x == self.game.baseX and cell.y == self.game.baseY,
                         "NEAREST_INVISIBLE": lambda cell: self.local_map.map[cell.y][cell.x] is None}

    def initialize(self, game):
        self.game = game
        self.local_map = LocalMap(self.game)

    def get_answer(self):
        self.local_map.update_map()
        pass

