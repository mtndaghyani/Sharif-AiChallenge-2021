from classes.agent import Agent, Direction
from classes.utilities.target import Target


class SarbazAgent(Agent):
    def get_answer(self) -> Direction:
        if len(self.path_to_follow) > 0:
            return self.path_to_follow.pop(0)

        path = self.local_map.get_path_to(self._targets.get(Target.NEAREST_INVISIBLE))
        if path is not None:
            self.path_to_follow = path
            print("New invisible found!")
            return self.get_answer()
        print("PATH NOT FOUND!")
        return SarbazAgent.get_random_direction()
