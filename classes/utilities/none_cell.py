from Model import Cell


class NoneCell:

    type = -1
    resource_value = -1
    resource_type = -1

    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def set_coord(self, x, y):
        self.x = x
        self.y = y