import numpy as np
from random import random


class CellGrid:
    DEFAULT_LIVE_PROBABILITY = 25  # 25%

    def __init__(self, x, y, all_live=False):
        self.x = x
        self.y = y
        self.grid = CellGrid.init_cell_grid(x, y, all_live)

    @staticmethod
    def init_cell_grid(x, y, all_live):
        if not all_live:
            return np.zeros((x,y))
        else:
            return np.ones((x,y))

    def get_live_neighbors(self):
        pad_top             = np.pad(self.grid, ((2,0), (1,1)))
        pad_top_right       = np.pad(self.grid, ((2,0), (0,2)))
        pad_right           = np.pad(self.grid, ((1,1), (0,2)))
        pad_bottom_right    = np.pad(self.grid, ((0,2), (0,2)))
        pad_bottom          = np.pad(self.grid, ((0,2), (1,1)))
        pad_bottom_left     = np.pad(self.grid, ((0,2), (2,0)))
        pad_left            = np.pad(self.grid, ((1,1), (2,0)))
        pad_top_left        = np.pad(self.grid, ((2,0), (2,0)))

        return (pad_top + pad_top_right + pad_right + \
                pad_bottom_right + pad_bottom + pad_bottom_left + \
                pad_left + pad_top_left)[1:-1, 1:-1]  # Unpad result

    def update(self):
        live_neighbors = self.get_live_neighbors()
        for x in range(self.x):
            for y in range(self.y):
                ln = live_neighbors[x][y]
                cell = self.grid[x][y]
                if cell == 1 and 2 <= ln < 4:
                    pass  # Keep cell alive
                elif cell == 0 and ln == 3:
                    self.grid[x][y] = 1
                else:
                    self.grid[x][y] = 0

    def reset(self):
        for x in range(self.x):
            for y in range(self.y):
                self.grid[x][y] = 0

    def randomize(self):
        self.reset()
        for x in range(self.x):
            for y in range(self.y):
                r = int(random()*100)
                if r <= CellGrid.DEFAULT_LIVE_PROBABILITY:
                    self.grid[x][y] = 1