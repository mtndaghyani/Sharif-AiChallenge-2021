from Model import *


class Agent:
    def __init__(self, game):
        self.game = game
        self.path_to_follow = []
        self.directions = [(1, 0),
                           (-1, 0),
                           (0, 1),
                           (0, -1)]

    def find_shortest_path(self, func):
        pass

    def get_neighbors(self):
        neighbors = []
        for direction in self.directions:
            cell = self.game.ant.getMapRelativeCell(direction[0], direction[1])
            if cell.type != CellType.WALL.value:
                neighbors.append(cell)
        return neighbors

    def get_destination(self) -> Direction:
        pass
