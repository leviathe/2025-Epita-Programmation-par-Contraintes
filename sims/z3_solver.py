from z3 import *
import itertools
from functools import lru_cache

from sims.utils import Tile
from sims.options import Opt
from sims.constraints import constraint_enabled, get_required_number_of_houses, get_required_number_of_hospitals, get_number_of_houses_required_near_hospital

import sims.generator as generator    

def solve(grid : list[list[int]]) -> list[list[int]]:
    w, h = len(grid[0]), len(grid)

    # constrained version of the grid
    s_grid = [[BitVec(f"cell_{y}_{x}", 3) for x in range(w)] for y in range(h)]
    s = Solver()

    fixed_tiles = [ Tile.ROAD, Tile.WATER ]
    buildings_tiles = [ Tile.HOUSE, Tile.HOSPITAL ]
    possible_tiles = [ Tile.NONE ] + buildings_tiles
    all_tiles = possible_tiles + fixed_tiles

    # this basically says which tile can be what in the grid
    for y, x in itertools.product(range(h), range(w)):
        if grid[y][x] in fixed_tiles:
            s.add(s_grid[y][x] == BitVecVal(grid[y][x], 3))
        else: s.add(Or([s_grid[y][x] == BitVecVal(dt, 3) for dt in possible_tiles]))

    nb_houses = get_required_number_of_houses()
    nb_hospitals = get_required_number_of_hospitals()

    # sets the number of houses there must be in the city
    s.add(Sum([If(s_grid[y][x] == BitVecVal(Tile.HOUSE, 3), 1, 0) for y in range(h) for x in range(w)]) == nb_houses)

    # sets the number of hopitals there must be in the city
    s.add(Sum([If(s_grid[y][x] == BitVecVal(Tile.HOSPITAL, 3), 1, 0) for y in range(h) for x in range(w)]) == nb_hospitals)

    def cond_tiles_of_type_in_square_radius(t : Tile, x0, y0, m, nb):
        result = []
        for dy, dx in itertools.product(range(-m, m + 1), range(-m, m + 1)):
            x, y = x0 + dx, y0 + dy
            if 0 <= x < w and 0 <= y < h:
                if abs(dx) + abs(dy) <= m: result.append((s_grid[y][x] == BitVecVal(t, 3), 1))
        return PbEq(result, nb)
    
    def cond_tiles_of_type_in_line(t: Tile, x0, y0, rad, nb):
        result = []
        for x in range(x0 - rad, x0 + rad + 1):
            if x >= 0 and x < w: result.append((s_grid[y0][x] == BitVecVal(t, 3), 1))
        return PbEq(result, nb)

    def cond_tiles_of_type_in_column(t: Tile, x0, y0, rad, nb):
        result = []
        for y in range(y0 - rad, y0 + rad + 1):
            if y >= 0 and y < h: result.append((s_grid[y][x0] == BitVecVal(t, 3), 1))
        return PbEq(result, nb)

    # tile of type 'source' must have at least n_min and at most n_max tiles of type 'in_radius' in a radius of 'rad'
    def constraint_n_select_in_square_radius(source : Tile, n : int, rad : int, in_radius : Tile):
        for y, x in itertools.product(range(h), range(w)):
            if grid[y][x] in fixed_tiles: continue
            c = cond_tiles_of_type_in_square_radius(in_radius, x, y, rad, n)
            s.add(Implies(s_grid[y][x] == source, c))

    # tile of type 'source' must have at least n_min and at most n_max tiles of type 'in_radius' in a its axises
    def constraint_n_select_in_axis(source : Tile, n : int, in_axis : Tile):
        for y, x in itertools.product(range(h), range(w)):
            if grid[y][x] in fixed_tiles: continue
            c_c = cond_tiles_of_type_in_column(in_axis, x, y, n)
            l_c = cond_tiles_of_type_in_line(in_axis, x, y, n)
            s.add(Implies(s_grid[y][x] == source, c_c, l_c))

    if constraint_enabled(Opt.BUILDINGS_NEXT_TO_AT_LEAST_A_ROAD):
        for t in buildings_tiles:
            constraint_n_select_in_square_radius(t, 1, 1, Tile.ROAD)

    if constraint_enabled(Opt.HOSPITALS_NEAR_PATIENTS):
        n = get_number_of_houses_required_near_hospital()
        constraint_n_select_in_square_radius(Tile.HOSPITAL, n, 3, Tile.HOUSE)
                
    if s.check() == sat:
        return [[s.model().evaluate(s_grid[y][x]).as_long() for x in range(w)] for y in range(h)]
    else:
        print('Z3 Unsolvable')
        return grid
    
generator.register_solver_func('Z3', solve)
