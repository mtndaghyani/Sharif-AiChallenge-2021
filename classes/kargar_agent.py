from classes.agent import Agent, Direction, CellType
from classes.utilities.target import Target


class KargarAgent(Agent):
    def get_answer(self) -> Direction:
        self.update_local_map()
        if self.game.ant.currentX == self.game.baseX and self.game.ant.currentY == self.game.baseY:
            self.path_from_home = []

        if len(self.path_to_follow) > 0:
            return self.handle_next_move()

        if self.game.ant.currentResource.value > 0:
            self.handle_home_path()
            return self.get_answer()
        else:
            path = self.local_map.get_path_to(self._targets.get(Target.RESOURCE), is_kargar=True)
            if path is not None:
                self.path_to_follow = path
                print("Resource found!")
                print(path)
                return self.get_answer()
            path = self.local_map.get_path_to(self._targets.get(Target.NEAREST_INVISIBLE),
                                              non_cell=True,
                                              is_kargar=True)
            if path is not None:
                self.path_to_follow = path
                print("New invisible found!")
                return self.get_answer()
            print("PATH NOT FOUND!")
            return KargarAgent.get_random_direction()

    def handle_home_path(self):
        print("Go home!")
        self.set_home_path()
        self.path_to_follow = self.path_to_home

    def handle_next_move(self):
        answer = self.path_to_follow.pop(0)
        cell = self.local_map.get_cell_from_direction(answer)
        if cell.type != CellType.WALL.value:
            self.path_from_home.append(answer)
            return answer
        answer = Direction.CENTER
        self.path_from_home.append(answer)
        return answer
