from queue import Queue

from Model import Direction


class LocalMap:
    def __init__(self, game):
        self.game = game
        self.directions = {(1, 0): Direction.DOWN,
                           (-1, 0): Direction.UP,
                           (0, 1): Direction.RIGHT,
                           (0, -1): Direction.LEFT,
                           (0, 0): Direction.CENTER}

        self.map = self.build_map()
        self.view_distance = self.game.viewDistance
        self.x = self.game.ant.currentX
        self.y = self.game.ant.currentY

    def build_map(self):
        length = self.game.mapHeight
        cells = [[None for i in range(length)] for j in range(length)]
        cells[self.y][self.x] = self.game.ant.getLocationCell()
        for j in range(-self.view_distance, self.view_distance + 1):
            for i in range(-self.view_distance, self.view_distance + 1):
                cell = self.game.ant.getMapRelativeCell(i, j)
                if cell is not None:
                    cells[cell.y][cell.x] = cell
        return cells

    def get_neighbors(self, cell):
        neighbors = []
        for direction in self.directions.keys():
            x, y = self._correct_coord(cell.x + direction[1], cell.y + direction[0])
            neighbor = self.map[y][x]
            if neighbor is not None:
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
                return reversed(path)
            else:
                neighbors = self.get_neighbors(cell)
                for neighbor in neighbors:
                    if not marked.get(neighbors, default=False):
                        marked[neighbor] = True
                        queue.put(neighbor)
                        father[neighbor] = cell
        return None

    def _get_direction(self, start_cell, end_cell):
        dx, dy = self._correct_coord(end_cell.x - end_cell.x, end_cell.y - start_cell.y)
        return self.directions.get((dy, dx))
