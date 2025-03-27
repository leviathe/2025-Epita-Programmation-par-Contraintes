from typing import Callable, List
import eel

from sims.options import Opt, get
from sims.river_rg import generate_river

ROAD_GENERATION_ALGORITHMS = {}
SOLVER_ALGORITHMS = {}

"""
Function to register road generation algorithms.

@param algo_name: Name of the algorithm (ex: Voronoi).
@param func: The function that takes the grid width and height and returns the grid with the generated roads.
"""
def register_road_generation_func(algo_name : str, func : Callable[[], list[list[int]]]):
    global ROAD_GENERATION_ALGORITHMS
    ROAD_GENERATION_ALGORITHMS[algo_name] = func

""" Same as above, for solvers.
"""
def register_solver_func(algo_name : str, func : Callable[[list[list[int]]], list[list[int]]]):
    global SOLVER_ALGORITHMS
    SOLVER_ALGORITHMS[algo_name] = func

@eel.expose
def generate():
    generated = ROAD_GENERATION_ALGORITHMS[get(Opt.ROAD_GENERATION_ALGORITHM)]()
    
    if get(Opt.GENERATE_RIVERS):
        generated = generate_river(generated)

    solver = get(Opt.SOLVER)

    if solver != 'NONE':
        generated = SOLVER_ALGORITHMS[solver](generated)

    # grid = z3_solver.solve(grid)
    return generated