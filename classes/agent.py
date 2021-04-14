from random import randint

from Model import *
from classes.utilities.local_map import LocalMap


class Agent:
    def __init__(self):
        print("Agent created!")
        self.game = None
        self.local_map = None
        self.path_to_follow = []
        self.path_from_home = []
        self.path_to_home = []
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

    def set_home_path(self):
        """Reverse path_from_home and calculate appropriate directions to make path_to_home"""
        temp = self.path_from_home[::-1]
        reversed_path = []
        for direction in temp:
            if direction.value == 1:
                reversed_path.append(Direction.LEFT)
            elif direction.value == 2:
                reversed_path.append(Direction.DOWN)
            elif direction.value == 3:
                reversed_path.append(Direction.RIGHT)
            else:
                reversed_path.append(Direction.UP)
        self.path_to_home = reversed_path
