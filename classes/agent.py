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
                         "NEAREST_INVISIBLE": lambda cell: cell.type == -1 and not LocalMap.in_cold_list(cell),
                         "OPPONENT": lambda cell: self.contains_opponent(cell)}

    def initialize(self, game):
        self.game = game
        self.update_local_map()

    def update_local_map(self):
        self.local_map = LocalMap(self.game)

    def get_answer(self):
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
            elif direction.value == 4:
                reversed_path.append(Direction.UP)
            else:
                reversed_path.append(Direction.CENTER)
        self.path_to_home = reversed_path

    @staticmethod
    def contains_opponent(cell):
        for ant in cell.ants:
            if ant.antTeam == AntTeam.ENEMY.value:
                return True
        return False

    def get_message(self):

        for j in range(-self.game.viewDistance, self.game.viewDistance + 1):
            for i in range(-self.game.viewDistance, self.game.viewDistance + 1):
                cell = self.game.ant.getMapRelativeCell(i, j)
                if cell is not None:
                    if cell.type == 0 and cell.x != self.game.baseX and cell.y != self.game.baseY:
                        return f'b/{cell.x}/{cell.y}'

        return f'n/{self.game.ant.currentX}/{self.game.ant.currentY}'

