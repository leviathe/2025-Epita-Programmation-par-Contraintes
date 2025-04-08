from typing import Callable, List, Tuple
import eel
import random

from sims.options import Opt, get
from sims.river_rg import generate_river

ROAD_GENERATION_ALGORITHMS = {}
SOLVER_ALGORITHMS = {}

"""
Function to register road generation algorithms.

@param algo_name: Name of the algorithm (ex: Voronoi).
@param func: The function that takes the grid width and height and returns the grid with the generated roads.
"""
def register_road_generation_func(algo_name : str, func : Callable[[], Tuple[bool, list[list[int]]]]):
    global ROAD_GENERATION_ALGORITHMS
    ROAD_GENERATION_ALGORITHMS[algo_name] = func

""" Same as above, for solvers.
"""
def register_solver_func(algo_name : str, func : Callable[[list[list[int]]], Tuple[bool ,list[list[int]]]]):
    global SOLVER_ALGORITHMS
    SOLVER_ALGORITHMS[algo_name] = func

SOLVING_PHRASES = ['Scratching my head', 'Powering up my neurons', 'Doing Harvard-level calculations', 'Loading brain.exe', 'Summoning logic', 'Doing brain yoga', 'Spinning gears', 'Crunching numbers', 'Thinking hard', 'Dialing the cosmos', 'Cracking the enigma', 'Engaging overdrive', 'Firing up logic cores', 'Warming up the IQ', 'Digging deep', 'Slapping together a solution', 'Wrestling with logic', 'Fighting the confusion']

def random_solving_phrase(i):
    return f'(solving) {random.choice(SOLVING_PHRASES)}... (try {i+1}/5)'

@eel.expose
def generate():
    eel.step('Generating roads 🛣️')
    r_generated = ROAD_GENERATION_ALGORITHMS[get(Opt.ROAD_GENERATION_ALGORITHM)]()
    
    if get(Opt.GENERATE_RIVERS):
        eel.step('Generating rivers 🌊')
        r_generated = generate_river(r_generated)

    solver = get(Opt.SOLVER)

    if solver != 'NONE':
        for i in range(5):
            eel.step(random_solving_phrase(i))
            b, generated = SOLVER_ALGORITHMS[solver](r_generated)
            
            if b:
                eel.step(f'Solved 🎉')
                return generated
        eel.step(f'Solving failed (either unsolvable or too complex) 😔')
    else:
        eel.step(f'You did not select a solver, so that\'s what you get 😎')

    # grid = z3_solver.solve(grid)
    return r_generated