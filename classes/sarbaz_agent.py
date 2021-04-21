from classes.agent import Agent, Direction
from classes.utilities.target import Target


class SarbazAgent(Agent):
    TURNS_TO_WAIT = 5

    def __init__(self):
        super().__init__()
        self.visited_cells = {}
        self.attack_mode = False
        self.target_x = 0
        self.target_y = 0
        self.waiting_turns = 0
        self.do_wait = False

    def get_answer(self) -> Direction:
        self.update_local_map()
        if self.attack_mode:
            return self.handle_attack_mode()
        self.visited_cells = {}
        return self.handle_explore_mode()

    def handle_explore_mode(self):
        if self.game.ant.getLocationCell().resource_value > 0 and self.do_wait:
            return self.handle_waiting_mode()
        self.do_wait = True
        if len(self.path_to_follow) > 0:
            return self.path_to_follow.pop(0)
        path = self.local_map.get_path_to(self._targets.get(Target.RESOURCE), shuffle_neighbors=False)
        if path is not None:
            self.path_to_follow = path
            print("Resource found!")
            return self.get_answer()
        path = self.local_map.get_path_to(self._targets.get(Target.NEAREST_INVISIBLE),
                                          non_cell=True,
                                          shuffle_neighbors=False)
        if path is not None:
            self.path_to_follow = path
            print("New invisible found!")
            return self.get_answer()
        print("PATH NOT FOUND!")
        return SarbazAgent.get_random_direction()

    def handle_attack_mode(self):
        x = self.game.ant.currentX
        y = self.game.ant.currentY
        if (abs(x - self.target_x) + abs(y - self.target_y)) <= self.game.ant.viewDistance:
            self.attack_mode = False
            return self.get_answer()
        self.visited_cells[(y, x)] = True
        return self.get_nearest_to_target_neighbor()

    def get_nearest_to_target_neighbor(self):
        current_cell = self.game.ant.getLocationCell()
        neighbors = self.local_map.get_neighbors(current_cell)
        nearest = None
        min_distance = 100000
        for neighbor in neighbors:
            if not self.visited_cells.get((neighbor.y, neighbor.x), False):
                distance = abs(neighbor.x - self.target_x) \
                           + abs(neighbor.y - self.target_y)
                if distance < min_distance:
                    nearest = neighbor
                    min_distance = distance
        return self.local_map.get_direction(current_cell, nearest)

    def handle_waiting_mode(self):
        self.waiting_turns += 1
        path = self.local_map.get_path_to(self._targets.get(Target.OPPONENT))
        if path is not None:
            self.waiting_turns = 0
        if self.waiting_turns <= SarbazAgent.TURNS_TO_WAIT:
            return Direction.CENTER
        self._reset_waiting_mode()
        path = self.local_map.get_path_to(self._targets.get(Target.NEAREST_INVISIBLE),
                                          non_cell=True,
                                          shuffle_neighbors=False)
        if path is not None:
            self.path_to_follow = path
            print("New invisible found!")
            return self.get_answer()

    def _reset_waiting_mode(self):
        self.waiting_turns = 0
        self.do_wait = False
