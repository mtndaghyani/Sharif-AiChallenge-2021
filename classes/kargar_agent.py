from classes.agent import Agent, Direction
from classes.utilities.target import Target


class KargarAgent(Agent):
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
            self.path_to_follow = [Direction.CENTER]
            print("PATH NOT FOUND!")
            return self.get_answer()

