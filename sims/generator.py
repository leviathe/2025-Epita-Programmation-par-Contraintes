from typing import Callable, List
import eel

GRID_WIDTH = 50
GRID_HEIGHT = 50

ROAD_GENERATION_ALGORITHMS = {}

SELECTED_ROAD_GENERATION_ALGORITHM = 'Labyrinth'

"""
Function to register road generation algorithms.

@param algo_name: Name of the algorithm (ex: Voronoi).
@param func: The function that takes the grid width and height and returns the grid with the generated roads.
"""
def register_road_generation_func(algo_name : str, func : Callable[[int, int], list[list[int]]]):
    global ROAD_GENERATION_ALGORITHMS
    ROAD_GENERATION_ALGORITHMS[algo_name] = func

@eel.expose
def generate():
    return ROAD_GENERATION_ALGORITHMS[SELECTED_ROAD_GENERATION_ALGORITHM](GRID_WIDTH, GRID_HEIGHT)