from Model import *
from classes.utilities.local_map import LocalMap


class Agent:
    def __init__(self, game):
        self.game = game
        self.local_map = LocalMap(self.game)
        self.path_to_follow = []
        self._targets = {"RESOURCE": lambda cell: cell.resource_value > 0,
                         "HOME": lambda cell: cell.x == self.game.baseX and cell.y == self.game.baseY,
                         "NEAREST_INVISIBLE": lambda cell: self.local_map.map[cell.y][cell.x] is None}

    def get_answer(self) -> Direction:
        if len(self.path_to_follow) > 0:
            return self.path_to_follow.pop(0)
        if self.game.ant.currentResource.value > 0:
            # TODO
            pass
        else:
            path = self.local_map.get_path_to(self._targets.get(Target.RESOURCE))
            if path is not None:
                self.path_to_follow = path
                print("Resource found!")
                return self.get_answer()
            path = self.local_map.get_path_to(self._targets.get(Target.NEAREST_INVISIBLE))
            if path is not None:
                self.path_to_follow = path
                print("New invisible found!")
                return self.get_answer()
            path = [Direction.CENTER]
            print("PATH NOT FOUND!")
            return self.get_answer()


class Target:
    RESOURCE = "RESOURCE"
    HOME = "HOME"
    NEAREST_INVISIBLE = "NEAREST_INVISIBLE"
