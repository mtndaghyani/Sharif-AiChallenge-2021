from queue import Queue
from random import shuffle
from Model import Direction, CellType, AntType
from random import randint
from classes.utilities.none_cell import NoneCell


class LocalMap:
    black_list = []
    map = []
    invalid_cell_types = []

    def __init__(self, game):
        self.game = game
        self.directions = {(1, 0): Direction.DOWN,
                           (-1, 0): Direction.UP,
                           (0, 1): Direction.RIGHT,
                           (0, -1): Direction.LEFT,
                           }

        self.x = self.game.ant.currentX
        self.y = self.game.ant.currentY
        self.view_distance = self.game.viewDistance
        self.update_map()

    def update_map(self):
        if len(LocalMap.map) == 0:
            LocalMap.map = [[NoneCell() for i in range(self.game.mapWidth)] for j in range(self.game.mapHeight)]
            if self.game.ant.antType == AntType.SARBAAZ:
                LocalMap.invalid_cell_types = [CellType.WALL.value,
                                               CellType.SWAMP.value]
            else:
                LocalMap.invalid_cell_types = [CellType.WALL.value,
                                               CellType.SWAMP.value,
                                               CellType.TRAP.value]
        LocalMap.map[self.y][self.x] = self.game.ant.getLocationCell()
        for j in range(-self.view_distance, self.view_distance + 1):
            for i in range(-self.view_distance, self.view_distance + 1):
                cell = self.game.ant.getMapRelativeCell(i, j)
                if cell is not None:
                    LocalMap.map[cell.y][cell.x] = cell
        LocalMap._update_cells()

    @classmethod
    def _update_cells(cls):
        for y in range(len(cls.map)):
            for x in range(len(cls.map[0])):
                if cls.map[y][x].type == -1:
                    cls.map[y][x].set_coord(x, y)

    def get_neighbors(self, cell):
        neighbors = []

        for direction in self.directions.keys():
            x, y = self._correct_coord(cell.x + direction[1], cell.y + direction[0])
            neighbor = LocalMap.map[y][x]
            if neighbor.type not in LocalMap.invalid_cell_types:
                neighbors.append(neighbor)
        return neighbors

    def _correct_coord(self, x, y):

        cell_x = x
        cell_y = y
        if cell_x < 0:
            cell_x += self.game.mapWidth
        elif cell_x >= self.game.mapWidth:
            cell_x -= self.game.mapWidth
        if cell_y < 0:
            cell_y += self.game.mapHeight
        elif cell_y >= self.game.mapHeight:
            cell_y -= self.game.mapHeight
        return cell_x, cell_y

    def get_path_to(self, func, non_cell=False,
                    shuffle_neighbors=True,
                    check_black_list=False,
                    max_depth=1000):
        """Returns the path if found or None if not found"""
        queue = Queue()
        father = {}
        marked = {}

        current_cell = self.game.ant.getLocationCell()
        queue.put(current_cell)
        marked[current_cell] = True
        father[current_cell] = None

        return self._find_path(father, func, marked, queue,
                               non_cell=non_cell,
                               shuffle_neighbors=shuffle_neighbors,
                               check_black_list=check_black_list,
                               max_depth=max_depth)

    def _find_path(self, father, func, marked, queue, **kwargs):
        non_cell = kwargs.get("non_cell")
        check_black_list = kwargs.get("check_black_list")
        max_depth = int(kwargs.get("max_depth"))
        depth = 0
        while queue.qsize() != 0 and depth <= max_depth:
            cell = queue.get()
            if func(cell) and cell != self.game.ant.getLocationCell():
                path = []
                while father[cell] is not None:
                    path.append(self.get_direction(father[cell], cell))
                    cell = father[cell]
                return path[::-1]
            else:
                neighbors = self.get_neighbors(cell)
                if kwargs.get("shuffle_neighbors"):
                    shuffle(neighbors)
                for neighbor in neighbors:
                    if neighbor.type == -1 and not non_cell:  # Check non_cell neighbor only if non_cell arg is True
                        continue
                    # Check whether neighbor is in black_list only if check_black_list is True
                    if check_black_list and LocalMap.in_blacklist(neighbor):
                        continue
                    elif not marked.get(neighbor, False):
                        marked[neighbor] = True
                        queue.put(neighbor)
                        father[neighbor] = cell
            depth += 1
        return None

    def get_direction(self, start_cell, end_cell):
        dx = end_cell.x - start_cell.x
        dy = end_cell.y - start_cell.y
        if dx < -1:
            dx += self.game.mapWidth
        elif dx > 1:
            dx -= self.game.mapWidth
        if dy < -1:
            dy += self.game.mapHeight
        elif dy > 1:
            dy -= self.game.mapHeight
        return self.directions.get((dy, dx))

    def get_cell_from_direction(self, direction):
        if direction.value == Direction.CENTER.value:
            return self.game.ant.getLocationCell()
        for coord in self.directions:
            if self.directions[coord].value == direction.value:
                return self.game.ant.getMapRelativeCell(coord[1], coord[0])

    @classmethod
    def add_to_black_list(cls, cell):
        LocalMap.black_list.append((cell.x, cell.y))

    @classmethod
    def in_blacklist(cls, cell):
        return (cell.x, cell.y) in LocalMap.black_list
