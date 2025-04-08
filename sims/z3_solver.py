from z3 import *
import itertools
from typing import Tuple

from sims.utils import Tile
from sims.options import Opt
from sims.constraints import constraint_enabled, get_required_number_of_houses, get_required_number_of_hospitals, get_number_of_houses_required_near_hospital

import sims.generator as generator    

z3.set_param("timeout", 5000)

def get_neighbors_pos(x, y, w, h):              
    neigh = []
    for (x0, y0) in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if x0 >= 0 and x0 < w and y0 >= 0 and y0 < h:
            neigh.append((x0,y0))
    return neigh

def get_neighbors_tiles(grid: list[list[int]], x, y, w, h):
    return [grid[y0][x0] for (x0, y0) in get_neighbors_pos(x, y, w, h)]

def has_neighboring_tile(grid: list[list[int]], x, y, tile : Tile, w, h):
    return tile in get_neighbors_tiles(grid, x, y, w, h) 

def get_non_fixed_positions(grid : list[list[int]], w, h, fixed_tiles : list[Tile]):
    non_fixed = []
    for y, x in itertools.product(range(h), range(w)):
        if not grid[y][x] in fixed_tiles:
            non_fixed.append((x, y))
    return non_fixed

def get_non_fixed_positions_next_to_roads(grid : list[list[int]], w, h, non_fixed):
    next_to_road = []
    for x, y in non_fixed:
        if has_neighboring_tile(grid, x, y, Tile.ROAD, w, h):
            next_to_road.append((x, y))
    return next_to_road

def solve(grid : list[list[int]]) -> Tuple[bool, list[list[int]]]:
    w, h = len(grid[0]), len(grid)

    # constrained version of the grid
    s_grid = [[BitVec(f"cell_{y}_{x}", 3) for x in range(w)] for y in range(h)]
    s = Solver()

    fixed_tiles = [ Tile.ROAD, Tile.WATER ]
    buildings_tiles = [ Tile.HOUSE, Tile.HOSPITAL ]
    possible_tiles = [ Tile.NONE ] + buildings_tiles
    all_tiles = possible_tiles + fixed_tiles

    non_fixed = get_non_fixed_positions(grid, w, h, fixed_tiles)
    next_to_road = get_non_fixed_positions_next_to_roads(grid, w, h, non_fixed)

    def get_possible_pos():
        if Opt.BUILDINGS_NEXT_TO_AT_LEAST_A_ROAD:
            return next_to_road
        else:
            return non_fixed

    print(get_possible_pos())

    # this basically says which tile can be what in the grid
    for y, x in itertools.product(range(h), range(w)):
        if not (x,y) in get_possible_pos():
            s.add(s_grid[y][x] == BitVecVal(grid[y][x], 3))
        else:
            s.add(Or([s_grid[y][x] == BitVecVal(dt, 3) for dt in possible_tiles]))

    nb_houses = get_required_number_of_houses()
    nb_hospitals = get_required_number_of_hospitals()

    print(f'There must be {nb_houses} houses on the grid.')
    print(f'There must be {nb_hospitals} hospitals on the grid.')

    # sets the number of houses there must be in the city
    s.add(Sum([If(s_grid[y][x] == BitVecVal(Tile.HOUSE, 3), 1, 0) for y in range(h) for x in range(w)]) == nb_houses)

    # sets the number of hopitals there must be in the city
    s.add(Sum([If(s_grid[y][x] == BitVecVal(Tile.HOSPITAL, 3), 1, 0) for y in range(h) for x in range(w)]) == nb_hospitals)

    def cond_tiles_of_type_in_square_radius(t : BitVecVal, x0, y0, rad, nb):
        result = []
        for dy, dx in itertools.product(range(-rad, rad + 1), range(-rad, rad + 1)):
            x, y = x0 + dx, y0 + dy
            if x >= 0 and x < w and y >= 0 and y < h and (x,y) in get_possible_pos():
                result.append((s_grid[y][x] == t, 1))
        return And(PbGe(result, nb), PbLe(result, nb))
    
    def cond_tiles_of_type_in_line(t: BitVecVal, x0, y0, rad, nb):
        result = []
        for x in range(x0 - rad, x0 + rad + 1):
            if x >= 0 and x < w:
                result.append((s_grid[y0][x] == t, 1))
        return And(PbGe(result, nb), PbLe(result, nb))
    
    def cond_tiles_of_type_in_column(t: BitVecVal, x0, y0, rad, nb):
        result = []
        for y in range(y0 - rad, y0 + rad + 1):
            if y >= 0 and y < h and grid[y][x0]:
                result.append((s_grid[y][x0] == t, 1))
        return And(PbGe(result, nb), PbLe(result, nb))

    # tile of type 'source' must have n tiles of type 'in_radius' in a radius of 'rad'
    def constraint_n_select_in_square_radius(source : Tile, n : int, rad : int, in_radius : Tile):
        for x, y in get_possible_pos():
            c = cond_tiles_of_type_in_square_radius(BitVecVal(in_radius, 3), x, y, rad, n)
            s.add(Implies(s_grid[y][x] == BitVecVal(source, 3), c))
            # print(Implies(s_grid[y][x] == BitVecVal(source, 3), c))

    # tile of type 'source' must have at least n_min and at most n_max tiles of type 'in_radius' in a its axises
    def constraint_n_select_in_axis(source : Tile, n : int, in_axis : Tile):
        for x, y in get_possible_pos():
            c_c = cond_tiles_of_type_in_column(BitVecVal(in_axis, 3), x, y, n)
            l_c = cond_tiles_of_type_in_line(BitVecVal(in_axis, 3), x, y, n)
            s.add(Implies(s_grid[y][x] == BitVecVal(source, 3), And(c_c, l_c)))

    if constraint_enabled(Opt.HOSPITALS_NEAR_PATIENTS):
        n = get_number_of_houses_required_near_hospital()
        print(f'Hospitals must have {n} houses around them in a radius of 3.')
        constraint_n_select_in_square_radius(Tile.HOSPITAL, n, 3, Tile.HOUSE)
    
    print('Checking satisfiability (solving constraints)...')
    if s.check() == sat:
        print('Solved.', flush=True)
        return True, [[s.model().evaluate(s_grid[y][x]).as_long() for x in range(w)] for y in range(h)]
    else:
        print('Z3 could not find a solution.')
        return False, None
    
generator.register_solver_func('Z3', solve)