import numpy as np


class CellGrid:
    def __init__(self, x, y, all_live=False):
        self.x = x
        self.y = y
        self.grid = self.init_cell_grid(x, y, all_live)

    
    def init_cell_grid(self, x, y, all_live):
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
        