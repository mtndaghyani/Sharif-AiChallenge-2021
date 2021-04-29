from classes.agent import Agent, Direction
from classes.utilities.local_map import LocalMap
from classes.utilities.target import Target


class KargarAgent(Agent):
    def get_answer(self) -> Direction:
        self.update_local_map()
        if self.game.ant.currentX == self.game.baseX and self.game.ant.currentY == self.game.baseY:
            self.path_from_home = []

        if len(self.path_to_follow) > 0:
            answer = self.path_to_follow.pop(0)
            cell = self.local_map.get_cell_from_direction(answer)
            if cell.type not in LocalMap.invalid_cell_types:
                self.path_from_home.append(answer)
                return answer
            answer = Direction.CENTER
            self.path_from_home.append(answer)
            return answer

        if self.game.ant.currentResource.value > 0:
            print("Go home!")
            self.set_home_path()
            self.path_to_follow = self.path_to_home
            return self.get_answer()
        else:
            path = self.local_map.get_path_to(self._targets.get(Target.RESOURCE))
            if path is not None:
                self.path_to_follow = path
                print("Resource found!")
                return self.get_answer()
            path = self.local_map.get_path_to(self._targets.get(Target.NEAREST_INVISIBLE), non_cell=True)
            if path is not None:
                self.path_to_follow = path
                print("New invisible found!")
                return self.get_answer()
            print("PATH NOT FOUND!")
            return KargarAgent.get_random_direction()
