from z3 import *
import itertools

from sims.utils import Tile
from sims.options import Opt
from sims.constraints import constraint_enabled, get_required_number_of_houses

import sims.generator as generator    

def solve(grid : list[list[int]]) -> list[list[int]]:
    w, h = len(grid[0]), len(grid)

    # constrained version of the grid
    s_grid = [[Int(f"cell_{y}_{x}") for x in range(w)] for y in range(h)]
    s = Solver()

    fixed_tiles = [ Tile.ROAD, Tile.WATER ]
    buildings_tiles = [ Tile.HOUSE ]
    possible_tiles = [ Tile.NONE ] + buildings_tiles 

    # this basically says which tile can be what in the grid
    for y, x in itertools.product(range(h), range(w)):
        if grid[y][x] in fixed_tiles:
            s.add(s_grid[y][x] == grid[y][x])
        else: s.add(Or([s_grid[y][x] == dt for dt in possible_tiles]))

    nb_houses = get_required_number_of_houses()

    # sets the number of houses there must be in the city
    s.add(Sum([If(s_grid[y][x] == Tile.HOUSE, 1, 0) for y in range(h) for x in range(w)]) == nb_houses)

    def sum_tiles_of_type_in_square_radius(t : Tile, x0, y0, m):
        result = []
        for dy, dx in itertools.product(range(-m, m + 1), range(-m, m + 1)):
            x, y = x0 + dx, y0 + dy
            if 0 <= x < w and 0 <= y < h:
                if abs(dx) + abs(dy) <= m: result.append(If(s_grid[y][x] == t, 1, 0))
        return Sum(result)

    def sum_tiles_of_type_in_line(t: Tile, x0, y0):
        result = []
        for x in range(w): result.append(If(s_grid[y0][x] == t, 1, 0))
        return Sum(result)

    def sum_tiles_of_type_in_column(t: Tile, x0, y0):
        result = []
        for y in range(h): result.append(If(s_grid[y][x0] == t, 1, 0))
        return Sum(result)

    # tile of type 'source' must have at least n_min and at most n_max tiles of type 'in_radius' in a radius of 'rad'
    def constraint_n_select_in_square_radius(source : Tile, n_min : int, n_max : int, rad : int, in_radius : Tile):
        for y, x in itertools.product(range(h), range(w)):
            if grid[y][x] in fixed_tiles: continue
            su = sum_tiles_of_type_in_square_radius(in_radius, x, y, rad)
            s.add(Implies(s_grid[y][x] == source, su >= n_min,  su <= n_max))

    # tile of type 'source' must have at least n_min and at most n_max tiles of type 'in_radius' in a its axises
    def constraint_n_select_in_axis(source : Tile, n_min : int, n_max : int, in_axis : Tile):
        for y, x in itertools.product(range(h), range(w)):
            if grid[y][x] in fixed_tiles: continue
            su_c = sum_tiles_of_type_in_column(in_axis, x, y)
            su_l = sum_tiles_of_type_in_line(in_axis, x, y)
            print(su_c)
            print(su_l)
            s.add(Implies(s_grid[y][x] == source, Or(
                And(su_c >= n_min, su_c <= n_max),
                And(su_l >= n_min, su_l <= n_max)
            )))

    if constraint_enabled(Opt.BUILDINGS_NEXT_TO_AT_LEAST_A_ROAD):
        constraint_n_select_in_axis(Tile.HOUSE, 1, 1, Tile.ROAD)

    print('yup')

    '''
    if constraint_enabled(Opt.BUILDINGS_NEXT_TO_AT_LEAST_A_ROAD):
        for y, x in itertools.product(range(h), range(w)):
            if not grid[y][x] in fixed_tiles:
                neighbors = get_neighbors(x, y)
                if neighbors: s.add(Implies(s_grid[y][x] == Tile.HOUSE, Or([n == Tile.ROAD for n in neighbors])))
    '''
                
    if s.check() == sat:
        return [[s.model().evaluate(s_grid[y][x]).as_long() for x in range(w)] for y in range(h)]
    else:
        print('Z3 Unsolvable')
        return grid
    
generator.register_solver_func('Z3', solve)