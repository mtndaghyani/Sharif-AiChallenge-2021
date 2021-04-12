class LocalMap:
    def __init__(self, game):
        self.game = game
        self.directions = [(1, 0),
                           (-1, 0),
                           (0, 1),
                           (0, -1)]

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
        for direction in self.directions:
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
