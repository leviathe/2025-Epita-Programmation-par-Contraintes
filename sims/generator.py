from typing import Callable, List
import sims.z3_solver as z3_solver
import eel

from sims.options import Opt, get
from sims.river_rg import generate_river

ROAD_GENERATION_ALGORITHMS = {}

"""
Function to register road generation algorithms.

@param algo_name: Name of the algorithm (ex: Voronoi).
@param func: The function that takes the grid width and height and returns the grid with the generated roads.
"""
def register_road_generation_func(algo_name : str, func : Callable[[int, int], list[list[int]]]):
    global ROAD_GENERATION_ALGORITHMS
    ROAD_GENERATION_ALGORITHMS[algo_name] = func

@eel.expose
def select_rg(algo_name):
    global SELECTED_ROAD_GENERATION_ALGORITHM

    if not algo_name in ROAD_GENERATION_ALGORITHMS:
        raise Exception(f'Non-existing road generation algorithm: {algo_name}.')

    SELECTED_ROAD_GENERATION_ALGORITHM = algo_name

    print(f'Road generation algorithm changed to : {algo_name}.')

@eel.expose
def generate():
    generated = ROAD_GENERATION_ALGORITHMS[get(Opt.ROAD_GENERATION_ALGORITHM)]()
    
    if get(Opt.GENERATE_RIVERS):
        generated = generate_river(generated)

    # grid = z3_solver.solve(grid)
    return generated