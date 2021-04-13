from queue import Queue
from random import shuffle
from Model import Direction


class LocalMap:
    def __init__(self, game):
        self.game = game
        self.directions = {(1, 0): Direction.DOWN,
                           (-1, 0): Direction.UP,
                           (0, 1): Direction.RIGHT,
                           (0, -1): Direction.LEFT,
                           (0, 0): Direction.CENTER}

        self.x = self.game.ant.currentX
        self.y = self.game.ant.currentY
        self.view_distance = self.game.viewDistance
        self.map = []
        self.update_map()

    def update_map(self):
        length = self.game.mapHeight
        cells = [[None for i in range(length)] for j in range(length)]
        cells[self.y][self.x] = self.game.ant.getLocationCell()
        for j in range(-self.view_distance, self.view_distance + 1):
            for i in range(-self.view_distance, self.view_distance + 1):
                cell = self.game.ant.getMapRelativeCell(i, j)
                if cell is not None:
                    cells[cell.y][cell.x] = cell
        self.map = cells

    def get_neighbors(self, cell):
        neighbors = []
        for direction in self.directions.keys():
            if self.directions != (0, 0):
                x, y = self._correct_coord(cell.x + direction[1], cell.y + direction[0])
                neighbor = self.map[y][x]
                if neighbor.type != 2:
                    neighbors.append(neighbor)
        shuffle(neighbors)
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

    def get_path_to(self, func):
        """Returns the path if found or None if not found"""
        queue = Queue()
        father = {}
        marked = {}

        current_cell = self.game.ant.getLocationCell()
        queue.put(current_cell)
        marked[current_cell] = True
        father[current_cell] = None

        return self._find_path(father, func, marked, queue)

    def _find_path(self, father, func, marked, queue):
        while queue.qsize() != 0:
            cell = queue.get()
            if func(cell):
                path = []
                while father[cell] is not None:
                    path.append(self._get_direction(father[cell], cell))
                    cell = father[cell]
                return path[::-1]
            else:
                neighbors = self.get_neighbors(cell)
                for neighbor in neighbors:
                    if not marked.get(neighbor, False):
                        marked[neighbor] = True
                        queue.put(neighbor)
                        father[neighbor] = cell
        return None

    def _get_direction(self, start_cell, end_cell):
        dx, dy = self._correct_coord(end_cell.x - end_cell.x, end_cell.y - start_cell.y)
        return self.directions.get((dy, dx))
