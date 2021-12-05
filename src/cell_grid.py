from collections import namedtuple
from functools import lru_cache
from random import random
import numpy as np

_Node = namedtuple('Node', ['k', 'a', 'b', 'c', 'd', 'n', 'hash'])

class Node(_Node):
    def __hash__(self):
        return self.hash

    def __repr__(self):
        return f"Node k={self.k}, {1<<self.k} x {1<<self.k}, pop {self.n}"


# Base level nodes:
on  = Node(0, None, None, None, None, 1, 1)
off = Node(0, None, None, None, None, 0, 0)


class CellGrid:
    DEFAULT_LIVE_PROBABILITY = 25  # 25%

    def __init__(self, x, y, all_live=False):
        self.x = x
        self.y = y
        # self.grid = self.init_cell_grid(x, y, all_live)
        # self.updateBuffer = [
        #     [
        #         0, 0, 0, 1, 0, 0, 0, 0, 0
        #     ], 
        #     [
        #         0, 0, 1, 1, 0, 0, 0, 0, 0
        #     ]
        # ]
    

    # def init_cell_grid(self, x, y, all_live):
    #     if not all_live:
    #         return np.zeros((x,y), dtype=np.uint8)
    #     else:
    #         return np.ones((x,y), dtype=np.uint8)
    

    # def get_live_neighbors(self):
    #     pad_top             = np.pad(self.grid, ((2,0), (1,1)))
    #     pad_top_right       = np.pad(self.grid, ((2,0), (0,2)))
    #     pad_right           = np.pad(self.grid, ((1,1), (0,2)))
    #     pad_bottom_right    = np.pad(self.grid, ((0,2), (0,2)))
    #     pad_bottom          = np.pad(self.grid, ((0,2), (1,1)))
    #     pad_bottom_left     = np.pad(self.grid, ((0,2), (2,0)))
    #     pad_left            = np.pad(self.grid, ((1,1), (2,0)))
    #     pad_top_left        = np.pad(self.grid, ((2,0), (2,0)))

    #     return (pad_top + pad_top_right + pad_right + \
    #             pad_bottom_right + pad_bottom + pad_bottom_left + \
    #             pad_left + pad_top_left)[1:-1, 1:-1]  # Unpad result


    @lru_cache(maxsize=2**24)
    def join(self, a, b, c, d):
        n = a.n + b.n + c.n + d.n
        nhash = (
            a.k + 2 +
            + 5131830419411 * a.hash + 3758991985019 * b.hash
            + 8973110871315 * c.hash + 4318490180473 * d.hash
        ) & ((1 << 63) - 1)
        return Node(a.k + 1, a, b, c, d, n, nhash)


    @lru_cache(maxsize=1024)
    def get_zero(self, k):
        return off if k==0 else self.join(self.get_zero(k-1), self.get_zero(k-1),
                                          self.get_zero(k-1), self.get_zero(k-1))


    def center(self, m):
        z = self.get_zero(m.k - 1)
        return self.join(
            self.join(z, z, z, m.a), self.join(z, z, m.b, z),
            self.join(z, m.c, z, z), self.join(m.d, z, z, z)
        )


    # Life rule for 3x3 collection of cells; E is the center:
    def life(self, a, b, c, d, E, f, g, h, i):
        outer = sum(t.n for t in [a, b, c, d, f, g, h, i]])
        return on if (E.n and outer == 2) or outer == 3 else off


    def life_4x4(self, m):
        ad = life(m.a.a, m.a.b, m.b.a, m.a.c, m.a.d, m.b.c, m.c.a, m.c.b, m.d.a)
        bc = life(m.a.b, m.b.a, m.b.b, m.a.d, m.b.c, m.b.d, m.c.b, m.d.a, m.d.b)
        cb = life(m.a.c, m.a.d, m.b.c, m.c.a, m.c.b, m.d.a, m.c.c, m.c.d, m.d.c)
        da = life(m.a.d, m.b.c, m.b.d, m.c.b, m.d.a, m.d.b, m.c.d, m.c.d, m.d.d)
        return self.join(ab, bc, cb, da)
    

    @lru_cache(maxsize=2**24)
    def successor(self, m, j=None):
        """Return the 2**k-1 x 2**k-1 successor, 2**j generations in the future"""
        if m.n == 0:  # Empty
            return m.a
        elif m.k == 2:  # Base case
            s = self.life_4x4(m)
        else:
            j = m.k - 2 if j is None else min(j, m.k - 2)
            c1 = successor(join(m.a.a, m.a.b, m.a.c, m.a.d), j)
            c2 = successor(join(m.a.b, m.b.a, m.a.d, m.b.c), j)
            c3 = successor(join(m.b.a, m.b.b, m.b.c, m.b.d), j)
            c4 = successor(join(m.a.c, m.a.d, m.c.a, m.c.b), j)
            c5 = successor(join(m.a.d, m.b.c, m.c.b, m.d.a), j)
            c6 = successor(join(m.b.c, m.b.d, m.d.a, m.d.b), j)
            c7 = successor(join(m.c.a, m.c.b, m.c.c, m.c.d), j)
            c8 = successor(join(m.c.b, m.d.a, m.c.d, m.d.c), j)
            c9 = successor(join(m.d.a, m.d.b, m.d.c, m.d.d), j)

            if j < m.k - 2:
                s = join(
                    (join(c1.d, c2.c, c4.b, c5.a)),
                    (join(c2.d, c3.c, c5.b, c6.a)),
                    (join(c4.d, c5.c, c7.b, c8.a)),
                    (join(c5.d, c6.c, c8.b, c9.a)),
                )
            else:
                s = join(
                    successor(join(c1, c2, c4, c5), j),
                    successor(join(c2, c3, c5, c6), j),
                    successor(join(c4, c5, c7, c8), j),
                    successor(join(c5, c6, c8, c9), j),
                )
                
        return s


    # From: https://johnhw.github.io/hashlife/index.md.html
    def update(self):


    # def reset(self):
    #     for x in range(self.x):
    #         for y in range(self.y):
    #             self.grid[x][y] = 0


    # def randomize(self):
    #     self.reset()
    #     for x in range(self.x):
    #         for y in range(self.y):
    #             r = int(random()*100)
    #             if r <= CellGrid.DEFAULT_LIVE_PROBABILITY:
    #                 self.grid[x][y] = 1