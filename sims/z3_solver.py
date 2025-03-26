from z3 import *
from sims.utils import Tile

def solve(grid : list[list[int]]) -> list[list[int]]:
    w, h = len(grid[0]), len(grid)

    s_grid = [[Int(f"cell_{y}_{x}") for x in range(w)] for y in range(h)]
    s = Solver()

    for y in range(h):
        for x in range(w):
            if grid[y][x] == Tile.ROAD:
                s.add(s_grid[y][x] == Tile.ROAD)
            else:
                s.add(Or(s_grid[y][x] == Tile.NONE, s_grid[y][x] == Tile.BUILDING))

    buildings = [If(s_grid[y][x] == Tile.BUILDING, 1, 0) for y in range(h) for x in range(w)]
    s.add(Sum(buildings) == 200)

    for y in range(h):
        for x in range(w):
            if grid[y][x] != Tile.ROAD:
                neighbors = []
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        neighbors.append(s_grid[ny][nx])

                if neighbors:
                    s.add(Implies(s_grid[y][x] == Tile.BUILDING, Or([n == Tile.ROAD for n in neighbors])))

    if s.check() == sat:
        m = s.model()
        r_grid = [[m.evaluate(s_grid[y][x]).as_long() for x in range(w)] for y in range(h)]
        return r_grid
    else:
        print('Z3 Unsolvable')
        return grid