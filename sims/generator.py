from typing import Callable, List
import eel

from sims.river_rg import generate_river

GRID_WIDTH = 50
GRID_HEIGHT = 50

ROAD_GENERATION_ALGORITHMS = {}

SELECTED_ROAD_GENERATION_ALGORITHM = None

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
    grid = ROAD_GENERATION_ALGORITHMS[SELECTED_ROAD_GENERATION_ALGORITHM](GRID_WIDTH, GRID_HEIGHT)
    grid = generate_river(grid, GRID_WIDTH, GRID_HEIGHT)

    return grid

def sync_rg_to_front():
    algorithms = list(ROAD_GENERATION_ALGORITHMS.keys())
    print(f'Syncing rg algorithms to front: {algorithms}.')
    eel.registerRoadGenerationAlgorithms(algorithms)