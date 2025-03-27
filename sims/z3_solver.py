from z3 import *
import itertools

from sims.utils import Tile
from sims.options import Opt
from sims.constraints import constraint_enabled, get_required_number_of_houses

import sims.generator as generator

def solve(grid : list[list[int]]) -> list[list[int]]:
    w, h = len(grid[0]), len(grid)

    # Constrained version of the grid
    s_grid = [[Int(f"cell_{y}_{x}") for x in range(w)] for y in range(h)]
    s = Solver()

    fixed_tiles = [ Tile.ROAD, Tile.WATER ]
    buildings_tiles = [ Tile.HOUSE ]
    possible_tiles = [ Tile.NONE ] + buildings_tiles 

    # This basically says which tile can be what in the grid
    for y, x in itertools.product(range(h), range(w)):
        if grid[y][x] in fixed_tiles:
            s.add(s_grid[y][x] == grid[y][x])
        else: s.add(Or([s_grid[y][x] == dt for dt in possible_tiles]))

    nb_houses = get_required_number_of_houses()

    # Sets the number of houses there must be in the city
    s.add(Sum([If(s_grid[y][x] == Tile.HOUSE, 1, 0) for y in range(h) for x in range(w)]) == nb_houses)

    def get_neighbors(x, y):
        neighbors = []
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                neighbors.append(s_grid[ny][nx])
        return neighbors

    if constraint_enabled(Opt.BUILDINGS_NEXT_TO_AT_LEAST_A_ROAD):
        for y, x in itertools.product(range(h), range(w)):
            if not grid[y][x] in fixed_tiles:
                neighbors = get_neighbors(x, y)
                if neighbors: s.add(Implies(s_grid[y][x] == Tile.HOUSE, Or([n == Tile.ROAD for n in neighbors])))

    if s.check() == sat:
        return [[s.model().evaluate(s_grid[y][x]).as_long() for x in range(w)] for y in range(h)]
    else:
        print('Z3 Unsolvable')
        return grid
    
generator.register_solver_func('Z3', solve)